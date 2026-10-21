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


class TestSupervisor(unittest.TestCase):
    def test_every_rig_button_routes_to_the_right_owner(self):
        from prototype.prove import export
        expected = {"healthy": (None, "PASS"), "copper_cut": ("copper", "FAIL"), "antenna": ("rf", "FAIL"),
                    "mains": ("power", "WARN"), "speaker": ("speaker", "FAIL"), "mic_taped": ("mic", "FAIL"),
                    "wrong_label": ("label", "FAIL"), "no_answer": ("answer_point", "FAIL")}
        got = export.scenario_results()
        for name, (fault, result) in expected.items():
            self.assertEqual(got[name]["result"]["diagnosis"], fault, name)
            self.assertEqual(got[name]["result"]["result"], result, name)

    def test_fading_speaker_warned_before_failure_and_no_false_alarms(self):
        from prototype.prove import supervisor
        hist, ledger = supervisor.demo_history()
        first_warn = next(r["night"] for r in hist if r["result"] == "WARN")
        first_fail = next(r["night"] for r in hist if r["diagnosis"] == "speaker")
        self.assertGreaterEqual(first_fail - first_warn, 3)
        self.assertTrue(ledger.verify()[0])
        self.assertEqual(supervisor.false_alarm_rate(nights=200, seed=3), 0)


class TestAlarm(unittest.TestCase):
    def test_contact_id_checksum_and_clean_decode(self):
        from prototype.prove import alarm
        m = alarm.contact_id(event="110", zone="007")
        self.assertTrue(alarm.checksum_ok(m))
        self.assertFalse(alarm.checksum_ok(m[:-1] + ("1" if m[-1] != "1" else "2")))
        self.assertEqual(alarm.decode_dtmf(alarm.dtmf(m)), m)

    def test_kissoff_detector_is_specific(self):
        from prototype.prove import alarm
        rng = np.random.default_rng(0)
        self.assertTrue(alarm.detect_tone(alarm.kissoff(), 1400, 0.4))
        self.assertFalse(alarm.detect_tone(alarm.dtmf(alarm.contact_id()), 1400, 0.4))
        self.assertFalse(alarm.detect_tone(rng.normal(0, 0.1, 8000), 1400, 0.4))

    def test_registered_beats_voice_path_and_dead_receiver_never_kisses_off(self):
        from prototype.prove import alarm
        r = alarm.success_rates(trials=20, seed=2)
        self.assertEqual(r["registered (##21 done)"]["first_try_rate"], 1.0)
        self.assertLess(r["unregistered number (voice path)"]["first_try_rate"], 0.9)
        self.assertEqual(r["receiver down"]["delivered_rate"], 0.0)


class TestInstallProof(unittest.TestCase):
    def test_receipts(self):
        from prototype.prove import install
        r = install.scenarios()
        self.assertEqual(r["all_good"]["verdict"], "TRUCK NOT NEEDED")
        self.assertEqual(r["sia_panel"]["verdict"], "TRUCK NEEDED")
        self.assertEqual(r["unregistered"]["verdict"], "FIX BY TEXT, THEN RE-RUN")
        alarm_line = next(x for x in r["unregistered"]["lines"] if x["check"] == "ALARM")
        self.assertIn("##21", alarm_line["detail"])
        self.assertEqual(next(x for x in r["no_batteries"]["lines"] if x["check"] == "BATTERY")["status"], "FAIL")
        self.assertEqual(next(x for x in r["basement"]["lines"] if x["check"] == "SIGNAL")["status"], "FAIL")


class TestWhoAnswers(unittest.TestCase):
    def test_classifier_person_vs_machine_under_stress(self):
        from prototype.prove import answer
        d = answer.confusion(trials=8, stress=True, seed=4)
        self.assertGreaterEqual(d["person_vs_not"], 0.97)
        self.assertGreaterEqual(d["accuracy"], 0.85)

    def test_route_answer_time_and_label(self):
        from prototype.prove import answer
        reg = answer.Registry()
        ok = answer.check_call(reg.answerer_number, "person", 12, reg.label, reg)
        self.assertTrue(ok["pass"], ok)
        self.assertIn("previous contractor", " ".join(answer.check_call("8005550199", "person", 10, reg.label, reg)["issues"]))
        self.assertIn("voicemail", " ".join(answer.check_call(reg.answerer_number, "voicemail", 20, None, reg)["issues"]))
        self.assertIn("45 s", " ".join(answer.check_call(reg.answerer_number, "person", 52, reg.label, reg)["issues"]))
        self.assertIn("Nashville", " ".join(answer.check_call(reg.answerer_number, "person", 9, "Nashville, TN", reg)["issues"]))


class TestCapacity(unittest.TestCase):
    def test_prove_never_adds_hours_and_scales_with_pass_rate(self):
        from prototype.prove import capacity
        rows = capacity.sensitivity()
        for r in rows:
            self.assertLessEqual(r["months_with_prove"], r["months_today"])
        by = {(r["fw_share"], r["prove_pass"]): r for r in rows}
        self.assertLess(by[(0.3, 0.8)]["months_with_prove"], by[(0.3, 0.3)]["months_with_prove"])
        self.assertEqual(capacity.plan()["vs_installed_base_x"], 6.5)


if __name__ == "__main__":
    unittest.main()
