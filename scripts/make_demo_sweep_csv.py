#!/usr/bin/env python3
"""Write a SYNTHETIC attenuation-sweep CSV so the team can rehearse the T5 analysis before bench data exist.

    python3 scripts/make_demo_sweep_csv.py          # -> field_data/demo_sweep_SYNTHETIC.csv
    python3 scripts/analyze_prove_lab.py field_data/demo_sweep_SYNTHETIC.csv

NOT A MEASUREMENT. It mirrors the protocol's shape, not any real box:
  steps     5 dB scout steps from 0 dB until service is lost, the dropout step A_edge itself,
            anchors at 0 and A_edge-20 dB, and fine 1 dB steps from A_edge-12 to A_edge-1;
  trials    per step, 20 voice + 20 alarm trials at fine steps and anchors, 4 + 4 at scouts, 10 + 10 setup
            attempts at A_edge; voice and alarm interleaved in random order; split over two bench dates per box
            (one box per day, so the boxes never share a date);
  outcomes  ASSUMED logistic curves in A_rel = atten - A_edge (scale 1 dB). Voice is clear at 90% down to
            A90_voice; alarm is confirmed at 90% down to A90_voice - delta, so the analyser's delta can be
            checked against the KNOWN injected value. A shared offset per date and per (date, step) moves both
            curves together. PESQ and keywords are built so that the pre-registered clear rule holds exactly
            when the latent voice score is >= 0. Given confirmation, the first block got through with
            probability 0.95 * P(confirmed), so the first-try rate tops out near 95%;
  setup     call setup fails with certainty at A_edge and beyond, and increasingly in the last 3 dB before
            it; a few connected calls drop there too;
  radio     RSRP falls 1 dB per dB until the noise floor; SINR follows an assumed interference + noise
            model reaching about -6 dB at A_edge. One cell (PCI, EARFCN) per box.
Every row's notes say SYNTHETIC.
"""
import csv
import datetime as dt
import os
import sys

import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "field_data", "demo_sweep_SYNTHETIC.csv")
COLUMNS = ["test_id", "date", "utc_start", "box", "atten_db", "rsrp_dbm", "sinr_db", "pci", "earfcn", "call_trial",
           "pesq_up", "pesq_down", "listener_keywords", "setup_ok", "fail_stage", "delivered", "attempts_used",
           "kissoff_s", "format", "registered_21", "account", "notes"]
# all ASSUMED: dropout step, injected delta, voice A90 (dB re A_edge), RSRP with no attenuator, SIR, one cell
BOXES = {"verizon_box": dict(edge=56, delta=3.0, a90_voice=-4.0, rsrp0=-78.0, sir=18.0, pci=287, earfcn=5230),
         "other_carrier_box": dict(edge=49, delta=2.0, a90_voice=-3.5, rsrp0=-81.0, sir=16.0, pci=112, earfcn=2050)}
DATES = ("2026-10-27", "2026-10-29")             # box i runs on these dates + i days (one box per bench day)
SCALE_DB, FIRST_TRY_CEIL, NOISE_FLOOR_DBM, EDGE_SINR_DB = 1.0, 0.95, -132.0, -6.0
NOTE = "SYNTHETIC: assumed logistic curves with an injected delta; not a measurement"


def sig(z):
    return 1 / (1 + np.exp(-np.asarray(z, float)))


def steps(edge, fine=20, anchor=20, scout=4, dead=10, dates=2):
    """{atten_db: trials of each kind per date}: scouts every 5 dB to the first dead one, A_edge, anchors, fine.
    Counts are per step over all dates and are split evenly between the dates."""
    per = {k: -(-v // dates) for k, v in dict(fine=fine, anchor=anchor, scout=scout, dead=dead).items()}
    out = {}
    for a in range(0, edge + 5, 5):
        out[a] = per["scout"]
        if a >= edge:
            break
    out[edge] = max(out.get(edge, 0), per["dead"])
    out.update({0: per["anchor"], edge - 20: per["anchor"]})
    out.update({a: per["fine"] for a in range(edge - 12, edge)})
    return out


def p_setup_fail(atten, edge):
    return 1.0 if atten >= edge else float(sig((atten - edge + 0.5) / 0.7))


def p_drop(atten, edge):
    return 0.3 * float(sig((atten - edge + 1.0) / 0.7))


def sinr_at(atten, sir, edge):
    """ASSUMED: the attenuator lowers signal and interference together, not the receiver's noise."""
    snr0 = edge + EDGE_SINR_DB
    return float(-10 * np.log10(10 ** (-sir / 10) + 10 ** (-(snr0 - atten) / 10)))


def voice(rng, z):
    """(pesq_up, pesq_down, keywords) from latent score z; clear under the pre-registered rule iff z >= 0."""
    worst = 1.0 + 3.4 * sig(0.35 * z + np.log(2 / 1.4))              # 3.0 at z = 0
    worst = max(worst, 3.0) if z >= 0 else min(worst, 2.999)
    other = min(4.5, worst + abs(rng.normal(0, 0.15)))
    kw = (10 if rng.random() < sig(z) else 9) if z >= 0 else int(rng.binomial(10, sig(1 + z)))
    up, down = (worst, other) if rng.random() < 0.5 else (other, worst)
    return np.floor(up * 100 + 1e-9) / 100, np.floor(down * 100 + 1e-9) / 100, min(kw, 10 if z >= 0 else 9)


def demo_rows(seed=0, deltas=None, boxes=None, dates=DATES, fine=20, anchor=20, scout=4):
    """Rows for every box and date. deltas: {box: injected delta dB} overriding BOXES; trial counts are per step
    of each kind (voice, alarm), split between the dates."""
    rng = np.random.default_rng(seed)
    boxes = {b: dict(p, **({"delta": deltas[b]} if deltas and b in deltas else {}))
             for b, p in (boxes or BOXES).items()}
    rows, n, acct = [], 0, 0
    for bi, (box, p) in enumerate(boxes.items()):
        edge = p["edge"]
        a50v = p["a90_voice"] + SCALE_DB * np.log(9)
        a50a = a50v - p["delta"]
        plan = steps(edge, fine, anchor, scout, dates=len(dates))
        for day0 in dates:
            t = dt.datetime.fromisoformat(day0) + dt.timedelta(days=bi, hours=8)
            date, day = t.date().isoformat(), rng.normal(0, 0.4)
            for atten in plan:
                off = day + rng.normal(0, 0.3)                       # shared by voice and alarm at this step
                a_eff = atten - edge + off
                kinds = ["V"] * plan[atten] + ["A"] * plan[atten]
                rng.shuffle(kinds)
                for kind in kinds:
                    n += 1
                    sinr = sinr_at(atten + off, p["sir"], edge) + rng.normal(0, 0.7)
                    rsrp = 10 * np.log10(10 ** ((p["rsrp0"] - atten - off) / 10) + 10 ** (NOISE_FLOOR_DBM / 10))
                    r = dict.fromkeys(COLUMNS, "")
                    r.update(test_id=f"SYN-{n:05d}", date=date, utc_start=t.strftime("%Y-%m-%dT%H:%M:%SZ"), box=box,
                             atten_db=atten, rsrp_dbm=round(float(rsrp) + rng.normal(0, 1.0), 1), sinr_db=round(sinr, 1),
                             pci=p["pci"], earfcn=p["earfcn"], call_trial=int(kind == "V"), registered_21=1,
                             notes=NOTE, format="voice" if kind == "V" else "CID")
                    t += dt.timedelta(seconds=75 if kind == "V" else 45)
                    if kind == "A":
                        r["account"] = ("1234", "1111")[acct % 2]
                        acct += 1
                    if rng.random() < p_setup_fail(atten, edge):
                        r.update(setup_ok=0, fail_stage="setup", delivered=0 if kind == "A" else "")
                    elif rng.random() < p_drop(atten, edge):
                        r.update(setup_ok=1, fail_stage="drop", delivered=0 if kind == "A" else "")
                    elif kind == "V":
                        up, down, kw = voice(rng, (a50v - a_eff) / SCALE_DB + rng.logistic())
                        r.update(setup_ok=1, pesq_up=f"{up:.2f}", pesq_down=f"{down:.2f}", listener_keywords=kw)
                    else:
                        pa = float(sig((a50a - a_eff) / SCALE_DB))
                        ok = (a50a - a_eff) / SCALE_DB + rng.logistic() >= 0
                        used = (1 if rng.random() < FIRST_TRY_CEIL * pa else int(rng.choice([2, 3, 4], p=[.6, .3, .1]))
                                ) if ok else 4
                        r.update(setup_ok=1, fail_stage="" if ok else "no_kissoff", delivered=int(ok), attempts_used=used,
                                 kissoff_s=round(0.8 + used * 1.76 + (used - 1) * 1.25 + rng.normal(0, 0.05), 2)
                                 if ok else "")
                    rows.append(r)
    return rows


def write_csv(path, rows, columns=COLUMNS):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else OUT
    rows = demo_rows()
    write_csv(path, rows)
    print(f"wrote {len(rows)} SYNTHETIC rows to {path}; injected delta: "
          + ", ".join(f"{b} {p['delta']:+.1f} dB (A_edge {p['edge']} dB)" for b, p in BOXES.items()))
