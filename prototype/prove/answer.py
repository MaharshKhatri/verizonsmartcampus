"""WHO ANSWERS: did a person actually pick up the elevator HELP call, fast enough, at the right place?

The code's line check never places a call (A17.1 2.27.1.1.6(a)), so it cannot
see the failures inspectors keep citing: HELP that reaches voicemail, a "not in
service" recording, a fax line, the previous contractor, or an operator shown
the wrong building. A17.1 also requires a staffed 24-hour answerer and a
redirect if the call is not acknowledged within 45 seconds.

This module runs at the gateway's analog port in the machine room (no work in
the car). It classifies who answered from the first seconds of call audio
using spectral features only (nothing is recorded or transcribed), and checks
the call's metadata against a registry. Signals here are synthetic stand-ins;
the classifier's thresholds are tuned on them and must be re-checked on real
calls during the pilot.
"""
from dataclasses import dataclass

import numpy as np

from .acoustic import FS, _band

SIT = (913.8, 1370.6, 1776.7)        # special information tones before "not in service" intercepts
REDIRECT_S = 45.0                    # A17.1-2022 2.27.1.1.2: redirect if not acknowledged within 45 s


def _tone(f, dur, amp=0.3):
    t = np.arange(int(dur * FS)) / FS
    return amp * np.sum([np.sin(2 * np.pi * x * t) for x in np.atleast_1d(f)], axis=0)


def _speech(rng, dur, rate=4.0):
    """Speech-like signal: band-limited noise shaped by formants, amplitude-modulated at syllable rate."""
    n = int(dur * FS)
    t = np.arange(n) / FS
    src = rng.normal(0, 1, n)
    X = np.fft.rfft(src)
    f = np.fft.rfftfreq(n, 1 / FS)
    shape = sum(np.exp(-0.5 * ((f - c) / w) ** 2) for c, w in ((500, 150), (1500, 250), (2500, 300)))
    y = np.fft.irfft(X * shape, n)
    env = np.clip(np.sin(2 * np.pi * rate * t + rng.uniform(0, 6)), 0, None) ** 0.7
    return 0.25 * y / (np.std(y) + 1e-9) * env


def synth(kind, rng):
    """First ~10 s of what the far end sends after the HELP call connects (plus ring time in seconds)."""
    sil = lambda s: np.zeros(int(s * FS))
    noise = lambda x: x + rng.normal(0, 0.003, len(x))
    if kind == "person":            # greeting ("Elevator emergency, where are you?"), then waits for the rider
        y = np.concatenate([_speech(rng, rng.uniform(1.2, 3.8)), sil(rng.uniform(2.5, 4.0)), _speech(rng, 1.0), sil(3.0)])
        ring = rng.uniform(4, 20)
    elif kind == "voicemail":       # long uninterrupted prompt, then a beep, then silence
        y = np.concatenate([_speech(rng, rng.uniform(6.5, 9.0)), sil(0.2), _tone(1000, 0.4), sil(1.5)])
        ring = rng.uniform(15, 30)
    elif kind == "ivr":             # menu prompt with short gaps that never stops for the caller
        y = np.concatenate(sum([[_speech(rng, 2.2), sil(0.5)] for _ in range(4)], []))
        ring = rng.uniform(2, 6)
    elif kind == "intercept":       # SIT tones then a recording
        y = np.concatenate([_tone(SIT[0], 0.274), _tone(SIT[1], 0.274), _tone(SIT[2], 0.38), sil(0.1), _speech(rng, 5.0)])
        ring = rng.uniform(0.5, 2)
    elif kind == "fax":             # answer tone (2100 Hz) from a fax or modem line
        y = np.concatenate([_tone(2100, 3.3), sil(0.5), _tone(1100, 0.5), sil(2.0)])
        ring = rng.uniform(2, 8)
    elif kind == "no_answer":       # ringback cadence, 2 s on / 4 s off, nobody picks up
        y = np.concatenate([_tone((440, 480), 2.0, 0.2), sil(4.0), _tone((440, 480), 2.0, 0.2), sil(2.0)])
        ring = 60.0
    elif kind == "busy":            # 480+620 Hz, 0.5 s on / 0.5 s off
        y = np.concatenate([np.concatenate([_tone((480, 620), 0.5, 0.2), sil(0.5)]) for _ in range(8)])
        ring = 0.0
    else:
        raise ValueError(kind)
    return _band(noise(y)), ring


def _fraction(fr, freqs):
    n = len(fr)
    p = np.mean(fr * fr) + 1e-12
    out = 0.0
    for f in np.atleast_1d(freqs):
        k = 2 * np.cos(2 * np.pi * f / FS)
        s1 = s2 = 0.0
        for x in fr:
            s1, s2 = x + k * s1 - s2, s1
        out += s1 * s1 + s2 * s2 - k * s1 * s2
    return out / (n * n / 4) / (2 * p)


def features(y):
    """Per-20-ms frame: active?, tonal at SIT / 1 kHz / 2100 Hz / ringback / busy; then summary features."""
    n = int(0.02 * FS)
    frames = [y[i:i + n] for i in range(0, len(y) - n, n)]
    rms = np.array([np.sqrt(np.mean(f * f)) for f in frames])
    active = rms > 0.02
    tonal = {name: np.array([a and _fraction(f, fr) > 0.6 for f, a in zip(frames, active)])
             for name, fr in (("sit", SIT), ("beep", 1000), ("ans", 2100), ("ring", (440, 480)), ("busy", (480, 620)))}
    speechy = active & ~np.any(np.vstack(list(tonal.values())), axis=0)
    # longest run of speech allowing gaps under 0.8 s (syllables, menu pauses)
    run, best, gap = 0, 0, 0
    for s in speechy:
        if s:
            run, gap = run + 1 + gap, 0
            best = max(best, run)
        elif run:
            gap += 1
            if gap > 40:
                run, gap = 0, 0
    # silence right after the first burst of speech: a person greets you and then waits for you to talk
    pause_after = 0.0
    idx = np.flatnonzero(speechy)
    if len(idx):
        i = last = idx[0]
        while i < len(speechy):
            if speechy[i]:
                last = i
            elif i - last > 40:
                break
            i += 1
        j = last + 1
        while j < len(active) and not active[j]:
            j += 1
        pause_after = (j - last - 1) * 0.02
    return {"longest_speech_s": best * 0.02, "pause_after_greeting_s": pause_after,
            **{f"{k}_s": float(v.sum() * 0.02) for k, v in tonal.items()}}


def classify(y):
    f = features(y)
    if f["sit_s"] >= 0.3:
        return "intercept", f
    if f["ans_s"] >= 1.0:
        return "fax", f
    if f["busy_s"] >= 1.0:
        return "busy", f
    if f["ring_s"] >= 1.5 and f["longest_speech_s"] < 0.5:
        return "no_answer", f
    if f["beep_s"] >= 0.2 and f["longest_speech_s"] >= 4.0:
        return "voicemail", f
    if f["longest_speech_s"] >= 5.0:
        return "ivr", f
    if f["longest_speech_s"] > 0.5 and f["pause_after_greeting_s"] >= 2.0:
        return "person", f
    return "unknown", f


@dataclass
class Registry:
    """What the building owner says HELP should do (from the HELP audit / contract)."""
    answerer_number: str = "7329327211"            # placeholder; the real number comes from Facilities
    old_numbers: tuple = ("8005550199",)           # previous contractor's call center, if known
    label: str = "Hill Center, Car 2"


def check_call(dialed, kind, ring_s, label_shown, reg, rng=None):
    """One HELP call (test or real): route, answerer type, answer time vs 45 s, and location shown."""
    rng = rng or np.random.default_rng(0)
    y, _ = synth(kind, rng)
    got, feats = classify(y)
    issues = []
    if dialed in reg.old_numbers:
        issues.append("dials the previous contractor's number")
    elif dialed == "911":
        issues.append("dials 911 directly instead of the 24-hour answering service")
    elif dialed != reg.answerer_number:
        issues.append("dials an unregistered number")
    if got != "person":
        issues.append(f"answered by: {got.replace('_', ' ')}")
    elif ring_s > REDIRECT_S:
        issues.append(f"answered after {ring_s:.0f} s (redirect required after {REDIRECT_S:.0f} s)")
    if got == "person" and label_shown is not None and label_shown != reg.label:
        issues.append(f"answerer's screen shows '{label_shown}'")
    return {"answered_by": got, "ring_s": round(ring_s, 1), "issues": issues, "pass": not issues,
            "features": {k: round(v, 2) for k, v in feats.items()}}


def hard(y, kind, rng):
    """Stress variant: random level, louder line noise; some voicemails have no beep."""
    y = y * rng.uniform(0.35, 1.6) + rng.normal(0, 0.012, len(y))
    if kind == "voicemail" and rng.random() < 0.3:
        n = int(0.6 * FS)
        y[-int(2.1 * FS):-int(2.1 * FS) + n] = rng.normal(0, 0.012, n)    # beep removed
    return y


def confusion(trials=25, seed=8, stress=False):
    kinds = ("person", "voicemail", "ivr", "intercept", "fax", "no_answer", "busy")
    rng = np.random.default_rng(seed)
    m = {k: {j: 0 for j in kinds + ("unknown",)} for k in kinds}
    for k in kinds:
        for _ in range(trials):
            y, _ = synth(k, rng)
            if stress:
                y = hard(y, k, rng)
            m[k][classify(y)[0]] += 1
    acc = sum(m[k][k] for k in kinds) / (trials * len(kinds))
    # the safety question is binary: did a person answer?
    person_ok = m["person"]["person"] + sum(trials - m[k]["person"] for k in kinds if k != "person")
    return {"accuracy": round(acc, 3), "person_vs_not": round(person_ok / (trials * len(kinds)), 3), "matrix": m}


if __name__ == "__main__":
    import json
    print(json.dumps(confusion(trials=10), indent=1))
