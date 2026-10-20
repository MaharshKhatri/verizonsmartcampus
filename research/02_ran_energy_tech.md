# 02 — RAN Energy, O-RAN, Slicing, Grid DR and Privacy: Technical Due Diligence

Prepared 2026-10-20 for the Rutgers Verizon Smart Campus Innovation Challenge team. Author role: 5G/MEC architecture research.

**How to read this document**
- Every number has a source link. Labels:
  - **[S]**: from a standards body or regulator (3GPP, O-RAN, PJM, U.S. Code, FCC).
  - **[P]**: from a peer-reviewed or arXiv paper.
  - **[V]**: a vendor or operator claim (marketing-grade; nobody independently measured it).
  - **[T]**: from trade press.
  - **[D]**: a value **we derived** by arithmetic from sourced inputs.
  - **[EST]**: an **estimate or placeholder**. It is not sourced. Replace it before quoting it to judges.
- **Not verified (do not cite):** a "Verizon + Enersponse 2023" demand-response partnership. Several searches found nothing on Verizon's newsroom, Enersponse's site or the trade press. The same applies to Verizon coverage claims at SHI Stadium. See §5.
- **Limit:** the web-search budget for this session ran out before every gap was closed. The remaining gaps are listed in §13.

---

## 1. How much energy the RAN uses, and typical equipment power

### 1.1 RAN share of operator energy
| Claim | Value | Source |
|---|---|---|
| RAN share of a mobile operator's total energy (GSMA Intelligence, *A Blueprint for Green Networks*, 2022) | **73%** on average | [T] [Light Reading, 1 Nov 2022](https://www.lightreading.com/business-management/network-operators-focus-on-energy-savings-as-costs-soar) |
| GSMA *Mobile Net Zero 2023*: about 90% of operator energy goes to the network, and the RAN uses more than 80% of network energy | 90% / >80% | [P] cited in [Kundu, Lin, Gadiyar (NVIDIA), arXiv 2402.11993](https://arxiv.org/pdf/2402.11993) |
| Ericsson: RAN is "over 75 percent" of mobile network energy. Far EasTone attributes 71% of its electricity bill to the RAN | >75% | [V] [Ericsson blog, Jun 2023](https://www.ericsson.com/en/blog/2023/6/intelligent-sustainability-ai-energy-consumption) |
| NGMN: the base station is the largest consumer at the site, about 50% of total site power. The rest is cooling, rectifiers and batteries | ~50% | [P] NGMN *Green Future Networks: Network Energy Efficiency* (Dec 2021), cited in [arXiv 2402.11993](https://arxiv.org/pdf/2402.11993) |
| PA, transceivers and cables are about 65% of base-station energy | ~65% | [P] cited in [Piovesan et al., IEEE Commun. Mag. Oct 2022, arXiv 2209.11600](https://arxiv.org/pdf/2209.11600) |
| Energy is the third-largest operator cost, after site rent and labor. Energy costs rose 2–8x in 2022 | — | [T] Light Reading (above), quoting GSMA's Emanuel Kolta |

**Pitch line:** "About three quarters of an operator's energy goes to the radio network (GSMA Intelligence, 2022)."

### 1.2 Equipment power draw
| Equipment | Value | Confidence and source |
|---|---|---|
| 64T64R massive-MIMO AAU (3.5 GHz class, the same class as Verizon C-band), maximum | **1.0–1.4 kW** | [V] Huawei *5G Power* publication: "maximum energy consumption of a 64T64R … AAU will be an estimated 1 to 1.4 kW" ([Huawei](https://www.huawei.com/en/huaweitech/publication/89/5g-power-green-grid-slashes-costs-emissions-energy-use)) |
| 64T64R AAU at 30% load | ~900 W; peak 1,200–1,400 W; BBU ~300 W | Low confidence: secondary forum quote of the Huawei white paper ([lafibre.info](https://lafibre.info/5g/la-consommation-de-la-5g/)). The primary PDF returned HTTP 403 |
| Ericsson AIR 6449 (64T64R massive MIMO) | DC power port rated "up to 1000 W" | [V] device database ([NetBox Labs](https://netboxlabs.com/ndx/ericsson/ericsson-air-6449)), citing the Ericsson product page. This is a port rating, not a measured draw |
| Whole tower with many bands (5G + legacy) | >10 kW maximum; >20 kW with 10+ bands | [V] [Huawei](https://www.huawei.com/en/huaweitech/publication/89/5g-power-green-grid-slashes-costs-emissions-energy-use) |
| 5G versus 4G, same configuration | 5G is 2.6x at idle, 3x at 50% load, 3.5x at 100% load | [V/T] Huawei field data from a Chinese operator, via Libération ([lafibre.info](https://lafibre.info/5g/la-consommation-de-la-5g/)) |
| 5G S111 site (3 sectors × 1 carrier) at 100% load | ~3.7–3.85 kW (equipment only, no cooling) | Low confidence: anonymous operator field test, reported on a blog ([dappworks](https://dappworks.com/front-line-data-study-about-5g-power-consumption-you-need-to-know-about-5g/)) |
| 3-sector macro site, our model | 3 AAUs × 1.0–1.4 kW + BBU/DU ≈ **3.3–4.5 kW** of radio equipment at peak, plus site overhead (cooling and rectifier losses) | [D] from the rows above. Overhead could reach ~1× the BS draw on legacy sites if NGMN's "BS ≈ 50% of site power" figure applies. Modern outdoor sites without air conditioning need less: **[EST] overhead 10–100%** |
| EARTH macro model, per transceiver | P_max 20 W RF, P0 130 W, slope 4.7, P_sleep 75 W | [P] Auer et al., "How much energy is needed to run a wireless network?", IEEE Wireless Commun. 2011. Values as tabulated in [EUDL](https://eudl.eu/pdf/10.1007/978-3-319-40352-6_51). Idle/full = 130/(130+4.7·20) = **58%** [D] |
| EARTH pico/small cell model (4G-era) | P_max 0.13 W, P0 6.8 W, slope 4.0, P_sleep 4.3 W | [P] same source |
| Indoor 5G small cell (Ericsson Radio Dot System) | "28–39.5–57 W". The page doesn't say whether this is per Dot or per IRU. One IRU drives up to 8 Dots | [V] [Ericsson/Cradlepoint](https://cradlepoint.ericsson.com/products/radios/ericsson-radio-dot-system/) |
| Indoor DAS remote unit | ~15 W per service; 45 W or more with 3+ services. A system with more than 50 RUs draws more than 1.5–3 kW | [patent] "Power management in distributed antenna systems" ([US 2014/0233442](https://patents.justia.com/patent/20140233442)) |
| Outdoor DAS remote unit | single-band ~400 W; quad-band up to 1,600 W AC. Head-end/BTS-hotel −48 V plants are sized 18–120 kW | [T] [ISE Magazine (2014/2016)](https://www.isemag.com/5g-6g-and-fixed-wireless-access-mobile-evolution/article/14269567/the-ins-and-outs-of-das-powering) |
| Ericsson claims for its Radio Dot versus DAS | up to 70% less power than legacy DAS (Stockholm); 45% less than active DAS (Taipei trial) | [V] via search results, [TelecomTV](https://www.telecomtv.com/content/5g/ericsson-and-proptivity-deploy-first-neutral-host-led-shared-indoor-5g-ran-47841/) |
| mmWave (28/39 GHz) small cell | **No public datasheet wattage found.** Model it with the 3GPP relative scaling: TR 38.864 Cat-1 Active-DL is 152 for FR2 (Set 3) versus 280 for 64T FR1 (Set 1), so **~0.54× a 64T C-band AAU ≈ 540–760 W** | **[D/EST]** The ratio comes from [TR 38.864 §5.1](https://itecspec.com/3gpp/38.864/s/5.1). The absolute value is an estimate; treat it as a sensitivity parameter |
| vRAN / edge server (vDU, vCU, MEC host) | "illustrative" server: 150 W at 50% utilization, 185 W at 90% | [P] [arXiv 2402.11993](https://arxiv.org/pdf/2402.11993). This high idle floor is why O-RAN specifies O-Cloud node shutdown (§3) |

### 1.3 Static (load-independent) power: the core of the argument
- **Field measurements:** Golard, Louveaux & Bol, *Ann. Telecommun.* 2023, fitted measurements from Belgian sites. The result is "a linear relationship between power consumption and data traffic with a static traffic-independent power component", and "the static energy consumption accounts for a major part of the total RAN energy consumption". 5G sleep modes could improve energy efficiency "by 10 times compared to 4G" ([UCLouvain DIAL abstract](https://research.dial.uclouvain.be/handle/2078.5/255323)). [P]
- **Huawei AAU field data, our fit:** a linear fit through ~900 W at 30% load and 1,200–1,400 W at peak gives an idle draw of **~690–770 W, about 50–64% of peak**, with no energy-saving features on. [D] from low-confidence inputs.
- **EARTH model:** idle is 58% of full load per transceiver. [D/P]
- **3GPP model (TR 38.864):** the model splits power into a static part (taken as the micro-sleep power P3) and a dynamic part. It uses a "PA-related fraction" A = 0.4 baseline (optional 0.1 or 0.7) ([TR 38.864 §5.1](https://itecspec.com/3gpp/38.864/s/5.1)). [S]
- **Takeaway for the simulator:** without energy-saving features, a 5G AAU at zero traffic still draws about half or more of its peak power. That idle draw is what sleep modes recover, and it is why predicting *when* traffic will be near zero is valuable.

---

## 2. Energy-saving mechanisms: savings and wake-up latency

### 2.1 3GPP Rel-18 base-station power model (TR 38.864, Table 5.1-x) [S]
Source: [iTecSpec mirror of TR 38.864 §5.1](https://itecspec.com/3gpp/38.864/s/5.1).

Reference configurations:
- Set 1: FR1 TDD, 100 MHz, 64T/64R, 55 dBm.
- Set 2: FR1 FDD, 20 MHz, 32T/32R, 49 dBm.
- Set 3: FR2 TDD, 100 MHz, 2 TxRUs, 33 dBm.

| State | Relative power, Cat 1 (Set 1 / Set 2 / Set 3) | Relative power, Cat 2 (Set 1 / Set 2 / Set 3) | Total transition time, Cat 1 / Cat 2 | Extra transition energy (rel·ms), Cat 1 / Cat 2 |
|---|---|---|---|---|
| Deep sleep | 1 | 1 | **50 ms / 10 s** | 1000 / 17000 |
| Light sleep | 25 | 2.1 | **6 ms / 640 ms** | 90 / 1088 |
| Micro sleep | 55 / 50 / 38 | 5.5 / 5 / 3 | 0 (immediate) | 0 |
| Active DL | 280 / 200 / 152 | 32 / 26 / 17.6 | — | — |
| Active UL | 110 / 90 / 80 | 6.5 / 5.8 / 4.2 | — | — |

*Note:* the extracted table lost its column alignment. Mapping light sleep to 25 for Cat 1 and 2.1 for Cat 2 is our inference, and it is consistent with the other rows. The TR does not define the categories on that page.

**Scaling rules:**
- P_DL = P_static + s_a·(…), where s_a is the fraction of active TxRUs. This is how antenna muting enters the model.
- Optional simplified form: P_DL = P4·(0.4 + 0.6·s_f·s_p·η)·(0.4 + 0.6·s_a).
- Intra-band contiguous extra carriers are scaled by 0.7.

### 2.2 Advanced Sleep Modes SM1–SM4 (from 3GPP discussions; academic convention) [P]
Source: [Lopez-Perez et al., *A Survey on 5G RAN Energy Efficiency* (Huawei), arXiv 2101.11246](https://arxiv.org/abs/2101.11246), §on ASM.

| Mode | What is switched off | Minimum duration (deactivation + reactivation) | Sleep power as a fraction of load-independent power (δs) |
|---|---|---|---|
| SM1 (≈ symbol-level cell DTX) | PA plus part of the BBU and analog front end | **71 µs** (one OFDM symbol) | 0.84 |
| SM2 | plus more of the analog front end | **1 ms** | 0.69 |
| SM3 | plus all digital BBU and nearly all analog front end except the clock | **10 ms** | 0.29 |
| SM4 | everything except wake-up circuits | **1 s** | < 0.1 |

**Constraints:**
- With 15 kHz SCS and two SSBs per burst, an NR cell can sleep up to 19 ms out of every 20 ms (95% sleep ratio). With a 160 ms SSB period, it can sleep up to 159 ms (99.38%).
- "Current 3GPP NR implementation cannot realise" SM4 because SM4 needs 1 s and NR can sleep at most 160 ms. This is the gap that cell switch-off, and the Rel-19 on-demand SSB/SIB1 features, are meant to close.

### 2.3 Savings per mechanism
| Mechanism (timescale) | Reported savings | Source |
|---|---|---|
| **Symbol shutdown / micro-DTX** (µs–ms, local and opportunistic) | **34%** below the AAU's zero-load power (real data, 7,760 AAUs in China) | [P] [Piovesan et al. 2022](https://arxiv.org/pdf/2209.11600) |
| Ericsson Micro Sleep Tx + Low Energy Scheduler Solution | "up to 15 percent" of radio equipment energy | [V/T] [eeNews Europe, Sep 2021](https://www.eenewseurope.com/en/machine-learning-helps-cut-5g-power-by-half/) |
| **Cell DTX/DRX** (Rel-18 normative) | **0.2%–71.4%** BS energy saving across company evaluations. User-perceived-throughput loss 0.91–15.5%, up to 62.4% in some configurations | [S] [TR 38.864 §7](https://itecspec.com/3gpp/38.864/s/7) |
| **Spatial-element adaptation / antenna muting** (C-1, e.g. 64T→32T/16T) | **0–48.2%**. Throughput impact under 10% with dynamic multi-CSI adaptation; up to 87% with static adaptation | [S] TR 38.864 §7 |
| TRP muting (C-2) | 19.7–41.6% | [S] TR 38.864 §7 |
| PDSCH power reduction (D-1) | 2.3–51.5% | [S] TR 38.864 §7 |
| SSB-less SCell / longer SSB periodicity | 0.3–98.4% on the energy-saving carrier; longer SSB period 0.9–84.8% (throughput drops as load rises) | [S] TR 38.864 §7 |
| **O-RAN RF channel switch-off** (near-RT) | ~80 W per O-RU (4T4R); **~230 W per O-RU (64T64R)** | [S] O-RAN WG1 NES TR v02.00 gain analysis, via [arXiv 2402.11993](https://arxiv.org/pdf/2402.11993) |
| **Carrier / capacity-layer shutdown** (minutes, non-RT) | **47%** below zero-load power for a multi-carrier AAU | [P] [Piovesan 2022](https://arxiv.org/pdf/2209.11600) |
| O-RAN carrier/cell switch-off | 150–180 W per O-RU (4T4R, 100 MHz, 4 layers, 30 W/antenna); **260–340 W per O-RU (64T64R, 16 layers)** | [S] O-RAN NES TR, via [arXiv 2402.11993](https://arxiv.org/pdf/2402.11993) |
| Ericsson Booster Carrier Sleep (Optus) | 2.23 kWh/day/site | [V] [Ericsson PR, 26 Feb 2024](https://www.ericsson.com/en/press-releases/7/2024/optus-welcomes-a-new-chapter-in-energy-efficiency-with-ericsson) |
| Ericsson Massive MIMO Sleep (Optus) | 2.5 kWh/day/site; 24–26% total daily saving with other measures | [V] same |
| **Deep sleep / dormancy** (seconds–minutes) | **70%** below normal operation (AAU field data) | [P] [Piovesan 2022](https://arxiv.org/pdf/2209.11600) |
| Ericsson 5G Deep Sleep | "around 70%" while hibernating (Optus); "up to 70%" in low-traffic hours (Vodafone UK) | [V] Ericsson PR (above); [TelecomTV, 11 Mar 2025](https://www.telecomtv.com/content/green-network/vodafone-uk-and-ericsson-trial-ai-solutions-for-improved-5g-energy-efficiency-52546/) |
| Nokia Extreme Deep Sleep (ReefShark/Habrok mMIMO) | "up to 95%" below active mode during inactive periods; "a factor of eight" (Orange) | [V] [Nokia blog](https://www.nokia.com/blog/ai-builds-the-foundation-for-zero-energy-use-at-zero-traffic/); [TelecomTV, 20 Feb 2024](https://www.telecomtv.com/content/green-network/nokia-and-orange-announce-extreme-deep-sleep-energy-power-saving-mode-mwc24-49684/) |
| ZTE hibernation: residual draw | AAU/RRU still consumes "dozens of watts" in deep sleep | [V] GSMA case study (page returned 403; quoted from the search index): ZTE Hibernation in 5G Base Stations |

### 2.4 Network-level results with AI orchestration (the comparison judges will make)
| Operator / vendor | Result | Source |
|---|---|---|
| **Verizon + Samsung AI-ESM rApp on Qualcomm Dragonwing RIC** (commercial 4G and 5G network; C-band and mmWave) | **15% average; up to 35% per sector** at low traffic | [V] [Verizon, 25 Feb 2025](https://www.verizon.com/about/news/verizon-open-ran-innovation); [Samsung blog](https://www.samsung.com/global/business/networks/insights/blog/0224-powering-a-greener-future-inside-samsungs-ai-driven-network-energy-innovation) |
| Vodafone UK + Ericsson (London) | up to 33% lower daily 5G radio-unit power | [V] TelecomTV 2025 |
| Far EasTone + Ericsson | 25% of daily RAN energy | [V] Ericsson blog 2023 |
| Optus + Ericsson | 24–26% total daily | [V] Ericsson PR 2024 |
| stc + Nokia MantaRay SON ESM | 6% across the 4G network | [V] [Nokia case study, Nov 2023](https://www.nokia.com/customer-success/stc-uses-nokia-son-to-improve-ran-energy-efficiency-with-ai-powered-energy-savings-management/) |
| Nokia MantaRay Energy (dynamic thresholds) | "up to 15% additional" | [V] Nokia blog |
| Huawei PowerStar 2.0 | "over 25%" under typical configurations | [V] [Telecom Review Asia, Oct 2021](https://www.telecomreviewasia.com/news/technology-news/2534-huawei-launches-greensite-and-powerstar-2-0-for-green-low-carbon-5g-networks/) |
| Rimedo Labs COOS rApp/xApp (Juniper RIC, Deutsche Telekom data, i14y PlugFest Spring 2025) | up to 30%; brochure claims ~25% on capacity layers | [V/T] search-indexed [EANTC i14y](https://eantc.de/i14y-lab-plug-fest-2025/); [Rimedo brochure on ericsson.com](https://www.ericsson.com/assets/local/ran/doc/Brochure-Rimedo-Labs-Cell-ONOFF-Switching-rApp.pdf) |

**Honest takeaway:** realistic network-wide AI savings are **6–35% of RAN energy**, with **15% being Verizon's own average**. Per-radio deep-sleep figures of 70–95% apply only during the hours the radio is actually asleep.

### 2.5 3GPP Rel-18 / Rel-19 Network Energy Savings (NES) features [S]
- **Rel-18 NES** (study TR 38.864, followed by normative work):
  - Cell DTX/DRX, aligned with UE C-DRX and exchanged between nodes.
  - Spatial adaptation of antenna ports and TxRU chains, with CSI enhancements.
  - PDSCH power-offset adaptation.
  - SSB-less SCell for inter-band CA.
  - Inter-node beam activation; paging in a limited area.
  - Cell barring of legacy UEs on NES cells.
  - **Conditional handover that is aware of NES state**. This is useful for a safe "coverage-layer handover before switch-off".
  - Sources: [TR 38.864 §7](https://itecspec.com/3gpp/38.864/s/7); [arXiv 2402.11993](https://arxiv.org/pdf/2402.11993).
- **Rel-18 AI/ML for NG-RAN** (TR 37.817, normative in TS 38.300/38.423):
  - Network energy saving is one of three AI/ML use cases.
  - Inputs include predicted UE trajectory, current and **predicted** resource status and energy efficiency, and neighbour energy state.
  - An "Energy Cost" index is exchanged over Xn ([TR 37.817 §5.1.2.4](https://itecspec.com/3gpp/37.817/s/5.1.2.4); [TS 38.743 note](https://www.itecspec.com/3gpp/38.743/s/5.3.1)).
  - *A standard home for "predicted load" already exists. Our contribution would be better predictions, not a new interface.*
- **Rel-19 NES enhancements** (WI Netw_Energy_NR_enh, RP-252332; rapporteur Ericsson):
  - **On-demand SSB for SCells**.
  - **On-demand SIB1 for idle/inactive UEs**, triggered by a PRACH-based uplink wake-up signal.
  - **Adaptation of SSB periodicity, PRACH occasions and paging occasions**.
  - Source: [TR 21.919 §5.1](https://www.itecspec.com/3gpp/21.919/s/5.1).
  - These features make longer and deeper sleep compatible with NR.

---

## 3. O-RAN: RIC, rApps, xApps and interfaces for energy saving

### 3.1 Architecture and control loops
- **Non-RT RIC (inside the SMO):**
  - Hosts **rApps**.
  - Control loop longer than 1 s ([DCD/SDx coverage of Verizon RIC](https://www.datacenterdynamics.com/en/news/verizon-deploys-multi-vendor-ric-into-its-commercial-network/)).
  - Configures E2 nodes (O-CU/O-DU) over **O1**, and O-RUs over the **Open Fronthaul M-Plane**.
  - Sends policies to the Near-RT RIC over **A1**.
  - rApps reach the platform through **R1** (named in the [O-RAN 2025 white paper](https://mediastorage.o-ran.org/white-papers/O-RAN.SuFG.Potential%20Energy%20Savings%20Features%20in%20O-RAN%20white%20paper%202025-01.pdf)).
- **Near-RT RIC:**
  - Hosts **xApps**.
  - Controls E2 nodes over **E2**. The relevant service model is **E2SM-CCC** (Cell Configuration and Control).
- **Real-time loop (<10 ms):** inside the O-DU/O-RU, e.g. ASM.
  - Source: [arXiv 2402.11993](https://arxiv.org/pdf/2402.11993) Fig. 3–4.
- **Fit for our idea:** a 15–60 minute demand forecast falls squarely in the **Non-RT RIC rApp** timescale.
  - It can run as an rApp that sets carrier/cell on-off and RF-channel policies.
  - It can push A1 policies so that a traffic-steering xApp empties a cell before switch-off. Rimedo's ES-rApp used exactly this A1 "FORBID" pattern.
  - (From knowledge, verify in O-RAN.WG2 A1 specs: A1 also defines an *Enrichment Information* service for feeding external data to the RIC. This is a natural standards hook for campus context.)

### 3.2 O-RAN Network Energy Savings (NES) work items [S]
Sources: the [O-RAN white paper *Potential Energy Savings Features in O-RAN*, v01.00, Jan 2025](https://mediastorage.o-ran.org/white-papers/O-RAN.SuFG.Potential%20Energy%20Savings%20Features%20in%20O-RAN%20white%20paper%202025-01.pdf) and [arXiv 2402.11993](https://arxiv.org/pdf/2402.11993).
- **Phase 1** (WG1 Use-Case TG technical report, Mar 2023, **O-RAN.WG1.NESUC-TR-R003-v02.00**): four use cases.
  - (1) Carrier and cell switch off/on. Two modes: hibernation (PA at minimum current) and complete switch-off. Specified normatively over O1.
  - (2) RF channel reconfiguration.
  - (3) Advanced sleep mode selection.
  - (4) O-Cloud resource energy saving: cloud node shutdown and CPU energy-saving states.
- **Phase 2** (completed July 2024):
  - RF Channel ES (UC2) and ASM (UC4) across WG2, WG3 and WG4.
  - **O-RU Deep Hibernate**: WG4; "completely disconnecting the M-Plane when the O-RU is inactive", with wake-up on a timer.
  - A1 policy and E2SM-CCC enhancements.
- **Proposed next phase:**
  - O-RU coordination with its **power source**: battery state of charge and renewable or grid supply, aligned with ETSI ES 202 336-11 and 3GPP TR 28.931 Key Issue #9, "RAN energy saving when using backup batteries".
  - PA dynamic voltage bias.
  - Artificial load generation.
  - O-Cloud workload consolidation.
- **Relevance to features (c) and (d):**
  - Deep Hibernate deliberately drops the management connection. To an operations system that doesn't know about it, an intentionally hibernating O-RU looks like a lost-M-Plane fault.
  - The proposed battery and power-source awareness is where grid co-optimization would plug in.

### 3.3 Verizon's O-RAN / vRAN position (important context)
- **vRAN scale:**
  - About **60,000 vRAN sites** in service. The count includes macro sites and small cells "in stadiums, at large events, and for enterprise private networks".
  - Early 2025: 22,900 sites, with 40% of the network on vRAN.
  - The platform is Samsung radio software on HPE servers with Wind River.
  - CTO Yago Tenorio: all vRAN sites are Samsung "as of today". "Ericsson is not ready. But they have a good plan now."
  - Sources: [Light Reading, 29 Jun 2026](https://www.lightreading.com/5g/verizon-ups-pressure-on-ericsson-to-be-open-like-samsung); [Light Reading, 11 Jun 2026](https://www.lightreading.com/network-automation/verizon-taps-ai-agents-for-network-automation).
- **O-RAN-capable radios:** 130,000 ([Light Reading, Feb 2024](https://www.lightreading.com/open-ran/verizon-embraces-open-ran-messaging)).
- **First multi-vendor RIC** (Feb 2025): Samsung **AI Energy Saving Manager** rApp on the **Qualcomm Dragonwing** RIC. It produced 15% average and 35% maximum savings ([Verizon](https://www.verizon.com/about/news/verizon-open-ran-innovation)).
  - **What judges will say: "Verizon already runs an AI energy-saving rApp in production."**
- **Agentic AI ops** (June 2026): rApps and the RIC "continuously monitor the network and make closed-loop changes". vRAN deployments are "completely automated" once hardware is connected (Umashankar Velusamy, Verizon) ([Light Reading](https://www.lightreading.com/network-automation/verizon-taps-ai-agents-for-network-automation)).
- **Energy digital twin** (2022–23):
  - Builds energy models across sites, flags cost outliers, and tunes sleep settings at sites that host both 4G and 5G.
  - Claimed "over $100 million a year" in energy-cost reductions.
  - Inputs: network performance data, utility bills, equipment configuration, power draw, renewable status and energy prices. **No events or weather are mentioned.**
  - Source: [TM Forum Inform, Jan 2023](https://inform.tmforum.org/features-and-opinion/how-verizon-is-using-digital-twins-to-reduce-energy-costs).

---

## 4. Vendor competition and our differentiation (honest assessment)

### 4.1 What each competitor's AI energy saving uses as input (from public sources)
| Vendor / product | Mechanisms | Data inputs stated publicly | External context? |
|---|---|---|---|
| **Samsung AI-ESM** (deployed at Verizon) | switches off cells, Tx paths and PAs below a learned threshold | traffic "across different locations and times of day", "historical data and real-time conditions", site environment, topology, radio hardware specifications ([Samsung](https://www.samsung.com/global/business/networks/insights/blog/0224-powering-a-greener-future-inside-samsungs-ai-driven-network-energy-innovation)) | **None mentioned** |
| **Ericsson** (Service Continuity AI app suite / Intelligent Energy Efficiency; 5G Deep Sleep; 4G Cell Sleep Mode Orchestration; MIMO Sleep; Booster Carrier Sleep; Micro Sleep Tx) | the full range of sleep and switch-off features | "live traffic data", predictive algorithms, behavioral models of cells ([TelecomTV](https://www.telecomtv.com/content/green-network/vodafone-uk-and-ericsson-trial-ai-solutions-for-improved-5g-energy-efficiency-52546/)). Separately, Ericsson says AI can combine **weather forecasts, tariffs and grid information** to optimize site power and batteries ([Ericsson blog](https://www.ericsson.com/en/blog/2023/6/intelligent-sustainability-ai-energy-consumption)) | Weather, tariffs and grid data for **power-system** optimization. **No event or schedule data found** |
| **Nokia MantaRay Energy / SON ESM; Extreme Deep Sleep** | cell-level sleep windows, dynamic thresholds | "predict future traffic patterns **based on historical traffic data**" ([Nokia](https://www.nokia.com/blog/ai-builds-the-foundation-for-zero-energy-use-at-zero-traffic/)) | **None**; Nokia says historical data explicitly |
| **Huawei PowerStar / 2.0** | symbol, channel and carrier shutdown plus power control, coordinated across bands | "precise traffic forecast based on spatial-temporal data"; service load ([GSMA wiki](https://www.gsma.com/futurenetworks/wiki/powerstar-and-mtn-south-africa-energy-saving-case-study/), [TRA](https://www.telecomreviewasia.com/news/technology-news/2534-huawei-launches-greensite-and-powerstar-2-0-for-green-low-carbon-5g-networks/)) | **None mentioned** |
| **Rimedo Labs** COOS/ES rApp and xApp (tested on the Juniper RIC with Keysight RICtest; product brochure hosted on ericsson.com) | cell on/off with traffic steering | RAN KPIs; trained on operator data at 15-minute granularity ([arXiv 2409.19807](https://export.arxiv.org/pdf/2409.19807); [EANTC](https://eantc.de/i14y-lab-plug-fest-2025/)) | **None mentioned** |
| **Qualcomm Dragonwing RIC** | platform for rApps | RAN AI services (HNN/DNN) | n/a |
| **T-Mobile Dynamic CX** (June 2026; built on its SON) | capacity and performance optimization for crowds; **not** energy | "**publicly available event information, schedules and online activity**" to anticipate mass gatherings. Made 11,000+ automated optimizations at 12 World Cup fan events ([TelecomTV, 5 Jun 2026](https://www.telecomtv.com/content/ai/t-mobile-introduces-dynamic-cx-55615/)) | **Yes**, for capacity |
| Academic: **ARENA** (NEC Labs and others, IEEE TNSM 2020) | forecasting RAN capacity for football events | past KPIs **plus event context** (16 sectors, a 30,000-seat stadium) ([arXiv 2010.09467](https://arxiv.org/abs/2010.09467)) | **Yes**, for capacity |

### 4.2 Verdict, to say out loud to Verizon judges
1. **"Hasn't Ericsson/Nokia already built this?" — Yes, for the mechanisms and the AI orchestration.**
   - Sleep modes, MIMO muting, carrier and cell switch-off, ML thresholds and rApps are commercial products.
   - **Verizon already runs one** (Samsung AI-ESM, 15% average). Do **not** pitch "AI puts radios to sleep" as new.
2. **What we found no public evidence of:** any vendor energy-saving product that ingests **external context**: class timetables, event calendars, transit GPS, Wi-Fi association counts or building management system (BMS) occupancy.
   - Every vendor states its inputs as RAN-internal: historical traffic, time of day, location, configuration and live KPIs.
   - Ericsson's external inputs (weather, tariffs) are for site power systems, not radio sleep decisions.
   - *Absence of evidence is not proof*: unpublished operator SON rules may encode holidays.
3. **External event context for network planning is NOT new:**
   - T-Mobile's Dynamic CX (June 2026) mines public event data.
   - The ARENA paper (2020) used event context.
   - Verizon runs a "centralized global event management center" for the World Cup ([RCR, Apr 2026](https://www.rcrwireless.com/20260420/uncategorized/verizon-world-cup)), and its Super Bowl prep uses "lots of dry runs" ([SVG, Feb 2025](https://www.sportsvideo.org/2025/02/08/live-from-super-bowl-lix-verizons-joe-russo-on-how-5g-can-get-to-the-next-level-for-broadcasters-fans/)).
   - **Expect a judge to cite T-Mobile.**
4. **Where we can honestly differentiate:**
   - (a) **Private, authoritative campus data** a web scraper cannot see: registrar timetables, room assignments, exam schedules, the bus AVL feed, Wi-Fi association counts and BMS occupancy. This data comes at building granularity, ahead of time, from a university data partner.
   - (b) Using that context **for energy**, in both directions:
     - safe *deeper and longer* sleep when the context says a building will be empty (breaks, snow days, finals end);
     - **pre-wake** before a predicted surge, so a cell doesn't stay asleep when a lecture lets out.
     - Pattern-only forecasters fail exactly on these exception days. **Our measurable claim should be lower forecast error and fewer KPI violations on anomaly days compared with a traffic-history baseline**, not "AI saves energy".
   - (c) **Telling sleep from fault:** cross-check an outage alarm against both the energy-saving state and the expected demand.
     - Standards already flag energy-saving state: TS 28.310 centralized and distributed ES with activation and deactivation procedures, and the TS 28.541 *CESManagementFunction*.
     - So the new part is the **context-based plausibility check**, e.g. "cell dark AND class letting out in 10 min ⇒ likely fault, dispatch", and handling O-RU Deep Hibernate's dropped M-Plane.
     - Present this as an operations-system add-on, not a new standard.
   - (d) **Campus-grid co-optimization** (HVAC, campus batteries, PJM DR). We found no RAN vendor offering this.
     - The closest analogues are Elisa/Gridle's telecom-battery virtual power plants (§7) and O-RAN's proposed power-source-aware O-RU features (§3.2).
5. **Be realistic about the size of the prize:**
   - On one campus, RAN savings are small in absolute terms. Example: ten 64T sectors at ~1 kW each, saving 15% around the clock, is 10 kW × 0.15 × 720 h ≈ **1 MWh/month [D/EST]**. At an assumed $0.15–0.20/kWh [EST], that is only about $150–200/month.
   - Campus HVAC is orders of magnitude bigger.
   - The **business case is the platform**: reuse across Verizon's ~60,000 vRAN sites, many on or near campuses and venues, plus enterprise private-network and slicing upsell. Do not claim campus energy savings alone pay for it.

---

## 5. Verizon-specific facts

| Topic | Fact | Source |
|---|---|---|
| AI RAN energy saving | Samsung AI-ESM on the Qualcomm RIC, commercial deployment: 15% average, 35% maximum per sector (25 Feb 2025) | [Verizon](https://www.verizon.com/about/news/verizon-open-ran-innovation) |
| Energy digital twin | ">$100M a year" in energy-cost reductions claimed (DTW 2022, reported Jan 2023) | [TM Forum](https://inform.tmforum.org/features-and-opinion/how-verizon-is-using-digital-twins-to-reduce-energy-costs) |
| Backup power | Battery backup at macro sites; permanent generators at most cell sites and all switch locations | [Verizon](https://verizon.com/about/node/924321) |
| Grid-support precedent | During a California Flex Alert, Verizon ran backup power at **six mobile switching centers** to take load off the grid | [T] [telecoms.com](https://telecoms.com/fibre/verizon-resorts-to-backup-power-amid-california-heatwave). Undated in our search excerpt; the page returned 403 |
| Verizon DR product for utilities | "Grid Wide" utility demand-response solution (older collateral) | [Verizon brief](https://www.verizon.com/business/resources/T9a/solutionsbriefs/grid-wide-utility-solutions-overview.pdf) |
| **Verizon + Enersponse (2023)** | **NOT FOUND.** No record on Verizon's newsroom, Enersponse's site (customers listed: Cinemark, Cucamonga Valley WD) or the trade press. **Do not cite without a primary source.** | searched 2026-10-20 |
| Network slicing products | **Enhanced Video Calling** (Dec 2024, iPhone, slicing-powered). **Frontline Network Slice** for public safety (launched 24 Apr 2025 in select markets; later expanded to 50 markets / nationwide on 5G UW). **5G Network Slice – Enhanced Internet** (18 Dec 2025: SLA-backed 200/45 Mbps fixed wireless; targets media, construction, healthcare and others). A "5G Mobile Network Slice" product page also exists | [Verizon Frontline](https://verizon.com/about/news/verizon-frontline-network-slice-launches); [SDxCentral](https://www.sdxcentral.com/news/verizon-frontline-dishes-up-network-slice-for-first-responders/); [Verizon, Dec 2025](https://www.verizon.com/about/news/feed/wireless-internet-ai-era-network-slicing-enables-sla-backed-service-verizon-business); [Light Reading](https://www.lightreading.com/mobile-core/verizon-uses-network-slicing-on-iphone-video-calls) |
| Slicing at events | Super Bowl LIX (Feb 2025): standalone 5G turned on throughout New Orleans for "5G advanced features", including slicing for first responders and creators. Broadcast-camera slicing is an aspiration ("early innings"). Game-day mmWave TDD tuned to **50/50 on 28 GHz and 80/20 on 39 GHz** (Joe Russo, EVP) | [SVG](https://www.sportsvideo.org/2025/02/08/live-from-super-bowl-lix-verizons-joe-russo-on-how-5g-can-get-to-the-next-level-for-broadcasters-fans/) |
| World Cup 2026 | 3–5x more bandwidth across all 11 U.S. host stadiums (including MetLife, NY/NJ); >50 TB per match expected; slicing for stadium operations "being worked through with FIFA"; Lenovo Referee View body cameras over 5G; centralized global event management center | [RCR, 20 Apr 2026](https://www.rcrwireless.com/20260420/uncategorized/verizon-world-cup) |
| Stadiums | 5G UW (mmWave) in all 30 NFL stadiums | [Verizon](https://verizon.com/about/node/926561) |
| **SHI Stadium (Rutgers)** | **No Verizon-specific announcement found.** Check the coverage map or ask Verizon or Rutgers Athletics | — |
| Private 5G | NHL arenas private 5G plus MEC (Feb 2024); NFL coach-to-coach managed private network; NVIDIA + Verizon AI-enabled portable private 5G platform (demos planned early 2025) | [RCR](https://www.rcrwireless.com/20240219/venues/verizon-deploy-private-5g-networks-across-nhl-arenas); [SVG](https://www.sportsvideo.org/2024/02/06/super-bowl-lviii-coaches-to-rely-on-verizon-5g-private-network-are-broadcasters-next/); [Yahoo/Nvidia](https://finance.yahoo.com/news/nvidia-partners-verizon-build-scalable-183202893.html) |
| MEC / AWS Wavelength | AWS lists **20 Verizon Wavelength Zones**, including **New York City** (nearest to Rutgers), Boston and Washington DC. Lenexa, KS was added 6 May 2025. **No retirement notice found** on the AWS locations page (2026) | [AWS locations](https://aws.amazon.com/wavelength/locations/); [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/05/aws-wavelength-zone-lenexa-kansas/) |
| AI Connect | Launched Jan 2025 with Q4 2024 earnings: fiber, 5G, edge sites, power and cooling for AI workloads; Google Cloud and Meta early users. Sales funnel "roughly doubled to **$2 billion**" (Q2 2025 call) | [TelecomTV](https://www.telecomtv.com/content/ai/verizon-unveils-ai-strategy-to-power-next-gen-ai-demands-52183/); [Verizon 2Q25 transcript](https://www.verizon.com/about/sites/default/files/2025-07/vz2q25_earnings_transcript_072125.pdf); [Benzinga](https://www.benzinga.com/markets/earnings/25/07/46537805/verizons-ai-connect-sales-surge-to-2-billion-fueled-by-real-time-inferencing-demand) |
| Crowd analytics | "Verizon 5G Edge Crowd Analytics": a SaaS AI platform for **college stadiums** (crowd movement, not network capacity) | [Verizon brief](https://verizon.com/business/resources/solutionsbriefs/how-5g-edge-crowd-analytics-can-transform-the-school-fan-experience.pdf) |

---

## 6. 3GPP network slicing, intent and APIs (for a natural-language slice-request feature)

- **Standardized slice types (SST)**, TS 23.501 Table 5.15.2.2-1 [S] ([iTecSpec](https://www.itecspec.com/3gpp/23.501/s/5.15.2.2)):

  | SST | Name | Use |
  |---|---|---|
  | 1 | eMBB | enhanced mobile broadband |
  | 2 | URLLC | ultra-reliable low-latency communications |
  | 3 | MIoT | massive IoT |
  | 4 | V2X | vehicle-to-everything |
  | 5 | HMTC | High-Performance Machine-Type Communications |
  | 6 | HDLLC | High Data rate and Low Latency Communications |
  | 7 | GBRSS | Guaranteed Bit Rate Streaming Service |

  - A PLMN does not have to support all of them.
  - GSMA NEST templates map to SST values in **GSMA NG.116 (Generic Network Slice Template, GST)**.
  - A **GBRSS** slice is the natural match for "broadcast cameras at a game".
- **Rel-17/18 slicing features** (from knowledge; verify in TS 23.501/38.300):
  - Rel-17: Network Slice Admission Control (NSAC), slice-based cell reselection and slice-specific RACH.
  - Rel-18: slice usage and continuity enhancements.
  - These were not re-verified this session.
- **Intent-driven management: 3GPP TS 28.312** [S]
  - Rel-18 WI *IDMS_MN_ph2* (Mar–Dec 2023) added scenarios including intent-driven **RAN energy saving** ([work-item record](https://whatthespec.net/3gpp/wi/990030-idms-mn-ph2)).
  - The Rel-19 TS 28.312 includes §5.1.7 "Intent containing an expectation for RAN energy saving", §6.2.2.1.1 "Radio Network Expectation", `IntentHandlingCapability`, and **Annex D.5, a YAML example of a RAN energy-saving intent** ([iTecSpec ToC](https://itecspec.com/3gpp/28.312/s/contents)).
  - **Design tip:** have the LLM emit a TS 28.312-style Intent (Expectation + Targets + Context) instead of a homemade JSON.
- **TM Forum TMF921 Intent Management API (v5.0)** exists in the TM Forum Open API directory ([page](https://www.tmforum.org/oda/open-apis/directory/intent-management-api-TMF921/v5.0); blocked by a Cloudflare challenge, so the path was confirmed but the contents were not read).
- **CAMARA / GSMA Open Gateway:**
  - **Fall '25 meta-release** (7 Oct 2025) had 60 APIs; **Quality on Demand** (with QoS Profiles) became stable ([CableLabs](https://www.cablelabs.com/blog/driving-the-future-of-network-apis-cablelabs-role-in-camaras-fall-25-meta-release); [CAMARA webinar](https://camaraproject.org/wp-content/uploads/sites/12/2025/10/CAMARA-Fall-25-webinar.pdf)).
  - **Network Slice Booking** (pre-1.0, no reference implementation):
    - `POST /slices` takes `serviceTime`, `serviceArea` (circle or polygon) and `sliceQosProfile` (max devices, per-device up/down rates, delay budgets) and returns `sliceId`.
    - Returns 422 `RESOURCES_INSUFFICIENT` when capacity is lacking.
    - Overlaps with the **Dedicated Networks** API ([5G-MAG](https://www.5g-mag.com/tech/network-apis/camara-network-slice-booking/)).
  - **Mapping for our feature:** natural language → TS 28.312 intent or CAMARA Slice Booking request (game-day polygon + kickoff−2h to final+1h) → operator SMO.

---

## 7. Grid demand response economics (PJM; New Jersey is in PJM)

### 7.1 PJM capacity (Base Residual Auction) prices [S]
| Delivery year | RTO clearing price ($/MW-day UCAP) | ≈ $/kW-year [D] | Auction date / notes | Source |
|---|---|---|---|---|
| 2024/25 | $28.92 | $10.6 | — | [S&P Global](https://www.spglobal.com/market-intelligence/en/news-insights/articles/2024/8/pjm-capacity-auction-clears-at-record-price-of-269-92-mw-day-across-footprint-82638602) |
| **2025/26** | **$269.92** (BGE $466.35, Dominion $444.26) | $98.5 | 30 Jul 2024; record high | same; [PJM report](https://pjm.com/-/media/markets-ops/rpm/rpm-auction-info/2025-2026/2025-2026-base-residual-auction-report.ashx) |
| **2026/27** | **$329.17** (cap) | $120.1 | Jul 2025 | [PJM 2027/28 BRA report](https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2027-2028/2027-2028-bra-report.pdf) |
| **2027/28** | **$333.44** (cap; floor $179.55 UCAP) | $121.7 | 17 Dec 2025; 6,623 MW short of the reliability requirement | same |
| **2028/29** | **$325.00** (cap) | $118.6 | 14 Jul 2026; 6,831.3 MW short; installed reserve margin 14.4% versus 20% target; uncapped simulation $554.72 | [PJM 2028/29 BRA report](https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2028-2029/2028-2029-bra-results-report.pdf) |

**Demand response in the capacity market:**
- ~7,017 MW UCAP of DR cleared for 2028/29 (100% of offers). New Jersey zones: **PSE&G 231.8 MW**, JCP&L 66.4 MW, AECO 40.3 MW, RECO 2.2 MW (PJM 2028/29 report).
- ELCC accreditation for 2027/28: **Demand Resource 92%** (up from 69%) and 4-hour storage 58% (up from 50%).
- The rise reflects FERC docket ER25-1525: the DR **performance window was removed**, so DR becomes a "24/7 resource" ([PJM MC presentation, 23 Jul 2025](https://www.pjm.com/-/media/DotCom/committees-groups/committees/mc/2025/20250723/20250723-item-02---2027-2028-bra-fpr-and-irm---presentation.pdf)).
- 4-hour storage ELCC is 59% for 2028/29 ([Modo Energy](https://modoenergy.com/research/en/pjm-capacity-auction-2028-2029-reliability-price-cap-elcc)).
- **Implication: DR is now accredited for all hours, so a campus DR resource needs to perform year-round, including winter.**

**DR program types** ([PJM DR page](https://www.pjm.com/markets-and-operations/demand-response)):
- Load Management (capacity) for emergency and pre-emergency events.
- Economic DR in the energy market.
- Participation in synchronized reserve and regulation.
- Customers participate through **Curtailment Service Providers (CSPs)**.

### 7.2 Behind-the-meter (BTM) battery and DR revenue
| Item | Value | Source |
|---|---|---|
| Behind-the-meter battery, wholesale-modeled revenue Jul 2025–2026 | **$55–231/kW-yr**; **PSE&G zone $167–231/kW-yr** | [V/T] [Modo Energy, 12 Aug 2026](https://modoenergy.com/research/en/pjm-distributed-bess-wmpa-skip-queue) (modeled, not realized) |
| Front-of-meter distributed battery | $352–449/kW-yr | same |
| Capacity-tag (Peak Load Contribution) shaving | ~**$100/kW-yr** per kW of PLC shaved; PSE&G transmission tag +$162/kW-yr | same |
| Share of BTM revenue from regulation | 47–66% (a thin 750 MW market; revenue erodes as more batteries join) | same |
| Demand-charge shaving | a 2–4 h battery shaves 45–65% of its kW size in demand charges (LBNL, via Modo) | same |
| 4-hour battery capacity revenue, 2028/29 | ~$70/kW-yr ($192/MW-day accredited) | [Modo](https://modoenergy.com/research/en/pjm-capacity-auction-2028-2029-reliability-price-cap-elcc) |
| DR capacity value, 2027/28 | $333.44 × 365 × 0.92 ELCC ≈ **$112/kW-yr gross** before the CSP's share and the Forecast Pool Requirement adjustment | **[D/EST]** rough |
| New Jersey policy | **Garden State Energy Storage Program**: Phase 2 (distributed storage, front-of-meter and behind-the-meter) expected to open in 2026 | [Modo](https://modoenergy.com/research/en/pjm-distributed-bess-wmpa-skip-queue) |

### 7.3 Telecom batteries as a virtual power plant (precedents)
- **Elisa (Finland), "Elisa Distributed Energy Storage" (now Gridle):**
  - Launched early 2020 to optimize Elisa's **base-station backup batteries**.
  - Grew into a VPP across **2,000+ sites, 150 MWh**.
  - Gridle started optimizing distributed telecom battery fleets in 2022.
  - **DNA Tower Finland** was the "world's first tower company to offer battery capacity in electricity reserve markets".
  - **Vantage Towers Spain** partnered with Gridle for VPP capability across mobile sites.
  - Source: [Elisa Industriq / Gridle](https://www.elisaindustriq.com/gridle).
- **O-RAN and 3GPP direction:** power-source-aware RAN, i.e. battery state of charge and renewables (TR 28.931 KI#9; ETSI ES 202 336-11) ([O-RAN WP 2025](https://mediastorage.o-ran.org/white-papers/O-RAN.SuFG.Potential%20Energy%20Savings%20Features%20in%20O-RAN%20white%20paper%202025-01.pdf)).
- **U.S. telcos:** we found no verified Verizon, AT&T or T-Mobile tower-battery VPP program. The only Verizon grid-support example is the Flex Alert switch to backup power described in §5.
- **Caveat for the pitch:** backup batteries exist for resilience. FCC and state backup-power expectations, plus Verizon's own outage risk, limit how deeply they can be discharged.
  - **Simulator rule:** reserve a minimum state of charge for N hours of outage autonomy.
  - Treat **N as a policy input**. Do not invent a regulatory number.

---

## 8. Occupancy-driven HVAC savings in universities (Wi-Fi as an occupancy sensor)
| Study | Setting | Result | Source |
|---|---|---|---|
| **Sentinel** (Balaji, Xu, Nwokafor, Gupta, Agarwal; ACM SenSys 2013; UCSD/CMU) | Commercial building; existing Wi-Fi | **17.8%** HVAC electrical savings, actuating 23% of zones for one day. Occupancy correct 86% of the time, 6.2% false negatives (phone power-saving was the main error) | [PDF](https://www.cs.virginia.edu/~bjc8c/class/cs6501-f17/balaji13sentinel.pdf) |
| **MARTINI** (Nweye & Nagy, UT Austin, arXiv 2021) | 5 buildings with Wi-Fi data (1,208 APs, hashed MACs, hourly building-level counts) out of 51 metered buildings, Jul–Dec 2019 | **8.1–10.8%** chilled-water savings (summer), 0.2–5.9% (fall); 1–5% across 51 buildings; ~$170k chilled-water savings | [arXiv 2110.08927](https://ar5iv.labs.arxiv.org/html/2110.08927) |
| **UBC** (Energy & Water Services; Cisco Wi-Fi feeding the BMS every 5 minutes) | Library pilot; lecture pavilion | ~**5%** energy reduction (library); ~10% lower AHU fan speed (lecture hall); start-up delayed about 1.5 h. No comfort complaints | [APPA award application](https://www1.appa.org/membershipawards/documents/UBC%20Wifi%20APPA%20Award%20Application.pdf) |
| **LBNL** (Clark, Prakash, Pritoni et al., ACEEE 2020) | Open-source Wi-Fi-to-occupancy library deployed in **65 campus buildings** | Challenges: static devices and the device-to-person ratio. Supports occupancy forecasting and peak-demand prediction | [LBNL](https://eta-publications.lbl.gov/bibcite/reference/34387) |
| LBNL / UC Merced / UTRC (2010) | Simulation | 10–14% less HVAC energy if occupancy is known throughout the building | [LBNL](https://eta-publications.lbl.gov/publications/occupancy-based-energy-management) |
| PNNL (2021) | Medium offices (simulation) | ~13% whole-building savings with presence-based control; 13–23% with people-count control (higher with an economizer) | [PNNL](https://www.pnnl.gov/publications/energy-savings-occupancy-based-controls-office-buildings) (page returned 403; figures from the search index) |

**Range to use:** **5–18% of HVAC energy** in field studies, with 10% as a defensible central value [D]. Cellular counts can add to Wi-Fi counts **only as aggregates** (§9).

---

## 9. Privacy: CPNI and location data (for privacy by design)
- **47 U.S.C. § 222** [S] ([Cornell LII](https://www.law.cornell.edu/uscode/text/47/222)):
  - **(c)(1):** without customer approval, carriers may use CPNI only to provide the service it came from, or related services.
  - **(f):** using **location** information requires the customer's "**express prior authorization**".
  - **(h)(1):** CPNI includes information on "quantity, technical configuration, type, destination, **location**, and amount of use".
  - **(h)(2) "Aggregate customer information":** "collective data that relates to a group or category of services or customers, from which individual customer identities and characteristics have been removed".
  - **(c)(3):** carriers **may** use and disclose aggregate customer information for purposes beyond (c)(1). Local exchange carriers must do so on nondiscriminatory terms.
  - **Design consequence:** per-building, per-15-minute device counts with identities removed fit the "aggregate" definition. Per-device trajectories do not.
- **FCC enforcement:**
  - **April 2024:** the FCC fined the four carriers ~**$196M** for sharing location data through aggregators without valid consent: **T-Mobile $80M, AT&T $57M, Verizon $46.9M, Sprint $12M** ([The Record](https://therecord.media/fcc-fines-carriers-selling-customer-data); [NBC](https://www.nbclosangeles.com/news/national-international/fcc-fines-wireless-carriers-sharing-user-locations-without-consent/3400831/)).
  - **4 June 2026:** the **Supreme Court (8–1, *FCC v. AT&T*, No. 25-406, consolidated with *Verizon v. FCC*, No. 25-567)** held that FCC forfeiture orders do not violate the Seventh Amendment.
    - Verizon's fine stands; AT&T's case was remanded to the Fifth Circuit.
    - Verizon's rehearing petition was denied (Aug 2026).
    - Sources: [SDxCentral](https://www.sdxcentral.com/news/supreme-court-upholds-fcc-att-verizon-fines-over-location-data-misuse/); [The Hill](https://thehill.com/regulation/court-battles/5909636-fcc-verizon-att-fines-supreme-court/); [Fox Business](https://www.foxbusiness.com/technology/supreme-court-rejects-verizon-effort-46-9m-fcc-fine-refund-location-data-case).
  - **Pitch line:** "Verizon has paid a $46.9M location-privacy fine that the Supreme Court let stand in 2026. Our design never moves an individual location out of the network."
- **Recommended architecture** [design recommendation, not law]:
  - Counting happens inside Verizon or university infrastructure.
  - Export only building/zone × 15-minute counts.
  - Suppress any bin with fewer than k devices (e.g. k ≥ 10) [EST].
  - Optionally add calibrated Laplace noise (differential privacy) to published dashboards.
  - Wi-Fi MACs hashed with rotating salts, as in the MARTINI and UT Austin practice.
  - Have counsel review FERPA for registrar timetables. Class schedules are directory-level data; enrollment-by-student is not.

---

## 10. Engineering parameters for our simulator

| # | Parameter | Value to use | Range / notes | Source / label |
|---|---|---|---|---|
| P1 | 64T64R C-band AAU, peak | **1,200 W** | 1,000–1,400 W | [V] Huawei; [V] Ericsson AIR 6449 port ≤1,000 W |
| P2 | AAU idle (no ES features) / peak | **0.55** | 0.49–0.64 (Huawei fit); 0.58 (EARTH) | [D] |
| P3 | AAU load model | P(L) = P_idle + (P_peak − P_idle)·L | linear in PRB load | [P] Golard 2023; Piovesan 2022 |
| P4 | BBU/DU, purpose-built | **300 W** | low confidence | lafibre (Huawei WP quote) |
| P5 | vDU / MEC server | **150 W at 50%, 185 W at 90%** | idle floor ≈ high; "illustrative" | [P] arXiv 2402.11993 |
| P6 | 3-sector macro radio equipment, peak | **3.9 kW** | 3.3–4.5 kW, plus overhead [EST] 10–100% | [D] |
| P7 | mmWave small cell | **~650 W** | 540–760 W; **sensitivity parameter** | [D/EST] TR 38.864 FR2/FR1 ratio |
| P8 | Indoor 5G small cell (Radio Dot class) | **40 W** | 28–57 W | [V] Ericsson |
| P9 | Indoor DAS remote unit | **45 W** (3 services) | 15 W per service | patent |
| P10 | Symbol shutdown saving (versus zero-load) | **34%** | Ericsson MSTx up to 15% of radio energy | [P]/[V] |
| P11 | Cell DTX/DRX saving | **20%** central | 0.2–71.4% (3GPP range) | [S]/[EST central] |
| P12 | Antenna muting 64T→32T/16T | **230 W per 64T O-RU** | 0–48% (3GPP C-1) | [S] O-RAN TR, TR 38.864 |
| P13 | Carrier/capacity-layer switch-off | **47%** of AAU zero-load power | 260–340 W per 64T O-RU | [P]/[S] |
| P14 | Deep sleep / dormancy | **70%** | Nokia extreme deep sleep up to 95% | [P]/[V] |
| P15 | Wake/transition: micro sleep (SM1) | **71 µs** | TR 38.864: 0 | [P]/[S] |
| P16 | Light sleep (SM2 / 3GPP light) | **1–6 ms** | Cat 2: 640 ms | [P]/[S] |
| P17 | SM3 | **10 ms** | — | [P] |
| P18 | 3GPP deep sleep | **50 ms** (Cat 1) | **10 s** (Cat 2) | [S] |
| P19 | SM4 / cell-off-class sleep | **≥1 s** | NR SSB limit is 160 ms without Rel-19 | [P] |
| P20 | Cell/carrier reactivation incl. UE re-attach | **[EST] 1–5 min** for policy (Non-RT loop >1 s) | **no public vendor figure found**; model it as a pre-wake lead time | [EST] |
| P21 | Network-level AI ES saving baseline (traffic-history only) | **15%** | 6–35% | [V] Verizon/Samsung; others |
| P22 | HVAC saving from occupancy control | **10%** | 5–18% | [P] Sentinel, MARTINI, UBC |
| P23 | PJM capacity price | **$325–333/MW-day** | $269.92 (25/26) | [S] PJM |
| P24 | DR ELCC (2027/28) | **92%** | 69% in 26/27 | [S] PJM |
| P25 | BTM battery, PSE&G zone | **$167–231/kW-yr** | modeled | [V] Modo |
| P26 | Privacy k-threshold | **k ≥ 10** | design choice | [EST] |

---

## 11. 3GPP / O-RAN / standards citations
**3GPP RAN (energy saving):**
- **TR 38.864**: Study on network energy savings for NR (Rel-18). Power model, techniques, gains.
- **TR 21.919**: Rel-19 description. §5.1 *Enhancements of network energy savings for NR* (on-demand SSB SCell, on-demand SIB1, common-signal adaptation).
- **TR 37.817**: Study on enhancement for data collection for NR and EN-DC (AI/ML for NG-RAN: energy saving, load balancing, mobility).
- **TS 38.300**: NR and NG-RAN overall description (NES and AI/ML stage-2).
- **TS 38.331**: RRC protocol.
- **TS 38.743**: Rel-19 AI/ML for NG-RAN enhancements (the source of the Energy Cost note).

**3GPP SA5 (management and intent):**
- **TS 28.310**: Management and orchestration; Energy efficiency of 5G (centralized and distributed ES, activation and deactivation, compensation).
- **TS 28.541**: 5G Network Resource Model (*CESManagementFunction* IOC).
- **TS 28.312**: Intent driven management services for mobile networks (RAN energy-saving intent, Radio Network Expectation).
- **TR 28.931**: Key Issue #9, "RAN energy saving when using backup batteries" (as cited by the O-RAN WP).

**3GPP SA2 (slicing):**
- **TS 23.501**: System architecture for 5GS (SST table 5.15.2.2-1).

**O-RAN Alliance:**
- **O-RAN.WG1.OAD**: Architecture Description.
- **O-RAN.WG1.NESUC-TR-R003-v02.00**: Network Energy Saving Use Cases Technical Report.
- **O-RAN.WG1.Use-Cases-Detailed-Specification**.
- **O-RAN.WP *Potential Energy Savings Features in O-RAN* v01.00 (Jan 2025)**.
- WG2 A1 and R1; WG3 E2SM-CCC; WG4 Open Fronthaul M-Plane/CUS-Plane v15 (RF channel ES, ASM, O-RU Deep Hibernate).

**Other:**
- **ETSI ES 202 336-11**: battery-system monitoring and control information model.
- **GSMA NG.116**: Generic Network Slice Template (GST) / NEST.
- **CAMARA**: Quality on Demand, Network Slice Booking, Dedicated Networks.
- **TM Forum TMF921**: Intent Management API.

**Law:**
- **47 U.S.C. § 222**.
- ***FCC v. AT&T***, No. 25-406 (U.S. June 4, 2026).

---

## 12. Grid/DR economics summary table
| Item | Value | Label |
|---|---|---|
| PJM BRA 2025/26 | $269.92/MW-day (≈$98.5/kW-yr) | [S] |
| PJM BRA 2026/27 | $329.17/MW-day (≈$120.1/kW-yr) | [S] |
| PJM BRA 2027/28 | $333.44/MW-day (≈$121.7/kW-yr) | [S] |
| PJM BRA 2028/29 | $325.00/MW-day (≈$118.6/kW-yr) | [S] |
| DR ELCC 26/27 → 27/28 | 69% → 92% | [S] |
| 4-hour storage ELCC 26/27 → 27/28 → 28/29 | 50% → 58% → 59% | [S]/[T] |
| DR cleared 2028/29 (RTO / PSE&G / JCP&L) | 7,017 / 231.8 / 66.4 MW UCAP | [S] |
| BTM battery revenue (PSE&G) | $167–231/kW-yr (modeled) | [V] |
| Capacity-tag shaving | ~$100/kW-yr | [V] |
| PSE&G transmission-tag shaving | +$162/kW-yr | [V] |
| DR capacity value, gross | ~$112/kW-yr (27/28) | [D/EST] |
| Telecom VPP precedent | Elisa 2,000+ sites, 150 MWh; DNA Tower in reserve markets; Vantage Towers Spain | [V] |

---

## 13. Open gaps (search budget exhausted, or no source found)
1. **Datasheet wattage for a mmWave (28/39 GHz) small cell** (Samsung Access Unit, Ericsson Streetmacro 6701/6705). No public figure found; P7 is a derived estimate.
2. **Measured cell/carrier reactivation time** (minutes versus seconds) from a vendor. P20 is an estimate.
3. **Verizon + Enersponse.** Unverified; drop it unless the team has a primary document.
4. **Verizon coverage at SHI Stadium.** Unverified.
5. The NGMN "BS ≈ 50% of site power" figure and the GSMA *Mobile Net Zero 2023* shares were taken from secondary citations in arXiv 2402.11993, not the original PDFs.
6. Rel-17/18 slicing feature list (NSAC and others) and the O-RAN A1 Enrichment Information service were stated from knowledge and need spec confirmation.
7. A primary source for the PNNL occupancy-control figures (the page returned 403).
