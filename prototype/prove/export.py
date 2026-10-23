"""Build the PROVE console's offline data file (console/data.js) and a JSON copy.

    python3 -m prototype.prove.export
"""
import json
import os
import re

from . import acoustic, alarm, answer, fleet, install, migration, supervisor, triage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
NOTICE_TXT = os.path.join(ROOT, "research", "sources", "verizon_nj_copper_retirement_notice_2026-03-A-NJ.txt")
NATIONAL_CSV = os.path.join(ROOT, "research", "sources", "verizon_frontier_copper_retirement_wire_centers_2026.csv")
OUT_JS = os.path.join(HERE, "console", "data.js")
OUT_JSON = os.path.join(ROOT, "prototype", "out", "prove_evidence.json")


def wire_centers():
    """Parse (name, address, CLLI) rows from the public notice text."""
    rows = []
    if not os.path.exists(NOTICE_TXT):
        return rows
    for line in open(NOTICE_TXT, encoding="utf-8"):
        m = re.match(r"^\s*(.+?)\s{2,}(.+?, NJ \d{5})\s+([A-Z0-9]{8})\s*$", line)
        if m:
            rows.append({"name": m.group(1).strip(), "address": m.group(2).strip(), "clli": m.group(3)})
    return rows


def national():
    """2026 Verizon + Frontier copper-retirement wire centers by state (public notices only)."""
    import csv
    from collections import Counter, defaultdict
    if not os.path.exists(NATIONAL_CSV):
        return {}
    rows = list(csv.DictReader(open(NATIONAL_CSV, encoding="utf-8")))
    by_state = Counter(r["clli"][4:6] for r in rows)
    dates = defaultdict(set)
    for r in rows:
        dates[r["clli"][4:6]].add(r["implementation"])
    return {"total": len({r["clli"] for r in rows}), "notices": len({r["notice_id"] for r in rows}),
            "states": {s: {"n": n, "dates": sorted(dates[s])} for s, n in by_state.items()},
            "source": "Verizon network disclosures and Frontier wholesale notices under 47 CFR 51.333, 2026"}


def answer_block():
    reg = answer.Registry()
    calls = {
        "A person answers in 12 s": (reg.answerer_number, "person", 12, reg.label),
        "Voicemail picks up": (reg.answerer_number, "voicemail", 24, None),
        "Dials the old contractor": ("8005550199", "person", 9, reg.label),
        "Answered after 52 s": (reg.answerer_number, "person", 52, reg.label),
        "Screen says Nashville, TN": (reg.answerer_number, "person", 8, "Nashville, TN"),
        "Number not in service": (reg.answerer_number, "intercept", 1, None),
    }
    out = {k: answer.check_call(*v, reg) for k, v in calls.items()}
    return {"calls": out, "honest": answer.honest_eval(trials=12), "label": reg.label}


SCENARIOS = {
    "healthy":        {},
    "copper_cut":     {"on_copper": True},
    "antenna":        {"antenna": False},
    "mains":          {"mains": False},
    "speaker":        {"speaker_gain": 0.0},
    "mic_taped":      {"mic_taped": True},
    "wrong_label":    {"reported_label": "1 Main St (gateway default address)"},
    "no_answer":      {"answer_point_ok": False},
}


def scenario_results():
    """One live-equivalent test per rig button, for offline mode."""
    from .server import apply_flags
    out = {}
    for name, flags in SCENARIOS.items():
        sup = supervisor.Supervisor(seed=21)
        for n in range(10):                     # a few clean nights first, so the baseline exists
            sup.run_test(n)
        apply_flags(sup, flags)
        out[name] = {"flags": flags, "result": sup.run_test(), "help": sup.help_pressed()}
    return out


def build():
    history, ledger = supervisor.demo_history()
    data = {
        "notice": {
            "id": "2026-03-A-NJ", "dated": "2026-09-08", "implementation": "2026-12-10",
            "carrier": "Verizon New Jersey Inc.", "rule": "47 CFR 51.333",
            "url": "https://www.verizon.com/about/sites/default/files/verizon-new-jersey-copper-retirement-notice-2026-0908.pdf",
            "quote": "Verizon may require customers and interconnecting entities to migrate services off of copper "
                     "facilities well before the copper retirement implementation date.",
            "wire_centers": wire_centers(),
            "fcc": [
                {"id": "DA 26-890", "date": "2026-08-26", "docket": "WC 26-227",
                 "text": "Comments invited on Verizon's section 214 application to discontinue residential and business "
                         "legacy TDM-based voice service in portions of AZ, DE, NJ, NM, OH, RI, SC, UT and VA "
                         "(authorized date on or after Oct 23, 2026).",
                 "url": "https://docs.fcc.gov/public/attachments/DA-26-890A1.pdf"},
                {"id": "DA 26-1038", "date": "2026-09-25", "docket": "WC 26-227",
                 "text": "Not automatically granted: \"The Commission requires additional time to complete its review.\"",
                 "url": "https://docs.fcc.gov/public/attachments/DA-26-1038A1.pdf"},
            ],
        },
        "national": national(),
        "install": install.scenarios(),
        "migration": migration.scenarios(),
        "answer": answer_block(),
        "alarm": {"rates": alarm.success_rates(trials=40), "loss_curve": alarm.loss_curve(trials=30),
                  "voice_vs_alarm": {"label": "model, assumptions in alarm.voice_vs_alarm_curve's docstring; "
                                              "not a bench result and no claim the bench will match",
                                     "plc_burst": alarm.voice_vs_alarm_curve(plc=True, burst=0.2),
                                     "worst_case": alarm.voice_vs_alarm_curve(plc=False, burst=None)}},
        "acoustic": acoustic.compare_designs(trials=30),
        "pass_db": acoustic.PASS_DB,
        "noise_only_max_db": round(float(acoustic.noise_only_margins(n=200).max()), 1),
        "fleet": fleet.compare(cars=120, seeds=range(20)),
        "sensitivity": fleet.sensitivity(cars=120, seeds=range(10)),
        "fleet_assumptions": {k: {"per_car_year": r, "repair_days": rep, "line_monitor_sees": lm}
                              for k, (r, rep, lm) in fleet.RATES.items()},
        "triage": {"nominal": triage.accuracy(), "perturbed_15pct": triage.accuracy(perturb=0.15),
                   "owners": {k: v[0] for k, v in triage.FAULTS.items()}},
        "false_alarms_per_healthy_car_year": [supervisor.false_alarm_rate(seed=k) for k in range(4)],
        "demo_car": history,
        "scenarios": scenario_results(),
        "ledger": {"entries": ledger.entries[-12:], "length": len(ledger.entries), "verified": ledger.verify()[0]},
    }
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(data, fh, indent=1)
    with open(OUT_JS, "w") as fh:
        fh.write("// generated by python3 -m prototype.prove.export\nwindow.PROVE = ")
        json.dump(data, fh, separators=(",", ":"))
        fh.write(";\n")
    return data


if __name__ == "__main__":
    d = build()
    print(f"wire centers parsed: {len(d['notice']['wire_centers'])}")
    print(json.dumps(d["fleet"], indent=1))
    print(f"wrote {OUT_JS}")
