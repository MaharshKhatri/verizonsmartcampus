#!/usr/bin/env python3
"""Write a SYNTHETIC attenuation-sweep CSV so the team can rehearse the analysis before bench data exist.

    python3 scripts/make_demo_sweep_csv.py          # -> field_data/demo_sweep_SYNTHETIC.csv
    python3 scripts/analyze_prove_lab.py field_data/demo_sweep_SYNTHETIC.csv

NOT A MEASUREMENT. Alarm trials come from prototype/prove/alarm.py's model
(Contact ID over the voice path, up to 4 attempts, kiss-off check). Everything
that links the attenuator to that model is ASSUMED:
  attenuation -> SINR   a fixed interference floor plus receiver noise, per box;
  SINR -> frame loss    signal_model._loss_from_sinr (the same curve for both boxes);
  frame loss -> voice   PESQ and listener-keyword scores from a made-up straight line;
  very low SINR         the call drops outright.
Both boxes share the same SINR -> loss curve, so any difference between them
in this file is chance. Every row's notes say SYNTHETIC.
"""
import csv
import os
import sys

import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, ROOT)

from prototype.prove import alarm, signal_model, tap  # noqa: E402

OUT = os.path.join(ROOT, "field_data", "demo_sweep_SYNTHETIC.csv")
COLUMNS = ["test_id", "date", "box", "firmware", "placement", "rsrp_dbm", "rsrq_db", "sinr_db", "device", "format",
           "registered_21", "attempt", "delivered", "kissoff_s", "attempts_used", "notes",
           "atten_db", "pesq", "listener_keywords", "call_trial"]
# box: (signal-to-interference dB, signal-to-noise dB with no attenuator, RSRP dBm with no attenuator), all ASSUMED
BOXES = {"verizon_box": (18.0, 52.0, -78.0), "other_carrier_box": (16.0, 49.0, -81.0)}
NOTE = "SYNTHETIC: alarm.py model + assumed atten->SINR->loss mapping; not a measurement"


def sinr_at(atten, sir, snr0):
    """ASSUMED: the attenuator lowers signal and interference together, but not the receiver's own noise."""
    return -10 * np.log10(10 ** (-sir / 10) + 10 ** (-(snr0 - atten) / 10))


def p_drop(sinr):
    """ASSUMED: chance the call itself drops (both voice and alarm fail) at very low SINR."""
    return 1 / (1 + np.exp((sinr + 6.0) / 1.0))


def alarm_trial(rng, loss, drop):
    """One alarm event through alarm.py's voice-path model: (confirmed, attempts_used, kissoff_s)."""
    msg = alarm.contact_id()

    def path(s):
        return alarm.voice_path(s, rng, loss=loss, snr_db=18.0, level_jitter_db=1.5)
    if rng.random() < drop:
        return False, 1, None
    for a in range(1, tap.MAX_ATTEMPTS + 1):
        hs = path(alarm.handshake())
        if not (alarm.detect_tone(hs, 1400, 0.06) and alarm.detect_tone(hs, 2300, 0.06)):
            continue
        heard = tap.decode_dtmf_fast(path(alarm.dtmf(msg)))          # same output as alarm.decode_dtmf, faster
        if alarm.checksum_ok(heard) and alarm.detect_tone(path(alarm.kissoff()), 1400, 0.4):
            return True, a, round(0.3 + 0.25 + a * 1.76 + (a - 1) * 1.25 + 0.25 + rng.normal(0, 0.05), 2)
    return False, tap.MAX_ATTEMPTS, None


def call_trial(rng, loss, drop):
    """ASSUMED voice quality: (PESQ or None if not measured, keywords right out of 10)."""
    if rng.random() < drop:
        pesq, kw = 1.0, 0
    else:
        pesq = float(np.clip(4.3 - 12.0 * loss + rng.normal(0, 0.12), 1.0, 4.5))
        kw = int(rng.binomial(10, 1 - 0.6 * loss))
    return (None if rng.random() < 0.3 else round(pesq, 2)), kw    # PESQ not run on about 30% of calls


def demo_rows(seed=4, attens=range(0, 62, 2), trials=10):
    rng = np.random.default_rng(seed)
    rows = []
    for box, (sir, snr0, rsrp0) in BOXES.items():
        for atten in attens:
            true_sinr = sinr_at(atten, sir, snr0)
            for kind in ("alarm", "call"):
                for i in range(trials):
                    sinr = true_sinr + rng.normal(0, 0.5)                  # what the admin page would show
                    loss, drop = signal_model._loss_from_sinr(sinr), p_drop(sinr)
                    r = dict.fromkeys(COLUMNS, "")
                    r.update(test_id=f"SYN-{box[:3].upper()}-{atten:02d}-{kind[0]}{i:02d}", date="SYNTHETIC",
                             box=box, firmware="n/a", placement="bench attenuator",
                             rsrp_dbm=round(rsrp0 - atten + rng.normal(0, 1), 1),
                             rsrq_db=round(-9 - (16 - sinr) * 0.45 + rng.normal(0, 1.0), 1), sinr_db=round(sinr, 1),
                             attempt=i + 1, notes=NOTE, atten_db=atten, call_trial=int(kind == "call"))
                    if kind == "alarm":
                        ok, used, ko = alarm_trial(rng, loss, drop)
                        r.update(device="contact_id_panel", format="contact_id", delivered=int(ok),
                                 attempts_used=used, kissoff_s="" if ko is None else ko)
                    else:
                        pesq, kw = call_trial(rng, loss, drop)
                        r.update(device="analog_phone", format="voice", pesq="" if pesq is None else pesq,
                                 listener_keywords=kw)
                    rows.append(r)
    return rows


def write_csv(path, rows):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else OUT
    rows = demo_rows()
    write_csv(path, rows)
    print(f"wrote {len(rows)} SYNTHETIC rows to {path}")
