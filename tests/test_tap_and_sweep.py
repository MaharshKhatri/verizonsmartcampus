"""Pocket PROVE tap (one recorded alarm call -> ALARM receipt line) and the attenuation-sweep summary."""
import contextlib
import csv
import io
import os
import sys
import tempfile
import unittest
import wave

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from prototype.prove import alarm, tap  # noqa: E402
import analyze_prove_lab as apl  # noqa: E402
import make_demo_sweep_csv as mk  # noqa: E402


def call(seed, **kw):
    return tap.analyse_call(tap.synth_call(np.random.default_rng(seed), **kw))


class TestTapDetectors(unittest.TestCase):
    def test_vectorised_goertzel_and_decoder_match_alarm_py(self):
        rng = np.random.default_rng(0)
        fr = rng.normal(0, 1, 200)
        p = tap.goertzel_power(fr[None, :], [697, 1400, 2300])[0]
        for got, f in zip(p, (697, 1400, 2300)):
            self.assertAlmostEqual(got, alarm._goertzel(fr, f), delta=1e-9 * got)
        for i in range(12):
            sig = alarm.voice_path(alarm.dtmf(alarm.contact_id(zone=f"{i:03d}")), rng, loss=0.03 * i)
            self.assertEqual(tap.decode_dtmf_fast(sig), alarm.decode_dtmf(sig))


class TestTapCalls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clean = call(1)
        cls.lossy = call(2, loss=0.4)
        cls.down = call(3, receiver_up=False)
        cls.noko = call(4, kissoff_ok=False)

    def test_clean_call_is_ok_and_plausible(self):
        r = self.clean
        self.assertEqual(r["verdict"], "OK")
        self.assertTrue(r["picked_up"] and r["full_code_sent"] and r["confirmed"])
        self.assertEqual(r["attempts"], 1)
        self.assertEqual(r["blocks"][0]["digits"], alarm.contact_id())
        self.assertEqual(r["dialled_digits"], tap.DIAL)
        self.assertLess(r["handshake_at_s"], r["blocks"][0]["start_s"])
        self.assertTrue(2.0 < r["confirm_s"] < 3.5, r["confirm_s"])      # handshake + 1.76 s block + gaps
        self.assertEqual(r["receipt_line"], f"Receiver picked up · full code sent · confirmed in {r['confirm_s']:.1f} s")

    def test_heavy_loss_is_garbled_or_unconfirmed(self):
        r = self.lossy
        self.assertIn(r["verdict"], ("CODE GARBLED", "NO CONFIRMATION"))
        self.assertFalse(r["confirmed"])
        self.assertIsNone(r["confirm_s"])
        self.assertTrue(r["picked_up"])

    def test_receiver_down_is_no_answer(self):
        r = self.down
        self.assertEqual(r["verdict"], "NO ANSWER")
        self.assertFalse(r["picked_up"])
        self.assertEqual((r["blocks"], r["attempts"]), ([], 0))

    def test_no_kissoff_is_no_confirmation_after_four_attempts(self):
        r = self.noko
        self.assertEqual(r["verdict"], "NO CONFIRMATION")
        self.assertEqual(r["attempts"], 4)
        self.assertTrue(r["full_code_sent"])
        self.assertTrue(all(b["checksum_ok"] for b in r["blocks"]))

    def test_receipt_is_a_test_record_not_proof_of_delivery(self):
        for r in (self.clean, self.lossy, self.down, self.noko):
            self.assertNotIn("deliver", r["receipt_line"].lower())
            self.assertIn("·", r["receipt_line"])


class TestWav(unittest.TestCase):
    def test_round_trip_and_resampling_from_16k(self):
        x = tap.synth_call(np.random.default_rng(5))
        with tempfile.TemporaryDirectory() as d:
            p8, p16, pst = (os.path.join(d, f) for f in ("a8.wav", "a16.wav", "st.wav"))
            tap.write_wav(p8, x, alarm.FS)
            y = tap.read_wav(p8)
            self.assertEqual(len(y), len(x))
            self.assertLess(np.max(np.abs(y - x)), 1e-4)                       # PCM16 rounding only
            tap.write_wav(p16, tap.resample(x, alarm.FS, 16000), 16000)
            y16 = tap.read_wav(p16)
            self.assertEqual(len(y16), len(x))
            self.assertEqual(tap.analyse_call(y16)["verdict"], "OK")
            t = np.arange(16000) / 16000                                       # a 1 kHz tone recorded at 16 kHz
            tone16 = 0.5 * np.sin(2 * np.pi * 1000 * t)
            tap.write_wav(p16, tone16, 16000)
            got = tap.read_wav(p16)
            want = 0.5 * np.sin(2 * np.pi * 1000 * np.arange(8000) / 8000)
            self.assertLess(np.max(np.abs(got - want)[200:-200]), 0.01)
            st = np.round(np.stack([tone16, 0.5 * tone16], 1) * 32767).astype("<i2")   # stereo mixes to mono
            with wave.open(pst, "wb") as w:
                w.setnchannels(2)
                w.setsampwidth(2)
                w.setframerate(16000)
                w.writeframes(st.tobytes())
            self.assertLess(np.max(np.abs(tap.read_wav(pst) - 0.75 * want)[200:-200]), 0.01)


class TestBudget(unittest.TestCase):
    def test_budget_is_positive_and_labelled(self):
        b = tap.compute_budget()
        for k in ("mmac_per_s", "mops_per_s", "ram_kb_detectors", "ram_kb_with_call_audio", "mac_per_sample"):
            self.assertGreater(b[k], 0, k)
        self.assertEqual(b["tones"], 10)
        self.assertGreater(b["mops_per_s"], b["mmac_per_s"])
        self.assertLess(b["mmac_per_s"], 1.0)                 # a few tenths of a million MAC/s
        self.assertEqual(b["basis"], "analytic estimate, not measured on target hardware")


class TestSweep(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = mk.demo_rows(seed=4, attens=range(40, 62, 2), trials=10)
        cls.s = apl.sweep_summary(cls.rows)

    def test_clear_rule(self):
        self.assertTrue(apl.call_clear({"pesq": "3.0", "listener_keywords": "2"}))
        self.assertFalse(apl.call_clear({"pesq": "2.9", "listener_keywords": "10"}))   # PESQ wins when present
        self.assertTrue(apl.call_clear({"pesq": "", "listener_keywords": "9"}))
        self.assertFalse(apl.call_clear({"listener_keywords": "8"}))
        self.assertIsNone(apl.call_clear({}))

    def test_finds_gap_steps(self):
        self.assertEqual(self.s["reference_box"], "verizon_box")
        self.assertTrue(any(b["gap_atten_db"] for b in self.s["boxes"].values()))
        for b in self.s["boxes"].values():
            for st in b["steps"]:
                if st["gap"]:
                    self.assertGreaterEqual(st["call_clear"]["rate"], 0.9)
                    self.assertLess(st["alarm_confirmed"]["rate"], 0.9)
            if b["gap_sinr_db"]:
                self.assertLessEqual(b["gap_sinr_db"][0], b["gap_sinr_db"][1])

    def test_matched_sinr_comparison_runs(self):
        m = self.s["matched"]
        self.assertTrue(m)
        for x in m:
            self.assertEqual(x["sinr_hi"] - x["sinr_lo"], 2.0)
            self.assertIsInstance(x["same"], bool)
            self.assertTrue(-1 <= x["diff"] <= 1)
        md = "\n".join(apl.sweep_markdown(self.s))
        self.assertIn("did the same", md)
        self.assertIn("PESQ (ITU-T P.862 MOS-LQO) >= 3.0", md)

    def test_analyser_runs_on_synthetic_csv_and_old_csv(self):
        self.assertTrue(all("SYNTHETIC" in r["notes"] for r in self.rows))
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "demo_sweep_SYNTHETIC.csv")
            mk.write_csv(p, self.rows)
            with contextlib.redirect_stdout(io.StringIO()):
                md = "\n".join(apl.main(p))
            for s in ("SYNTHETIC DATA", "Attenuation sweep (voice clear vs alarm confirmed)", "Gap steps",
                      "Matched-SINR comparison", "Learned SIGNAL threshold"):
                self.assertIn(s, md)
            old = os.path.join(d, "old.csv")                  # an old CSV without the sweep columns
            with open(old, "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=["box", "device", "format", "placement", "delivered", "kissoff_s",
                                                   "attempts_used"])
                w.writeheader()
                w.writerows([{"box": "LAN", "device": "p", "format": "cid", "placement": "x", "delivered": 1,
                              "kissoff_s": 2.5, "attempts_used": 1}] * 3)
            with contextlib.redirect_stdout(io.StringIO()):
                md = "\n".join(apl.main(old))
            self.assertIn("3/3", md)
            self.assertNotIn("Attenuation sweep", md)


if __name__ == "__main__":
    unittest.main()
