"""PROVE nightly acoustic test: does sound actually get through, both ways?

A line that answers is not the same as a phone that works. A dead car speaker
or a taped-over car mic still answers a heartbeat. PROVE checks each direction
on its own, with two different probe chirps:

  downlink  console -> voice call -> gateway -> car speaker -> air -> PROVE sensor mic
  uplink    PROVE piezo -> air -> car mic -> phone (echo canceller) -> gateway -> console

Why not one loopback (console chirp out of the speaker, back in through the car
mic)? Hands-free phones run acoustic echo cancellation and voice switching,
which exist to remove exactly that signal. A naive loopback can fail on a
healthy phone. `loopback_test` models that design so the comparison is
explicit. Real hardware decides it (Gate B bench test); this module is a
simulation with stated assumptions, not a measurement.

Narrowband telephony (8 kHz, 300-3400 Hz) is assumed throughout because the
car station is an analog phone on an FXS port.
"""
from dataclasses import dataclass, field

import numpy as np

FS = 8000
PROBE_S = 0.4
PASS_DB = 22.0          # detection margin needed to pass; pure noise peaks at <=17.8 dB (see noise_only_margins)
FLOOR = 0.003           # fixed self-noise of the PROVE sensor mic and comfort noise on the uplink
BANDS = ((600, 1200), (1200, 2000), (2000, 3000))


def chirp(f0, f1, dur=PROBE_S, fs=FS):
    t = np.arange(int(dur * fs)) / fs
    k = (f1 - f0) / dur
    x = np.sin(2 * np.pi * (f0 * t + 0.5 * k * t * t))
    return x * np.hanning(len(x))


DOWN_PROBE = chirp(600, 3000)    # up-sweep: console -> car
UP_PROBE = chirp(3000, 600)      # down-sweep: car -> console (low cross-correlation with DOWN_PROBE)


def _band(x, lo=300.0, hi=3400.0, fs=FS):
    """Ideal band-pass by FFT masking (good enough for a channel model)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / fs)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def _lowpass(x, fc, fs=FS):
    return _band(x, 0.0, fc, fs)


def _room_ir(rng, rt60=0.15, fs=FS):
    """Small, hard-walled car: direct path plus an exponentially decaying tail."""
    n = int(rt60 * fs)
    t = np.arange(n) / fs
    ir = rng.normal(0, 1, n) * np.exp(-6.9 * t / rt60) * 0.25
    ir[0] = 1.0
    return ir / np.sqrt(np.sum(ir ** 2))


def _noise(rng, n, level):
    """Pink-ish ambient noise (fan, machine hum) with a 60 Hz hum component."""
    w = rng.normal(0, 1, n)
    pink = np.cumsum(w)
    pink -= np.convolve(pink, np.ones(64) / 64, mode="same")
    pink /= (np.std(pink) + 1e-12)
    hum = np.sin(2 * np.pi * 60 * np.arange(n) / FS) * 0.3
    return level * (pink + hum)


def _codec(x, rng, loss=0.0):
    """Telephone band, mu-law quantization, and random 20 ms frame loss."""
    y = _band(x)
    peak = np.max(np.abs(y)) + 1e-12
    mu = 255.0
    yn = y / peak
    q = np.sign(yn) * np.log1p(mu * np.abs(yn)) / np.log1p(mu)
    q = np.round(q * 127) / 127
    y = np.sign(q) * (np.expm1(np.abs(q) * np.log1p(mu)) / mu) * peak
    if loss > 0:
        frame = int(0.02 * FS)
        for i in range(0, len(y), frame):
            if rng.random() < loss:
                y[i:i + frame] = 0.0
    return y


@dataclass
class CarState:
    """Ground truth for one elevator car's emergency phone path."""
    speaker_gain: float = 1.0      # 0 = dead speaker, ~0.15 = blown/obstructed
    mic_gain: float = 1.0          # 0 = dead mic
    mic_taped: bool = False        # tape / grime: -20 dB and high-frequency loss
    noise_level: float = 0.02      # ambient noise relative to a healthy speaker at the sensor
    packet_loss: float = 0.0       # marginal RF / congested cell
    call_connects: bool = True     # gateway registered, RF attached, VoLTE call set up
    voice_switched: bool = True    # phone mutes its mic while the far end is talking (common in hands-free units)
    aec: bool = True               # full-duplex phones: echo canceller + residual suppression


@dataclass
class DirectionResult:
    margin_db: float
    passed: bool
    band_db: list = field(default_factory=list)   # per-band margin, low/mid/high


def detect(received, probe):
    """Normalised matched filter. Returns (margin dB, per-band margins dB).

    Margin = correlation peak over the robust noise floor of the correlation
    away from the peak. Band margins correlate against sub-sweeps of the probe
    (a linear chirp maps time to frequency), which exposes high-frequency loss
    from a taped mic or a damaged speaker cone.
    """
    def margin(sig, ref):
        c = np.abs(np.correlate(sig, ref / (np.linalg.norm(ref) + 1e-12), mode="valid"))
        if len(c) == 0:
            return -60.0
        k = int(np.argmax(c))
        guard = len(ref) // 4
        mask = np.ones(len(c), bool)
        mask[max(0, k - guard):k + guard] = False
        floor = np.median(c[mask]) if mask.any() else 1e-9
        return float(20 * np.log10((c[k] + 1e-12) / (floor + 1e-12)))

    total = margin(received, probe)
    up = probe is DOWN_PROBE
    n = len(probe)
    bands = []
    for lo, hi in BANDS:
        f0, f1 = (600, 3000) if up else (3000, 600)
        a = int((lo - f0) / (f1 - f0) * n) if up else int((f0 - hi) / (f0 - f1) * n)
        b = int((hi - f0) / (f1 - f0) * n) if up else int((f0 - lo) / (f0 - f1) * n)
        a, b = max(0, min(a, b)), min(n, max(a, b))
        bands.append(margin(received, probe[a:b]) if b - a > 32 else -60.0)
    return total, bands


def _pad(x, rng, pre=0.15, post=0.25):
    return np.concatenate([np.zeros(int(pre * FS) + int(rng.integers(0, 400))), x, np.zeros(int(post * FS))])


def downlink_test(car, rng):
    """Console chirp -> car speaker -> PROVE sensor mic in the car operating panel."""
    if not car.call_connects:
        return DirectionResult(-60.0, False, [-60.0] * 3)
    x = _codec(_pad(DOWN_PROBE, rng), rng, car.packet_loss)
    air = np.convolve(x * car.speaker_gain, _room_ir(rng))[:len(x)]
    rx = air + _noise(rng, len(air), car.noise_level) + rng.normal(0, FLOOR, len(air))
    m, b = detect(rx, DOWN_PROBE)
    return DirectionResult(m, m >= PASS_DB, b)


def uplink_test(car, rng):
    """PROVE piezo chirp -> car mic -> phone -> gateway -> console.

    The phone's echo canceller only removes the far-end (downlink) reference.
    During this test the console sends silence, so voice switching leaves the
    mic open and a locally generated probe passes through.
    """
    if not car.call_connects:
        return DirectionResult(-60.0, False, [-60.0] * 3)
    src = _pad(UP_PROBE, rng) * 0.8
    air = np.convolve(src, _room_ir(rng))[:len(src)]
    mic = air * car.mic_gain
    if car.mic_taped:
        mic = _lowpass(mic, 900) * 0.1
    mic = mic + _noise(rng, len(mic), car.noise_level) * max(car.mic_gain, 0.05)
    rx = _codec(mic + rng.normal(0, FLOOR, len(mic)), rng, car.packet_loss)
    m, b = detect(rx, UP_PROBE)
    return DirectionResult(m, m >= PASS_DB, b)


def _nlms_aec(far, mic, taps=128, mu=0.5):
    """Normalised LMS echo canceller with the far-end signal as reference."""
    w = np.zeros(taps)
    buf = np.zeros(taps)
    out = np.zeros_like(mic)
    for i in range(len(mic)):
        buf = np.roll(buf, 1)
        buf[0] = far[i]
        e = mic[i] - w @ buf
        out[i] = e
        w += mu * e * buf / (buf @ buf + 1e-6)
    return out


def loopback_test(car, rng):
    """The naive single-chirp design: console chirp out of the car speaker, back in through the car mic.

    The phone treats that chirp as its own echo. Voice-switched phones mute the
    mic while the far end talks; full-duplex phones cancel the echo (NLMS) and
    then suppress the residual (non-linear processor) and insert comfort
    noise. Either way a healthy phone can fail the test. `aec=False` models a
    phone with no echo control, which is the only case where loopback works.
    """
    if not car.call_connects:
        return DirectionResult(-60.0, False, [-60.0] * 3)
    far = _codec(_pad(DOWN_PROBE, rng), rng, car.packet_loss)
    echo = np.convolve(far * car.speaker_gain, _room_ir(rng))[:len(far)] * car.mic_gain
    if car.mic_taped:
        echo = _lowpass(echo, 900) * 0.1
    mic = echo + _noise(rng, len(echo), car.noise_level) * max(car.mic_gain, 0.05)
    env = np.convolve(np.abs(far), np.ones(160) / 160, mode="same")
    far_active = env > 0.02
    if car.voice_switched:
        out = np.where(far_active, mic * 0.001, mic)        # mic muted while the far end talks
    elif car.aec:
        out = _nlms_aec(far, mic)
        out = np.where(far_active, out * 0.03, out)         # NLP: residual echo suppression (~-30 dB)
    else:
        out = mic
    rx = _codec(out + rng.normal(0, FLOOR, len(out)), rng, car.packet_loss)   # comfort noise / line floor
    m, b = detect(rx, DOWN_PROBE)
    return DirectionResult(m, m >= PASS_DB, b)


def two_direction_test(car, rng):
    return downlink_test(car, rng), uplink_test(car, rng)


# Conditions for the design comparison and the triage symptom model.
CONDITIONS = {
    "healthy": CarState(),
    "healthy_full_duplex": CarState(voice_switched=False),
    "healthy_no_echo_control": CarState(voice_switched=False, aec=False),
    "speaker_dead": CarState(speaker_gain=0.0),
    "speaker_weak": CarState(speaker_gain=0.15),
    "mic_dead": CarState(mic_gain=0.0),
    "mic_taped": CarState(mic_taped=True),
    "noisy_machine_room": CarState(noise_level=0.12),
    "marginal_rf": CarState(packet_loss=0.25),
    "no_call": CarState(call_connects=False),
}
PATH_OK = {"healthy": True, "healthy_full_duplex": True, "healthy_no_echo_control": True,
           "speaker_weak": True, "noisy_machine_room": True, "marginal_rf": True}
# speaker_weak still passes (audible) but its margin falls well below the car's own baseline;
# `trend.py` turns that drop into a "degrading" warning before it becomes a failure.


def noise_only_margins(n=400, seed=3):
    """Detector margin when no probe is present: sets PASS_DB with headroom."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        x = _noise(rng, FS, 0.02) + rng.normal(0, FLOOR, FS)
        out.append(detect(_codec(x, rng), DOWN_PROBE)[0])
        out.append(detect(x, UP_PROBE)[0])
    return np.array(out)


def compare_designs(trials=40, seed=11):
    """Pass rates for the two-transducer test and the naive loopback, per condition.

    'Correct' means: pass when the voice path works both ways, fail when it does not.
    """
    rng = np.random.default_rng(seed)
    rows = {}
    for name, car in CONDITIONS.items():
        ok_truth = PATH_OK.get(name, False)
        two_pass = loop_pass = 0
        margins = {"down": [], "up": [], "loop": []}
        for _ in range(trials):
            d, u = two_direction_test(car, rng)
            lb = loopback_test(car, rng)
            two_pass += d.passed and u.passed
            loop_pass += lb.passed
            margins["down"].append(d.margin_db)
            margins["up"].append(u.margin_db)
            margins["loop"].append(lb.margin_db)
        rows[name] = {
            "path_ok": ok_truth,
            "two_direction_pass_rate": round(two_pass / trials, 3),
            "loopback_pass_rate": round(loop_pass / trials, 3),
            "two_direction_correct": round((two_pass if ok_truth else trials - two_pass) / trials, 3),
            "loopback_correct": round((loop_pass if ok_truth else trials - loop_pass) / trials, 3),
            "median_down_db": round(float(np.median(margins["down"])), 1),
            "median_up_db": round(float(np.median(margins["up"])), 1),
            "median_loop_db": round(float(np.median(margins["loop"])), 1),
        }
    return rows


if __name__ == "__main__":
    import json
    print(json.dumps(compare_designs(), indent=1))
