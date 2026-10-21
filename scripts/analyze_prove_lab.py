#!/usr/bin/env python3
"""Summarize the PROVE Lab bench CSV (deliverables/PROVE_LAB_BENCH_PROTOCOL.md).

    python3 scripts/analyze_prove_lab.py field_data/prove_lab.csv

Reports delivery and first-try rates with Wilson 95% intervals per
arm x device x format x placement, the difference between the Verizon-box arm
and the LAN baseline, and (if signal columns exist) the learned SIGNAL threshold.
Writes a markdown summary next to the CSV.
"""
import csv
import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


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


def main(path):
    rows = list(csv.DictReader(open(path, newline="")))
    if not rows:
        sys.exit("no rows")
    groups = defaultdict(list)
    for r in rows:
        key = (r.get("box", "?"), r.get("device", "?"), r.get("format", "?"), r.get("placement", "?"))
        groups[key].append(r)
    md = [f"# PROVE Lab summary: {os.path.basename(path)}", "", f"{len(rows)} trials.", "",
          "| Arm / box | Device | Format | Placement | n | Delivered (95% CI) | First try (95% CI) | Median kiss-off s |",
          "|---|---|---|---|---:|---|---|---:|"]
    rates = {}
    for key, rs in sorted(groups.items()):
        n = len(rs)
        k = sum(yes(r.get("delivered")) for r in rs)
        f = sum(yes(r.get("delivered")) and str(r.get("attempts_used", "")).strip() == "1" for r in rs)
        ko = sorted(float(r["kissoff_s"]) for r in rs if r.get("kissoff_s") not in (None, "", "NA"))
        med = ko[len(ko) // 2] if ko else float("nan")
        lo, hi = wilson(k, n)
        flo, fhi = wilson(f, n)
        rates[key] = k / n
        md.append(f"| {key[0]} | {key[1]} | {key[2]} | {key[3]} | {n} | {k}/{n} ({lo:.0%}-{hi:.0%}) | "
                  f"{f}/{n} ({flo:.0%}-{fhi:.0%}) | {med:.1f} |")
    base = {k[1:]: v for k, v in rates.items() if "lan" in k[0].lower()}
    diffs = [(k, v - base[k[1:]]) for k, v in rates.items() if "lan" not in k[0].lower() and k[1:] in base]
    if diffs:
        md += ["", "### Difference from the LAN baseline (same device, format, placement)", ""]
        md += [f"- {k[0]} / {k[1]} / {k[2]} / {k[3]}: {d:+.0%}" for k, d in diffs]
    if rows and "sinr_db" in rows[0]:
        from prototype.prove import signal_model
        sm = signal_model.fit(signal_model.load_rows(path))
        md += ["", f"### Learned SIGNAL threshold (n={sm['n']})", "",
               f"SINR for 90% first-try delivery: {sm['sinr_for_90pct_first_try_db']} dB "
               f"(95% CI {sm['ci95_db'][0]} to {sm['ci95_db'][1]} dB)."]
    md += ["", "Report nulls. Send any failure to the Verizon mentor before publishing."]
    out = os.path.splitext(path)[0] + "_summary.md"
    open(out, "w").write("\n".join(md) + "\n")
    print("\n".join(md))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
