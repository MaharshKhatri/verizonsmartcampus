"""Model v4: opt-in concealment and bursty loss, speech under the same path, 32-column receipts."""
import os
import re
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from prototype.prove import alarm, install  # noqa: E402
from prototype.prove.acoustic import FS, _band  # noqa: E402


def old_voice_path(sig, rng, snr_db=14.0, level_jitter_db=3.0, onset_clip=0.6, loss=0.02):
    """Verbatim copy of voice_path before v4 (independent loss, lost frames zeroed)."""
    y = _band(sig.copy())
    frame = int(0.02 * FS)
    p = np.mean(y * y) + 1e-12
    for i in range(0, len(y), frame):
        seg = y[i:i + frame]
        seg *= 10 ** (rng.normal(0, level_jitter_db) / 20)
        if rng.random() < loss:
            seg[:] = 0.0
    env = np.convolve(np.abs(y), np.ones(40) / 40, mode="same")        # 5 ms envelope
    active = env > 0.05
    onsets = np.flatnonzero(np.diff(active.astype(int)) == 1)
    for o in onsets:                                   # noise suppression clips tone onsets
        y[o:o + int(0.015 * FS)] *= (1 - onset_clip)
    y += rng.normal(0, np.sqrt(p / 10 ** (snr_db / 10)), len(y))
    return y


def first_try(n, seed, **kw):
    rng = np.random.default_rng(seed)
    calls = [alarm.alarm_call(rng, registered=False, voice_kw=kw, fast=True) for _ in range(n)]
    return sum(c["delivered"] and c["attempts"] == 1 for c in calls) / n


class TestDefaultsUnchanged(unittest.TestCase):
    def test_voice_path_defaults_byte_identical(self):
        sigs = (alarm.dtmf(alarm.contact_id()), alarm.handshake(), alarm.kissoff())
        for seed in range(4):
            for kw in ({}, {"loss": 0.3}, {"snr_db": 20.0, "level_jitter_db": 1.0, "onset_clip": 0.3, "loss": 0.05}):
                for s in sigs:
                    a = alarm.voice_path(s, np.random.default_rng(seed), **kw)
                    b = old_voice_path(s, np.random.default_rng(seed), **kw)
                    self.assertEqual(a.tobytes(), b.tobytes(), (seed, kw))

    def test_alarm_call_default_unchanged_and_fast_detectors_agree(self):
        old = alarm.voice_path
        try:
            alarm.voice_path = old_voice_path
            ref = [alarm.alarm_call(np.random.default_rng(s), registered=False) for s in range(3)]
        finally:
            alarm.voice_path = old
        self.assertEqual([alarm.alarm_call(np.random.default_rng(s), registered=False) for s in range(3)], ref)
        rng = np.random.default_rng(1)
        for k in range(12):
            kw = {"loss": 0.05 * (k % 3), "plc": bool(k % 2), "burst": (0.03, 0.2) if k % 4 == 0 else None}
            for s, f, ms in ((alarm.handshake(), 2300, 0.06), (alarm.kissoff(), 1400, 0.4)):
                y = alarm.voice_path(s, rng, **kw)
                self.assertEqual(alarm.detect_tone(y, f, ms), alarm.detect_tone_fast(y, f, ms))
            y = alarm.voice_path(alarm.dtmf(alarm.contact_id()), rng, **kw)
            self.assertEqual(alarm.decode_dtmf(y), alarm.decode_dtmf_fast(y))

    def test_plc_without_loss_is_the_default_path(self):
        s = alarm.dtmf(alarm.contact_id())
        a = alarm.voice_path(s, np.random.default_rng(5), loss=0.0, plc=True)
        self.assertEqual(a.tobytes(), alarm.voice_path(s, np.random.default_rng(5), loss=0.0).tobytes())


class TestConcealmentAndBursts(unittest.TestCase):
    def test_plc_raises_first_try_success_at_one_percent_loss(self):
        zeroed, pitch = first_try(150, 11, loss=0.01), first_try(150, 11, loss=0.01, plc=True)
        self.assertGreaterEqual(pitch - zeroed, 0.1, (zeroed, pitch))
        self.assertGreaterEqual(pitch, 0.9)
        self.assertGreater(first_try(150, 11, loss=0.01, plc="frame"), zeroed)

    def test_gilbert_elliott_mean_loss_matches_theory(self):
        rng = np.random.default_rng(0)
        for p_gb, p_bg, good, bad in ((0.02, 0.2, 0.01, 0.5), (0.05, 0.1, 0.0, 0.8)):
            lost = alarm.gilbert_elliott(200_000, rng, p_gb, p_bg, loss=good, bad_loss=bad)
            theory = alarm.ge_mean_loss(p_gb, p_bg, good, bad)
            self.assertAlmostEqual(lost.mean(), theory, delta=0.08 * theory)
        self.assertAlmostEqual(alarm.ge_mean_loss(0.02, 0.2, 0.01, 0.5), (0.2 * 0.01 + 0.02 * 0.5) / 0.22)

    def test_concealment_stretches_a_digit_into_its_gap_and_decoder_is_untouched(self):
        msg = alarm.contact_id_variant(repeated=True)        # 1111...: digits 2 and 3 are both '1'
        sig = alarm.dtmf(msg)
        mask = np.zeros(int(np.ceil(len(sig) / 160)), bool)
        mask[[8, 9, 10]] = True                              # 160-220 ms: the 2nd digit's tail up to the 3rd
        gap = slice(1330, 1750)                              # the silence between the 2nd and 3rd digits
        rms = {}
        for plc in (False, True):
            y = alarm.voice_path(sig, np.random.default_rng(0), lost=mask, plc=plc)
            rms[plc] = np.sqrt(np.mean(y[gap] ** 2))
            # what the unchanged decoder makes of it: the phase jump where the stretched tone meets
            # the next '1' keeps the two digits apart in this model (documented, not tuned)
            self.assertEqual(alarm.decode_dtmf(y), msg)
        self.assertGreater(rms[True], 2 * rms[False])

    def test_no_repeat_account_has_no_adjacent_repeats(self):
        m, r = alarm.contact_id_variant(repeated=False), alarm.contact_id_variant(repeated=True)
        self.assertEqual(len(m), 16)
        self.assertTrue(alarm.checksum_ok(m) and alarm.checksum_ok(r))
        self.assertTrue(all(a != b for a, b in zip(m, m[1:])), m)          # checksum key included
        self.assertTrue(m.startswith(alarm.NO_REPEAT_ACCOUNT) and r.startswith("1111"))
        self.assertTrue(alarm.has_adjacent_repeat(r))
        self.assertTrue(alarm.has_adjacent_repeat(alarm.contact_id()))     # the default message repeats '1' and '0'


class TestSpeechProxy(unittest.TestCase):
    @staticmethod
    def scores(n, **kw):
        rng = np.random.default_rng(7)
        out = []
        for _ in range(n):
            s = alarm.speech_like(rng)
            out.append(alarm.speech_quality_proxy(s, alarm.voice_path(s, rng, **kw)))
        return np.array(out)

    def test_speech_like_is_voiced_bursts_with_pauses(self):
        s = alarm.speech_like(np.random.default_rng(1))
        self.assertEqual(len(s), 3 * FS)
        self.assertAlmostEqual(np.sqrt(np.mean(s * s)), 0.1, places=6)
        frames = np.sqrt(np.mean(s[:len(s) // 160 * 160].reshape(-1, 160) ** 2, 1))
        self.assertGreater(np.mean(frames < 0.01), 0.1)                     # pauses
        self.assertGreater(np.mean(frames > 0.05), 0.3)                     # voiced stretches

    def test_clean_path_near_4_3_and_heavy_loss_under_2(self):
        s = alarm.speech_like(np.random.default_rng(2))
        self.assertGreater(alarm.speech_quality_proxy(s, s), 4.45)
        clean, heavy = self.scores(25, loss=0.0), self.scores(25, loss=0.3)
        self.assertTrue(4.1 < np.median(clean) < 4.45, np.median(clean))
        self.assertLess(np.median(heavy), 2.0)
        self.assertGreater(np.median(self.scores(25, loss=0.3, plc=True)), np.median(heavy))


class TestVoiceVsAlarmCurve(unittest.TestCase):
    def test_curves_and_l90s(self):
        r = alarm.voice_vs_alarm_curve(losses=(0, 0.01, 0.03, 0.06, 0.12), trials=30, plc=False, burst=None)
        self.assertIn("model", r["label"])
        for key in ("voice_clear", "alarm_first_try", "alarm_within_4"):
            ys = [row[key] for row in r["rows"]]
            self.assertGreater(ys[0], ys[-1], key)
            self.assertTrue(all(b <= a + 0.15 for a, b in zip(ys, ys[1:])), (key, ys))    # monotone-ish
        for key in ("voice_clear", "alarm_first_try"):
            self.assertIsNotNone(r["l90"][key], key)
            self.assertTrue(0 <= r["l90"][key] <= 0.12)
        self.assertEqual(r["fails_first"]["first_try_vs_voice"], "alarm")
        for v in r["fails_first"].values():
            self.assertIn(v, ("alarm", "voice", "together", "neither drops below 90% in this range"))
        b = alarm.voice_vs_alarm_curve(losses=(0, 0.05), trials=10, plc=True, burst=0.2)
        self.assertTrue(b["plc"] and "Gilbert-Elliott" in b["loss"])

    def test_l90_helpers(self):
        self.assertEqual(alarm._l90([0, 0.1, 0.2], [1.0, 0.95, 0.85]), 0.15)
        self.assertEqual(alarm._l90([0, 0.1], [0.8, 0.7]), 0.0)
        self.assertIsNone(alarm._l90([0, 0.1], [1.0, 0.95]))
        self.assertEqual(alarm._nonincreasing([1.0, 0.9, 0.95, 0.5]), [1.0, 0.925, 0.925, 0.5])
        self.assertEqual(alarm._first(0.02, 0.025), "together")
        self.assertEqual(alarm._first(0.01, None), "alarm")


class TestReceipts(unittest.TestCase):
    def test_32_column_receipts(self):
        texts = {}
        for i, (name, setup) in enumerate(install.SCENARIOS.items()):
            for events in (1, 3):
                for src in (False, True):
                    res = install.install_proof(setup, seed=i, alarm_events=events, sources=src)
                    t = install.receipt_text(res, width=32)
                    texts[name, events, src] = t
                    self.assertLessEqual(max(len(ln) for ln in t.splitlines()), 32, t)
                    self.assertIn("Test record, not a guarantee.", t.splitlines())
                    self.assertIn(res["verdict"], " ".join(" ".join(t.splitlines()).split()))
                    self.assertNotIn("delivered", t.lower())
        green = texts["all_good", 1, True]
        self.assertIn("GREEN: all checks passed ·\n       no visit requested", green)
        for label in ("SIGNAL (box reading)", "ALARM (line tap)"):
            self.assertIn(label, green)
        self.assertIn("VOICE (call to PROVE test\n     responder)", green)
        self.assertRegex(green, r"confirmed in \d+\.\d s")
        self.assertIn("confirmed 3/3", texts["all_good", 3, False])
        proxy = install.install_proof(install.HomeSetup(signal_source="phone"), sources=True)
        self.assertEqual(proxy["lines"][0]["source"], "SIGNAL (phone near box, proxy)")

    def test_alarm_line_wording_and_defaults(self):
        one = install.install_proof(install.HomeSetup(), alarm_events=1)
        line = next(x for x in one["lines"] if x["check"] == "ALARM")
        self.assertTrue(re.fullmatch(r"Receiver picked up · full code sent · confirmed in \d+\.\d s", line["detail"]))
        res = install.install_proof(install.HomeSetup())
        self.assertEqual(next(x for x in res["lines"] if x["check"] == "ALARM")["detail"],
                         "Receiver picked up · full code sent · confirmed 3/3")
        self.assertEqual(res["verdict"], "GREEN: all checks passed · no visit requested")
        self.assertTrue(all("source" not in x for x in res["lines"]))
        self.assertEqual(install.receipt_text(res).splitlines()[:2], ["PROVE · test record", "-" * 34])


class TestRetryWarning(unittest.TestCase):
    """An alarm that gets through only after the panel retried leaves little margin: WARN, not GREEN."""

    def test_confirmed_after_retries_is_warn_with_fix(self):
        from unittest import mock
        import numpy as np
        from prototype.prove import install
        calls = iter([{"delivered": True, "attempts": 2}, {"delivered": True, "attempts": 1},
                      {"delivered": True, "attempts": 3}])
        with mock.patch.object(install, "_alarm_call_with_loss", lambda rng, loss, **kw: next(calls)):
            st, msg, fix, truck = install._alarm_check(install.HomeSetup(), 0.0, np.random.default_rng(0))
        self.assertEqual(st, "WARN")
        self.assertIn("only after retries (first try 1/3)", msg)
        self.assertIn("window", fix)
        self.assertNotIn("delivered", msg.lower())
        self.assertFalse(truck)


if __name__ == "__main__":
    unittest.main()
