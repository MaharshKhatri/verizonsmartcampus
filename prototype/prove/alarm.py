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


def voice_path(sig, rng, snr_db=14.0, level_jitter_db=3.0, onset_clip=0.6, loss=0.02):
    """Ordinary voice path, ASSUMED impairments of a speech codec on pure tones."""
    y = _band(sig.copy())
    frame = int(0.02 * FS)
    p = np.mean(y * y) + 1e-12
    for i in range(0, len(y), frame):
        seg = y[i:i + frame]
        seg *= 10 ** (rng.normal(0, level_jitter_db) / 20)
        if rng.random() < loss:
            seg[:] = 0.0
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


def alarm_call(rng, registered=True, receiver_up=True, attempts=4, message=None):
    """One alarm event: up to `attempts` tries; returns what the panel believes and what really happened."""
    msg = message or contact_id()
    path = alarm_path if registered else voice_path
    for attempt in range(1, attempts + 1):
        if not receiver_up:
            continue
        hs = path(handshake(), rng)                     # receiver -> panel
        if not (detect_tone(hs, 1400, 0.06) and detect_tone(hs, 2300, 0.06)):
            continue
        heard = decode_dtmf(path(dtmf(msg), rng))       # panel -> receiver
        if not checksum_ok(heard):
            continue
        ko = path(kissoff(), rng)                       # receiver -> panel
        if detect_tone(ko, 1400, 0.4):
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


if __name__ == "__main__":
    import json
    m = contact_id()
    print(m, checksum_ok(m))
    print(json.dumps(success_rates(), indent=1))
