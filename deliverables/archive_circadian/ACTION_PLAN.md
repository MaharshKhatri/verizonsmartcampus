# Action plan: now → Nov 8 → Feb 3 → Mar 4

## Today, Tue Oct 20, 3–5 PM: Verizon mentor drop-in (BSC "The Cove")
Bring the dashboard on a laptop (`python3 prototype/server.py`). Ask, in this order:
1. Is the final presentation 5 or 10 minutes, and is a live demo required? (The official pages conflict.)
2. Is Verizon's AI energy saving (Samsung AI-ESM) suspended or tuned down at venues on event days? *This sizes our "event-safe" lever.*
3. Which carriers are on the SHI Stadium DAS, and is there Verizon 5G UW or mmWave in the bowl?
4. Would Verizon Business treat "occupancy intelligence + HVAC shared savings + slices" as an E&PS product? Who prices slices / On Site 5G?
5. Is aggregate per-building device counting (k ≥ 20) something Verizon's privacy team would consider "aggregate customer information" under § 222(c)(3)?

## Oct 21–30: data and access
| Owner | Ask | Why |
|---|---|---|
| Faculty sponsor (ECE) | COSMOS / WINLAB account; time on the Weeks Hall private-5G domain | Measure real cell sleep/wake latency (replaces our 5–15 min estimate) |
| Rutgers OIT | Hourly Juniper Mist association counts for 5 buildings (Hill, ARC, BSC, LSM, Weeks), 4 weeks | Replace the synthetic history; train the forecaster on real data |
| Rutgers DOTS | TripShot / Academy bus feed (GTFS-RT or AVL export), passenger counts if available | Real lead indicator |
| Rutgers IP&O / Energy | Current utility spend, BMS vendor per building, which buildings have VAV | Lighthouse building list; update the 2021 $60M figure |
| Registrar | Seats scheduled per building per period (aggregate) | The timetable prior |

## Sat Oct 31: Michigan at SHI, 12:30 PM kickoff (the only home game before the deadline)
- Two people, two phones (one Verizon): speed test + signal (RSRP/SINR via a field-test app) every 15 minutes from 9:30 AM at Busch Student Center, the bus lane, the gates and in the bowl; log time and location.
- Film ingress for the video's first 7 seconds; film the bus lane.
- Note where service degrades and when. This is primary evidence for "Impact: criticality".

## Nov 1–8: video
- Lock the script (`deliverables/NOV8_VIDEO_PITCH_SCRIPT.md`), record the dashboard demo, edit, caption every number.
- Check every number against `RESEARCH_DOSSIER.md` §3 "Safe to say".
- Follow the competition's "Guidelines for Responsible AI Use" PDF (disclose AI-assisted tooling as required).
- Submit by **Sun Nov 8, 11:59 PM**.

## Nov 9 – Feb 3: poster showcase (Wed Feb 3, 6–9 PM, The Cove)
- Retrain on real Mist counts; publish forecast error vs persistence and timetable on real data.
- Run the planner against measured wake latency from COSMOS.
- Poster panels: (1) problem + rhythm map, (2) one forecast / three paychecks, (3) frontier chart (energy vs congestion), (4) game-day evidence (Oct 31 + Nov 14 data), (5) 10-K ledger, (6) privacy architecture. Live dashboard on a laptop next to it with the chaos buttons.
- Mid-December: when business teams are assigned, hand them `FINANCIAL_PROJECTION.md` and the pricing questions in §5 of the dossier.

## Feb 4 – Mar 4: finals (Thu Mar 4, 6–9 PM)
- A 5-building lighthouse proposal with IPMVP M&V plan and a Verizon-funded 90-day budget (~$350k estimate).
- Rehearse the Q&A bible until every answer is under 30 seconds.
