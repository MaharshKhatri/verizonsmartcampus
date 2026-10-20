"""Parameters for the Circadian digital twin of Rutgers Busch + Livingston.

Every engineering or economic constant carries a source tag. Tags resolve in
SOURCES below and in research/*.md. A value tagged "est:" is a team
assumption the Rutgers pilot is designed to measure, not a published fact.
"""
from dataclasses import dataclass

STEP_MIN = 5
STEPS_PER_DAY = 24 * 60 // STEP_MIN  # 288
HORIZON_STEPS = 12                   # forecast 60 minutes ahead
HISTORY_DAYS = 14                    # synthetic history used to train the forecaster


@dataclass(frozen=True)
class AssetType:
    key: str
    label: str
    layer: str             # "coverage" never sleeps; "capacity" may sleep
    p_max_w: float         # input power at 100% load
    p_static_w: float      # load-independent input power while active
    capacity_mbps: float   # effective (not peak) downlink capacity
    source: str


ASSET_TYPES = {
    "lowband": AssetType("lowband", "Low-band coverage layer (LTE/NR 700-850 MHz)", "coverage",
                         p_max_w=520, p_static_w=330, capacity_mbps=60, source="est"),
    "cband": AssetType("cband", "C-band 64T64R massive-MIMO sector (n77)", "capacity",
                       p_max_w=1200, p_static_w=660, capacity_mbps=480, source="ran_power"),   # P1, P2
    "mmwave": AssetType("mmwave", "mmWave small cell (n261)", "capacity",
                        p_max_w=650, p_static_w=390, capacity_mbps=650, source="ran_power"),   # P7 (sensitivity)
    "small": AssetType("small", "Indoor 5G small cell (radio-dot class)", "capacity",
                       p_max_w=45, p_static_w=28, capacity_mbps=85, source="ran_power"),      # P8
    "das": AssetType("das", "Venue DAS sector (head-end share + ~40 remotes)", "capacity",
                     p_max_w=1400, p_static_w=950, capacity_mbps=1500, source="est"),         # P9 x remotes
}


@dataclass(frozen=True)
class SleepMode:
    name: str
    static_factor: float    # multiplier on p_static_w
    capacity_factor: float  # share of capacity_mbps still available
    wake_steps: int         # 5-minute steps needed to return to ACTIVE


# Ordered shallow -> deep; savings are research/02 parameters P12-P14, wake
# times are policy-level estimates (P20: no public vendor figure). Symbol
# shutdown (micro-DTX) is modelled inside the load-dependent power curve
# because radios apply it automatically at sub-millisecond scale.
SLEEP_MODES = {
    "ACTIVE": SleepMode("ACTIVE", 1.00, 1.00, 0),
    "MIMO_MUTE": SleepMode("MIMO_MUTE", 0.65, 0.40, 0),     # 64T -> 16T antenna muting (~230 W of 660)
    "CARRIER_OFF": SleepMode("CARRIER_OFF", 0.53, 0.0, 1),  # carrier / cell switch-off: -47%
    "DEEP_SLEEP": SleepMode("DEEP_SLEEP", 0.30, 0.0, 2),    # deep sleep / dormancy: -70%
    "DORMANT": SleepMode("DORMANT", 0.05, 0.0, 3),          # extreme deep sleep (Nokia: up to -95%)
}
MODE_ORDER = ["ACTIVE", "MIMO_MUTE", "CARRIER_OFF", "DEEP_SLEEP", "DORMANT"]
MICRO_DTX_SAVING = 0.34      # symbol shutdown: share of zero-load power saved (P10)

# Site equipment that never sleeps: baseband/transport per zone (P4), plus
# rectifier and cooling losses proportional to radio power (est).
BASEBAND_W = {"macro": 300.0, "indoor": 90.0}
POWER_CONVERSION_OVERHEAD = 0.12

# Quality-of-service thresholds
CONGESTION_UTIL = 0.92       # utilisation above this counts as a congested step
GUARD_UTIL = 0.80            # Circadian's emergency-wake trigger

# Demand model
VERIZON_SHARE = 0.38         # est: share of devices on campus that are Verizon subscribers
MBPS_PER_SUB = {             # busy-hour average Mbps per Verizon subscriber present
    "in_class": 0.16,        # most traffic offloaded to campus Wi-Fi indoors
    "moving": 0.70,          # walking/bus between classes: cellular-heavy
    "social": 0.42,
    "residence": 0.32,
    "venue": 0.40,           # stadium uploads/video
}

# Economics (Rutgers pilot scale; national scale lives in CFO_10K_MODEL.py)
ENERGY_PRICE_USD_KWH = 0.1663    # nj_price: EIA NJ commercial average, 2025
CAMPUS_ENERGY_PRICE_USD_KWH = 0.14  # est: Rutgers avoided cost (part self-generated)
GRID_TCO2E_PER_MWH = 0.325       # vz_scope2: Verizon 2025 location-based Scope 2 / grid MWh
TRUCK_ROLL_USD = 375.0           # truck_roll: midpoint of the $150-600 industry range
TICKET_USD = 8.01                # care_cost: Gartner (2019) cost per live-agent contact
ENTERPRISE_TICKET_USD = 65.0     # care_cost: MetricNet Level-2 ticket ($62-69)
COMPLAINTS_PER_CONGESTED_USER_STEP = 0.0015  # est: share of congested users who contact care
DR_ENERGY_USD_MWH = 250.0        # est: illustrative event energy payment
DR_CAPACITY_USD_KW_YR = 104.0    # pjm_capacity: $329.17/MW-day (2026/27 BRA), net of aggregator (est)
SLICE_PRICE_USD_HR = {           # est: illustrative list prices for campus slice-hours
    "eMBB-UL": 45.0, "URLLC": 120.0, "MC-PRIORITY": 0.0, "mIoT": 8.0,
}

# HVAC model
HVAC_W_PER_SQFT = {"mild": 0.55, "warm": 0.95, "hot": 1.35}
HVAC_SETBACK_FACTOR = 0.45
HVAC_VENT_SHARE = 0.30           # share of HVAC power that is ventilation (scales with people)
HVAC_PRECONDITION_STEPS = 6      # start conditioning 30 minutes before forecast arrival

# Cell-site batteries for demand response
SITE_BATTERY_KWH = 40.0          # est: per macro site, usable
SITE_BATTERY_RESERVE = 0.5       # keep half for outage backup (resilience constraint)

SOURCES = {
    "ran_power": "research/02_ran_energy_tech.md - massive-MIMO/small-cell power figures",
    "nj_price": "research/01_sec_forensic.md s5 - EIA: NJ commercial 16.63 c/kWh (2025)",
    "vz_scope2": "research/01_sec_forensic.md s3 - 3,335,994 tCO2e / 10.25 TWh (EY-assured 2025)",
    "truck_roll": "research/01_sec_forensic.md s5 - $150-600 per truck roll (OSP Magazine via Asentria)",
    "care_cost": "research/01 s5 + research/04 - Gartner $8.01/live contact; MetricNet L2 $62-69",
    "pjm_capacity": "research/01 s5 + research/04 - PJM BRA $269.92 / $329.17 / $333.44 per MW-day",
    "est": "Team assumption - to be measured in the Rutgers pilot",
}
