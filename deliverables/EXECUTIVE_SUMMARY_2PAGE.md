# PROVE: every lifeline Verizon moves arrives with proof it still reaches someone

**Verizon Smart Campus Innovation Challenge 2026-27 · Rutgers University · Pillar 1: AI-Driven Automation & Efficiency (secondary: Pillar 2, cost)**

## The problem: "sent" isn't "received"
- **The volume.** When Verizon retires a copper line, the home or business gets a replacement box on Verizon's wireless network. Verizon reports about **46,000** fixed-wireless POTS-replacement customers nationwide. Its 2026 discontinuance filings cover about **417,000** more lines (two filings, verified). Copper-retirement notices in 2026 name **1,763** wire centers in 21 states, Piscataway's among them.
- **What is plugged in.** Many of those lines still carry alarm panels and medical-alert units. The alarm industry counts about **5 million** dialer alarm panels still in service.
- **Who tests it.** Verizon's own guide for the box says alarm and medical compatibility "is determined by your testing ... at time of install". It asks the customer to register the alarm company's number and then test the alarm, and warns that failure to verify "may result in your alarm not working". The box swap guide's only check is "make a test call".
- **Why nobody notices.** A keypad that says "sent" cannot tell whether anyone received it. A phone that gives dial tone says nothing about the alarm.
- **The FCC's position.** In March 2026 the FCC declined to impose alarm-compatibility conditions on these transitions. It instead "encourage[s] carriers to ensure their IP networks are appropriately configured so as to prevent alarm signaling failures". Nothing in the process measures whether that happened, home by home.

## The solution: PROVE, a test record for every migrated lifeline
1. **At install:** the customer, or the alarm company remotely, triggers the panel's communicator test. PROVE listens through Verizon's live network and checks three things:
   - the receiver's handshake;
   - a checksum-valid message;
   - the acknowledgement ("kiss-off").

   It also checks signal at the box's exact spot (judged on its worst season), voice both ways, and battery backup. A test call to a Verizon-hosted receiver proves the part of the path Verizon owns.
2. **A receipt, spoken and printed:**
   - **GREEN:** no visit needed.
   - **FIX AND RE-RUN:** a plain instruction spoken through the handset, e.g. "move the box toward a window", "re-enter the alarm number", "insert batteries". With consent it can also be texted to a caregiver.
   - **VISIT NEEDED:** names the right party (Verizon technician, alarm company).
3. **After install:** the same checks can repeat on a schedule. Cutover Watch rolls results up per migration batch for Network Transformation.
4. **Campus extension (Round 3 pilot):** WHO ANSWERS for elevator HELP buttons. A challenge-response test call checks:
   - "press 1 and read back the car ID";
   - the time to a person against A17.1's 45-second rule;
   - caller-ID continuity at cutover, since answering centers often look up the car by it.

## Why Verizon
- **Fewer failed self-installs.** Value is measured on KPIs Verizon already tracks: first-time-right, repeat dispatch within 30 days, care contacts per install, and alarm households confirmed working. Formula: avoided visits and calls × Verizon's own loaded costs. No invented dollars.
- **Safer no-truck migrations.** Verizon already ships mail-in swaps and self-installed gateways. PROVE makes that path safe for the alarm households that need it most.
- **Retention at a forced migration.** Alarm and medical households are among the stickiest landline customers, and a green receipt keeps them with Verizon.
- **Built on Verizon's stack:**
  - the replacement box (firmware via Verizon device management);
  - VoLTE/IMS with a Verizon-hosted test receiver;
  - ThingSpace;
  - the order and dispatch record.
- **The ask:** a 30-day trial in one migration batch's self-install kits, against a control group.

## Evidence (what is real today)
| Item | Status |
|---|---|
| Copper notices, FCC filings, Verizon device guides, FCC 26-19 text | Primary sources read and saved in `research/sources/` |
| Working prototype (`prototype/prove`) | Contact ID encoder/decoder with handshake and kiss-off detectors; install receipt (signal, voice, alarm, battery, worst-season signal); before/after cutover receipt (SAME ANSWER); two-direction acoustic test for elevator phones; challenge-response "who answers" test; hash-chained evidence ledger verified in the browser; live console; 60 automated tests |
| Rutgers PROVE Lab bench (Oct 22-31) | Real panel, real Verizon box, three control paths (straight wire, other carrier, Verizon), CIs reported. Results go to Verizon first |
| Modelled, labelled as such | Alarm delivery falls before voice quality does as frame loss rises (5% loss: 60% delivered within 4 tries) |

**Honest negatives we publish:**
- Passive "who answered?" detection fails on a real 2-wire line, so we switched to challenge-response.
- Rutgers' own fire communicators and blue lights already left copper, so Rutgers is the proving ground, not a countdown.

## Rutgers
- A **Rutgers PROVE Lab** in ECE: measured alarm-over-carrier data that nobody publishes.
- A **usability session** with older-adult volunteers on unboxing and self-install.
- For the final, a Facilities-co-signed **elevator HELP pilot**, framed as a joint fix.

## Risks and how we handle them
- **Verizon may already test some of this.** We asked the mentor (5 questions). PROVE adds the in-band alarm proof, which device telemetry cannot see.
- **Dealers are moving panels to cellular communicators.** PROVE is for the homes still on the box's alarm port.
- **Liability.** The receipt is a timestamped test record, never a guarantee, and the alarm company still confirms the test on its side.
- **No 911 calls, ever.** Our own receivers only. Used panels are factory-defaulted before they touch a line.
