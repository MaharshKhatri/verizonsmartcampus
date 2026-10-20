"""Build every artifact the dashboard and the financial model consume.

    python3 -m prototype.engine.export [--retrain]

Writes:
  prototype/out/trained_model.json     forecaster + learned margins
  prototype/out/sim_kpis.json          per-scenario KPIs (input to CFO_10K_MODEL.py)
  prototype/out/evidence.json          efficient frontier + forecast skill
  prototype/dashboard/data.js          everything the offline dashboard replays
"""
import argparse
import importlib.util
import json
import os
import time

from . import analysis, campus, sim
from . import config
from .config import ASSET_TYPES, SLEEP_MODES, STEP_MIN

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "prototype", "out")
DASH_DATA = os.path.join(ROOT, "prototype", "dashboard", "data.js")
CFO_PATH = os.path.join(ROOT, "CFO_10K_MODEL.py")

DEMO_INTENTS = [
    "Guarantee 400 Mbps uplink for 12 broadcast cameras at SHI Stadium from 10am to 4:30pm",
    "Low-latency 10 ms slice with 60 Mbps for the robotics lab in Weeks Hall from 10:20am to 11:40am",
    "Priority access for Rutgers Police across Busch campus from 6pm to 11pm",
    "Reserve 300 Mbps for the career fair livestream at Busch Student Center from 1pm to 4pm",
    "Connect 400 air-quality sensors in the Livingston Apartments all day",
    "Give me 5 Gbps at the stadium at 4pm",
]


def campus_geometry():
    return {
        "zones": [{"key": z.key, "name": z.name, "campus": z.campus, "kind": z.kind, "lat": z.lat, "lon": z.lon,
                   "peak": z.peak, "sqft": z.sqft, "assets": z.assets, "study": z.study_space}
                  for z in campus.ZONES],
        "gateways": {k: {"name": v[0], "lat": v[1], "lon": v[2]} for k, v in campus.GATEWAYS.items()},
        "routes": campus.BUS_ROUTES,
        "periods": campus.CLASS_PERIODS,
        "asset_types": {k: {"label": v.label, "layer": v.layer, "p_max_w": v.p_max_w, "p_static_w": v.p_static_w,
                            "capacity_mbps": v.capacity_mbps} for k, v in ASSET_TYPES.items()},
        "sleep_modes": {k: {"static_factor": m.static_factor, "capacity_factor": m.capacity_factor,
                            "wake_min": m.wake_steps * STEP_MIN} for k, m in SLEEP_MODES.items()},
    }


def demo_intents(model):
    from . import slicing, demand
    out = []
    for name, text in (("gameday", DEMO_INTENTS[0]), ("weekday", DEMO_INTENTS[1]), ("weekday", DEMO_INTENTS[2]),
                       ("weekday", DEMO_INTENTS[3]), ("weekday", DEMO_INTENTS[4]), ("gameday", DEMO_INTENTS[5])):
        day, _ = sim.make_scenario_day(name)
        prior = demand.occupancy(day, truth=False)
        spec = slicing.parse(text, day.games)
        res = slicing.admit(spec, prior)
        res["text"] = text
        res["scenario"] = name
        out.append(res)
    return out


def load_cfo():
    if not os.path.exists(CFO_PATH):
        return None
    spec = importlib.util.spec_from_file_location("cfo_model", CFO_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(retrain=False, verbose=True):
    t0 = time.time()
    model = sim.load_or_train(retrain=retrain)
    traces = {}
    for name in sim.SCENARIOS:
        traces[name] = sim.simulate(name, model=model)
        if verbose:
            s = traces[name]["summary"]
            print(f"  {name:11s} radio energy -{s['ran_saving_vs_always_on_pct']}% vs always-on, "
                  f"-{s['ran_saving_vs_baseline_pct']}% vs traffic-history AI; HVAC -{s['hvac_saving_pct']}%; "
                  f"congested user-steps {s['congested_user_steps']['baseline']:.0f} -> "
                  f"{s['congested_user_steps']['circadian']:.0f}")
    kpis = analysis.pilot_kpis(traces)
    all_zones = [z.key for z in campus.ZONES]
    if verbose:
        print("  evidence: frontier, forecast skill, event mode, sensing and bus ablations ...")
    evidence = {"frontier": {"weekday": analysis.frontier(model, "weekday"),
                             "gameday": analysis.frontier(model, "gameday", all_zones)},
                "forecast_skill": analysis.forecast_skill(model),
                "demand_skill": analysis.demand_skill(model),
                "event_mode": analysis.event_mode_comparison(model),
                "hvac_policies": analysis.hvac_policies(traces),
                "hvac_ventilation": analysis.hvac_ventilation_share(model),
                "sensing": analysis.sensing_ablation(),
                "bus": analysis.bus_ablation(),
                "headroom": analysis.headroom_sensitivity(model)}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "sim_kpis.json"), "w") as fh:
        json.dump(kpis, fh, indent=1)
    with open(os.path.join(OUT, "evidence.json"), "w") as fh:
        json.dump(evidence, fh, indent=1)

    finance = None
    cfo = load_cfo()
    if cfo is not None:
        finance = cfo.run(kpis_path=os.path.join(OUT, "sim_kpis.json"), write=True, verbose=verbose)

    payload = {
        "generated": time.strftime("%Y-%m-%d %H:%M"),
        "campus": campus_geometry(),
        "scenarios": {k: {"title": v["title"]} for k, v in sim.SCENARIOS.items()},
        "traces": traces,
        "evidence": evidence,
        "kpis": {k: v for k, v in kpis.items() if not k.startswith("triage")},
        "triage_accuracy": kpis["triage_accuracy"],
        "triage_accuracy_robust": kpis["triage_accuracy_robust"],
        "triage_storm": kpis["triage_storm"],
        "intents": demo_intents(model),
        "finance": finance.get("dashboard") if isinstance(finance, dict) else None,
        "constants": {"energy_price": config.ENERGY_PRICE_USD_KWH, "campus_price": config.CAMPUS_ENERGY_PRICE_USD_KWH,
                      "tco2e_per_mwh": config.GRID_TCO2E_PER_MWH, "truck_roll_usd": config.TRUCK_ROLL_USD,
                      "verizon_share": config.VERIZON_SHARE, "step_min": STEP_MIN},
    }
    with open(DASH_DATA, "w") as fh:
        fh.write("// Generated by prototype/engine/export.py - do not edit by hand.\n")
        fh.write("window.CIRCADIAN_DATA = ")
        json.dump(payload, fh, separators=(",", ":"))
        fh.write(";\n")
    if verbose:
        size = os.path.getsize(DASH_DATA) / 1e6
        print(f"wrote {os.path.relpath(DASH_DATA, ROOT)} ({size:.1f} MB) in {time.time() - t0:.1f}s")
    return payload


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--retrain", action="store_true", help="retrain the forecaster and margin bandit")
    args = ap.parse_args()
    build(retrain=args.retrain)


if __name__ == "__main__":
    main()
