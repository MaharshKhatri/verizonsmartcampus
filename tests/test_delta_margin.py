"""T5 headline: delta, the dB margin above each box's own dropout; setup failures kept out; the signal bar's filter."""
import contextlib
import csv
import io
import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from prototype.prove import signal_model  # noqa: E402
import analyze_prove_lab as apl  # noqa: E402
import make_demo_sweep_csv as mk  # noqa: E402

LINE = re.compile(r"^- (\w+): alarm data needed (\d+\.\d) dB (more|less) signal than a clear call \(95% CI (-?\d+\.\d) "
                  r"to (-?\d+\.\d); n = (\d+) voice \+ (\d+) alarm answered trials\)\. Gap: (yes|no)\.$", re.M)


def run_main(path):
    with contextlib.redirect_stdout(io.StringIO()):
        return "\n".join(apl.main(path))


def box_rows(rows, box):
    return [r for r in rows if r["box"] == box]


class TestDeltaRecovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = mk.demo_rows()                                    # injected: verizon 3.0 dB, other 2.0 dB
        cls.s = apl.sweep_summary(cls.rows)
        cls.md = "\n".join(apl.sweep_markdown(cls.s))

    def test_injected_deltas_inside_ci_and_edges_found(self):
        for box, p in mk.BOXES.items():
            m = self.s["boxes"][box]["margin"]
            lo, hi = m["delta_ci"]
            self.assertTrue(lo <= p["delta"] <= hi, (box, m["delta"], lo, hi))
            self.assertTrue(m["gap"], box)
            self.assertEqual((m["a_edge"], m["edge_found"]), (p["edge"], True))
            self.assertLess(m["a90_alarm"], m["a90_voice"])
            self.assertTrue(all(st["a_rel_db"] <= 0 for st in self.s["boxes"][box]["steps"] if st["answered"]["k"]))
        self.assertTrue(self.s["cross"]["same_pattern"])

    def test_headline_lines(self):
        got = {m[0]: m for m in LINE.findall(self.md)}
        self.assertEqual(set(got), set(mk.BOXES))
        for box, m in got.items():
            self.assertEqual((m[2], m[7]), ("more", "yes"))
            self.assertLessEqual(float(m[3]), float(m[1]))
            self.assertGreater(int(m[5]) + int(m[6]), 400)
        for s in ("Same pattern", "NOT evidence", "Sensitivity, PESQ threshold 3.5", "call setup and drops",
                  "Matched-SINR comparison (secondary", apl.SINR_NOTE, "Fail stages"):
            self.assertIn(s, self.md)

    def test_no_injected_delta_gives_no_gap(self):
        s = apl.sweep_summary(mk.demo_rows(deltas={b: 0.0 for b in mk.BOXES}))
        for box in mk.BOXES:
            m = s["boxes"][box]["margin"]
            self.assertTrue(m["delta_ci"][0] <= 0 <= m["delta_ci"][1], (box, m["delta"], m["delta_ci"]))
            self.assertIs(m["gap"], False)
        md = "\n".join(apl.margin_markdown(s))
        self.assertEqual(sorted((m[0], m[7]) for m in LINE.findall(md)), sorted((b, "no") for b in mk.BOXES))
        self.assertFalse(s["cross"]["same_pattern"])
        self.assertIn("No box shows a gap", md)


class TestSetupFailuresExcluded(unittest.TestCase):
    def test_setup_failures_and_drops_never_count_as_voice_or_alarm_failures(self):
        rows = box_rows(mk.demo_rows(), "verizon_box")
        base = apl.margin(rows, boot=60)
        extra = []
        for r in rows:                                               # a failed setup or a drop next to every trial
            if r["fail_stage"] == "" and 44 <= r["atten_db"] <= 55:
                extra.append(dict(r, test_id=r["test_id"] + "s", setup_ok=0, fail_stage="setup", delivered=0,
                                  pesq_up="", pesq_down="", listener_keywords=""))
                extra.append(dict(r, test_id=r["test_id"] + "d", setup_ok=1, fail_stage="drop", delivered=0,
                                  pesq_up="1.0", pesq_down="1.0", listener_keywords=0))
        more = apl.margin(rows + extra, boot=60)
        for k in ("a_edge", "n_voice", "n_alarm", "delta", "delta_ci", "a90_voice", "a90_alarm"):
            self.assertEqual(more[k], base[k], k)
        self.assertEqual(more["n_trials"], base["n_trials"] + len(extra))
        self.assertLess(more["a90_setup"], base["a90_setup"] - 1)     # the setup curve does see them
        st = {x["atten_db"]: x for x in apl.sweep_summary(rows + extra, boot=20)["boxes"]["verizon_box"]["steps"]}
        st0 = {x["atten_db"]: x for x in apl.sweep_summary(rows, boot=20)["boxes"]["verizon_box"]["steps"]}
        self.assertEqual(st[50]["alarm_confirmed"], st0[50]["alarm_confirmed"])
        self.assertEqual(st[50]["call_clear"], st0[50]["call_clear"])
        self.assertGreater(st[50]["fail_stages"]["setup"], st0[50]["fail_stages"].get("setup", 0))

    def test_setup_columns(self):
        f = signal_model.setup_failed
        self.assertTrue(f({"setup_ok": "0", "fail_stage": ""}))
        self.assertFalse(f({"setup_ok": "1", "fail_stage": "drop"}))           # setup_ok wins when logged
        self.assertTrue(f({"fail_stage": "drop"}) and f({"setup_ok": "", "fail_stage": "setup"}))
        self.assertFalse(f({"fail_stage": "no_kissoff"}) or f({}))
        self.assertFalse(signal_model.answered({"setup_ok": "1", "fail_stage": "drop"}))
        rs = [{"atten_db": a, "fail_stage": "setup" if a >= 50 else ""} for a in (40, 50, 50, 55)]
        self.assertEqual(apl.a_edge(rs), (50.0, True))
        self.assertEqual(apl.a_edge([{"atten_db": a} for a in (40, 46)]), (46.0, False))

    def test_clear_rule_both_directions(self):
        c = apl.call_clear
        self.assertTrue(c({"pesq_up": "3.1", "pesq_down": "3.0", "listener_keywords": "9"}))
        self.assertFalse(c({"pesq_up": "3.1", "pesq_down": "2.9", "listener_keywords": "10"}))
        self.assertFalse(c({"pesq_up": "3.4", "pesq_down": "3.6", "listener_keywords": "8"}))
        self.assertTrue(c({"pesq_up": "3.4", "pesq_down": "3.6", "listener_keywords": ""}))
        self.assertFalse(c({"pesq_up": "3.4", "pesq_down": "3.6"}, 3.5))
        self.assertFalse(c({"pesq_up": "2.0", "pesq_down": ""}))
        self.assertIsNone(c({"pesq_up": "3.9", "pesq_down": ""}))                  # one direction: not rated


class TestSignalBarFilter(unittest.TestCase):
    def test_bar_unchanged_by_voice_sia_and_unregistered_rows(self):
        rows = mk.demo_rows()
        noise = []
        for i, r in enumerate(x for x in rows if x["box"] == "verizon_box" and x["call_trial"] == 0):
            noise.append(dict(r, call_trial=1, delivered=1 - int(r["delivered"] or 0)))           # voice rows
            noise.append(dict(r, format="SIA", delivered=0, attempts_used=4))                  # other format
            noise.append(dict(r, registered_21=0, delivered=0, attempts_used=4, atten_db=r["atten_db"] + 0.5))
        mixed = [x for pair in zip(rows, noise) for x in pair] + rows[len(noise):]
        with tempfile.TemporaryDirectory() as d:
            a, b = os.path.join(d, "a.csv"), os.path.join(d, "b.csv")
            mk.write_csv(a, rows)
            mk.write_csv(b, mixed)
            ra, rb = signal_model.load_rows(a, "verizon_box"), signal_model.load_rows(b, "verizon_box")
            self.assertEqual(ra, rb)
            self.assertEqual(len(ra), sum(r["box"] == "verizon_box" and r["call_trial"] == 0 and r["setup_ok"] == 1
                                          and r["fail_stage"] != "drop" for r in rows))
            for kw in ({}, {"ceiling": True}):
                self.assertEqual(signal_model.fit(ra, boot=40, **kw), signal_model.fit(rb, boot=40, **kw))
            line = [x for x in run_main(a).splitlines() if "bench alarm tests (box verizon_box" in x]
            self.assertEqual(line, [x for x in run_main(b).splitlines() if "bench alarm tests (box verizon_box" in x])
            self.assertIn(f"- n = {len(ra)} bench alarm tests (box verizon_box, one cell). SINR for 90%", line[0])

    def test_ceiling_fit(self):
        rows = signal_model.filter_rows(mk.demo_rows(), "verizon_box")
        r = signal_model.fit(rows, boot=40, ceiling=True)
        self.assertTrue(0.8 < r["ceiling"] < 1.0)
        self.assertAlmostEqual(r["target_p"], 0.9 * r["ceiling"], places=2)
        self.assertGreater(r["coef"][1], 0)
        self.assertTrue(r["bootstrap"].startswith("cluster date+atten_db"))
        ps = [c["p_first_try"] for c in r["curve"]]
        self.assertEqual(ps, sorted(ps))
        self.assertLessEqual(max(ps), r["ceiling"])


class TestOldCsv(unittest.TestCase):
    def test_legacy_sweep_csv_without_new_columns(self):
        old_cols = ["test_id", "date", "box", "firmware", "placement", "rsrp_dbm", "rsrq_db", "sinr_db", "device",
                    "format", "registered_21", "attempt", "delivered", "kissoff_s", "attempts_used", "notes",
                    "atten_db", "pesq", "listener_keywords", "call_trial"]
        old = []
        for r in mk.demo_rows():
            v = r["call_trial"] == 1                                 # old CSVs logged a failed call as unclear
            pesq = min(float(r["pesq_up"]), float(r["pesq_down"])) if r["pesq_up"] else (1.0 if v else "")
            old.append(dict(r, date="SYNTHETIC", rsrq_db=-10, device="panel", placement="bench", registered_21="",
                            format="voice" if v else "contact_id", pesq=pesq,
                            listener_keywords=r["listener_keywords"] if r["pesq_up"] else (0 if v else "")))
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "old_sweep.csv")
            mk.write_csv(p, old, old_cols)
            md = run_main(p)
        for s in ("SYNTHETIC DATA", "Attenuation sweep (voice clear vs alarm confirmed)", "Gap steps",
                  "Matched-SINR comparison", "Learned SIGNAL threshold", "Headline: delta"):
            self.assertIn(s, md)
        self.assertIn("(no step lost service on every trial; largest step tested)", md)
        self.assertIn("n = 0 bench alarm tests", md)                # registered_21 blank: not counted as registered
        self.assertNotIn("call setup and drops", md)
        self.assertNotIn("Fail stages", md)

    def test_alarm_only_csv_with_signal_but_no_sweep(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t1.csv")
            with open(p, "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=["box", "device", "format", "placement", "delivered", "kissoff_s",
                                                   "attempts_used", "sinr_db"])
                w.writeheader()
                w.writerows([{"box": "verizon_box", "device": "p", "format": "CID", "placement": "x",
                              "delivered": int(i % 4 > 0), "kissoff_s": 2.5, "attempts_used": 1, "sinr_db": i % 12 - 2}
                             for i in range(40)])
            md = run_main(p)
        self.assertIn("30/40", md)
        self.assertIn("n = 40 bench alarm tests (box verizon_box, cell not logged)", md)
        self.assertNotIn("Attenuation sweep", md)


if __name__ == "__main__":
    unittest.main()
