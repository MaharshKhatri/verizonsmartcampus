# Field kit: Michigan at SHI Stadium, Sat Oct 31, 12:30 PM kickoff

**Why this matters:** primary data is the one thing a competitor's LLM cannot invent. Even 3 hours of careful measurements gives the video and the poster something real. It also gives our forecaster and planner their first real numbers. This is the only home game before the Nov 8 deadline; Nebraska (Nov 14) and Michigan State (Nov 28) are follow-ups for the Feb 3 poster.

## What to measure (all aggregate, no personal data)
| Measurement | Tool | Every |
|---|---|---|
| Signal: RSRP, RSRQ, SINR, band, cell ID/PCI, 5G or LTE | Android: "Network Cell Info Lite" or "NetMonster" (export CSV); iPhone: Field Test Mode (`*3001#12345#*`, screenshot) | 5 min |
| Throughput + latency | Speedtest by Ookla or the Verizon-agnostic "Fast.com" (screenshot or app history export) | 15 min |
| Crowd estimate where you stand | Count people passing a line for 60 s, or photo + later count (no faces needed) | 15 min |
| Wi-Fi: SSID visible, can you connect, speed | Same speed app on Wi-Fi | 30 min |
| Bus: route, crowding (empty / seats / standing / full), wait time | Notes + TripShot screenshot | each ride |
| Notes: "app failed", "ticket wouldn't load", "message didn't send" | Notes app with timestamps | when it happens |

Use at least one **Verizon** phone and, if possible, one phone on another carrier as a control. Put phones in the same pocket position each time, and don't measure while plugged in.

## Where and when
| Time | Place | Why |
|---|---|---|
| 9:30–10:30 | Busch Student Center, Busch bus hub | Baseline before the crowd |
| 10:30–11:45 | Lots near the stadium (tailgating), shuttle stops | Crowd building outdoors |
| 11:45–12:30 | Gates, concourse | Ingress peak: the critical window |
| 12:30–14:00 | In the bowl: student section and one other section | Peak load; halftime surge around 13:45–14:05 |
| Final whistle → +45 min | Exits, bus lane, Busch hub | Egress surge |

## Data sheet (CSV columns)
`timestamp, location, lat, lon, phone_carrier, tech(5G/LTE), band, rsrp_dbm, rsrq_db, sinr_db, down_mbps, up_mbps, latency_ms, crowd_count_60s, wifi_ok(y/n), notes`

Save as `field_data/2026-10-31_shi.csv` (one file per phone is fine; add a `phone` column). Then run:

```bash
python3 scripts/analyze_walktest.py field_data/2026-10-31_shi.csv
```

It prints a summary by location and time window and writes `field_data/2026-10-31_shi_summary.md`.

## Ethics and rules
- Measure your own phones only. No packet capture, no other people's data, no photos of faces.
- Follow stadium rules; don't block aisles or gates.
- Say "student research project, connectivity measurements" if asked.
- Report results honestly, including "no problems observed". A null result is still evidence.

## Film for the video at the same time
- 7-second establishing shot of the crowd entering (no identifiable faces in close-up).
- A screen recording of one speed test at the gate during ingress.
- The bus lane after the game.
