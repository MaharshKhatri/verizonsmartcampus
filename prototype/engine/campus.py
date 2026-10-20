"""Rutgers Busch + Livingston campus model: zones, radio assets, buses, timetable.

Coordinates come from OpenStreetMap (research/03_competition_and_rutgers.md,
section 4); BRES, TIL, RBS, LDINE and LRES are approximate cluster centroids.
Radio asset counts are a representative deployment for simulation, not
Verizon's actual site inventory. Building areas and peak headcounts are
estimates the pilot would replace with Juniper Mist and registrar data.
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Zone:
    key: str
    name: str
    campus: str            # "busch" | "livingston"
    kind: str              # academic | student_center | library | dining | residence | rec | venue
    lat: float
    lon: float
    peak: int              # typical peak people present on a normal weekday
    sqft: int              # conditioned floor area (est)
    assets: dict = field(default_factory=dict)  # asset type -> count
    study_space: bool = False


ZONES = [
    # --- Busch ---
    Zone("BSC", "Busch Student Center", "busch", "student_center", 40.52333, -74.45886, 3400, 115_000,
         {"lowband": 1, "cband": 1, "mmwave": 1, "small": 3}, study_space=True),
    Zone("HILL", "Hill Center", "busch", "academic", 40.52173, -74.46253, 1800, 220_000,
         {"lowband": 1, "cband": 1, "small": 3}, study_space=True),
    Zone("ENG", "Weeks Hall & Engineering Complex", "busch", "academic", 40.52438, -74.45969, 2600, 420_000,
         {"lowband": 1, "cband": 1, "mmwave": 1, "small": 4}, study_space=True),
    Zone("ARC", "Allison Road Classroom Bldg", "busch", "academic", 40.52383, -74.46523, 2200, 105_000,
         {"lowband": 1, "cband": 1, "small": 3}),
    Zone("LSM", "Library of Science & Medicine", "busch", "library", 40.52481, -74.46719, 900, 140_000,
         {"lowband": 1, "cband": 1, "small": 2}, study_space=True),
    Zone("BDINE", "Busch Dining Hall", "busch", "dining", 40.52267, -74.45780, 1100, 45_000,
         {"lowband": 1, "small": 3}),
    Zone("BRES", "Busch Residence Halls", "busch", "residence", 40.51950, -74.45600, 3200, 650_000,
         {"lowband": 1, "cband": 1, "small": 5}),
    Zone("WERB", "Werblin Recreation Center", "busch", "rec", 40.51962, -74.46101, 700, 160_000,
         {"lowband": 1, "small": 2}),
    Zone("SHI", "SHI Stadium", "busch", "venue", 40.51350, -74.46514, 0, 90_000,
         {"lowband": 1, "cband": 4, "mmwave": 8, "das": 6}),   # stadiums are provisioned for the sellout peak
    # --- Livingston ---
    Zone("LSC", "Livingston Student Center", "livingston", "student_center", 40.52358, -74.43722, 3000, 125_000,
         {"lowband": 1, "cband": 1, "mmwave": 2, "small": 3}, study_space=True),
    Zone("TIL", "Tillett & Lucy Stone Halls", "livingston", "academic", 40.52200, -74.43650, 2400, 170_000,
         {"lowband": 1, "cband": 1, "small": 3}),
    Zone("RBS", "Rutgers Business School", "livingston", "academic", 40.52260, -74.44030, 1800, 165_000,
         {"lowband": 1, "cband": 1, "small": 3}, study_space=True),
    Zone("LDINE", "Livingston Dining Commons", "livingston", "dining", 40.52420, -74.43570, 1200, 60_000,
         {"lowband": 1, "small": 3}),
    Zone("LRES", "Livingston Apartments, Quads & Towers", "livingston", "residence", 40.52680, -74.43450, 4500, 950_000,
         {"lowband": 1, "cband": 2, "small": 6}),
    Zone("ARENA", "Jersey Mike's Arena", "livingston", "venue", 40.52520, -74.44136, 0, 230_000,
         {"lowband": 1, "cband": 2, "mmwave": 2, "das": 2}),
]

ZONE_BY_KEY = {z.key: z for z in ZONES}

# Off-map gateways that buses connect to (College Ave and Cook student centers).
GATEWAYS = {
    "CAVE": ("College Avenue", 40.50263, -74.45251),
    "COOK": ("Cook/Douglass", 40.47913, -74.43147),
}

# Simplified route geometry: (route, ordered stops). Stops are zone keys or gateways.
BUS_ROUTES = {
    "B": ["LSC", "RBS", "ARENA", "BSC", "HILL", "ARC", "LSM", "BSC", "ARENA", "LSC"],
    "H": ["CAVE", "BSC", "HILL", "ARC", "BRES", "WERB", "BSC", "CAVE"],
    "A": ["CAVE", "LSM", "ARC", "HILL", "BSC", "CAVE"],
    "LX": ["CAVE", "LSC", "TIL", "LRES", "LDINE", "LSC", "CAVE"],
    "REXB": ["COOK", "BSC", "HILL", "COOK"],
    "REXL": ["COOK", "LSC", "TIL", "COOK"],
}
# Routes per IPO (research/03, section 6); operator Academy Bus Lines and the TripShot
# app since July 1 2026. ~70,000 daily NB riders on ~60 buses (Rutgers estimate).
BUS_TRAVEL_STEPS = 4      # a cross-campus trip is ~20 minutes door to door
BUS_SHARE_OF_ARRIVALS = 0.35   # est: share of class arrivals that come by bus

# Rutgers-New Brunswick standard course periods (80-minute classes, Mon-Fri),
# minutes after midnight; 30-minute class-change windows between them.
# Source: scheduling.rutgers.edu/standard-course-periods (research/03, section 7).
CLASS_PERIODS = [
    (8 * 60 + 30, 9 * 60 + 50),
    (10 * 60 + 20, 11 * 60 + 40),
    (12 * 60 + 10, 13 * 60 + 30),
    (14 * 60 + 0, 15 * 60 + 20),
    (15 * 60 + 50, 17 * 60 + 10),
    (17 * 60 + 40, 19 * 60 + 0),
    (19 * 60 + 30, 20 * 60 + 50),
    (21 * 60 + 20, 22 * 60 + 40),
]
# Share of a building's peak seats scheduled in each period (est; registrar data in the pilot).
PERIOD_FILL = [0.55, 0.88, 0.95, 0.90, 0.74, 0.42, 0.22, 0.08]

SHI_CAPACITY = 52_454     # listed capacity; record crowd 55,942 (Iowa, Sep 19 2025)
ARENA_CAPACITY = 8_000


def neighbors(key):
    """Zones adjacent on the bus/walk graph (used as spatial features)."""
    adj = set()
    for stops in BUS_ROUTES.values():
        for a, b in zip(stops, stops[1:]):
            if a == key and b in ZONE_BY_KEY:
                adj.add(b)
            if b == key and a in ZONE_BY_KEY:
                adj.add(a)
    adj.discard(key)
    return sorted(adj)


def asset_inventory(overrides=None):
    """Expand zone asset counts into a flat, stably ordered list of (asset_id, zone_key, type).

    overrides: {zone_key: {asset_type: count}} for sensitivity runs (e.g. a tighter stadium).
    """
    out = []
    for z in ZONES:
        assets = dict(z.assets, **(overrides or {}).get(z.key, {}))
        for typ, count in assets.items():
            for i in range(count):
                out.append((f"{z.key}-{typ}-{i + 1}", z.key, typ))
    return out
