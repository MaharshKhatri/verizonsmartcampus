"""Zero-touch, intent-based network slicing for campus customers.

Campus IT types a request in plain English; the engine turns it into a 3GPP
slice profile (S-NSSAI SST + 5QI), checks it against the occupancy forecast
(crowd demand + other reservations must fit the zone's capacity), and either
admits it, counter-offers, or explains why not. Admitted slices become hard
wake constraints for the Circadian controller.

The parser is deterministic and offline (works on a poster-session laptop
with no internet). The same JSON contract can be produced by an LLM.
"""
import re
from dataclasses import dataclass, field, asdict

from . import campus
from .config import SLICE_PRICE_USD_HR, STEP_MIN, STEPS_PER_DAY, VERIZON_SHARE, ASSET_TYPES

ALIASES = {
    "SHI": ["shi stadium", "stadium", "shi", "football"],
    "ENG": ["weeks hall", "richard weeks", "engineering", "robotics lab", "eng "],
    "HILL": ["hill center", "hill"],
    "BSC": ["busch student center", "busch campus center", "the cove", "bsc"],
    "LSM": ["library of science", "lsm", "science library"],
    "ARC": ["allison road", "arc"],
    "WERB": ["werblin", "rec center", "recreation center"],
    "BDINE": ["busch dining"],
    "BRES": ["busch residence", "busch dorms", "busch suites"],
    "LSC": ["livingston student center", "lsc"],
    "TIL": ["tillett", "lucy stone"],
    "RBS": ["business school", "rbs"],
    "LDINE": ["livingston dining"],
    "LRES": ["livingston apartments", "quads", "towers", "livingston dorms"],
    "ARENA": ["jersey mike", "arena", "rac"],
}
CAMPUS_WIDE = {"busch": "busch campus", "livingston": "livingston campus"}

PROFILES = {   # slice type -> (SST, 5QI, description)
    "eMBB-UL": (1, "2", "GBR live video uplink, 150 ms packet delay budget"),
    "eMBB": (1, "4", "GBR video / bulk downlink, 300 ms"),
    "URLLC": (2, "82", "Delay-critical GBR, 10 ms packet delay budget"),
    "MC-PRIORITY": (1, "65/67/69", "Mission-critical PTT voice, video and signalling; ARP pre-emption"),
    "mIoT": (3, "9", "Massive IoT, non-GBR"),
}


@dataclass
class SliceSpec:
    text: str
    zones: list = field(default_factory=list)
    start: int = 0
    end: int = STEPS_PER_DAY
    mbps: float = 0.0
    direction: str = "DL"
    latency_ms: int = 0
    devices: int = 0
    slice_type: str = "eMBB"
    sst: int = 1
    five_qi: str = "9"
    issues: list = field(default_factory=list)

    def to_dict(self):
        d = asdict(self)
        d["window"] = f"{_clock(self.start)}-{_clock(self.end)}"
        return d


def _clock(step):
    m = min(step * STEP_MIN, 24 * 60)
    return f"{m // 60:02d}:{m % 60:02d}"


TIME = r"(\d{1,2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?"
RANGE = re.compile(TIME + r"\s*(?:to|-|–|until|and|till)\s*" + TIME)


def _to_minutes(h, m, ampm):
    h, m = int(h), int(m or 0)
    ampm = (ampm or "").replace(".", "")
    if ampm == "pm" and h < 12:
        h += 12
    if ampm == "am" and h == 12:
        h = 0
    if not ampm and 1 <= h <= 7:      # "from 2 to 6" on a campus most likely means afternoon
        h += 12
    return h * 60 + m


def parse(text, games=()):
    low = " " + text.lower() + " "
    spec = SliceSpec(text=text)

    for key, names in ALIASES.items():
        if any(n in low for n in names):
            spec.zones.append(key)
    for c, phrase in CAMPUS_WIDE.items():
        if phrase in low or (f"across {c}" in low):
            spec.zones = [z.key for z in campus.ZONES if z.campus == c]
    if not spec.zones:
        spec.issues.append("Which building or campus? (e.g. 'SHI Stadium', 'Weeks Hall', 'across Busch')")

    bw = re.search(r"(\d+(?:\.\d+)?)\s*(gbps|gb/s|mbps|mb/s|megabits)", low)
    if bw:
        spec.mbps = float(bw.group(1)) * (1000.0 if bw.group(2).startswith("g") else 1.0)
    lat = re.search(r"(\d+)\s*(ms|millisecond)", low)
    if lat:
        spec.latency_ms = int(lat.group(1))
    elif any(w in low for w in ("low latency", "low-latency", "real-time", "realtime")):
        spec.latency_ms = 20
    dev = re.search(r"(\d+)\s+(?:[\w-]+\s+){0,3}?(cameras|devices|sensors|robots|radios|officers|units|drones)\b", low)
    if dev:
        spec.devices = int(dev.group(1))
    if any(w in low for w in ("uplink", "upload", " ul ", "cameras", "broadcast", "livestream", "live stream")):
        spec.direction = "UL"

    rng = RANGE.search(low)
    if rng:
        h1, m1, a1, h2, m2, a2 = rng.groups()
        a1n, a2n = (a1 or "").replace(".", ""), (a2 or "").replace(".", "")
        end = _to_minutes(h2, m2, a2n or a1n)
        if a1n:
            start = _to_minutes(h1, m1, a1n)
        else:   # "10 to 2pm" -> 10am; "1 to 4pm" -> 1pm: pick the reading that starts before the end
            options = [_to_minutes(h1, m1, a2n), _to_minutes(h1, m1, "am"), _to_minutes(h1, m1, "pm")]
            start = next((o for o in options if o < end), options[0])
        if end <= start:
            spec.issues.append("The window ends before it starts - check the times.")
        spec.start, spec.end = start // STEP_MIN, min(STEPS_PER_DAY, -(-end // STEP_MIN))
    elif "during the game" in low or "game day" in low or "gameday" in low:
        g = next((g for g in games if g.zone in (spec.zones or ["SHI"])), None)
        if g:
            spec.start, spec.end = max(0, g.kickoff - 36), min(STEPS_PER_DAY, g.kickoff + 54)
        else:
            spec.issues.append("No game is scheduled today - give a time window.")
    elif "all day" not in low:
        spec.issues.append("What time window? (e.g. 'from 1pm to 7pm')")

    if any(w in low for w in ("police", "rupd", "public safety", "emergency", "ems", "first responder", "fire")):
        spec.slice_type = "MC-PRIORITY"
    elif spec.latency_ms and spec.latency_ms <= 20:
        spec.slice_type = "URLLC"
    elif any(w in low for w in ("sensor", "iot", "meter", "telemetry")):
        spec.slice_type = "mIoT"
    elif spec.direction == "UL":
        spec.slice_type = "eMBB-UL"
    spec.sst, spec.five_qi, _ = PROFILES[spec.slice_type]

    if not spec.mbps:
        if spec.slice_type == "MC-PRIORITY":
            spec.mbps = 50.0
        elif spec.devices:
            per = {"eMBB-UL": 25.0, "URLLC": 5.0, "mIoT": 0.1}.get(spec.slice_type, 10.0)
            spec.mbps = spec.devices * per
        else:
            spec.issues.append("How much bandwidth? (e.g. '400 Mbps uplink')")
    return spec


def zone_max_capacity(zone_key):
    z = campus.ZONE_BY_KEY[zone_key]
    return sum(ASSET_TYPES[t].capacity_mbps * n for t, n in z.assets.items())


def admit(spec, prior_occ, q90=0.15, reservations=()):
    """Check the request against forecast crowd demand + existing reservations.

    Returns a dict with status ADMITTED / COUNTER_OFFER / NEEDS_INFO / REJECTED.
    """
    if spec.issues:
        return {"status": "NEEDS_INFO", "questions": spec.issues, "spec": spec.to_dict()}
    per_zone = spec.mbps / max(1, len(spec.zones)) if len(spec.zones) > 1 else spec.mbps
    worst_headroom = None
    for zk in spec.zones:
        cap = zone_max_capacity(zk) * 0.85
        series = prior_occ[zk]
        for t in range(spec.start, spec.end):
            crowd = VERIZON_SHARE * series["rate_people"][t] * (1.0 + q90)
            other = sum(r.mbps / max(1, len(r.zones)) for r in reservations
                        if zk in r.zones and r.start <= t < r.end)
            headroom = cap - crowd - other
            if worst_headroom is None or headroom < worst_headroom[0]:
                worst_headroom = (headroom, zk, t)
    hours = (spec.end - spec.start) * STEP_MIN / 60.0
    price = SLICE_PRICE_USD_HR[spec.slice_type if spec.slice_type in SLICE_PRICE_USD_HR else "eMBB-UL"]
    quote = round(price * hours * max(1.0, spec.mbps / 100.0), 2)
    result = {"spec": spec.to_dict(), "hours": round(hours, 2), "quote_usd": quote,
              "profile": PROFILES[spec.slice_type][2]}
    if spec.slice_type == "MC-PRIORITY" or worst_headroom is None or worst_headroom[0] >= per_zone:
        result["status"] = "ADMITTED"
        result["explanation"] = (f"Forecast leaves room for {spec.mbps:.0f} Mbps {spec.direction} in "
                                 f"{', '.join(spec.zones)} {_clock(spec.start)}-{_clock(spec.end)}; "
                                 f"radios will be pre-woken 15 min before the window.")
        return result
    headroom, zk, t = worst_headroom
    if headroom > 0.25 * per_zone:
        offer = int(headroom * max(1, len(spec.zones)) // 10 * 10)
        result["status"] = "COUNTER_OFFER"
        result["offer_mbps"] = offer
        result["explanation"] = (f"At {_clock(t)} the forecast crowd in {zk} leaves only ~{headroom:.0f} Mbps; "
                                 f"we can guarantee {offer} Mbps, or full rate outside that peak.")
        return result
    result["status"] = "REJECTED"
    result["explanation"] = f"{zk} is forecast to be saturated at {_clock(t)}; suggest a different window."
    return result
