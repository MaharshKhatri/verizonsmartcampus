"""Radio access network model and the three energy policies compared in the demo.

  ALWAYS_ON  - legacy: every carrier active (micro-DTX only)
  REACTIVE   - legacy vendor energy saving: threshold rules on the radio's
               own measured load, light sleep in daytime, deep sleep only in a
               fixed night window (kept for the efficient-frontier analysis)
  planner    - latency-aware deepest-safe sleep over a 60-minute forecast,
               slice reservations as hard constraints, and an SLA guard that
               wakes capacity on forecast misses. The traffic-history AI
               baseline and Circadian both use it; only their forecasts differ.
"""
from dataclasses import dataclass

from . import campus
from .config import (ASSET_TYPES, BASEBAND_W, CONGESTION_UTIL, GUARD_UTIL, MICRO_DTX_SAVING, MODE_ORDER,
                     POWER_CONVERSION_OVERHEAD, SLEEP_MODES, STEP_MIN, STEPS_PER_DAY)

MIN_DEEP_SLEEP_GAP = 4     # deep modes must pay back their wake-up: idle 20+ min beyond the wake time
TARGET_UTIL = 0.72         # Circadian plans capacity so P90 demand stays below this


@dataclass
class Asset:
    id: str
    zone: str
    type: str
    mode: str = "ACTIVE"
    waking: int = 0              # steps left until ACTIVE (0 = not waking)
    fault: str = ""              # active fault type, "" if healthy
    fault_capacity: float = 1.0  # capacity multiplier imposed by the fault
    low_steps: int = 0           # REACTIVE: consecutive low-load observations

    @property
    def spec(self):
        return ASSET_TYPES[self.type]

    def capacity(self):
        if self.waking:
            return 0.0
        return self.spec.capacity_mbps * SLEEP_MODES[self.mode].capacity_factor * self.fault_capacity

    def power(self, util):
        """Input power in watts at a given utilisation of this asset."""
        s = self.spec
        if self.fault == "psu_failure":
            return 0.0
        if self.waking:
            return s.p_static_w * (1.0 - MICRO_DTX_SAVING)   # booting + calibration at idle draw
        m = SLEEP_MODES[self.mode]
        if m.capacity_factor == 0.0:
            return s.p_static_w * m.static_factor
        static = s.p_static_w * m.static_factor * (1.0 - MICRO_DTX_SAVING * (1.0 - util))
        return static + (s.p_max_w - s.p_static_w) * util * m.capacity_factor

    def request(self, mode):
        """Ask the radio to move to `mode`. Returns True if anything changed."""
        if mode == self.mode and not self.waking:
            return False
        cur = SLEEP_MODES[self.mode]
        tgt = SLEEP_MODES[mode]
        if self.waking:
            if tgt.capacity_factor == 0.0:          # abort the wake, go back to sleep
                self.waking, self.mode = 0, mode
                return True
            return False
        if cur.capacity_factor == 0.0 and tgt.capacity_factor > 0.0:
            self.waking = max(1, cur.wake_steps)    # carrier must boot before it serves
            self.mode = mode
            return True
        self.mode = mode
        return True

    def tick(self):
        if self.waking:
            self.waking -= 1


def build_network(overrides=None):
    return [Asset(aid, zk, typ) for aid, zk, typ in campus.asset_inventory(overrides)]


def by_zone(assets):
    out = {z.key: [] for z in campus.ZONES}
    for a in assets:
        out[a.zone].append(a)
    return out


def serve(zone_assets, demand, extra_mbps=0.0, extra_w=0.0):
    """Serve one zone's demand for one step. Returns (capacity, util, watts, congested_share).

    extra_mbps / extra_w model capacity lent by neighbouring cells during
    cell-outage compensation (3GPP SON).
    """
    cap = sum(a.capacity() for a in zone_assets) + extra_mbps
    util = min(1.0, demand / cap) if cap > 0 else 1.0
    radio = sum(a.power(util if a.capacity() > 0 else 0.0) for a in zone_assets)
    macro = any(a.type in ("cband", "mmwave", "das") for a in zone_assets)
    watts = (radio + extra_w) * (1.0 + POWER_CONVERSION_OVERHEAD) + BASEBAND_W["macro" if macro else "indoor"]
    congested = 0.0
    if demand > 0 and demand > cap * CONGESTION_UTIL:
        congested = 1.0 - (cap * CONGESTION_UTIL) / demand
    return cap, util, watts, congested


def _efficiency(a):
    return a.spec.capacity_mbps / a.spec.p_static_w


# --------------------------------------------------------------------------
# REACTIVE (vendor-style) policy
# --------------------------------------------------------------------------
REACTIVE_SLEEP_UTIL = 0.35   # switch a carrier off if the rest would run below this load ...
REACTIVE_WAKE_UTIL = 0.65    # ... and wake one when measured load exceeds this


def reactive_step(zone_assets, last_demand, t, sleep_util=REACTIVE_SLEEP_UTIL, wake_util=REACTIVE_WAKE_UTIL,
                  day_deep=False):
    """Threshold rules on the zone's own last measured load.

    day_deep=True lets the reactive policy use deep sleep around the clock -
    used only for the efficient-frontier comparison.
    """
    minute = t * STEP_MIN
    night = day_deep or 60 <= minute < 5 * 60
    cap_assets = [a for a in zone_assets if a.spec.layer == "capacity" and not a.fault]
    cap_now = sum(a.capacity() for a in zone_assets)
    util = last_demand / cap_now if cap_now > 0 else 1.0
    changes = []

    # Scheduled end of the night window: deep-sleeping carriers come back.
    if not night:
        for a in cap_assets:
            if a.mode == "DEEP_SLEEP" and not a.waking and a.request("ACTIVE"):
                changes.append((a, "WAKE", "night energy-saving window ended"))

    # Wake on measured overload (most capacity first).
    if util > wake_util:
        asleep = sorted([a for a in cap_assets if a.mode != "ACTIVE" and not a.waking],
                        key=lambda a: -a.spec.capacity_mbps)
        need = 2 if util > 0.85 else 1
        for a in asleep[:need]:
            if a.request("ACTIVE"):
                changes.append((a, "ACTIVE", f"measured load {util:.0%} > {wake_util:.0%}"))
        return changes

    # MIMO muting on light load.
    for a in cap_assets:
        if a.type in ("cband", "das") and a.mode == "ACTIVE" and util < 0.30:
            a.request("MIMO_MUTE")
        elif a.mode == "MIMO_MUTE" and util > 0.50:
            a.request("ACTIVE")

    # Switch off one carrier after 15 minutes of low load.
    awake = [a for a in cap_assets if a.capacity() > 0]
    awake.sort(key=_efficiency)
    for a in awake:
        rest = cap_now - a.capacity()
        u_without = last_demand / rest if rest > 0 else 1.0
        if u_without < sleep_util:
            a.low_steps += 1
        else:
            a.low_steps = 0
    for a in awake:
        if a.low_steps >= 4:
            mode = "DEEP_SLEEP" if night else "CARRIER_OFF"
            a.request(mode)
            a.low_steps = 0
            changes.append((a, mode, "load below threshold for 20 min"))
            break
    return changes


# --------------------------------------------------------------------------
# CIRCADIAN (predictive) policy
# --------------------------------------------------------------------------
def circadian_plan(zone_assets, need_mbps):
    """Greedy efficiency-ordered capacity cover over the forecast horizon.

    need_mbps[k] is the capacity required k steps from now (k=0 is this step).
    Returns (first_needed, mute_ok): the first step each capacity asset is part
    of the cover (None if never within the horizon), and whether the marginal
    asset at k=0 can run MIMO-muted.
    """
    coverage = sum(a.spec.capacity_mbps * a.fault_capacity for a in zone_assets if a.spec.layer == "coverage")
    cands = [a for a in zone_assets if a.spec.layer == "capacity" and not a.fault]
    cands.sort(key=lambda a: -_efficiency(a))
    first_needed = {a.id: None for a in cands}
    mute_ok = set()
    for k, need in enumerate(need_mbps):
        have = coverage
        marginal = None
        for a in cands:
            if have >= need:
                break
            if first_needed[a.id] is None:
                first_needed[a.id] = k
            marginal = (a, have)
            have += a.spec.capacity_mbps * a.fault_capacity
        if k == 0 and marginal is not None:
            a, before = marginal
            if a.type in ("cband", "das"):
                mute_cap = a.spec.capacity_mbps * a.fault_capacity * SLEEP_MODES["MIMO_MUTE"].capacity_factor
                if before + mute_cap >= need and all(n <= need for n in need_mbps[1:3]):
                    mute_ok.add(a.id)
    return cands, first_needed, mute_ok


def circadian_step(zone_assets, need_mbps, last_util):
    """Apply the plan. Returns (changes, guard_fired)."""
    changes = []
    if last_util > GUARD_UTIL:
        # SLA guard: the forecast envelope was wrong - wake the fastest-waking capacity now.
        asleep = [a for a in zone_assets if a.spec.layer == "capacity" and not a.fault
                  and SLEEP_MODES[a.mode].capacity_factor == 0 and not a.waking]
        asleep.sort(key=lambda a: (SLEEP_MODES[a.mode].wake_steps, -a.spec.capacity_mbps))
        for a in asleep[:2]:
            if a.request("ACTIVE"):
                changes.append((a, "WAKE", f"SLA guard: measured load {last_util:.0%} broke the P90 envelope"))
        if changes:
            return changes, True

    cands, first_needed, mute_ok = circadian_plan(zone_assets, need_mbps)
    horizon = len(need_mbps)
    for a in cands:
        fn = first_needed[a.id]
        slack = horizon if fn is None else fn
        cur = SLEEP_MODES[a.mode]
        if a.waking:
            if fn is None:                                   # no longer needed: abort the wake
                a.request("CARRIER_OFF")
                changes.append((a, "CARRIER_OFF", "wake cancelled: demand no longer forecast"))
            continue
        if fn == 0:
            target = "MIMO_MUTE" if a.id in mute_ok else "ACTIVE"
            if cur.capacity_factor == 0:
                a.request(target)
                changes.append((a, "WAKE", "needed now (late wake)"))
            elif a.mode != target:
                a.request(target)
                changes.append((a, target, "partial capacity is enough for P90 demand" if target == "MIMO_MUTE"
                                else "full capacity needed for P90 demand"))
            continue
        if cur.capacity_factor == 0:                          # asleep and needed later (or never)
            if cur.wake_steps + 1 > slack:
                a.request("ACTIVE")
                changes.append((a, "WAKE", f"pre-wake: forecast needs it in {slack * STEP_MIN} min, "
                                           f"wake latency {cur.wake_steps * STEP_MIN} min"))
                continue
            best = deepest_allowed(slack)
            if best and MODE_ORDER.index(best) > MODE_ORDER.index(a.mode):
                a.request(best)
                changes.append((a, best, _idle_reason(slack, horizon)))
            continue
        best = deepest_allowed(slack)                         # awake but not needed now
        if best:
            a.request(best)
            changes.append((a, best, _idle_reason(slack, horizon)))
    return changes, False


def deepest_allowed(slack):
    """Deepest sleep mode that can still be ACTIVE in time and is worth its wake-up."""
    best = None
    for m in ("CARRIER_OFF", "DEEP_SLEEP", "DORMANT"):
        w = SLEEP_MODES[m].wake_steps
        if slack >= w + 1 + (MIN_DEEP_SLEEP_GAP if w >= 2 else 0):
            best = m
    return best


def _idle_reason(slack, horizon):
    if slack >= horizon:
        return "P90 forecast: not needed in the next 60 min"
    return f"P90 forecast: not needed for {slack * STEP_MIN} min"


def zone_static_full_power(zone_assets):
    return sum(a.spec.p_static_w for a in zone_assets)


assert STEPS_PER_DAY == 288
