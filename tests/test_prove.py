"""PROVE: acoustic test, triage routing, evidence ledger, fleet comparison."""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from prototype.prove import acoustic, fleet, triage  # noqa: E402
from prototype.prove.ledger import EvidenceLedger  # noqa: E402


class TestAcoustic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = acoustic.compare_designs(trials=6, seed=2)

    def test_threshold_clears_noise(self):
        m = acoustic.noise_only_margins(n=60)
        self.assertLess(m.max(), acoustic.PASS_DB - 2.0)

    def test_two_direction_correct_everywhere(self):
        for name, r in self.rows.items():
            self.assertGreaterEqual(r["two_direction_correct"], 0.99, name)

    def test_each_direction_isolates_its_fault(self):
        self.assertLess(self.rows["speaker_dead"]["median_down_db"], acoustic.PASS_DB)
        self.assertGreater(self.rows["speaker_dead"]["median_up_db"], acoustic.PASS_DB)
        self.assertLess(self.rows["mic_taped"]["median_up_db"], acoustic.PASS_DB)
        self.assertGreater(self.rows["mic_taped"]["median_down_db"], acoustic.PASS_DB)

    def test_naive_loopback_fails_healthy_voice_switched_phone(self):
        self.assertLessEqual(self.rows["healthy"]["loopback_pass_rate"], 0.2)
        self.assertGreaterEqual(self.rows["healthy_no_echo_control"]["loopback_pass_rate"], 0.8)

    def test_weak_speaker_shows_as_margin_drop(self):
        drop = self.rows["healthy"]["median_down_db"] - self.rows["speaker_weak"]["median_down_db"]
        self.assertGreater(drop, 10.0)


class TestTriage(unittest.TestCase):
    def test_routes_rf_to_verizon_and_mic_to_contractor(self):
        self.assertEqual(triage.diagnose({"call_setup_fail", "down_fail", "up_fail", "rsrp_low"})["fault"], "rf")
        self.assertEqual(triage.diagnose({"up_fail", "up_hf_loss"})["owner"], "Elevator contractor")
        self.assertEqual(triage.diagnose({"label_mismatch"})["fault"], "label")

    def test_accuracy_and_robustness(self):
        self.assertGreater(triage.accuracy(trials=1500)["owner_accuracy"], 0.85)
        self.assertGreater(triage.accuracy(trials=1500, perturb=0.15)["owner_accuracy"], 0.8)


class TestLedger(unittest.TestCase):
    def test_tamper_is_detected(self):
        led = EvidenceLedger()
        for n in range(5):
            led.append({"car": "car-001", "night": n, "result": "PASS", "down_db": 60, "up_db": 61})
        self.assertEqual(led.verify(), (True, None))
        led.entries[2]["record"]["result"] = "FAIL"
        self.assertEqual(led.verify(), (False, 2))

    def test_deleting_an_entry_breaks_chain(self):
        led = EvidenceLedger()
        for n in range(4):
            led.append({"car": "car-002", "night": n, "result": "PASS"})
        del led.entries[1]
        self.assertFalse(led.verify()[0])


class TestFleet(unittest.TestCase):
    def test_regime_ordering(self):
        rows = fleet.compare(cars=40, seeds=range(4))
        self.assertGreater(rows["annual"]["broken_car_days"], rows["line_monitor"]["broken_car_days"])
        self.assertGreater(rows["line_monitor"]["broken_car_days"], 3 * rows["prove"]["broken_car_days"])

    def test_edge_shrinks_without_silent_faults(self):
        rates = {k: (r if lm else 0.0, rep, lm) for k, (r, rep, lm) in fleet.RATES.items()}
        lm = fleet.simulate(cars=60, seed=1, regime="line_monitor", rates=rates, migrate=False)
        pr = fleet.simulate(cars=60, seed=1, regime="prove", rates=rates, migrate=False)
        # with only line faults, a line monitor is as good as PROVE (within repair-time noise)
        self.assertLess(abs(lm["broken_car_days"] - pr["broken_car_days"]), 0.2 * lm["broken_car_days"] + 5)


if __name__ == "__main__":
    unittest.main()
