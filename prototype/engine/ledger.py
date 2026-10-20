"""Maps simulated operations to Verizon 10-K line items (Rutgers pilot scale).

  Cost of services  - radio-network electricity, field dispatches (truck rolls)
  SG&A              - care contacts caused by congestion, NOC/enterprise tickets,
                      sales-engineer hours to provision slices manually
  Revenue (VBG)     - slice-hours sold, share of the campus's HVAC savings,
                      demand-response payments
"""
from .config import (CAMPUS_ENERGY_PRICE_USD_KWH, COMPLAINTS_PER_CONGESTED_USER_STEP, DR_ENERGY_USD_MWH,
                     ENERGY_PRICE_USD_KWH, ENTERPRISE_TICKET_USD, GRID_TCO2E_PER_MWH, STEP_MIN, TICKET_USD,
                     TRUCK_ROLL_USD)

STEP_H = STEP_MIN / 60.0
MANUAL_SLICE_ENGINEER_HOURS = 6.0     # est: design + config + test per custom request today
ENGINEER_USD_HR = 110.0               # est: loaded sales/solutions engineer cost
HVAC_SHARED_SAVINGS = 0.25            # est: Verizon's share of verified campus HVAC savings


class Ledger:
    def __init__(self):
        self.kwh = {"ALWAYS_ON": 0.0, "BASELINE": 0.0, "CIRCADIAN": 0.0}
        self.cong_users = {"ALWAYS_ON": 0.0, "BASELINE": 0.0, "CIRCADIAN": 0.0}
        self.cong_steps = {"ALWAYS_ON": 0, "BASELINE": 0, "CIRCADIAN": 0}
        self.hvac_kwh = {"baseline": 0.0, "circadian": 0.0, "reactive": 0.0}
        self.comfort_miss = {"baseline": 0.0, "circadian": 0.0, "reactive": 0.0}
        self.trucks = {"sq": 0, "ci": 0}
        self.tickets = {"sq": 0, "ci": 0}
        self.outage_min = {"sq": 0, "ci": 0}
        self.faults = 0
        self.dr_kwh = 0.0
        self.dr_peak_kw = 0.0
        self.slices = []
        self.guard_events = 0

    # ---- accumulation ---------------------------------------------------
    def ran(self, policy, zone, watts, congested_users, congested):
        self.kwh[policy] += watts / 1000.0 * STEP_H
        self.cong_users[policy] += congested_users
        self.cong_steps[policy] += int(congested)

    def hvac(self, base_kw, circ_kw, base_miss, circ_miss, react_kw=0.0, react_miss=0.0):
        """Timetable (baseline), forecast-driven (circadian), measured-occupancy only (reactive)."""
        self.hvac_kwh["baseline"] += base_kw * STEP_H
        self.hvac_kwh["circadian"] += circ_kw * STEP_H
        self.hvac_kwh["reactive"] += react_kw * STEP_H
        self.comfort_miss["baseline"] += base_miss
        self.comfort_miss["circadian"] += circ_miss
        self.comfort_miss["reactive"] += react_miss

    def fault(self, sq, ci):
        self.faults += 1
        self.trucks["sq"] += sq.trucks
        self.trucks["ci"] += ci.trucks
        self.tickets["sq"] += sq.tickets
        self.tickets["ci"] += ci.tickets
        self.outage_min["sq"] += (sq.repaired_at - sq.start) * STEP_MIN
        self.outage_min["ci"] += (ci.repaired_at - ci.start) * STEP_MIN

    def dr(self, kw):
        self.dr_kwh += kw * STEP_H
        self.dr_peak_kw = max(self.dr_peak_kw, kw)

    def slice_admitted(self, spec, res):
        self.slices.append({"type": spec.slice_type, "mbps": spec.mbps, "hours": res["hours"],
                            "quote_usd": res["quote_usd"]})

    # ---- money ----------------------------------------------------------
    def care_contacts(self, policy):
        return self.cong_users[policy] * COMPLAINTS_PER_CONGESTED_USER_STEP

    def snapshot(self):
        """Running totals for the dashboard counters (Circadian vs. today's AI baseline and NOC)."""
        energy_usd = (self.kwh["BASELINE"] - self.kwh["CIRCADIAN"]) * ENERGY_PRICE_USD_KWH
        truck_usd = (self.trucks["sq"] - self.trucks["ci"]) * TRUCK_ROLL_USD
        care_usd = (self.care_contacts("BASELINE") - self.care_contacts("CIRCADIAN")) * TICKET_USD
        ticket_usd = (self.tickets["sq"] - self.tickets["ci"]) * ENTERPRISE_TICKET_USD
        slice_usd = len(self.slices) * MANUAL_SLICE_ENGINEER_HOURS * ENGINEER_USD_HR
        saved_mwh = ((self.kwh["BASELINE"] - self.kwh["CIRCADIAN"])
                     + (self.hvac_kwh["baseline"] - self.hvac_kwh["circadian"])) / 1000.0
        return {
            "kwh_a": self.kwh["ALWAYS_ON"], "kwh_b": self.kwh["BASELINE"], "kwh_c": self.kwh["CIRCADIAN"],
            "hvac_b": self.hvac_kwh["baseline"], "hvac_c": self.hvac_kwh["circadian"],
            "cong_b": self.cong_users["BASELINE"], "cong_c": self.cong_users["CIRCADIAN"],
            "trucks_sq": self.trucks["sq"], "trucks_ci": self.trucks["ci"],
            "usd_cos": energy_usd + truck_usd,
            "usd_sga": care_usd + ticket_usd + slice_usd,
            "tco2e": saved_mwh * GRID_TCO2E_PER_MWH,
            "dr_kwh": self.dr_kwh,
        }

    def summary(self, day, extras):
        a, b, c = self.kwh["ALWAYS_ON"], self.kwh["BASELINE"], self.kwh["CIRCADIAN"]
        hb, hc = self.hvac_kwh["baseline"], self.hvac_kwh["circadian"]
        snap = self.snapshot()
        slice_rev = sum(s["quote_usd"] for s in self.slices)
        hvac_usd = (hb - hc) * CAMPUS_ENERGY_PRICE_USD_KWH
        return {
            "scenario": day.name,
            "ran_kwh": {"always_on": round(a, 1), "baseline": round(b, 1), "circadian": round(c, 1)},
            "ran_saving_vs_always_on_pct": round(100 * (a - c) / a, 1) if a else 0.0,
            "baseline_saving_vs_always_on_pct": round(100 * (a - b) / a, 1) if a else 0.0,
            "ran_saving_vs_baseline_pct": round(100 * (b - c) / b, 1) if b else 0.0,
            "congested_user_steps": {"baseline": round(self.cong_users["BASELINE"], 1),
                                     "circadian": round(self.cong_users["CIRCADIAN"], 1),
                                     "always_on": round(self.cong_users["ALWAYS_ON"], 1)},
            "congested_zone_steps": dict(self.cong_steps),
            "care_contacts": {"baseline": round(self.care_contacts("BASELINE"), 2),
                              "circadian": round(self.care_contacts("CIRCADIAN"), 2)},
            "sla_guard_events": self.guard_events,
            "hvac_kwh": {"baseline": round(hb, 1), "circadian": round(hc, 1),
                         "reactive": round(self.hvac_kwh["reactive"], 1)},
            "hvac_saving_pct": round(100 * (hb - hc) / hb, 1) if hb else 0.0,
            "hvac_reactive_saving_pct": round(100 * (hb - self.hvac_kwh["reactive"]) / hb, 1) if hb else 0.0,
            "comfort_miss_people_steps": {k: round(v) for k, v in self.comfort_miss.items()},
            "faults": self.faults,
            "truck_rolls": dict(self.trucks),
            "tickets": dict(self.tickets),
            "outage_minutes": dict(self.outage_min),
            "dr_kwh": round(self.dr_kwh, 1),
            "dr_peak_kw": round(self.dr_peak_kw, 1),
            "dr_payment_usd": round(self.dr_kwh / 1000.0 * DR_ENERGY_USD_MWH, 2),
            "slices": self.slices,
            "slice_revenue_usd": round(slice_rev, 2),
            "usd": {
                "cost_of_services": round(snap["usd_cos"], 2),
                "sga": round(snap["usd_sga"], 2),
                "campus_hvac_savings": round(hvac_usd, 2),
                "verizon_share_of_hvac_savings": round(hvac_usd * HVAC_SHARED_SAVINGS, 2),
                "energy_usd_vs_always_on": round((a - c) * ENERGY_PRICE_USD_KWH, 2),
            },
            "tco2e_avoided": round(snap["tco2e"], 3),
        }
