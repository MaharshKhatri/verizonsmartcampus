# 04 · Market Sizing & Go-to-Market: Verizon "Smart Campus" (Occupancy Intelligence + Grid + Network)

*Prepared 2026-10-20 for the Rutgers team in the Verizon Smart Campus Innovation Challenge. Written from a GTM point of view (ex-Verizon Business product lead).*

**How to read this file**
- Every figure has a source. Labels used throughout:
  - **[S]**: primary or official source (EIA, NCES, AHA, PJM, SEC 10-K, Rutgers, PSE&G, Verizon).
  - **[S2]**: secondary source, such as trade press, a vendor claim or an aggregator. Treat these with care.
  - **[EST]**: our own estimate. The math is shown.
  - **[REC]**: our recommendation.
- Energy-spend baselines come from EIA CBECS 2018, the latest full commercial-buildings survey. Those are 2018 dollars, and NJ commercial electricity prices have risen since then (see §5), so spend-based figures are conservative for 2026.
- Limitation: the shared web-search budget ran out near the end of this research pass. The "Open items" section (§9) lists what could not be verified.

---

## 0. Key numbers at a glance

| Metric | Value | Label |
|---|---|---|
| U.S. degree-granting institutions (fall 2021) | 3,777 | [S] NCES |
| Institutions with ≥5,000 / ≥10,000 / ≥20,000 students | 958 / 488 / 196 | [S] NCES |
| Share of all students enrolled at ≥5,000-student institutions | 78% (14.53M of 18.62M) | [S] NCES, our arithmetic |
| U.S. hospitals / community hospitals (2024 survey) | 6,100 / 5,121 | [S] AHA |
| Education buildings, energy spend (2018) | $15.9B; $1.17/sq ft | [S] CBECS |
| Inpatient hospitals, energy spend (2018) | $7.18B; $3.18/sq ft | [S] CBECS |
| HVAC share of energy (heating + cooling + ventilation): education / inpatient / office | 61% / 53% / 57% | [EST] from CBECS end-use table E1 |
| Rutgers: floor area / annual energy spend | ~29M sq ft, 1,009+ buildings / ~$60M | [S] Rutgers |
| NJ commercial electricity, Jan–Jul 2026 YTD | 17.78¢/kWh vs U.S. 13.97¢ (+27%) | [S] EIA |
| PJM capacity prices, 2025/26 → 2028/29 ($/MW-day, UCAP) | $269.92 → $329.17 → $333.44 → $325 | [S] PJM |
| Occupancy-based control savings (simulation, national weighted) | 17.8% with people-counting sensors vs 5.9% with common sensors | [S] PNNL-22072 |
| Wi-Fi-driven HVAC savings (field) | 17.8% of HVAC electricity (Sentinel, 1 day); 8.1–10.8% chilled water in summer (MARTINI, 5 buildings) | [S] |
| Verizon Enterprise & Public Sector revenue, 2025 | $13.53B, down 4.8%; wireline down $532M | [S] VZ 10-K |
| Help-desk cost per ticket, Level 1 vs Level 2 | $22 vs $62–$69 | [S] MetricNet via HDI |

---

## 1. TAM / SAM / SOM

### 1a. Market counts (who we sell to)

| Segment | Count | Source |
|---|---|---|
| Degree-granting postsecondary institutions, fall 2021 | **3,777**. By size: 492 <200; 419 200–499; 444 500–999; 867 1,000–2,499; 597 2,500–4,999; **470** 5,000–9,999; **292** 10,000–19,999; **94** 20,000–29,999; **102** ≥30,000 | [S] [NCES Digest Table 317.40 (2022 ed.)](https://nces.ed.gov/programs/digest/d22/tables/dt22_317.40.asp) |
| ≥5,000 students | **958** institutions: 764 public, 167 private nonprofit, 27 for-profit. They enroll 14,531,822 students (78% of 18,621,073) | [S] same table; [EST] for the sums |
| ≥10,000 students | **488** institutions, enrolling 11.16M students (60%) | [S] same table; [EST] for the sums |
| ≥20,000 students | **196** institutions, enrolling 7.10M students (38%) | [S] same table; [EST] for the sums |
| R1 ("Research university, very high") | 146 institutions. 137 of them have ≥10,000 students (31 + 43 + 63) | [S] same table |
| Institutions with first-year undergraduates, AY2021–22 | 3,542 | [S] [NCES Condition of Education](https://nces.ed.gov/programs/coe/indicator/csa/postsecondary-institutions) |
| U.S. hospitals, total | **6,100**: 5,121 community, of which 3,567 are in a system; 210 federal; 907,216 staffed beds | [S] [AHA Fast Facts 2026 (2024 survey)](https://www.aha.org/statistics/fast-facts-us-hospitals) |
| Large medical campuses (proxy) | CBECS 2018 counts about 9,000 inpatient buildings, of which about 3,000 are over 200,000 sq ft (1,883M sq ft). A 2011 AHA-registry tabulation counted 315 hospitals with ≥500 beds | [S] [CBECS B6/B7](https://www.eia.gov/consumption/commercial/data/2018/bc/html/b7.php); [S2] [BMC HSR table](https://bmchealthservres.biomedcentral.com/articles/10.1186/s12913-017-2078-6/tables/2) (2011 data) |
| Corporate campuses (proxy) | No published U.S. count of office parks was found. Proxy from CBECS 2018: **28,000 office buildings over 100,000 sq ft** (7,385M sq ft), and 11,000 over 200,000 sq ft (4,973M sq ft) | [S] [CBECS B6/B7](https://www.eia.gov/consumption/commercial/data/2018/bc/html/b6.php) |
| K-12 (optional, later) | 13,318 regular school districts (2022–23, per EdWeek citing NCES); 19,186 operating districts and 99,297 schools (2023–24, NCES CCD) | [S2] [EdWeek](https://www.edweek.org/leadership/education-statistics-facts-about-american-schools/2019/01); [S] [NCES CCD](https://nces.ed.gov/ccd/tables/202324_summary_2.asp) |

### 1b. Floor area and energy spend (what the money is)

| Building type (CBECS 2018) | Floor space | Major-fuel energy spend | $/sq ft | HVAC share of energy [EST]* |
|---|---|---|---|---|
| Education (all, including K-12) | 13,623M sq ft; 437,000 bldgs | **$15,875M** | **$1.17** | 60.8% = (362+92+65)/854 TBtu |
| …of which College/university classroom-type buildings | 1,827M sq ft; 60,000 bldgs; 157 TBtu; 85.8 kBtu/sq ft | ~$2.92B [EST] = 157 TBtu × $18.59/MMBtu (education average) | — | — |
| Inpatient health care (hospitals) | 2,259M sq ft; 9,000 bldgs | **$7,182M** | **$3.18** | 53.4% = (140+28+65)/436 |
| Office (all) | 16,662M sq ft | $27,203M | $1.63 | 56.7% = (325+81+214)/1,093 |

Sources: [S] [CBECS 2018 Table C2](https://www.eia.gov/consumption/commercial/data/2018/ce/pdf/c2.pdf) (spend), [C4](https://www.eia.gov/consumption/commercial/data/2018/ce/pdf/c4.pdf) ($/sq ft and $/MMBtu), [C12](https://www.eia.gov/consumption/commercial/data/2018/ce/pdf/c12.pdf) (college subcategory), [E1](https://www.eia.gov/consumption/commercial/data/2018/ce/pdf/e1.pdf) (end use).

*HVAC share = space heating + cooling + ventilation, as a share of site Btu. It is not a dollar share. Cooling and fans are electric and cost more per Btu than gas heat, so the dollar share likely differs.

**Why CBECS understates the campus:** CBECS classifies each building by its main activity. Dorms (840M sq ft of "dormitory, fraternity, sorority" across the U.S.), labs, and central plants are counted outside "College/university." Whole-campus figures:

| Whole-campus higher-ed metric | Value | Label |
|---|---|---|
| Total campus space | ">6 billion square feet… 210,000 buildings… replacement value of $2 trillion" | [S2] [BDC Network, 2023](https://www.bdcnetwork.com/higher-education-construction-costs-2023?page=1) (original source not named) |
| Average utilities cost | **$2.19/sq ft** (APPA average, as cited in a 2019 campus report) | [S2] [Colorado College 2019 Energy Report](https://www.coloradocollege.edu/offices/facilities/energy-management/CC%202019%20Annual%20Energy%20Report%20Rev1.pdf) |
| Annual higher-ed energy spend | "about $14 billion annually on energy costs" (attributed to DOE; mid-2010s) | [S2] [Microgrid Knowledge](https://www.microgridknowledge.com/uncategorized/article/11432726/no-up-front-energy-efficiency-measure-costs-for-these-higher-ed-institutions) |
| Cross-check [EST] | 6.0B sq ft × $2.19 = **$13.1B/yr**, consistent with the ~$14B figure | [EST] |
| VAV share of college floor space | 88% of post-1980 college floor space and 49% of pre-1980 floor space has VAV systems. For hospitals the figures are 95% and 67%. VAV is the system type that occupancy-based control can actuate | [S] [PNNL-22072, Table 2.1](https://www.pnnl.gov/main/publications/external/technical_reports/pnnl-22072.pdf) |

### 1c. TAM / SAM / SOM table

| Layer | Definition | Math | Result | Label |
|---|---|---|---|---|
| **TAM: HVAC-related energy spend** in U.S. higher ed, hospitals and large offices | Annual HVAC-related energy dollars our control layer acts on | Higher ed: 6.0B sq ft × $2.19 × 60.8% = $8.0B. Hospitals: $7.18B × 53.4% = $3.8B. Offices >100k sq ft: 7,385M sq ft × $1.63 × 56.7% = $6.8B | **≈ $18.7B/yr** | [EST] |
| TAM: savings pool | Value created if occupancy-driven control saves 5–10% of HVAC energy (range from §3 evidence) | $18.7B × 5% to 10% | **≈ $0.9B–$1.9B/yr** | [EST] |
| TAM: software revenue | Price × addressable floor space (15.6B sq ft = 6.0B + 2.26B + 7.39B) | At our recommended platform price of $0.02–0.03/sq ft (§9): $0.31–0.47B. Plus a 20% performance fee on the $0.93–1.87B savings pool: $0.19–0.37B. For comparison, at Occuspace-style sensor pricing of $0.105–0.15 the platform alone would be $1.6–2.3B | **≈ $0.5B–$0.84B/yr at our recommended pricing** | [EST] |
| **SAM** | Higher ed ≥5,000 students (958 institutions) + inpatient buildings >200k sq ft + offices >200k sq ft | Higher ed: 6.0B × 78% enrollment share* = 4.68B sq ft. Hospitals: 1.88B sq ft. Offices: 4.97B sq ft. Total 11.5B sq ft. HVAC spend: 4.68B × $2.19 × 60.8% + $7.18B × (1,883/2,259) × 53.4% + 4.97B × $1.63 × 56.7%. Revenue: 11.5B × $0.02–0.03 = $0.23–0.35B platform, plus 20% × (5–10% × $14.0B) = $0.14–0.28B performance | **11.5B sq ft; ≈ $14.0B/yr HVAC spend; ≈ $0.37–0.63B/yr revenue potential** | [EST] |
| SAM beachhead | PJM states, where demand-response revenue is available, plus high-price NJ/NY | NJ commercial power 17.78¢ vs U.S. 13.97¢ (Jan–Jul 2026) | Start in NJ / Mid-Atlantic | [S] EIA; [REC] |
| **SOM (Year-3 target, not a forecast)** | 20 universities (~2% of the 958), 5 hospital campuses, 5 corporate campuses | Floor space (assumed): 20 × 4M + 5 × 1.5M + 5 × 2M = 97.5M sq ft. Platform: 97.5M × $0.03 (the <5M-GSF tier) = $2.93M. Performance fee: HVAC spend (80M × $1.33 + 7.5M × $1.70 + 10M × $0.92 = $128M) × 7% savings (assumed) × 20% = $1.80M. DR share: 30 campuses × 1 MW (assumed) × $103.7k × 15% = $0.47M | **≈ $5.2M ARR from software, grid and energy**, plus private 5G and slicing pull-through (not modeled) | [EST]; inputs marked "assumed" are ours |

*Assumes campus floor area scales with enrollment. This is unverified: large research universities carry more sq ft per student, while large online for-profits carry almost none.

**Strategic read:** On software alone this is a mid-sized market, roughly $0.4–0.6B/yr in SAM revenue at our recommended pricing. The case for Verizon is the **bundle**:
- Energy and DR savings make the campus deal fundable.
- The same deal pulls through Enterprise & Public Sector connectivity, private 5G and slicing (§4).
- It feeds the student consumer funnel (§8).
- It provides the occupancy forecast Verizon uses to sleep its own radios.

---

## 2. Rutgers specifics (the lighthouse account)

| Item | Value | Source |
|---|---|---|
| Buildings and floor area | "more than 1,009 buildings representing 29 million square feet across the state of New Jersey" | [S] [Rutgers University Facilities](https://construction.rutgers.edu/university-facilities) |
| Gross square feet (owned and leased) | ~30 million GSF | [S] [Rutgers IP&O Space Management](https://ipo.rutgers.edu/node/639) |
| Students in on-campus housing | "over 19,000 students living on-campus" | [S] same IP&O source |
| Annual energy spend | "Given annual energy expenditures of about $60 million…" (Rutgers estimates ~$20M/yr of efficiency savings for ~$80M invested, with 3–5-year paybacks) | [S] [Rutgers Climate Action Plan, Buildings & Energy WG Supplement (2021)](https://climateaction.rutgers.edu/wp-content/uploads/2026/08/EnergyAndBuildingsWG_Supplement.pdf) |
| Implied energy intensity | $60M ÷ 29M sq ft = **$2.07/sq ft**, close to the APPA average of $2.19 | [EST] |
| FY2026-27 budget | Total expense $6.12B. **"Plant Operation & Maintenance" (non-salary) = $203.95M**, of which New Brunswick $100.4M and Central $83.7M. FY2025-26: $180.27M. This line includes utilities and upkeep; it is not a utilities-only figure | [S] [Rutgers BOG FY27 budget (July 9, 2026)](https://finance.rutgers.edu/sites/default/files/2026-07/Budget-%20FY27-%20BOG%2026July09.pdf); [FY26 budget](https://finance.rutgers.edu/sites/default/files/2025-12/FY25-26%20University%20Budget_Final-BOG-Approved.pdf) |
| Building-sector emissions baseline | ~359,541 t CO2e. Natural-gas cogeneration on Busch/Livingston and the Newark RBHS campus | [S] Rutgers CAP supplement (as above) |
| Savings tiers the CAP cites (GSA) | Metering alone: up to 2%. Cost allocation: 2.5–5%. **Tune-up plus demand management: 5–15%.** Ongoing commissioning: 15–45% | [S] Rutgers CAP supplement |
| HVAC-related energy [EST] | $60M × 60.8% = **$36.5M/yr**. At 5% savings that is **$1.8M/yr**; at 10%, **$3.6M/yr** | [EST]. Assumes the CBECS education end-use mix applies; cogeneration complicates the picture |

---

## 3. Evidence that occupancy-driven HVAC saves energy (and the competitive landscape)

### 3a. Savings evidence

| Study | Method | Result | Source |
|---|---|---|---|
| **Sentinel** (UCSD/CMU, ACM SenSys 2013) | Existing Wi-Fi APs and smartphones used to infer occupancy in a commercial/campus building | Occupancy inferred correctly 86% of the time (6.2% false negatives). Actuated 23% of HVAC zones for one day and measured **17.8% HVAC electrical savings**. Cites prior sensor/camera systems at up to 42% | [S] [Balaji et al. 2013](https://www.cs.virginia.edu/~bjc8c/class/cs6501-f17/balaji13sentinel.pdf) |
| **MARTINI** (UT Austin, 2021) | Wi-Fi occupancy clustering plus smart-meter data | 5 buildings over 7 months: **8.1–10.8% chilled-water savings in summer**, 0.2–5.9% in fall. Potential across **51 academic buildings: 1–5%** | [S] [arXiv 2110.08927](https://arxiv.org/abs/2110.08927) |
| **PNNL-22072** (DOE, 2013) | Simulation of occupancy-based control of VAV terminal boxes and lighting, large office, 15 climate zones | Construction-weighted national average: **17.8% savings with advanced (people-counting) occupancy sensing vs 5.9% with common occupancy sensors**. 17–23% in climate zones 3C–8; NJ is zone 4A | [S] [PNNL-22072](https://www.pnnl.gov/main/publications/external/technical_reports/pnnl-22072.pdf) |
| PNNL / *Applied Energy* 2023 (Pang et al.) | Code-adoption cost-effectiveness study across 40 cities | Occupancy-based controls "may not be cost-effective in office and school buildings" **because of current sensor prices**. Cutting sensor cost to ~60% of current would "greatly shorten" payback. **This is our wedge: we reuse existing network data and need no new sensors.** | [S] [OSTI record](https://www.osti.gov/pages/biblio/2201287-adopting-occupancy-based-hvac-controls-commercial-building-energy-codes-analysis-cost-effectiveness-decarbonization-potential) |
| iSchedule (UMass Amherst) | HVAC schedules learned from Wi-Fi activity across 112 campus buildings | 37% less "waste time" (an energy proxy) and 3% less "miss time" (a comfort proxy) | [S2] [UMass LASS paper](https://lass.cs.umass.edu/papers/pdf/ischedule.pdf) (via search summary) |
| Portland State (EDUCAUSE 2022 session) | Wi-Fi occupancy data tied to HVAC controls | "up to 20%" lower energy in unoccupied rooms | [S2] [EDUCAUSE agenda](https://events.educause.edu/annual-conference/2022/agenda/reducing-oncampus-covid-exposure-and-energy-use-with-wifibased-occupancy-data) (page blocked; via search summary) |
| LBNL building-analytics study (2022) | Field data from thousands of buildings | FDD users: **9% median annual savings**. Energy-information-system users: 3% | [S] [Lin et al., *Energies* 2022](https://eta-publications.lbl.gov/publications/building-analytics-tool-deployment) |

**Planning assumption [REC]:** use **5–10% of HVAC energy** in financial models. That range is defensible from MARTINI, the PNNL common-to-advanced sensing range and the LBNL FDD median. Present 15–18% (Sentinel, PNNL advanced sensing) only as an upside case.

### 3b. Competitor / vendor table

| Vendor | What it does | Pricing (public, if any) | Gap vs our concept | Source |
|---|---|---|---|---|
| **Occuspace / Waitz** | Sensors that count nearby Bluetooth and Wi-Fi signals (one sensor per 2,500–5,000 sq ft, ~90% accuracy), plus the Waitz "how busy is it" student app. Customers include Vanderbilt, Purdue, Columbia and UCLA | **~$600/yr for <5,000 sq ft (2022). $10,500–$15,000/yr for a 100,000 sq ft site (2020)**, i.e. $0.105–$0.15/sq ft/yr | Closest match to our student navigator, but requires hardware. No HVAC actuation, no DR, no cellular data, no network SLA | [S2] [Campus Technology 2022](https://campustechnology.com/articles/2022/11/17/occuspace-expands-occupancy-monitoring-to-more-colleges-and-universities.aspx); [2020](https://campustechnology.com/articles/2020/08/12/de-densification-tech-monitors-foot-traffic.aspx) |
| **Lambent Spaces (offered by Siemens)** | **Software-only** occupancy and utilization analytics built on a campus's existing Wi-Fi. Targets higher ed and commercial real estate. Siemens lists it as "AI-Enhanced Occupancy and Utilization Analytics… powered by Lambent Spaces" in its Xcelerator portfolio; whether Siemens owns or resells it is not confirmed | Contact vendor | **Biggest threat:** same "no new hardware" pitch, marketed by a building-automation major. No cellular or 5G data, no DR, no slicing | [S] [Siemens product page](https://www.siemens.com/en-us/products/lambent-spaces-ai-enhanced-occupancy-and-utilization-analytics/); [S2] [Capterra](https://www.capterra.com/p/192517/Lambent-Spaces/) |
| **Siemens Enlighted** | Sensors embedded in light fixtures (lighting control plus occupancy data). CSU Dominguez Hills: 424 sensors, about $26,000/yr saved, 78% lighting savings in hallways (2014). U. of Birmingham: 23,000 sensors | Not public. One promotional source says Enlighted takes a share of savings instead of charging for installation | Requires a lighting retrofit, and savings are mostly lighting, not HVAC | [S2] [Campus Technology 2014](https://campustechnology.com/articles/2014/07/24/cal-state-dominguez-hills-saves-with-smart-sensor-lighting.aspx) |
| **Density** | Depth and radar people-counting sensors for workplaces | **"Coverage Pricing" based on square footage (2023); rate not public.** 2016: $45/sensor/month. Waffle sensor: $149/device + $95/yr | Hardware cost; workplace focus; no HVAC actuation or network | [S2] [Smart Buildings Mag 2023](https://smartbuildingsmagazine.com/news/density-unveils-advanced-sensors-that-cut-cost-of-workplace-measurement); [TechCrunch 2016](https://techcrunch.com/2016/07/27/density-series-a/); [BusinessWire 2024](https://www.businesswire.com/news/home/20241014409432/en/Density-Unveils-Self-Installable-Sensor-for-Real-Time-People-Count) |
| **Butlr** | Thermal people-sensing sensors and platform | Subscription (warranty tied to active subscription); price not public | Hardware | [S2] [Butlr support](https://support.butlr.io/hc/en-us/articles/33781555446285) |
| **Cisco Spaces** | Wi-Fi location and occupancy analytics on Cisco networks | Licensed per access point (3/5/7-year terms) or per sq ft ("Smart Spaces"). List price not found | Works only on Cisco networks; no cellular data, no DR, no slicing | [S] [Cisco Spaces FAQ](https://spaces.cisco.com/?p=1858) |
| **R-Zero** | Occupancy-based demand-controlled ventilation using its own sensors and BACnet setpoint changes | **Shared-savings model**. Claims 20–40% HVAC reduction (vendor claim) | Hardware; no network or DR layer | [S2] [R-Zero higher-ed page](https://rzero.com/higher-education/) |
| **BrainBox AI** | Autonomous AI control of HVAC through the existing BMS | **$0.25/sq ft/yr on a 12-month term (AWS Marketplace listing as reported by a third party; unverified).** Vendor says pricing is custom | Uses no occupancy ground truth from the network | [S2] [rfp.wiki comparison](https://www.rfp.wiki/specialty-industries/energy-utilities-software/energy-management-and-optimization-systems/brainbox-ai/energycap) |
| FDD / building-analytics tools (e.g., Clockworks, CopperTree, which U. Rochester piloted) | Fault detection and diagnostics on BMS data | **LBNL medians: $0.06/sq ft base cost and $0.02/sq ft/yr recurring.** Energy information systems: $0.01 and $0.01 | No occupancy signal; complementary (they can consume our feed) | [S] [LBNL 2022](https://eta-publications.lbl.gov/publications/building-analytics-tool-deployment) |
| **Curtailment service providers** (Enel North America / Enel X, CPower, Voltus) | Register and dispatch customers in PJM demand response | Revenue split not published. Voltus case studies average about **$60/kW-yr** of gross DR revenue (Thundersaid analysis). GridBeyond advertises "up to 100%" revenue share | No occupancy forecasting. **Partner, don't compete** | [S2] [Thundersaid](https://thundersaidenergy.com/?p=71244); [GridBeyond](https://gridbeyond.com/earn-more-curtail-less-the-most-profitable-demand-response-opportunity-in-pjm/) |
| Johnson Controls OpenBlue, Honeywell | Building-automation incumbents | No public pricing found in this pass (not researched in depth) | Incumbent BMS owners: the integration partners or channel we need | — |
| **AT&T** | Campus 5G/MEC: UConn Stamford private 5G (2021), U. Miami (first campus on AT&T 5G+ and MEC), U. Tennessee testbed. **Turbo Live** one-time event network passes (2026) | Turbo Live: one-time pass, "prices vary" by venue | Strong on events and MEC; no energy/occupancy offer found | [S2] [Fierce](https://www.fierce-network.com/private-wireless/at-t-and-university-connecticut-launch-private-5g-network); [S&P Global 2026](https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/04/mobile-world-congress-2026-can-the-industry-sell-network-experiences); [Droid-Life](https://www.droid-life.com/2026/01/21/att-to-sell-one-time-vip-passes-to-faster-network-during-live-events/) |
| **T-Mobile** | 5G Advanced Network Solutions (Bradley University was the first university). **SuperMobile**, a business plan built on a nationwide slice. **T-Priority** first-responder slice | SuperMobile: **$42/line/month at launch for 6+ lines** (Recon Analytics). T-Priority: **$7.50/month add-on** (Feb 2025) | Slicing productized at the plan level; no energy/occupancy offer found | [S2] [Recon Analytics](https://www.reconanalytics.com/?p=3422); [S] [T-Mobile/BusinessWire](https://www.businesswire.com/news/home/20250220370759/en/T-Mobile-Unveils-Big-Moves-for-T-Priority-That-Put-First-Responders-First); [S2] [TeckNexus (Bradley)](https://tecknexus.com/5gusecase/5g-advances-in-bradley-universitys-education-with-t-mobile/62) |

**White space:** no vendor we found combines (a) occupancy from both cellular and Wi-Fi with no new hardware, (b) closed-loop HVAC control plus DR dispatch, and (c) a carrier-grade network SLA (slicing or private 5G) in one contract. Siemens/Lambent is the most likely fast follower on (a)+(b). AT&T and T-Mobile could match (c).

---

## 4. Verizon Business: product facts and context

| Item | Fact | Source |
|---|---|---|
| Business segment revenue, 2025 | **$29,069M (−1.6%)**. Enterprise & Public Sector **$13,534M (−4.8%)**. Business Markets & Other $13,581M (+3.7%). Wholesale $1,954M (−11.7%) | [S] [Verizon 2025 10-K](https://www.sec.gov/Archives/edgar/data/732712/000073271226000015/a2025_aronform10-k.pdf) |
| Why Enterprise & Public Sector declined | "a decrease of **$532 million in wireline revenue**… declines in networking, traditional data and voice…" and "a decrease of $193 million in Wireless service revenue… **pressure in Public Sector** in part from government efficiency efforts." Public-sector customers explicitly include "educational institutions" | [S] same 10-K |
| Business FWA | 2.32M connections at end of 2025 (+25.1%). Business postpaid phone churn 1.23%/month | [S] same 10-K |
| **On Site 5G** (private 5G) | Launched June 2021 for large enterprise and public sector. Custom-designed, fully managed, can run on customer-licensed spectrum. **Pricing and deal sizes are not public** | [S] [Verizon news](https://www.verizon.com/about/node/921433); [welcome kit](https://verizon.com/business/welcome-kits/on-site-5g) |
| Private 5G references | Port of Virginia (NIT, 270-acre terminal, Nov 2023). Wichita State "Smart Factory" private 5G. USC Innovation Experience Hub with a private network (2022). ASU 5G Innovation Hub (2022). **FIFA World Cup 2026: private 5G in host stadiums and testing of network slicing.** Buffalo Bills' new Highmark Stadium: Verizon owns the neutral-host DAS (announced May 2025) | [S2] [RCR](https://www.rcrwireless.com/20231117/featured/verizon-business-build-new-5g-private-network-port-virginia); [Central SC](https://www.centralsc.org/news/verizon-usc-partner-on-5g-powered-technology-developments); [ASU](https://tech.asu.edu/features/asu-verizon-5g); [Light Reading](https://www.lightreading.com/5g/verizon-talks-up-5g-fwa-support-for-2026-fifa-world-cup); [S] [Verizon (Bills)](https://www.verizon.com/about/news/buffalo-bills-announce-verizon-partner-highmark-stadium) |
| **Verizon Frontline Network Slice** | Launched April 2025 and nationwide by June 2025 (**50 major markets**). Eligible public-safety agencies get it "at the same cost as current 5G UW plans." The first implementation used Cradlepoint R980 routers | [S] [Verizon, June 12 2025](https://www.verizon.com/about/news/verizon-frontline-network-slice-now-available-nationwide); [S2] [Light Reading](https://www.lightreading.com/mobile-core/verizon-launches-network-slice-for-public-safety) |
| **5G Mobile Network Slice – Enhanced Video Calling** | Add-on to the Enterprise Choice Unlimited plan, described as "an easy, affordable add-on" (no price published). The consumer version is included at no extra cost on Unlimited Ultimate and Business Unlimited Pro | [S] [Verizon solution brief](https://www.verizon.com/business/resources/solutionsbriefs/5g-mobile-network-slicing-video-calling.pdf); [S2] [telecoms.com](https://www.telecoms.com/5g-6g/verizon-gives-away-network-slicing-to-consumers) |
| **5G Network Slice – Enhanced Internet** (FWA) | Dec 18, 2025: "SLA-backed" 200 Mbps down / 45 Mbps up, no data caps, priority during congestion, fixed monthly price (amount not published) | [S] [Verizon news](https://www.verizon.com/about/news/wireless-internet-ai-era-network-slicing-enables-sla-backed-service-verizon-business) |
| Intelligent Lighting / Smart Communities | Came from the 2016 Sensity acquisition. Still marketed as an end-to-end SaaS (hardware, software, services, connectivity) on ThingSpace. GSMA resource dated July 2025 | [S] [ThingSpace](https://thingspace.verizon.com/solutions/intelligent-lighting/); [S2] [GSMA 2025](https://www.gsma.com/solutions-and-impact/technologies/internet-of-things/gsma_resources/smarter-safer-greener-cities-with-verizon-intelligent-lighting/) |
| Verizon and universities | Smart Campus Competition across multiple universities (Rutgers held its 2nd annual in April 2026; NJIT reported 600+ students and 150 teams across 4 schools); UT Dallas OpenLab partnership | [S] [Rutgers SoE](https://soe.rutgers.edu/news/verizon-smart-campus-competition); [NJIT](https://news.njit.edu/verizon-5g-smart-competition-presented-challenge-students-njit-had-solutions); [UT Dallas](https://news.utdallas.edu/campus-community/ut-dallas-verizon-partnership-2026/) |

**GTM implication:** Enterprise & Public Sector, the unit that sells to universities and hospitals, is shrinking because legacy wireline is declining. A product that (1) attaches recurring software and services to wireless and private-network deals and (2) is budget-neutral for the customer, because it is funded from energy savings, works directly against that decline.

---

## 5. Pricing benchmarks

| Benchmark | Value | Label / source |
|---|---|---|
| NJ commercial electricity price | **19.17¢/kWh (Jul 2026); 17.78¢ for Jan–Jul 2026 YTD** (16.44¢ a year earlier). U.S. commercial 13.97¢ YTD. NJ all-sector 20.15¢ YTD | [S] [EIA EPM Table 5.6.A](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a) / [5.6.B](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_b) |
| Sensor-based occupancy analytics (Occuspace) | $0.105–$0.15/sq ft/yr ($10.5k–$15k per 100k sq ft); $600/yr below 5k sq ft | [S2] Campus Technology (§3b) |
| FDD software (LBNL medians) | $0.06/sq ft base; **$0.02/sq ft/yr recurring**; 9% median savings | [S] LBNL 2022 |
| EIS software (LBNL medians) | $0.01/sq ft base; $0.01/sq ft/yr recurring; 3% median savings | [S] LBNL 2022 |
| AI HVAC optimization (BrainBox) | $0.25/sq ft/yr (12-month term; unverified third-party report) | [S2] |
| Density | Per-sq-ft "Coverage Pricing" (rate not public) | [S2] |
| ESCO shared-savings split | Wide range. One state guide gives a "typical division" of **85% ESCO / 15% owner**. One vendor gives 70% owner / 30% ESCO. Chile is cited at 60/40. In North America, guaranteed-savings contracts dominate | [S] [Hawaii State Energy Office 2013](https://energy.hawaii.gov/wp-content/uploads/2012/06/Pros-and-Cons-of-guaranteed-vs.-shared-energy-savings-2013.pdf); [S] [IEA](https://www.iea.org/reports/energy-service-companies-escos-2/esco-contracts); [S2] [Trexon](https://trexon.my/solutions/esco) |
| NJ ESIP (performance contracting for public entities, including colleges and universities) | Terms up to 15 years (20 with CHP). Must be cash-flow positive each year. Not treated as new debt | [S2] NJ BPU/ESIP materials via search summary: [ESIP How-To Guide](https://www.nj.gov/state/bac/planning/documents/resources/ESIP_HowToGuide_V2_2019.pdf) |
| **PSE&G Engineered Solutions** (eligible: hospitals, colleges and universities, school districts, etc.) | Free investment-grade audit. PSE&G pays down the project's simple payback by **up to 6 years**. The customer's share is repaid **interest-free on the bill over 60 months** | [S] [PSE&G program page](https://mybizenergy.pseg.com/engineered-solutions-program) |
| PSE&G Tier 2 Advanced Custom (2025 guide) | **HVAC Controls & Chiller Plant Optimization: $1.00 per kWh saved. Gas: $7.00 per therm.** Custom lighting: $0.50/kWh. **Capped at 60% of total project cost.** Requires M&V / BMS data; pre-approval required | [S] [PSE&G 2025 Tier 2 guide](https://bizsave.pseg.com/wp-content/uploads/2025/04/2025-Engineered-Solutions-Tier-2-Advance-Custom-Incentive-Guide-V1.0.pdf) |
| NJCEP Large Energy Users (as described in the Rutgers CAP, 2021) | Incentive capped at the least of: $4M; 75% of project cost; 90% of prior-year NJCEP fund contribution (~$2M); or $0.33/kWh plus $3.75 per unit of annual Btu savings, as written in the source | [S] Rutgers CAP supplement |
| Carrier slice and plan anchors | T-Priority $7.50/month. SuperMobile $42/line (6+ lines, launch). Verizon Frontline slice at 5G UW plan prices. AT&T Turbo Live: one-time event pass, price varies | [S]/[S2] §3b, §4 |
| Private 5G build (vendor ballpark only) | Small cells $5,000–$10,000 each; core $50,000–$100,000; licensing ~$10,000 (placeholder) | [S2] [Firecell cost estimator](https://firecell.io/private-5g-cost-estimator/) (vendor) |
| Verizon student discount | **$10/month off (1 line) or $25/month off (2 lines)** on Unlimited Ultimate, Plus and Welcome; up to 4 years with annual re-verification through ID.me | [S] [Verizon FAQ](https://www.verizon.com/support/college-students-discount-faqs) |

**PSE&G incentive insight [EST]:** For a software-led project, the 60% cap on project cost, not the $1.00/kWh rate, is what limits the incentive. Example: 1M kWh saved × $1.00 = a $1.0M nominal incentive, but a $300k project caps it at $180k. **Bundle the software with BMS/VAV controls upgrades** so the utility incentive covers a meaningful share of Verizon's deployment cost.

---

## 6. Demand-response economics (PJM; Rutgers is in the PSEG zone)

| Delivery year | RTO clearing price ($/MW-day, UCAP) | $/kW-yr (UCAP) [EST] = price × 365 ÷ 1,000 | DR cleared (MW UCAP) | Notes | Source |
|---|---|---|---|---|---|
| 2025/26 | **$269.92** (BGE $466.35; DOM $444.26) | $98.5 | 6,064.7 | — | [S] [PJM 2026/27 BRA report](https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2026-2027/2026-2027-bra-report.pdf) |
| 2026/27 | **$329.17** (cap, entire RTO) | $120.1 | 5,530.6 | DR ELCC 69%; FPR 0.917 → ≈ **$76/kW-yr per kW of nominated (ICAP) load** [EST: × 0.69 × 0.917] | [S] PJM 2026/27 and [2027/28 BRA reports](https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2027-2028/2027-2028-bra-report.pdf) |
| 2027/28 | **$333.44** (cap) | $121.7 | **7,298.6** | DR ELCC rose to 92% and DR must now be **available in all hours of the year**. FPR 0.926 → ≈ **$104/kW-yr per kW ICAP** [EST: × 0.92 × 0.926]. Without the cap the price would have been $529.80 | [S] PJM 2027/28 BRA report |
| 2028/29 | **$325** (cap) | $118.6 | DR = 5% of supply mix | Without the cap the price would have been $554.72 | [S] [PJM release, July 14 2026](https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/2026-releases/20260714-pjm-capacity-auction-procures-138318-mw-of-generation-resources.pdf) |

| What the participant actually receives | Value | Label |
|---|---|---|
| Customer share of revenue through a curtailment service provider | **Not published**; set by each contract. Voltus case studies average ~$60/kW-yr gross (Thundersaid). GridBeyond markets "up to 100%" | [S2] |
| Per 1 MW of curtailable campus load (2027/28) | Gross capacity value ≈ $103.7k/yr. If the customer keeps 50–80% (assumed range; actual splits are not published) → **$52k–$83k per MW-year** | [EST] |
| Second value stream: peak-load contribution (PLC) management | Cutting load in PJM's five system-peak hours lowers the customer's capacity charges. Temple University reports **over $9M in avoided capacity costs** | [S] [Enel/Temple case study](https://enelnorthamerica.com/content/dam/enel-na/solutions/case-studies/temple-university/Temple-University_Case-Study_PJM_06-19.pdf) |
| **University example: Temple (PA, PJM)** | **$14.5M+ in savings and revenue over ~10 years**: Synchronized Reserve $2.3M since 2007 (~$226k/yr); Emergency Load Response $998k+; "nearly $4.1M" gross DR revenue; >$1.5M supply savings; >$9M avoided capacity. Much of this was earned at far lower capacity prices than today's $325–$333/MW-day | [S] Enel case study; [S2] [casestudies.com](https://www.casestudies.com/company/enel-x/case-study/temple-university-earns-millions-by-stacking-demand-response-programs) |
| Other universities in PJM DR | Christopher Newport, U. Dayton and Norfolk State all report DR revenue but publish no dollar amounts. Delaware Valley College earned ">$25,000" (2007–08) | [S2] |

**Why occupancy matters for DR [REC]:** The 2027/28 rule that DR be available in all hours of the year raises performance risk for campuses. An occupancy forecast tells the dispatcher which buildings can shed load without hurting comfort at any hour. That lets a campus nominate more MW with less penalty risk, and that is the value we monetize.

---

## 7. Customer-care cost benchmarks

| Benchmark | Value | Source |
|---|---|---|
| Cost per ticket by support level, North America (MetricNet) | **Level 1 service desk $22; Level 2 desktop support $62; Level 3 (apps, NOC, networking) $85; field support $196; vendor support $471.** A ticket escalated from L1 to L2 costs $84 in total | [S] [HDI / MetricNet, J. Rumburg](https://www.thinkhdi.com/~/media/HDICorp/Files/Library-Archive/Insider%20Articles/Percent%20Resolved%20Level%201%20Capable.pdf) (c. 2010–11) |
| Desktop support (L2), 2010 | $62 average (range $27–$490). Per incident $48; per service request $113 | [S] [HDI "Cost per Ticket"](https://www.thinkhdi.com/~/media/HDICorp/Files/Library-Archive/Insider%20Articles/Cost%20per%20Ticket.pdf) |
| Update, 2018 | Service desk $22 + desktop support **$69** | [S] [HDI SupportWorld 2018](https://www.thinkhdi.com/library/supportworld/2018/metric-of-month-percent-resolved-level-1-capable) |
| Service desk, 2017 North American average | **$15.56** per ticket | [S] [HDI SupportWorld 2017](https://www.thinkhdi.com/library/supportworld/2017/metric-of-month-desktop-support-cost-per-ticket) |
| HDI Support Center Practices & Salary Report 2015 | **$16 median** cost per ticket (fully loaded). Channel mix: phone 52%, email 35%, chat 10%, walk-up 9% | [S] [HDI 2015](https://www.thinkhdi.com/~/media/HDICorp/Files/Industry-Reports/SCPSR/scpsr-2015-web.pdf) |
| Live vs self-service (Gartner 2019 poll) | Live channels (phone, chat, email) **$8.01/contact**; self-service **~$0.10/contact** | [S2] [DestinationCRM citing Gartner](https://www.destinationcrm.com/Articles/CRM-Insights/Insight/Gartner-Survey-Finds-Self-Service-Insufficient-135436.aspx) |
| Verizon enterprise support model | Account Management (sales lead), Solutions Architect (pre-sales design), Client Service Management (service governance and SLA compliance), Billing Support, and Incident Management with **"24x7 post-sales technical support through Verizon Enterprise Center"** that "escalates and manages repair teams, carriers and third parties" | [S] [Verizon Customer Success Reference Guide (State of CT)](https://business.ct.gov/-/media/DAS/Business-Office/Telecom/Verizon-SOCT-Customer-Success-Reference-Guide.pdf) |
| Verizon cost context | More than 13,000 job cuts announced in Nov 2025 under CEO Dan Schulman. Press reports quote him saying AI could replace "a large percentage" of customer-service work | [S2] [TechRadar](https://www.techradar.com/pro/verizon-is-laying-off-over-13-000-workers); [PhoneArena](https://www.phonearena.com/news/verizon-ai-replacing-employees_id180887) |

**Care design for the product [REC]:**
- Occupancy-driven HVAC creates a new ticket type: "my room is too hot or too cold."
- Route these first to self-service in the student/staff app, with an automatic BMS override and an occupancy-aware explanation. At Gartner's figures that costs ~$0.10 instead of $8.01 per contact.
- Route to Tier 1 ($15.56–$22) next. Escalate to Tier 2 or 3 ($62–$85) only for faults in the control loop.
- Illustration [EST]: 1,000 comfort tickets a year (assumed) with 70% deflected to self-service costs 700 × $0.10 + 300 × $22 = **$6.7k**. Handling them all at L1 costs **$22k**. Escalating 40% of them to L2 adds another 400 × $62 = $24.8k.
- Keep Verizon Enterprise Center as the single 24x7 front door, so the energy SaaS does not create a separate support org, consistent with Verizon's cost posture.

---

## 8. Campus network experience and the student cohort

| Data point | Value | Source |
|---|---|---|
| Boldyn Campus Connectivity Report (spring 2025; 1,087 students + 250 staff) | **73%** say consistent residence-hall internet is "essential," but only **26%** are very satisfied (20% in classrooms and admin buildings). **81%** had an internet issue in the past year; **84%** say poor internet affected schoolwork; **96%** of students and staff want digitally connected campus features. Vendor-sponsored survey | [S2] [Boldyn](https://www.boldyn.com/news/new-data-exposes-47-point-gap-between-student-expectations-and-satisfaction-in-boldyns-campus-connectivity-report) |
| Wi-Fi and college choice (dated) | "Nearly three in five" students said they would not attend a college without free Wi-Fi (Wi-Fi Alliance / Wakefield, 2008, n=501) | [S2] [Campus Technology 2008](https://campustechnology.com/Articles/2008/10/College-Students-Find-WiFi-Essential-to-Education-Survey-Reports.aspx) |
| Gen Z carrier behavior (KPMG, July 2024, n=1,000) | **75% of Gen Z are with a top-3 carrier. 63% of Gen Z have been with their carrier 3 years or less. 25% of Gen Z plan to switch carriers to cut their bill** within 6 months | [S] [KPMG](https://kpmg.com/kpmg-us/content/dam/kpmg/pdf/2024/carriers-embrace-genai-wireless-customers-share-what-really-matters.pdf) |
| Gen Z network experience (J.D. Power, Jan 2024) | Gen Z customers "use phones more and experience more network problems" (300+ minutes/day per press summary) | [S2] [BusinessWire headline](https://www.businesswire.com/news/home/20240118426069/en/Generation-Z-Customers-Use-Phones-More-and-Experience-More-Network-Problems-J.D.-Power-Finds) (page not opened) |
| Carrier share among 18–24-year-olds | **Not found** in a citable 2025–26 source | — |
| Verizon Consumer economics, 2025 | Postpaid phone churn **0.92%/month**; postpaid ARPA **$147.31**; 2.95 connections per account → ≈ **$49.94 per connection per month** [EST] | [S] Verizon 2025 10-K |
| Value of a student line [EST] | 36 months × $49.94 ≈ **$1,800 in service revenue** (gross, before margin and the $10–$25 student discount). At Verizon's average churn the implied lifetime is ~109 months (≈ $5,400), but KPMG's tenure data suggests students churn faster | [EST] |
| Students reachable | 14.5M students at ≥5,000-student institutions (fall 2021). Rutgers has 19,000+ residents on campus | [S] NCES; Rutgers IP&O |

**GTM implication [REC]:** The crowd/quiet-space navigator should be **free to students and paid for by the campus license**. It gives Verizon a reason to engage students during the months they set up their own phone plans, which is when the $10/$25 student discount and an on-campus 5G experience can win them. Measure success by the attach rate of verified-student lines per campus.

---

## 9. Recommended pricing & business model **[REC: our reasoned recommendation, grounded in the benchmarks above]**

### 9a. Packaging: one contract, four layers

| Layer | What the customer buys | Recommended price | Anchors (from this file) |
|---|---|---|---|
| **1. Occupancy Intelligence** (space analytics + student navigator + API to the BMS) | Privacy-preserving aggregate occupancy from Verizon 5G and campus Wi-Fi. No new hardware | **$0.02–$0.03 per GSF per year**, tiered: $0.03 below 5M GSF, $0.025 for 5–15M, $0.02 above 15M. Minimum $50k/yr | About 1/5 of sensor-based Occuspace ($0.105–0.15) because there is no hardware. Matches the LBNL FDD median recurring cost ($0.02) so it fits existing facilities budgets. Well below BrainBox's reported $0.25 |
| **2. Occupancy-driven HVAC (energy performance)** | Closed-loop setpoint/VAV scheduling, with savings verified under IPMVP M&V | **Customer keeps 80%; Verizon earns 20% of verified savings** for 5 years. Optional guarantee: if verified savings fall short of the Layer 1 fee, Verizon credits the difference | Far more customer-friendly than the ESCO "85% ESCO / 15% owner" split, because Verizon finances no heavy equipment. Shared savings is already the model at R-Zero and (reportedly) Enlighted. Fits NJ ESIP's cash-flow-positive test |
| **3. Grid (DR + PLC)** | Occupancy-informed dispatch, delivered **with an incumbent CSP** (Enel, CPower or Voltus) as registrant | **15% of incremental DR and avoided-capacity value**, measured against the customer's pre-program baseline | At 2027/28 prices ≈ $104/kW-yr ICAP-equivalent; the all-hours availability rule makes forecasting more valuable. Partnering avoids PJM CSP membership obligations in Year 1 |
| **4. Network SLA** | (a) Frontline slice for campus police and EMS; (b) event slices (games, commencement, move-in); (c) On Site 5G for labs and hospitals | (a) **Catalog price, at the same cost as 5G UW plans.** (b) **Per event-day, with N event-days per year bundled in.** (c) Managed-service monthly fee over 5 years | Anchored to T-Priority $7.50/month, SuperMobile $42/line and AT&T Turbo Live passes. Private 5G capex ballpark: $5–10k per small cell plus $50–100k core (vendor). **Price (b) and (c) need Verizon Business pricing validation** |

### 9b. Rutgers lighthouse economics [EST]

| Line | Low case (5% HVAC savings) | High case (10%) | Math |
|---|---|---|---|
| Gross HVAC energy savings to Rutgers | $1.82M/yr | $3.65M/yr | $60M × 60.8% × 5% or 10% |
| Layer 1 fee (29M GSF × $0.02) | $0.58M | $0.58M | — |
| Layer 2 fee (20% of savings) | $0.36M | $0.73M | — |
| **Rutgers net benefit before DR and incentives** | **$0.88M/yr** | **$2.34M/yr** | Savings − fees |
| Verizon software revenue | $0.94M/yr | $1.31M/yr | Layers 1 + 2 |
| DR upside per MW curtailable | +$52k–$83k to Rutgers; +$15.6k to Verizon (15% of $103.7k) | same | 2027/28 PJM math, §6 |
| PSE&G incentive | Up to $1.00/kWh saved for HVAC controls, **capped at 60% of project cost**. This offsets the deployment and controls-integration capex | same | §5 |

### 9c. Go-to-market sequence

1. **Land (Q1–Q2 2027):** A Verizon-funded 90-day lighthouse pilot in 5–10 Rutgers New Brunswick academic and library buildings that have VAV systems.
   - Deliverables: IPMVP M&V, the student navigator in Waitz-style UX, and one event slice (football game or commencement).
   - Rutgers gets free M&V data; Verizon gets a reference case and a PSE&G Tier 2 application.
2. **Expand:** Campus-wide Layer 1 + 2, procured through NJ ESIP or a cooperative contract. Add the PJM DR/PLC partnership before the 2027/28 delivery year, when the all-hours DR rule applies.
3. **Replicate:**
   - First, the 488 institutions with ≥10,000 students, prioritizing PJM states and high-price states (NJ at 17.78¢ vs 13.97¢ U.S.).
   - Then academic medical centers. Hospitals pay 2.7× education's $/sq ft ($3.18 vs $1.17) and have 95% VAV in post-1980 floor space.
   - Then corporate campuses (28,000 office buildings over 100k sq ft).
4. **Channel:**
   - Lead with Verizon's Enterprise & Public Sector account teams (Account Manager + Solutions Architect).
   - Partner with BMS integrators (JCI, Honeywell, or Siemens despite its Lambent overlap) and one CSP.
   - Support through the Verizon Enterprise Center 24x7 model (§7).
5. **Defensibility:**
   - Carrier-side occupancy (5G) is something Wi-Fi-only rivals such as Lambent and Cisco Spaces cannot replicate.
   - The same forecast drives Verizon's radio-sleep savings, so Verizon gains on its own opex even at software break-even.

### 9d. Risks to price in

- **Savings uncertainty:** field results range from 1–5% (MARTINI's 51-building estimate) to 17.8% (Sentinel, 1 day). Mitigate with the Layer 2 guarantee and conservative 5–10% planning.
- **Cogeneration campuses (Rutgers Busch/Livingston):** electric savings can lower cogeneration utilization rather than grid purchases, so the M&V baseline must model the central plant.
- **Fast followers:** Siemens/Lambent (Wi-Fi software-only), plus AT&T and T-Mobile on slicing.
- **Privacy and governance:** sell only aggregate, k-anonymized occupancy. The surveys show student trust is needed (only 26% very satisfied with connectivity).
- **Policy volatility:** PJM's price cap and collar, and changes to PSE&G or NJ program rules. Incentives quoted here are from 2025 guides; confirm the current year's terms.

---

## 10. Open items / not verified in this pass

- Verizon On Site 5G / private network pricing and deal sizes, and the price of the Enterprise Choice Enhanced Video Calling add-on: **not public**.
- Rutgers' utilities-only budget line (the FY27 figure is the broader "Plant Operation & Maintenance," $204.0M). The $60M energy figure is from 2021.
- Wireless carrier share among 18–24-year-olds: no citable 2025–26 source found.
- Typical CSP revenue split in PJM: not published.
- BrainBox AI $0.25/sq ft (third-party report of an AWS listing), J.D. Power Gen Z details, the AAMC teaching-hospital count, and the Portland State "up to 20%" figure: secondary or unopened sources.
- The web-search budget ran out during this pass. A follow-up session can verify the items above.
