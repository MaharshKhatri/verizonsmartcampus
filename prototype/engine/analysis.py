"""Evidence the pitch relies on, computed from the simulator rather than asserted.

  frontier()          energy saved vs. congestion for every policy setting
  forecast_skill()    forecaster error vs. persistence and timetable-only baselines
  pilot_kpis()        per-scenario results split into everyday zones vs. event venues,
                      consumed by CFO_10K_MODEL.py
"""
from . import campus, sim, triage
from .forecaster import evaluate
from .learning import ARMS
from .config import STEP_MIN

EVERYDAY = [z.key for z in campus.ZONES if z.kind != "venue"]
VENUES = [z.key for z in campus.ZONES if z.kind == "venue"]


def _zone_sum(out, keys, field):
    return sum(sum(out["zones"][k][field]) for k in keys)


def _cong_user_minutes(out, keys, policy_key):
    # congested share x subscribers present, summed over steps and zones, in user-minutes
    from .config import VERIZON_SHARE
    total = 0.0
    for k in keys:
        z = out["zones"][k]
        total += sum(c * o * VERIZON_SHARE for c, o in zip(z[f"cong_{policy_key}"], z["occ"]))
    return total * STEP_MIN


def frontier(model, scenario="weekday", keys=None):
    """Each point: % radio-site energy saved vs always-on and congested user-minutes over `keys` zones."""
    keys = keys or EVERYDAY
    points = []

    def run(extras_update, label, family, key):
        day, extras = sim.make_scenario_day(scenario)
        extras.update(extras_update)
        out = sim.simulate_day(day, extras, sim.fresh(model), record=True)
        a = _zone_sum(out, keys, "w_a")
        saved = 1.0 - _zone_sum(out, keys, f"w_{key}") / a
        points.append({"family": family, "label": label, "saving_pct": round(100 * saved, 1),
                       "congested_user_min": round(_cong_user_minutes(out, keys, key))})

    for s, w in ((0.20, 0.50), (0.35, 0.65), (0.50, 0.75)):
        run({"baseline": "reactive", "reactive": (s, w, False)}, f"light sleep, sleep<{s:.0%} wake>{w:.0%}",
            "legacy thresholds", "b")
        run({"baseline": "reactive", "reactive": (s, w, True)}, f"deep sleep, sleep<{s:.0%} wake>{w:.0%}",
            "legacy thresholds", "b")
    for m in ARMS:
        run({"baseline": "history", "baseline_margin": m, "event_lockout": False}, f"margin +{m:.0%}",
            "traffic-history AI, no event mode", "b")
        run({"baseline": "history", "baseline_margin": m}, f"margin +{m:.0%}",
            "traffic-history AI + event mode (today)", "b")
    for m in ARMS:
        run({"fixed_margin": m}, f"margin +{m:.0%}", "Circadian (fixed margin)", "c")
    run({}, "learned margins", "Circadian (learned)", "c")
    return points


def event_mode_comparison(model, scenarios=("gameday", "arena")):
    """Event days: traffic-history AI with and without the operator's event mode vs Circadian (all zones)."""
    keys = EVERYDAY + VENUES
    rows = []
    for name in scenarios:
        for label, upd in (("Today's AI, no event mode", {"event_lockout": False}),
                           ("Today's AI + manual event mode", {})):
            day, extras = sim.make_scenario_day(name)
            extras.update(upd)
            out = sim.simulate_day(day, extras, sim.fresh(model), record=True)
            a = _zone_sum(out, VENUES, "w_a")
            rows.append({"scenario": name, "policy": label,
                         "congested_user_min": round(_cong_user_minutes(out, keys, "b")),
                         "venue_energy_saved_pct": round(100 * (1 - _zone_sum(out, VENUES, "w_b") / a), 1),
                         "campus_energy_saved_pct": round(100 * (1 - _zone_sum(out, keys, "w_b") / _zone_sum(out, keys, "w_a")), 1)})
        rows.append({"scenario": name, "policy": "Circadian",
                     "congested_user_min": round(_cong_user_minutes(out, keys, "c")),
                     "venue_energy_saved_pct": round(100 * (1 - _zone_sum(out, VENUES, "w_c") / a), 1),
                     "campus_energy_saved_pct": round(100 * (1 - _zone_sum(out, keys, "w_c") / _zone_sum(out, keys, "w_a")), 1)})
    return rows


def hvac_policies(traces):
    """Timetable vs measured-occupancy (no forecast) vs forecast-driven HVAC, per scenario."""
    rows = []
    for name, tr in traces.items():
        s = tr["summary"]
        rows.append({"scenario": name, "timetable_kwh": s["hvac_kwh"]["baseline"],
                     "reactive_saving_pct": s["hvac_reactive_saving_pct"], "circadian_saving_pct": s["hvac_saving_pct"],
                     "miss_timetable": s["comfort_miss_people_steps"]["baseline"],
                     "miss_reactive": s["comfort_miss_people_steps"]["reactive"],
                     "miss_circadian": s["comfort_miss_people_steps"]["circadian"]})
    return rows


def hvac_ventilation_share(model, scenario="weekday"):
    """How much of Circadian's HVAC saving is ventilation-by-headcount vs setback."""
    day, extras = sim.make_scenario_day(scenario)
    extras["hvac_dcv"] = False
    s = sim.simulate_day(day, extras, sim.fresh(model), record=False)["summary"]
    return {"scenario": scenario, "saving_without_ventilation_control_pct": s["hvac_saving_pct"]}


def sensing_ablation(scenarios=("weekday", "surprise", "gameday")):
    """Retrain with each sensing source and compare forecast error (vs truth) and outcomes."""
    from .forecaster import evaluate as ev
    rows = []
    for mode in ("fused", "wifi", "carrier"):
        model = sim.train(sensing=mode)
        for name in scenarios:
            day, extras = sim.make_scenario_day(name)
            extras["sensing"] = mode
            truth, _, _, view = sim._view(day, mode)
            err = ev(model[0], view, 6, truth={k: v["total"] for k, v in truth.items()})
            s = sim.simulate_day(day, extras, sim.fresh(model), record=False)["summary"]
            rows.append({"sensing": mode, "scenario": name, "mae30_vs_truth_pct": round(100 * err["model"], 2),
                         "timetable_mae30_pct": round(100 * err["timetable"], 2),
                         "ran_vs_todays_ai_pct": s["ran_saving_vs_baseline_pct"],
                         "congested_user_steps": s["congested_user_steps"]["circadian"],
                         "hvac_comfort_miss": s["comfort_miss_people_steps"]["circadian"]})
    return rows


def bus_ablation(scenarios=("weekday", "surprise")):
    """Retrain with bus telemetry zeroed: does the bus lead indicator earn its place?"""
    from . import demand as dm
    from .forecaster import evaluate as ev
    original = dm.bus_telemetry

    def zero(inflow, seed, lookahead=4):
        return {c: [[0.0] * len(r) for r in rows] for c, rows in original(inflow, seed, lookahead).items()}
    out = []
    with_bus = sim.train()
    dm.bus_telemetry = zero
    try:
        no_bus = sim.train()
        for name in scenarios:
            day, _ = sim.make_scenario_day(name)
            v0 = sim._view(day)[3]
            dm.bus_telemetry = original
            v1 = sim._view(day)[3]
            dm.bus_telemetry = zero
            out.append({"scenario": name, "mae30_with_bus_pct": round(100 * ev(with_bus[0], v1, 6)["model"], 3),
                        "mae30_without_bus_pct": round(100 * ev(no_bus[0], v0, 6)["model"], 3)})
    finally:
        dm.bus_telemetry = original
    return out


def headroom_sensitivity(model):
    """Game day at SHI with sellout-provisioned capacity vs ~30% less stadium capacity."""
    rows = []
    for label, override in (("sellout-provisioned (6 DAS sectors)", None),
                            ("30% tighter (4 DAS sectors)", {"SHI": {"das": 4}})):
        day, extras = sim.make_scenario_day("gameday")
        if override:
            extras["asset_overrides"] = override
        out = sim.simulate_day(day, extras, sim.fresh(model), record=True)
        rows.append({"stadium": label,
                     "congested_user_min_baseline": round(_cong_user_minutes(out, VENUES, "b")),
                     "congested_user_min_circadian": round(_cong_user_minutes(out, VENUES, "c")),
                     "venue_saving_baseline_pct": round(100 * (1 - _zone_sum(out, VENUES, "w_b") / _zone_sum(out, VENUES, "w_a")), 1),
                     "venue_saving_circadian_pct": round(100 * (1 - _zone_sum(out, VENUES, "w_c") / _zone_sum(out, VENUES, "w_a")), 1)})
    return rows


def demand_skill(model, scenarios=("weekday", "gameday", "arena", "finals", "surprise", "snowday"), horizon=6):
    """30-minute cellular-demand forecast error: Circadian (context) vs today's AI (traffic history).

    Error is normalised per zone by max(peak demand that day, 50 Mbps) so near-empty venues
    don't dominate.
    """
    from .config import VERIZON_SHARE, STEPS_PER_DAY
    fc, _, hist, _ = model
    rows = []
    for name in scenarios:
        day, _ = sim.make_scenario_day(name)
        _, prior, _, view = sim._view(day)
        ec = eh = n = 0.0
        for z in campus.ZONES:
            pt, pr = prior[z.key]["total"], prior[z.key]["rate_people"]
            dem = view.dem_obs[z.key]
            sc = max(max(dem), 50.0)
            for t in range(1, STEPS_PER_DAY - horizon):
                s = t + horizon
                mix = pr[s] / pt[s] if pt[s] > 1 else 0.2
                c50 = fc.predict(view, z, t)[horizon - 1][0] * VERIZON_SHARE * mix
                h50 = hist.predict(view, day.day_type, z, t)[horizon - 1][0]
                ec += abs(c50 - dem[s]) / sc
                eh += abs(h50 - dem[s]) / sc
                n += 1
        rows.append({"scenario": name, "circadian_mae_pct": round(100 * ec / n, 2),
                     "history_ai_mae_pct": round(100 * eh / n, 2)})
    return rows


def forecast_skill(model, scenarios=("weekday", "gameday", "finals", "surprise")):
    fc = model[0]
    rows = []
    for name in scenarios:
        day, _ = sim.make_scenario_day(name)
        view = sim._view(day)[3]
        for h in (1, 3, 6, 12):
            e = evaluate(fc, view, h)
            rows.append({"scenario": name, "horizon_min": h * STEP_MIN,
                         **{k: round(100 * v, 2) for k, v in e.items()}})
    return rows


def pilot_kpis(traces):
    """Per-scenario KPIs split by zone class, for the CFO model."""
    out = {}
    for name, tr in traces.items():
        s = tr["summary"]
        row = {"summary": s}
        for label, keys in (("everyday", EVERYDAY), ("venues", VENUES)):
            a = _zone_sum(tr, keys, "w_a")
            b = _zone_sum(tr, keys, "w_b")
            c = _zone_sum(tr, keys, "w_c")
            row[label] = {
                "always_on_kwh": round(a * STEP_MIN / 60 / 1000, 2),
                "baseline_kwh": round(b * STEP_MIN / 60 / 1000, 2),
                "circadian_kwh": round(c * STEP_MIN / 60 / 1000, 2),
                "baseline_saving_pct": round(100 * (1 - b / a), 2) if a else 0.0,
                "circadian_saving_pct": round(100 * (1 - c / a), 2) if a else 0.0,
                "incremental_vs_baseline_pct": round(100 * (b - c) / b, 2) if b else 0.0,
                "congested_user_min_baseline": round(_cong_user_minutes(tr, keys, "b")),
                "congested_user_min_circadian": round(_cong_user_minutes(tr, keys, "c")),
            }
        out[name] = row
    out["triage_accuracy"] = round(triage.accuracy(), 3)
    out["triage_accuracy_robust"] = round(triage.robust_accuracy(), 3)
    out["triage_storm"] = triage.storm_monte_carlo(sim.SCENARIOS["faultstorm"]["faults"])
    return out
