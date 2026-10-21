#!/usr/bin/env python3
"""Summarize the PROVE Lab bench CSV (deliverables/PROVE_LAB_BENCH_PROTOCOL.md).

    python3 scripts/analyze_prove_lab.py field_data/prove_lab.csv

Reports delivery and first-try rates with Wilson 95% intervals per
arm x device x format x placement, the difference between the Verizon-box arm
and the LAN baseline, and (if signal columns exist) the learned SIGNAL threshold.
If the CSV has an `atten_db` column (the SMA attenuator sweep), it also reports
voice-clear vs alarm-confirmed per attenuation step, the "gap" steps, and a
matched-SINR comparison between boxes. Writes a markdown summary next to the CSV.

Optional sweep columns: atten_db, pesq (ITU-T P.862 MOS-LQO), listener_keywords
(out of 10 Harvard-sentence keywords), call_trial (1 = voice-call trial row).
"""
import csv
import math
import os
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

PESQ_CLEAR, KEYWORDS_CLEAR, GAP_RATE, BIN_DB = 3.0, 9, 0.9, 2.0
CLEAR_RULE = (f"Pre-registered rule: a call is clear if PESQ (ITU-T P.862 MOS-LQO) >= {PESQ_CLEAR:.1f}; "
              f"where PESQ was not measured, if a blinded listener got >= {KEYWORDS_CLEAR} of 10 "
              "Harvard-sentence keywords.")


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


def call_clear(r):
    """The pre-registered rule; None if the row has neither score."""
    p = num(r.get("pesq"))
    if p is not None:
        return p >= PESQ_CLEAR
    k = num(r.get("listener_keywords"))
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


def signal_rows(rows):
    """signal_model.load_rows, on alarm rows already in memory."""
    out = []
    for r in rows:
        try:
            out.append({"sinr_db": float(r["sinr_db"]), "rsrq_db": float(r["rsrq_db"]),
                        "delivered_first_try": int(str(r.get("attempts_used", "1")).strip() == "1"
                                                   and yes(r.get("delivered", "0")))})
        except (KeyError, ValueError, TypeError):
            continue
    return out


def _rate(flags):
    k, n = int(sum(flags)), len(flags)
    return {"k": k, "n": n, "rate": k / n if n else None, "ci": wilson(k, n)}


def reference_box(boxes):
    """Verizon's box is the reference; every other box is compared against it."""
    return next((b for b in boxes if "verizon" in b.lower()), sorted(boxes)[0])


def sweep_summary(rows, bin_db=BIN_DB):
    """Attenuation sweep: per box and step, call-clear vs alarm-confirmed; gap steps; matched-SINR comparison."""
    rows = [r for r in rows if num(r.get("atten_db")) is not None]
    boxes = sorted({r.get("box") or "?" for r in rows})
    ref = reference_box(boxes) if boxes else None
    boxes = sorted(boxes, key=lambda b: b != ref)       # reference box first
    out = {"rule": CLEAR_RULE, "reference_box": ref, "boxes": {}, "matched": []}
    for box in boxes:
        steps = defaultdict(list)
        for r in rows:
            if (r.get("box") or "?") == box:
                steps[num(r["atten_db"])].append(r)
        table = []
        for a in sorted(steps):
            rs = steps[a]
            sinr = [s for s in (num(r.get("sinr_db")) for r in rs) if s is not None]
            call = _rate([c for c in (call_clear(r) for r in rs if is_call(r)) if c is not None])
            alm = _rate([alarm_confirmed(r) for r in rs if not is_call(r)])
            gap = bool(call["n"] and alm["n"] and call["rate"] >= GAP_RATE and alm["rate"] < GAP_RATE)
            table.append({"atten_db": a, "median_sinr_db": statistics.median(sinr) if sinr else None,
                          "call_clear": call, "alarm_confirmed": alm, "gap": gap})
        gaps = [s for s in table if s["gap"]]
        gs = [s["median_sinr_db"] for s in gaps if s["median_sinr_db"] is not None]
        out["boxes"][box] = {"steps": table, "gap_atten_db": [s["atten_db"] for s in gaps],
                             "gap_sinr_db": [min(gs), max(gs)] if gs else None}
    bins = defaultdict(lambda: defaultdict(list))        # each alarm trial's own SINR, 2 dB bins
    for r in rows:
        s = num(r.get("sinr_db"))
        if not is_call(r) and s is not None:
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


def sweep_markdown(s):
    """Markdown lines for the sweep section."""
    md = ["", "### Attenuation sweep (voice clear vs alarm confirmed)", "", s["rule"],
          "Alarm confirmed: the receiver logged the event with a valid checksum and sent the kiss-off "
          "(`delivered` column), within the panel's attempts."]
    for box, b in s["boxes"].items():
        md += ["", f"#### {box}", "",
               "| Atten dB | Median SINR dB | Call clear (95% CI) | Alarm confirmed (95% CI) | Gap |",
               "|---:|---:|---|---|---|"]
        for st in b["steps"]:
            sinr = "n/a" if st["median_sinr_db"] is None else f"{st['median_sinr_db']:.1f}"
            c, a = st["call_clear"], st["alarm_confirmed"]
            md.append(f"| {st['atten_db']:g} | {sinr} | {kn(c['k'], c['n'])} | {kn(a['k'], a['n'])} | "
                      f"{'GAP' if st['gap'] else ''} |")
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
    md += ["", f"#### Matched-SINR comparison (alarm confirmed, {BIN_DB:g} dB SINR bins, each trial's own SINR)", ""]
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
        from prototype.prove import signal_model
        sm = signal_model.fit(signal_rows(alarm_rows))
        md += ["", f"### Learned SIGNAL threshold (n={sm['n']})", "",
               f"SINR for 90% first-try delivery: {sm['sinr_for_90pct_first_try_db']} dB "
               f"(95% CI {sm['ci95_db'][0]} to {sm['ci95_db'][1]} dB)."]
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
