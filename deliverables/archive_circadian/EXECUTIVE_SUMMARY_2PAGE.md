# CIRCADIAN: one campus forecast, three paychecks
**Rutgers School of Engineering · 2026–27 Verizon Smart Campus Innovation Challenge · Lead pillar: Cost & Sustainability Transformation**

## The problem
Campuses run on a rhythm (class changes every 80 minutes, 70,000 daily bus riders, 52,454 fans on game day), but their buildings and networks run on fixed schedules. Rutgers spends about **$60M a year on energy**, and heating, cooling and ventilation are **~61%** of education-building energy (CBECS 2018). Buildings ventilate for crowds that left; stadium radios are either asleep or locked "on" for hours around an event.

Verizon has already attacked its side: AI sleep modes have produced "**over $200 million of energy savings**" (CEO Dan Schulman, Apr 2026), with 15% average savings in Samsung/Qualcomm field tests. That AI learns from traffic history. On event days operators protect quality with a manual "event mode" that switches energy saving off around the venue for hours.

## The insight
A campus already has the data to predict itself: the registrar timetable, the event calendar, and **counts of connected devices**, per building, from its own Wi-Fi (12,550 Juniper Mist access points at Rutgers) and, where Wi-Fi can't see (stadium bowl, arena, outdoors), from Verizon's network. Aggregated and k-anonymised, those counts become one 30-minute occupancy forecast that is worth money to three parties.

## The solution
| Who | What Circadian does | Pillar |
|---|---|---|
| **The campus pays** | Occupancy intelligence; ventilation by headcount and comfort-safe setback (pre-condition before arrivals); PJM demand response; guaranteed network slices, sold by Verizon Business | 2, 3 |
| **Verizon saves** | Its AI energy saving no longer needs a blanket event mode: it pre-wakes venue radios before the crowd and keeps saving the rest of the time. Intent-aware triage runs remote fixes before a truck rolls | 1, 2 |
| **Students win** | Quiet-study and crowd navigator, "busy in 30 minutes" alerts, guaranteed service at events, rooms that are comfortable when people are actually in them | 3 |

**Architecture.** Device counts are aggregated per building per 5 minutes and suppressed below 20 devices (aggregate customer information under 47 U.S.C. § 222(c)(3)); nothing per device leaves either network. A forecaster and latency-aware planner run as an O-RAN Non-RT RIC rApp issuing A1 energy-saving policies; triage uses the TS 28.541 energy-saving state; slices map to TS 23.501 SST/5QI and CAMARA APIs; the HVAC loop speaks BACnet to the campus BMS through its integrator.

## Evidence from our working prototype
A digital twin of 15 Busch and Livingston zones (Rutgers' real timetable, landmarks and bus routes). **Today's practice** = a traffic-history AI with learned safety margins **plus manual event mode**. Circadian uses the **same planner, radios, SLA guard and margin learner**; only the forecast differs.

| Result (simulated, 8 scenarios) | Today's practice | Circadian |
|---|---:|---:|
| Game day at SHI: venue radio energy saved · congestion | 58.1% · none | **65.3%** · none |
| One-off weeknight arena game: venue energy · congested user-minutes | 77.7% · 72 (without event mode: 5,650) | **82.0% · 0** |
| Snow day (classes cancelled): extra radio energy | — | **+2.5%** |
| Ordinary days: extra radio energy | — | **tie** (−0.6% to +0.2%) |
| 30-min demand forecast error, % of zone peak (snow day) | 2.2–3.8% (44%) | **1.9–2.2% (2.2%)** |
| HVAC vs facilities timetable · people left in setback or recovering | — · 70–19,858 people-steps | **−6.5 to −13.1% · 0–182** |
| Fault storm, 2,000 draws: dispatches per 7 faults · restore time | 5.7 · 1,241 min | **3.6 · 620 min** |

**What the ablations taught us (and changed in the pitch):** Wi-Fi is the primary indoor sensor; Verizon-only counts are worse than the timetable indoors (12% vs 4–5% error) but are the only working sensor in the stadium. HVAC kWh come almost entirely from ventilation by headcount; a no-forecast controller saves slightly more but leaves 2,500–93,000 people-steps uncomfortable, so the forecast buys **comfort-safe** setback. A simple "timetable × today's ratio" rule is nearly as accurate as our learned model: the value is the campus data, not model complexity. The bus feed added nothing and is no longer claimed.

## Business case (CFO_10K_MODEL.py; estimates labeled)
**Rutgers lighthouse:** 5–10% of HVAC energy = **$1.8–3.6M/yr** saved; Verizon earns **$0.9–1.3M/yr** ($0.02/sq ft platform + 20% of verified savings); Rutgers nets $0.9–2.3M/yr before PSE&G incentives and demand response.

**National base case:** ~120 campuses live by 2031 (universities, hospitals, corporate campuses), after churn.
| 10-K line | 2031 |
|---|---:|
| Operating revenue, Business segment (E&PS) | **+$56.6M** |
| **EBITDA** (after delivery, platform, M&V, data licences, privacy program, sales) | **+$20.7M** (bear −$3.0M · bull +$140.8M) |
| 5-year NPV at 7% | **+$3.4M**; IRR 18%; payback 52 months; +$54M with terminal value |

**What we don't claim.** Context adds only **~0.3%** radio energy over a campus year, because ordinary days tie; the network benefit is event-day efficiency without manual event mode. Software alone has a 5-year NPV of **−$4.1M**: the case needs Verizon's network pull-through (event slices, Frontline, On Site 5G), which is the first number to validate. Monte Carlo: P(NPV > 0) = 58%. It is a fundable pilot and a growth line for E&PS (revenue −$684M in 2025), not a moonshot.

## Why it can win, and why it's feasible
- **It works at the network layer** (O-RAN RIC, 5G energy-saving states, slicing, Frontline). Past winners were apps.
- **It is built and tested:** a zero-dependency Python engine and dashboard with 31 automated tests. An independent red team audited it, and we retracted two of our own claims (see EVOLUTION_LOG.md).
- **The pilot path uses Rutgers assets:** the Weeks Hall private-5G pilot factory, COSMOS/WINLAB O-RAN radios, Juniper Mist counts, the existing BMS.

## Our asks
1. A Verizon read on how event mode is run today and on slice / On Site 5G pricing (it decides the business case).
2. Introductions to Rutgers OIT (Mist counts), IP&O (BMS, utility data) and a faculty sponsor for COSMOS.
3. A 90-day, 5–10-building lighthouse with IPMVP measurement and verification (~$350k, estimate).
