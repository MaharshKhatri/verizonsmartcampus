"""Verification tests for the Circadian prototype.  Run:  python3 -m unittest discover -s tests"""
import importlib.util
import json
import os
import sys
import threading
import unittest
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from prototype.engine import analysis, campus, demand, forecaster, ran, sim, slicing, triage  # noqa: E402
from prototype.engine.config import SLEEP_MODES, STEPS_PER_DAY  # noqa: E402

MODEL = sim.load_or_train()
_CACHE = {}


def run(name, injections=()):
    key = (name, json.dumps(injections, sort_keys=True))
    if key not in _CACHE:
        _CACHE[key] = sim.simulate(name, injections=list(injections), model=MODEL)
    return _CACHE[key]


class ForecasterTests(unittest.TestCase):
    def test_beats_persistence_and_timetable_at_30_min(self):
        day, _ = sim.make_scenario_day("weekday")
        view = sim._view(day)[3]
        err = forecaster.evaluate(MODEL[0], view, horizon=6)
        self.assertLess(err["model"], err["persistence"] * 0.6)
        self.assertLess(err["model"], err["timetable"])

    def test_p90_is_above_p50(self):
        day, _ = sim.make_scenario_day("gameday")
        view = sim._view(day)[3]
        for z in campus.ZONES:
            for p50, p90 in MODEL[0].predict(view, z, 140):
                self.assertGreaterEqual(p90, p50)

    def test_wifi_sees_buildings_carrier_sees_the_stadium(self):
        day, _ = sim.make_scenario_day("gameday")
        truth = demand.occupancy(day)

        def err(mode, zone, t0=120, t1=200):
            o = demand.observe(truth, day.seed, mode)[zone]
            tr = truth[zone]["total"]
            return sum(abs(o[t] - tr[t]) for t in range(t0, t1)) / sum(max(tr[t], 1) for t in range(t0, t1))
        self.assertGreater(err("wifi", "SHI"), 0.5)          # Wi-Fi is blind in the bowl
        self.assertLess(err("fused", "SHI"), 0.2)            # carrier/DAS counts fill the gap
        self.assertLess(err("fused", "BSC"), err("carrier", "BSC"))   # indoors Wi-Fi beats carrier

    def test_k_anonymity_floor(self):
        day = demand.make_day("t", 1)
        obs = demand.observe(demand.occupancy(day), 1)
        for row in obs.values():
            for v in row:
                self.assertTrue(v == demand.K_ANON_FLOOR // 2 or v >= demand.K_ANON_FLOOR)


class RadioTests(unittest.TestCase):
    def test_dormant_radio_needs_its_wake_latency(self):
        a = ran.Asset("X-cband-1", "BSC", "cband", mode="DORMANT")
        a.request("ACTIVE")
        for _ in range(SLEEP_MODES["DORMANT"].wake_steps):
            self.assertEqual(a.capacity(), 0.0)
            a.tick()
        self.assertGreater(a.capacity(), 0.0)

    def test_sleep_saves_power(self):
        a = ran.Asset("X-cband-1", "BSC", "cband")
        idle = a.power(0.0)
        for mode in ("CARRIER_OFF", "DEEP_SLEEP", "DORMANT"):
            a.mode = mode
            self.assertLess(a.power(0.0), idle)
            idle = a.power(0.0)

    def test_planner_never_picks_a_mode_it_cannot_wake_from_in_time(self):
        for slack in range(0, 13):
            mode = ran.deepest_allowed(slack)
            if mode:
                self.assertLessEqual(SLEEP_MODES[mode].wake_steps + 1, slack)

    def test_coverage_layer_never_sleeps(self):
        out = run("weekday")
        idx = [i for i, a in enumerate(out["assets"]) if a["type"] == "lowband"]
        for modes in out["modes_c"]:
            for i in idx:
                self.assertIn(modes[i], "AF")


class SimulationTests(unittest.TestCase):
    def test_deterministic(self):
        a = sim.simulate("weekday", model=MODEL)["summary"]
        b = sim.simulate("weekday", model=MODEL)["summary"]
        self.assertEqual(a, b)

    def test_energy_ordering(self):
        for name in sim.SCENARIOS:
            s = run(name)["summary"]["ran_kwh"]
            self.assertLess(s["circadian"], s["always_on"], name)
            self.assertLess(s["baseline"], s["always_on"], name)

    def test_game_day_stays_uncongested(self):
        s = run("gameday")["summary"]["congested_user_steps"]
        self.assertEqual(s["circadian"], 0)

    def test_event_days_beat_todays_practice(self):
        """Without event mode today's AI congests at the one-off arena game; with event mode it
        wastes venue energy. Circadian must avoid both."""
        rows = {(r["scenario"], r["policy"]): r for r in analysis.event_mode_comparison(MODEL)}
        self.assertGreater(rows[("arena", "Today's AI, no event mode")]["congested_user_min"], 1000)
        for day in ("gameday", "arena"):
            circ = rows[(day, "Circadian")]
            self.assertEqual(circ["congested_user_min"], 0, day)
            self.assertGreater(circ["venue_energy_saved_pct"],
                               rows[(day, "Today's AI + manual event mode")]["venue_energy_saved_pct"] + 1.0, day)

    def test_ordinary_days_tie(self):
        for name in ("weekday", "finals", "heatwave", "surprise"):
            self.assertLess(abs(run(name)["summary"]["ran_saving_vs_baseline_pct"]), 1.5, name)

    def test_context_saves_energy_when_campus_is_quieter_than_history(self):
        self.assertGreater(run("snowday")["summary"]["ran_saving_vs_baseline_pct"], 1.0)

    def test_guard_contains_an_unannounced_crowd(self):
        inj = ({"type": "crowd", "zone": "HILL", "t": 170, "crowd": 1500, "duration": 12},)
        out = run("weekday", inj)
        congested = sum(1 for c in out["zones"]["HILL"]["cong_c"] if c > 0)
        self.assertLessEqual(congested, 4)
        self.assertTrue(any("SLA guard" in e["reason"] for e in out["feed"] if e["zone"] == "HILL"))

    def test_hvac_saves_energy_without_leaving_people_in_setback(self):
        for name in sim.SCENARIOS:
            s = run(name)["summary"]
            self.assertLess(s["hvac_kwh"]["circadian"], s["hvac_kwh"]["baseline"], name)
            miss = s["comfort_miss_people_steps"]
            self.assertLess(miss["circadian"], miss["reactive"], name)   # the forecast is what buys comfort
            self.assertLess(miss["circadian"], miss["baseline"], name)

    def test_triage_reduces_truck_rolls_and_outage_time(self):
        mc = triage.storm_monte_carlo(sim.SCENARIOS["faultstorm"]["faults"], n=400)
        self.assertGreater(mc["dispatch_avoided_share"], 0.15)
        self.assertLess(mc["outage_min_circadian"], mc["outage_min_status_quo"])

    def test_demand_response_sheds_load(self):
        s = run("heatwave")["summary"]
        self.assertGreater(s["dr_kwh"], 0)

    def test_trace_shapes(self):
        out = run("weekday")
        self.assertEqual(len(out["modes_c"]), STEPS_PER_DAY)
        for z in campus.ZONES:
            self.assertEqual(len(out["zones"][z.key]["occ"]), STEPS_PER_DAY)


class TriageTests(unittest.TestCase):
    def test_diagnosis_accuracy(self):
        self.assertGreater(triage.accuracy(), 0.75)


class SlicingTests(unittest.TestCase):
    def test_broadcast_uplink(self):
        s = slicing.parse("Guarantee 400 Mbps uplink for 12 broadcast cameras at SHI Stadium from 10am to 4:30pm")
        self.assertEqual((s.zones, s.mbps, s.direction, s.slice_type, s.sst, s.five_qi),
                         (["SHI"], 400.0, "UL", "eMBB-UL", 1, "2"))
        self.assertEqual(s.to_dict()["window"], "10:00-16:30")

    def test_urllc(self):
        s = slicing.parse("Low-latency 10 ms slice with 60 Mbps for the robotics lab in Weeks Hall from 10:20am to 11:40am")
        self.assertEqual((s.zones, s.slice_type, s.sst, s.five_qi), (["ENG"], "URLLC", 2, "82"))

    def test_public_safety_campus_wide(self):
        s = slicing.parse("Priority access for Rutgers Police across Busch campus from 6pm to 11pm")
        self.assertEqual(s.slice_type, "MC-PRIORITY")
        self.assertEqual(set(s.zones), {z.key for z in campus.ZONES if z.campus == "busch"})

    def test_ambiguous_time(self):
        s = slicing.parse("need 50 mbps at hill center 10 to 2pm")
        self.assertEqual(s.to_dict()["window"], "10:00-14:00")

    def test_missing_window_asks_a_question(self):
        day, _ = sim.make_scenario_day("gameday")
        res = slicing.admit(slicing.parse("Give me 5 Gbps at the stadium at 4pm", day.games),
                            demand.occupancy(day, truth=False))
        self.assertEqual(res["status"], "NEEDS_INFO")

    def test_oversubscription_is_not_admitted(self):
        day, _ = sim.make_scenario_day("gameday")
        res = slicing.admit(slicing.parse("Give me 8 Gbps at the stadium from 12pm to 3pm", day.games),
                            demand.occupancy(day, truth=False))
        self.assertIn(res["status"], ("COUNTER_OFFER", "REJECTED"))


class FinanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("cfo", os.path.join(ROOT, "CFO_10K_MODEL.py"))
        cls.cfo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.cfo)

    def test_scenarios_are_ordered(self):
        e = {s: self.cfo.evaluate(self.cfo.scenario_values(s)) for s in ("bear", "base", "bull")}
        self.assertLess(e["bear"]["y5"]["ebitda"], e["base"]["y5"]["ebitda"])
        self.assertLess(e["base"]["y5"]["ebitda"], e["bull"]["y5"]["ebitda"])

    def test_ledger_lines_sum_to_ebitda(self):
        y5 = self.cfo.evaluate(self.cfo.scenario_values("base"))["y5"]
        total = sum(v for _, _, v in self.cfo.ledger_lines(y5))
        self.assertAlmostEqual(total, y5["ebitda"], delta=1.0)

    def test_irr_matches_npv_sign(self):
        flows = [-100.0, 30.0, 40.0, 50.0, 60.0]
        r = self.cfo.irr(flows)
        self.assertAlmostEqual(self.cfo.npv(r, flows), 0.0, delta=1e-6)


class ServerTests(unittest.TestCase):
    def test_intent_endpoint(self):
        from http.server import ThreadingHTTPServer
        from prototype import server
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            port = httpd.server_address[1]
            body = json.dumps({"text": "Reserve 300 Mbps at Busch Student Center from 1pm to 4pm",
                               "scenario": "weekday"}).encode()
            req = urllib.request.Request(f"http://127.0.0.1:{port}/api/intent", data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.load(resp)
            self.assertIn(data["status"], ("ADMITTED", "COUNTER_OFFER"))
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=10) as resp:
                self.assertTrue(json.load(resp)["ok"])
        finally:
            httpd.shutdown()
            httpd.server_close()


class DashboardDataTests(unittest.TestCase):
    def test_data_bundle(self):
        path = os.path.join(ROOT, "prototype", "dashboard", "data.js")
        if not os.path.exists(path):
            self.skipTest("run python3 scripts/build_all.py first")
        with open(path) as fh:
            text = fh.read()
        payload = json.loads(text[text.index("=") + 1:].rstrip().rstrip(";"))
        self.assertEqual(set(payload["traces"]), set(sim.SCENARIOS))
        for key in ("campus", "evidence", "intents", "constants"):
            self.assertIn(key, payload)


if __name__ == "__main__":
    unittest.main()
