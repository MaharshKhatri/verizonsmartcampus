"""Pocket PROVE tap: turn one recorded alarm test call into the receipt's ALARM line.

Phase 1 needs no firmware. A technician clips a small Raspberry Pi with a
passive, isolated line tap onto the box's alarm (phone) port and records one
test call as mono audio. On a 2-wire line both directions are mixed, so the
recording holds the panel's DTMF and the receiver's tones in one track:

  dial tone, dialling -> ringback or silence -> handshake (1400 then 2300 Hz)
  -> Contact ID block (16 DTMF digits), resent up to 4 times -> kiss-off (1400 Hz)

`analyse_call` walks that recording in time order with the Goertzel and tone
detectors from alarm.py and says whether the receiver picked up, whether a
full code with a good checksum went out, and whether a kiss-off confirmed it.

What a tap on the box's phone port can and cannot see: it hears the panel's
digits BEFORE the radio leg, so "code garbled" there means the panel or the
house wiring mangled them. Loss on the radio leg shows up only as resends and a
missing kiss-off. The kiss-off is the one end-to-end signal, and it means "the
receiver accepted a block", not "someone acted on the alarm". `synth_call`
applies its frame loss before the tap, which matches a second tap at the
receiver end (the bench's dual taps) or a fault on the house side.

    python3 -m prototype.prove.tap call.wav     # JSON for one recording
    python3 -m prototype.prove.tap --demo       # three synthetic calls
    python3 -m prototype.prove.tap --budget     # on-box CPU/RAM estimate
"""
import wave

import numpy as np

from . import alarm
from .acoustic import _lowpass

FS = alarm.FS
DIAL = "2015550123"          # fictional 555-01xx receiver number the synthetic panel dials
RETRY_WAIT_S = 1.25          # Contact ID: the panel resends if no kiss-off comes within 1.25 s
MAX_ATTEMPTS = 4             # blocks a panel sends per call before it hangs up
FAR_GAIN = 0.6               # the receiver's tones reach the tap quieter than the panel's own digits
LEVEL = 0.3                  # recordings are scaled so their loud frames sit near this RMS
MIN_RMS = 0.01               # quieter frames count as silence (about 30 dB under LEVEL)
BLOCK_GAP_S = 0.6            # silence that separates two blocks (digits in a block are 55 ms apart)
KISSOFF_MIN_S = 0.4          # same kiss-off rule as alarm.alarm_call


def _frames(x, n, hop):
    """Frame starts and an (frames x n) matrix, using the same walk as alarm.decode_dtmf."""
    starts = np.arange(0, len(x) - n, hop)
    return starts, x[starts[:, None] + np.arange(n)]


def goertzel_power(frames, freqs):
    """Goertzel power of every frame at every frequency at once (the same numbers as alarm._goertzel)."""
    w = np.exp(-2j * np.pi * np.outer(np.arange(frames.shape[1]), freqs) / FS)
    return np.abs(frames @ w) ** 2


def _runs(mask):
    """(first, last + 1) index pairs of each run of True."""
    d = np.diff(np.concatenate([[0], np.asarray(mask, int), [0]]))
    return list(zip(np.flatnonzero(d == 1), np.flatnonzero(d == -1)))


def _cut(x, a, b):
    return x[max(0, int(a * FS)):max(0, int(b * FS))]


def _dtmf_labels(x, frame=0.025, hop=0.0125, min_rms=0.02):
    """DTMF key heard in each hop ('' for none), by alarm.decode_dtmf's rules: dominance, twist, level."""
    n, h = int(frame * FS), int(hop * FS)
    starts, F = _frames(x, n, h)
    if not len(starts):
        return starts, np.array([], dtype="<U1")
    pr, pc = goertzel_power(F, alarm.ROWS), goertzel_power(F, alarm.COLS)
    r, c, i = pr.argmax(1), pc.argmax(1), np.arange(len(starts))
    p = np.mean(F * F, 1)
    dominant = (pr[i, r] + pc[i, c]) / (n * n / 4) / (2 * (p + 1e-12)) > 0.6
    twist = pr[i, r] / (pc[i, c] + 1e-12)
    ok = (np.sqrt(p) > min_rms) & dominant & (twist > 0.25) & (twist < 4.0)
    return starts, np.array([alarm.KEYS[a][b] if k else "" for a, b, k in zip(r, c, ok)])


def dtmf_events(x, min_rms=0.02):
    """Digits with their start times (s): alarm.decode_dtmf's two-hops-per-digit rule, vectorised."""
    starts, keys = _dtmf_labels(x, min_rms=min_rms)
    h = int(0.0125 * FS)
    out, last, run = [], None, 0
    for s, k in zip(starts, keys):
        k = k or None
        if k == last:
            run += 1
        else:
            last, run = k, 1
        if k is not None and run == 2:
            out.append((k, (s - h) / FS))
    return out


def decode_dtmf_fast(x, min_rms=0.02):
    """Same output as alarm.decode_dtmf, about 50 times faster (used for sweeps and the receiver model)."""
    return "".join(k for k, _ in dtmf_events(x, min_rms))


def _tone_runs(x, f, frame=0.02, hop=0.01):
    """(start_s, end_s) of each stretch where frequency f carries most of the power (alarm.detect_tone's test)."""
    n, h = int(frame * FS), int(hop * FS)
    starts, F = _frames(x, n, h)
    if not len(starts):
        return []
    p = np.mean(F * F, 1) + 1e-12
    on = (np.sqrt(p) > MIN_RMS) & (goertzel_power(F, [f])[:, 0] / (n * n / 4) / (2 * p) > 0.6)
    return [(starts[a] / FS, (starts[b - 1] + n) / FS) for a, b in _runs(on)]


def _level(x):
    """Remove DC and scale so the loud frames sit near LEVEL; a tap's recording level is arbitrary."""
    x = x - np.mean(x) if len(x) else x
    _, F = _frames(x, int(0.02 * FS), int(0.01 * FS))
    ref = np.percentile(np.sqrt(np.mean(F * F, 1)), 99) if len(F) else 0.0
    gain = LEVEL / ref if ref > 1e-6 else 1.0
    return x * gain, gain


def _handshake(x, t1400, t2300):
    """First 1400 Hz burst (about 100 ms) followed by 2300 Hz; checked again with alarm.detect_tone."""
    for a, b in t1400:
        if not 0.05 <= b - a <= 0.35:
            continue
        for c, d in t2300:
            if b - 0.03 <= c <= b + 0.4 and d - c >= 0.05:
                w = _cut(x, a - 0.03, d + 0.03)
                if alarm.detect_tone(w, 1400, 0.06, MIN_RMS) and alarm.detect_tone(w, 2300, 0.06, MIN_RMS):
                    return a, d
    return None


def _blocks(x, after_s, tones):
    """Contact ID blocks after the handshake: active stretches that are not handshake/kiss-off tones."""
    n, h = int(0.02 * FS), int(0.01 * FS)
    starts, F = _frames(x, n, h)
    t = starts / FS
    active = (np.sqrt(np.mean(F * F, 1)) > MIN_RMS) & (t >= after_s)
    for a, b in tones:                                   # keep the receiver's tones (and their edges) out
        active &= ~((t + n / FS > a - 0.03) & (t < b + 0.03))
    segs = []
    for i, j in _runs(active):
        s, e = t[i], t[j - 1] + n / FS
        if segs and s - segs[-1][1] < BLOCK_GAP_S:      # a lost digit or two does not split a block
            segs[-1][1] = e
        else:
            segs.append([s, e])
    out = []
    for s, e in segs:
        seg = _cut(x, s - 0.03, e + 0.03)
        if np.count_nonzero(_dtmf_labels(seg, min_rms=MIN_RMS)[1]) < 3:
            continue                                     # a click or a noise burst, not digits
        digits = alarm.decode_dtmf(seg, min_rms=MIN_RMS)
        out.append({"digits": digits, "checksum_ok": alarm.checksum_ok(digits),
                    "start_s": round(float(s), 2), "end_s": round(float(e), 2)})
    return out


def _receipt(r):
    n = len(r["blocks"])
    if r["verdict"] == "OK":
        return f"Receiver picked up · full code sent · confirmed in {r['confirm_s']:.1f} s"
    if r["verdict"] == "NO ANSWER":
        return "No receiver pickup (no handshake heard) · no code sent · no confirmation"
    if r["verdict"] == "NO CONFIRMATION":
        return f"Receiver picked up · full code sent · no confirmation after {n} attempt{'s' * (n != 1)}"
    if n == 0:
        return "Receiver picked up · no code heard · no confirmation"
    bad = sum(not b["checksum_ok"] for b in r["blocks"])
    tail = "kiss-off heard, but not after a valid code" if r["kissoff_heard"] else "no confirmation"
    return f"Receiver picked up · code garbled (checksum failed {bad}/{n}) · {tail}"


def analyse_call(signal, fs=FS):
    """Walk one recorded call in time order: handshake -> Contact ID block(s) -> kiss-off.

    Returns the evidence (times in seconds from the start of the recording), a
    verdict in {OK, NO ANSWER, CODE GARBLED, NO CONFIRMATION} and receipt_line.
    confirm_s runs from the start of the handshake to the start of the kiss-off;
    attempts counts the blocks sent up to the confirmed one (all of them if none).
    """
    x, gain = _level(resample(np.asarray(signal, float), fs))
    t1400, t2300 = _tone_runs(x, 1400), _tone_runs(x, 2300)
    hs = _handshake(x, t1400, t2300)
    r = {"picked_up": hs is not None, "handshake_at_s": None, "dialled_digits": "", "blocks": [],
         "full_code_sent": False, "confirmed": False, "confirm_s": None, "attempts": 0,
         "kissoff_heard": False, "duration_s": round(len(x) / FS, 2), "level_gain_db": round(float(20 * np.log10(gain)), 1)}
    r["dialled_digits"] = decode_dtmf_fast(_cut(x, 0, hs[0]) if hs else x, MIN_RMS)
    if hs:
        t0, t_end = hs
        r["handshake_at_s"] = round(float(t0), 2)
        kos = [a for a, b in t1400 if a >= t_end and b - a >= KISSOFF_MIN_S
               and alarm.detect_tone(_cut(x, a - 0.02, b + 0.02), 1400, KISSOFF_MIN_S, MIN_RMS)]
        r["blocks"] = _blocks(x, t_end, t1400 + t2300)
        r["kissoff_heard"] = bool(kos)
        r["full_code_sent"] = any(b["checksum_ok"] for b in r["blocks"])
        valid_ends = [b["end_s"] for b in r["blocks"] if b["checksum_ok"]]
        ko = next((a for a in kos if valid_ends and a >= min(valid_ends) - 0.05), None)
        r["confirmed"] = ko is not None
        if ko is not None:
            r["confirm_s"] = round(float(ko - t0), 2)
            r["attempts"] = int(sum(b["start_s"] < ko for b in r["blocks"]))
        else:
            r["attempts"] = len(r["blocks"])
    r["verdict"] = ("NO ANSWER" if not r["picked_up"] else "CODE GARBLED" if not r["full_code_sent"]
                    else "NO CONFIRMATION" if not r["confirmed"] else "OK")
    r["receipt_line"] = _receipt(r)
    return r


def synth_call(rng, loss=0.0, receiver_up=True, kissoff_ok=True, attempts=MAX_ATTEMPTS, gap_s=0.25, noise=0.002):
    """A whole alarm test call as the tap records it (both directions mixed), at alarm.FS.

    The panel hears dial tone, dials, hears ringback or silence, then the
    receiver's handshake. It sends its Contact ID block and resends it, up to
    `attempts` times, until a kiss-off comes. `loss` is voice_path-style frame
    loss on the panel -> receiver block. The receiver kisses off only if its own
    decode of that block passes the checksum (and `kissoff_ok`). The tap adds a
    little white noise (`noise`) and 60 Hz hum.
    """
    msg = alarm.contact_id()

    def z(s):
        return np.zeros(int(s * FS))

    def far(s):                                        # receiver -> panel: telephone channel, quieter at the tap
        return FAR_GAIN * alarm.alarm_path(s, rng)

    parts = [z(rng.uniform(0.3, 0.6)), alarm._tone((350, 440), 0.6, 0.1), z(0.15), alarm.dtmf(DIAL), z(0.3)]
    if not receiver_up:
        parts += [alarm._tone((440, 480), 2.0, 0.08), z(4.0)] * 2   # rings twice, then the panel gives up
    else:
        if rng.random() < 0.5:
            parts += [alarm._tone((440, 480), 2.0, 0.08), z(rng.uniform(0.3, 1.0))]
        else:
            parts += [z(rng.uniform(1.0, 2.5))]
        parts += [far(alarm.handshake())]
        for a in range(attempts):
            heard = alarm.voice_path(alarm.dtmf(msg), rng, snr_db=24.0, level_jitter_db=1.0, onset_clip=0.3, loss=loss)
            parts += [z(gap_s if a == 0 else RETRY_WAIT_S), heard]
            if kissoff_ok and alarm.checksum_ok(alarm.decode_dtmf(heard)):
                parts += [z(gap_s), far(alarm.kissoff())]
                break
        else:
            parts += [z(RETRY_WAIT_S)]                   # waited for a kiss-off that never came
    parts += [z(rng.uniform(0.2, 0.5))]
    x = np.concatenate(parts)
    t = np.arange(len(x)) / FS
    return x + 2 * noise * np.sin(2 * np.pi * 60 * t) + rng.normal(0, noise, len(x))


def resample(x, fs, to=FS):
    """Linear-interpolation resampler, numpy only; low-passes first when the rate goes down."""
    x = np.asarray(x, float)
    if int(fs) == int(to) or not len(x):
        return x
    if fs > to:
        x = _lowpass(x, 0.45 * to, fs)                   # anti-alias before decimating
    n = int(round(len(x) * to / fs))
    return np.interp(np.arange(n) / to, np.arange(len(x)) / fs, x)


def read_wav(path):
    """16-bit PCM WAV (mono or stereo, any rate) -> mono float array at alarm.FS."""
    with wave.open(str(path), "rb") as w:
        if w.getsampwidth() != 2:
            raise ValueError(f"{path}: need 16-bit PCM, got {8 * w.getsampwidth()}-bit")
        ch, fs, raw = w.getnchannels(), w.getframerate(), w.readframes(w.getnframes())
    x = np.frombuffer(raw, "<i2").astype(float) / 32768
    if ch > 1:
        x = x[:len(x) // ch * ch].reshape(-1, ch).mean(1)   # 2-wire tap: mix both channels
    return resample(x, fs)


def write_wav(path, x, fs=FS):
    """Mono float array -> 16-bit PCM WAV (clipped to full scale)."""
    pcm = np.round(np.clip(np.asarray(x, float), -1.0, 32767 / 32768) * 32768).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(int(fs))
        w.writeframes(pcm.tobytes())


def compute_budget(fs=FS, dtmf_frame=0.025, dtmf_hop=0.0125, tone_frame=0.02, call_s=20.0):
    """Analytic CPU and RAM estimate for running these detectors on the box's own DSP.

    Streaming Goertzel: per tone per sample, s = x + k*s1 - s2, i.e. one
    multiply-accumulate (MAC) and one subtract. DTMF frames overlap (25 ms every
    12.5 ms), so each sample feeds two DTMF frames; the 1400 and 2300 Hz
    detectors use back-to-back 20 ms frames. Each frame also needs its energy
    (1 MAC per sample) and, at its end, 3 multiplies + 2 adds per tone and about
    20 operations of decisions (dominance, twist, run counting).
    """
    n_dtmf, n_tone = len(alarm.ROWS) + len(alarm.COLS), 2
    overlap = dtmf_frame / dtmf_hop
    dtmf_fps, tone_fps = 1 / dtmf_hop, 1 / tone_frame
    mac_per_sample = n_dtmf * overlap + n_tone + (overlap + 1)          # Goertzel loops + frame energy
    sample_macs = fs * mac_per_sample
    frame_macs = dtmf_fps * n_dtmf * 3 + tone_fps * n_tone * 3          # power out of each Goertzel
    frame_other = dtmf_fps * (n_dtmf * 2 + 20) + tone_fps * (n_tone * 2 + 10)
    macs = sample_macs + frame_macs
    ops = 2 * macs + fs * (n_dtmf * overlap + n_tone) + frame_other     # MAC = 2 ops, plus the subtracts
    f32 = 4
    working = (2 * int(dtmf_frame * fs) * f32                          # double-buffered input frame
               + 2 * (n_dtmf * overlap + n_tone) * f32                 # Goertzel state (s1, s2)
               + (n_dtmf + n_tone) * f32                               # coefficients
               + MAX_ATTEMPTS * (16 + 4) + 64)                          # digit log with start times
    audio = call_s * fs * 2                                             # optional PCM16 copy of the call
    return {"tones": n_dtmf + n_tone, "fs_hz": fs, "goertzel_mac_per_tone_per_sample": 1,
            "mac_per_sample": round(mac_per_sample, 1),
            "mmac_per_s": round(macs / 1e6, 3), "mops_per_s": round(ops / 1e6, 3),
            "ram_kb_detectors": round(working / 1024, 2),
            "ram_kb_with_call_audio": round((working + audio) / 1024, 1),
            "pct_of_assumed_100_mmacs_dsp": round(100 * macs / 100e6, 2),
            "assumptions": [f"{n_dtmf} DTMF tones on {dtmf_frame * 1e3:.1f} ms frames every {dtmf_hop * 1e3:.1f} ms",
                            f"1400 and 2300 Hz on {tone_frame * 1e3:.0f} ms frames, no overlap",
                            "float32 state; a fixed-point DSP needs similar counts",
                            f"call audio kept for {call_s:.0f} s as PCM16 (optional, for the record)",
                            "100 MMAC/s is an assumed spare budget for scale, not a spec of any Verizon box"],
            "basis": "analytic estimate, not measured on target hardware"}


def demo(seed=11):
    """Three synthetic calls: clean, lossy (code garbled), and a receiver that never kisses off."""
    cases = (("clean", {}), ("lossy", {"loss": 0.4}), ("no_kissoff", {"kissoff_ok": False}))
    return {name: analyse_call(synth_call(np.random.default_rng(seed + i), **kw)) for i, (name, kw) in enumerate(cases)}


if __name__ == "__main__":
    import argparse
    import json
    ap = argparse.ArgumentParser(description="Pocket PROVE tap: analyse one recorded alarm test call.")
    ap.add_argument("wav", nargs="?", help="16-bit PCM WAV recorded on the box's alarm port")
    ap.add_argument("--demo", action="store_true", help="analyse three synthetic calls")
    ap.add_argument("--budget", action="store_true", help="print the on-box CPU/RAM estimate")
    args = ap.parse_args()
    if args.demo:
        print(json.dumps(demo(), indent=1, ensure_ascii=False))
    elif args.budget:
        print(json.dumps(compute_budget(), indent=1))
    elif args.wav:
        print(json.dumps({"file": args.wav, **analyse_call(read_wav(args.wav))}, indent=1, ensure_ascii=False))
    else:
        ap.error("give a WAV file, --demo or --budget")
