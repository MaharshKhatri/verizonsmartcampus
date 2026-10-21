# Founder's contender v3: "PROVE IT": every copper replacement proves itself, at install and every night after

**One line:** On Oct 15, 2026 the FCC stopped requiring carriers to show that copper replacements work with alarms, medical alerts and other key applications. Verizon's own Voice Connect guide says "Compatibility is determined by your testing of your alarm and/or medical device at time of install." PROVE IT is the test. It is a routine on Verizon's replacement box, or a $1.50/month ThingSpace probe for retrofits, that proves in-band, end to end, that the voice, the alarm, the medical alert and the elevator HELP button get through. It runs at install, so a pass sends no truck, and then every night. Verizon sees the health of every lifeline it moved, per wire center, across 1,763 retiring wire centers.

## Problem (all verified; sources in research/06 and research/sources)
**Scale and timing**
- Verizon and Frontier 2026 copper-retirement notices: 1,763 wire centers in 21 states. Piscataway (Busch/Livingston area) is on or after Dec 10, 2026.
- Verizon's B1, PBX-trunk and key-system discontinuance (WC 26-228) lists NJ "on or after Oct 23, 2026". We found no pause for it.
- The residential and business legacy-voice application (WC 26-227) was pulled from auto-grant on Sept 25 (DA 26-1038). It has about 615 filings.

**The rules stopped checking (FCC 26-19, effective Oct 15, 2026)**
- §63.602 is removed: no showing of "interoperability with key applications".
- The customer notices are gone: "may not provide line power" and "steps ... to ensure safe use".
- The FCC refused AICC's alarm condition (G.711, RFC 2833 disabled) and only "encourage[s] carriers to ... prevent alarm signaling failures". AICC counts about 5M dialer alarm panels.
- The FCC's §9.20 backup-power rule was removed in 2026 ("sunset ... September 1, 2025").

**Verizon's own replacement shifts the burden to the customer (Voice Connect / BPC100 guide, verified)**
- The alarm company's number must be keyed in by hand (##21*number#), the box power-cycled, then the alarm tested: "Failure to verify may result in your alarm not working."
- "Verizon is not responsible for unsuccessful alarm responses or medical device relays."
- Backup is 3 AA batteries: "up to 3 talk hours, or up to 23 standby hours", replaced "every six months or after a power outage".
- Verizon's mailed T2050-to-BPC100 swap guide mentions alarm, medical or ##21 zero times.
- Installs are done by technicians: "installed and serviced by the same reliable technicians".
- The BPC100 supports Contact ID only.

**Elevator code checks the wire, not the voice**
- A17.1 2.27.1.1.6 line verification "shall not require activation of the two-way communication link" and may take up to 24 h.
- Chicago inspections: about 24% of elevator maintenance violations are emergency-phone faults (wrong address, wrong car, old contractor).
- Analog stations behind cellular gateways lose diagnostics (Talkaphone's own notes).

**Mobile "adequate" coverage is an outdoor map** (47 CFR 1.7004(c)(5)), while the phone jack and the alarm panel are in the basement.

## Product
- **PROVE at install** (self-install, no truck when it passes). Through the real Verizon voice path to test endpoints, it checks:
  - voice both ways;
  - alarm Contact ID handshake and kiss-off to the registered number (catches a missing ##21);
  - medical-alert path (pre-arranged with the monitoring company);
  - fax T.30;
  - battery present (AC-pull test);
  - RF at the placement spot (RSRP/RSRQ/SINR, frame loss), with "move it 1 m to the window".
  - It prints or texts a receipt.
- **PROVE nightly:**
  - the same in-band checks on a schedule;
  - mains and battery sentinel with predicted minutes left;
  - for elevators, the two-direction in-car acoustic test, delivered location label and answer/redirect time (A17.1's 45 s).
- **Fault routing:** to Verizon (RF, gateway), the customer or alarm company (registration, battery), the elevator contractor (speaker, mic) or dispatch (no answer). Results go to a hash-chained evidence record.
- **Cutover Watch:** carrier-facing lifeline health per wire center. No vendor offers a carrier-side view.
- **Where it runs:** in production, as BPC100/Inseego firmware via Verizon MDM; for retrofits and the demo, a ThingSpace self-serve LTE-M probe ($1.50 to $6 a month).

## Verizon value (labeled assumptions; no copper savings credited to us)
1. **Cost of services:** install truck rolls avoided when PROVE passes. Formula: migrated lines x pass share x cost per roll. Illustration: 100k lines x 60% x $250 = $15M. Repeat visits for silent alarm failures are avoided too.
2. **A faster, cleaner copper exit:** evidence that answers the objection classes in 26-227 (alarms, medical, power, coverage). Verizon's 2022 figure was about $180M/yr from 36 COs; that is a reason speed matters, not our claim.
3. **Retention at a forced migration:** alarm and medical households are the stickiest landline customers (17% and 24% of keepers).
4. **"Verizon did what the FCC encouraged":** a voluntary, evidence-backed standard.

## Rutgers as proving ground
- **The Rutgers PROVE Lab (ECE bench):** the first public device-by-path matrix of alarm formats, PERS bases, fax and TTY across Verizon's replacement paths, with success rates. Nobody publishes this.
- **Elevator PROVE pilot** on Rutgers cars: the HELP audit for answer time vs 45 s and location known, the visual car audit, and machine-room RF.
- **Household panel:** consented commuter students in retiring wire centers (Piscataway, Metuchen, Dunellen, South River, Fords): what is plugged into the copper, plus an indoor 5/1 and VoLTE test at the jack.

## Demo (mostly built in prototype/prove)
- **Box beats:**
  - Hold up the BPC100: "Today a technician drives out to plug this in."
  - Plug in an alarm keypad, an old phone and a medical-alert base; press PROVE.
  - The receipt reads VOICE ok, ALARM kiss-off 5.8 s ok, BATTERY none: AAs in the mail, SIGNAL move 1 m to window, then TRUCK NOT NEEDED.
  - Swap the box per Verizon's guide and press PANIC: the keypad says "sent", PROVE says "no kiss-off: alarm number not registered".
- **Elevator beat:** tape the car mic, and the ticket goes to the elevator contractor.
- **Map:** 1,763 wire centers.
- **Already built:**
  - console, fault routing and hash-chained ledger;
  - acoustic two-direction test;
  - Contact ID / kiss-off model, which shows alarm delivery collapsing with frame loss (5% loss leaves 60% delivered within 4 tries in the model), so placement RF matters more for alarms than for voice;
  - fleet model: mean days a broken elevator phone stays broken, 107 under annual inspection, 45 with line monitoring, 2.8 with PROVE.

## Weaknesses
- **Verizon may already do some of this.** Its technicians test at install, and MDM may see battery state.
- **Prior art:**
  - alarm dealers' cellular communicators;
  - IP emergency phones that self-test;
  - EU lift phones with audio tests;
  - UK SENTINEL managed migration.
- **The money is moderate and assumption-driven.**
- **The campus is the proving ground, not the customer**, and Rutgers' own copper exposure is probably small.
- **The demo needs care:** medical-alert and central-station tests require permission, and we never dial 911.

## v4 corrections and merges (latest research; these override anything above)
- **Campus anchor = WHO ANSWERS (elevators), with no in-car work.**
  - A unit at the gateway's analog port in the machine room (fail-safe relay, so the car always wins the line) runs three checks:
    - a nightly test call through the real migrated Verizon voice path to a Verizon-hosted responder: tones both ways, DTMF integrity, VoLTE registration, RF, battery;
    - passive metadata on every real call: digits dialed vs a registry (old contractor, 911 misprogramming), seconds to answer, 45 s redirect, voicemail/IVR detected from spectral features only;
    - a monthly 10-second confirmation that the real answerer's screen shows the right building and car.
  - The in-car two-transducer acoustic test is an optional add-on installed by a licensed mechanic.
  - Evidence: Chicago inspections, 24% emergency-phone faults. Ooma AirDial at BOMA 2024 (vendor claim): "about 50% of them don't work at the time we go to replace them". FDNY: 27,247 occupied-elevator emergencies in 2025, 98.5% via the phone. Kings III reportedly says its auto-test cannot detect mic, speaker or wiring faults. UK SENTINEL excludes lift audio.
- **National scale = Plug-and-PROVE for Voice Connect/BPC100 installs.**
  - Verizon has about 46k fixed-wireless POTS-replacement customers nationwide, against about 140k legacy lines in Frontier's 8 states alone and 277k/750k in Verizon filings (press). Installs must scale several-fold.
  - The technician visit checks only phone jacks and coverage; alarm and medical are left to the customer. Device swaps are already mail-and-IVR self-installs.
  - Self-proof at install is a capacity enabler, not just a cost saver.
- **Alarm scope narrowed.** Panels already send periodic Contact ID 602 test signals that central stations supervise, so the kiss-off check is install-time only (and "a kiss-off is not proof", per Napco). It is not a nightly product.
- **The lab resolves Verizon's own contradictions.** For the same BPC100 hardware, Verizon and Inseego documents disagree on medical alerts ("cannot be made" / "supports most" / "not compatible") and on fax. The Rutgers PROVE Lab publishes the measured matrix.
- **FIND precedent.** BT searched its call records for alarm-centre numbers in 2020, so cite it as precedent, not invention. Verizon owns a lapsed speaker/mic self-test patent (US8630423), so patent risk is low.
- **FCC framing.** The home-phone exit (26-227) is paused. The business-line exit (26-228: B1, PBX trunk, key system; NJ with no "portions of") drew no pause, and authority starts Oct 23, 2026 per the docket. Never say "approved".
