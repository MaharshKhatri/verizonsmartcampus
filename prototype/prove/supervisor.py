"""PROVE supervisor: one box per elevator car, one test per night.

Runs the checks in order: heartbeat, call setup, downlink chirp, uplink
chirp, location label, answer. It turns the raw results into symptoms, asks
triage for a cause and an owner, writes everything to the evidence ledger,
and watches each car's nightly margins for a slow fade before a hard failure.

In the demo the "hardware" is acoustic.CarState plus a few flags that the
rig buttons flip (pull copper, unplug antenna, tape mic, kill mains). On the
real rig the same interface is fed by the Pi's audio interface and the
gateway's status; nothing above this layer changes.
"""
from dataclasses import dataclass, field, asdict

import numpy as np

from . import acoustic, triage
from .ledger import EvidenceLedger

WARN_DROP_DB = 10.0       # warn when a direction is this far below the car's own baseline
EARLY_DROP_DB = 6.0       # ...or this far below it while still falling, two nights running
EARLY_SLOPE_DB = -0.5     # dB per night over the last week
BASELINE_NIGHTS = 30      # baseline = median of the last 30 clean (PASS) nights


@dataclass
class Rig:
    """Everything the supervisor can observe about one car's emergency path."""
    car_id: str = "demo-car-1"
    label: str = "Hill Center, Car 2 (demo label)"          # provisioned at install
    reported_label: str = None                                # what the answering console receives
    on_copper: bool = False                                   # the demo starts after migration
    antenna: bool = True
    mains: bool = True
    battery_hours: float = 24.0
    gateway_ok: bool = True
    answer_point_ok: bool = True
    car: acoustic.CarState = field(default_factory=acoustic.CarState)

    def rsrp_dbm(self):
        return -98.0 if self.antenna else -128.0


def symptoms_for(rig, down, up):
    s = set()
    if not rig.gateway_ok or (not rig.mains and rig.battery_hours <= 0):
        s.add("heartbeat_lost")
    if rig.rsrp_dbm() < -120:
        s |= {"rsrp_low", "attach_fail"}
    if not rig.mains:
        s.add("mains_lost")
        if rig.battery_hours < 4:
            s.add("battery_low")
    if not rig.car.call_connects:
        s.add("call_setup_fail")
    if not down.passed:
        s.add("down_fail")
    if not up.passed:
        s.add("up_fail")
        if up.band_db and up.band_db[0] - up.band_db[-1] > 10:
            s.add("up_hf_loss")
    if rig.car.call_connects and not rig.answer_point_ok:
        s.add("no_answer")
    if (rig.reported_label or rig.label) != rig.label:
        s.add("label_mismatch")
    if rig.on_copper:
        s.add("still_on_copper")          # known from the line inventory, not from the test
    return s


NON_BLOCKING = {"mains_lost", "battery_low"}    # path still works on battery: warn and ticket, don't fail


class Supervisor:
    def __init__(self, rig=None, ledger=None, seed=1):
        self.rig = rig or Rig()
        self.ledger = ledger or EvidenceLedger()
        self.rng = np.random.default_rng(seed)
        self.history = []          # clean nights only: (night, down_db, up_db)
        self.recent = []           # every night that completed a call: (night, down_db, up_db)
        self.night = 0

    def _sync(self):
        """Map rig flags onto the voice path: no RF, no gateway or no power means no call."""
        r = self.rig
        powered = r.mains or r.battery_hours > 0
        r.car.call_connects = bool(r.antenna and r.gateway_ok and powered and not r.on_copper_cut())
        return r

    def run_test(self, night=None):
        night = self.night if night is None else night
        rig = self._sync()
        down, up = acoustic.two_direction_test(rig.car, self.rng)
        syms = symptoms_for(rig, down, up)
        if down.passed and up.passed:
            self.recent.append((night, down.margin_db, up.margin_db))
        warn = self._trend_warning(down.margin_db, up.margin_db) if down.passed and up.passed else None
        result = "PASS" if not syms else ("WARN" if syms <= NON_BLOCKING and down.passed and up.passed else "FAIL")
        if result == "PASS" and warn:
            result = "WARN"
        diag = triage.diagnose(syms) if syms else None
        rec = {"car": rig.car_id, "night": night, "result": result,
               "down_db": round(down.margin_db, 1), "up_db": round(up.margin_db, 1),
               "label": rig.reported_label or rig.label, "rsrp_dbm": rig.rsrp_dbm(),
               "symptoms": sorted(syms), "warning": warn,
               "diagnosis": diag["fault"] if diag else None, "owner": diag["owner"] if diag else None,
               "confidence": diag["confidence"] if diag else None,
               "ticket": f"T-{rig.car_id}-{night}" if diag else ""}
        entry = self.ledger.append(rec)
        if result == "PASS":
            self.history.append((night, down.margin_db, up.margin_db))
        self.night = night + 1
        return dict(rec, hash=entry["hash"], band_down=[round(b, 1) for b in down.band_db],
                    band_up=[round(b, 1) for b in up.band_db])

    def _trend_warning(self, down_db, up_db):
        clean = self.history[-BASELINE_NIGHTS:]
        if len(clean) < 5:
            return None
        week = self.recent[-7:]
        for i, (name, now, hint) in enumerate((("downlink", down_db, "speaker fading?"),
                                               ("uplink", up_db, "mic fading or obstructed?")), start=1):
            base = float(np.median([h[i] for h in clean]))
            drop = base - now
            slope = float(np.polyfit([w[0] for w in week], [w[i] for w in week], 1)[0]) if len(week) >= 5 else 0.0
            prev_drop = base - self.recent[-2][i] if len(self.recent) >= 2 else 0.0
            if drop > WARN_DROP_DB or (drop > EARLY_DROP_DB and prev_drop > EARLY_DROP_DB / 2
                                       and slope < EARLY_SLOPE_DB):
                return f"{name} {drop:.0f} dB below this car's baseline, {slope:+.1f} dB/night: {hint}"
        return None

    def help_pressed(self):
        """HELP sends the label as data before the voice call, so the answerer knows where without asking."""
        rig = self._sync()
        return {"car": rig.car_id, "label_sent": rig.reported_label or rig.label,
                "voice_call": rig.car.call_connects,
                "text_mode": {"to_car": "Help is coming. Are you hurt? Tap YES or NO.",
                              "choices": ["YES", "NO"]},
                "fallback": None if rig.car.call_connects else "No voice path: alert sent to RUPD by data path if available"}

    def state(self):
        d = asdict(self.rig)
        d["rsrp_dbm"] = self.rig.rsrp_dbm()
        return d


def _cut(rig):
    return False


Rig.on_copper_cut = lambda self: bool(self.on_copper)   # a line still on copper goes dead at the cut


def false_alarm_rate(nights=365, seed=9):
    """Warnings per healthy car-year (nothing is wrong, so every warning is false)."""
    sup = Supervisor(seed=seed)
    return sum(sup.run_test(n)["result"] != "PASS" for n in range(nights))


def demo_history(nights=60, seed=4):
    """One car over 60 nights: healthy, a slowly fading speaker that PROVE warns on
    before it fails, a repair, then an antenna fault routed to Verizon."""
    sup = Supervisor(seed=seed)
    out = []
    for n in range(nights):
        car = sup.rig.car
        if 20 <= n < 38:
            car.speaker_gain = max(0.0, 1.0 - (n - 19) * 0.06)     # fades ~0.06 per night
        elif n == 38:
            car.speaker_gain = 1.0                                 # contractor replaced the speaker
        sup.rig.antenna = not (50 <= n < 52)
        out.append(sup.run_test(n))
    return out, sup.ledger
