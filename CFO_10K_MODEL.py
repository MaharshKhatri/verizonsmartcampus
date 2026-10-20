#!/usr/bin/env python3
"""Circadian CFO model: Rutgers pilot + Verizon national rollout, mapped to 10-K lines.

    python3 CFO_10K_MODEL.py            # writes FINANCIAL_PROJECTION.md, verizon_10k_sensitivity.csv
    python3 CFO_10K_MODEL.py --print    # also prints the summary

Standard library only. Every input is a (bear, base, bull) triple with a source
tag. Tags starting "10-K", "EIA", "NCES", "CBECS", "PJM", "Rutgers" or
"research/" are sourced facts; "est" marks a team assumption that the Rutgers
pilot or a Verizon Business conversation must validate. Simulator outputs
(prototype/out/sim_kpis.json) calibrate the network levers when present.

Revenue and cost conventions follow Verizon's income statement:
  Operating revenue  - Business segment (Enterprise & Public Sector customers)
  Cost of services   - network energy, field dispatches, platform hosting,
                       delivery cost of pulled-through network services
  SG&A               - sales and support, care contacts
  EBITDA             - revenue - cost of services - SG&A (no D&A)
"""
import argparse
import csv
import json
import math
import os
import random

ROOT = os.path.dirname(os.path.abspath(__file__))
YEARS = [2027, 2028, 2029, 2030, 2031]

# --------------------------------------------------------------------------
# Verizon baseline (FY2025 10-K, filed 2026-02-17) - research/01_sec_forensic.md
# --------------------------------------------------------------------------
VZ = {
    "revenue": 138_191e6,
    "cost_of_services": 27_789e6,
    "sga": 33_818e6,
    "adj_ebitda": 49_997e6,
    "eps_revenue": 13_534e6,           # Enterprise & Public Sector, FY2025 (-4.8% YoY)
    "eps_revenue_fy24": 14_218e6,
    "capex_2026_guide": (16.0e9, 16.5e9),
    "grid_mwh": 10_246_417,            # 2025 grid electricity (EY-assured energy data)
    "scope2_location_t": 3_335_994,
}

# --------------------------------------------------------------------------
# Assumptions: name -> (bear, base, bull, source, 10-K line, note)
# --------------------------------------------------------------------------
A = {
    # adoption (cumulative customers by 2031); ramp shape is fixed below
    "univ_2031": (40, 90, 160, "est; NCES: 488 institutions >=10k students", "Revenue", "universities live by 2031"),
    "hosp_2031": (10, 30, 60, "est; AHA: 6,100 hospitals", "Revenue", "hospital campuses live by 2031"),
    "corp_2031": (10, 25, 50, "est; CBECS: 11,000 offices >200k sq ft", "Revenue", "corporate campuses live by 2031"),
    "univ_gsf": (4e6, 6e6, 8e6, "est; Rutgers 29M GSF is a large outlier", "Revenue", "avg GSF per university"),
    "hosp_gsf": (1.0e6, 1.5e6, 2.0e6, "est; CBECS 1,883M sq ft over ~3,000 large inpatient bldgs", "Revenue", "avg GSF per hospital campus"),
    "corp_gsf": (1.5e6, 2.0e6, 3.0e6, "est", "Revenue", "avg GSF per corporate campus"),
    # pricing (research/04 section 9)
    "platform_usd_gsf": (0.020, 0.025, 0.030, "research/04 s9 (LBNL median $0.02; Occuspace $0.105-0.15)", "Revenue", "Layer 1 occupancy intelligence"),
    "hvac_saving": (0.05, 0.07, 0.10, "research/04 s3 (Sentinel 17.8%, MARTINI 8-11%, UBC ~5%); sim 8-19%", "Revenue", "share of HVAC energy saved"),
    "perf_fee": (0.15, 0.20, 0.25, "research/04 s9 (customer keeps 80%)", "Revenue", "Verizon share of verified savings"),
    "dr_mw_univ": (0.5, 1.0, 2.0, "est", "Revenue", "curtailable MW per university"),
    "dr_usd_kw_yr": (90.0, 104.0, 118.0, "PJM BRA $269.92-333.44/MW-day; research/04 s6", "Revenue", "capacity value $/kW-yr"),
    "dr_share": (0.10, 0.15, 0.20, "research/04 s9", "Revenue", "Verizon share of DR value"),
    "pull_through_arr": (100e3, 250e3, 600e3, "est; needs Verizon Business pricing validation", "Revenue", "slices + Frontline + private 5G ARR per customer"),
    "pull_through_margin": (0.25, 0.35, 0.45, "est", "Cost of services", "contribution margin on pulled-through services"),
    # HVAC economics of customers (CBECS 2018; APPA)
    "hvac_usd_gsf_univ": (1.20, 1.33, 1.45, "APPA $2.19/sq ft x CBECS 60.8% HVAC", "Revenue", "HVAC energy $/GSF, higher ed"),
    "hvac_usd_gsf_hosp": (1.55, 1.70, 1.85, "CBECS $3.18/sq ft x 53.4%", "Revenue", "HVAC energy $/GSF, hospitals"),
    "hvac_usd_gsf_corp": (0.85, 0.92, 1.00, "CBECS $1.63/sq ft x 56.7%", "Revenue", "HVAC energy $/GSF, offices"),
    # internal network levers, per customer campus
    "sites_per_campus": (10, 20, 35, "est (macro sectors + small cells serving a campus)", "Cost of services", "Verizon radio sites per customer"),
    "site_energy_usd": (4_000, 5_300, 6_500, "research/02 P6 3.9 kW + overhead; EIA 13.4c/kWh", "Cost of services", "annual electricity per site"),
    "ran_incremental": (0.0, 0.005, 0.015, "default; replaced by the simulator's weighted day mix", "Cost of services", "extra radio energy saved"),
    "faults_per_site_yr": (0.5, 1.0, 1.5, "est", "Cost of services", "radio faults per site per year"),
    "truck_avoid_share": (0.15, 0.30, 0.45, "default; replaced by the simulator's fault-storm Monte Carlo", "Cost of services", "dispatches avoided per fault"),
    "truck_roll_usd": (150.0, 375.0, 600.0, "research/01 s5: $150-600 industry range", "Cost of services", "cost per truck roll"),
    "event_days": (6, 12, 25, "Rutgers: 7 home football games + arena/commencement", "SG&A", "big event days per campus per year"),
    "care_contacts_event": (0, 5, 20, "est; sim: event-mode baseline already avoids most congestion", "SG&A", "care contacts avoided per event day"),
    "care_usd": (5.0, 8.01, 12.0, "Gartner 2019 $8.01 per live contact", "SG&A", "cost per care contact"),
    # costs
    "platform_build": (9e6, 6e6, 4e6, "est: ~25 FTE for 12 months", "CapEx", "platform build (capitalised)"),
    "platform_run": (2.5e6, 1.5e6, 1.0e6, "est: core team + cloud at pilot scale", "Cost of services", "fixed annual platform run cost"),
    "platform_run_per_customer": (25e3, 15e3, 10e3, "est: cloud/MEC + SRE share per campus", "Cost of services", "variable platform cost per customer"),
    "deploy_per_customer": (400e3, 150e3, 70e3, "est; BMS + Wi-Fi API integration via the campus's BMS integrator", "CapEx", "integration per customer"),
    "implementation_fee_share": (0.25, 0.50, 0.80, "est; PSE&G pays up to $1.00/kWh saved, capped at 60% of project cost", "Revenue", "share of integration billed to the customer"),
    "ot_security_per_customer": (50e3, 25e3, 15e3, "est; OT/BMS network segmentation review", "CapEx", "one-time OT security work per customer"),
    "mv_per_customer": (60e3, 35e3, 20e3, "est; IPMVP M&V + support", "Cost of services", "annual M&V + support per customer"),
    "data_license_per_customer": (20e3, 10e3, 5e3, "est; Wi-Fi analytics / BMS API licences", "Cost of services", "annual data and API licences per customer"),
    "privacy_program": (0.8e6, 0.5e6, 0.3e6, "est; CPNI aggregate-data governance, audits (47 U.S.C. s222)", "Cost of services", "annual privacy and compliance program"),
    "churn": (0.08, 0.05, 0.03, "est", "Revenue", "annual customer churn"),
    "sales_pct": (0.20, 0.15, 0.10, "est", "SG&A", "sales & support as % of B2B revenue"),
    "pilot_cost": (600e3, 350e3, 250e3, "est: 90-day Rutgers lighthouse", "SG&A", "Rutgers pilot, 2027"),
    # finance
    "wacc": (0.08, 0.07, 0.065, "est for Verizon", "-", "discount rate"),
    "tax": (0.24, 0.23, 0.22, "est (Verizon effective rate ~22-24%)", "-", "cash tax rate"),
    "grid_t_per_mwh": (0.325, 0.325, 0.325, "Verizon 2025 location-based Scope 2 / grid MWh", "-", "emission factor"),
}
RAMP = [0.02, 0.10, 0.30, 0.62, 1.00]     # share of 2031 customers live in each year (Rutgers in 2027)
TORNADO_KEYS = ["univ_2031", "hosp_2031", "corp_2031", "platform_usd_gsf", "hvac_saving", "perf_fee",
                "pull_through_arr", "pull_through_margin", "dr_mw_univ", "sites_per_campus", "ran_incremental",
                "truck_avoid_share", "platform_run", "platform_run_per_customer", "deploy_per_customer",
                "implementation_fee_share",
                "mv_per_customer", "churn", "sales_pct", "wacc"]
CONTRACT_YEARS = 5                       # research/04 s9: performance fee runs for 5 years
TERMINAL_GROWTH = 0.02


def base(key):
    return A[key][1]


def scenario_values(which):
    idx = {"bear": 0, "base": 1, "bull": 2}[which]
    return {k: v[idx] for k, v in A.items()}


def calibrate(kpis_path):
    """Pull network-lever evidence from the simulator, if it has been run."""
    if not kpis_path or not os.path.exists(kpis_path):
        return {"source": "defaults (simulator outputs not found)"}
    with open(kpis_path) as fh:
        k = json.load(fh)
    inc = {n: v["summary"]["ran_saving_vs_baseline_pct"] / 100.0 for n, v in k.items()
           if isinstance(v, dict) and "summary" in v}
    # A campus year (est): ~300 ordinary days (classes, weekends, breaks), 14 finals days,
    # 7 home football games, ~21 arena/one-off events, ~2 closures. Negative days count.
    mix = {"weekday": 300, "finals": 14, "gameday": 7, "arena": 21, "snowday": 2}
    weighted = sum(inc.get(n, 0.0) * d for n, d in mix.items()) / sum(mix.values())
    storm = k.get("triage_storm", {})
    ev = k.get("arena", {}).get("summary", {}).get("congested_user_steps", {})
    hvac = {n: v["summary"]["hvac_saving_pct"] for n, v in k.items() if isinstance(v, dict) and "summary" in v}
    return {"source": "prototype/out/sim_kpis.json", "ran_incremental_weighted": weighted,
            "incremental_by_day": inc, "day_mix": mix,
            "truck_avoid_share": storm.get("dispatch_avoided_share"), "storm": storm,
            "event_congested_user_steps": ev,
            "hvac_saving_pct_by_day": hvac, "triage_accuracy": k.get("triage_accuracy")}


def apply_calibration(cal):
    """Replace the base value of network levers with simulator evidence (bear 0.5x, bull 1.5x of the
    magnitude); the model never uses a network number the simulator contradicts."""
    if "ran_incremental_weighted" in cal:
        w = cal["ran_incremental_weighted"]
        A["ran_incremental"] = (min(w, 0.0) if w > 0 else w * 1.5, w, max(w * 1.5, 0.0),
                                "sim: context vs traffic-history AI + event mode, weighted campus day mix",
                                "Cost of services", "extra radio energy saved")
    if cal.get("truck_avoid_share"):
        t = cal["truck_avoid_share"]
        A["truck_avoid_share"] = (t * 0.5, t, min(0.6, t * 1.5),
                                  "sim: 2,000 fault-storm draws (dispatch probabilities are assumptions)",
                                  "Cost of services", "dispatches avoided per fault")


# --------------------------------------------------------------------------
# Core projection
# --------------------------------------------------------------------------
def project(p):
    """Return per-year rows for one parameter set p (dict of floats)."""
    rows = []
    built = 0.0
    for i, year in enumerate(YEARS):
        f = RAMP[i]
        keep = (1.0 - p["churn"]) ** i                  # attrition of earlier cohorts (approximation)
        univ = max(1.0, p["univ_2031"] * f * keep)      # Rutgers is customer #1
        hosp = p["hosp_2031"] * f * keep
        corp = p["corp_2031"] * f * keep
        customers = univ + hosp + corp
        new_customers = max(0.0, customers - built)
        built = customers
        gsf = univ * p["univ_gsf"] + hosp * p["hosp_gsf"] + corp * p["corp_gsf"]
        hvac_spend = (univ * p["univ_gsf"] * p["hvac_usd_gsf_univ"] + hosp * p["hosp_gsf"] * p["hvac_usd_gsf_hosp"]
                      + corp * p["corp_gsf"] * p["hvac_usd_gsf_corp"])
        customer_savings = hvac_spend * p["hvac_saving"]

        rev_platform = gsf * p["platform_usd_gsf"]
        rev_perf = customer_savings * p["perf_fee"]
        dr_mw = univ * p["dr_mw_univ"] + 0.5 * (hosp + corp) * p["dr_mw_univ"]
        rev_dr = dr_mw * 1000 * p["dr_usd_kw_yr"] * p["dr_share"]
        rev_pull = customers * p["pull_through_arr"]
        rev_impl = new_customers * p["deploy_per_customer"] * p["implementation_fee_share"]
        revenue = rev_platform + rev_perf + rev_dr + rev_pull + rev_impl

        sites = customers * p["sites_per_campus"]
        save_energy = sites * p["site_energy_usd"] * p["ran_incremental"]
        save_trucks = sites * p["faults_per_site_yr"] * p["truck_avoid_share"] * p["truck_roll_usd"]
        save_care = customers * p["event_days"] * p["care_contacts_event"] * p["care_usd"]

        cos_pull = rev_pull * (1 - p["pull_through_margin"])
        cos_mv = customers * p["mv_per_customer"]
        cos_data = customers * p["data_license_per_customer"]
        cos_platform = p["platform_run"] + customers * p["platform_run_per_customer"]
        cos = cos_pull + cos_platform + cos_mv + cos_data + p["privacy_program"] - save_energy - save_trucks
        sga_sales = (revenue - rev_impl) * p["sales_pct"]
        sga_pilot = p["pilot_cost"] if i == 0 else 0.0
        sga = sga_sales + sga_pilot - save_care
        ebitda = revenue - cos - sga
        capex_deploy = new_customers * (p["deploy_per_customer"] + p["ot_security_per_customer"])
        capex = (p["platform_build"] if i == 0 else 0.0) + capex_deploy
        dep = p["platform_build"] / 5.0 + (sum(r["capex_deploy"] for r in rows) + capex_deploy) / 5.0
        ebit = ebitda - dep
        tax = max(0.0, ebit) * p["tax"]
        fcf = ebitda - tax - capex
        ran_mwh = save_energy / 0.134 / 1000.0                  # at the U.S. commercial rate used for sites
        customer_mwh = customer_savings / 0.17 / 1000.0           # est blended customer HVAC $/kWh
        rows.append({
            "year": year, "customers": customers, "universities": univ, "gsf": gsf,
            "rev_platform": rev_platform, "rev_performance": rev_perf, "rev_dr": rev_dr, "rev_pull_through": rev_pull,
            "rev_implementation": rev_impl, "revenue": revenue, "customer_hvac_savings": customer_savings,
            "save_ran_energy": save_energy, "save_truck_rolls": save_trucks, "save_care": save_care,
            "cos_pull_through": cos_pull, "cos_platform": cos_platform, "cos_mv": cos_mv, "cos_data": cos_data,
            "cos_privacy": p["privacy_program"], "sga_sales": sga_sales, "sga_pilot": sga_pilot,
            "cost_of_services": cos, "sga": sga, "ebitda": ebitda,
            "capex": capex, "capex_deploy": capex_deploy, "depreciation": dep,
            "tax": tax, "fcf": fcf, "tco2e_verizon": ran_mwh * p["grid_t_per_mwh"],
            "tco2e_enabled": customer_mwh * p["grid_t_per_mwh"],
        })
    return rows


def npv(rate, flows):
    return sum(cf / (1 + rate) ** (i + 1) for i, cf in enumerate(flows))


def irr(flows):
    """IRR by bisection on [-0.99, 10]; None if the sign never changes."""
    lo, hi = -0.99, 10.0
    f = lambda r: sum(cf / (1 + r) ** (i + 1) for i, cf in enumerate(flows))
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        fm = f(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def payback_months(flows):
    cum = 0.0
    for i, cf in enumerate(flows):
        if cum + cf >= 0 and cf > 0 and cum < 0:
            return round(12 * i + 12 * (-cum / cf))
        cum += cf
        if i == 0 and cum >= 0:
            return 0
    return None


def evaluate(p):
    rows = project(p)
    flows = [r["fcf"] for r in rows]
    y5 = rows[-1]
    # Terminal value: shared-savings fees end with their 5-year contracts and one-time
    # implementation fees stop, so the steady state keeps platform, DR and pull-through only.
    steady_ebitda = y5["ebitda"] - y5["rev_performance"] * (1 - p["sales_pct"]) - y5["rev_implementation"]
    steady_fcf = steady_ebitda * (1 - p["tax"])
    g = TERMINAL_GROWTH - p["churn"]
    terminal = steady_fcf * (1 + g) / (p["wacc"] - g) / (1 + p["wacc"]) ** len(rows)
    margin_bps = 1e4 * ((VZ["adj_ebitda"] + y5["ebitda"]) / (VZ["revenue"] + y5["revenue"])
                        - VZ["adj_ebitda"] / VZ["revenue"])
    core = dict(p, pull_through_arr=0.0)
    core_flows = [r["fcf"] for r in project(core)]
    return {"rows": rows, "npv5": npv(p["wacc"], flows), "npv_terminal": npv(p["wacc"], flows) + terminal,
            "terminal_share": terminal / (npv(p["wacc"], flows) + terminal) if npv(p["wacc"], flows) + terminal else 0,
            "npv5_core_software": npv(p["wacc"], core_flows),
            "irr": irr(flows), "payback_months": payback_months(flows), "y5": y5,
            "margin_bps": margin_bps, "ebitda_bps_of_revenue": 1e4 * y5["ebitda"] / VZ["revenue"]}


def monte_carlo(n=4000, seed=42):
    rng = random.Random(seed)
    npvs, ebitdas = [], []
    for _ in range(n):
        p = {k: rng.triangular(min(v[0], v[2]), max(v[0], v[2]), v[1]) for k, v in A.items()}
        r = evaluate(p)
        npvs.append(r["npv5"])
        ebitdas.append(r["y5"]["ebitda"])
    npvs.sort()
    ebitdas.sort()
    q = lambda xs, f: xs[int(f * (len(xs) - 1))]
    return {"n": n, "npv_p10": q(npvs, .1), "npv_p50": q(npvs, .5), "npv_p90": q(npvs, .9),
            "ebitda_p10": q(ebitdas, .1), "ebitda_p50": q(ebitdas, .5), "ebitda_p90": q(ebitdas, .9),
            "prob_npv_positive": sum(1 for x in npvs if x > 0) / n}


def tornado(p0):
    out = []
    base_npv = evaluate(p0)["npv5"]
    for k in TORNADO_KEYS:
        lo_v, _, hi_v = A[k][0], A[k][1], A[k][2]
        res = {}
        for label, v in (("bear", lo_v), ("bull", hi_v)):
            p = dict(p0)
            p[k] = v
            res[label] = evaluate(p)["npv5"]
        out.append({"parameter": k, "line_item": A[k][4], "description": A[k][5], "bear_value": lo_v,
                    "base_value": A[k][1], "bull_value": hi_v, "npv_bear": res["bear"], "npv_bull": res["bull"],
                    "swing": abs(res["bull"] - res["bear"]), "npv_base": base_npv, "source": A[k][3]})
    out.sort(key=lambda r: -r["swing"])
    return out


def pilot(cal):
    """Rutgers lighthouse economics (research/04 section 9b, plus simulator network levers)."""
    energy_spend = 60e6                       # Rutgers Climate Action Plan supplement (2021)
    hvac_share = 0.608                        # CBECS education HVAC share of energy
    gsf = 29e6                                # Rutgers University Facilities
    out = {}
    for label, s in (("low", 0.05), ("high", 0.10)):
        savings = energy_spend * hvac_share * s
        fee1 = gsf * 0.02
        fee2 = savings * 0.20
        out[label] = {"hvac_savings": savings, "platform_fee": fee1, "performance_fee": fee2,
                      "rutgers_net": savings - fee1 - fee2, "verizon_revenue": fee1 + fee2}
    out["dr_per_mw_verizon"] = 1000 * 104.0 * 0.15
    out["sim_hvac_saving_pct"] = cal.get("hvac_saving_pct_by_day", {})
    return out


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------
def m(x):
    if abs(x) < 1e6:
        return f"{'-' if x < 0 else ''}${abs(x) / 1e3:,.0f}k"
    return f"{'-' if x < 0 else ''}${abs(x) / 1e6:,.1f}M"


def upside_options(cal):
    """Levers deliberately excluded from the base case, sized so judges can see why."""
    ran_bill = (0.65e9, 1.10e9)                     # research/01 s3: 73-80% x $0.88-1.37B (estimate)
    inc = cal.get("ran_incremental_weighted", A["ran_incremental"][1])
    network_wide = [b * 0.30 * inc for b in ran_bill]  # est: 30% of sites have usable public context
    students = 90 * 15_000                           # base-case universities x est. students per campus
    acquisition = students * 0.005 * 900.0           # est: +0.5 pt share at partner campuses x $900 contribution
    return [
        ("Network-wide context on Verizon's ~60,000 vRAN sites (public event + school calendars)",
         f"RAN electricity $0.65-1.10B (est) x 30% of sites x {100 * inc:.1f}% extra saving",
         network_wide[0], network_wide[1]),
        ("Student acquisition at partner campuses",
         "90 campuses x 15,000 students x 0.5 pt share gain x $900 contribution (all est)",
         acquisition * 0.5, acquisition * 1.5),
        ("Verizon as customer zero: occupancy-driven HVAC in Verizon's own offices",
         "Not sized - Verizon does not disclose office energy; 10-Q cites +$114M Q1-26 building costs", 0.0, 0.0),
    ]


def write_outputs(results, sens, mc, cal, pilot_econ):
    base_r, bear_r, bull_r = results["base"], results["bear"], results["bull"]
    lines = []
    w = lines.append
    w("# Financial projection: Circadian (Verizon Smart Campus)")
    w("")
    w("*Generated by `CFO_10K_MODEL.py`. Do not edit by hand; change assumptions in the model and re-run.*")
    w("")
    w("## Bottom line")
    y5 = base_r["y5"]
    w(f"- **Base case, 2031 run-rate:** revenue {m(y5['revenue'])}, EBITDA {m(y5['ebitda'])} "
      f"({base_r['ebitda_bps_of_revenue']:.1f} bps of FY2025 revenue; consolidated margin "
      f"{base_r['margin_bps']:+.1f} bps).")
    irr_txt = f"IRR {base_r['irr']:.0%}" if base_r["irr"] is not None else "IRR n/a"
    pb_txt = f"payback {base_r['payback_months']} months" if base_r["payback_months"] else "no payback within 5 years"
    w(f"- **5-year NPV (2027-2031, no terminal value):** {m(base_r['npv5'])} at {A['wacc'][1]:.1%}; {irr_txt}; "
      f"{pb_txt}. With a terminal value ({TERMINAL_GROWTH:.0%} growth less churn, shared-savings fees ending with "
      f"their {CONTRACT_YEARS}-year contracts): {m(base_r['npv_terminal'])}.")
    w(f"- **Software alone is not enough:** without Layer-4 network pull-through the 5-year NPV is "
      f"{m(base_r['npv5_core_software'])}. The pull-through ARR per customer is the number Verizon Business "
      "must validate first.")
    w(f"- **Range:** 2031 EBITDA {m(bear_r['y5']['ebitda'])} (bear) to {m(bull_r['y5']['ebitda'])} (bull); "
      f"5-year NPV {m(bear_r['npv5'])} to {m(bull_r['npv5'])}. Monte Carlo ({mc['n']:,} draws, every assumption "
      f"triangular): NPV P10 {m(mc['npv_p10'])}, P50 {m(mc['npv_p50'])}, P90 {m(mc['npv_p90'])}; "
      f"P(NPV > 0) = {mc['prob_npv_positive']:.0%}.")
    w(f"- **Context:** Enterprise & Public Sector revenue fell {m(VZ['eps_revenue_fy24'] - VZ['eps_revenue'])} "
      f"in 2025 (10-K). The base case adds {m(y5['revenue'])} of E&PS revenue by 2031, "
      f"about {y5['revenue'] / (VZ['eps_revenue_fy24'] - VZ['eps_revenue']):.0%} of one year's decline.")
    w(f"- **Honest scale check:** a ~{y5['ebitda'] / 1e6:,.0f}M/yr EBITDA business line by 2031, about "
      f"{100 * y5['ebitda'] / 5e9:.1f}% of the $5B 2026 opex-savings program. Not a moonshot: a product Verizon "
      "Business can pilot next year, whose network side makes AI energy saving cheaper on event days.")
    w("")
    w("## What the simulator says about the network levers (calibration)")
    w(f"- Source: `{cal.get('source')}`. Baseline = traffic-history AI with learned margins **plus the operator's "
      "manual event mode** (no energy saving on venue cells 2 h before to 4 h after a ticketed event).")
    if "ran_incremental_weighted" in cal:
        inc = cal["incremental_by_day"]
        w("- Extra radio energy saved by campus context, by day type: " +
          ", ".join(f"{n} {100 * v:+.1f}%" for n, v in inc.items()) +
          f". Campus-year mix {cal['day_mix']} -> **{100 * cal['ran_incremental_weighted']:+.2f}%**, the model's base "
          "value (bear 1.5x worse, bull 1.5x better). Small, as expected: context pays on irregular days only.")
        ev = cal.get("event_congested_user_steps") or {}
        if ev:
            w(f"- One-off arena event: congested user-steps today's practice {ev.get('baseline', 0):,.0f} vs "
              f"Circadian {ev.get('circadian', 0):,.0f}: event mode already protects quality, so the event-day "
              "value is energy, not congestion. Care savings are therefore small in the model.")
        st = cal.get("storm") or {}
        if st:
            w(f"- Fault storm, {st['draws']:,} random draws: dispatches {st['trucks_status_quo']} -> "
              f"{st['trucks_circadian']} per {st['faults']} faults (**{st['dispatch_avoided_share']:.0%}** avoided; "
              f"no gain in {st['p_no_gain']:.0%} of storms); restore time {st['outage_min_status_quo']} -> "
              f"{st['outage_min_circadian']} min. These follow from assumed dispatch and remote-fix probabilities.")
        w(f"- HVAC savings in the twin by day: " + ", ".join(f"{k} {v:.1f}%" for k, v in cal["hvac_saving_pct_by_day"].items())
          + f". Almost all of it is ventilation by headcount. Planning uses the literature range "
          f"{A['hvac_saving'][0]:.0%}-{A['hvac_saving'][2]:.0%} (base {A['hvac_saving'][1]:.0%}), not the twin.")
    w("")
    w("## Rutgers lighthouse pilot (research/04 s9b)")
    w("| | Low (5% HVAC saving) | High (10%) |")
    w("|---|---:|---:|")
    for key, label in (("hvac_savings", "Rutgers HVAC energy savings"), ("platform_fee", "Layer 1 fee (29M GSF x $0.02)"),
                       ("performance_fee", "Layer 2 fee (20% of savings)"), ("rutgers_net", "Rutgers net benefit"),
                       ("verizon_revenue", "Verizon revenue")):
        w(f"| {label} | {m(pilot_econ['low'][key])} | {m(pilot_econ['high'][key])} |")
    w(f"| DR upside to Verizon per curtailable MW | {m(pilot_econ['dr_per_mw_verizon'])} | same |")
    w("")
    w("Inputs: $60M/yr Rutgers energy spend (Climate Action Plan supplement, 2021), 60.8% HVAC share (CBECS 2018 "
      "education), 29M GSF (Rutgers University Facilities). Pilot cost to Verizon (est): "
      f"{m(A['pilot_cost'][1])} for a 90-day, 5-10 building lighthouse with IPMVP M&V.")
    w("")
    w("## National projection by year (base case)")
    w("| Year | Customers | Revenue | Cost of services | SG&A | EBITDA | CapEx | Free cash flow |")
    w("|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in base_r["rows"]:
        w(f"| {r['year']} | {r['customers']:.0f} | {m(r['revenue'])} | {m(r['cost_of_services'])} | {m(r['sga'])} | "
          f"{m(r['ebitda'])} | {m(r['capex'])} | {m(r['fcf'])} |")
    w("")
    w("## 2031 run-rate mapped to Verizon's 10-K lines (base case)")
    w("| 10-K line | Driver | 2031 |")
    w("|---|---|---:|")
    for line, driver, val in ledger_lines(y5):
        w(f"| {line} | {driver} | {m(val)} |")
    w(f"| **Consolidated EBITDA** | revenue - cost of services - SG&A | **{m(y5['ebitda'])}** |")
    w("")
    w("Sign convention: revenue lines and savings are positive (good for EBITDA); costs are negative.")
    w("")
    w("## Upside options (excluded from every scenario above)")
    w("| Option | Math | Annual value |")
    w("|---|---|---:|")
    for name, math_, lo, hi in upside_options(cal):
        w(f"| {name} | {math_} | {m(lo)}-{m(hi)} |" if hi else f"| {name} | {math_} | not sized |")
    w("")
    w("The first row is why radio energy is not the headline: even network-wide, context adds single-digit "
      "millions on top of the AI energy saving Verizon already runs (\"over $200 million\", Schulman, Q1-26 call).")
    w("")
    w("## Carbon")
    w(f"- Verizon Scope 2 (location-based) avoided at customer sites, 2031: {y5['tco2e_verizon']:,.0f} tCO2e "
      "(small: radio energy is not where this product's money is).")
    w(f"- Customer HVAC emissions avoided ('enabled' reductions, not Verizon's own inventory), 2031: "
      f"{y5['tco2e_enabled']:,.0f} tCO2e at {A['grid_t_per_mwh'][1]} t/MWh.")
    w("")
    w("## Scenarios")
    w("| | Bear | Base | Bull |")
    w("|---|---:|---:|---:|")
    for key, label in (("revenue", "2031 revenue"), ("ebitda", "2031 EBITDA")):
        w(f"| {label} | {m(bear_r['y5'][key])} | {m(base_r['y5'][key])} | {m(bull_r['y5'][key])} |")
    w(f"| 5-yr NPV | {m(bear_r['npv5'])} | {m(base_r['npv5'])} | {m(bull_r['npv5'])} |")
    w(f"| Customers live 2031 | {bear_r['y5']['customers']:.0f} | {base_r['y5']['customers']:.0f} | "
      f"{bull_r['y5']['customers']:.0f} |")
    w("")
    w("## Sensitivity (NPV swing, one assumption at a time; full table in `verizon_10k_sensitivity.csv`)")
    w("| Assumption | 10-K line | Bear -> Bull value | NPV bear | NPV bull |")
    w("|---|---|---|---:|---:|")
    for s in sens[:10]:
        w(f"| {s['description']} | {s['line_item']} | {s['bear_value']:g} -> {s['bull_value']:g} | "
          f"{m(s['npv_bear'])} | {m(s['npv_bull'])} |")
    w("")
    w("## Every assumption")
    w("| Key | Bear | Base | Bull | Source | 10-K line |")
    w("|---|---:|---:|---:|---|---|")
    for k, v in A.items():
        w(f"| `{k}` ({v[5]}) | {v[0]:g} | {v[1]:g} | {v[2]:g} | {v[3]} | {v[4]} |")
    w("")
    w("Verizon baseline (FY2025 10-K): revenue $138.2B, cost of services $27.8B, SG&A $33.8B, adj. EBITDA $50.0B, "
      "E&PS revenue $13.5B (FY2024 $14.2B). See research/01_sec_forensic.md.")
    with open(os.path.join(ROOT, "FINANCIAL_PROJECTION.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(os.path.join(ROOT, "verizon_10k_sensitivity.csv"), "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=["parameter", "description", "line_item", "bear_value", "base_value",
                                            "bull_value", "npv_bear", "npv_base", "npv_bull", "swing", "source"])
        wr.writeheader()
        for s in sens:
            wr.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in s.items()})


def ledger_lines(y):
    """Every component of 2031 EBITDA, by 10-K line (no plugs: tests check the sum)."""
    return [
        ("Operating revenue (Business / E&PS)", "Layer 1 occupancy-intelligence platform fee", y["rev_platform"]),
        ("Operating revenue (Business / E&PS)", "Layer 2 share of verified HVAC savings", y["rev_performance"]),
        ("Operating revenue (Business / E&PS)", "Layer 3 demand-response share", y["rev_dr"]),
        ("Operating revenue (Business / E&PS)", "Layer 4 slices, Frontline, private 5G pull-through", y["rev_pull_through"]),
        ("Operating revenue (Business / E&PS)", "Implementation fees (share of integration)", y["rev_implementation"]),
        ("Cost of services", "Delivery cost of pull-through services", -y["cos_pull_through"]),
        ("Cost of services", "Platform run (cloud, MEC, SRE)", -y["cos_platform"]),
        ("Cost of services", "M&V and customer support", -y["cos_mv"]),
        ("Cost of services", "Wi-Fi / BMS data and API licences", -y["cos_data"]),
        ("Cost of services", "Privacy and CPNI compliance program", -y["cos_privacy"]),
        ("Cost of services", "Radio energy saved at customer campuses (context vs today's practice)", y["save_ran_energy"]),
        ("Cost of services", "Truck rolls avoided by intent-aware triage", y["save_truck_rolls"]),
        ("SG&A", "Sales & support", -y["sga_sales"]),
        ("SG&A", "Rutgers pilot (2027 only)", -y["sga_pilot"]),
        ("SG&A", "Care contacts avoided on event days", y["save_care"]),
    ]


def run(kpis_path=None, write=True, verbose=True):
    kpis_path = kpis_path or os.path.join(ROOT, "prototype", "out", "sim_kpis.json")
    cal = calibrate(kpis_path)
    apply_calibration(cal)
    results = {s: evaluate(scenario_values(s)) for s in ("bear", "base", "bull")}
    sens = tornado(scenario_values("base"))
    mc = monte_carlo()
    pilot_econ = pilot(cal)
    if write:
        write_outputs(results, sens, mc, cal, pilot_econ)
    b = results["base"]
    y5 = b["y5"]
    dashboard = {
        "year5_ebitda_usd": y5["ebitda"], "year5_revenue_usd": y5["revenue"],
        "year5_ebitda_bps": b["ebitda_bps_of_revenue"], "margin_bps": b["margin_bps"],
        "npv_usd": b["npv5"], "npv_terminal_usd": b["npv_terminal"], "npv_core_usd": b["npv5_core_software"],
        "irr": b["irr"], "wacc": A["wacc"][1], "payback_months": b["payback_months"],
        "year5_ebitda_low_usd": results["bear"]["y5"]["ebitda"], "year5_ebitda_high_usd": results["bull"]["y5"]["ebitda"],
        "lines": [{"line": l, "driver": d, "usd": v} for l, d, v in ledger_lines(y5)],
        "co2e_note": f"Enabled customer HVAC reductions ~{y5['tco2e_enabled']:,.0f} tCO2e/yr by 2031.",
        "pilot": pilot_econ, "monte_carlo": mc,
    }
    if verbose:
        print(f"CFO model: 2031 EBITDA {m(y5['ebitda'])} (bear {m(results['bear']['y5']['ebitda'])}, "
              f"bull {m(results['bull']['y5']['ebitda'])}); 5-yr NPV {m(b['npv5'])}; "
              f"MC P10-P90 NPV {m(mc['npv_p10'])} to {m(mc['npv_p90'])}")
    out = {"dashboard": dashboard, "calibration": cal,
           "scenarios": {k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in results.items()},
           "rows_base": b["rows"]}
    if write:
        os.makedirs(os.path.join(ROOT, "prototype", "out"), exist_ok=True)
        with open(os.path.join(ROOT, "prototype", "out", "finance.json"), "w") as fh:
            json.dump(out, fh, indent=1, default=float)
    return out


def main():
    ap = argparse.ArgumentParser(description="Circadian CFO model")
    ap.add_argument("--kpis", help="path to sim_kpis.json (default prototype/out/sim_kpis.json)")
    ap.add_argument("--print", action="store_true", help="print FINANCIAL_PROJECTION.md after writing it")
    args = ap.parse_args()
    run(args.kpis)
    if args.print:
        with open(os.path.join(ROOT, "FINANCIAL_PROJECTION.md")) as fh:
            print(fh.read())


if __name__ == "__main__":
    main()


assert math.isclose(sum(1 for _ in YEARS), len(RAMP))
