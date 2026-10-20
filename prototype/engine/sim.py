"""Run one campus day: a single ground truth, three RAN policies, two HVAC policies,
two fault-operations models, slices, demand response, and the 10-K ledger.

RAN policies (same radios, same sleep modes, same SLA guard):
  ALWAYS_ON  every carrier active (micro-DTX only) - the reference
  BASELINE   today's practice: traffic-history AI energy saving (RAN KPIs only) with
             learned margins, plus the operator's manual "event mode" that disables
             energy saving on venue cells around ticketed events. Variants via extras:
             baseline="reactive" (legacy thresholds), event_lockout=False
  CIRCADIAN  ours: context-aware forecast (timetable, events, buses, occupancy)

BASELINE and CIRCADIAN share the planner, the SLA guard and the margin learner,
so the measured difference is the value of campus context alone.
"""
import json
import os
import random

from . import buildings, campus, demand, ran, slicing, triage
from .config import (CONGESTION_UTIL, HORIZON_STEPS, SITE_BATTERY_KWH, SITE_BATTERY_RESERVE, SLEEP_MODES,
                     STEP_MIN, STEPS_PER_DAY, VERIZON_SHARE)
from .demand import Event, Game
from .forecaster import DayView, Forecaster, HistoryForecaster
from .learning import ARMS, MarginBandit, reward
from .ledger import Ledger

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out")
MODEL_PATH = os.path.join(OUT_DIR, "trained_model.json")
POLICIES = ("ALWAYS_ON", "BASELINE", "CIRCADIAN")
MEASURED_FLOOR_DECAY = 0.93   # planner floor: measured demand now, fading ~50% over 50 minutes
LOCKOUT_BEFORE, LOCKOUT_AFTER = 24, 48   # baseline "event mode": 2 h before to 4 h after a ticketed event
MODE_CODE = {"ACTIVE": "A", "MIMO_MUTE": "M", "CARRIER_OFF": "C", "DEEP_SLEEP": "D", "DORMANT": "Z"}
EPOCH = 12                    # bandit epoch: one hour
MODEL_VERSION = 14             # bump when features/training change so stale caches retrain


def hm(h, m=0):
    return (h * 60 + m) // STEP_MIN


SCENARIOS = {
    "weekday": dict(
        title="Tuesday in October - a normal class day", day_type="weekday", weather="mild", seed=2026,
        events=[Event("BSC", hm(13), hm(16), 900, True, "Career fair (on the calendar)")],
        slices=["Low-latency 10 ms slice with 60 Mbps for the robotics lab in Weeks Hall from 10:20am to 11:40am"],
        faults=[(hm(11, 15), "HILL-small-2", "software_hang")]),
    "gameday": dict(
        title="Game day: Michigan at SHI Stadium, Sat Oct 31, 12:30 pm kickoff (52,454 seats)",
        day_type="saturday", weather="mild", seed=1869,
        games=[Game("SHI", hm(12, 30), 52_000, "Michigan at Rutgers")],
        slices=["Guarantee 400 Mbps uplink for 12 broadcast cameras at SHI Stadium from 10am to 4:30pm",
                "Priority access for Rutgers Police at SHI Stadium during the game"],
        faults=[(hm(11, 10), "SHI-mmwave-3", "beam_misalignment")]),
    "finals": dict(
        title="Finals week - 24-hour study rush", day_type="finals", weather="mild", seed=1766,
        events=[Event("LSC", hm(21), hm(23, 30), 700, True, "Late-night study break (calendar)")],
        slices=[], faults=[(hm(22, 40), "LSM-small-1", "config_drift")]),
    "heatwave": dict(
        title="September heat wave + PJM demand-response event 2-6 pm", day_type="weekday", weather="hot", seed=777,
        dr_window=(hm(14), hm(18)), slices=[], faults=[]),
    "surprise": dict(
        title="Unannounced 2,500-person rally at Busch Student Center", day_type="weekday", weather="mild", seed=3030,
        events=[Event("BSC", hm(14, 5), hm(15, 20), 2500, False, "Unannounced rally")],
        slices=[], faults=[]),
    "arena": dict(
        title="One-off weeknight game at Jersey Mike's Arena (on the athletics calendar, not in traffic history)",
        day_type="weekday", weather="mild", seed=5150,
        games=[Game("ARENA", hm(19), 8_000, "Weeknight basketball, moved for TV")],
        slices=[], faults=[]),
    "snowday": dict(
        title="Snow day: classes cancelled by a 6 am Rutgers alert", day_type="cancelled", weather="mild",
        seed=2027, slices=[], faults=[]),
    "faultstorm": dict(
        title="Wind storm: seven radio faults in one afternoon", day_type="weekday", weather="mild", seed=4242,
        slices=[],
        faults=[(hm(9, 40), "BSC-mmwave-1", "beam_misalignment"), (hm(10, 5), "ARC-cband-1", "config_drift"),
                (hm(11, 30), "LSC-mmwave-2", "beam_misalignment"), (hm(12, 20), "ENG-small-3", "backhaul_flap"),
                (hm(13, 45), "TIL-cband-1", "pa_failure"), (hm(15, 10), "BRES-small-4", "psu_failure"),
                (hm(16, 0), "RBS-small-1", "software_hang")]),
}


# --------------------------------------------------------------------------
# Training (nightly retrain in production; cached here)
# --------------------------------------------------------------------------
def history_days(n_weekdays=8):
    rng = random.Random(99)
    days = [demand.make_day(f"hist-wd{i}", 500 + i, "weekday", rng.choice(["mild", "warm", "hot"]))
            for i in range(n_weekdays)]
    days.append(demand.make_day("hist-game1", 601, "saturday", "warm", games=[Game("SHI", hm(12), 46_000)]))
    days.append(demand.make_day("hist-game2", 602, "saturday", "mild", games=[Game("SHI", hm(19, 30), 52_000)]))
    days.append(demand.make_day("hist-arena", 603, "weekday", "mild", games=[Game("ARENA", hm(19), 7_200)]))
    days.append(demand.make_day("hist-finals", 604, "finals", "mild"))
    days.append(demand.make_day("hist-sat", 605, "saturday", "mild"))
    return days


def _view(day, sensing="fused"):
    truth = demand.occupancy(day, truth=True)
    prior = demand.occupancy(day, truth=False)
    obs = demand.observe(truth, day.seed, sensing)
    tele = demand.bus_telemetry(demand.bus_inflow(truth), day.seed)
    view = DayView(prior, obs, tele)
    rng = random.Random(day.seed * 7 + 5)
    view.dem_obs = {zk: [demand.demand_mbps(truth[zk], t) * (1.0 + rng.gauss(0.0, 0.03))
                         for t in range(STEPS_PER_DAY)] for zk in truth}   # RAN-measured traffic
    return truth, prior, obs, view


def train(n_weekdays=8, bandit_days=4, verbose=False, sensing="fused"):
    """Nightly retrain: forecaster + traffic-history baseline + one margin bandit per policy."""
    days = history_days(n_weekdays)
    views = [_view(d, sensing)[3] for d in days]
    fc = Forecaster().fit(views)
    hist = HistoryForecaster().fit([(d.day_type, v) for d, v in zip(days, views)])
    zones = [z.key for z in campus.ZONES]
    bandit, bandit_b = MarginBandit(zones), MarginBandit(zones)
    for d in days[:bandit_days]:
        simulate_day(d, {"sensing": sensing}, (fc, bandit, hist, bandit_b), record=False, learn=True)
    if verbose:
        print(f"trained on {len(days)} days; bandits pretrained on {bandit_days}")
    return fc, bandit, hist, bandit_b


def load_or_train(path=MODEL_PATH, retrain=False):
    if not retrain and os.path.exists(path):
        with open(path) as fh:
            data = json.load(fh)
        if data.get("version") == MODEL_VERSION:
            return (Forecaster.from_json(data["forecaster"]), MarginBandit.from_json(data["bandit"]),
                    HistoryForecaster.from_json(data["history"]), MarginBandit.from_json(data["bandit_b"]))
    fc, bandit, hist, bandit_b = train()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump({"version": MODEL_VERSION, "forecaster": fc.to_json(), "bandit": bandit.to_json(),
                   "history": hist.to_json(), "bandit_b": bandit_b.to_json()}, fh)
    return fc, bandit, hist, bandit_b


def fresh(model):
    """Copy of a trained model whose bandits can learn without touching the original."""
    fc, bandit, hist, bandit_b = model
    return (fc, MarginBandit.from_json(bandit.to_json()), hist, MarginBandit.from_json(bandit_b.to_json()))


# --------------------------------------------------------------------------
# Simulation
# --------------------------------------------------------------------------
def make_scenario_day(name, injections=()):
    sc = SCENARIOS[name]
    day = demand.make_day(name, sc["seed"], sc["day_type"], sc["weather"],
                          scheduled_events=list(sc.get("events", [])), games=list(sc.get("games", [])),
                          surprise_rate=0.5)
    extras = {"slices": list(sc.get("slices", [])), "faults": list(sc.get("faults", [])),
              "dr_window": sc.get("dr_window"), "title": sc["title"]}
    for inj in injections:
        if inj.get("type") == "crowd":
            start = int(inj["t"])
            day.events.append(Event(inj["zone"], start, start + int(inj.get("duration", 12)),
                                    int(inj.get("crowd", 2000)), False, inj.get("label", "Injected surge")))
        elif inj.get("type") == "fault":
            extras["faults"].append((int(inj["t"]), inj["asset"], inj["fault"]))
        elif inj.get("type") == "slice":
            extras["slices"].append(inj["text"])
    return day, extras


def simulate(name, injections=(), model=None, record=True):
    day, extras = make_scenario_day(name, injections)
    return simulate_day(day, extras, fresh(model or load_or_train()), record=record, learn=True)


def simulate_day(day, extras, model, record=True, learn=True):
    fc, bandit, hist, bandit_b = model
    baseline_mode = extras.get("baseline", "history")
    fixed_b = extras.get("baseline_margin")
    event_lockout = extras.get("event_lockout", True)
    truth, prior, obs, view = _view(day, extras.get("sensing", "fused"))

    blend = extras.get("blend_history", True)
    irregular_day = day.day_type not in ("weekday", "saturday") or bool(day.games)

    def ordinary(zk, t):
        """Calendar says nothing unusual for this zone in the next two hours: traffic history is valid."""
        if irregular_day and (day.day_type != "weekday" or any(g.zone == zk for g in day.games)):
            return False
        return not any(ev.announced and ev.zone == zk and ev.start - 24 <= t < ev.end for ev in day.events)

    def locked(zk, t):
        """Operator event mode: no energy saving on a venue from 2 h before to 4 h after a ticketed event."""
        return event_lockout and any(g.zone == zk and g.kickoff - LOCKOUT_BEFORE - 3 <= t < g.kickoff + LOCKOUT_AFTER
                                     for g in day.games)
    zones = campus.ZONES
    weather = day.weather
    dr_window = extras.get("dr_window")
    ledger = Ledger()
    feed = []

    # ---- slices: parsed from natural language, admitted against the forecast
    reservations, slice_log = [], []
    for text in extras.get("slices", []):
        spec = slicing.parse(text, day.games)
        res = slicing.admit(spec, prior, reservations=reservations)
        if res["status"] == "COUNTER_OFFER":
            spec.mbps = float(res["offer_mbps"])
        if res["status"] in ("ADMITTED", "COUNTER_OFFER"):
            reservations.append(spec)
            ledger.slice_admitted(spec, res)
            feed.append(_entry(0, "slice", ",".join(spec.zones), "", res["status"],
                               f"{spec.slice_type} {spec.mbps:.0f} Mbps {spec.direction} "
                               f"{res['spec']['window']} (SST {spec.sst}, 5QI {spec.five_qi}) - provisioned in <1 s"))
        slice_log.append(res)

    def reserved(zk, t):
        return sum(s.mbps / len(s.zones) for s in reservations if zk in s.zones and s.start - 3 <= t < s.end)

    def slice_traffic(zk, t):
        return sum(0.8 * s.mbps / len(s.zones) for s in reservations
                   if zk in s.zones and s.start <= t < s.end and s.slice_type != "MC-PRIORITY")

    # ---- networks and faults
    nets = {p: ran.build_network(extras.get("asset_overrides")) for p in POLICIES}
    zone_assets = {p: ran.by_zone(nets[p]) for p in POLICIES}
    by_id = {p: {a.id: a for a in nets[p]} for p in POLICIES}
    rng_sq, rng_ci = random.Random(day.seed * 3 + 1), random.Random(day.seed * 5 + 2)
    cases = {"sq": [], "ci": []}
    for start, aid, ftype in sorted(extras.get("faults", [])):
        if aid not in by_id["CIRCADIAN"]:
            continue
        zk = by_id["CIRCADIAN"][aid].zone
        cases["sq"].append(triage.status_quo(aid, zk, ftype, start, rng_sq))
        cases["ci"].append(triage.circadian(aid, zk, ftype, start, rng_ci))
    ops_for = {"ALWAYS_ON": "sq", "BASELINE": "sq", "CIRCADIAN": "ci"}
    for sq, ci in zip(cases["sq"], cases["ci"]):
        ledger.fault(sq, ci)
        feed.append(_entry(ci.start + triage.CI_DETECT, "triage", ci.zone, ci.asset_id, ci.action,
                           f"{triage.FAULTS[ci.ftype][2]} - diagnosed {ci.diagnosis}; "
                           f"{'no truck roll' if ci.trucks == 0 else str(ci.trucks) + ' truck roll(s)'}; "
                           f"status quo: {sq.trucks} truck roll(s), "
                           f"restored after {(sq.repaired_at - sq.start) * STEP_MIN} min vs "
                           f"{(ci.repaired_at - ci.start) * STEP_MIN} min"))

    def compensation(policy, zk, t):
        """Circadian lends neighbour capacity to a zone with a detected hardware outage."""
        if policy != "CIRCADIAN":
            return 0.0, 0.0
        mbps = w = 0.0
        for case in cases["ci"]:
            if case.zone == zk and triage.FAULTS[case.ftype][0] == "hard" and \
                    case.start + triage.CI_DETECT <= t < case.repaired_at:
                spec = by_id["CIRCADIAN"][case.asset_id].spec
                mbps += triage.COMPENSATION_SHARE * spec.capacity_mbps
                w += triage.COMPENSATION_W
        return mbps, w

    # ---- per-zone helpers
    mix = {}
    for z in zones:
        pt, pr = prior[z.key]["total"], prior[z.key]["rate_people"]
        mix[z.key] = [(pr[t] / pt[t]) if pt[t] > 1 else 0.2 for t in range(STEPS_PER_DAY)]

    last_demand = {z.key: 0.0 for z in zones}

    def floor(zk, k):
        """Never plan below what the radios are measuring now (decays over the horizon)."""
        return last_demand[zk] * MEASURED_FLOOR_DECAY ** k
    last_util = {p: {z.key: 0.0 for z in zones} for p in POLICIES}
    hvac = buildings.CircadianHVAC(dcv=extras.get("hvac_dcv", True))
    hvac_reactive = buildings.CircadianHVAC()
    battery_used = {z.key: 0.0 for z in zones}
    fixed = extras.get("fixed_margin")
    learn_c = learn and fixed is None
    learn_b = learn and fixed_b is None
    arm = {z.key: (ARMS.index(fixed) if fixed is not None else
                   bandit.choose(z.key) if learn_c else bandit.exploit(z.key)) for z in zones}
    arm_b = {z.key: (bandit_b.choose(z.key) if learn_b else bandit_b.exploit(z.key)) for z in zones}
    epoch_kwh = {z.key: [0.0, 0.0, 0.0] for z in zones}
    epoch_cong = {z.key: [0, 0] for z in zones}
    last_contrast = {}

    rec = _Recorder(zones, nets["CIRCADIAN"]) if record else None
    reactive_thresholds = extras.get("reactive", (ran.REACTIVE_SLEEP_UTIL, ran.REACTIVE_WAKE_UTIL))

    for t in range(STEPS_PER_DAY):
        # faults (each policy sees its own ops model's repair time)
        for p in POLICIES:
            for case in cases[ops_for[p]]:
                a = by_id[p][case.asset_id]
                if case.start <= t < case.repaired_at:
                    a.fault, a.fault_capacity = case.ftype, triage.FAULTS[case.ftype][1]
                elif t == case.repaired_at:
                    a.fault, a.fault_capacity = "", 1.0

        # forecasts made with telemetry up to t-1, for steps t .. t+11
        fcast = {}
        for z in zones:
            if t == 0:
                pt = prior[z.key]["total"]
                fcast[z.key] = [(pt[min(k, STEPS_PER_DAY - 1)], pt[min(k, STEPS_PER_DAY - 1)] * 1.2)
                                for k in range(HORIZON_STEPS)]
            else:
                fcast[z.key] = fc.predict(view, z, t - 1)

        # policy decisions
        guard_zones = set()
        for z in zones:
            if baseline_mode == "reactive":
                ran.reactive_step(zone_assets["BASELINE"][z.key], last_demand[z.key], t, *reactive_thresholds)
            elif locked(z.key, t):
                for a in zone_assets["BASELINE"][z.key]:
                    if a.spec.layer == "capacity" and not a.fault and a.mode != "ACTIVE":
                        a.request("ACTIVE")
            else:
                margin_b = fixed_b if fixed_b is not None else ARMS[arm_b[z.key]]
                need_b = [max(p90 * (1.0 + margin_b), floor(z.key, k)) / ran.TARGET_UTIL
                          + reserved(z.key, min(t + k, STEPS_PER_DAY - 1))
                          for k, (_, p90) in enumerate(hist.predict(view, day.day_type, z, max(0, t - 1)))]
                ran.circadian_step(zone_assets["BASELINE"][z.key], need_b, last_util["BASELINE"][z.key])
            margin = ARMS[arm[z.key]]
            need = []
            hist_p90 = None
            if blend and ordinary(z.key, t):
                hist_p90 = [p90 for _, p90 in hist.predict(view, day.day_type, z, max(0, t - 1))]
            for k, (_, p90) in enumerate(fcast[z.key]):
                s = min(t + k, STEPS_PER_DAY - 1)
                dem90 = p90 * VERIZON_SHARE * mix[z.key][s]
                if hist_p90 is not None:     # calendar says ordinary: average with traffic history
                    dem90 = 0.5 * (dem90 + hist_p90[k])
                need.append(max(dem90 * (1.0 + margin), floor(z.key, k)) / ran.TARGET_UTIL + reserved(z.key, s))
            changes, guard = ran.circadian_step(zone_assets["CIRCADIAN"][z.key], need,
                                                last_util["CIRCADIAN"][z.key])
            if guard:
                guard_zones.add(z.key)
                ledger.guard_events += 1
            for a, action, why in changes:
                feed.append(_entry(t, "ran", z.key, a.id, action, why))

        # serve demand
        for z in zones:
            d = demand.demand_mbps(truth[z.key], t) + slice_traffic(z.key, t)
            subs = truth[z.key]["total"][t] * VERIZON_SHARE
            results = {}
            for p in POLICIES:
                comp_mbps, comp_w = compensation(p, z.key, t)
                cap, util, watts, cong = ran.serve(zone_assets[p][z.key], d, comp_mbps, comp_w)
                results[p] = (cap, util, watts, cong)
                ledger.ran(p, z.key, watts, cong * subs, cong > 0)
                last_util[p][z.key] = d / cap if cap > 0 else 9.9
            last_demand[z.key] = d
            epoch_kwh[z.key][0] += results["ALWAYS_ON"][2]
            epoch_kwh[z.key][1] += results["CIRCADIAN"][2]
            epoch_kwh[z.key][2] += results["BASELINE"][2]
            epoch_cong[z.key][0] += results["CIRCADIAN"][3] > 0
            epoch_cong[z.key][1] += results["BASELINE"][3] > 0
            if results["BASELINE"][3] > 0.02 and results["CIRCADIAN"][3] == 0 and \
                    t - last_contrast.get(z.key, -99) >= 6:
                last_contrast[z.key] = t
                feed.append(_entry(t, "contrast", z.key, "", "BASELINE MISS",
                                   f"Traffic-history AI congested {results['BASELINE'][3]:.0%} of users here "
                                   f"(no timetable/event context); Circadian had capacity pre-woken"))

            # buildings
            people_now = obs[z.key][t - 1] if t > 0 else prior[z.key]["total"][0]
            b_kw, _, b_miss = buildings.baseline_kw(z, weather, t, day, truth[z.key]["total"][t])
            p90s = [p90 for _, p90 in fcast[z.key]]
            c_kw, cond, c_miss, note = hvac.step(z, weather, t, people_now, p90s, dr_window,
                                                 people_true=truth[z.key]["total"][t])
            r_kw, _, r_miss, _ = hvac_reactive.step(z, weather, t, people_now, [], None,
                                                    people_true=truth[z.key]["total"][t])
            ledger.hvac(b_kw, c_kw, b_miss, c_miss, r_kw, r_miss)
            if note and z.kind not in ("residence",):
                feed.append(_entry(t, "hvac", z.key, "", "PRE-CONDITION" if "pre" in note else "SETBACK", note))

            # demand response: cell-site batteries carry the radios during the event
            dr_kw = 0.0
            if dr_window and dr_window[0] <= t < dr_window[1]:
                dr_kw += max(0.0, b_kw - c_kw)
                macro = sum(n for typ, n in z.assets.items() if typ in ("cband", "das"))
                if macro:
                    cap_kwh = SITE_BATTERY_KWH * macro * (1.0 - SITE_BATTERY_RESERVE)
                    site_kw = results["CIRCADIAN"][2] / 1000.0
                    take = min(site_kw, max(0.0, cap_kwh - battery_used[z.key]) * 60.0 / STEP_MIN)
                    battery_used[z.key] += take * STEP_MIN / 60.0
                    dr_kw += take
                ledger.dr(dr_kw)
            if rec:
                rec.zone_step(z.key, t, truth[z.key]["total"][t], obs[z.key][t], fcast[z.key], d, results,
                              b_kw, c_kw, ARMS[arm[z.key]], dr_kw)

        if dr_window and t == dr_window[0]:
            feed.append(_entry(t, "grid", "CAMPUS", "", "DEMAND RESPONSE",
                               "PJM event: +3F setpoints in academic buildings, cell sites on battery "
                               f"(keeping {SITE_BATTERY_RESERVE:.0%} reserve for outages)"))

        # bandit epoch
        if (learn_c or learn_b) and (t + 1) % EPOCH == 0:
            for z in zones:
                ref, circ, base = epoch_kwh[z.key]
                if ref > 0 and learn_c:
                    bandit.update(z.key, arm[z.key], reward(circ / ref, epoch_cong[z.key][0]))
                    arm[z.key] = bandit.choose(z.key)
                if ref > 0 and learn_b:
                    bandit_b.update(z.key, arm_b[z.key], reward(base / ref, epoch_cong[z.key][1]))
                    arm_b[z.key] = bandit_b.choose(z.key)
                epoch_kwh[z.key] = [0.0, 0.0, 0.0]
                epoch_cong[z.key] = [0, 0]

        if rec:
            rec.modes(t, nets["BASELINE"], nets["CIRCADIAN"])
            rec.cumulative(ledger)
        for p in POLICIES:
            for a in nets[p]:
                a.tick()

    feed.sort(key=lambda e: e["t"])
    summary = ledger.summary(day, extras)
    if not rec:
        return {"summary": summary}
    return rec.export(day, extras, summary, feed, slice_log, cases)


def _entry(t, kind, zone, asset, action, reason):
    m = (t * STEP_MIN) % (24 * 60)
    return {"t": t, "clock": f"{m // 60:02d}:{m % 60:02d}", "kind": kind, "zone": zone, "asset": asset,
            "action": action, "reason": reason}


class _Recorder:
    FIELDS = ("occ", "obs", "fc30", "fc30hi", "dem", "cap_a", "cap_b", "cap_c", "util_b", "util_c",
              "w_a", "w_b", "w_c", "cong_b", "cong_c", "hvac_b", "hvac_c", "margin", "dr_kw")

    def __init__(self, zones, assets):
        self.z = {z.key: {f: [0] * STEPS_PER_DAY for f in self.FIELDS} for z in zones}
        self.assets = [{"id": a.id, "zone": a.zone, "type": a.type} for a in assets]
        self.modes_b, self.modes_c = [], []
        self.cum = {k: [] for k in ("kwh_a", "kwh_b", "kwh_c", "hvac_b", "hvac_c", "cong_b", "cong_c",
                                    "trucks_sq", "trucks_ci", "usd_cos", "usd_sga", "tco2e", "dr_kwh")}

    def zone_step(self, zk, t, occ, obs, fcast, d, results, b_kw, c_kw, margin, dr_kw):
        r = self.z[zk]
        r["occ"][t], r["obs"][t] = round(occ), round(obs)
        if t + 5 < STEPS_PER_DAY:          # forecast made at t-1 for t+5 = 30 minutes ahead
            r["fc30"][t + 5], r["fc30hi"][t + 5] = round(fcast[5][0]), round(fcast[5][1])
        r["dem"][t] = round(d, 1)
        for p, key in (("ALWAYS_ON", "a"), ("BASELINE", "b"), ("CIRCADIAN", "c")):
            cap, util, watts, cong = results[p]
            r[f"cap_{key}"][t] = round(cap)
            r[f"w_{key}"][t] = round(watts)
            if key != "a":
                r[f"util_{key}"][t] = round(min(9.99, d / cap if cap else 9.99), 3)
                r[f"cong_{key}"][t] = round(cong, 3)
        r["hvac_b"][t], r["hvac_c"][t] = round(b_kw, 1), round(c_kw, 1)
        r["margin"][t] = margin
        r["dr_kw"][t] = round(dr_kw, 1)

    def modes(self, t, net_b, net_c):
        def code(a):
            if a.fault:
                return "F"
            if a.waking:
                return "W"
            return MODE_CODE[a.mode]
        self.modes_b.append("".join(code(a) for a in net_b))
        self.modes_c.append("".join(code(a) for a in net_c))

    def cumulative(self, ledger):
        snap = ledger.snapshot()
        for k in self.cum:
            self.cum[k].append(round(snap[k], 3))

    def export(self, day, extras, summary, feed, slice_log, cases):
        return {
            "meta": {"name": day.name, "title": extras.get("title", day.name), "day_type": day.day_type,
                     "weather": day.weather, "attendance": round(day.attendance, 3), "step_min": STEP_MIN,
                     "dr_window": extras.get("dr_window"), "baseline": extras.get("baseline", "history"),
                     "games": [{"zone": g.zone, "kickoff": g.kickoff, "attendance": g.attendance} for g in day.games],
                     "events": [{"zone": e.zone, "start": e.start, "end": e.end, "crowd": e.crowd,
                                 "announced": e.announced, "label": e.label} for e in day.events]},
            "zones": self.z,
            "assets": self.assets,
            "modes_b": self.modes_b,
            "modes_c": self.modes_c,
            "cum": self.cum,
            "feed": feed[:1500],
            "slices": slice_log,
            "faults": [{"asset": sq.asset_id, "zone": sq.zone, "type": sq.ftype, "label": triage.FAULTS[sq.ftype][2],
                        "start": sq.start, "sq": {"end": sq.repaired_at, "trucks": sq.trucks, "action": sq.action},
                        "ci": {"end": ci.repaired_at, "trucks": ci.trucks, "action": ci.action,
                               "diagnosis": ci.diagnosis}}
                       for sq, ci in zip(cases["sq"], cases["ci"])],
            "summary": summary,
        }


assert set(MODE_CODE) == set(SLEEP_MODES)
assert CONGESTION_UTIL < 1.0
