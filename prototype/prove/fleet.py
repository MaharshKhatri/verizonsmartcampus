"""A year of emergency-phone failures across a fleet of elevator cars.

Compares how long a broken path stays broken under three regimes:

  annual       today at many buildings: found at the yearly inspection, or by
               the rider who presses HELP and gets nothing
  line_monitor a modern phone or gateway that reports line loss (it catches
               RF, power and gateway faults, but not a dead speaker or mic,
               a wrong location label or an unanswered call)
  prove        nightly two-direction acoustic test, label check, answer check

All failure rates, repair times and the entrapment rate are ASSUMPTIONS (see
RATES); the pilot replaces them. The fleet is synthetic. Results are reported
with a sensitivity sweep so no single guess carries the story.
"""
import random
from dataclasses import dataclass

from . import triage
from .ledger import EvidenceLedger

# fault: (failures per car per year, repair days once detected, caught by line monitoring?)
RATES = {
    "rf":           (0.10, 1.0, True),
    "power":        (0.05, 1.0, True),
    "gateway":      (0.05, 2.0, True),
    "speaker":      (0.04, 5.0, False),
    "mic":          (0.06, 5.0, False),
    "answer_point": (0.03, 1.0, False),
}
LABEL_ERROR_AT_MIGRATION = 0.03   # share of migrated lines whose location label is wrong (assumption)
ENTRAPMENTS_PER_CAR_YEAR = 0.5    # rider presses HELP for real (assumption)
DEGRADE_SHARE = 0.4               # speaker/mic failures that fade over weeks rather than fail suddenly
DEGRADE_DAYS = 30

REGIMES = ("annual", "line_monitor", "prove")


@dataclass
class Failure:
    car: int
    fault: str
    start: float
    detected: float = None
    fixed: float = None
    warned: float = None


def _detect_day(fault, start, inspect_day, entrapments, regime, rng, degrading):
    """Day the owner learns the path is broken (or None if not within the horizon)."""
    if regime == "prove":
        if degrading and fault in ("speaker", "mic"):
            return start, start - DEGRADE_DAYS * 0.5      # warned mid-fade, before it fails outright
        return start + rng.uniform(0, 1), None             # next nightly test
    if regime == "line_monitor" and RATES.get(fault, (0, 0, False))[2]:
        return start + rng.uniform(0, 1), None
    # found at the next annual inspection or the next real entrapment, whichever comes first
    nxt_inspect = inspect_day if inspect_day >= start else inspect_day + 365
    nxt_trap = next((t for t in entrapments if t >= start), float("inf"))
    return min(nxt_inspect, nxt_trap), None


def simulate(cars=120, years=1, seed=7, regime="prove", rates=None, migrate=True, ledger=None):
    rng = random.Random(seed)
    rates = rates or RATES
    horizon = 365 * years
    out = []
    broken_days = 0.0
    trapped_dead = 0
    for car in range(cars):
        inspect_day = rng.uniform(0, 365)
        traps, t = [], 0.0
        while True:
            t += rng.expovariate(ENTRAPMENTS_PER_CAR_YEAR / 365)
            if t > horizon + 365:
                break
            traps.append(t)
        fails = []
        for fault, (rate, repair, _) in rates.items():
            if rate <= 0:
                continue
            t = 0.0
            while True:
                t += rng.expovariate(rate / 365)
                if t > horizon:
                    break
                fails.append((fault, t, repair))
        if migrate and rng.random() < LABEL_ERROR_AT_MIGRATION:
            fails.append(("label", 0.0, 1.0))
        for fault, start, repair in sorted(fails, key=lambda f: f[1]):
            degrading = fault in ("speaker", "mic") and rng.random() < DEGRADE_SHARE
            if fault == "label":
                # a wrong label only shows when someone calls; PROVE checks it every night
                det = start + 1 if regime == "prove" else next((x for x in traps if x >= start), horizon + 365)
                warned = None
            else:
                det, warned = _detect_day(fault, start, inspect_day, traps, regime, rng, degrading)
            fixed = det + repair
            f = Failure(car, fault, start, det, fixed, warned)
            out.append(f)
            end = min(fixed, horizon)
            if fault != "label":
                broken_days += max(0.0, end - start)
                trapped_dead += sum(1 for x in traps if start <= x < end)
            if ledger is not None and regime == "prove" and det <= horizon:
                d = triage.diagnose(triage.sample_symptoms(fault, rng))
                ledger.append({"car": f"car-{car:03d}", "night": int(det), "result": "FAIL", "fault": fault,
                               "diagnosis": d["fault"], "owner": d["owner"], "ticket": f"T{len(ledger.entries):05d}"})
    return {"regime": regime, "cars": cars, "failures": len(out),
            "broken_car_days": round(broken_days, 1),
            "mean_days_broken": round(broken_days / max(1, sum(1 for f in out if f.fault != "label")), 1),
            "entrapments_meeting_dead_phone": trapped_dead,
            "label_errors": sum(1 for f in out if f.fault == "label"),
            "warned_before_failure": sum(1 for f in out if f.warned is not None)}


def compare(cars=120, seeds=range(20)):
    rows = {}
    for regime in REGIMES:
        rs = [simulate(cars=cars, seed=s, regime=regime) for s in seeds]
        rows[regime] = {k: round(sum(r[k] for r in rs) / len(rs), 1)
                        for k in ("failures", "broken_car_days", "mean_days_broken", "entrapments_meeting_dead_phone",
                                  "warned_before_failure")}
    return rows


def sensitivity(cars=120, seeds=range(10)):
    """PROVE's edge over a line monitor comes only from failures a line monitor
    cannot see (speaker, mic, unanswered calls). Scale those rates from 0.1x to
    3x, keeping RF/power/gateway fixed, and report how the edge moves."""
    out = []
    for scale in (0.1, 0.25, 0.5, 1.0, 2.0, 3.0):
        rates = {k: (r * (1.0 if lm else scale), rep, lm) for k, (r, rep, lm) in RATES.items()}
        row = {"silent_fault_rate_scale": scale}
        for regime in REGIMES:
            rs = [simulate(cars=cars, seed=s, regime=regime, rates=rates) for s in seeds]
            row[regime] = round(sum(r["broken_car_days"] for r in rs) / len(rs), 1)
        row["prove_vs_line_monitor_reduction"] = round(1 - row["prove"] / max(row["line_monitor"], 1e-9), 3)
        out.append(row)
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(compare(), indent=1))
    print(json.dumps(sensitivity(), indent=1))
    led = EvidenceLedger()
    simulate(regime="prove", ledger=led)
    print(led.verify(), len(led.entries))
