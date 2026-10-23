"""Learned SIGNAL bar: P(alarm confirmed on the first try | box modem SINR), one box, one cell.

The receipt's SIGNAL line should not be a guess about bars. It should come
from measured alarm delivery at measured signal. This module fits a small
logistic model in SINR only (RSRQ is carried through when logged but is not a
feature; nothing here models season or placement) with bootstrap intervals.
Until the Rutgers bench produces real rows (field_data/prove_lab.csv),
`synthetic_rows` stands in, generated from the alarm model in alarm.py with an
ASSUMED SINR-to-frame-loss mapping, and every output says so.

Rows used (`filter_rows`): Contact ID alarm trials (call_trial 0 or blank,
format CID or blank) on a registered box (registered_21 truthy, or no such
column), from one box when one is named, whose call was answered (call setup
neither failed nor dropped). Voice, SIA, 4/2, unregistered and no-setup rows
never move the bar.

Optional ceiling (`fit(..., ceiling=True)`): p = c * sigmoid(a + b * sinr),
with c fixed to the box's first-try rate in its strongest-signal decile
(capped at 1.0, re-estimated in each bootstrap draw). The bar is then the SINR
where p = 0.9 * c, i.e. 90% of what that box achieves at its best signal. This
keeps a box that needs a resend now and then at any signal from pulling the
bar off the end of the tested range.
"""
import csv
import math

import numpy as np

from . import alarm

CID_FORMATS = {"cid", "contact id", "contact_id"}
CLUSTER = ("date", "atten_db")


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


def _yes(v):
    return str(v).strip().lower() in ("1", "y", "yes", "true")


def _blank(v):
    return v is None or str(v).strip() == ""


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def setup_failed(r):
    """Call setup failed: setup_ok = 0 when logged, else fail_stage 'setup' or 'drop'."""
    if not _blank(r.get("setup_ok")):
        return not _yes(r["setup_ok"])
    return str(r.get("fail_stage") or "").strip().lower() in ("setup", "drop")


def answered(r):
    """The call connected and did not drop; only these rows can count as voice or alarm outcomes."""
    return not setup_failed(r) and str(r.get("fail_stage") or "").strip().lower() != "drop"


def keep(r, box=None):
    """None if the row belongs in the bar, else why it does not."""
    if str(r.get("call_trial") or "").strip().lower() not in ("", "0", "0.0", "n", "no", "false"):
        return "voice"
    if not _blank(r.get("format")) and str(r["format"]).strip().lower() not in CID_FORMATS:
        return "not Contact ID"
    if "registered_21" in r and not _yes(r["registered_21"]):
        return "not registered"
    if box is not None and (r.get("box") or "") != box:
        return "other box"
    if not answered(r):
        return "setup failed or dropped"
    if _num(r.get("sinr_db")) is None:
        return "no SINR"
    return None


def filter_rows(rows, box=None, why=None):
    """CSV dict rows -> model rows (see the module docstring). `why`, a dict, collects exclusion counts."""
    out = []
    for r in rows:
        reason = keep(r, box)
        if reason:
            if why is not None:
                why[reason] = why.get(reason, 0) + 1
            continue
        out.append({"sinr_db": float(r["sinr_db"]), "rsrq_db": _num(r.get("rsrq_db")),
                    "delivered_first_try": int(str(r.get("attempts_used", "1")).strip() == "1" and _yes(r.get("delivered"))),
                    "date": r.get("date"), "atten_db": _num(r.get("atten_db")),
                    "cell": (r.get("pci") or "", r.get("earfcn") or "")})
    return out


def load_rows(path, box=None):
    """Filtered model rows from a bench CSV; len() of the result is the filtered n."""
    with open(path, newline="") as fh:
        return filter_rows(csv.DictReader(fh), box)


def _fit(X, y, l2=1e-2, iters=60, c=1.0):
    """Logistic regression (Newton / Fisher scoring) with a small ridge; p = c * sigmoid(X @ w)."""
    w = np.zeros(X.shape[1])
    for _ in range(iters):
        s = 1 / (1 + np.exp(-np.clip(X @ w, -35, 35)))
        q = 1 - c * s
        g = X.T @ ((y - c * s) * (1 - s) / q) - l2 * w
        H = X.T @ (X * (c * s * (1 - s) ** 2 / q)[:, None]) + l2 * np.eye(len(w))
        step = np.linalg.solve(H, g)
        w += step
        if np.max(np.abs(step)) < 1e-9:
            break
    return w


def ceiling_of(sinr, y):
    """First-try rate in the strongest-signal decile (at least 5 rows), capped at 1.0."""
    top = sinr >= np.percentile(sinr, 90)
    if top.sum() < 5:
        top = np.argsort(sinr)[-5:]
    return float(min(1.0, max(np.mean(y[top]), 0.05)))


def fit(rows, boot=200, seed=0, cluster_key=None, ceiling=False):
    """Fit and bootstrap. cluster_key: row keys resampled together (default ('date', 'atten_db') when every
    row carries both, else single rows). ceiling: see the module docstring."""
    sinr = np.array([r["sinr_db"] for r in rows], float)
    y = np.array([r["delivered_first_try"] for r in rows], float)
    X = np.column_stack([np.ones_like(sinr), sinr])
    if cluster_key is None and rows and all(r.get(k) not in (None, "") for r in rows for k in CLUSTER):
        cluster_key = CLUSTER
    keys = [tuple(r[k] for k in cluster_key) for r in rows] if cluster_key else list(range(len(rows)))
    groups = {}
    for i, k in enumerate(keys):
        groups.setdefault(k, []).append(i)
    members = [np.array(groups[k]) for k in sorted(groups, key=str)]
    c = ceiling_of(sinr, y) if ceiling else 1.0
    w = _fit(X, y, c=c)
    rng = np.random.default_rng(seed)
    ws, cs = [], []
    for _ in range(boot):
        draw = rng.integers(0, len(members), len(members))
        idx = np.concatenate([members[j] for j in draw]) if cluster_key else draw
        if y[idx].min() == y[idx].max():
            continue
        cb = ceiling_of(sinr[idx], y[idx]) if ceiling else 1.0
        ws.append(_fit(X[idx], y[idx], c=cb))
        cs.append(cb)
    ws, cs = np.array(ws), np.array(cs)

    def threshold(target, ww):
        return (math.log(target / (1 - target)) - ww[0]) / ww[1] if ww[1] > 0 else float("nan")

    t90 = threshold(0.9, w)
    lo, hi = np.nanpercentile([threshold(0.9, x) for x in ws], [2.5, 97.5]) if len(ws) else (np.nan, np.nan)
    curve = []
    for s in (-2.0, 2.0, 6.0, 10.0):
        p = c / (1 + np.exp(-np.clip(w[0] + w[1] * s, -35, 35)))
        ps = cs / (1 + np.exp(-np.clip(ws[:, 0] + ws[:, 1] * s, -35, 35))) if len(ws) else np.array([p])
        curve.append({"sinr_db": s, "p_first_try": round(float(p), 3),
                      "ci95": [round(float(np.percentile(ps, 2.5)), 3), round(float(np.percentile(ps, 97.5)), 3)]})
    return {"n": int(len(y)), "coef": [round(float(x), 3) for x in w],
            "sinr_for_90pct_first_try_db": round(float(t90), 1), "ci95_db": [round(float(lo), 1), round(float(hi), 1)],
            "ceiling": round(c, 3), "target_p": round(0.9 * c, 3),
            "bootstrap": f"{'cluster ' + '+'.join(cluster_key) if cluster_key else 'row'}, {len(members)} units, "
                         f"{len(ws)} draws",
            "curve": curve}


if __name__ == "__main__":
    import json
    import sys
    path, box = (sys.argv[1:] + [None, None])[:2]
    rows = load_rows(path, box) if path else synthetic_rows()
    src = path or "SYNTHETIC (alarm model + assumed SINR-to-loss mapping)"
    print(json.dumps({"source": src, "box": box, "plain": fit(rows), "with_ceiling": fit(rows, ceiling=True)},
                     indent=1))
