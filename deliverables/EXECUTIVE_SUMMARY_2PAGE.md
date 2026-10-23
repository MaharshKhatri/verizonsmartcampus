# PROVE: every lifeline Verizon moves arrives with proof it still reaches someone

**2026 Verizon Smart Campus Innovation Challenge · Rutgers University · Pillar 1: AI-Driven Automation & Efficiency (secondary: Pillar 2, Cost & Sustainability Transformation)**

> **In brief.**
> - **The gap.** When Verizon swaps a copper line for a wireless box, customers with an alarm are asked to test it themselves, and a clear phone call can't tell them whether the alarm works.
> - **PROVE.** It turns that test into one guided check with a receipt. A model learned from bench alarm tests decides whether the signal at that spot is strong enough.
> - **The bench result** *(this line follows the video's decision-table row)*.
>   - *Row 1:* on our bench at Rutgers, at one weak signal, phone calls on two carriers' boxes were clear [k/20] times while alarms got through about [m/20]. The alarm needed [X] dB more signal than a clear call.
>   - *Row 1b:* with the alarm number not registered, the call was clear [k/20] times and the alarm got through [m/20].

## The problem: "sent" isn't "received"
- **How many lines move.** Verizon replaces retired copper with fiber or cable VoIP, mobile service, or a fixed-wireless box (Voice Connect, Voice Gateway, Business Phone Connect), which connects the old phones and alarm panel to Verizon's LTE network. PROVE is for that box.
  - Verizon told the FCC this summer that about **46,000** homes and businesses use these boxes.¹
  - Two 2026 filings cover about **417,000** more legacy lines.²
  - Verizon's 2026 copper-retirement notices name **1,763** wire centers in 21 states, Piscataway's among them.³
- **What is plugged in.** Some of those lines carry alarm panels, and no filing says how many. The alarm industry's committee told the FCC that about 5 million installed panels still dial out over phone lines.⁴ Verizon's copper page promises support for "many legacy alarm systems".
- **Who tests.** Verizon's guide for the box says alarm compatibility "is determined by your testing ... at time of install", and warns that failure to verify "may result in your alarm not working".⁵ The box-swap guide's only check is "make a test call".
- **Why nobody notices.** A clear test call says nothing about the alarm. The panel finds out only on the night it has to call.
- **Why now.** The FCC encouraged carriers "to ensure their IP networks are appropriately configured so as to prevent alarm signaling failures".⁶ PROVE lets Verizon show, voluntarily and home by home, that it did.

## The solution: a test record for every migrated lifeline
1. **One guided check at install.** The customer, technician or alarm company presses PROVE, then the panel's own test. PROVE listens on the line and checks three things:
   - the receiver picked up (handshake);
   - the panel sent a well-formed Contact ID code (checksum);
   - the receiver confirmed it (kiss-off).
   It also checks voice both ways and battery backup. The alarm company still confirms the event on its side, as today.
2. **AI that sets the bar.**
   - **Learned signal bar.** A logistic model fitted to bench alarm tests maps the box's SINR to the chance an alarm gets through on the first try, with a confidence interval. It decides GREEN or MOVE THE BOX. Until bench data exists, the bar comes from an assumed loss model; it is a placeholder, not a prediction. Bench refit: [x] dB, CI [a-b], from n = [N] bench alarm tests on one cell. Field data refits it in Phase 1. A leaf-on margin is an assumed dB offset, stated as such.
   - **Fault triage.** A triage model routes each failure to its owner: Verizon RF, the alarm company, the customer's batteries, or a copper line not yet moved. It is 92% accurate in simulation, and 87% when our symptom assumptions are off by 15 points.
   - Fix wording is rule-based today.
3. **A receipt, spoken through the handset and printed or texted.**
   - **GREEN:** all checks passed, no visit requested.
   - **FIX AND RE-RUN:** a plain instruction, e.g. "move the box nearer a window", "re-enter the alarm number", "insert batteries".
   - **VISIT NEEDED:** names the right party.
   - Every receipt is a hash-chained test record, never a guarantee.
4. **After install.** The same checks can repeat on a schedule. Cutover Watch rolls results up per migration batch for Network Transformation.
5. **Campus extension (for the final).** WHO ANSWERS for elevator HELP phones:
   - a challenge-response test call ("press 1 and read back the car ID");
   - time to acknowledgement, against A17.1's rule that an unacknowledged call be redirected within 45 s;
   - caller-ID continuity at cutover.

## The ask: two phases, the first with no firmware
| Phase | What | When | Cost |
|---|---|---|---|
| **1. Pocket PROVE tap** | For 30 days, technicians on one batch of alarm installs carry a pocket tap, against a matched batch without it. The tap is a Raspberry Pi with a passive, isolated line tap on the box's alarm port, a USB sound card, a small thermal printer and a battery. It runs our decoder (`prototype/prove/tap.py`). It reads signal from the box's own diagnostics, or a labelled proxy phone. The receipt prints or goes to the technician's phone. Spoken prompts through the handset and automatic battery checks arrive with Phase 2. | Ready to start after the bench readout | About $100-200 in parts per tap, less than one truck roll. No change to the box or the network. |
| **2. Box firmware** | The same checks shipped to the box through Verizon device management, for self-installs and mail-in swaps. The box already decodes DTMF to dial. PROVE is a small add-on to the box's existing tone decoder: a Contact ID parser and two tone detectors. We estimate it at well under 1% of a modest DSP and about 2 KB of memory (`tap.compute_budget()`); this is an estimate, not yet ported or measured on the box. | Firmware scoping with the box's maker after the trial readout | Engineering time only |

**Pre-registered success rule for Phase 1** (written before the trial, so nobody can move the goalposts):
- **Primary: the catch rate.** This is the share of alarm installs where PROVE flags an alarm failure that a plain phone call passed, reported with its 95% CI. It is measurable within one batch: about ±3 points at 300 installs if the rate is near 5-10%.
- **Secondary:**
  - the share of PROVE installs that end GREEN after at most one fix (target ≥ 95%);
  - 30-day repeat dispatch and care contacts vs the matched batch, reported as estimates.
- **Power, stated up front.** A significance claim on repeat dispatch needs about 3,200 installs per arm (a 2-point drop from a 10% base, 80% power, two-sided 5%). That is more than one batch, so we don't promise it.
- **Break-even:** the PROVE cost per install ÷ Verizon's loaded repeat-dispatch cost.

## Why Verizon
- **Truck rolls, sized without invented dollars.**
  - **Per 1,000 alarm installs:** each 1-point drop in 30-day repeat dispatch avoids 10 truck rolls, and each 1-point drop in care contacts avoids 10 calls. Value = those counts × Verizon's own loaded costs (asked of the mentor).
  - **For scale only:** vendor blogs put a loaded truck roll at $250-1,000. At the low end, 1 point per 1,000 installs is $2,500.
- **One RAN-native number Verizon can reuse.** The bench reports delta: how many more dB of signal Contact ID needs than a clear call, on each box against its own dropout point.
  - Applied to the address-level indoor coverage predictions Verizon already uses to qualify homes for fixed wireless, that margin flags alarm homes near the edge **before install**, without PROVE touching customer data.
  - It describes the alarm format's fragility, not the quality of Verizon's network.
  - Verizon can join our trial timestamps to its own eNB/IMS traces.
- **Addressable base, as a range until Verizon counts it.** The alarm committee's 5 million dial-out panels⁴ divided by the FCC's 78 million wireline voice connections (June 2025)⁷ is about 6%. Divided by the 26 million residential connections, it is about 19%. Applied to 46,000 boxes, that crude range is about 3,000-9,000 alarm households. Verizon can replace it with an exact count: every box with an alarm number registered via ##21 (mentor question 6).
- **Safer no-truck migrations.** Verizon already ships mail-in swaps and self-installed gateways. PROVE makes that path safe for the households that need it most.
- **Retention at a forced migration.** A forced move is a moment a household can leave, and Verizon's CEO calls churn the company's biggest lever (Jan 30, 2026). A green receipt gives an alarm household a reason to stay.
- **Built on Verizon's stack:**
  - the replacement box (VoLTE; firmware via device management);
  - a proposed Verizon-hosted IMS test receiver for ground truth on Verizon's leg;
  - ThingSpace for reporting;
  - the order and dispatch record.

## Evidence (what is real today)
| Item | Status |
|---|---|
| Copper notices, FCC filings, Verizon device guides, FCC order text | Primary sources read and saved in `research/sources/` |
| Working prototype (`prototype/prove`) | Contact ID encoder/decoder with handshake and kiss-off detectors; whole-call tap analyser; learned signal bar with bootstrap CIs; fault triage; install, cutover and elevator receipts; hash-chained evidence ledger verified in the browser; live console; 67 automated tests |
| Bench at Rutgers | [Filled before submission: arms, n, CIs.] Three arms: lab baseline, another carrier's box, Verizon's box. Attenuation sweep in 2 dB steps at matched SINR. "Clear" means PESQ ≥ 3.0, a pre-registered rule. Results go to Verizon first. |
| Modelled, labelled as such | Speech and Contact ID run through the same simulated path, with codec concealment and bursty radio loss. The alarm's **first try** drops below 90% at about 2% frame loss, while voice holds to about 5%. The panel's **retries** then rescue most alarms (90% within 4 tries up to about 10%). Our own model therefore predicts that weak signal shows up first as **slow, retried confirmations**, not outright failure, and the receipt flags exactly that: "confirmed only after retries" is a WARN, not GREEN. In the worst case (no concealment), retried alarms and voice fail together. Speech quality is a crude proxy, not PESQ. |

**Honest negatives we publish.** Passive "who answered?" detection fails in our simulation of a 2-wire line once the car's location message plays, so we switched to challenge-response.

## Rutgers
- **Rutgers has already done this for two lifelines.** It moved fire communicators in 450 buildings to dual-path IP/cellular units in 2020, and in 2023 replaced blue lights with solar units that report their health daily. Elevator HELP phones are the lifeline still without that proof. PROVE adds it, and we are proposing a pre-announced pilot to Facilities ([N] cars in scope, per Facilities/OIT).
- **A PROVE bench in a Rutgers ECE lab** produces measured alarm-over-wireless data we could not find published anywhere.
- **A usability session** with older-adult volunteers: [k of n] followed PROVE's spoken fix to a green receipt without help (counts only, never percentages).

## Risks and how we handle them
- **Verizon may already test some of this.** We have sent the mentor six questions (Oct [22]). PROVE adds the in-band alarm check (answered and confirmed), which device telemetry cannot see.
- **Dealers are moving panels to cellular communicators.** PROVE is for the homes still on the box's alarm port. The same engine covers voice, signal, battery and elevator HELP lines as that number shrinks.
- **Liability.** The receipt is a test record, never a guarantee, and the alarm company still confirms the test on its side.
- **Safety.** No 911 calls, ever. We use our own receivers only, and used panels are factory-defaulted before they touch a line.

---
¹ Verizon applications in WC 26-170 (FL PSC copy) and WC 26-227 (RI PUC copy), July-Aug 2026. ² WC 26-227 (~277,000 lines) and WC 26-170 (~140,000). ³ Verizon and Frontier 2026 network-change notices; NJ notice 2026-03-A-NJ lists Piscataway (PSWYNJPI). ⁴ AICC filing in the FCC copper-retirement proceeding. ⁵ Verizon Voice Connect user guide. ⁶ FCC 26-19 ¶31 (March 2026). Since Oct 15, 2026, 47 CFR 63.602's adequate-replacement test no longer applies. ⁷ FCC, *Voice Telephone Services: Status as of June 30, 2025* (saved in `research/sources/`).
