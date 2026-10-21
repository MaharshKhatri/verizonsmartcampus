# Generation 3: founder tournament (2026-10-21)

Generation 3 asked one question: **is Circadian the idea that wins, or only the idea we built first?** A multi-agent tournament simulated the crowd, ran fresh research, generated 120 ideas through 14 lenses, screened them down to 27 concepts, built 9 deep dossiers with two red teams each, and had a judge panel score the finalists on the official rubric.

**Verdict: replace Circadian.** The red team killed it (about $3 of venue radio energy per game; ties Verizon's AI on ordinary days; NPV negative without network pull-through; and energy and digital twins are the most crowded LLM space). The new champion is **Last Copper**, built on a Verizon program with a public date. The Circadian code stays as our engineering bench.

## 1. The crowd: what other LLM-assisted teams will pitch

We asked agents to brainstorm the way a default LLM would for this brief. We avoid these ideas and their close variants.

| # | Crowd idea | Verizon tech it leans on |
|---|---|---|
| 1 | ScarletTwin: Real-Time 5G Campus Digital Twin | 5G Ultra Wideband, Verizon 5G Edge (MEC with AWS Wavelength), ThingSpace IoT platform, LTE-M/NB-IoT sensors, private 5G network option, netw |
| 2 | GreenRAN: AI-Native O-RAN Energy Optimizer on COSMOS | O-RAN Near-RT/Non-RT RIC (xApps/rApps), vRAN, Massive MIMO cell/carrier sleep, SON, AI/ML network analytics, COSMOS/WINLAB testbed with srsR |
| 3 | SentinelEdge: 5G Edge-AI Public Safety and Emergency Response | Verizon Frontline (public safety network, priority and preemption), 5G network slicing (mission-critical slice), Verizon 5G Edge MEC for vid |
| 4 | SliceU: Intent-Based Dynamic Network Slicing for Campus Services | 5G Standalone core, end-to-end network slicing (eMBB/URLLC/mMTC), Verizon Network as a Service / Network APIs (Quality on Demand), O-RAN RIC |
| 5 | RU-Connect V2X: 5G Smart Transit and Autonomous Shuttle Network | C-V2X / 5G V2X, Verizon Hyper Precise Location (RTK), Verizon 5G Edge MEC, Verizon Connect fleet telematics, ThingSpace IoT, 5G Ultra Wideba |
| 6 | HoloClass: 5G Edge-Rendered Immersive AR/VR Learning | 5G Ultra Wideband (mmWave and C-band), Verizon 5G Edge with AWS Wavelength (cloud/split rendering), network slicing (low-latency XR slice),  |
| 7 | ScarletArena 5G: Connected Smart Stadium Experience | 5G Ultra Wideband mmWave in-venue, Verizon 5G Edge MEC, multi-access edge video streaming, network slicing for broadcast and operations, pre |
| 8 | CampusCare 5G: Connected Health and Rapid Medical Response | 5G Ultra Wideband and LTE-M wearables via ThingSpace, Verizon 5G Edge for real-time health inference, Verizon Frontline priority for EMS, 5G |
| 9 | EcoCampus AI: Smart Building Energy Optimizer | 5G UWB / LTE-M / NB-IoT sensors, ThingSpace IoT platform, Verizon Mobile Edge Computing (MEC) for real-time AI, Verizon Business energy/IoT  |
| 10 | ScarletPark: AI Smart Parking & Dynamic Pricing | 5G UWB connected cameras, NB-IoT/LTE-M parking sensors, ThingSpace, MEC video analytics, Verizon Connect |
| 11 | RU Ride AI: Smart Transit & Bus Optimization | Verizon Connect fleet telematics, 5G/LTE onboard connectivity, ThingSpace IoT, MEC for real-time routing, edge AI passenger counting |
| 12 | CampusTwin: 5G Digital Twin & Predictive Maintenance | 5G UWB and private 5G (Verizon On Site 5G), ThingSpace, MEC, Verizon Business IoT managed services, network slicing for critical infrastruct |
| 13 | Scarlet 5G Stadium: Smart Venue Fan Experience | 5G Ultra Wideband (mmWave) in-venue, MEC for low-latency AR/video, network slicing for ticketing/POS/broadcast, Verizon venue/stadium soluti |
| 14 | Scarlet Assist: AI Campus Concierge | 5G UWB, MEC for low-latency inference, Verizon AI/CX platform (Gemini-powered agents), Verizon Business messaging/APIs, student plan integra |
| 15 | SafeCampus AI: Connected Public-Safety Network | Verizon Frontline (priority and preemption), 5G network slicing for first responders, 5G connected cameras and drones, MEC video analytics,  |
| 16 | Verizon Campus Connect: Private 5G + Student Connectivity Platform | Verizon Private 5G / On Site 5G, network slicing, 5G Home Internet (FWA), MEC, ThingSpace, Verizon student and consumer plans |
| 17 | GreenCell AI: Predictive RAN Sleep for Campus ("Schulman's $200M, at campus scale") | O-RAN rApp/xApp on the RIC, vRAN (~60k sites), Samsung AI Energy Saving Manager integration, 5G UW small cells, MEC inference; prototype on  |
| 18 | ScarletAgent: AI-Native Verizon Concierge for Students ("Every Student Has a Name") | Verizon AI voice/chat agents (Gemini), My Verizon APIs, Verizon network APIs (device status, SIM swap, location for fraud), CRM micro-segmen |
| 19 | Zero-Touch Campus NOC: Multi-Agent Self-Healing Network | Verizon AI network operations/AIOps, O-RAN SMO + RIC, network digital twin, intent-based automation, MEC, Verizon Business managed services |
| 20 | GameDay Autopilot: Predictive Stadium Capacity + Dynamic Network Slicing at SHI | 5G Ultra Wideband mmWave/C-band, 5G SA network slicing, Verizon Frontline slice, MEC (Verizon 5G Edge with AWS Wavelength), predictive capac |
| 21 | RU Digital Twin: 5G-IoT Smart Building Energy Platform | Verizon ThingSpace IoT, LTE-M/NB-IoT, private 5G (Verizon On Site 5G), Verizon 5G Edge/MEC, Verizon Business IoT managed services, AI analyt |
| 22 | Scarlet Shield: 5G Public Safety + AI Emergency Response | Verizon Frontline (priority/preemption, network slice), 5G UW, Verizon drones/Skyward, MEC video analytics, Verizon Intelligent Video, conne |
| 23 | RU Transit AI: 5G-Connected Smart Bus Network | Verizon Connect fleet telematics, 5G/LTE IoT gateways, C-V2X, MEC computer vision for passenger counts, ThingSpace, Verizon Hyper Precise Lo |
| 24 | ReCircle: AI Device Diagnostics & Circular Trade-In | Verizon network diagnostics/device telemetry APIs, My Verizon app, AI care agents, MEC-hosted vision models, Verizon device trade-in and cer |
| 25 | RU Ride: AI bus tracker and crowding predictor (often bundled with smart parking) | 5G Ultra Wideband and LTE-M telematics on buses, ThingSpace IoT platform for door counters and lot sensors, Verizon 5G Edge (MEC with AWS Wa |
| 26 | StudySpot: real-time study space and library seat finder | ThingSpace IoT with NB-IoT/LTE-M occupancy sensors, 5G Ultra Wideband for real-time updates, Verizon 5G Edge for on-campus inference, aggreg |
| 27 | ScarletShield: campus safety, SOS and safe-walk app | Verizon Frontline (priority and preemption for first responders), 5G Ultra Wideband video uplink, Hyper Precise Location, Verizon Intelligen |
| 28 | RU Assist: AI campus concierge and all-in-one super app | Verizon 5G Edge (MEC) for low-latency on-campus LLM inference, 5G Ultra Wideband, Verizon AI Connect / network APIs for location context, pr |
| 29 | DineSmart: dining hall wait times and food-waste AI | ThingSpace IoT smart scales and counters, Verizon Intelligent Video (computer vision) on 5G Edge, 5G Ultra Wideband for camera backhaul, LTE |
| 30 | GreenRU: campus energy digital twin, smart bins and dorm energy competition | ThingSpace IoT and NB-IoT/LTE-M sensors, Verizon 5G Edge for real-time optimization, private 5G network for building telemetry, Verizon Busi |
| 31 | ScarletVision: AR campus navigation and 5G game-day stadium experience | 5G Ultra Wideband (mmWave) in SHI Stadium, Verizon 5G Edge for AR rendering and multi-camera replay streaming, Hyper Precise Location for in |
| 32 | MindfulRU: AI wellness and mental-health early-warning companion | 5G Ultra Wideband telehealth video, Verizon IoT wearable connectivity (ThingSpace, cellular smartwatches), Verizon 5G Edge for private on-ca |
| 33 | ScarletAI: Your 24/7 Campus Concierge Agent | Verizon 5G Edge (MEC / AWS Wavelength) for low-latency LLM inference, 5G Ultra Wideband, ThingSpace IoT APIs for live occupancy data, option |
| 34 | NetSentinel: Autonomous AI Agent for Self-Healing Campus Networks | 5G network slicing, Verizon Network APIs (Quality on Demand, Network Status), private 5G / Verizon Business Private Network, Mobile Edge Com |
| 35 | EcoScarlet: AI Energy Agent and Campus Digital Twin | ThingSpace IoT platform, LTE-M / NB-IoT sensors, 5G Edge for real-time control, Verizon Intelligent Lighting / smart building solutions, AI- |
| 36 | RU Transit AI: Predictive Bus Agent | Verizon Connect fleet telematics, 5G-connected onboard cameras and APC sensors, 5G Edge video analytics, ThingSpace, C-V2X as a 'future' sli |
| 37 | GuardianAI: Intelligent Campus Safety and Emergency Response Agent | Verizon Frontline (public safety priority and preemption), 5G network slicing for first responders, 5G Edge video analytics, Verizon Intelli |
| 38 | GameDay AI: Smart Stadium Experience Agent for SHI Stadium | 5G Ultra Wideband / mmWave at venues, 5G Edge for AR rendering and video analytics, network slicing for fan and broadcast traffic, Verizon v |
| 39 | SpaceFinder AI: Real-Time Study Space and Crowd Navigator | ThingSpace IoT sensors over LTE-M/5G, anonymized network-based crowd analytics, 5G Edge inference for camera people-counting, Verizon Locati |
| 40 | ScholarAgent: Personalized AI Academic and Wellness Copilot | 5G Ultra Wideband for AR/VR learning, 5G Edge for low-latency AI tutoring, Verizon 5G Home / FWA for off-campus students, wearable connectiv |

## 2. Fresh research digests (Gen 3)

### What Verizon sells to universities and the public sector in 2025-2026, and what it launched (Frontline slice, Business slicing, private 5G and neutral host, network APIs and Aduna, satellite, NG911, AI Connect, education)

- {"fact": "Verizon Frontline Network Slice launched April 24, 2025 in 29 markets. It is a 5G Ultra Wideband slice reserved for public safety and costs the same as existing 5G UW plans. It first worked only in vehicles through Cradlepoint R980 routers and needs a 5G standalone (SA) capable device.", "status": "VERIFIED", "url": "https://www.verizon.com/about/news/verizon-frontline-network-slice-launches"}
- {"fact": "On June 12, 2025 the slice expanded to 50 major markets, including New York and Philadelphia. Verizon says it is available wherever 5G UW is offered. On April 23, 2026 it was extended to compatible phones, tablets and laptops nationwide.", "status": "VERIFIED", "url": "https://www.verizon.com/about/news/verizon-frontline-network-slice-available-nationwide"}
- {"fact": "Verizon's Frontline page claims 45,000+ agencies and #1 public-safety voice share (Q4 2025). It also states that priority and preemption are NOT yet offered on 5G Ultra Wideband: congested users fall back to 4G LTE.", "status": "VERIFIED", "url": "https://www.verizon.com/business/solutions/public-sector/public-safety/"}
- {"fact": "Public materials do not say whether campus or university police qualify for Frontline or the slice. Eligibility is decided by Verizon sales case by case.", "status": "UNVERIFIED", "url": "https://www.verizon.com/business/answers/best-tablets-for-working-in-the-field/"}
- {"fact": "Verizon Business sells four slice products: Frontline; 5G Network Slice - Enhanced Internet (launched Dec 18, 2025; fixed wireless, 200 down / 45 up Mbps, SLA, no caps, aimed at uplink-heavy AI and computer-vision work); Enhanced Video Calling (Dec 2024); and Business App Management (per-user, MDM-integrated, guaranteed bandwidth for chosen apps). There is no on-demand or event slice and no public slice API.", "status": "VERIFIED", "url": "https://www.verizon.com/business/products/networks/5g-network-slice/"}
- {"fact": "Verizon Frontline App Developer Challenge: entries ran Oct 28, 2025 to Apr 2, 2026 with a $25K grand prize. On May 20, 2026 'Apex Eye' won; it turns drone video into AI situational awareness. Two of the three finalists were college students (UMass Boston, James Madison). Finalists pitched at the NYSE and joined the Frontline Innovation Program.", "status": "VERIFIED", "url": "https://finviz.com/news/356034/verizon-champions-the-innovators-of-tomorrow-names-winner-of-verizon-frontline-app-developer-challenge"}
- {"fact": "Verizon's Frontline survey, published Oct 13, 2026: daily AI use in public safety is about 32%, roughly triple 2025. Daily drone/robot use is 26%, up from 15%. Over 77% of respondents name resilience and reliability as their top requirement.", "status": "VERIFIED", "url": "https://www.verizon.com/about/news/verizon-frontline-survey-public-safety-ai"}
- {"fact": "On Jan 14, 2026 a Verizon outage lasted at least 10 hours and hit millions of customers. Phones showed SOS mode and some 911 calls failed. FCC PS Docket 26-21 (DA 26-94) asks whether PSAPs (911 answering centers) got timely, actionable outage notice and whether 911 calls carried caller number and location (ANI/ALI).", "status": "VERIFIED", "url": "https://docs.fcc.gov/public/attachments/DA-26-94A1.pdf"}
- {"fact": "FCC rules require providers to tell affected PSAPs about 911 outages within 30 minutes, with an update within 2 hours. Expanded rules took effect April 15, 2025 according to law-firm and vendor summaries.", "status": "SECONDARY", "url": "https://hwglaw.com/?p=10591"}
- {"fact": "ThingSpace Intelligence 'Wireless Network Performance' APIs exist: near real-time network conditions, coverage and site proximity, 30-day device experience history, and triggers for service-impacting events. They need a Verizon enterprise billing account plus the Intelligence premium bundle. Verizon sells the same data to public safety as Wireless Network Performance Manager.", "status": "VERIFIED", "url": "https://thingspace.verizon.com/documentation/apis/intelligence/wireless-network-performance.html"}
- {"fact": "Verizon's network API page lists Number Verification, SIM Swap, ThingSpace, Voice APIs, device-status and coverage-assessment features. It lists no Quality on Demand and no Device Location API.", "status": "VERIFIED", "url": "https://www.verizon.com/business/solutions/network-apis/"}
- {"fact": "Aduna (Ericsson plus operators; AT&T, T-Mobile and Verizon are US equity partners) said on Feb 26, 2026 that it is the only aggregator with full US CAMARA API coverage (300M+ connections). On July 8, 2026 it introduced carrier Number Verification across all three US carriers as an alternative to SMS codes. Authsignal launched it commercially in the US in October 2026.", "status": "VERIFIED", "url": "https://www.prnewswire.com/news-releases/aduna-with-major-us-carriers-introduces-network-based-authentication-as-an-alternative-to-sms-codes-302819808.html"}

Warnings:
- Do not build on Quality on Demand, Device Location or on-demand slice APIs. I found none live from Verizon or Aduna in the US; only Number Verification, SIM Swap and KYC Match are listed. An 'intent-based slicing API' claim is technically unsupported today.
- Satellite direct-to-cell is a trap for a New Jersey campus. AST and Verizon commercial service is unconfirmed (about 13 satellites in orbit), and Schulman says satellite is rural and complementary. At most, mention it as a fallback.
- NG911 is not a Verizon product line. NJ's ESInet belongs to Lumen (2022, 248 PSAPs), Verizon itself sought deadline waivers, and AT&T is the carrier marketing AI NG911. Frame any 911 idea as carrier-network resilience and awareness, not 'Verizon NG911'.
- The incumbent Circadian's event-capacity and 'no manual event mode' story is now a shipped competitor product (T-Mobile Dynamic CX, June 2026). Verizon also ran real-time event operations at the World Cup. Judges may see it as me-too or as a T-Mobile idea.
- Frontline eligibility for campus police is unconfirmed, the slice needs 5G SA devices, and priority/preemption does not yet work on 5G UW. Do not claim RUPD can get the slice tomorrow; say 'pilot subject to Verizon eligibility'.
- The Jan 14, 2026 outage is sensitive to Verizon. Present it through the FCC docket and the industry-wide 77% resilience finding, as 'we make your network outages survivable and visible', never as Verizon-bashing.

### Rutgers-New Brunswick student pain points, 2024-2026 (buses after the Academy/TripShot switch, Wi-Fi and cellular, safety, game day, basic needs, scams, crisis access), with evidence, sizing, and what they mean for a unique Verizon Smart Campus idea

- {"fact": "The University Senate adopted a bus resolution on Apr 24, 2026. It lists chronic overcrowding, inconsistent arrivals, unannounced driver breaks, an arrival app that is 'not effective', sexual assault, harassment and groping on buses, poor stop lighting, and buses and stops that are not fully ADA compliant. It asks for public bus-capacity data, a real-time problem hotline and dispatch system (including sending a replacement bus after a breakdown), bus and stop cameras, notification of the driver and RUPD in real time when an incident is reported, and wheelchair lifts returned to service.", "status": "VERIFIED", "url": "https://senate.rutgers.edu/wp-content/uploads/2026/04/Resolution-for-the-Improvement-of-the-Bus-Transportation-at-RU-New-Brunwsick.pdf"}
- {"fact": "In its reply (May 22, 2026), the administration says students helped write the KPIs in the new bus contract. It says a six-month performance review 'can be provided after January 2027'. That falls right before Round 2 (Feb 3, 2027) and the finals (Mar 4, 2027).", "status": "VERIFIED", "url": "https://senate.rutgers.edu/wp-content/uploads/2026/05/RE-Resolution-for-the-Improvement-of-Bus-Transportation-at-RU-New-Brunswick-.pdf"}
- {"fact": "The New Brunswick bus service-level agreement runs Jul 1, 2026 to Jun 30, 2027. Its KPIs: on-time performance, missed trips with root-cause analysis, field-supervisor coverage, at least 95% preventive-maintenance compliance, no more than 1 preventable accident per 50k miles, fewer than 1 driver incident per 100k miles, 90% of complaints acknowledged within 24h and resolved within 48h, and no more than 10% escalated. Nothing measures crowding, load factor, pass-ups (bus too full to board), bunching or headway, or rider wait time. Those are exactly the problems students complain about. TripShot is named as the official app, and the Knight Mover late-night service (3-6 AM Mon-Thu) can only be booked by phone.", "status": "VERIFIED", "url": "https://ipo.rutgers.edu/sla/dots/nb"}
- {"fact": "Academy Bus Lines began full-scale New Brunswick student shuttle service in fall 2026 (press release, Sept 3, 2026; Rutgers selected it on Mar 17, 2026), and TripShot replaced Passio as the official tracker on July 1. Wikipedia gives the contract end as June 30, 2046 (secondary source).", "status": "VERIFIED", "url": "https://academybus.com/news/details/rutgers-university-fall-semester-shuttle-service"}
- {"fact": "Early student reaction to the new buses is partly positive. The Targum (Sept 10, 2026) quotes a senior calling them 'pretty solid'. Students still want more LX and weekend buses, and the administration says year one will focus on driver breaks and an accurate on-time rate. A RUSA town hall for feedback was scheduled for Thu Oct 22, 2026. The Targum returns 403 to automated fetches, so this comes from search snippets only.", "status": "SECONDARY", "url": "https://www.dailytargum.com/article/targum-exclusive-academy-ushers-in-new-era-of-rutgers-buses-20260910"}
- {"fact": "Ridership numbers conflict. The '70,000 daily New Brunswick riders, 60 buses, 25.55M per year' figures come from a Rutgers advertising media kit (Feb 2025), and the same kit also shows '55,000 Daily Bus Riders'. Academy's own release says Rutgers' transportation system moves 'more than six million passengers each year'. A 2008 Rutgers News article said 65,000 per day.", "status": "SECONDARY", "url": "https://communications.rutgers.edu/sites/default/files/MSS_Media_Kit.pdf"}
- {"fact": "The standard New Brunswick schedule has eight 80-minute periods a day with exactly 30-minute gaps (8:30, 10:20, 12:10, 2:00, 3:50, 5:40, 7:30, 9:20). Movement across campus, and demand on buses and networks, surges in sync up to eight times a day.", "status": "VERIFIED", "url": "https://scheduling.rutgers.edu/?p=1562"}
- {"fact": "xRadar, a third-party app from X Radar, Inc. that the Senate resolution endorsed, already shows live passenger capacity per Rutgers bus, ETAs and alerts (4.5 stars from 62 ratings). Bus apps built before it: 'RU RealTime' (2017, crowd sensors), the HackRU entry 'ru moving' (bus ETAs), and RU There Yet and RURadar (bus trackers covered by the Targum). A bus-crowding app for riders would not be unique.", "status": "VERIFIED", "url": "https://apps.apple.com/us/app/xradar/id6472299023"}
- {"fact": "Rutgers IT, FY2025 (all campuses): 167,222 wireless devices connected on an average day, 14,421 access points, 394,231 devices onboarded. Rutgers installed 12,550 new Juniper Mist APs in 2024-25, adding the newest Wi-Fi frequency band.", "status": "VERIFIED", "url": "https://it.rutgers.edu/wp-content/uploads/2025/11/AnnualReview24-25-Nov19Web-final.pdf"}
- {"fact": "eduroam became the primary network on Sept 29, 2026, and RUWireless Secure will be turned off on Jan 5, 2027. The Wi-Fi page also says RUWireless (the guest network) is used to onboard devices to eduroam. Every student device has to migrate about four weeks before Round 2.", "status": "VERIFIED", "url": "https://it.rutgers.edu/2026/09/22/wi-fi-at-rutgers-is-moving-to-eduroam/"}
- {"fact": "Rutgers IT's 2026 alert log has 7 campus network connectivity incidents between January and October. One on Oct 12, 2026 ran from 8:09 AM to 2:06 PM on a weekday and needed help from an outside provider. A separate Oct 14 incident blocked the RBHS networks.", "status": "VERIFIED", "url": "https://it.rutgers.edu/alerts/"}
- {"fact": "Verizon had a nationwide outage on Jan 14, 2026. Rutgers IT posted an alert at 2:58 PM, and Verizon reported it resolved at 10:31 PM. Press reports put it at about 10 hours, with phones stuck in SOS mode, possible problems reaching 911, and a $20 credit.", "status": "VERIFIED", "url": "https://it.rutgers.edu/alerts/2026/01/14/verizon-outage-affecting-various-internet-phone-and-other-communications-services/"}

Warnings:
- '295 new blue-light phones' is unconfirmed. The only verified number is 145 Knightscope devices (138 towers and 7 E-Phones) in 2023. Do not use 295.
- 'About 110,000 wireless devices a day' is out of date. Rutgers IT FY2025 reports 167,222 average daily devices and 14,421 APs, university-wide rather than New Brunswick only.
- 'RUWireless shut off in early Jan 2027' is imprecise. The IT news post says RUWireless Secure goes off on Jan 5, 2027. RUWireless (guest) is described as the eduroam onboarding network, although one line on the Wi-Fi page says 'RUWireless' and is ambiguous.
- '70,000 daily bus riders / 60 buses' comes from an advertising media kit that also prints 55,000. Academy says more than 6M passengers a year. Cite these as approximate or give a range.
- The buses may have improved since Academy took over: early Targum quotes are partly positive. Pitching 'the buses are broken' with 2016-2024 complaints is risky. Get fresh data from fall 2026, especially LX, weekends and class-change peaks.
- A bus crowding or ETA app is not unique. xRadar already shows live capacity and the Senate endorsed it, and RU RealTime, ru moving, RU There Yet and RURadar came before. In 2018 Rutgers also planned passenger counters and onboard bus Wi-Fi (Targum), so APC data may exist. Ask DOTS before claiming a gap in sensing.

### Campus life-safety and 911 at Rutgers and US universities: wireless 911 routing (sector vs FCC location-based routing), RUSSECC's role, z-axis and dispatchable location rules (wireless, Kari's Law and RAY BAUM'S Act for MLTS), NJ NG911, Clery alert duties, WEA geotargeting, cardiac arrest, overdose and severe-weather gaps

- {"fact": "The FCC location-based routing (LBR) order (FCC 24-4, adopted Jan 25 2024) took effect May 13 2024. Nationwide carriers had 6 months to route wireless 911 voice calls by location, a deadline of about Nov 13 2024. Non-nationwide carriers had 24 months (about May 13 2026). All carriers had 24 months for RTT. Both deadlines have now passed.", "status": "VERIFIED", "url": "https://www.govinfo.gov/content/pkg/FR-2024-03-13/html/2024-03157.htm"}
- {"fact": "LBR is required only when the caller's location is known within a 165 m radius at 90% or higher confidence. Otherwise carriers fall back to 'best available' routing, which in practice is tower or sector routing. The rule covers only IP networks (4G LTE, 5G), not legacy TDM.", "status": "VERIFIED", "url": "https://www.govinfo.gov/content/pkg/FR-2024-03-13/html/2024-03157.htm"}
- {"fact": "Scale of misroutes under legacy routing: ATIS estimates about 12% of wireless 911 calls are misrouted, and NENA about 23M calls a year. A misroute adds roughly 1 minute, and each transfer takes 15-90 seconds to set up. Transfers waste more than 200,000 hours a year of 911 staff time. The FCC estimated 13,837 lives saved a year from a 1-minute faster response. US wireless 911 voice volume was about 158M calls in 2022.", "status": "VERIFIED", "url": "https://www.govinfo.gov/content/pkg/FR-2024-03-13/html/2024-03157.htm"}
- {"fact": "Misroutes cluster along PSAP boundaries, in areas with many PSAPs, around major water features, and along narrow strips of jurisdiction (ATIS). Palm Beach saw at least 11% misroutes overall and 20-50% along PSAP boundaries under tower routing. The FCC itself says calls near boundaries can still be misrouted under LBR if PSAP boundary maps are out of date.", "status": "VERIFIED", "url": "https://docs.fcc.gov/public/attachments/FCC-24-4A1.pdf"}
- {"fact": "Measured LBR effects: AT&T says 10% of its wireless 911 calls got a better route and avoided a transfer. In a Texas beta, transfers fell about 4-5% at 2 of 3 PSAPs.", "status": "VERIFIED", "url": "https://docs.fcc.gov/public/attachments/FCC-24-4A1.pdf"}
- {"fact": "Z-axis rule: nationwide carriers had to deploy z-axis or dispatchable location nationwide by April 3 2025, and non-nationwide carriers by April 3 2026. The standard is +/-3 m for 80% of indoor calls, reported as Height Above Ellipsoid (HAE). Apple HELO and Google ELS together passed the +/-3 m / 80% test.", "status": "VERIFIED", "url": "https://docs.fcc.gov/public/attachments/FCC-25-22A1.pdf"}
- {"fact": "In the March 2025 Sixth FNPRM (FCC 25-22), the FCC says the z-axis data PSAPs receive is 'frequently not actionable'. APCO says few 911 centers can use HAE. The FCC proposed reporting height above ground level and asked about floor-level estimates. Whether final rules have been adopted as of Oct 2026 could not be confirmed.", "status": "VERIFIED", "url": "https://docs.fcc.gov/public/attachments/FCC-25-22A1.pdf"}
- {"fact": "Only about 0.89% of live wireless 911 calls from the nationwide carriers (2023 through part of 2024) carried a dispatchable location (street address plus floor or room). That is 310,542 calls in total. The rule has required dispatchable location 'if technically feasible' since Jan 6 2022, with no benchmark.", "status": "VERIFIED", "url": "https://docs.fcc.gov/public/attachments/FCC-25-22A1.pdf"}
- {"fact": "The FCC asks whether carriers should be required to plan for dispatchable location where calls come from indoor spaces with Wi-Fi APs, femtocells or IoT devices that can be mapped. It asks about the accuracy of programming APs with street address and floor, and about small cells and DAS, smart-building sensors, Wi-Fi RTT (802.11mc), 5G positioning, and benchmarks for multi-story office and apartment buildings, hotels and similar sites.", "status": "VERIFIED", "url": "https://docs.fcc.gov/public/attachments/FCC-25-22A1.pdf"}
- {"fact": "Verizon told the FCC it has started delivering dispatchable location for some 911 calls over Wi-Fi Calling and indoor DAS. It also said third parties' 'business and policy priorities' do not always line up with carriers' E911 compliance needs. Device-based hybrid location was used for about 80% of wireless 911 calls by 2022, up from 17% in 2017.", "status": "VERIFIED", "url": "https://docs.fcc.gov/public/attachments/FCC-25-22A1.pdf"}
- {"fact": "RUSSECC is a full PSAP, staffed 24/7 and CALEA-accredited. It dispatches RUPD and EMS for all Rutgers campuses and transfers calls outside its jurisdiction. It also handles 911 and dispatch for the City of New Brunswick, Metuchen and Middlesex College (agreement of July 17 2023), and answers Text-to-911 for all of Middlesex County.", "status": "VERIFIED", "url": "https://middlesexcollege.edu/campus-safety/"}
- {"fact": "Rutgers says all 911 calls made on its campuses reach RUSSECC first. No public source explains how wireless voice calls from Busch and Livingston (in Piscataway, across the Raritan from New Brunswick) are routed. It is unconfirmed whether they reach RUSSECC directly under LBR or go to the Piscataway or county PSAP and are transferred.", "status": "UNVERIFIED", "url": "https://ipo.rutgers.edu/node/1092"}

Warnings:
- Do NOT pitch location-based routing as new. Nationwide carriers including Verizon had to route by location by about Nov 13 2024, and the remaining deadlines passed in May 2026. The gaps are fallback when there is no 165 m/90% fix, stale PSAP boundary maps, and lack of room or floor detail.
- Do NOT claim carriers send no vertical location. Z-axis (+/-3 m, 80% of calls) has been required nationwide since April 2025. The real problem is that HAE is not usable and floor is not given. The FCC 25-22 changes (height above ground, floor level, dispatchable-location benchmarks) were proposals as of March 2025; check docket 07-114 for any 2026 order before claiming they are final.
- Dispatchable location is required only 'if technically feasible', with no numeric benchmark. Do not say Verizon is out of compliance; frame the project as helping Verizon scale something it already does for Wi-Fi and DAS.
- Never place test calls to 911. Validate with the device's own location APIs, mock PSAPs, and only PSAP-coordinated tests. NJ penalizes 911 misuse (exact statute not checked).
- Do not claim Rutgers violates Kari's Law. The 'obtain an outside line' text may be out of date, or the phone system may be grandfathered (installed before Feb 16 2020). Ask OIT.
- The claim that Busch and Livingston wireless calls are transferred from Piscataway is UNVERIFIED. Rutgers says all campus 911 calls reach RUSSECC first. Get RUSSECC or OPRA data before citing a number.

### Emerging 3GPP / 5G-Advanced capabilities (Rel-17 to Rel-20) a Rutgers team could demo on COSMOS/WINLAB or cheap hardware by Feb 2027: maturity, Verizon status, demoability and campus use cases. Method note: the shared WebSearch budget was already used up when this agent started, so every fact below comes from WebFetch of primary pages (3GPP, eCFR via Cornell LII, GitHub, COSMOS wiki, Verizon, Rutgers) or is labelled SECONDARY or UNVERIFIED.

- {"fact": "3GPP Release 19 is complete, with 'fully implementable specifications at the end of December 2025'. It is the second 5G-Advanced release.", "status": "VERIFIED", "url": "https://www.3gpp.org/specifications-technologies/releases/release-19"}
- {"fact": "Release 20 is the last release that is only 5G-Advanced (it also hosts the 6G studies; normative 6G work is in Rel-21). Stage 2 freeze was Sept 2026, Stage 3 is targeted for March 2027 and ASN.1/OpenAPI freeze for June 2027. Listed focus areas include energy efficiency, AI/ML, satellite/NTN, and 'Sensing + Communications'. Nothing that is still Rel-20 will be in commercial networks by the Feb 2027 poster.", "status": "VERIFIED", "url": "https://www.3gpp.org/specifications-technologies/releases/release-20"}
- {"fact": "3GPP Ambient IoT exists only as studies. Rel-18 TR 38.848 was finalised Sept 2023. The Rel-19 study FS_Ambient_IoT_solutions (TR 38.769, rapporteur CMCC) ran Dec 2023 to Dec 2024 and covers about 1 uW to 10 mW backscatter and self-carrier devices. TR 38.769 was re-issued as v20.0.0 in March 2026. No commercial 3GPP ambient-IoT tag, reader or network exists. Whether there is a normative work item is UNVERIFIED.", "status": "VERIFIED", "url": "https://www.3gpp.org/ftp/Specs/archive/38_series/38.769"}
- {"fact": "Battery-less ambient IoT that works today is Bluetooth-based (not 3GPP). Example: Walmart announced a large ambient-IoT sensor deployment in October 2025.", "status": "SECONDARY", "url": "https://en.wikipedia.org/wiki/Ambient_IoT"}
- {"fact": "ISAC is still at requirements and study stage. The Rel-19 study TR 22.837 (v19.4.0, June 2024) covers intruder detection, object tracking, weather and similar uses. The service requirements spec TS 22.137 now has Rel-20 and Rel-21 versions, both dated 2 Oct 2026, under the Rel-20 'Sensing' work items. No operator ISAC service exists, and Verizon has no ISAC deployment (absence UNVERIFIED).", "status": "VERIFIED", "url": "https://www.3gpp.org/ftp/Specs/archive/22_series/22.137"}
- {"fact": "The AI/ML air-interface study (Rel-18 TR 38.843) covers three use cases: CSI compression and prediction, beam-management prediction, and positioning (direct AI/ML 'fingerprinting' and AI-assisted). TR 38.843 v18.0.0 was published Jan 2024 and a v19 in Sept 2025. TS 38.305 (positioning stage 2) is at Rel-19 v19.3.0 (Sept 2026), and per an AI summary on whatthespec it includes AI/ML downlink positioning and sidelink positioning.", "status": "VERIFIED", "url": "https://www.3gpp.org/technologies/ai-ml-nr"}
- {"fact": "NTN by release: Rel-17 was the first normative NTN (transparent payload, bands n255/n256, UEs must have GNSS). Rel-18 added network-verified UE location and Ka-band. Rel-19 adds regenerative payload (gNB functions on the satellite), RedCap UEs over NTN and store-and-forward IoT-NTN.", "status": "VERIFIED", "url": "https://www.3gpp.org/technologies/ntn-overview"}
- {"fact": "Verizon direct-to-device status: a $100M AST SpaceMobile partnership (May 2024) using 850 MHz, and an FCC test authority (Jan 2025). AST's BlueBird 7 was lost after launch in April 2026, and there is no US commercial launch date. Skylo (3GPP Rel-17 NTN) has offered satellite SOS since Aug 2024 and SMS since Mar 2025 on Pixel 9 and Verizon Galaxy S25 models. These are texting and SOS only, not campus broadband.", "status": "SECONDARY", "url": "https://en.wikipedia.org/wiki/AST_SpaceMobile"}
- {"fact": "srsRAN Project features: 4x4 MIMO, slicing (24.10), NTN GEO (24.04), split 7.2 Open Fronthaul (23.10), E2 with KPM and RC service models (23.10), UL-MIMO using SRS (25.04). Release 25.10 (Nov) split CU-CP and CU-UP. Neither the feature list nor the release notes mention positioning (PRS, LMF, NRPPa), RedCap or energy saving.", "status": "VERIFIED", "url": "https://github.com/srsran/srsRAN_Project/releases"}
- {"fact": "The OpenAirInterface gNB feature set lists Rel-16 PRS generation, nrUE time-of-arrival estimation, NRPPa with UL-TDOA positioning, 'initial support for RedCap' (gNB MAC, RedCap and normal UEs together), NTN-LEO support in RFsimulator, an O-RAN E2 agent (FlexRIC KPM/RC) plus an E3 agent for dApps, and an O-RAN 7.2 O-DU. OAI is the only open stack here with real 5G positioning code.", "status": "VERIFIED", "url": "https://github.com/OPENAIRINTERFACE/openairinterface5g/blob/develop/doc/FEATURE_SET.md"}
- {"fact": "Limits of OAI PRS: only comb sizes 2 and 4, no muting, and it 'can only be validated in phy-test mode'. Using several gNBs needs tight GPSDO synchronisation. It was tested on USRP X310 and N310. ToA is printed in samples.", "status": "VERIFIED", "url": "https://github.com/OPENAIRINTERFACE/openairinterface5g/blob/develop/doc/RUN_NR_PRS.md"}
- {"fact": "The OAI CN5G LMF supports only 1 of 7 TS 23.273 LMF functions: a single location request from the AMF. Periodic and triggered location, positioning-method selection, reporting to a GMLC and assistance-data broadcast are not implemented.", "status": "VERIFIED", "url": "https://github.com/OPENAIRINTERFACE/oai-cn5g-lmf/blob/master/docs/FEATURE_SET.md"}

Warnings:
- The shared WebSearch budget was used up before this agent ran. Facts were gathered by fetching specific primary URLs, so recent Verizon press items (RedCap launches, Verizon network-API catalog, NEAD status) could not be searched and are labelled UNVERIFIED.
- TRAP: COSMOS is mostly NOT on campus. The main outdoor testbed is in West Harlem, NYC. Rutgers-side resources are the Grid and sandboxes at WINLAB (North Brunswick, not Busch) and a single sector in Weeks Hall. Do not claim a 'campus-wide 5G testbed' or multi-cell positioning in Weeks Hall.
- TRAP: srsRAN (OCUDU) has no positioning or RedCap in its published feature list. Positioning demos must use OAI, and OAI PRS works only in phy-test mode (no full attach + LPP flow), has no muting, and its LMF handles only single on-demand requests with no method selection. Claim 'ToA/ranging accuracy on OAI + LMF call flow in a digital twin', not 'sub-meter 5G indoor positioning of phones'.
- TRAP: Commercial phones on Verizon do not expose 5G PRS positioning to apps, and Verizon sells no indoor NR-positioning product (only RTK HPL outdoors and 1 km coarse location). Do not say 'Verizon's 5G already locates you to sub-meter indoors'.
- TRAP: Apple and Google already send device-based hybrid location (GNSS + Wi-Fi) to PSAPs. A 911 idea must target what is still missing: a validated dispatchable building/floor/room, PSAP-boundary routing on campus, and the PIDF-LO/LIS handoff. It is not 'adding GPS'. Whether wireless 911 calls on campus reach RUSSECC directly or via county or municipal PSAPs must be confirmed with RUPD (UNVERIFIED).
- TRAP: Ambient IoT and ISAC are not deployable by Feb 2027. Both are studies or requirements, and Rel-20 Stage 3 freezes March 2027. Calling them 'Verizon-deployed' or 'standardized products' is false. Bluetooth ambient tags (as at Walmart) are not 3GPP.

### What wins Verizon-sponsored university innovation challenges (Smart Campus at Rutgers, NJIT, UT Dallas and Northeastern; other Verizon challenges), who judges, Verizon's 2026 messaging, and what that means for a unique winning idea. Note: the shared WebSearch budget was already used up when this agent started, so every fact below comes from fetching official pages, PDFs, earnings transcripts and SEC filings directly. Items that need search to confirm are marked UNVERIFIED.

- {"fact": "The official Rubric Scoring Guide defines Feasibility LOW as 'Impractical or purely technical, solution would work only in a lab, not realistic for real-world application'. MEDIUM is 'lacks adoption strategies or scalability; limited end-user feedback'. HIGH is 'Real-world, cost-effective solution that can be rapidly prototyped and tested; addresses adoption barriers successfully'. Implication: end-user feedback and adoption barriers are scored explicitly, and a network-internal, lab-only idea scores Low.", "status": "VERIFIED", "url": "https://soe.rutgers.edu/sites/default/files/2025-10/Smart%20Campus%20Competition_%20Rubric%20Scoring%20Guide.pdf"}
- {"fact": "The same guide defines Creativity LOW as 'conventional or replicates existing ideas' and HIGH as 'fresh ideas or approaches not commonly seen in the current market'. Content HIGH is 'backed by data, research, or real-world validation'. Impact HIGH is a 'highly significant problem with multiple beneficiaries impacted; solution addresses a critical real need'. Presentation HIGH is 'captivates the audience, with strong visuals and confident delivery'.", "status": "VERIFIED", "url": "https://soe.rutgers.edu/sites/default/files/2025-10/Smart%20Campus%20Competition_%20Rubric%20Scoring%20Guide.pdf"}
- {"fact": "The Round 1 scorecard asks the following. Significance: 'Is the problem clearly defined?' Ubiquity: 'How pervasive is this problem? How many people does it impact?' Criticality: 'How important is it to address this problem?' Complexity: 'How complete is the solution and the incorporation of Verizon network technologies?' Presentation sub-scores are Organized, Engaged and Clarity, 10 points each. The total is 95.", "status": "VERIFIED", "url": "https://soe.rutgers.edu/sites/default/files/2025-10/Round%201_%20Pitch%20Concept%20%28Video%20Submission%29%20Rubric%20Scorecard.pdf"}
- {"fact": "The General Guidelines frame the challenge as using Verizon 5G 'to enhance a personal experience, focusing on areas like sustainability, connectivity, and personal services'. Judges 'look for creative, well-researched solutions that address a real personal need'. Verizon MENTORS judge Rounds 1 and 2. Winners 'may be invited to expand into a technical trial or business case competition'. Demos 'are not required and will not affect the judging evaluation'. Teams can book 15-minute mentor sessions up to the Round 1 deadline.", "status": "VERIFIED", "url": "https://soe.rutgers.edu/sites/default/files/2025-10/Smart%20Campus%20Competition%20-%20General%20%26%20Round%20One%20Guidelines.pdf"}
- {"fact": "Verizon's AI-use guideline for the competition: 'If AI significantly contributes to your project, be prepared to discuss how it was used and how your team ensured originality'. Teams must fact-check AI output. It also says 'Do not input confidential, personal, or proprietary data into AI systems', which bears on how survey or interview data is handled.", "status": "VERIFIED", "url": "https://soe.rutgers.edu/sites/default/files/2025-10/Guidelines%20for%20Responsible%20AI%20Use.pdf"}
- {"fact": "Rutgers 2024-25 final-round judges, by title. Verizon: SVP for strategy and transformation, AVP for network planning, and Senior Director for network planning. Rutgers: SoE Dean, SVP and Chief Information Officer, and Vice Provost for experiential learning. There were 10 finalists giving 5-minute talks, and the 3 winners then presented at Verizon's Executive Business Center in Basking Ridge. The panel was half network-planning executives and half Rutgers leadership, including the campus CIO.", "status": "VERIFIED", "url": "https://soe.rutgers.edu/news/verizon-smart-campus-competition-winners-deliver-innovative-solutions"}
- {"fact": "Rutgers 2025-26: 7 finalists each gave a 10-minute presentation followed by judges' questions, and 'a panel of Verizon and Rutgers leaders' deliberated. Winners were AeroBin (solar IoT bin sensors at about $100 per unit with AI routing), EchoClass SafeRoute (safety navigation) and RU Experience (web AR stats). Other finalists covered 'sustainability, infrastructure, student safety, wellness, and digital engagement'. No judge commentary was published.", "status": "VERIFIED", "url": "https://soe.rutgers.edu/news/verizon-smart-campus-competition"}
- {"fact": "The 2027 finals event page says 'polished, 5-minute presentation', but the 2025-26 finals actually ran 10-minute talks plus Q&A, and the main-page FAQ says 10 minutes. Talk length is still unresolved.", "status": "VERIFIED", "url": "https://soe.rutgers.edu/event/smart-campus-competition-final-presentations-0"}
- {"fact": "NJIT 2025-26: 198 students; teams narrowed 33, then 15, then 7, then 3. Winners were Decibel (motion and volume sensors for study-space occupancy), Highlanders 4 Highlanders (class group chats with AI-moderated boards) and HOP (campus wayfinding). In Round 2 'every team member delivered part of the pitch', and Verizon judges 'asked hard questions'. Finals went to Verizon senior leadership at Basking Ridge HQ. Verizon counted 600+ students and 150 teams across 4 schools. A Verizon SVP said: 'This is just like the real world'.", "status": "VERIFIED", "url": "https://news.njit.edu/verizon-5g-smart-competition-presented-challenge-students-njit-had-solutions"}
- {"fact": "UT Dallas 2025-26 winners: NOTED (AI plus edge over Verizon private 5G with medical AR glasses, sold by subscription); Vanguard ('premium network routing' for first responders and medics in danger zones); and Smart Compass (centimeter-accurate indoor navigation, funded by ads plus B2B crowd analytics). An associate director in Verizon's Tech Ambassador Office praised 'practical, 5G-enabled solutions that addressed real-world challenges' and said the work 'sparked internal discussions at Verizon'. The format was Shark Tank-style, and winners pitched at Verizon's Irving, TX office.", "status": "VERIFIED", "url": "https://news.utdallas.edu/students-teaching/smart-campus-competition-finals-2026/"}
- {"fact": "Northeastern (Khoury) 2025-26 winners: VitaLink (5G with federated-learning patient monitoring), FoodTrace (food-pantry inventory) and a Real-Time Crash Defense System (Verizon Smart Intersections, AI dashcams and V2X). The source page returned 503 and failed TLS, so this comes from earlier search snippets only.", "status": "SECONDARY", "url": "https://www.khoury.northeastern.edu/in-verizon-competition-khoury-students-pioneer-solutions-for-road-safety-food-insecurity-and-health-care/"}
- {"fact": "Rutgers Business School's Verizon Go-to-Market pilot drew about 400 students on 90 teams, who wrote GTM plans for earlier SoE winners. The winning RU360 plan for UNIVIEW stressed 'scalability to other campuses and stadiums'. No Verizon judge quotes were published. Implication: past SoE winners are turned into business cases, so scalability beyond one campus counts.", "status": "VERIFIED", "url": "https://www.business.rutgers.edu/news/verizon-competition-students-valued-experience-much-prize"}

Warnings:
- CROWDED, ALREADY-WON CATEGORIES: occupancy and space-finding (UNIVIEW, NJIT Decibel); navigation and wayfinding (HOP, Smart Compass, SafeRoute); AR overlays (AccessED, RU Experience, NOTED); course and social apps (RUNetworking, Highlanders 4 Highlanders); smart bins (AeroBin). The rubric scores 'replicates existing ideas' as LOW creativity. A crowd or quiet-space navigator is squarely in this zone.
- SAFETY-WALK APPS ARE DOUBLY TAKEN. SafeRoute won at Rutgers in 2026, and Verizon Family already includes 'Safe Walk' at no extra cost (Oct 14, 2026 release). A safety idea must be network-side (slicing, priority, resilience), not a routing app.
- NETWORK-INTERNAL OPTIMIZATION TRAP. RAN energy saving, RIC xApps or a pure digital twin risk Feasibility LOW ('purely technical, solution would work only in a lab'). They also score weakly on Ubiquity and the guideline's 'real personal need'. Circadian's own evidence (about 0.3% campus-year radio gain) makes this worse.
- SUSTAINABILITY FRAMING RISK (inference). Verizon's current Environmental and Responsible Business pages lead with disaster resilience and show no climate target. A carbon-only pitch may land weaker than a resilience framing. Do not claim Verizon dropped its climate targets; that is unverified.
- DO NOT CLAIM priority and preemption on 5G Ultra Wideband. Verizon says it is 'not available on 5G Ultra Wideband at this time'. Frame this carefully as a gap the idea fills, not a criticism.
- OUTAGE SENSITIVITY. The January 2026 outage is verified, but date, duration and cause were not found, so don't state them. Frame the pitch as resilience with Verizon as the hero, not as blame.

### Identity, fraud and cybersecurity at universities and carriers (2024-2026): SIM swap and account takeover, MFA fatigue and Duo at Rutgers, ghost students, scams aimed at students, carrier network APIs (Aduna/CAMARA) and how much is lost. Method note: the shared WebSearch budget was already used up when this agent started, so every fact below comes from fetching known primary-source URLs directly (PDFs pulled and text-extracted where needed).

- {"fact": "On July 8, 2026, Aduna launched carrier Number Verification across the U.S. with AT&T, T-Mobile and Verizon, with one integration covering all three. It confirms the number, SIM and device in real time with no SMS code. Aduna says it now works 'across all major operating systems and network types', which fixes the old limit that silent auth failed on Wi-Fi. Verizon Business is quoted in the release.", "status": "VERIFIED", "url": "https://www.adunaglobal.com/resources/aduna-with-major-us-carriers-introduces-network-based-authentication-as-an-alternative-to-sms-codes-1/"}
- {"fact": "Aduna's API roadmap (global page, not U.S.-specific). Live or in development: Number Verification, SIM Swap, KYC Match (checks name, DOB, address and email against carrier records without returning PII). 'Available soon / commercially ready later in 2026': Device Swap, Call Forwarding Signal, SCAM Signals/Call State ('detect social engineering during live transactions'), SIM Swap Subscriptions, KYC Tenure (how long the person has held the number), Number Recycling, Device Reachability, Age Verification.", "status": "VERIFIED", "url": "https://www.adunaglobal.com/work-with-us/availability/"}
- {"fact": "Aduna is a joint venture of Ericsson and 12 operators, including Verizon, AT&T and T-Mobile. It is built on the CAMARA standards (GSMA/Linux Foundation). Developers reach it through Google Cloud, Infobip, Sinch and Vonage.", "status": "VERIFIED", "url": "https://www.adunaglobal.com/resources/aduna-with-major-us-carriers-introduces-network-based-authentication-as-an-alternative-to-sms-codes-1/"}
- {"fact": "Twilio Lookup SIM Swap is in Private Beta. The United States is on its coverage list. It needs carrier registration and approval (2-4 weeks, possibly longer), bills per request, and in beta may not cover every major carrier.", "status": "VERIFIED", "url": "https://www.twilio.com/docs/lookup/v2-api/sim-swap"}
- {"fact": "Twilio Verify Silent Network Auth is available in 9 countries, including the US, and takes 2-4 seconds per check.", "status": "VERIFIED", "url": "https://www.twilio.com/docs/verify/sna"}
- {"fact": "Vonage 'Silent Authentication Advanced' uses GSMA TS.43 SIM cryptography and works over cellular, Wi-Fi and VPN. Test access is available through Vonage's Network Registry. Production use needs operator approval. Vonage Identity Insights bundles SIM swap, original carrier and subscriber match. This is a practical sandbox route for an undergraduate demo.", "status": "VERIFIED", "url": "https://developer.vonage.com/en/verify/concepts/silent-authentication"}
- {"fact": "FBI IC3 2025: 1,008,597 complaints and $20.877B in losses (+26%). Ages 20-29: 112,069 complaints and $563.1M lost. Under 20: 31,254 complaints and $67.1M. The 2024 total was $16.6B.", "status": "VERIFIED", "url": "https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf"}
- {"fact": "SIM swap is small and shrinking in IC3 data: 2,026 complaints / $72.65M (2022), 1,075 / $48.8M (2023), 982 / $25.98M (2024), 971 / $17.37M (2025). In 2025, only 61 complaints and $153,247 came from people aged 20-29.", "status": "VERIFIED", "url": "https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf"}
- {"fact": "Losses from employment (job) scams reported to IC3 rose 5x in two years: $70.2M (2023), $264.2M (2024), $362.9M (2025, 24,688 complaints). Government impersonation: $797.9M in 2025. Phishing/spoofing: 191,561 complaints and $215.8M.", "status": "VERIFIED", "url": "https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf"}
- {"fact": "IC3 received more than 75,000 sextortion submissions in 2025. Ages 20-29 were the largest group (22,061), ahead of under-20 (11,316). Extortion overall: 89,129 complaints.", "status": "VERIFIED", "url": "https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf"}
- {"fact": "FTC 2024: consumers reported losing more than $12.5B to fraud (+25%). Job and employment-agency scams: $501M, up from $90M in 2020. Imposter scams: $2.95B.", "status": "VERIFIED", "url": "https://www.ftc.gov/news-events/news/press-releases/2025/03/new-ftc-data-show-big-jump-reported-losses-fraud-125-billion-2024"}
- {"fact": "FTC: reported losses to text-message scams were $470M in 2024, more than 5x 2020. The top types were fake package delivery, fake task jobs, fake fraud alerts and toll scams.", "status": "VERIFIED", "url": "https://www.ftc.gov/news-events/data-visualizations/data-spotlight/2025/04/top-text-scams-2024"}

Warnings:
- Search limit: WebSearch was exhausted before this agent ran (200 per turn, shared across agents). Everything here came from direct fetches of known primary URLs. ed.gov, fcc.gov, cisa.gov, gao.gov and github.com blocked access. The ED June 2025 ghost-student figures ($90M, $30M to the dead, FAFSA ID requirement) and the Salt Typhoon/CISA advice are unconfirmed. Verify them before putting them on a slide.
- Do not headline SIM swap for students. IC3 shows it is small and falling ($72.7M in 2022, $17.4M in 2025), with only 61 complaints and about $153K from ages 20-29 in 2025. Student harm is concentrated in job, impersonation and extortion scams and in account takeover. SIM swap works only as one input signal, not as the problem statement.
- The SCAM Signals/Call State, Call Forwarding Signal, KYC Tenure and Number Recycling APIs are listed as 'available soon / later in 2026' on a global page, not confirmed live in the U.S. Only Number Verification has a confirmed U.S. launch (July 8, 2026). U.S. SIM Swap is in Twilio private beta and needs carrier approval (2-4+ weeks). Label anything mocked or simulated as such, or judges will catch it.
- Carrier APIs are not open to students by default. Aggregators (Vonage Network Registry, Twilio) require registration and operator approval and bill per request. Start sandbox applications in November, and build the WINLAB/COSMOS emulation as a fallback.
- 'Silent auth fails on Wi-Fi' is outdated for Aduna and Vonage TS.43 (both say they work over Wi-Fi), but Twilio's SNA still depends on a cellular data session. State which path you use, especially since campus phones sit on eduroam.
- Verizon's own 2026 DBIR says the top initial-access vector in education is exploited vulnerabilities (34%), not phishing (22%) or credential abuse (8%). An identity product addresses social engineering and account takeover, not the biggest breach vector. Say so before a judge does.

## 3. Screen: 27 concepts distilled from 120 ideas

`total` is the screening composite. `official` is the rubric estimate out of 95. `uniqueness` and `verizon` are 0–10. `convergence` counts how many of the 14 lenses landed on the idea.

| Concept | Total | Official /95 | Unique | Verizon | Convergence |
|---|---|---|---|---|---|
| Last Copper: life-safety lines off Verizon's retiring Piscataway copper | 90.2 | 63.7 | 8 | 7 | 14 |
| Floor Truth: floor, room and seat-level 911 location for every call and text | 90.0 | 65.0 | 8 | 6 | 5 |
| HangUp: the carrier pauses the payment while the scammer is on the line | 88.7 | 62.7 | 8 | 6.666666666666667 | 7 |
| 911 Path Assurance: canaries detect failure in 60 s, the core hands back failed callers | 86.8 | 61.7 | 8.333333333333334 | 5.666666666666667 | 5 |
| Second Witness: network corroboration tells a swatting hoax from a real attack | 86.0 | 62.0 | 8 | 5.333333333333333 | 3 |
| RightRoom: Wi-Fi Calling 911 that knows the room, not your parents' house | 85.8 | 60.3 | 9 | 5 | 8 |
| First Minute: verified AEDs, Narcan and nearby responders the instant a crisis starts | 85.3 | 65.5 | 6.666666666666667 | 4.333333333333333 | 4 |
| Clery Clock: measured time-to-reach for emergency alerts, by carrier | 83.2 | 60.7 | 8 | 4.333333333333333 | 7 |
| Code Path: pager-grade delivery for clinical smartphones at Rutgers Health | 82.2 | 55.2 | 8 | 7.333333333333333 | 4 |
| 988 Bridge: consented crisis-to-911 escalation | 81.8 | 57.3 | 9 | 4.333333333333333 | 1 |
| Exam Lifeline: no student loses an exam to a network failure | 80.8 | 58.3 | 8 | 4.333333333333333 | 4 |
| Trust Tick: carrier-verified landlords and posters before a deposit | 80.7 | 56.7 | 8 | 5.333333333333333 | 4 |
| AlertCell: building-precise alerts by 5G cell broadcast | 80.0 | 58.0 | 8 | 4 | 2 |
| Seismograph: crowd-crush and venue-incident warning fused from network signals | 79.4 | 59.2 | 6 | 5.5 | 4 |
| RU Real?: network-verified Rutgers calls and texts, flagged fakes, scam early warning | 79.0 | 57.7 | 6.666666666666667 | 5.333333333333333 | 3 |
| RainLink: Verizon links as a flash-flood rain gauge | 78.7 | 56.7 | 8 | 4 | 5 |
| LastPath: survivable 911 in every room | 75.2 | 51.7 | 8 | 5 | 2 |
| Verified Silent Reports: bus and place-verified help with no rider tracking | 74.5 | 56.7 | 6.666666666666667 | 3 | 3 |
| Glass Ceiling: green low-E buildings block C-band | 72.7 | 49.7 | 8 | 4.666666666666667 | 2 |
| Pass-Up Ledger: count the riders the full bus left behind | 66.0 | 55.0 | 4 | 2 | 4 |
| Lifeline Video: slice for sign language | 64.3 | 44.7 | 7.333333333333333 | 3.3333333333333335 | 3 |
| Day-Zero Line: verified US number before landing | 60.3 | 41.3 | 6 | 4.666666666666667 | 3 |
| Circadian (incumbent) | 59.7 | 49.3 | 2.6666666666666665 | 3.3333333333333335 | 3 |
| Out-of-band LTE-M safety nodes | 56.8 | 40.0 | 5.666666666666667 | 3.6666666666666665 | 3 |
| Huddle: game-day common channel | 55.7 | 38.0 | 5.333333333333333 | 4.666666666666667 | 2 |
| SIM Is the Key: Passpoint EAP-AKA' on eduroam | 55.0 | 35.3 | 7.333333333333333 | 3.3333333333333335 | 2 |
| Turnover: 5G Home that stays with the rental | 44.8 | 31.0 | 3.6666666666666665 | 4.333333333333333 | 4 |

## 4. Leaderboard after deep dossiers, red teams and judges

| Avg | Judges | Entry |
|---|---|---|
| 94.0 | 3 | Last Copper: find, move and prove every lifeline before the copper goes dark |
| 89.0 | 3 | HangUp: the network speaks up during the scam call |
| 87.8 | 5 | Floor Truth |
| 86.0 | 5 | Heard: 911 Path Assurance |
| 83.5 | 2 | Last Copper |
| 83.5 | 2 | HangUp |
| 81.8 | 4 | First Minute: every AED on campus, live to 911 |
| 79.0 | 1 | Second Witness (revised): floor-level 911 for every phone on campus |
| 79.0 | 1 | First Minute |
| 77.0 | 1 | FirstRing (revised from RightRoom): right 911 center, right floor |
| 74.7 | 3 | FirstRing (revised from RightRoom) |
| 74.0 | 1 | FirstRing |
| 74.0 | 1 | Circadian Headcount (pivot) |
| 72.8 | 4 | Second Witness (revised) |
| 71.5 | 2 | Alert Clock |
| 71.0 | 3 | Circadian Headcount |
| 71.0 | 1 | Circadian (original incumbent, reference only) |
| 69.7 | 3 | Alert Clock (formerly Clery Clock) |
| 69.0 | 1 | Circadian Headcount (pivot of Circadian) |

## 5. Champion: Last Copper: Who Answers? (PROVE-first)

> Verizon is retiring its Piscataway copper (Busch, Livingston and SHI Stadium are in Piscataway) on or after Dec 10, 2026. Last Copper finds the elevator, refuge and fire-alarm lines still on that copper before they are cut, moves each one to a Verizon LTE line, and then tests every line every night: a tone through the car speaker, a tone back through the car mic, the location label checked, and a text mode for Deaf riders. Whoever presses HELP reaches a person, and Verizon has a record showing it works.

### Why it wins
1. The judges already picked it: 94 average, against 89 for HangUp. All three scoring judges named it the winner, on the condition that the Oct 31 gate passes. No other finalist got a "winner" verdict.

2. A default LLM brainstorm cannot reach this idea. The trigger is Verizon New Jersey Copper Retirement Notice 2026-03-A-NJ, published Sept 8, 2026. That is after the training data of the models most teams use (ours ends mid-2026), so a team can only find it by doing live research on Verizon's regulatory disclosures. The crowded LLM space is energy, digital twins, AI-RAN sleep, crowd navigators, smart parking, safety-routing apps, AR, bins and chatbots. Every past winner (UNIVIEW, AccessED, RUNetworking, AeroBin, SafeRoute, AR stats) is a consumer app. Ours is the only entry built on a program Verizon itself is running, with a public date, and that date falls between Round 1 and Round 2. Anyone who converges here anyway still has to match our Rutgers count, our HELP-button audit, our machine-room RF map and a physical rig that works on Verizon's production network.

3. How it scores against the rubric (95 points):
- Impact (30). Criticality is as high as it gets: a person trapped in an elevator, or a fire-alarm path that summons the fire department to an empty building at night. Significance: nobody holds a list of these lines, they fail silently, inspections are annual at most, and a hard cutoff date is forcing every building owner to touch them this winter. Ubiquity: everyone who rides an elevator or occupies a building whose alarm reports over a phone line. That is 46,934 New Brunswick students plus staff across 980+ Rutgers buildings in Phase 2, about 1,566 retiring wire centers nationally in 2026, and the roughly 15% of US adults who report trouble hearing (Deaf text mode, timed to the NJ IBC 3001.2 visual-communication rule, which becomes mandatory around mid-Feb 2027).
- Presentation (30). This is the most tactile demo in the field. Pull the copper and the path goes green. Unplug the antenna and the console reads "RF". The nightly chirp passes. Tape the mic and the test fails with "audio path". Press HELP and the location is announced. Deaf text mode works. The video has three beats: the notice, the chirp, the text.
- Content (15). It runs on Verizon's production network (LTE-M, Cat-1/VoLTE, ThingSpace Connectivity Management and Device Diagnostics, Verizon's POTS-replacement channel) and on the 47 CFR 51.333 / 63.71 retirement process. It is not an open-source core standing in for Verizon, which is the main weakness of HangUp, Heard and FirstRing.
- Feasibility (15). Certified partner hardware, ThingSpace self-serve lines bought with a credit card, no new hoistway wiring, and a per-line fee aimed at or below the current POTS bill.
- Creativity (5). Three parts nobody sells together: a CPNI-safe lifeline finder that runs inside Verizon, an end-to-end acoustic proof that works with any vendor, and a Deaf-mode text channel.

4. A Verizon executive can defend it. Copper retirement is one of Schulman's opex levers and part of the Frontier integration. We claim no copper savings. We claim three things: retention at a forced-migration moment (AirDial is certified on AT&T and T-Mobile, and cable VoIP is named in Verizon's own notice), lower cutover risk (the worst headline is a dead elevator line), and Enterprise & Public Sector growth (revenue $13.5B, down 4.8%) through recurring ThingSpace lines. We publish no invented dollar figures. The CFO tab is a formula the business team fills in with Verizon.

5. It survives its own kill gate. If the Rutgers copper count comes back low, judges said a national-first pitch with Rutgers as the PROVE pilot "keeps most of the score". Silent failure of elevator phones does not depend on copper, so the Rutgers anchor stays either way.

### Relation to Circadian
REPLACE Circadian as champion, and keep its repository as the engineering bench. Red teams killed both Circadian (energy/HVAC/radio sleep: about $3 of venue radio energy per game, ties Verizon's AI on ordinary days, NPV negative without pull-through) and its pivot, Circadian Headcount. No energy, HVAC, slicing or radio-sleep claim goes into the new pitch.

What we reuse (paths under /home/user/verizonsmartcampus):
- prototype/engine/triage.py becomes the PROVE fault triage. The naive-Bayes symptom-to-fault model and playbook structure carry over directly; only the tables change. New faults: rf, power, gateway, audio_downlink (car speaker), audio_uplink (car mic), answering_point_no_answer, location_label_mismatch. New symptoms: heartbeat_lost, rsrp_drop, attach_fail, mains_lost, battery_low, chirp_down_fail, chirp_up_fail, call_setup_fail, no_answer. The playbook becomes a routing table: Verizon, OIT, the elevator contractor, or the answering point. The status-quo comparison (SQ_DETECT, truck-roll probabilities) carries over as "annual inspection vs nightly proof".
- prototype/engine/ledger.py becomes the PROVE evidence ledger: an append-only, hash-chained record of every nightly test, exported as an inspection-ready evidence sheet. It is voluntary documentation, never a compliance claim.
- prototype/server.py plus prototype/dashboard/index.html and data.js become the console: path status per line, test history, HELP queue with location, two-way text chat, and a countdown map of wire centers built only from public notices. The dashboard's dark and light theming and map code are reused.
- prototype/engine/sim.py and demand.py patterns become find/synth.py, a seeded synthetic call-record generator. Device archetypes: fire-alarm communicator with a fixed-interval test call to a central-station receiver, elevator phone (near-idle, occasional short inspection calls), alarm panel, fax/modem/meter, ordinary business voice.
- forecaster.py (ridge solver _solve, evaluate) is the baseline scorer for FIND, with a naive-Bayes or logistic variant. The honest-evaluation habit carries over: FIND must beat a "line-type code only" baseline, or we say it does not.
- CFO_10K_MODEL.py and verizon_10k_sensitivity.csv become the per-wire-center value formula: (lifelines found early x retention uplift x monthly margin x months) + (failed cutovers avoided x cost per incident) + (PROVE lines x price x months). Every input is labeled as an assumption, anchored to FY2025 10-K facts (E&PS $13.5B, -4.8%). The business team arriving in mid-December fills it in.
- scripts/analyze_walktest.py and deliverables/FIELD_KIT_OCT31.md become the machine-room / controller-room LTE-M survey (RSRP, RSRQ, attach success, time-to-attach) with an escort. The Oct 31 game-day crowd study is dropped.
- tests/test_engine.py (31 tests) is the harness. Add test_prove.py, test_find.py and test_triage_routing.py.
- deliverables/JUDGE_QA_DEFENSE_BIBLE.md format and Circadian's habit of honest ablation and reporting null results are our credibility style.
- Optional: scratchpad/soc_in_session.py (the Rutgers timetable occupancy analysis) ranks which buildings' lines PROVE covers first, by people-hours exposed.

Dropped: ran.py, buildings.py (HVAC), slicing.py (intent parser), learning.py (bandit), all energy figures, NPV and ESCO claims.

Narrative reuse: one Q&A line. "Circadian taught us to compare a system's intended state with its measured state. PROVE does that for the one line that must never be silently wrong."

### Full concept
LAST COPPER, revised by the founder. PROVE is the hero, FIND gets one slide, MOVE uses partner hardware.
PILLAR 1, AI-Driven Automation & Efficiency. AI finds hidden lifelines and diagnoses failures, and nightly automated proof replaces the annual manual check. Pillar 3 is mentioned but not claimed.

PROBLEM (verified; the sources are in the dossier)
- Verizon NJ notice 2026-03-A-NJ (Sept 8, 2026) retires copper "at all remaining locations" in 62 NJ wire centers, including Piscataway (4 Skiles Ave, CLLI PSWYNJPI), "on or after December 10, 2026". Verizon may require migration "well before" that date. I re-read the notice text in the scratchpad this pass. New Brunswick is not on the list.
- The rules do not require anyone to find life-safety lines: 47 CFR 51.333 requires 90 days' notice, and 63.71(f)(2) auto-grants discontinuance on day 31. About 1,566 wire centers in 20 states were noticed in 2026 by Verizon and Frontier combined.
- Verizon's own POTS Replacement page names elevator phones, alarm panels and fire alarms, and hands life-safety lines to partners. NJ elevator inspections happen at most once a year. A cellular POTS vendor admits "we don't know if a transmission is successful or not." Failures are silent.
- NJ R.2026 d.086 (effective Aug 17, 2026, with a six-month grace period, so mandatory around mid-Feb 2027 by our inference) restores IBC 3001.2, which requires elevator emergency communication in "both visual and audible" modes for Deaf, hard-of-hearing and speech-impaired riders.

FOUNDER CHANGES TO THE DOSSIER VERSION (what makes it stronger)
1. PROVE leads. FIND is a single slide and a single line in the video. MOVE is certified partner hardware and never our product.
2. Technical fix: two-transducer acoustic test. Hands-free elevator phones run acoustic echo cancellation, which is built to remove the speaker's own signal from the mic. A naive "speaker to mic loopback" may cancel itself and fail on a healthy phone. PROVE therefore tests each direction separately:
   - Downlink: the console plays a chirp, the car speaker emits it, and a small PROVE sensor mic in the car operating panel detects it.
   - Uplink: a small PROVE piezo emits a different chirp, the car's own mic carries it, and the console detects it with a matched filter.
   Taping the car mic fails the uplink test; disconnecting the speaker fails the downlink test. We bench-test echo cancellation in week 1 (Gate B).
3. Location assurance, grafted from Floor Truth and FirstRing. Each HELP event carries a provisioned label (building / car / landing zone), and the nightly test confirms the answering console receives the right one. When a line moves from copper (where location comes from the service-address record) to a cellular gateway (a registered address), a wrong or default address is a new silent failure. PROVE flags any mismatch as a ticket.
4. Cutover Watch for Verizon, grafted from Heard. Nightly PROVE results across every migrated line in a wire center become a cutover-health signal for Network Transformation. Thousands of per-line events are correlated into one wire-center status (green, or "3 lifelines failing since batch 7"), so cutover problems surface in a day rather than after an incident.
5. Inspection-ready evidence record, grafted from Alert Clock. The hash-chained ledger exports a per-car test history that the owner can hand to the elevator inspector or AHJ. It is voluntary documentation and never a compliance claim.
6. Zero-install Phase 2 option. This is subject to Rutgers counsel review because of NJ wiretap law and privacy. Every night at 3 AM, with the car idle, the console calls each real elevator phone number. If the phone auto-answers, the console checks that the line answers and that the car mic carries a non-silent ambient noise floor. A dead mic sends digital silence. Only spectral features are computed; no audio is stored. This lets us pilot dozens of real cars without touching the elevator.
7. Roadmap only, grafted from First Minute and kept out of the video: the same ThingSpace LTE-M endpoint and console supervise other life-safety endpoints on retiring copper or with no monitoring at all (blue-light phones, AED cabinets, fire-alarm communicator paths).

THE THREE VERBS
- FIND runs inside Verizon. Students never see CPNI. It is a classifier that ranks each remaining copper line in a retiring wire center by how likely it is to be a lifeline. Features: periodicity of short calls (autocorrelation or FFT of call times, which is the communicator test-timer signature); calls to known central-station receiver and elevator-maintainer call-center numbers; idle ratio; service-address type. The output is a "move first, never just cut" worklist, optionally ordered by occupancy exposure using Circadian's timetable analysis. We score it on synthetic call records against a baseline that uses only line-type codes. Legal basis: 47 USC 222(c)(1) and (d)(1), for migration outreach only, subject to counsel review.
- MOVE uses Verizon-certified POTS gateways (Inseego BPC100, ATEL V810V, or partner equivalents) on Verizon LTE-M or Cat-1 with VoLTE voice, with 24-hour battery backup per Verizon's spec. They connect at the existing termination in the controller or machine room, so no new hoistway wiring or antennas are needed. Rutgers' wired network is an optional second path where network closets have emergency power (unverified per building).
- PROVE is our layer and works with any vendor. A supervisor (MCU or Pi-class device on its own ThingSpace LTE-M line) does six things:
  (a) a heartbeat plus ThingSpace Connectivity Management and Device Diagnostics state;
  (b) the nightly two-direction acoustic test;
  (c) the location-label check;
  (d) HELP events sent as data, with the location announced at the start of the call;
  (e) two-way text between a car-station display and the console, with tiny payloads suited to LTE-M;
  (f) trend analysis of nightly SNR and frequency response, which warns of a degrading mic or speaker before it fails outright.
  On a failure, the reused naive-Bayes triage labels the cause (RF, power, gateway, uplink audio, downlink audio, answering point, location) and routes the ticket automatically to Verizon, OIT, the elevator contractor or the answering point.

ARCHITECTURE
Car station (push-button HELP, hands-free, visual display) plus PROVE sensor mic and piezo in the car operating panel -> existing traveling cable -> controller/machine room -> certified POTS gateway (LTE-M or Cat-1, VoLTE) plus optional wired IP path -> PROVE supervisor (own LTE-M line) -> ThingSpace APIs plus our console (forked from Circadian's server and dashboard) -> whoever answers Rutgers elevator calls today (RUPD/RUSSECC or the contractor's call center; to be confirmed in the HELP audit). Roadmap: two-way video on 5G SA RedCap. We do not claim slicing.

VERIZON VALUE (no copper savings credited to us)
(a) Retention at a forced-migration moment.
(b) Lower cutover risk: fewer escalations, repeat truck rolls and headlines, with Cutover Watch as the signal.
(c) E&PS growth through recurring ThingSpace lines, plus a public university and PSAP as the reference customer.
Per-line revenue falls when a POTS line ($75-150 per month, vendor claim) becomes a cellular line ($45-55, vendor claim), so the pitch is retention, not per-line growth. The CFO formula has labeled assumptions only.

BUSINESS MODEL
Rutgers pays per line, at or below its current POTS bill (read from the OPRA invoices). PROVE is sold as a ThingSpace add-on or partner-channel feature per line. Target supervisor bill of materials is under $150, and the prototype has to prove it. FIND is an internal Network Transformation tool. Verizon pays no subsidy.

PRIVACY, LEGAL AND SAFETY
- FIND runs only inside Verizon. Given the $46.9M location fine, the team never receives CPNI.
- No personal data. Location is provisioned per device, never tracked.
- Lifeline locations are never published; the public map shows wire centers only.
- No claim of code compliance. Real installs use listed devices, a licensed contractor and AHJ acceptance.
- We never dial 911 and never build fire-alarm communicators.
- Ambient-mic checks only after counsel review, with features only and no recordings.

### Two-minute story (draft)
The script is about 270 words, with two speakers. Every [bracketed] number is filmed only if it has been measured.

0:00-0:10. Real Rutgers elevator, filmed with Facilities' written permission. Doors close, a finger presses HELP, a ring.
V/O: "When you press this button, who answers? And if the line is dead, who would know?"

0:10-0:25. The Verizon notice fills the screen. Highlight: "Piscataway ... on or after December 10, 2026." A countdown ticks. A map shows 62 NJ wire centers, then about 1,566 nationwide.
V/O: "Verizon is retiring the copper in Piscataway, home of Busch, Livingston and the stadium, and in about 1,566 wire centers nationwide this year. Elevator phones and fire alarms ride on lines like these. Nobody has the list, and inspections happen at most once a year."

0:25-0:40. Primary-data montage: the audit clipboard and the numbers.
V/O: "We asked Rutgers: [N] life-safety lines on Verizon copper. We pressed HELP in [N] elevators. [N] answered, median [X] seconds, and [N] knew which building."

0:40-1:20. The rig, live. One screen for FIND (5 s), then hands on hardware.
V/O: "Last Copper finds these lines inside Verizon so they move first, never just get cut. It moves each one to a Verizon LTE line." (Pull the copper wire. The console turns green.) "Then every night it proves the whole path, not just the modem." (Chirp out the speaker, PASS. Chirp back through the car mic, PASS.) "Tape the mic." (FAIL: audio path, ticket to the elevator contractor.) "Unplug the antenna." (RF, ticket to Verizon.) "Press HELP." (The console reads 'Hill Center, Car 2', demo label.)

1:20-1:35. Deaf mode. The car display reads "Help is coming. Are you hurt? YES / NO". A finger taps YES.
V/O: "New Jersey is making elevator help visual as well as audible, for Deaf and hard-of-hearing riders. Last Copper does it today."

1:35-1:50. Three icons.
V/O: "For Verizon: keep the customer at a forced migration, no cutover headlines, and a ThingSpace line in every car."

1:50-2:00. Back to the elevator. The HELP light glows green.
V/O: "Make Rutgers the first campus to prove every lifeline before the copper goes dark. Last Copper."

Rules for the cut:
- Regulatory detail appears as one line of on-screen text at most.
- The rig carries the story.
- Never say "the Piscataway central office serves Busch" until the wire-center check confirms it. Say "copper in Piscataway, home of Busch and Livingston".
- If Gate A fails, the 0:25 beat becomes the HELP-audit numbers plus "every Rutgers elevator line is tested at most once a year", and the 0:10 beat stays national.

### Demo and build plan
Today is Wed Oct 21, 2026, and the video is due in 18 days. A gate is decided at each milestone.

WEEK 1 (Oct 21-27): requests, orders, bench test
- Oct 21-22, outreach:
  - Ask a faculty sponsor (ECE/WINLAB) to co-sign every request.
  - Written request to OIT Telecom and Facilities (elevator shop, fire-alarm shop): how many Verizon NJ loops are billed to Piscataway service addresses, and what each is used for (elevator, refuge, fire-alarm communicator, alarm panel, blue light, fax).
  - File an NJ OPRA request for Verizon NJ invoices and line lists, asking for counts by line type, not locations.
  - Ask RUPD/RUSSECC who answers elevator HELP calls.
  - Contact the Office of Disability Services, and through it a Deaf or hard-of-hearing student.
  - Ask Facilities for permission to run a HELP-button audit with the answering point notified in advance.
- Oct 21-23, purchases (all ship-fast; prices are estimates, about $800-1,500 total plus about $10-40 per line per month):
  - ThingSpace self-serve LTE-M lines (2-3).
  - A Verizon-certified LTE-M dev kit (Nordic nRF91-series DK or Sequans Monarch 2 EVK; confirm Verizon certification).
  - A voice-capable Verizon FXS gateway: Verizon-branded home/business phone base or a certified Inseego/ATEL unit, whichever is in stock first.
  - A hands-free ADA elevator emergency phone (Viking/RATH/Janus class), new or surplus.
  - Raspberry Pi 5 with USB audio, a 3.5" display, piezo plus MEMS mic, and a UPS HAT.
  - An ATA plus Asterisk on a Pi to act as the "copper line" and "central station", labeled as simulated.
- Oct 24-27, Gate B (echo cancellation): bench-test whether the hands-free phone's echo canceller suppresses a speaker-to-mic chirp. We expect it might, so the two-transducer design is the default.
- Gate C (voice): VoLTE through the gateway completes calls to the team console number.

SOFTWARE (Oct 22-Nov 4), all in the existing repo
- prove/supervisor.py: heartbeat (60 s in the demo), scheduler, two-direction chirp test with matched-filter detection and SNR/frequency-response features, HELP event with provisioned label, text relay.
- Console: fork prototype/server.py and dashboard/ to show path status, test history, HELP queue, text chat, and the public-notice countdown map.
- prototype/engine/triage.py: retarget the fault and symptom tables and add a routing table.
- prototype/engine/ledger.py: hash-chained test record plus evidence-sheet export.
- find/synth.py and find/model.py: synthetic call records with documented archetypes, and a scorer reusing forecaster._solve plus naive Bayes. Report precision, recall and PR-AUC against a "line-type code only" baseline.
- cfo/wirecenter.py: formula with labeled assumptions, adapted from CFO_10K_MODEL.py.
- tests/test_prove.py and test_find.py, keeping the suite green.

FIELD (Oct 26-31)
- Visual walk audit of public elevator car stations on Busch and Livingston: push-button vs handset, display yes/no, signage. No permission is needed to look.
- HELP-button audit only with written Facilities permission and a pre-announced test window with the answering point. Measure answer time, whether the answerer knows the building and car, and whether location is announced.
- LTE-M RSRP, RSRQ and attach success at controller and machine-room locations with an escort, using analyze_walktest.py. If no escort, measure at the nearest accessible point and label it as a proxy.

OCT 31: GATE A (founder decision)
- 25 or more life-safety lines on Verizon copper in a retiring wire center: Rutgers-first pitch.
- 1-24, or no answer yet: national-first pitch, with Rutgers as the PROVE pilot site. The video's local beat becomes the HELP audit plus "tested at most once a year".
- OIT confirms zero copper exposure AND Facilities refuses any PROVE pilot: escalate to a switch to HangUp, the 89-point runner-up.

NOV 1-7: film the rig (six beats), the audit footage and the notice graphics; edit to the script; rehearse two speakers; submit Nov 7, one day early.

ROUND 2, FEB 3 POSTER
- Nov: find a Verizon mentor in Network Transformation or Verizon Business POTS replacement. Ask: do you already flag lifelines by line-type code, and where do cutovers stall?
- Nov-Dec: Facilities pilot. Option 1 is a zero-install nightly dial-in check on 10-30 real cars, after counsel review. Option 2 is 1-3 cars with a supervisor box, with the contractor and Facilities.
- Dec 10: Cutover Watch, logging what happens to Rutgers lines around the retirement date (or a post-mortem if they migrated early, which is still a strong story).
- Mid-Dec: the business team fills in the CFO formula.
- Jan: Deaf/HoH user test of text mode, timed to the NJ 3001.2 date (around Feb 17).
- Poster table: the live rig (pull copper, unplug antenna, chirp, tape mic, HELP, Deaf text); Rutgers numbers; FIND precision/recall vs baseline; triage confusion matrix; machine-room RF map; pilot pass/fail history; letters of support (Facilities, RUPD/RUSSECC, Disability Services).

ROUND 3, MAR 4 FINALS
- 6+ weeks of pilot data: failures caught that the annual inspection would have missed (reported honestly, even if zero).
- Verizon feedback, the filled-in CFO tab, and national wire-center rollout logic.
- An AHJ/inspector reaction to the evidence sheet.
- A one-page pilot MoU draft for Rutgers Facilities, with Verizon as the line provider.

### Primary research plan
Goal: by Oct 31, numbers no LLM-only team can produce; by Feb 3, a working pilot. Each item lists owner, deadline and the decision it drives.

1. Copper exposure (Gate A, Oct 31). Sources: OIT Telecom and Facilities written answers, plus OPRA (filed Oct 22, about 7 business days). Count Verizon NJ loops by service address and use, and the serving wire center for each, from the bill's service addresses and circuit IDs. Busch, Livingston, SHI and the RBHS Piscataway (Hoes Lane) buildings are the priority. Cook/Douglass and College Ave are New Brunswick, which is not retiring. Also check Rutgers sites in other listed wire centers (Metuchen, Dunellen, Fords).
2. Who answers (by Nov 3, with permission). HELP-button audit of 15-30 elevators, pre-announced to the answering point and supervised by Facilities. Record answer time, whether the answerer knew building and car, whether location was announced, and text capability. This is the video's cold open.
3. Car-station walk audit (Oct 26-31, visual only, public elevators): push-button vs handset, display present, signage. Gives the baseline for NJ 3001.2 visual communication.
4. RF reality (Oct 26-Nov 7, escorted): LTE-M RSRP, RSRQ, attach success and time-to-attach in controller and machine rooms, with Verizon plus one control carrier labeled "Carrier B". Decides the antenna, Cat-1 fallback and dual-path design.
5. Stakeholder interviews and letters (Oct-Jan):
   - RUPD/RUSSECC: who answers, what they see, would they host test windows;
   - Facilities elevator shop and the elevator contractor: phone models, auto-answer, existing line monitoring;
   - fire safety / fire-alarm shop: how campus fire alarms report, DACT vs campus network;
   - Office of Disability Services plus a Deaf or hard-of-hearing student: text-mode wording and usability;
   - OIT: emergency power in network closets;
   - Rutgers counsel: the ambient-mic dial-in check.
6. Echo-cancellation bench study (Oct 24-27): chirp detection on a real hands-free elevator phone. Single-transducer vs two-transducer, across mic-taped and speaker-disconnected conditions. Reported as measured.
7. FIND evaluation (Oct 22-Nov 4, refined through Feb): synthetic call-record generator built from documented device behaviors (communicator test intervals, elevator-phone idle patterns, central-station numbers). Pre-registered metrics: precision, recall, PR-AUC vs a line-type-code baseline. Rutgers' bill and walk-audit data serve as ground truth for the feature logic only.
8. Pilot data (Nov-Mar): nightly PROVE results on real cars (zero-install dial-in after counsel review, or 1-3 instrumented cars). Measure pass rate, failures found, time-to-detect vs the annual inspection, and false alarms. Null results are published.
9. Verizon validation (Nov-Dec): mentor or business-team questions. Does Verizon already identify lifelines by line type? Where do cutovers stall? Is PROVE a ThingSpace add-on or a partner-channel feature? What are the retention and cutover-incident inputs for the formula?
10. Code and regulatory reads (by Feb 3; the web-search budget ran out this pass, so these are open):
   - the ASME A17.1 edition NJ enforces and its two-way communication monitoring rules;
   - NFPA 72 DACT connection, test-interval and single-path cellular rules;
   - whether IBC 3001.2 applies to existing cars or only to new and altered ones;
   - whether incumbent monitoring firms (e.g., Kings III) already run automated daily line tests. If they do, our claim narrows to end-to-end acoustic proof, location assurance and Cutover Watch.
Ethics:
- No 911 calls ever.
- Test windows are pre-announced in writing.
- No personal data, and no recordings of elevator audio.
- No lifeline location maps are published.
- IRB determination before any survey.
- Findings go to Facilities privately first and are presented in aggregate.

## 6. Runner-ups and what we graft from each

### HangUp: the network speaks up during the scam call (89)
- **Why not champion:** The core feature runs on Kamailio, not on Verizon's network, and a Verizon judge will say so. The red team returned a kill on the 222(d)(2) legal reading. Verified Rutgers harm data is thin until OPRA results arrive. Campus revenue is about $5K a year, and scale depends on banks adopting it.
- **Graft:** The privacy-safe reversed data flow, where an event goes in and only an action comes out, already shapes FIND: it runs inside Verizon on its own CPNI and only the worklist leaves. HangUp is also the designated fallback if Gate A fails AND Facilities refuses any PROVE pilot, because it has the best theater after ours.

### Floor Truth (validated floor for 911 heights)
- **Why not champion:** The improvement comes from building measurement and probability, not from Verizon's network, so Content and Verizon complexity are weak. Verizon money is small. It depends on RUSSECC consent for test calls. The data could show low-rise Rutgers buildings barely need it. The 20-building survey must be done in 17 days.
- **Graft:** Location assurance. PROVE checks that each HELP event and each migrated line carries the right building, car and landing label, so a gateway's default or wrong registered address becomes a ticket instead of a silent failure.

### Heard: 911 Path Assurance
- **Why not champion:** Verizon may already run internal 911-impact KPIs. Production counters are often 15-minute bins. The IMS and 911 legs are simulated on open-source cores. The money is compliance and trust only. The framing sits close to Verizon's Jan 2026 outage, which is risky in front of Verizon judges.
- **Graft:** Alarm correlation and the 'witness' framing, turned into Cutover Watch. Thousands of nightly PROVE results become one wire-center health status for Network Transformation, plus the principle that failures nobody counts must be counted.

### First Minute: every AED on campus, live to 911
- **Why not champion:** Verizon money is a rounding error ($1.50 per device per month). Avive and PulsePoint already cover most functions. Campus cardiac arrests are rare, which weakens Ubiquity. Reading the AED status indicator is unproven.
- **Graft:** (1) Its filmed, timed field test ('find the AED in 3 minutes') becomes our pre-announced HELP-button audit and video cold open. (2) The same ThingSpace LTE-M endpoint and console extend to AED cabinets and blue-light phones as a roadmap-only Phase 3.

### Second Witness / FirstRing (campus 911 routing and floor)
- **Why not champion:** Red-team kills on both. The routing premise may simply be false if location-based routing already lands calls at RUSSECC. Nothing can be built natively in Verizon's E911 path by students. Floor-level vendors (RapidSOS/GeoComm) already exist. There is no P&L.
- **Graft:** Stakeholder questions for RUSSECC (what the dispatcher actually sees) feed our 'who answers' interview. The PIDF-LO-style labeled location is a format option for HELP events reaching a NG911-ready answering point.

### Alert Clock (time each stage of a Rutgers alert and add the WEA broadcast path)
- **Why not champion:** No revenue by law (47 USC 1201). The headline finding ('use WEA') may already be true at Rutgers. The biggest delay is the human decision, which this project does not fix. It reads as a critique of Rutgers OEM in front of university leadership.
- **Graft:** The voluntary 'evidence sheet' becomes PROVE's inspection-ready, hash-chained test record per car, plus its measurement-study discipline: pre-registered metrics and published nulls.

### Circadian and Circadian Headcount (incumbent and pivot)
- **Why not champion:** Both were killed by the red team. Radio value is about $3 per game, ordinary days tie with Verizon's AI, Wi-Fi does the sensing, NPV is negative without pull-through, and the energy and digital-twin space is crowded with LLM-assisted teams. The Headcount pivot depends on carrier APIs Verizon does not offer and overlaps with Mist occupancy.
- **Graft:** The code bench (triage, ledger, console, synthetic-data generator, CFO formula, walk-test analyzer, tests) and the Rutgers timetable occupancy analysis, used to order the FIND/PROVE rollout by people-hours exposed.

## 7. Open questions handed to Generation 4

- GATE A: How many Rutgers life-safety lines (elevator, refuge, fire-alarm communicator, alarm panel, blue light) ride Verizon NJ copper, and which central office serves each one? Piscataway PSWYNJPI or New Brunswick, which is not retiring. Township is not wire center, so this has to come from the bills' service addresses and circuit IDs, not from the map.
- Has Verizon already notified Rutgers, or has OIT already migrated these lines (to Rutgers' Cisco/Teams PBX, AirDial or another carrier) before Dec 10? If so, does 'Cutover Watch / post-mortem' beat 'countdown' for the Feb 3 poster?
- Who actually answers a Rutgers elevator HELP call today (RUPD/RUSSECC, the elevator contractor's call center, or a third-party monitoring firm)? How fast, and do they know the building and car without asking?
- Does a real hands-free elevator phone's acoustic echo canceller defeat a speaker-to-mic loopback? Does the two-transducer design (a sensor mic and piezo in the car operating panel) count as an elevator alteration that needs AHJ acceptance under the A17.1 edition NJ enforces?
- Does the ASME A17.1 edition NJ enforces already require automatic monitoring of the emergency communication link, and do incumbents (e.g., Kings III, AVIRE, MarketSpark, CSG) already run automated daily line tests? If so, how narrow is PROVE's moat: end-to-end acoustic proof, location assurance and Cutover Watch? (Unverified: the web-search budget was exhausted this pass.)
- NFPA 72: must a fire-alarm communicator connect to the public network upstream of any PBX (which would make communicators the main Verizon-copper subset)? What test intervals and single- vs dual-path rules apply to a cellular replacement, and will the local AHJ accept one Verizon LTE path?
- Does Verizon already identify life-safety lines from service-order or line-type codes? What precision and recall would FIND need on top of that baseline to be worth running? Will Verizon counsel accept CPNI use under 222(c)(1)/(d)(1) for migration outreach, given the $46.9M fine?
- When an elevator or alarm line moves from copper to a cellular gateway, what location does a central-station or 911 call carry (the service-address record vs the registered address vs cell-based location)? Can PROVE verify the registered address remotely?
- Does NJ IBC 3001.2 visual communication apply to existing elevators or only to new and altered ones? Does replacing a car station trigger it? Is the mid-Feb 2027 mandatory date (Aug 17, 2026 plus six months) correct?
- Is a nightly zero-install dial-in check that analyzes only ambient-noise features legal under NJ wiretap law and acceptable to Rutgers counsel and Facilities? Do Rutgers elevator phones auto-answer incoming calls at all?
- What Verizon LTE-M and Cat-1 signal and attach reliability do Rutgers controller and machine rooms actually get? Which buildings need external antennas, a Cat-1 fallback, or a wired second path, and do those network closets have emergency power?
- Who inside Verizon would own this (Network Transformation, Verizon Business POTS Replacement, ThingSpace), and what are real values for retention uplift, failed-cutover cost, truck-roll cost and PROVE price per line, so the CFO formula stops being all assumptions?
- Are other Rutgers teams converging on copper retirement? (14 of 14 internal lenses landed here.) If so, which primary-data asset (HELP audit, OIT count, pilot data, Verizon mentor) is the most defensible differentiator to lead with?
- If Gate A fails, is 'national-first with Rutgers as the PROVE pilot' really stronger than switching to HangUp? What evidence by Oct 31 would settle that?

## 8. Founder verification after the tournament (Gen 4, 2026-10-21)

- **Verified:** Verizon New Jersey's *Public Notice of Copper Retirement under Rule 51.333*, ID **2026-03-A-NJ**, is dated **September 8, 2026**, with implementation **on or after December 10, 2026**. It covers 62 wire centers, including **Piscataway, 4 Skiles Avenue, CLLI PSWYNJPI**. New Brunswick is not listed. The extracted text is in `research/sources/verizon_nj_copper_retirement_notice_2026-03-A-NJ.txt`.
- **Notice language we rely on:** Verizon retires copper "at all remaining locations". The affected services "depend on obsolete time-division multiplexing and also use SS7 signaling". Verizon "may require customers and interconnecting entities to migrate services off of copper facilities well before the copper retirement implementation date."
- **Still unverified:** whether Rutgers life-safety lines are served from PSWYNJPI on Verizon copper (Gate A); who answers Rutgers elevator calls; and the scope of prior art for acoustic self-test. Generation 4 researches all three.
