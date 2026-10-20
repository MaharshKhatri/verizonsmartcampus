"""Ground-truth crowd generator and the telemetry the AI is allowed to see.

The same generator produces two views of a day:
  * truth  - actual attendance, per-zone noise, unannounced surprise events
  * prior  - what the registrar timetable, event calendar and game schedule
             predict (nominal attendance, no noise, announced events only)

The forecaster only ever sees the prior, noisy aggregate telemetry and bus
passenger counts - never the truth.
"""
import math
import random
from dataclasses import dataclass, field

from . import campus
from .config import STEP_MIN, STEPS_PER_DAY, VERIZON_SHARE, MBPS_PER_SUB

NOMINAL_ATTENDANCE = 0.87
K_ANON_FLOOR = 20          # aggregate counts below this are suppressed (privacy)

# The timetable is not the building: seats scheduled differ from people present by a
# building-specific factor the prior never sees (study rooms, labs, staff, skipped
# sections). Fixed across days so the forecaster must learn it from telemetry.
_bias_rng = random.Random(424242)
ZONE_BIAS = {z.key: max(0.7, _bias_rng.gauss(1.0, 0.12)) for z in campus.ZONES}

# Sensing (research/03: 12,550 Juniper Mist APs; Verizon ~38% of devices, est).
WIFI_COVERAGE = {"venue": 0.0}         # share of people whose device is associated to campus Wi-Fi;
WIFI_COVERAGE_DEFAULT = 0.80           # the stadium's 180 student-section APs are not a sample of the bowl
WIFI_NOISE = 0.06
CARRIER_NOISE = 0.15                   # per-building attribution from sector / small-cell counts
CARRIER_MISATTRIBUTED = {"venue": 0.01}  # in-bowl DAS sectors barely hear neighbouring buildings
CARRIER_MISATTRIBUTED_DEFAULT = 0.30


@dataclass
class Event:
    zone: str
    start: int             # step
    end: int               # step
    crowd: int
    announced: bool
    label: str = "event"
    expected: int = 0      # organiser's estimate used by the prior (0 -> 80% of crowd)


@dataclass
class Game:
    zone: str
    kickoff: int           # step
    attendance: int
    label: str = "Home game"
    expected: int = 0      # ticketing forecast used by the prior (0 -> 93% of attendance)


@dataclass
class DayContext:
    name: str
    day_type: str          # weekday | saturday | finals
    weather: str           # mild | warm | hot
    attendance: float
    zone_noise: dict
    events: list = field(default_factory=list)
    games: list = field(default_factory=list)
    seed: int = 0


def _h(hours):
    return int(round(hours * 60))


def interp(points, minute):
    """Piecewise-linear profile; points are (minute, value) sorted by minute."""
    if minute <= points[0][0]:
        return points[0][1]
    for (m0, v0), (m1, v1) in zip(points, points[1:]):
        if minute <= m1:
            return v0 + (v1 - v0) * (minute - m0) / (m1 - m0)
    return points[-1][1]


PROFILES = {
    ("dining", "weekday"): [(0, 0), (_h(7), .02), (_h(7.5), .15), (_h(8.5), .30), (_h(9.5), .12), (_h(11), .25),
                            (_h(12), 1.0), (_h(13.5), .85), (_h(14.5), .25), (_h(16.5), .20), (_h(17.5), .80),
                            (_h(18.5), .95), (_h(20), .30), (_h(21), .05), (_h(24), 0)],
    ("library", "weekday"): [(0, .05), (_h(2), .02), (_h(7.5), .02), (_h(9), .25), (_h(12), .50), (_h(15), .75),
                             (_h(17), .60), (_h(19), .85), (_h(22), .70), (_h(24), .25)],
    ("library", "finals"): [(0, .60), (_h(3), .35), (_h(6), .10), (_h(8), .35), (_h(11), .90), (_h(15), 1.25),
                            (_h(18), 1.10), (_h(21), 1.45), (_h(24), 1.0)],
    ("residence", "weekday"): [(0, .88), (_h(7), .90), (_h(9), .55), (_h(11), .32), (_h(16), .30), (_h(18), .55),
                               (_h(21), .75), (_h(24), .88)],
    ("residence", "saturday"): [(0, .70), (_h(4), .85), (_h(10), .82), (_h(13), .60), (_h(18), .45), (_h(22), .50),
                                (_h(24), .65)],
    ("rec", "weekday"): [(0, 0), (_h(6), .02), (_h(7), .20), (_h(9), .15), (_h(12), .35), (_h(15), .40), (_h(17), .85),
                         (_h(20), 1.0), (_h(22), .60), (_h(23), .05), (_h(24), 0)],
    ("student_center", "weekday"): [(0, .02), (_h(7), .05), (_h(9), .30), (_h(11.5), .65), (_h(12.5), .85),
                                    (_h(14), .60), (_h(17), .45), (_h(19), .40), (_h(22), .20), (_h(24), .03)],
    ("student_center", "finals"): [(0, .45), (_h(3), .30), (_h(6), .05), (_h(9), .40), (_h(12.5), .95), (_h(16), .90),
                                   (_h(20), 1.05), (_h(24), .80)],
    ("academic_bg", "weekday"): [(0, 0), (_h(7), .02), (_h(8), .06), (_h(17), .06), (_h(21), .03), (_h(23), 0)],
}

SATURDAY_SCALE = {"dining": .55, "library": .45, "rec": .70, "student_center": .45, "academic_bg": .30}
CANCELLED_SCALE = {"dining": .80, "library": .35, "rec": .85, "student_center": .50, "academic_bg": .15}
FINALS_CLASS_SCALE = 0.55   # finals week: exams replace most lectures


def profile(kind, day_type, minute):
    """Share of a zone's peak present. day_type: weekday | saturday | finals | cancelled (snow day)."""
    key = (kind, day_type)
    if key in PROFILES:
        return interp(PROFILES[key], minute)
    if day_type == "cancelled":
        if kind == "residence":
            return min(1.0, 1.1 * interp(PROFILES[("residence", "saturday")], minute))
        return interp(PROFILES[(kind, "weekday")], minute) * CANCELLED_SCALE.get(kind, 1.0)
    base = interp(PROFILES[(kind, "weekday")], minute)
    if day_type == "saturday":
        return base * SATURDAY_SCALE.get(kind, 1.0)
    return base


def make_day(name, seed, day_type="weekday", weather="mild", scheduled_events=(), games=(),
             surprise_rate=0.8, attendance=None):
    """Draw a random day. scheduled_events are announced; surprises are not."""
    rng = random.Random(seed)
    att = attendance if attendance is not None else rng.uniform(0.76, 0.95)
    zone_noise = {z.key: rng.gauss(1.0, 0.05) for z in campus.ZONES}
    events = list(scheduled_events)
    n_surprise = _poisson(rng, surprise_rate)
    kinds = ("student_center", "library", "dining") if day_type == "cancelled" else \
        ("student_center", "academic", "library", "dining")      # classroom buildings are closed on a snow day
    candidates = [z.key for z in campus.ZONES if z.kind in kinds]
    for _ in range(n_surprise):
        zk = rng.choice(candidates)
        start = rng.randint(_h(10) // STEP_MIN, _h(19) // STEP_MIN)
        dur = rng.randint(6, 18)
        crowd = int(rng.uniform(0.25, 0.6) * campus.ZONE_BY_KEY[zk].peak)
        events.append(Event(zk, start, start + dur, crowd, announced=False, label="Unannounced crowd"))
    return DayContext(name, day_type, weather, att, zone_noise, events, list(games), seed)


def _poisson(rng, lam):
    k, p, threshold = 0, 1.0, math.exp(-lam)
    while True:
        p *= rng.random()
        if p <= threshold:
            return k
        k += 1


def _class_weight(minute, start, end):
    """(seated, moving) weights for one class period at a given minute."""
    if start - 15 <= minute < start:
        return 0.0, (minute - (start - 15)) / 15.0
    if start <= minute < end:
        return 1.0, 0.0
    if end <= minute < end + 10:
        return 0.0, 1.0 - (minute - end) / 10.0
    return 0.0, 0.0


def _venue_curve(minute, kickoff_min, attendance, short=False):
    """Crowd in a venue zone (stadium bowl + lots) around an event."""
    if short:   # arena: shorter ingress/egress
        pts = [(-120, 0), (-60, .15), (-20, .70), (10, 1.0), (130, 1.0), (150, .35), (175, .05), (200, 0)]
    else:       # football: tailgating, ~3.5 h game
        pts = [(-300, 0), (-240, .08), (-120, .30), (-30, .72), (15, 1.0), (200, 1.0), (215, .55), (245, .12),
               (290, 0)]
    pts = [(kickoff_min + m, v * attendance) for m, v in pts]
    return interp(pts, minute)


def occupancy(day, truth=True):
    """Return {zone: {"total": [...], "rate_people": [...]}} for one day.

    rate_people[t] = sum over activities of people * busy-hour Mbps per subscriber,
    so demand_mbps = VERIZON_SHARE * rate_people.
    """
    rng = random.Random(day.seed * 7919 + 17) if truth else None
    att = day.attendance if truth else NOMINAL_ATTENDANCE
    bias = ZONE_BIAS if truth else {}
    out = {}
    class_scale = FINALS_CLASS_SCALE if day.day_type == "finals" else 1.0
    has_classes = day.day_type in ("weekday", "finals")
    campus_moving = {"busch": [0.0] * STEPS_PER_DAY, "livingston": [0.0] * STEPS_PER_DAY}

    # Pass 1: academic buildings drive the between-class movement.
    for z in campus.ZONES:
        if z.kind != "academic":
            continue
        noise = day.zone_noise[z.key] * bias.get(z.key, 1.0) if truth else 1.0
        total, rate = [], []
        for t in range(STEPS_PER_DAY):
            minute = t * STEP_MIN + STEP_MIN / 2
            seated = moving = 0.0
            if has_classes:
                for p, (st, en) in enumerate(campus.CLASS_PERIODS):
                    s, m = _class_weight(minute, st, en)
                    seats = z.peak * campus.PERIOD_FILL[p] * att * noise * class_scale
                    seated += s * seats
                    moving += m * seats
            bg = z.peak * profile("academic_bg", day.day_type, minute)
            total.append(seated + moving + bg)
            rate.append(seated * MBPS_PER_SUB["in_class"] + moving * MBPS_PER_SUB["moving"]
                        + bg * MBPS_PER_SUB["social"])
            campus_moving[z.campus][t] += moving
        out[z.key] = {"total": total, "rate_people": rate}

    # Pass 2: everything else.
    for z in campus.ZONES:
        if z.kind == "academic":
            continue
        noise = day.zone_noise[z.key] * bias.get(z.key, 1.0) if truth else 1.0
        total, rate = [], []
        for t in range(STEPS_PER_DAY):
            minute = t * STEP_MIN + STEP_MIN / 2
            if z.kind == "student_center":
                social = z.peak * 0.75 * profile("student_center", day.day_type, minute) * noise
                hub = 0.22 * campus_moving[z.campus][t]
                total.append(social + hub)
                rate.append(social * MBPS_PER_SUB["social"] + hub * MBPS_PER_SUB["moving"])
            elif z.kind == "residence":
                people = z.peak * profile("residence", day.day_type, minute) * noise
                total.append(people)
                rate.append(people * MBPS_PER_SUB["residence"])
            elif z.kind in ("dining", "rec"):
                people = z.peak * profile(z.kind, day.day_type, minute) * noise
                total.append(people)
                rate.append(people * MBPS_PER_SUB["social"])
            elif z.kind == "library":
                people = z.peak * profile("library", day.day_type, minute) * noise
                total.append(people)
                rate.append(people * MBPS_PER_SUB["in_class"])
            elif z.kind == "venue":
                people = 20.0 if 8 * 60 <= minute <= 18 * 60 else 6.0   # staff
                for g in day.games:
                    if g.zone == z.key:
                        crowd = g.attendance * noise if truth else (g.expected or 0.93 * g.attendance)
                        people += _venue_curve(minute, g.kickoff * STEP_MIN, crowd, short=(z.key == "ARENA"))
                halftime = any(g.zone == z.key and 85 <= minute - g.kickoff * STEP_MIN <= 110 for g in day.games)
                total.append(people)
                rate.append(people * MBPS_PER_SUB["venue"] * (1.25 if halftime else 1.0))
            else:
                total.append(0.0)
                rate.append(0.0)
        out[z.key] = {"total": total, "rate_people": rate}

    # Calendar events (announced ones only in the prior) and surprises (truth only).
    for ev in day.events:
        if not truth and not ev.announced:
            continue
        series = out[ev.zone]
        for t in range(max(0, ev.start - 3), min(STEPS_PER_DAY, ev.end + 3)):
            if t < ev.start:
                w = (t - (ev.start - 3)) / 3.0
            elif t >= ev.end:
                w = 1.0 - (t - ev.end + 1) / 3.0
            else:
                w = 1.0
            add = max(0.0, w) * (ev.crowd if truth else (ev.expected or 0.8 * ev.crowd))
            series["total"][t] += add
            series["rate_people"][t] += add * (0.3 * MBPS_PER_SUB["moving"] + 0.7 * MBPS_PER_SUB["social"])

    # Correlated measurement-free "reality" noise on top of everything.
    if truth:
        for z in campus.ZONES:
            e = 0.0
            tot, rate = out[z.key]["total"], out[z.key]["rate_people"]
            for t in range(STEPS_PER_DAY):
                e = 0.85 * e + rng.gauss(0.0, 0.03)
                f = max(0.6, 1.0 + e)
                tot[t] *= f
                rate[t] *= f
    return out


def demand_mbps(series, t):
    return VERIZON_SHARE * series["rate_people"][t]


def observe(truth_occ, seed, mode="fused"):
    """Aggregate, k-anonymised occupancy estimates per zone and step.

    Two sources, each a count of devices (never identities):
      wifi     campus Wi-Fi association counts (the university's own Juniper Mist data):
               good indoors, nearly blind in the stadium bowl
      carrier  Verizon connected-device counts: ~38% of people, attributed to a building
               from sector / small-cell geometry, so some spill into a neighbouring zone
    mode = "fused" (Wi-Fi where it sees the zone, carrier where it doesn't; the default),
    "wifi" or "carrier" (single-source ablations).
    Each raw count below K_ANON_FLOOR is suppressed before it is used.
    """
    rng = random.Random(seed * 104729 + 3)
    obs = {}
    keys = list(truth_occ)
    for zk in keys:
        z = campus.ZONE_BY_KEY[zk]
        p_w = WIFI_COVERAGE.get(z.kind, WIFI_COVERAGE_DEFAULT)
        mis = CARRIER_MISATTRIBUTED.get(z.kind, CARRIER_MISATTRIBUTED_DEFAULT)
        nbrs = [n for n in campus.neighbors(zk) if n in truth_occ] or [zk]
        row = []
        for t, v in enumerate(truth_occ[zk]["total"]):
            # Wi-Fi: binomial sampling + device-per-person noise
            w = (v * p_w * (1.0 + rng.gauss(0.0, WIFI_NOISE))
                 + rng.gauss(0.0, math.sqrt(max(v * p_w * (1 - p_w), 0.0)))) if p_w > 0 else 0.0
            # Carrier: own share minus spill-out plus spill-in from a neighbour
            nb = truth_occ[nbrs[t % len(nbrs)]]["total"][t]
            seen = (1.0 - mis) * v + mis * nb
            c = seen * VERIZON_SHARE * (1.0 + rng.gauss(0.0, CARRIER_NOISE))
            ests, upper = [], None
            for source, count, p, rel in (("wifi", w, p_w, WIFI_NOISE),
                                          ("carrier", c, VERIZON_SHARE, CARRIER_NOISE + mis / 2)):
                if p <= 0 or mode not in ("fused", source):
                    continue
                if count < K_ANON_FLOOR:
                    # A suppressed count still says "fewer than k devices": an upper bound.
                    bound = K_ANON_FLOOR / p
                    upper = bound if upper is None else min(upper, bound)
                    continue
                est = count / p
                ests.append((est, rel ** 2 + (1.0 - p) / max(est * p, 1.0)))
            if not ests:
                row.append(float(K_ANON_FLOOR // 2))
                continue
            # Wi-Fi first: where campus Wi-Fi sees the zone its estimate is used as is, because
            # carrier attribution error is a bias (neighbour spill), not noise that averages out.
            # Carrier counts take over where Wi-Fi is blind (stadium bowl, arena, outdoors).
            est = ests[0][0]
            row.append(round(min(est, upper) if upper is not None else est))
        obs[zk] = row
    return obs


def bus_inflow(occ):
    """People arriving at each campus by bus, per step, derived from occupancy increases."""
    inflow = {"busch": [0.0] * STEPS_PER_DAY, "livingston": [0.0] * STEPS_PER_DAY}
    for z in campus.ZONES:
        if z.kind not in ("academic", "student_center", "venue"):
            continue
        share = 0.30 if z.kind == "venue" else campus.BUS_SHARE_OF_ARRIVALS
        tot = occ[z.key]["total"]
        for t in range(1, STEPS_PER_DAY):
            inc = tot[t] - tot[t - 1]
            if inc > 0:
                inflow[z.campus][t] += share * inc
    return inflow


def bus_telemetry(inflow, seed, lookahead=campus.BUS_TRAVEL_STEPS):
    """At step t, passengers already on buses tell us arrivals for t+1..t+lookahead (with noise)."""
    rng = random.Random(seed * 15485863 + 11)
    tele = {}
    for c, series in inflow.items():
        rows = []
        for t in range(STEPS_PER_DAY):
            row = []
            for k in range(1, lookahead + 1):
                idx = t + k
                v = series[idx] if idx < STEPS_PER_DAY else 0.0
                row.append(max(0.0, v * (1.0 + rng.gauss(0.0, 0.10))))
            rows.append(row)
        tele[c] = rows
    return tele
