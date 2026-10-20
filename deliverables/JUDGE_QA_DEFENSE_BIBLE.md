# Judge Q&A Defense Bible

25 questions Verizon judges are likely to ask, with answers that hold up. Sources: `RESEARCH_DOSSIER.md` (facts), `FINANCIAL_PROJECTION.md` (model), `prototype/out/evidence.json` and `sim_kpis.json` (simulation). **How to answer:** give the number, say where it comes from, then say what we don't know. Judges reward calibrated answers more than confident ones. Several of these answers exist because our own red team broke an earlier claim (EVOLUTION_LOG.md).

---

## A. Strategy and "why Verizon"

**1. "Verizon already saves 'over $200 million' with AI sleep modes. What's new?"**
We agree, and we tested against it. Our baseline is a traffic-history AI with learned safety margins plus the operator's manual event mode. With the same planner, Circadian **ties on ordinary days** (−0.6% to +0.2%). Its value is on irregular days. On game day, event mode keeps venue radios on for six hours; Circadian pre-wakes them and saves **65% of venue radio energy vs 58%** with the same zero congestion. At a one-off weeknight arena game it saves 82% vs 78% with 0 vs 72 congested user-minutes. On a snow day it saves 2.5% more. Over a campus year that is only **~0.3%** of radio energy, so we don't sell this as an energy program for Verizon. We sell it as event-day efficiency without manual event mode.

**2. "T-Mobile's Dynamic CX already uses event data."**
It uses *public* event information for *capacity*. We use *private* campus data (registrar timetable, room bookings, BMS and Wi-Fi counts) under a customer contract, for energy, capacity *and* buildings. The data partnership comes with a paying customer; that is the moat, not the algorithm.

**3. "Siemens Lambent, Cisco Spaces and Juniper Mist already sell Wi-Fi occupancy. Why buy from Verizon?"**
Honestly, indoors **Wi-Fi is the better sensor**: in our ablation, Verizon-only counts are worse than the plain timetable indoors (12% vs 4–5% error), while Wi-Fi counts score about 2%. Verizon adds three things Wi-Fi vendors can't: (a) counts where Wi-Fi is blind (stadium bowl, arena, outdoors), where Wi-Fi-only forecasting fails; (b) the network SLA in the same contract (event slices, Frontline for RUPD, On Site 5G); (c) the RAN energy loop. If Rutgers already licenses Mist analytics, we ingest it.

**4. "Which pillar is this?"**
We lead with **Pillar 2, Cost & Sustainability Transformation**, and show it is AI-native (Pillar 1) and customer-facing (Pillar 3, Next-Gen Products & Services to Enhance Customer Experience), because one forecast drives all three.

**5. "Why does this need 5G at all?"**
Guaranteed QoS needs slicing (S-NSSAI/5QI), which campus Wi-Fi can't sell; stadiums and outdoor areas are cellular; the venue headcount comes from the carrier side; and the energy loop runs in Verizon's radios.

## B. Technical

**6. "How do you know which building a phone is in?"**
We don't track phones. We use *counts* per zone: Wi-Fi association counts per building from the campus controller, and carrier counts per sector or small cell. Carrier attribution leaks into neighbouring buildings; we model 30% spill indoors, which is why indoors we use Wi-Fi and use carrier counts only where Wi-Fi is blind. Each raw count below 20 devices is suppressed; a suppressed count is still used as an upper bound ("fewer than 20 devices").

**7. "What does the forecaster do, and does the ML matter?"**
A ridge regression per building type and horizon (5–60 min) on context features: the timetable/event prior, the current count, today's deviation from the prior, a short-term trend, and a bus-arrival feature that turned out to add nothing. It is retrained nightly; P90 comes from empirical residuals. 30-minute error on a weekday is 2.7% of zone peak vs 6.9% for persistence and 5.0% for the timetable alone. A simple rule (timetable × today's observed ratio) scores 2.8%, nearly as good. **The value is the campus data, not the model.** We keep the learned model because it is better on event days and gives calibrated P90s.

**8. "A sleeping radio can't serve a crowd instantly."**
That is why the planner is latency-aware. Each sleep depth has a wake time (5–15 min in our conservative model; no vendor publishes cell reactivation time), and a radio may enter a sleep state only if the P90 forecast says it won't be needed before it could wake. A measured-load floor (never plan below what the radios measure now) and an SLA guard wake capacity immediately when the forecast is wrong.

**9. "What happens when the forecast is wrong, e.g. an unannounced rally?"**
The guard and floor handle crowds that build over minutes: in the unannounced 2,500-person rally scenario, nobody was congested. What no guard fixes is a forecast that is confidently wrong for an hour, which is why operators use event mode today. Per-zone safety margins are learned by a bandit (UCB1); the baseline gets its own identical bandit, so the comparison is fair.

**10. "Isn't your simulation circular?"**
Partly, and here is how we limit it. Truth includes things the model never sees: a fixed per-building gap between seats scheduled and people present, random daily attendance, AR(1) noise, unannounced crowds, ticket sales that differ from the forecast, and sensor noise and misattribution. Training and test days use different seeds. The headline comparison holds the planner, guard and margin learner fixed and swaps only the forecast. Our red team still found two claims that were artifacts, and we retracted them (a game-day congestion gap and HVAC comfort scoring). The twin is a design tool; the pilot replaces it with real counts.

**11. "Which standards does this touch?"**
3GPP TR 38.864 (NR network energy savings), TS 28.310 (energy-saving management), TS 28.541 (CESManagementFunction, so the NOC knows a cell is asleep on purpose), TS 28.312 (intent-driven management), TS 23.501 (S-NSSAI SST, 5QI); O-RAN WG1 network energy-saving use cases (Non-RT RIC rApp + A1 policy) and WG4 RF-channel sleep; GSMA NG.116; CAMARA Quality-on-Demand / Network Slice Booking; TM Forum TMF921.

**12. "Where does it run?"**
The forecaster and planner run as a Non-RT RIC rApp (decisions on a minutes scale, A1 policies to Verizon's Samsung vRAN), with an SMO-level ops add-on for triage. The HVAC loop sends BACnet setpoint schedules to the existing BMS through the campus's integrator. MEC is optional.

**13. "How does triage avoid truck rolls?"**
Energy-saving state is already standard (TS 28.541), so a sleeping cell opens no ticket. We add a context plausibility check ("cell dark *and* a class lets out in 10 minutes ⇒ probably a fault"). We also add a naive-Bayes diagnosis over six symptoms with remote playbooks (restart, config rollback, beam re-weight, reroute), and cell-outage compensation plus a dispatch with the right part for hardware faults. Over 2,000 simulated fault storms: **5.7 → 3.6 dispatches per 7 faults (37% avoided)**, restore time 1,241 → 620 minutes; **no gain in 19% of storms**. Diagnosis accuracy is 84% (82% when real symptom rates differ from our table by ±0.15). The dispatch probabilities are assumptions, not Verizon data.

**14. "Plain-English slicing sounds like a toy."**
The parser outputs a standards-shaped profile (SST, 5QI, window, bandwidth, area) and checks it against forecast crowd demand plus other reservations. It admits, counter-offers (a lower guaranteed rate at the forecast peak, full rate otherwise) or asks a clarifying question. It runs offline; the same JSON contract can be filled by an LLM.

## C. Financial

**15. "Show me the 10-K line to the dollar."**
Base case 2031: **+$56.6M Business-segment (E&PS) revenue** and **+$20.7M EBITDA**. That is after network delivery cost, platform, M&V, data licences, a privacy program and sales. Network savings inside cost of services are small (radio energy +0.3%, truck rolls) and we say so. Line by line: FINANCIAL_PROJECTION.md.

**16. "That's tiny."**
It is ~0.4% of the $5B 2026 savings program. The bull case is $141M EBITDA. It is a pilot-able product line for E&PS, whose revenue fell $684M in 2025, not a moonshot.

**17. "What's the NPV?"**
+$3.4M over 5 years at 7% (IRR 18%, payback 52 months); +$54M with a terminal value that ends shared-savings fees with their 5-year contracts and nets out churn. Monte Carlo over every assumption gives P(NPV > 0) = 58% (P10 −$7.8M, P90 +$13.4M). Adoption and network pull-through drive it.

**18. "So it only works if Verizon sells network services on top?"**
Yes, and we say so: software alone has a 5-year NPV of −$4.1M. Pull-through (event slices, Frontline lines, On Site 5G for labs and hospitals) at $250k per customer per year is an **estimate**, and it is the first number to validate with Verizon Business. The strategic point is that a campus energy deal opens the door for E&PS connectivity sales.

**19. "Why would Rutgers pay?"**
$60M energy × 60.8% HVAC × 5–10% savings = $1.8–3.6M/yr. After Verizon's fees ($0.58M platform + 20% of verified savings), Rutgers nets $0.9–2.3M/yr, before PSE&G incentives (up to $1.00/kWh saved, capped at 60% of project cost) and demand response. In the twin, the forecast's job in HVAC is comfort, not kWh. A controller with no forecast saves about a point more but leaves thousands of people-steps in cold or stuffy rooms. Circadian leaves 0–182 against a facilities timetable's 70–19,858.

**20. "What does the pilot cost, and what are the hidden costs?"**
~$350k (estimate) for a 90-day, 5–10-building lighthouse. The national model carries $150k integration per campus (50% billed to the customer, often covered by utility incentives), $25k OT security review, $35k/yr M&V, $10k/yr data licences, a $0.5M/yr privacy program and 5% annual churn.

## D. Privacy, law, risk

**21. "We paid a $46.9M location-privacy fine and the Supreme Court let it stand in June 2026."**
Which is why the design is aggregate-only: 47 U.S.C. § 222(c)(3) allows aggregate customer information, meaning "identities and characteristics removed". Per-building, per-5-minute counts, raw counts suppressed below 20 devices, no trajectories, nothing per device leaves the network. Indoors the work is done by the university's own Wi-Fi data under its own policy.

**22. "Could a crowd forecast be misused, e.g. to track a protest?"**
Counts are coarse (building, 5 minutes, k ≥ 20) and kept only as long as the forecast needs them. Public-safety use is limited to capacity (a priority slice), not surveillance. We would publish the data-use policy with the university.

**23. "What if you sleep a radio and someone needs 911?"**
The low-band coverage layer never sleeps (a test enforces it); only capacity layers do. Mission-critical slices are hard constraints that keep capacity awake.

## E. Execution

**24. "Can a student team actually do this?"**
The prototype is real software: a digital twin, forecaster, planner, HVAC controller, triage, slicing and a CFO model, with 31 automated tests and no dependencies. An independent red-team review made us retract two claims and rebuild the baseline. The pilot path uses Rutgers assets: the Weeks Hall private-5G pilot factory and COSMOS/WINLAB O-RAN radios (faculty sponsor needed), Juniper Mist counts (OIT), and the BMS through IP&O's integrator.

**25. "What would you do with the next 90 days?"**
(1) Walk-test and film the Oct 31 Michigan game. (2) Get 4 weeks of Mist counts for 5 buildings and replace the synthetic history. (3) Measure cell reactivation time on COSMOS. (4) Learn how Verizon runs event mode today, since that sizes the network benefit. (5) Price slices and On Site 5G with Verizon Business. (6) Turn the dashboard into the Feb 3 poster demo.
