"""Kiss-off check: did the alarm actually reach the alarm company?

An alarm panel on a copper replacement dials its central station and sends a
Contact ID message as DTMF tones. The receiver answers with a handshake
(1400 Hz then 2300 Hz) and, only if the message arrived intact, a kiss-off
tone (1400 Hz, about 0.8 s). The panel's keypad can say "sent" either way.
PROVE listens for the kiss-off.

Verizon's Voice Connect / Business Phone Connect (Inseego BPC100) needs the
alarm company's number entered by hand (##21*number#) so the box can treat
those calls as alarm calls; its guide warns "Failure to verify may result in
your alarm not working" (research/sources). Calls to an unregistered number go
through the ordinary voice path.

This module is a model. The registered path is treated as transparent
(telephone band, mu-law). The voice path gets assumed speech-codec impairments
(per-frame level jitter, codec noise, onset clipping by noise suppression,
frame loss). The bench (an Asterisk AlarmReceiver on a real number) replaces
these assumptions with measured rates.
"""
import numpy as np

from .acoustic import FS, _band

ROWS = (697, 770, 852, 941)
COLS = (1209, 1336, 1477, 1633)
KEYS = ("123A", "456B", "789C", "*0#D")
DIGIT_ON, DIGIT_OFF = 0.055, 0.055
# Contact ID hex digit -> DTMF key (data 0 travels as '0' with checksum value 10; E/F use * and #)
HEX_TO_KEY = {**{str(i): str(i) for i in range(10)}, "A": "0", "B": "B", "C": "C", "D": "D", "E": "*", "F": "#"}
KEY_TO_VAL = {**{str(i): i for i in range(1, 10)}, "0": 10, "B": 11, "C": 12, "D": 13, "*": 14, "#": 15}


def contact_id(account="1234", qualifier="1", event="120", group="01", zone="003"):
    """16-digit Contact ID message (ACCT MT Q XYZ GG CCC S) with the mod-15 checksum.

    Event 120 = panic, 110 = fire, 130 = burglary; qualifier 1 = new event.
    """
    body = f"{account}18{qualifier}{event}{group}{zone}"
    total = sum(10 if c == "0" else int(c, 16) for c in body)
    s = (15 - total % 15) or 15
    check = "0" if s == 10 else format(s, "X")
    return "".join(HEX_TO_KEY.get(c, c) for c in body + check)


def checksum_ok(keys):
    return len(keys) == 16 and sum(KEY_TO_VAL.get(k, 99) for k in keys) % 15 == 0


def has_adjacent_repeat(keys):
    """True if two neighbouring DTMF keys are the same (concealment can merge them into one digit)."""
    return any(a == b for a, b in zip(keys, keys[1:]))


TEST_EVENT = {"qualifier": "1", "event": "601", "group": "01", "zone": "012"}   # 601 = manual test report
REPEAT_ACCOUNT, NO_REPEAT_ACCOUNT = "1111", "2468"   # 2468 -> 2468181601010124: no neighbours alike, checksum included


def contact_id_variant(repeated=True):
    """Test-report message (event 601) whose 16 keys do (account 1111) or do not (account 2468) repeat a neighbour."""
    msg = contact_id(REPEAT_ACCOUNT if repeated else NO_REPEAT_ACCOUNT, **TEST_EVENT)
    assert has_adjacent_repeat(msg) == repeated, msg
    return msg


def _tone(freqs, dur, amp=0.35):
    t = np.arange(int(dur * FS)) / FS
    return sum(amp * np.sin(2 * np.pi * f * t) for f in freqs)


def dtmf(keys):
    out = []
    for k in keys:
        r = next(i for i, row in enumerate(KEYS) if k in row)
        c = KEYS[r].index(k)
        out += [_tone((ROWS[r], COLS[c]), DIGIT_ON), np.zeros(int(DIGIT_OFF * FS))]
    return np.concatenate(out)


def handshake():
    return np.concatenate([_tone((1400,), 0.1, 0.5), np.zeros(int(0.1 * FS)), _tone((2300,), 0.1, 0.5)])


def kissoff():
    return _tone((1400,), 0.8, 0.5)


def _goertzel(frame, f):
    k = 2 * np.cos(2 * np.pi * f / FS)
    s1 = s2 = 0.0
    for x in frame:
        s1, s2 = x + k * s1 - s2, s1
    return s1 * s1 + s2 * s2 - k * s1 * s2


def _fraction(frame, freqs):
    """Share of the frame's power carried by the given frequencies (about 1.0 for a clean tone pair)."""
    n = len(frame)
    p = np.mean(frame * frame) + 1e-12
    return sum(_goertzel(frame, f) for f in freqs) / (n * n / 4) / (2 * p)


def decode_dtmf(sig, frame=0.025, hop=0.0125, min_rms=0.02):
    """Goertzel DTMF decoder: tone-pair dominance, twist limit, and two consecutive hops per digit."""
    n, h = int(frame * FS), int(hop * FS)
    seq, last, run = [], None, 0
    for i in range(0, len(sig) - n, h):
        fr = sig[i:i + n]
        key = None
        if np.sqrt(np.mean(fr * fr)) > min_rms:
            pr = [_goertzel(fr, f) for f in ROWS]
            pc = [_goertzel(fr, f) for f in COLS]
            r, c = int(np.argmax(pr)), int(np.argmax(pc))
            dominant = _fraction(fr, (ROWS[r], COLS[c])) > 0.6
            twist_ok = 0.25 < pr[r] / (pc[c] + 1e-12) < 4.0
            if dominant and twist_ok:
                key = KEYS[r][c]
        if key == last:
            run += 1
        else:
            last, run = key, 1
        if key is not None and run == 2:
            seq.append(key)
    return "".join(seq)


def detect_tone(sig, f, min_s, min_rms=0.02):
    """True if frequency f carries most of the power for at least min_s seconds."""
    n = int(0.02 * FS)
    need, run = int(round(min_s / 0.02)), 0
    for i in range(0, len(sig) - n, n):
        fr = sig[i:i + n]
        if np.sqrt(np.mean(fr * fr)) > min_rms and _fraction(fr, (f,)) > 0.6:
            run += 1
            if run >= need:
                return True
        else:
            run = 0
    return False


def ge_mean_loss(p_gb, p_bg, loss=0.0, bad_loss=0.5):
    """Long-run frame-loss rate of a Gilbert-Elliott channel: time share of each state times its loss."""
    pi_bad = p_gb / (p_gb + p_bg) if p_gb + p_bg else 0.0
    return (1 - pi_bad) * loss + pi_bad * bad_loss


def gilbert_elliott(n, rng, p_gb, p_bg, loss=0.0, bad_loss=0.5):
    """n frames of two-state bursty loss (True = lost), starting from the stationary state mix.

    p_gb, p_bg: per-frame chance of good->bad and bad->good (mean bad stay 1/p_bg frames);
    a frame is lost with chance `loss` in the good state and `bad_loss` in the bad one.
    """
    move = rng.random(n)
    b = rng.random() < (p_gb / (p_gb + p_bg) if p_gb + p_bg else 0.0)
    bad = np.empty(n, bool)
    for i in range(n):
        bad[i] = b
        b = move[i] >= p_bg if b else move[i] < p_gb
    return rng.random(n) < np.where(bad, bad_loss, loss)


PLC_STEP_DB, PLC_MAX_FRAMES = 3.0, 3        # concealment: -3 dB per lost frame in a row, muted after 3


def _period(x, lo=20, hi=120):
    """Concealment repeat length: lag (samples) of the normalised autocorrelation peak in [lo, hi)."""
    n = len(x)
    hi = min(hi, n - lo)
    if hi <= lo:
        return n
    ac = np.correlate(x, x, "full")[n - 1:]
    e = np.cumsum(x * x)
    lag = np.arange(lo, hi)
    return int(lag[np.argmax(ac[lag] / np.sqrt(e[n - 1 - lag] * (e[-1] - e[lag - 1]) + 1e-12))])


def voice_path(sig, rng, snr_db=14.0, level_jitter_db=3.0, onset_clip=0.6, loss=0.02, plc=False, burst=None,
               bad_loss=0.5, lost=None):
    """Ordinary voice path, ASSUMED impairments of a speech codec on pure tones.

    Defaults are the original model: independent 20 ms frame loss, lost frames zeroed.
    plc: crude stand-in for codec concealment, -3 dB per lost frame in a row, the 4th lost
    frame in a row and later muted. plc=True continues the last good frame's final
    pitch-ish period (autocorrelation lag, 2.5-15 ms), as CELP-style concealment does;
    plc="frame" replays the whole last good frame. Both can stretch a DTMF digit into
    the gap after it (decode_dtmf is left as it is).
    burst=(p_gb, p_bg): Gilbert-Elliott loss, `loss` in the good state and `bad_loss` in the
    bad state (mean rate: ge_mean_loss). Without burst the random draws match the default's.
    lost: explicit per-frame loss pattern (bools), overriding loss and burst; for tests and demos.
    """
    y = _band(sig.copy())
    frame = int(0.02 * FS)
    p = np.mean(y * y) + 1e-12
    if not plc and burst is None and lost is None:
        for i in range(0, len(y), frame):
            seg = y[i:i + frame]
            seg *= 10 ** (rng.normal(0, level_jitter_db) / 20)
            if rng.random() < loss:
                seg[:] = 0.0
    else:
        starts = range(0, len(y), frame)
        if lost is not None:
            gains, lost = rng.normal(0, level_jitter_db, len(starts)), np.resize(np.asarray(lost, bool), len(starts))
        elif burst is None:
            draws = [(rng.normal(0, level_jitter_db), rng.random() < loss) for _ in starts]
            gains, lost = [d[0] for d in draws], [d[1] for d in draws]
        else:
            gains = rng.normal(0, level_jitter_db, len(starts))
            lost = gilbert_elliott(len(starts), rng, *burst, loss=loss, bad_loss=bad_loss)
        good, run = None, 0
        for i, g, gone in zip(starts, gains, lost):
            seg = y[i:i + frame]
            seg *= 10 ** (g / 20)
            if not gone:
                good, run = seg.copy(), 0
                continue
            run += 1
            if not plc or good is None or run > PLC_MAX_FRAMES:
                seg[:] = 0.0
                continue
            if plc == "frame":
                fill = good[:len(seg)]
            else:
                lag = _period(good) if run == 1 else lag
                fill = good[len(good) - lag + np.arange((run - 1) * frame, (run - 1) * frame + len(seg)) % lag]
            seg[:] = fill * 10 ** (-PLC_STEP_DB * run / 20)
    env = np.convolve(np.abs(y), np.ones(40) / 40, mode="same")        # 5 ms envelope
    active = env > 0.05
    onsets = np.flatnonzero(np.diff(active.astype(int)) == 1)
    for o in onsets:                                   # noise suppression clips tone onsets
        y[o:o + int(0.015 * FS)] *= (1 - onset_clip)
    y += rng.normal(0, np.sqrt(p / 10 ** (snr_db / 10)), len(y))
    return y


def alarm_path(sig, rng):
    """Registered alarm number: transparent telephone channel (band limit, mu-law, light noise)."""
    y = _band(sig)
    peak = np.max(np.abs(y)) + 1e-12
    q = np.sign(y / peak) * np.log1p(255 * np.abs(y / peak)) / np.log1p(255)
    y = np.sign(q) * np.expm1(np.abs(np.round(q * 127) / 127) * np.log1p(255)) / 255 * peak
    return y + rng.normal(0, 0.002, len(y))


def detect_tone_fast(sig, f, min_s, min_rms=0.02):
    """Same rule as detect_tone (20 ms frames, level gate, 0.6 power share), vectorised for sweeps."""
    from .tap import goertzel_power
    n = int(0.02 * FS)
    starts = np.arange(0, len(sig) - n, n)
    if not len(starts):
        return False
    F = sig[starts[:, None] + np.arange(n)]
    p = np.mean(F * F, 1)
    on = (np.sqrt(p) > min_rms) & (goertzel_power(F, [f])[:, 0] / (n * n / 4) / (2 * (p + 1e-12)) > 0.6)
    d = np.diff(np.concatenate([[0], on.astype(int), [0]]))
    return bool(on.any()) and int((np.flatnonzero(d == -1) - np.flatnonzero(d == 1)).max()) >= int(round(min_s / 0.02))


def decode_dtmf_fast(sig, min_rms=0.02):
    """Same output as decode_dtmf (tap.py's vectorised copy of it)."""
    from .tap import decode_dtmf_fast as fast
    return fast(sig, min_rms)


def alarm_call(rng, registered=True, receiver_up=True, attempts=4, message=None, voice_kw=None, fast=False):
    """One alarm event: up to `attempts` tries; returns what the panel believes and what really happened.

    voice_kw: options passed to voice_path on the unregistered path (loss, plc, burst, ...).
    fast: vectorised detectors with the same rules (for sweeps).
    """
    msg = message or contact_id()
    path = alarm_path if registered else (lambda s, r: voice_path(s, r, **(voice_kw or {})))
    tone, decode = (detect_tone_fast, decode_dtmf_fast) if fast else (detect_tone, decode_dtmf)
    for attempt in range(1, attempts + 1):
        if not receiver_up:
            continue
        hs = path(handshake(), rng)                     # receiver -> panel
        if not (tone(hs, 1400, 0.06) and tone(hs, 2300, 0.06)):
            continue
        heard = decode(path(dtmf(msg), rng))            # panel -> receiver
        if not checksum_ok(heard):
            continue
        ko = path(kissoff(), rng)                       # receiver -> panel
        if tone(ko, 1400, 0.4):
            return {"delivered": True, "attempts": attempt, "received": heard, "kissoff": True}
    return {"delivered": False, "attempts": attempts, "received": None, "kissoff": False}


def success_rates(trials=40, seed=3):
    rng = np.random.default_rng(seed)
    out = {}
    for name, kw in (("registered (##21 done)", {"registered": True}),
                     ("unregistered number (voice path)", {"registered": False}),
                     ("receiver down", {"registered": True, "receiver_up": False})):
        res = [alarm_call(rng, **kw) for _ in range(trials)]
        ok = [r for r in res if r["delivered"]]
        out[name] = {"delivered_rate": round(len(ok) / trials, 3),
                     "mean_attempts_when_delivered": round(float(np.mean([r["attempts"] for r in ok])), 2) if ok else None,
                     "first_try_rate": round(sum(r["attempts"] == 1 for r in ok) / trials, 3)}
    return out


def loss_curve(losses=(0.0, 0.01, 0.02, 0.05, 0.1), trials=30, seed=5):
    """Unregistered (voice-path) alarm delivery vs assumed frame loss: first-try and within-4-tries rates."""
    rng = np.random.default_rng(seed)
    out = []
    for loss in losses:
        def path(sig, r, _l=loss):
            return voice_path(sig, r, loss=_l)
        first = within = 0
        msg = contact_id()
        for _ in range(trials):
            for attempt in range(1, 5):
                hs = path(handshake(), rng)
                if not (detect_tone(hs, 1400, 0.06) and detect_tone(hs, 2300, 0.06)):
                    continue
                if checksum_ok(decode_dtmf(path(dtmf(msg), rng))) and detect_tone(path(kissoff(), rng), 1400, 0.4):
                    first += attempt == 1
                    within += 1
                    break
        out.append({"frame_loss": loss, "first_try": round(first / trials, 3), "within_4_tries": round(within / trials, 3)})
    return out


# Formants (F1, F2, F3 in Hz) of five vowels, textbook adult averages; bandwidths 60/90/120 Hz.
VOWELS = ((730, 1090, 2440), (270, 2290, 3010), (300, 870, 2240), (530, 1840, 2480), (570, 840, 2410))
FORMANT_BW = (60.0, 90.0, 120.0)


def _syllable(rng, m, f0):
    """One voiced syllable, m samples (+30 ms ring): glottal pulses -> 3 formant resonators, raised-sine envelope."""
    x = np.zeros(m + int(0.03 * FS))
    f = f0 * np.linspace(1.0, rng.uniform(0.9, 1.1), m)                 # pitch glide over the syllable
    x[:m] = np.diff(np.floor(np.cumsum(f) / FS), prepend=0.0) * np.sin(np.pi * np.arange(m) / m) ** 2
    fr = np.fft.rfftfreq(len(x), 1 / FS)
    zi = np.exp(-2j * np.pi * fr / FS)
    H = 1 / np.sqrt(1 + (fr / 300) ** 2)                               # source tilt, about -6 dB/oct
    for F, B in zip(VOWELS[rng.integers(len(VOWELS))], FORMANT_BW):
        r, c = np.exp(-np.pi * B / FS), np.cos(2 * np.pi * F / FS)
        H = H * (1 - 2 * r * c + r * r) / (1 - 2 * r * c * zi + r * r * zi * zi)
    return np.fft.irfft(np.fft.rfft(x) * H, len(x))


def speech_like(rng, seconds=3.0, level=0.1):
    """Synthetic speech-LIKE test signal (not speech, not a P.501 test signal).

    Words of 2-4 voiced syllables at about 4 syllables/s (the syllable envelope is the 4 Hz
    amplitude modulation), F0 100-200 Hz per word, gently falling, then 0.15-0.45 s pauses.
    Scaled to `level` RMS so voice_path's absolute onset detector sees it like the tones.
    """
    n = int(seconds * FS)
    out = np.zeros(n + int(0.05 * FS))
    t = rng.uniform(0.05, 0.2)
    while t < seconds - 0.2:
        f0 = rng.uniform(100, 200)
        for _ in range(rng.integers(2, 5)):
            m = int(rng.uniform(0.18, 0.32) * FS)
            a = int(t * FS)
            if a + m > n:
                break
            seg = _syllable(rng, m, f0)
            out[a:a + len(seg)] += seg[:len(out) - a]
            f0 *= rng.uniform(0.92, 1.02)
            t += m / FS
        t += rng.uniform(0.15, 0.45)
    out = out[:n]
    return out * level / (np.sqrt(np.mean(out * out)) + 1e-12)


def log_spectral_distance(clean, degraded, frame=0.016, floor_db=-15.0, active_db=-20.0):
    """Mean frame-wise log-spectral distance (dB), both signals limited to the telephone band.

    Hann frames of 16 ms every 8 ms (short enough that one lost 20 ms frame fills some),
    300-3400 Hz bins, averaged over the clean signal's active frames (within `active_db` of
    its loudest). Both power spectra get a floor `floor_db` under the clean signal's mean
    active spectrum, so pauses, spectral valleys and the path's noise do not dominate.
    """
    clean, degraded = _band(np.asarray(clean, float)), _band(np.asarray(degraded, float))
    n = int(frame * FS)
    m = min(len(clean), len(degraded))
    idx = np.arange(0, m - n + 1, n // 2)[:, None] + np.arange(n)
    w = np.hanning(n)
    fr = np.fft.rfftfreq(n, 1 / FS)
    band = (fr >= 300) & (fr <= 3400)
    C = np.abs(np.fft.rfft(clean[idx] * w, axis=1))[:, band] ** 2
    D = np.abs(np.fft.rfft(degraded[idx] * w, axis=1))[:, band] ** 2
    e = C.sum(1)
    act = e > e.max() * 10 ** (active_db / 10)
    fl = C[act].mean() * 10 ** (floor_db / 10)
    d = 10 * np.log10((C[act] + fl) / (D[act] + fl))
    return float(np.mean(np.sqrt(np.mean(d * d, 1))))


PROXY_LSD_MID, PROXY_LSD_SCALE = 3.27, 0.22   # ARBITRARY logistic; calibration in speech_quality_proxy
VOICE_CLEAR = 3.0                              # proxy score for "voice clear", mirroring the bench's MOS >= 3.0 rule


def speech_quality_proxy(clean, degraded):
    """Crude objective score on a 1-4.5 "proxy MOS" scale. NOT PESQ, NOT POLQA, not a MOS.

    log_spectral_distance mapped through 1 + 3.5 / (1 + exp((LSD - mid) / scale)). The mapping
    is ARBITRARY. mid and scale put the median of 300 speech_like clips at 4.3 on the default
    voice path at zero loss (median LSD 2.64 dB) and at 1.8 with 20% independent frame loss
    and no concealment (3.54 dB). No listening test stands behind any value in between, and
    clip-to-clip spread at zero loss (about 0.3 dB) leaves a few clean clips under 3.0.
    """
    lsd = log_spectral_distance(clean, degraded)
    return float(1 + 3.5 / (1 + np.exp((lsd - PROXY_LSD_MID) / PROXY_LSD_SCALE)))


def _nonincreasing(ys):
    """Closest non-increasing sequence (pool adjacent violators, equal weights): smooths sampling noise."""
    blocks = []
    for y in ys:
        blocks.append([float(y), 1])
        while len(blocks) > 1 and blocks[-2][0] < blocks[-1][0]:
            (a, n), (b, m) = blocks[-2], blocks.pop()
            blocks[-1] = [(a * n + b * m) / (n + m), n + m]
    return [v for v, n in blocks for _ in range(n)]


def _l90(xs, ys, level=0.9):
    """Loss rate where ys first drops below `level`, linearly interpolated; 0.0 if already below, None if never."""
    if ys[0] < level:
        return 0.0
    for x0, y0, x1, y1 in zip(xs, ys, xs[1:], ys[1:]):
        if y1 < level:
            return round(x0 + (x1 - x0) * (y0 - level) / (y0 - y1), 4)
    return None


def _first(l_alarm, l_voice, tol=0.01):
    """Which crosses 90% at the lower loss rate ('together' within `tol`; None = never in range)."""
    a, v = (float("inf") if x is None else x for x in (l_alarm, l_voice))
    if a == v == float("inf"):
        return "neither drops below 90% in this range"
    return "together" if abs(a - v) <= tol else ("alarm" if a < v else "voice")


def voice_vs_alarm_curve(losses=(0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12), trials=80, plc=True, burst=0.2,
                         bad_loss=0.5, seed=8, message=None):
    """MODEL, not a bench result: voice-clear rate vs alarm success on the SAME voice path, per mean frame loss.

    Assumptions (all ours): speech is speech_like(), 3 s clips; "voice clear" is
    speech_quality_proxy >= 3.0 (an arbitrary map of log-spectral distance, not PESQ).
    Alarms ride voice_path with the same options (unregistered number: no ##21 path),
    through alarm_call's logic (handshake, 16 digits with checksum, kiss-off, up to 4 tries).
    Other impairments stay at voice_path's defaults (14 dB SNR, 3 dB per-frame level jitter,
    onset clipping), which were written for tones; the onset clipper also chops speech.
    burst=None: independent loss at the stated rate. burst=p_bg: Gilbert-Elliott loss with
    no loss in the good state, `bad_loss` in the bad state, mean bad stay 1/p_bg frames, and
    p_gb solved so the long-run loss equals the stated rate; each path call starts afresh.
    L90 = loss rate where a rate drops below 90%, interpolated on a non-increasing fit of the
    rates. With 80 trials a 90% rate has a standard error of about 3 points, which moves a
    shallow curve's L90 by about a point of loss; "together" means within one point.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for loss in losses:
        if burst is None:
            kw = {"loss": loss, "plc": plc}
        else:
            pb = loss / bad_loss
            kw = {"loss": 0.0, "plc": plc, "burst": (burst * pb / (1 - pb), burst), "bad_loss": bad_loss}
        q = []
        for _ in range(trials):
            s = speech_like(rng)
            q.append(speech_quality_proxy(s, voice_path(s, rng, **kw)))
        calls = [alarm_call(rng, registered=False, message=message, voice_kw=kw, fast=True) for _ in range(trials)]
        q = np.array(q)
        rows.append({"mean_loss": loss, "voice_clear": round(float(np.mean(q >= VOICE_CLEAR)), 3),
                     "median_proxy": round(float(np.median(q)), 2),
                     "alarm_first_try": round(sum(c["delivered"] and c["attempts"] == 1 for c in calls) / trials, 3),
                     "alarm_within_4": round(sum(c["delivered"] for c in calls) / trials, 3)})
    xs = [r["mean_loss"] for r in rows]
    l90 = {k: _l90(xs, _nonincreasing([r[k] for r in rows])) for k in ("voice_clear", "alarm_first_try", "alarm_within_4")}
    return {"label": "model, assumptions in docstring", "plc": plc,
            "loss": "independent" if burst is None else f"Gilbert-Elliott, bad-state loss {bad_loss}, p_bg {burst}",
            "trials": trials, "rows": rows, "l90": l90,
            "fails_first": {"first_try_vs_voice": _first(l90["alarm_first_try"], l90["voice_clear"]),
                            "within_4_vs_voice": _first(l90["alarm_within_4"], l90["voice_clear"])}}


if __name__ == "__main__":
    import json
    m = contact_id()
    print(m, checksum_ok(m))
    print(json.dumps(success_rates(), indent=1))
