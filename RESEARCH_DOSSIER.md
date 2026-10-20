# Research Dossier: Verizon Smart Campus Innovation Challenge 2026–27

**Status:** Generation 1 (2026-10-20). Synthesizes four parallel research passes:

| File | Agent | Scope |
|---|---|---|
| [`research/01_sec_forensic.md`](research/01_sec_forensic.md) | SEC forensic | FY2025 10-K, Q1/Q2 2026 10-Qs, call transcripts, ESG data, unit-cost benchmarks |
| [`research/02_ran_energy_tech.md`](research/02_ran_energy_tech.md) | 5G/MEC architect | RAN power, sleep modes, O-RAN, vendors, slicing, PJM, CPNI |
| [`research/03_competition_and_rutgers.md`](research/03_competition_and_rutgers.md) | Rutgers campus ops | Competition rules, rubric, past winners, WINLAB/COSMOS, campus facts |
| [`research/04_market_and_gtm.md`](research/04_market_and_gtm.md) | Go-to-market | TAM/SAM/SOM, competitors, pricing, DR economics, care costs |

**Rule:** a number goes on a slide only if it is in §3 "Safe to say", or if it is in a research file with a source URL and labeled VERIFIED. Estimates are always called estimates.

---

## 1. The competition (verified on the official page)

Official page: <https://soe.rutgers.edu/smart-campus> ("The 2026 Verizon Smart Campus Innovation Challenge", Verizon with the Rutgers School of Engineering, third Rutgers cycle).

| Item | Verified fact |
|---|---|
| Round 1 | **2-minute video**, due **Nov 8, 2026** |
| Round 2 | Poster showcase **Wed Feb 3, 2027, 6–9 PM**, Busch Student Center "The Cove" |
| Round 3 | Final presentations **Thu Mar 4, 2027, 6–9 PM**, same building. Top 3 later present "to Verizon and University leadership at a Verizon location" |
| Mentor drop-in | **Tue Oct 20, 2026, 3–5 PM**, BSC "The Cove" (optional one-on-one with a Verizon mentor) |
| Mid-December | Business teams assigned |
| Pillars (use the official wording) | 1. AI-Driven Automation & Efficiency · 2. Cost & Sustainability Transformation · 3. **Next-Gen Products & Services to Enhance Customer Experience** |
| Round 1 rubric (95 pts) | **Impact 30** (significance 10, ubiquity "how many people does it impact?" 10, criticality 10) · Feasibility 15 (real-world, cost-effective, scalable) · Content 15 (comprehensive, researched, **complexity = "incorporation of Verizon network technologies"**) · Creativity 5 · **Presentation 30** (organized, engaged, clarity) |
| Prizes / eligibility | $500 per finalist team; $3,000 to each top-3 team. Rutgers undergrads; at least 2 engineering students per team |
| Open questions for the mentor | Final talk is 10 minutes on one page and 5 on another; old guidelines say no demo needed, 2026 FAQ asks for one |

**Past winners were consumer apps:** UNIVIEW (parking/study-space cameras), AccessED (AR captioning), RUNetworking (course planner) in 2024–25; AeroBin (smart bins), SafeRoute (safety routing), an AR stadium-stats app in 2025–26. None operated at the network layer.

## 2. Verizon ground truth (FY2025 10-K filed 2026-02-17; 2026 10-Qs)

| Line (US$) | FY2025 | FY2024 |
|---|---:|---:|
| Total operating revenue | **138.2B** | 134.8B |
| Consumer / Business revenue | 106.8B / 29.1B | 102.9B / 29.5B |
| Enterprise & Public Sector revenue | **13.5B** (−4.8%) | 14.2B |
| Cost of services | **27.8B** | 28.0B |
| Cost of wireless equipment | 29.0B | 26.1B |
| SG&A | **33.8B** (incl. ~$1.7B severance) | 34.1B |
| Total operating expenses | **108.9B** | 106.1B |
| Adjusted EBITDA | **50.0B** | 48.8B |
| CapEx | 17.0B (2026 guide **16.0–16.5B**) | 17.1B |
| Debt (6/30/2026, post-Frontier) | total 165.2B; long-term 143.4B; net unsecured 128.7B (2.5x) | — |
| FWA subscribers | 6.2M (6/30/2026) | — |

Note: from Q1 2026 Verizon stopped reporting E&PS / Business Markets / Wholesale revenue separately.

### Corrections to the original brief (do not repeat these)
| Brief said | Truth | Source |
|---|---|---|
| Opex ~$106.0B | $108.9B ($106.1B was FY2024) | 4Q25 EX-99 |
| Cost of services ~$28.5B | $27.8B | same |
| SG&A ~$30.4B | $33.8B | same |
| Wireless equipment cost ~$25B | $29.0B ($25.5B is equipment *revenue*) | same |
| LTD ~$139B "post-Frontier" | $139.5B was pre-close; $143.4B at 6/30/26 | 2Q26 EX-99 |
| "300+ data signals per customer" | "the 300-plus different **ways** we can look at you" (Bloomberg Tech, Jun 4 2026) | CX Dive |
| "June 2026 AI mandate" | Not found. Real: AI stack "substantially complete … by July … fully done by November" (Q1'26 call) | transcript |
| "~75% of network electricity is RAN, ~$1.8B/yr" | Unsupported. RAN share is an *industry* figure (GSMA 73–80%). Verizon's **total** electricity ≈ $0.9–1.4B/yr (estimate) | research/01 §3 |
| CapEx $16–16.5B for 2025 | That is **2026** guidance; 2025 actual $17.0B | 4Q25 EX-99 |
| SHI Stadium "55,000+" capacity | Capacity **52,454**; record crowd 55,942 | research/03 §8 |
| 20 minutes between classes | **30 minutes** | scheduling.rutgers.edu |
| Transdev / Passio GO buses | **Academy Bus Lines** + **TripShot** since Jul 1 2026 | research/03 §6 |
| Verizon–Enersponse DR program | No source found. **Drop it** | research/01, 02 |

## 3. Safe to say on stage (fully sourced)
1. "Verizon did **$138.2 billion** in revenue in 2025; operating expenses were **$108.9 billion**: **$27.8 billion** cost of services and **$33.8 billion** SG&A."
2. "Dan Schulman set **$5 billion** of 2026 opex savings, later 'at least **$9 billion** of OpEx and CapEx savings'."
3. "Schulman: Verizon already has '**over $200 million of energy savings**' from AI in the network" (Q1'26 call, Apr 27 2026).
4. "Verizon's AI sleep-mode field tests with Samsung and Qualcomm cut energy **15% on average, up to 35% per sector**" (Feb 2025).
5. "Verizon used **11.4 TWh** of energy in 2025, ~**10.2 TWh** grid electricity: roughly **$0.9–1.4B** a year at EIA rates (our estimate)."
6. "Verizon's Q1 2026 10-Q: building and facility costs rose **$114 million**, partly from **higher utility rates**."
7. "New Jersey commercial power averaged **16.6¢/kWh** in 2025 (+14%); PJM capacity cleared at the cap, **$325–333/MW-day**."
8. "**74%** renewable electricity in 2025; Scope 1+2 down **73%** since 2019; net-zero operations by **2035**."
9. "Enterprise & Public Sector revenue fell **4.8%** to **$13.5B** in 2025."
10. "Schulman wants Verizon '**AI-native**'; AI voice agents lifted care satisfaction **1,280 bps**; 'up to **85%** of our domain issues are autonomously resolved'."
11. "Industry truck rolls cost **$150–600**; live-agent contacts **~$8** vs **$0.10** self-service (Gartner 2019)."
12. "Rutgers New Brunswick: **46,934** students, ~**70,000** daily bus riders, **12,550** new Juniper Mist access points, **52,454**-seat SHI Stadium."
13. "Rutgers spends about **$60 million a year** on energy (Climate Action Plan supplement); HVAC is **~61%** of education-building energy (CBECS 2018)."
14. "Verizon paid a **$46.9M** FCC location-privacy fine that the **Supreme Court let stand** in June 2026; our design never moves an individual location out of the network."

## 4. Network technology facts (research/02)

**Energy:** RAN ≈ 73% (GSMA) to ~80% (GSMA via Ericsson 2026) of *mobile-network* energy. 64T64R C-band AAU ≈ 1.0–1.4 kW peak, idle ≈ 55% of peak; indoor 5G small cell 28–57 W; mmWave small cell ≈ 650 W (estimate, sensitivity parameter).

**Sleep mechanisms (savings vs zero-load power):** symbol shutdown −34%; antenna muting ≈ −230 W per 64T O-RU; carrier/cell switch-off −47%; deep sleep −70%; Nokia extreme deep sleep up to −95%. Wake times: µs (SM1) to ~1 s (SM4); **no vendor publishes cell reactivation time**; our 5–15 min policy wake times are conservative estimates.

**Who already does what (the "hasn't Ericsson built this?" answer):**
- Sleep modes + AI scheduling: commercial (Samsung AI-ESM at Verizon, Ericsson, Nokia MantaRay, Huawei PowerStar). All state **RAN-internal inputs** (traffic history, live KPIs). No public evidence any of them use class timetables, transit feeds, Wi-Fi counts or BMS occupancy.
- External event context **for capacity**: T-Mobile **Dynamic CX** (June 2026, public event data); ARENA paper (2020). **Expect a judge to cite T-Mobile.**
- Our honest whitespace: (a) *private* campus data at building granularity, ahead of time; (b) using it for energy in both directions (deeper sleep, pre-wake); (c) context plausibility check for sleep-vs-fault; (d) campus HVAC + grid co-optimization. Measurable claim: **fewer misses on irregular days vs a traffic-history baseline**, not "AI saves energy".

**Standards to name:** 3GPP TR 38.864 (NR network energy savings), TS 28.310 (energy efficiency management), TS 28.541 (CESManagementFunction), TS 28.312 (intent-driven management), TS 23.501 (S-NSSAI / SST, 5QI), O-RAN WG1 Network Energy Saving use cases + WG4 RF-channel ES / O-RU Deep Hibernate, GSMA NG.116 (GST/NEST), CAMARA Quality-on-Demand / Network Slice Booking, TM Forum TMF921 (intent API).

**Verizon scale:** ~**60,000 vRAN sites** (Samsung), including stadium, event and enterprise private-network small cells.

**Rutgers test infrastructure:** WINLAB/COSMOS (O-RAN 7.2x radios, srsRAN/OpenAirInterface, A100 GPUs) and a **private-5G pilot factory in Weeks Hall on Busch** (Siemens + Rutgers). Accounts need a faculty sponsor. ORBIT folded into COSMOS on Aug 1 2026.

## 5. Market and pricing (research/04)

| Item | Value |
|---|---|
| U.S. degree-granting institutions | 3,777; **488** with ≥10k students; 196 with ≥20k (NCES) |
| Hospitals | 6,100 (AHA); ~3,000 inpatient buildings >200k sq ft (CBECS) |
| Large offices | 28,000 buildings >100k sq ft (CBECS) |
| Energy $/sq ft | higher-ed utilities **$2.19** (APPA); hospitals $3.18; offices $1.63 (CBECS 2018) |
| HVAC share of energy | education 60.8%, hospitals 53.4%, offices 56.7% |
| TAM (HVAC spend acted on) | ≈ **$18.7B/yr** → savings pool $0.9–1.9B/yr (5–10%) |
| SAM revenue at recommended pricing | ≈ **$0.37–0.63B/yr** |
| Occupancy-HVAC savings evidence | 5–18% (Sentinel 17.8%, MARTINI 8–11%, UBC ~5%); PNNL: sensor cost is why occupancy controls often fail to pay off; **we remove the sensor** |
| Competitors | Siemens **Lambent Spaces** (software-only Wi-Fi analytics, biggest threat), Cisco Spaces, Juniper Mist location, Occuspace/Waitz ($0.105–0.15/sq ft/yr sensors), Density, Butlr |
| PJM capacity | $269.92 (25/26), $329.17 (26/27), $333.44 (27/28), $325 (28/29) per MW-day; ~**$104/kW-yr**; from 2027/28 enrolled load must be available all hours |
| Care costs | L1 ticket $22, L2 $62–69 (MetricNet); live contact $8.01 (Gartner 2019) |
| Competitor slices | T-Mobile T-Priority $7.50/mo; SuperMobile $42/line |

**Recommended packaging (one contract, four layers):** (1) occupancy intelligence **$0.02–0.03/GSF/yr**; (2) occupancy-driven HVAC, **Verizon keeps 20% of verified savings** (IPMVP M&V); (3) demand response with an incumbent curtailment service provider, **15% of value**; (4) network SLA: Frontline slice at catalog price, event-day slices, On Site 5G for labs/hospitals.

**Rutgers lighthouse:** $60M energy × 60.8% HVAC × 5–10% = **$1.8–3.6M/yr** savings; Verizon revenue **$0.9–1.3M/yr**; Rutgers nets **$0.9–2.3M/yr**. PSE&G pays up to $1.00/kWh saved for HVAC controls (capped at 60% of project cost).

## 6. Privacy and law (design constraint, not an afterthought)
- **47 U.S.C. § 222(c)(3)** lets carriers use and disclose **aggregate customer information** ("collective data … from which individual customer identities and characteristics have been removed"). Per-building, per-5-minute device *counts* qualify; per-device trajectories do not.
- April 2024: FCC fined the four carriers ~$196M for location-data sharing (Verizon **$46.9M**); **June 4 2026** the Supreme Court (*FCC v. AT&T*, consolidated with *Verizon v. FCC*) let the fines stand.
- Our design: counts are aggregated inside the network, suppressed below **k = 20** devices (the twin's `K_ANON_FLOOR`), never exported per device; campus Wi-Fi counts come from the university's own Juniper Mist controller under the university's policy.

## 7. Rutgers facts for the digital twin (research/03)
- Standard course periods (80-min classes, Mon–Fri): 8:30, 10:20, 12:10, 2:00, 3:50, 5:40, 7:30, 9:20; **30-minute** class-change windows.
- SHI Stadium 52,454 seats; 2025 average 48,459; remaining 2026 home games: **Michigan Sat Oct 31 12:30 PM** (only one before Nov 8), Nebraska Nov 14, Michigan State Nov 28.
- Rutgers OIT: ~110,000 wireless devices daily; 12,550 Juniper Mist APs; RUWireless shuts off early Jan 2027 (move to eduroam) – irrelevant to AP association counts, which are SSID-agnostic.
- Energy assets: 17.1 MW Busch cogeneration plant; 8 MW Livingston solar canopy + 14.5 MW DSD carports; carbon neutral target 2040; ~470,000 tCO₂e/yr.
- Public safety: RUPD + RUSSECC PSAP; ENS SMS alerts; 295 new blue-light phones.
- Coordinates for 28 landmarks: research/03 §4 (OpenStreetMap).

## 8. What is still unverified (do not assert; validate before Nov 8 where possible)
| Gap | How to close it |
|---|---|
| Building-level cellular dead zones on Busch/Livingston | Walk test (RSRP/SINR screenshots, speed tests) at Hill, ARC, Livingston dorms |
| Which carriers are on an SHI Stadium DAS; any Verizon stadium 5G | Ask the Verizon mentor; measure at the **Oct 31 Michigan game** |
| Whether operators suspend AI energy saving on event days | Ask the Verizon mentor (this sizes the "event-safe" lever) |
| Rutgers current utility spend (the $60M is from 2021) | Ask Rutgers IP&O / Energy office |
| TripShot / Academy bus API or GTFS-RT | Ask Rutgers DOTS for a data-sharing agreement |
| Juniper Mist occupancy API access | Ask Rutgers OIT (Mist has location/occupancy analytics) |
| Private 5G and slice pricing | Verizon Business conversation |
| Cell reactivation latency | Measure on COSMOS / Weeks Hall private 5G |
