"""Install capacity for the copper exit, with and without self-proof at install.

The judges' question is not "how many dollars" but "can Verizon physically
migrate the filed lines by the authorized dates?". Verizon's July 2026 filing
says it has about 46,000 fixed-wireless POTS-replacement customers nationwide,
while about 140,000 legacy lines remain in Frontier's 8 states alone (both
verified, research/06). Press reports put the 2026 Verizon applications at
about 277k and 750k lines (unverified).

Every input except those two counts is an ASSUMPTION, named and labeled, for a
Verizon mentor to replace. The output is technician-hours and months of
install work, not dollars.
"""
from dataclasses import dataclass, asdict

INSTALLED_FW_POTS = 46_000           # verified: Verizon fixed-wireless POTS replacement customers, nationwide (Jul 2026)
FRONTIER_8_STATE_LINES = 140_000     # verified: legacy voice lines left in the 8 Frontier states (WC 26-170)


@dataclass
class Assumptions:
    lines: int = 1_000_000            # ASSUMPTION: order of magnitude of lines in 2026 filings (press: ~277k + ~750k)
    fw_share: float = 0.30            # ASSUMPTION: share whose replacement is fixed wireless (rest: fiber, cable, mobile)
    tech_hours_per_install: float = 2.0   # ASSUMPTION: 1.25 h on site + 0.75 h travel
    techs: int = 600                  # ASSUMPTION: technicians available for this work
    hours_per_tech_month: float = 120.0   # ASSUMPTION: productive install hours per technician per month
    prove_pass: float = 0.60          # ASSUMPTION until measured: share of self-installs PROVE clears with no truck
    fix_by_text_share: float = 0.15   # ASSUMPTION: share that fail first but pass after a texted fix (no truck)


def plan(a=None):
    a = a or Assumptions()
    installs = a.lines * a.fw_share
    capacity = a.techs * a.hours_per_tech_month
    base_hours = installs * a.tech_hours_per_install
    trucks_with = installs * (1 - a.prove_pass - a.fix_by_text_share)
    prove_hours = trucks_with * a.tech_hours_per_install
    return {
        "assumptions": asdict(a),
        "fixed_wireless_installs": round(installs),
        "vs_installed_base_x": round(installs / INSTALLED_FW_POTS, 1),
        "tech_hours_today": round(base_hours),
        "tech_hours_with_prove": round(prove_hours),
        "months_today": round(base_hours / capacity, 1),
        "months_with_prove": round(prove_hours / capacity, 1),
        "trucks_avoided": round(installs - trucks_with),
    }


def sensitivity():
    """How the months of install work move with the two numbers we cannot know from outside."""
    rows = []
    for fw in (0.15, 0.30, 0.50):
        for p in (0.3, 0.6, 0.8):
            r = plan(Assumptions(fw_share=fw, prove_pass=p))
            rows.append({"fw_share": fw, "prove_pass": p, "months_today": r["months_today"],
                         "months_with_prove": r["months_with_prove"], "trucks_avoided": r["trucks_avoided"]})
    return rows


if __name__ == "__main__":
    import json
    print(json.dumps(plan(), indent=1))
    for r in sensitivity():
        print(r)
