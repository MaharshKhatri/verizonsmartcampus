#!/usr/bin/env python3
"""Summarize a field walk-test CSV (see deliverables/FIELD_KIT_OCT31.md).

    python3 scripts/analyze_walktest.py field_data/2026-10-31_shi.csv

Groups measurements by location and by 30-minute window, and writes a
markdown summary next to the CSV. Standard library only.
"""
import csv
import os
import statistics
import sys
from collections import defaultdict

NUMERIC = ("rsrp_dbm", "rsrq_db", "sinr_db", "down_mbps", "up_mbps", "latency_ms", "crowd_count_60s")


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _window(ts):
    """'2026-10-31 12:47' or '12:47' -> '12:30'."""
    hhmm = ts.strip().split()[-1][:5]
    try:
        h, m = int(hhmm[:2]), int(hhmm[3:5])
    except ValueError:
        return "unknown"
    return f"{h:02d}:{0 if m < 30 else 30:02d}"


def summarize(rows, key):
    groups = defaultdict(list)
    for r in rows:
        groups[key(r)].append(r)
    out = []
    for g, items in sorted(groups.items()):
        stats = {"group": g, "n": len(items)}
        for f in NUMERIC:
            vals = [x for x in (_num(i.get(f)) for i in items) if x is not None]
            stats[f] = round(statistics.median(vals), 1) if vals else None
        stats["wifi_ok_share"] = (sum(1 for i in items if (i.get("wifi_ok") or "").lower().startswith("y"))
                                  / len(items))
        stats["notes"] = "; ".join(i["notes"] for i in items if i.get("notes"))[:200]
        out.append(stats)
    return out


def table(stats, title):
    cols = ["group", "n", "rsrp_dbm", "sinr_db", "down_mbps", "up_mbps", "latency_ms", "crowd_count_60s"]
    lines = [f"### {title}", "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for s in stats:
        lines.append("| " + " | ".join("" if s.get(c) is None else str(s.get(c)) for c in cols) + " |")
    return "\n".join(lines)


def main(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.exit("no rows")
    by_loc = summarize(rows, lambda r: r.get("location", "?"))
    by_time = summarize(rows, lambda r: _window(r.get("timestamp", "")))
    by_carrier = summarize(rows, lambda r: r.get("phone_carrier", "?"))
    worst = sorted((r for r in rows if _num(r.get("down_mbps")) is not None), key=lambda r: _num(r["down_mbps"]))[:5]
    md = [f"# Walk-test summary: {os.path.basename(path)}", "", f"{len(rows)} measurements (medians shown).", "",
          table(by_loc, "By location"), "", table(by_time, "By 30-minute window"), "",
          table(by_carrier, "By carrier"), "", "### Five slowest measurements", ""]
    for r in worst:
        md.append(f"- {r.get('timestamp')} at {r.get('location')}: {r.get('down_mbps')} Mbps down, "
                  f"{r.get('latency_ms')} ms, {r.get('notes', '')}")
    out_path = os.path.splitext(path)[0] + "_summary.md"
    with open(out_path, "w") as fh:
        fh.write("\n".join(md) + "\n")
    print("\n".join(md))
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
