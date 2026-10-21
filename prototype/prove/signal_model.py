"""Learned SIGNAL threshold: P(alarm delivered on first try | box modem SINR, RSRQ).

The receipt's SIGNAL line should not be a guess about bars. It should come
from measured alarm delivery at measured signal. This module fits a small
logistic model with bootstrap intervals. Until the Rutgers bench produces real
rows (field_data/prove_lab.csv), `synthetic_rows` stands in, generated from the
alarm model in alarm.py with an ASSUMED SINR-to-frame-loss mapping, and every
output says so.
"""
import csv

import numpy as np

from . import alarm


def _loss_from_sinr(sinr):
    """ASSUMED mapping from SINR (dB) to voice-frame loss; replaced by bench data."""
    return float(np.clip(0.12 / (1 + np.exp((sinr - 3.0) / 1.8)), 0.0, 0.12))


def synthetic_rows(n=120, seed=21):
    rng = np.random.default_rng(seed)
    rows = []
    msg = alarm.contact_id()
    for _ in range(n):
        sinr = rng.uniform(-4, 16)
        rsrq = -9 - (16 - sinr) * 0.45 + rng.normal(0, 1.0)
        loss = _loss_from_sinr(sinr)

        def path(s, r):
            return alarm.voice_path(s, r, loss=loss, snr_db=18.0, level_jitter_db=1.5)
        hs = path(alarm.handshake(), rng)
        ok = (alarm.detect_tone(hs, 1400, 0.06) and alarm.detect_tone(hs, 2300, 0.06)
              and alarm.checksum_ok(alarm.decode_dtmf(path(alarm.dtmf(msg), rng)))
              and alarm.detect_tone(path(alarm.kissoff(), rng), 1400, 0.4))
        rows.append({"sinr_db": round(sinr, 1), "rsrq_db": round(rsrq, 1), "delivered_first_try": int(ok)})
    return rows


def load_rows(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        try:
            out.append({"sinr_db": float(r["sinr_db"]), "rsrq_db": float(r["rsrq_db"]),
                        "delivered_first_try": int(str(r.get("attempts_used", "1")).strip() == "1"
                                                   and str(r.get("delivered", "0")).strip().lower() in ("1", "true", "y", "yes"))})
        except (KeyError, ValueError):
            continue
    return out


def _fit(X, y, l2=1e-2, iters=60):
    """Newton-Raphson logistic regression with a small ridge penalty."""
    w = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w))
        g = X.T @ (p - y) + l2 * w
        H = X.T @ (X * (p * (1 - p))[:, None]) + l2 * np.eye(len(w))
        w -= np.linalg.solve(H, g)
    return w


def fit(rows, boot=200, seed=0):
    sinr = np.array([r["sinr_db"] for r in rows])
    y = np.array([r["delivered_first_try"] for r in rows], float)
    X = np.column_stack([np.ones_like(sinr), sinr])
    w = _fit(X, y)
    rng = np.random.default_rng(seed)
    ws = []
    for _ in range(boot):
        idx = rng.integers(0, len(y), len(y))
        if y[idx].min() == y[idx].max():
            continue
        ws.append(_fit(X[idx], y[idx]))
    ws = np.array(ws)

    def threshold(target, ww):
        return (np.log(target / (1 - target)) - ww[0]) / ww[1] if ww[1] > 0 else float("nan")

    t90 = threshold(0.9, w)
    lo, hi = np.nanpercentile([threshold(0.9, x) for x in ws], [2.5, 97.5]) if len(ws) else (np.nan, np.nan)
    grid = [(-2.0, None), (2.0, None), (6.0, None), (10.0, None)]
    curve = []
    for s, _ in grid:
        p = 1 / (1 + np.exp(-(w[0] + w[1] * s)))
        ps = 1 / (1 + np.exp(-(ws[:, 0] + ws[:, 1] * s))) if len(ws) else np.array([p])
        curve.append({"sinr_db": s, "p_first_try": round(float(p), 3),
                      "ci95": [round(float(np.percentile(ps, 2.5)), 3), round(float(np.percentile(ps, 97.5)), 3)]})
    return {"n": int(len(y)), "coef": [round(float(x), 3) for x in w],
            "sinr_for_90pct_first_try_db": round(float(t90), 1), "ci95_db": [round(float(lo), 1), round(float(hi), 1)],
            "curve": curve}


if __name__ == "__main__":
    import json
    import sys
    rows = load_rows(sys.argv[1]) if len(sys.argv) > 1 else synthetic_rows()
    src = sys.argv[1] if len(sys.argv) > 1 else "SYNTHETIC (alarm model + assumed SINR-to-loss mapping)"
    print(json.dumps({"source": src, **fit(rows)}, indent=1))
