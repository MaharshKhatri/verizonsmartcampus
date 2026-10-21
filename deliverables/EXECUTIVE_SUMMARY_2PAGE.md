# PROVE: every lifeline Verizon moves arrives with proof it still reaches someone

**2026 Verizon Smart Campus Innovation Challenge · Rutgers University · Pillar 1: AI-Driven Automation & Efficiency (secondary: Pillar 2, Cost & Sustainability Transformation)**

## The problem: "sent" isn't "received"
- **The volume.** When Verizon retires a copper line, the replacement is fiber or cable VoIP, mobile service, or a fixed-wireless box (Voice Connect, Voice Gateway, Business Phone Connect). The box connects the old phones and alarm panel to Verizon's LTE network, and PROVE is for that box.
  - Verizon told the FCC in July and August 2026 that about **46,000** homes and businesses use these boxes.
  - Two of its 2026 discontinuance filings cover about **417,000** more legacy lines (277,000 in WC 26-227 and 140,000 in WC 26-170; primary copies saved).
  - Verizon's 2026 copper-retirement notices, including Frontier's, name **1,763** wire centers in 21 states, Piscataway's among them.
- **What is plugged in.** Some of those lines carry alarm panels and medical-alert units, and no filing says how many. The alarm industry's committee (AICC) told the FCC that about **5 million** installed panels still dial out over phone lines. Verizon's copper page promises support for "many legacy alarm systems" and "many medical devices".
- **Who tests it.** Verizon's guide for the box says alarm and medical compatibility "is determined by your testing ... at time of install". It asks customers who use the alarm port to register the alarm company's number and test the alarm, warning that failure to verify "may result in your alarm not working". The box-swap guide's only check is "make a test call".
- **Why nobody notices.** A clear test call says nothing about the alarm, and a panel only finds out on the night it has to call.
- **What the rules require.** In March 2026 the FCC declined the alarm industry's proposed alarm-signaling condition on these transitions and "encourage[s] carriers to ensure their IP networks are appropriately configured so as to prevent alarm signaling failures". Since Oct 15, 2026, no federal rule requires a carrier to show, home by home, that alarms still work: the adequate-replacement test in 47 CFR 63.602 was removed.

## The solution: PROVE, a test record for every migrated lifeline
1. **At install:** the customer (or the alarm company, remotely) presses PROVE and then the panel's own test. PROVE listens through Verizon's live network and checks three things:
   - the receiver picked up (handshake);
   - the panel sent a well-formed Contact ID code;
   - the receiver confirmed it (acknowledgement).

   The alarm company confirms the event on its side, as today.

   It also checks signal at the box's exact spot (judged on its worst season), voice both ways, and battery backup. A proposed synthetic test call to a Verizon-hosted receiver would prove the part of the path Verizon owns.
2. **A receipt, spoken and printed:**
   - **GREEN:** no visit needed.
   - **FIX AND RE-RUN:** a plain instruction spoken through the handset, e.g. "move the box toward a window", "re-enter the alarm number", "insert batteries". With consent it can also be texted to a caregiver.
   - **VISIT NEEDED:** names the right party (Verizon technician, alarm company).
3. **After install:** the same checks can repeat on a schedule. Cutover Watch rolls results up per migration batch for Network Transformation.
4. **Campus extension (proposed to Facilities for the final):** WHO ANSWERS for elevator HELP buttons. A challenge-response test call checks:
   - "press 1 and read back the car ID";
   - the time to acknowledgement, against A17.1's rule that an unacknowledged call be redirected within 45 s;
   - caller-ID continuity at cutover, since some answering centers identify the car by the calling number.

## Why Verizon
- **Fewer failed self-installs.** Value is measured on install KPIs (first-time-right, repeat dispatch within 30 days, care contacts per install) plus one new KPI, alarm households confirmed working. We are asking the Verizon mentor which of these Verizon tracks today. Formula: avoided visits and calls × Verizon's own loaded costs. No invented dollars.
- **Safer no-truck migrations.** Verizon already ships mail-in swaps and self-installed gateways. PROVE makes that path safe for the alarm households that need it most.
- **Retention at a forced migration.** A forced migration is a moment a household can leave, and Verizon's CEO calls churn the company's biggest lever (Jan 30, 2026). A green receipt gives alarm households a reason to stay.
- **Built on Verizon's stack:**
  - the replacement box (VoLTE; firmware via Verizon device management);
  - a proposed Verizon-hosted IMS test receiver;
  - ThingSpace for the reporting path;
  - the order and dispatch record.
- **The ask:** a 30-day trial in one migration batch's self-install kits, against a control group.

## Evidence (what is real today)
| Item | Status |
|---|---|
| Copper notices, FCC filings, Verizon device guides, FCC 26-19 text | Primary sources read and saved in `research/sources/` |
| Working prototype (`prototype/prove`) | Contact ID encoder/decoder with handshake and kiss-off detectors; install receipt (signal, voice, alarm, battery, worst-season signal); before/after cutover receipt (SAME ANSWER); two-direction acoustic test for elevator phones; challenge-response "who answers" test; hash-chained evidence ledger verified in the browser; live console; 55 automated tests |
| PROVE bench in a Rutgers ECE lab | **Planned** Oct 22-31 (live-box gate K1 on Oct 29). Real panel, Verizon box, three paths (lab baseline, another carrier, Verizon), CIs reported. Results go to Verizon first |
| Modelled, labelled as such | Alarm delivery falls steeply as frame loss rises (5% loss: 13% first try, 60% within 4 tries; 30 simulated calls). Voice quality is not modelled; bench test T5 measures both |

**Honest negatives we publish:**
- Passive "who answered?" detection fails in our simulation of a 2-wire line once the car's location message plays, so we switched to challenge-response.
- Rutgers moved fire communicators in 450 buildings to dual-path IP/cellular units in 2020, and in 2023 replaced its blue lights with solar units that send daily health reports. Rutgers is the proving ground, not a countdown.

## Rutgers
- A **PROVE bench in a Rutgers ECE lab**: measured alarm-over-carrier data we could not find published anywhere.
- A **usability session** with older-adult volunteers on unboxing and self-install.
- For the final, an **elevator HELP pilot we are proposing to Facilities**, framed as a joint fix.

## Risks and how we handle them
- **Verizon may already test some of this.** We are asking the mentor five questions (sent Oct [22]). PROVE adds the in-band alarm check (answered and acknowledged), which device telemetry cannot see.
- **Dealers are moving panels to cellular communicators.** PROVE is for the homes still on the box's alarm port.
- **Liability.** The receipt is a timestamped test record, never a guarantee, and the alarm company still confirms the test on its side.
- **No 911 calls, ever.** Our own receivers only. Used panels are factory-defaulted before they touch a line.
