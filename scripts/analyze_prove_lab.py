#!/usr/bin/env python3
"""Summarize the PROVE Lab bench CSV (deliverables/PROVE_LAB_BENCH_PROTOCOL.md).

    python3 scripts/analyze_prove_lab.py field_data/prove_lab.csv

Reports delivery and first-try rates with Wilson 95% intervals per
arm x device x format x placement, the difference between the Verizon-box arm
and the LAN baseline, and (if signal columns exist) the learned SIGNAL bar per box.
If the CSV has an `atten_db` column (the SMA attenuator sweep), the headline is
delta: how many dB more signal margin, above each box's own dropout, alarm
data needed than a clear voice call, with a cluster-bootstrap 95% CI. It also
keeps the per-step tables, the gap steps and (secondary) the matched-SINR
comparison. Writes a markdown summary next to the CSV.

Optional sweep columns: atten_db, date, pesq_up / pesq_down (ITU-T P.862.1 MOS-LQO
each way; older CSVs: one `pesq`), listener_keywords (out of 10 Harvard-sentence
keywords), call_trial (1 = voice-call trial row), setup_ok, fail_stage
('setup', 'drop', ...). Call-setup failures and drops are reported on their own
and never count as voice or alarm failures.
"""
import csv
import math
import os
import statistics
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from prototype.prove import signal_model  # noqa: E402
from prototype.prove.signal_model import answered, setup_failed  # noqa: E402

PESQ_CLEAR, PESQ_SENS, KEYWORDS_CLEAR, GAP_RATE, BIN_DB, BOOT = 3.0, 3.5, 9, 0.9, 2.0, 300
SINR_NOTE = ("SINR from two modems on two bands is not standardized; primary comparison is margin above each "
             "box's own dropout.")


def clear_rule(thr=PESQ_CLEAR):
    return (f"Pre-registered rule: a call is clear if PESQ MOS-LQO (ITU-T P.862.1) >= {thr:.1f} in both directions "
            f"(pesq_up, pesq_down) and, where scored, a blinded listener got >= {KEYWORDS_CLEAR} of 10 Harvard-sentence "
            f"keywords. Older CSVs with one `pesq` column: PESQ (ITU-T P.862 MOS-LQO) >= {thr:.1f}; where PESQ was not "
            f"measured, >= {KEYWORDS_CLEAR} of 10 keywords. Sensitivity analysis: the same rule at {PESQ_SENS:.1f}.")


CLEAR_RULE = clear_rule()


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def yes(v):
    return str(v).strip().lower() in ("1", "y", "yes", "true")


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def is_call(r):
    """Voice-call trial rows (call_trial = 1); everything else is an alarm trial."""
    return yes(r.get("call_trial"))


def call_clear(r, thr=PESQ_CLEAR):
    """The pre-registered rule; False if any measured part fails, None if the row cannot be rated."""
    up, down, k = num(r.get("pesq_up")), num(r.get("pesq_down")), num(r.get("listener_keywords"))
    if up is not None or down is not None:
        if not all([v >= thr for v in (up, down) if v is not None] + ([k >= KEYWORDS_CLEAR] if k is not None else [])):
            return False
        return True if up is not None and down is not None else None     # one direction passed: not rated
    p = num(r.get("pesq"))
    if p is not None:
        return p >= thr
    return None if k is None else k >= KEYWORDS_CLEAR


def alarm_confirmed(r):
    """The receiver logged the event with a valid checksum and kissed off (the `delivered` column)."""
    return yes(r.get("delivered"))


def kn(k, n):
    lo, hi = wilson(k, n)
    return f"{k}/{n} ({lo:.0%}-{hi:.0%})" if n else "n/a"


def arm_table(rows):
    """Markdown lines: per-arm delivery and first-try rates, and the difference from the LAN baseline."""
    groups = defaultdict(list)
    for r in rows:
        key = (r.get("box", "?"), r.get("device", "?"), r.get("format", "?"), r.get("placement", "?"))
        groups[key].append(r)
    md = ["| Arm / box | Device | Format | Placement | n | Delivered (95% CI) | First try (95% CI) | Median kiss-off s |",
          "|---|---|---|---|---:|---|---|---:|"]
    rates = {}
    for key, rs in sorted(groups.items()):
        n = len(rs)
        k = sum(yes(r.get("delivered")) for r in rs)
        f = sum(yes(r.get("delivered")) and str(r.get("attempts_used", "")).strip() == "1" for r in rs)
        ko = sorted(float(r["kissoff_s"]) for r in rs if r.get("kissoff_s") not in (None, "", "NA"))
        med = ko[len(ko) // 2] if ko else float("nan")
        rates[key] = k / n
        md.append(f"| {key[0]} | {key[1]} | {key[2]} | {key[3]} | {n} | {kn(k, n)} | {kn(f, n)} | {med:.1f} |")
    base = {k[1:]: v for k, v in rates.items() if "lan" in k[0].lower()}
    diffs = [(k, v - base[k[1:]]) for k, v in rates.items() if "lan" not in k[0].lower() and k[1:] in base]
    if diffs:
        md += ["", "### Difference from the LAN baseline (same device, format, placement)", ""]
        md += [f"- {k[0]} / {k[1]} / {k[2]} / {k[3]}: {d:+.0%}" for k, d in diffs]
    return md


def reference_box(boxes):
    """Verizon's box is the reference; every other box is compared against it."""
    return next((b for b in boxes if "verizon" in b.lower()), sorted(boxes)[0])


def signal_markdown(rows, boot=200):
    """Learned SIGNAL bar per box, on signal_model's filtered rows (Contact ID alarm, registered, answered)."""
    boxes = sorted({r.get("box") or "" for r in rows})
    ref = reference_box(boxes)
    md = ["", "### Learned SIGNAL threshold", "",
          "SINR at which an alarm is confirmed on the first try 90% of the time, per box: Contact ID alarm trials on "
          "a registered box whose call was answered. Logistic in SINR only; 95% CI from a (date, atten_db) cluster "
          "bootstrap when those columns exist."]
    for box in sorted(boxes, key=lambda b: b != ref):
        why = {}
        rs = signal_model.filter_rows(rows, box, why)
        cells = {r["cell"] for r in rs if any(r["cell"])}
        cell = "one cell" if len(cells) == 1 else f"{len(cells)} cells" if cells else "cell not logged"
        head = f"- n = {len(rs)} bench alarm tests (box {box or '?'}, {cell})"
        left = ", ".join(f"{v} {k}" for k, v in sorted(why.items()) if k != "other box") or "none"
        if len(rs) < 10 or len({r["delivered_first_try"] for r in rs}) < 2:
            md += [head + ": too few rows, or no variation in first-try confirmation, to fit a bar.",
                   f"  - Excluded rows: {left}."]
            continue
        a, b = signal_model.fit(rs, boot=boot), signal_model.fit(rs, boot=boot, ceiling=True)
        md += [head + f". SINR for 90% first-try confirmation: {a['sinr_for_90pct_first_try_db']} dB "
               f"(95% CI {a['ci95_db'][0]} to {a['ci95_db'][1]} dB; bootstrap: {a['bootstrap']}).",
               f"  - With a ceiling c = {b['ceiling']:.2f} (first-try rate in the strongest-signal decile): SINR where "
               f"p = 0.9c = {b['target_p']:.2f}: {b['sinr_for_90pct_first_try_db']} dB "
               f"(95% CI {b['ci95_db'][0]} to {b['ci95_db'][1]} dB).",
               f"  - Excluded rows: {left}."]
    return md


def a_edge(rs):
    """(dropout step, found): the smallest atten_db where call setup failed on every trial; else the largest step."""
    by = defaultdict(list)
    for r in rs:
        by[num(r["atten_db"])].append(setup_failed(r))
    dead = [a for a, f in by.items() if all(f)]
    return (min(dead), True) if dead else (max(by), False)


def a90(x, k, n, target=GAP_RATE, l2=1e-3):
    """A_rel where a binomial logistic fit of k/n on x falls to `target`; nan if the fitted curve does not fall."""
    m = n > 0
    x, k, n = x[m], k[m], n[m]
    if not len(x) or k.sum() in (0, n.sum()):
        return float("nan")
    xm = float(np.average(x, weights=n))
    X = np.column_stack([np.ones_like(x), x - xm])
    w = np.zeros(2)
    for _ in range(60):
        p = 1 / (1 + np.exp(-np.clip(X @ w, -35, 35)))
        step = np.linalg.solve(X.T @ (X * (n * p * (1 - p))[:, None]) + l2 * np.eye(2), X.T @ (k - n * p) - l2 * w)
        w += step
        if np.max(np.abs(step)) < 1e-9:
            break
    return xm + (math.log(target / (1 - target)) - w[0]) / w[1] if w[1] < 0 else float("nan")


def margin(rs, boot=BOOT, seed=0):
    """One box: A_edge, then on answered trials the A90 of voice-clear and alarm-confirmed curves in A_rel,
    delta = A90_voice - A90_alarm, the same at PESQ 3.5, and the call-setup curve, with a cluster bootstrap that
    resamples (date, atten_db) clusters (voice and alarm resampled together)."""
    edge, found = a_edge(rs)
    keys = sorted({(r.get("date") or "", num(r["atten_db"])) for r in rs})
    pos = {k: i for i, k in enumerate(keys)}
    x = np.array([a - edge for _, a in keys])
    M = np.zeros((len(keys), 8))          # clear k, n | clear at 3.5 k, n | alarm k, n | answered k, trials n
    for r in rs:
        i = pos[(r.get("date") or "", num(r["atten_db"]))]
        M[i, 7] += 1
        if not answered(r):
            continue
        M[i, 6] += 1
        if is_call(r):
            for j, thr in ((0, PESQ_CLEAR), (2, PESQ_SENS)):
                c = call_clear(r, thr)
                if c is not None:
                    M[i, j:j + 2] += (c, 1)
        else:
            M[i, 4:6] += (alarm_confirmed(r), 1)

    def est(wt):
        S = M * wt[:, None]
        v, s, a, u = (a90(x, S[:, j], S[:, j + 1]) for j in (0, 2, 4, 6))
        return [v, a, v - a, s - a, u]

    full = est(np.ones(len(keys)))
    rng = np.random.default_rng(seed)
    reps = np.array([est(np.bincount(rng.integers(0, len(keys), len(keys)), minlength=len(keys)).astype(float))
                     for _ in range(boot)])
    with np.errstate(all="ignore"):
        ci = [[float(v) for v in np.nanpercentile(reps[:, j], [2.5, 97.5])] if np.isfinite(reps[:, j]).any()
              else [float("nan")] * 2 for j in range(5)]
    names = ("a90_voice", "a90_alarm", "delta", "delta_pesq35", "a90_setup")
    out = {"a_edge": edge, "edge_found": found, "clusters": len(keys), "boot": boot,
           "n_voice": int(M[:, 1].sum()), "n_alarm": int(M[:, 5].sum()), "n_trials": int(M[:, 7].sum()),
           "failed_draws": int(np.isnan(reps[:, 2]).sum())}
    seen = x[(M[:, 1] + M[:, 5]) > 0]                   # steps with answered voice or alarm trials
    out["tested"] = [float(seen.min()), float(seen.max())] if len(seen) else None
    for j, name in enumerate(names):
        out[name], out[name + "_ci"] = full[j], ci[j]
    for d in ("delta", "delta_pesq35"):
        lo = out[d + "_ci"][0]
        out[d.replace("delta", "gap")] = (None if not (math.isfinite(out[d]) and math.isfinite(lo)) else bool(lo > 0))
    return out


def _rate(flags):
    k, n = int(sum(flags)), len(flags)
    return {"k": k, "n": n, "rate": k / n if n else None, "ci": wilson(k, n)}


def sweep_summary(rows, bin_db=BIN_DB, boot=BOOT, seed=0):
    """Attenuation sweep: per box the margin estimand (delta), per-step tables on answered trials,
    gap steps, call setup; across boxes the cross-box verdict and the (secondary) matched-SINR comparison."""
    rows = [r for r in rows if num(r.get("atten_db")) is not None]
    cols = set().union(*rows) if rows else set()
    boxes = sorted({r.get("box") or "?" for r in rows})
    ref = reference_box(boxes) if boxes else None
    boxes = sorted(boxes, key=lambda b: b != ref)       # reference box first
    out = {"rule": CLEAR_RULE, "reference_box": ref, "boxes": {}, "matched": [],
           "has_setup": bool({"setup_ok", "fail_stage"} & cols), "has_fail_stage": "fail_stage" in cols}
    for box in boxes:
        brs = [r for r in rows if (r.get("box") or "?") == box]
        m = margin(brs, boot, seed)
        steps = defaultdict(list)
        for r in brs:
            steps[num(r["atten_db"])].append(r)
        table = []
        for a in sorted(steps):
            rs = steps[a]
            ans = [r for r in rs if answered(r)]
            sinr = [s for s in (num(r.get("sinr_db")) for r in rs) if s is not None]
            call = _rate([c for c in (call_clear(r) for r in ans if is_call(r)) if c is not None])
            alm = _rate([alarm_confirmed(r) for r in ans if not is_call(r)])
            gap = bool(call["n"] and alm["n"] and call["rate"] >= GAP_RATE and alm["rate"] < GAP_RATE)
            stages = Counter(str(r.get("fail_stage") or "").strip() for r in rs)
            stages.pop("", None)
            table.append({"atten_db": a, "a_rel_db": a - m["a_edge"],
                          "median_sinr_db": statistics.median(sinr) if sinr else None,
                          "call_clear": call, "alarm_confirmed": alm, "gap": gap, "trials": len(rs),
                          "setup_failed": sum(setup_failed(r) for r in rs), "answered": _rate([answered(r) for r in rs]),
                          "dropped": sum(str(r.get("fail_stage") or "").strip().lower() == "drop" for r in rs),
                          "fail_stages": dict(sorted(stages.items()))})
        gaps = [s for s in table if s["gap"]]
        gs = [s["median_sinr_db"] for s in gaps if s["median_sinr_db"] is not None]
        out["boxes"][box] = {"steps": table, "gap_atten_db": [s["atten_db"] for s in gaps],
                             "gap_sinr_db": [min(gs), max(gs)] if gs else None, "margin": m}
    gapped = [b for b in boxes if out["boxes"][b]["margin"]["gap"]]
    out["cross"] = {"boxes": boxes, "gap_boxes": gapped, "same_pattern": len(boxes) > 1 and len(gapped) == len(boxes)}
    bins = defaultdict(lambda: defaultdict(list))        # each answered alarm trial's own SINR, 2 dB bins
    for r in rows:
        s = num(r.get("sinr_db"))
        if not is_call(r) and s is not None and answered(r):
            bins[math.floor(s / bin_db) * bin_db][r.get("box") or "?"].append(alarm_confirmed(r))
    for lo in sorted(bins):
        for other in boxes:
            if other == ref or ref not in bins[lo] or other not in bins[lo]:
                continue
            a, b = _rate(bins[lo][ref]), _rate(bins[lo][other])
            out["matched"].append({"sinr_lo": lo, "sinr_hi": lo + bin_db, "other_box": other, "ref": a, "other": b,
                                   "diff": b["rate"] - a["rate"],
                                   "same": a["ci"][0] <= b["ci"][1] and b["ci"][0] <= a["ci"][1]})
    return out


def _db(v):
    return "n/a" if v is None or not math.isfinite(v) else f"{v:.1f}".replace("-0.0", "0.0")


def _ci(c):
    return f"95% CI {_db(c[0])} to {_db(c[1])}"


def delta_line(box, m):
    """The one plain-English headline line per box."""
    n = f"n = {m['n_voice']} voice + {m['n_alarm']} alarm answered trials"
    d = m["delta"]
    if not math.isfinite(d):
        why = ("the voice-clear curve" if not math.isfinite(m["a90_voice"]) else "the alarm-confirmed curve")
        return f"{box}: delta not estimable; {why} never fell to 90% in the tested range ({n}). Gap: not estimable."
    verdict = "not estimable" if m["gap"] is None else ("yes" if m["gap"] else "no")
    return (f"{box}: alarm data needed {abs(d):.1f} dB {'more' if d >= 0 else 'less'} signal than a clear call "
            f"(95% CI {_db(m['delta_ci'][0])} to {_db(m['delta_ci'][1])}; {n}). Gap: {verdict}.")


def margin_markdown(s):
    """Headline section: delta per box, sensitivity at PESQ 3.5, call setup, cross-box verdict."""
    md = ["", "#### Headline: delta, the dB margin (primary)", "",
          "A_edge is each box's dropout: the smallest attenuation step at which call setup failed on every trial "
          "(else the largest step tested). A_rel = atten_db - A_edge, dB below that box's own dropout. On answered "
          "trials only, logistic curves in A_rel give A90, where voice-clear (call_trial=1) and alarm-confirmed "
          "(call_trial=0) each fall to 90%. delta = A90_voice - A90_alarm: positive means alarm data needs delta dB "
          f"more signal margin than a clear call. 95% CI: cluster bootstrap over (date, atten_db), {BOOT} draws, "
          "fixed seed. A gap counts only if the CI's lower bound is above 0 dB.", ""]
    for box, b in s["boxes"].items():
        m = b["margin"]
        md.append("- " + delta_line(box, m))
        edge = f"A_edge {m['a_edge']:g} dB" + ("" if m["edge_found"] else " (no step lost service on every trial; "
                                                "largest step tested)")
        md.append(f"  - {edge}; A90 voice {_db(m['a90_voice'])} dB ({_ci(m['a90_voice_ci'])}), A90 alarm "
                  f"{_db(m['a90_alarm'])} dB ({_ci(m['a90_alarm_ci'])}); {m['clusters']} (date, step) clusters.")
        if m["tested"] and any(math.isfinite(v) and not m["tested"][0] <= v <= m["tested"][1]
                               for v in (m["a90_voice"], m["a90_alarm"])):
            md.append(f"  - An A90 lies outside the answered steps ({m['tested'][0]:g} to {m['tested'][1]:g} dB A_rel): "
                      "extrapolated.")
        if m["failed_draws"]:
            md.append(f"  - {m['failed_draws']} of {m['boot']} bootstrap draws had a curve that never fell to 90%; "
                      "the CI uses the rest.")
        g = m["gap_pesq35"]
        md.append(f"  - Sensitivity, PESQ threshold {PESQ_SENS:.1f}: delta {_db(m['delta_pesq35'])} dB "
                  f"({_ci(m['delta_pesq35_ci'])}). Gap: {'not estimable' if g is None else 'yes' if g else 'no'}.")
        if s["has_setup"]:
            md.append(f"  - Call setup (connected and not dropped) holds at 90% down to A_rel {_db(m['a90_setup'])} dB "
                      f"({_ci(m['a90_setup_ci'])}). Setup failures and drops are not counted as voice or alarm failures.")
    c = s["cross"]
    if len(c["boxes"]) > 1:
        md += ["", "Cross-box: " + "; ".join(f"{b} delta {_db(s['boxes'][b]['margin']['delta'])} dB "
                                             f"({_ci(s['boxes'][b]['margin']['delta_ci'])})" for b in c["boxes"]) + "."]
        if c["same_pattern"]:
            md.append("Same pattern: every box shows a gap (alarm data needed more margin than a clear call).")
        else:
            who = ", ".join(c["gap_boxes"]) or "no box"
            md.append(f"Not shown to be the same pattern: only {who} shows a gap." if c["gap_boxes"]
                      else "No box shows a gap, so there is no pattern to compare.")
        md.append("Overlapping delta CIs are NOT evidence that the boxes behave the same; they only mean this "
                  "sample cannot tell them apart.")
    return md


def sweep_markdown(s):
    """Markdown lines for the sweep section."""
    md = ["", "### Attenuation sweep (voice clear vs alarm confirmed)", "", s["rule"],
          "Alarm confirmed: the receiver logged the event with a valid checksum and sent the kiss-off "
          "(`delivered` column), within the panel's attempts."]
    md += margin_markdown(s)
    fs = s["has_fail_stage"]
    for box, b in s["boxes"].items():
        md += ["", f"#### {box}: per step (answered trials)", "",
               "| Atten dB | A_rel dB | Median SINR dB | Call clear (95% CI) | Alarm confirmed (95% CI) | Gap |"
               + (" Fail stages |" if fs else ""), "|---:|---:|---:|---|---|---|" + ("---|" if fs else "")]
        for st in b["steps"]:
            sinr = "n/a" if st["median_sinr_db"] is None else f"{st['median_sinr_db']:.1f}"
            c, a = st["call_clear"], st["alarm_confirmed"]
            stages = ", ".join(f"{k} {v}" for k, v in st["fail_stages"].items())
            md.append(f"| {st['atten_db']:g} | {st['a_rel_db']:g} | {sinr} | {kn(c['k'], c['n'])} | "
                      f"{kn(a['k'], a['n'])} | {'GAP' if st['gap'] else ''} |" + (f" {stages} |" if fs else ""))
        if s["has_setup"]:
            md += ["", f"#### {box}: call setup and drops (reported separately)", "",
                   "| Atten dB | A_rel dB | Trials | Setup failed | Dropped | Answered (95% CI) |",
                   "|---:|---:|---:|---:|---:|---|"]
            for st in b["steps"]:
                u = st["answered"]
                md.append(f"| {st['atten_db']:g} | {st['a_rel_db']:g} | {st['trials']} | {st['setup_failed']} | "
                          f"{st['dropped']} | {kn(u['k'], u['n'])} |")
    md += ["", f"#### Gap steps (calls clear in >= {GAP_RATE:.0%} of trials, alarm confirmed in < {GAP_RATE:.0%})", ""]
    for box, b in s["boxes"].items():
        if not b["gap_atten_db"]:
            md.append(f"- {box}: no gap steps.")
            continue
        steps = ", ".join(f"{a:g}" for a in b["gap_atten_db"])
        rng = b["gap_sinr_db"]
        where = "SINR n/a" if rng is None else (f"SINR {rng[0]:.1f} dB" if rng[0] == rng[1]
                                                else f"SINR {rng[0]:.1f} to {rng[1]:.1f} dB")
        n = len(b["gap_atten_db"])
        md.append(f"- {box}: {n} gap step{'s' * (n != 1)} at {steps} dB attenuation; {where} (step medians). "
                  "Voice sounded fine there, but the alarm was not reliably confirmed.")
    md += ["", f"#### Matched-SINR comparison (secondary: alarm confirmed, {BIN_DB:g} dB SINR bins, each answered "
           "trial's own SINR)", "", SINR_NOTE, ""]
    if not s["matched"]:
        md.append("- No SINR bin has alarm trials from more than one box.")
    ref = s["reference_box"]
    for m in s["matched"]:
        a, b = m["ref"], m["other"]
        few = " (few trials, wide CIs)" if min(a["n"], b["n"]) < 5 else ""
        verdict = ("did the same (95% CIs overlap)" if m["same"] else
                   f"did not do the same: it confirmed {'more' if m['diff'] > 0 else 'less'} often (95% CIs do not overlap)")
        md.append(f"- SINR {m['sinr_lo']:g} to {m['sinr_hi']:g} dB: {ref} {kn(a['k'], a['n'])}, "
                  f"{m['other_box']} {kn(b['k'], b['n'])}, difference {100 * m['diff']:+.0f} pts. "
                  f"The other carrier's box {verdict}{few}.")
    if s["matched"]:
        same = sum(m["same"] for m in s["matched"])
        md += ["", f"Overall: the other carrier's box did the same in {same} of {len(s['matched'])} matched bins. "
               "Overlapping CIs mean no clear difference at this sample size, not proof that the boxes are equal."]
    return md


def main(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.exit("no rows")
    alarm_rows = [r for r in rows if not is_call(r)]
    md = [f"# PROVE Lab summary: {os.path.basename(path)}", ""]
    if any("SYNTHETIC" in (r.get("notes") or "") for r in rows):
        md += ["**SYNTHETIC DATA: for rehearsing the analysis only. Not a measurement.**", ""]
    calls = len(rows) - len(alarm_rows)
    md += [f"{len(rows)} trials." if not calls else f"{len(rows)} trials ({len(alarm_rows)} alarm, {calls} voice call).", ""]
    md += arm_table(alarm_rows)
    if rows and "sinr_db" in rows[0]:
        md += signal_markdown(rows)
    if rows and "atten_db" in rows[0]:
        md += sweep_markdown(sweep_summary(rows))
    md += ["", "Report nulls. Send any failure to the Verizon mentor before publishing."]
    out = os.path.splitext(path)[0] + "_summary.md"
    with open(out, "w") as fh:
        fh.write("\n".join(md) + "\n")
    print("\n".join(md))
    print(f"\nwrote {out}")
    return md


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
