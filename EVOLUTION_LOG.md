# Evolution Log

Each generation records what changed and why, so the next one can attack it.

## Generation 0: reconnaissance (2026-10-20)
- Four parallel research agents (SEC forensic, RAN/MEC architect, Rutgers campus ops, go-to-market) wrote `research/01–04`.
- **The original brief was partly wrong:** SG&A is $33.8B (not $30.4B), cost of services $27.8B (not $28.5B), opex $108.9B (not $106.0B); the "$1.8B RAN electricity" claim is unsupported (Verizon's *total* electricity ≈ $0.9–1.4B, estimate); the "June 2026 AI mandate" and the Enersponse program could not be found; SHI capacity is 52,454; classes are 30 minutes apart; buses are Academy/TripShot.
- **The competition is real** and the dates check out, but the video is **2 minutes**, the official rubric weights Impact 30 / Presentation 30, and Pillar 3 is officially "Next-Gen Products & Services to Enhance Customer Experience".
- **Verizon already runs AI sleep modes** (Samsung AI-ESM, 15% average) with "over $200 million of energy savings". T-Mobile Dynamic CX already uses public event data for capacity. Whitespace: *private* campus context, used for energy and HVAC.

## Generation 1: tournament, synthesis, build (2026-10-20)
- 13 theses scored (`IDEA_LEADERBOARD.md`). Seed A (EcoSlice) led on paper; the Grand Unified Thesis **Circadian** merged A + D (network-as-sensor HVAC) + G (intent slicing) + triage.
- Built the twin (15 zones, real coordinates and timetable), context forecaster, latency-aware planner with 5 sleep modes (savings from research/02), HVAC, demand response, triage, slicing, ledger, dashboard, server, CFO model, tests.
- **Calibration lesson 1:** first runs showed 77% radio savings, far above Verizon's real 15%. The cause was over-provisioning and over-deep sleep factors; we re-grounded power and savings in published per-mechanism values.
- **Calibration lesson 2:** a weak "reactive thresholds" baseline made context look worth 30%. We replaced it with a **traffic-history AI baseline using the same planner, radios and guard**, so only the forecast differs. Result: on ordinary days context adds ~1% energy. Radio energy was demoted from headline to supporting proof; the B2B product became the money.
- **Bug found and fixed:** the planner aborted SLA-guard wakes because the forecast still said "empty". Added a measured-load floor (never plan below measured demand).
- **Evidence retracted:** a "7,861 congested user-minutes on game day" result was an artifact. A slice rejection had removed a reservation; once fixed, both AIs keep the regular game uncongested because 2–3-hour ingress is slow enough for the guard. Replaced by robust results:
  - one-off weeknight arena event: today's AI congests ~4,000 user-minutes **at any safety margin**; Circadian 0 *(superseded in Gen 2: operators use event mode, so the honest gap is energy, not congestion)*;
  - snow day: +3.6% energy;
  - 30-min demand forecast error 1.5–1.8% vs 2.3–3.9% (snow day 1.8% vs 45.5%).
- CFO base case (Gen 1, superseded): 2031 revenue ≈ $66M, EBITDA ≈ $26M; bull ≈ $168M; 5-yr NPV ≈ $10M (≈ $260M with terminal value).

## Generation 2: red-team audit and fixes (2026-10-20)
An independent red-team agent audited the code, the experiment design and the CFO model (read-only; it ran its own experiments). Findings and what changed:

| # | Finding | Severity | Fix in Gen 2 |
|---|---|---|---|
| W1 | Event-day claim compared against a strawman (no event mode, fixed margin vs Circadian's learned margins); fragile to one parameter | critical | Baseline is now **traffic-history AI + the operator's manual event mode + its own margin bandit**. New claim: same quality, more event-day energy saved (game day 65% vs 58% venue radio energy; arena 82% vs 78% with 0 vs 72 congested user-min) |
| W2 | "The network is the sensor" was really Wi-Fi-grade data; Verizon-only sensing loses to the timetable | critical | Explicit two-source sensing model (Wi-Fi 80% coverage indoors, blind in the bowl; carrier 38% share with 30% neighbour spill). Ablation: Wi-Fi ~2.2–2.4% error, carrier-only ~11–13%, timetable 3.6–5.0%. Pitch now says Wi-Fi is the primary indoor sensor; Verizon adds venues and outdoors |
| W3 | Prior was the noise-free generator; skill table omitted strong simple baselines | high | Truth adds a fixed per-building seats-vs-people gap, ticket sales differ from forecasts, organiser crowd estimates are low. Skill tables add the history AI and a no-learning "timetable × ratio" rule (2.8% vs model 2.7%): the value is the data, not the model |
| W4 | HVAC comfort metric could not fail; savings came from ventilation; baseline had no weekend/closure schedule | high | Comfort scored against ground truth incl. a 15-min recovery window; facilities timetable gets weekend, closure and finals schedules; a no-forecast controller is reported alongside. Result: forecast ≈ comfort, ventilation ≈ kWh |
| W5 | NPV lived in pull-through and terminal value; costs missing; double count; calibration display-only | high | Added integration $150k (50% billed), OT security, M&V $35k, data licences, $0.5M privacy program, 5% churn; removed engineering-hours double count; terminal value ends shared-savings fees after 5 years; simulator calibration now drives the model; software-only NPV reported (−$4.1M). Base 5-yr NPV +$3.4M, P(NPV>0) 58% |
| W6 | Why Verizon vs Lambent/Cisco/Mist; who owns BMS integration | high | Answered in the Q&A bible: ingest Mist, Verizon adds venue counts + network SLA + RAN loop; BMS via the campus's integrator |
| W7 | Bus feed derived from future truth and adds nothing | medium | Ablation shows zero effect; claims about buses removed |
| W8 | Triage results rest on assumed probabilities and one draw | medium | 2,000-storm Monte Carlo (37% dispatches avoided, no gain in 19%); robustness of diagnosis to mis-specified likelihoods (82%); claims labeled as assumption-driven |
| W9 | Day mix over-counted snow days and dropped negative days | medium | Honest campus-year mix incl. negative days → +0.3% radio energy |
| W10 | Several tests could not fail | low | Tests now assert the event-mode trade-off, ordinary-day tie, comfort vs a no-forecast controller, sensing behaviour, and a ledger built from components |

Also added in Gen 2: Circadian blends traffic history into its forecast when the calendar says a zone's day is ordinary (removed a small ordinary-day penalty); suppressed privacy counts are used as upper bounds; venue Wi-Fi is treated as non-representative; tailgaters don't trigger stadium HVAC.
