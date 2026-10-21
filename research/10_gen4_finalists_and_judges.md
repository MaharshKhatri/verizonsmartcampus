# Generation 4 final: two finalists, four red teams, five judges

**Finalist F1 (install hero):** Plug-and-PROVE on Verizon's copper-replacement box.
**Finalist F2 (elevator hero):** WHO ANSWERS for elevator HELP calls.
Each got a founder-grade dossier and two independent red teams; then five judge personas scored both on the official rubric.

## Judge panel

| Judge | F1 install hero | F2 elevator hero | Winner |
|---|---:|---:|---|
| verizon_svp | 62 | 57 | F1_install_hero |
| verizon_planning | 59 | 55 | F1_install_hero |
| rutgers_cio | 57.5 | 55 | F1_install_hero |
| rutgers_dean | 55 | 54 | F1_install_hero |
| verizon_business | 56 | 59 | F2_elevator_hero |

**Result: F1 wins 4-1.** Neither wins as written (54-62); every judge puts the fixed version in the high 70s. F1's fixes are edits; F2's need a redesign (challenge-response, Verizon-only checks, Facilities approvals).

### verizon_svp

- **F1_install_hero: 62** (I20 F10 C11 Cr3 P18). This is the only finalist that sits in my own P&L lane. It is a verification step for the box my copper exit actually ships (BPC100, Voice Gateway), it runs over our production VoLTE/IMS and MDM, and its ask (a 30-day trial on one migration batch) is something my Transformation Office could approve on Monday. Impact (20): the criticality is real, since alarm households fail silently and our own guide puts compatibility on 'your testing at time of install', and the scale is anchored in our filings (417k verified lines against 46k installed). But the capacity hero is wrong for us. Voice Gateway is already a self-install, with the alarm number entered in Settings. 348 technicians over six months is noise next to one quarter of Fios installs. And '7x everything installed' compares a stock with a flow and leans on a vendor's 750k. Campus ubiquity is thin, because Rutgers is mostly a room here. Feasibility (10): the bench is buildable (Asterisk AlarmReceiver, a Contact ID panel, a Pi with FXO), but there are three problems. K1, activating a business line in 5 days, is a single point of failure. The 'one button' is false for ALARM in production, because the customer or the dealer still has to trigger the panel test. And the SIP DID leg confounds any 'measured on Verizon's live network' claim unless they run the three-arm control. 'SIA 0/20' would only measure Asterisk, which cannot decode SIA. OLLI-RU with an IRB in 9 days will not happen. Content (11): this is the real stack the exit runs on (box modem KPIs via MDM, an IMS test responder, order and dispatch integration). The ThingSpace puck is padding, and there is no network-native novelty beyond the IMS test number. Creativity (3): an install receipt is sensible and incremental, and Inseego could ship it in one firmware cycle. Presentation (18): the receipt prop and the poster 'break it' table, where judges take home a receipt, are excellent for Rounds 2-3. The video as written has problems. It opens on two text cards. It sets our disclaimer next to 'the FCC no longer asks' and cites an open 214 docket, which my regulatory team would hate. It mislabels 26-227 as the 'home-phone exit'. And its hero receipt certifies a life-safety line with BATTERY: NONE as TRUCK NOT NEEDED. Fixable. With the red-team rebuild (lead on self-install fallout, open on the customer, no dockets, ALARM as the climax, the three-arm bench, Voice Gateway as the hero) I'd put it around 74-78.
- **F2_elevator_hero: 57** (I19 F7 C7 Cr4 P20). The best story in the pool. 'You're stuck between floors at 2 a.m. Who answers?' and 'The code checks the wire, we check the call' are the strongest cold open and tagline any finalist has, and the campus fit is real: elevators are in every Rutgers building, and the walk audit and HELP audit are data nobody else will have. My first question in Q&A, though, would be 'why is this ours?', and the dossier has no answer. Every fault it catches (voicemail, a vacant number, the old contractor, a wrong label) belongs to the owner, the contractor or the answering point. The same check on MarketSpark's AT&T SIM gives the same proof, so the retention lever collapses. Elevator lines are B1 lines under 26-228, which drew no pause, so elevator evidence unblocks nothing in 26-227. The add-on revenue goes to CSG or MarketSpark. The team itself says it is $2.4M a year per 10k lines. Impact (19): criticality is the highest of the finalists and campus ubiquity is high. But the faults it can catch automatically are about 0.1% of the inspections in its own Chicago data, and there is no evidence yet that Rutgers elevator lines ride Verizon at all. Feasibility (7): two independent probes show the hero classifier mislabels real answerers as IVR on a 2-wire tap (20/20 and 25/25) once the car's location message or a live operator's talk-to-silence is present. The synthetic 100% will not survive day one on real hardware. On top of that: a mailed elevator phone with loop-current risk, Facilities and RUPD approvals in 9 days, an overnight census that looks like prank-calling dispatch, and a daily ring-and-abandon probe that no PSAP will accept. Content (7): production is either a CDR query (dialed number, release cause, answer time are already in our records) or partner firmware. The on-camera Verizon piece is a BPC100 in a configuration we do not market for elevators (3 h of talk against A17.1's 4 h standby). Creativity (4): grading the far end of the call is a genuinely fresh reframe. Presentation (20): the opening is excellent, but the video is too dense (8 beats, 5 sources, two code clauses in 47 s). '3 of 4 failed' staged on a Verizon line, right after 'these lines are leaving copper onto Verizon's network', implies our migration strands trapped riders, and that is a sponsor-embarrassment risk in my own competition. The Rutgers card may be empty or all-pass. The 'SAME ANSWER' rebuild (challenge-response, registered address vs registry, caller-ID continuity at the migration order, POTSolve-exclusive) could reach about 75, but only after a hardware pivot inside 18 days.

**Winner rationale.** I pick Plug-and-PROVE, conditionally, and neither finalist is a winner as written (62 vs 57). Five reasons:
1. As the SVP who owns copper retirement and runs the Ambassador Office, I'm judging against the brief's demand for clear, measurable business value tied to a pillar. Plug-and-PROVE is the only finalist whose product lives inside Verizon's own process. It runs on the box we ship, over our VoLTE/IMS and MDM, and writes to our order and dispatch record.
2. Its value maps to metrics GN&T already tracks: first-time-right, repeat dispatch within 30 days, care contacts per install, and alarm households confirmed working. It also maps to our named cost program (copper decommissioning and contractor spend).
3. Its ask, a 30-day trial on one migration batch's self-install kits against a control group, is something I could actually approve.
4. WHO ANSWERS has the better 2-minute story and the better campus fit, but it fails the 'why Verizon?' test. Its faults are carrier-agnostic, its production form is a CDR query or partner firmware, and its revenue is self-admittedly a rounding error. Its hero classifier also breaks on real 2-wire audio, which puts the Round 1 bench at risk.
5. Plug-and-PROVE already carries WHO ANSWERS as its poster and finals campus pilot, so choosing it keeps the elevator story for Rounds 2-3 without betting the video on a broken detector.

The conditions for the video, all taken from the red teams:
- Kill the capacity story ('7x', the ≈1M bar) and pitch reduced self-install fallout instead.
- Strip every docket, '§63.602', 'paused' and 'regulator stopped checking' line.
- Open on the customer: 'Verizon already asks every customer to test their alarm. We made it one button.'
- Make ALARM the climax, with the Verizon side proven by a synthetic call to an IMS test receiver and the dealer side honestly scoped.
- Show only a Contact ID pass line from a three-arm controlled bench.
- Fix the BATTERY: NONE → TRUCK NOT NEEDED self-own.
- Use Voice Gateway as the hero device if it can be ordered.
- Show a measured OLLI usability count, or nothing.

If those land, it is the strongest Verizon-relevant entry in the field, at roughly 74-78.

**What would change my mind.** Any of these would move me to WHO ANSWERS, or knock Plug-and-PROVE down:
1. WHO ANSWERS becomes a Verizon-only cutover acceptance check ('SAME ANSWER'), with all of these in place by early November:
   - challenge-response test calls in place of the passive classifier;
   - the E911 or registered dispatchable address Verizon holds, matched against the owner's building and car registry;
   - a caller-ID continuity check at the migration order;
   - a POTSolve-exclusive feature, so the proof exists only on the Verizon path.
   Combined with its cold open and campus fit, that is a story plus a Verizon-owned mechanism, and it would beat Plug-and-PROVE.
2. OIT or OPRA confirms that Rutgers elevator lines ride Verizon B1 copper in the retiring Piscataway wire center, and the team films one real, Facilities-approved HELP press at Rutgers, graded live. That gives the elevator entry both campus and Verizon relevance.
3. The Verizon mentor (gate K4) says self-install fallout is not a tracked problem, or that Voice Gateway already runs an automated alarm check at install. Plug-and-PROVE's value case then collapses to a firmware nicety.
4. K1 fails: no live Verizon box reaching a controlled receiver by Oct 29. Plug-and-PROVE then has no measured result, and its hero is a simulation.
5. The final Plug-and-PROVE cut keeps the regulatory juxtaposition: Verizon's disclaimer next to the Oct 15 deletions and the paused 26-227 docket. I would mark Presentation down hard for creating public exposure in an open 214 proceeding.
6. Plug-and-PROVE's bench publishes a failure line ('SIA 0/20' or a low Contact ID count) without a non-Verizon control arm. That would be an unfair public claim about our box, and I would mark it down sharply.

### verizon_planning

- **F1_install_hero: 59** (I19 F9 C10 Cr3 P18). Scored as written for the Round 1 video. This is the only finalist that sits inside a process I own: Verizon's box, Verizon's install, Verizon's dispatch. Alarm signaling over the replacement path is a real migration pain point (AICC's no-access appointments and the 3-hour communicator truck rolls are real). An IMS test responder plus firmware pushed through device management is a credible production path, and the receipt is a physical hero you can film. Overreach I would catch on the first pass: (1) The capacity story does not hold. The 46k is a running total of customers, not an install rate. In NJ most copper moves to Fios Digital Voice or to mobile, not to a fixed-wireless box, so f=0.30 is generous. And 125k installs over six months is small next to one quarter of fiber installs. Dispatch capacity is not my bottleneck. My KPIs are first-time-right, repeat dispatch within 30 days, care contacts per install, and no-access appointments. Pitch those. (2) The 'one button' proves ALARM only on the bench. In the field the customer or the dealer still has to put the account on test and trip the communicator, because the box cannot make the panel dial. (3) A kiss-off seen at the box is not delivery, since the receiver's line card can acknowledge a corrupt frame. The 'checksum-valid frame plus kiss-off' Q&A answer fails with any alarm-literate judge. (4) The bench runs panel, then VoLTE, then a PSTN interconnect, then a third-party SIP DID, then Asterisk. With no LAN baseline and no non-Verizon trunk control, 'measured on Verizon's live network' can pin a DID vendor's RFC 2833 handling on us. Asterisk's AlarmReceiver also cannot decode SIA FSK, so 'SIA 0/20' measures your own receiver. (5) A phone's field-test app is a different modem, antenna and band set from the box. 'Move 1 m toward window' from one sample is multipath noise. (6) BATTERY: NONE followed by TRUCK NOT NEEDED certifies a life-safety line with no backup power. (7) The hero box is probably last generation. The Voice Gateway is the self-install box the filings name, and K1 (activating a Business line through Rutgers procurement in 5 days) is a single point of failure. (8) The ThingSpace puck is padding to earn Content points. (9) The first 24 seconds are a quote card and a Federal Register card, and the narration cites docket numbers. 'When the regulator stops checking' reads as a jab at a deregulation Verizon asked for, in Verizon's own contest. (10) There is no campus object. Rutgers is a room unless the OLLI-RU study happens, and an IRB determination in 9 days is not realistic. Fixed version (Voice Gateway as hero, a three-arm controlled bench with one pass line on screen, value as self-install fallout, opening on 'Verizon already asks every customer to test their alarm; we made it one press', no dockets): I see a ceiling of 74-78. Rounds 2-3: the 'break it' table, where judges pull the AAs and take their receipt home, is the best stage demo in either dossier. That holds only if step attenuators replace the steel box and Asterisk runs on a cloud VM rather than behind campus NAT.
- **F2_elevator_hero: 55** (I18 F6 C6 Cr4 P21). Scored as written. It has the best cold open and the best tagline in the pool. 'The code checks the wire; we check the call' is a real insight: under A17.1 2.27.1.1.6(a), verification is written so it never has to place a call. Every campus has elevators, and the re-derivation of the Chicago open data is genuine primary analysis. But it overreaches inside my own domain: (1) The hero classifier sits on a passive 2-wire bridge, so it hears both directions summed. The car's own location announcement, a recorded preamble, or an operator talking to a silent car all classify as IVR (both red teams reproduced this at 20/20 and 25/25). The synthetic 100% will not survive the first real elevator phone. (2) Voicemail and a live person both return SIP 200 OK, so 'signaling checks in Verizon's voice network' cannot do the novel part. The rest (dialed number, release cause, answer time) is a CDR query, and SIT detection on customers' emergency calls is media inspection we will not run in the core. (3) Classifying carriers from LERG data on localcallingguide gives the block holder, not the current carrier, because of number portability. A Network Planning judge catches that in five seconds. (4) The daily pre-answer probe rings a 24/7 answering point and hangs up. PSAPs call abandoned calls back, so this is a non-starter. (5) The video puts an elevator phone on a BPC100, which Verizon does not market for elevators (3 AA cells, 3 h talk against A17.1 standby), so it shows an unsupported configuration of our product. The phone's 20 mA loop-current minimum on an ATA port is untested. (6) The staged faults (voicemail, old contractor, vacant number) total about 6 of 6,725 Chicago inspections. The faults that are actually common (location or car ID, including Nashville) need a cooperative human read-back, not the tap. (7) Verizon value is carrier-agnostic: the same check on MarketSpark's AT&T SIM gives the same proof. Elevator lines are B1 lines under WC 26-228, which drew no pause, so this evidence unblocks nothing. The add-on revenue goes to CSG, MarketSpark or Kings III, and Verizon's take is one LTE-M line. That is why Content is weak. (8) Rutgers elevator lines may not ride Verizon at all (OIT analog over Rutgers copper, Windstream, Kings III cellular), and Gate E answers that only after the video is locked. (9) Overnight calls to posted 24/7 numbers may reach RUPD or RUSSECC, which looks like prank-calling emergency services in front of the CIO. (10) Putting 'lines leaving copper onto Verizon's network' next to '1 of 4 reached a person' and a rival-SIM jab implies our migration causes the failures, when none of the staged faults is a network fault. Fixed version (one real, pre-announced HELP press approved by Facilities and graded live; challenge-response test calls; recast as a Verizon cutover-acceptance check with an ANI-continuity check and a registered dispatchable address check at the migration order): 72-76, with the higher presentation ceiling. But it needs a rebuild of the core detection plus three campus permissions inside 18 days.

**Winner rationale.** Plug-and-PROVE wins 59 to 55. WHO ANSWERS makes the better two minutes of video. Plug-and-PROVE wins because its hero claim survives contact with real hardware and it lives inside a process Verizon owns. Its weaknesses are framing problems: the capacity math, the regulatory jabs, the opening text cards and the last-generation box. Each can be fixed in days without changing the product. WHO ANSWERS' weaknesses are structural. A passive 2-wire tap cannot tell a person from a machine. Signaling cannot either, since voicemail also returns 200 OK. The faults it can catch automatically are the rarest in its own data. And the value is carrier-agnostic, so a Verizon AVP's first question, 'why is this ours?', has no good answer. On Content (15) and Feasibility (15) Plug-and-PROVE leads by 7 points combined, more than WHO ANSWERS' 3-point Presentation edge. Looking ahead to Rounds 2-3, Plug-and-PROVE's poster rig (press PROVE, break it, take the receipt home) is repeatable and survives a noisy hall. WHO ANSWERS' speakerphone on a 2-wire bridge in a crowded venue is exactly where its classifier fails. Conditions for the win to hold: drop 'install capacity' and the ~1M bar from the video in favour of self-install fallout KPIs; open on the customer, not the Federal Register; put only one controlled, pass or neutral measured line on screen (Contact ID through the box, with LAN and non-Verizon-trunk controls); and stop implying that one button makes the panel dial.

**What would change my mind.** I would flip to WHO ANSWERS if, by about Oct 30, three things happen. (a) OIT or the bills confirm that Rutgers elevator lines ride Verizon B1 or a Verizon replacement path. (b) Facilities approves at least one real, pre-announced, filmed HELP press, graded live with a challenge-response read-back of the car ID. (c) The team recasts the product as Verizon's own cutover-acceptance step, with an ANI-continuity check and a registered dispatchable address check at the migration order, which only Verizon holds. That would fix Content and campus fit, and with its better story it would then out-present Plug-and-PROVE. I would also downgrade Plug-and-PROVE below WHO ANSWERS in four cases: K1 fails, so there is no live BPC100 or Voice Gateway on Verizon by Oct 29 and the measured beat becomes a simulation; the Verizon mentor says install-time alarm verification already exists or the Voice Gateway self-install already handles alarm numbers well enough; the alarm dealers' shift to cellular communicators means very few migrated homes still use the box's alarm port; or the team keeps the capacity/~1M framing and the FCC-docket opening in the final cut.

### rutgers_cio

- **F1_install_hero: 57.5** (I17 F9 C11 Cr3.5 P17). STRENGTHS. This pitch fits Verizon best. It sits inside Global Networks & Technology's own copper/TDM exit, the program run by the organisation behind this competition. The hero object is Verizon's actual copper-replacement box (BPC100 / Voice Connect), tested over Verizon's VoLTE/IMS and device management. The core claim is one an ECE bench can really prove in 18 days: a Contact ID alarm event goes through a live Verizon box, reaches a receiver and comes back acknowledged. The receipt with three verdicts (truck not needed, fix by text, truck needed) is a strong physical prop, and the Feb 3 'break it' table, where judges press PROVE and keep their receipt, would be the best poster in the room. For my office there is little operational exposure: nothing touches campus lifelines, RUPD or Facilities.

PROBLEMS IN THE SCRIPT AS WRITTEN.
- Opening: the first 24 s are two text cards, and both are regulatory gotchas: Verizon's 'determined by your testing' disclaimer, then the Federal Register.
- Numbers: the capacity beat compares a running total (46k customers installed) with installs still needed. 'About a million' gets 64% of its lines from a vendor blog, '7x' multiplies an assumption, and 'home-phone exit' mislabels WC 26-227.
- Premise: Verizon already has customers self-install the Voice Gateway, so 'the truck goes only where the receipt says' is a weak argument.
- Sponsor risk: Asterisk cannot decode SIA. Publishing 'SIA 0/20, measured on Verizon's live network' would make a false public claim about Rutgers' own telecom vendor, and that would embarrass us.
- Tagline: 'When the regulator stops checking' jabs at a deregulation the sponsor supported, inside the sponsor's own contest.
- Hero receipt: it certifies a lifeline with BATTERY: NONE and TRUCK NOT NEEDED. It also shows a keypad being 'plugged in', but panels connect through the RJ31X jack.
- Research compliance: an OLLI-RU IRB determination in 9 days is unrealistic. Filming older adults without one is a Rutgers compliance risk.
- Smart Campus fit is thin: Rutgers appears as a lab bench and a community-service study, not as a campus system.

OUTLOOK. Almost every fix is an edit: open on the customer, make the alarm path the hero, run three controlled bench arms with a locked G.711 DID, and pitch self-install fallout instead of capacity. The path through Rounds 2-3 is credible.
- **F2_elevator_hero: 55** (I19 F6 C7 Cr4 P19). STRENGTHS. This is the best story in the pool and the most relevant to campus. Elevator HELP is life safety in every building on every Rutgers campus. The cold open ('stuck between floors at 2 a.m., who answers?'), the Chicago 'NASHVILLE, TN' citation, and 'the code checks the wire, we check the call' are what a judge would remember after 40 videos. The split screen ('Phone: CONNECTED x4' against '1 of 4 reached a person') is a strong visual.

WHY IT CONCERNS ME AS CIO. Elevator phones are my office's voice turf, and the plan as written puts OIT, Facilities and RUPD at risk.
- Framing: the video opens on 'Rutgers. 2:00 a.m.' and includes a results card that may say Rutgers numbers reached 'a recording or no one'.
- Overnight census: calls to posted 24/7 numbers would follow only an emailed 'heads-up', and some of those numbers may forward to RUPD or RUSSECC.
- Daily probe: a ringing pre-answer probe would create phantom abandoned calls every day.
- LERG data is presented as the current carrier, but it shows only who holds the number block. My telecom staff would catch that immediately.
- Q&A answer 5 takes a swipe at Facilities' 4:30 closing time.
- The premise that Rutgers elevator lines meet Verizon's replacement voice path is unverified, and it may simply be false (OIT runs analog emergency voice over Rutgers-owned copper).

TECHNICAL WEAKNESS. The hero classifier fails on real hardware. On a two-wire tap, a real person answering while the car plays its location message was labelled IVR 20 times out of 20, so the demo works only on synthetic audio or coached teammates. The three staged FAIL cards show the rarest faults in the team's own data: voicemail and old-contractor faults are about 6 of 6,725 Chicago inspections. The common fault, location, is not automated at all. Labelling an IVR front-end a FAIL contradicts ASME interpretation 13-1022.

VERIZON FIT. The value case is carrier-agnostic: the same verdict comes back on an AT&T SIM. Production lives in partner firmware, a CDR check is just a query, the BPC100 is an unsupported configuration for elevators, and the rival-SIM line is awkward in front of Verizon.

OUTLOOK. Very high ceiling if it is rebuilt as a challenge-response cutover-acceptance check co-signed by Facilities, with one real pre-announced HELP press. That is a redesign plus relationship capital, though, not an edit, and only 18 days remain.

**Winner rationale.** Plug-and-PROVE wins narrowly, on reliability, Verizon fit and low risk to Rutgers.\n\nWHERE WHO ANSWERS IS BETTER. It has the better story, and on paper it offers the larger campus benefit.\n\nWHY PLUG-AND-PROVE WINS.\n1. It survives real hardware. Its core claim is that a Contact ID alarm reaches a receiver and is acknowledged through a live Verizon box, and a Rutgers ECE bench can honestly measure that by Nov 8. WHO ANSWERS rests on a passive classifier that the red team showed mislabels a real answerer as IVR 20 times out of 20 once the car's location message is on the line. Its own red team concludes that the first real phone breaks the hero claim.\n2. Content (15 points) and the Verizon judges favour it decisively. It runs on Verizon's own copper-replacement box, VoLTE/IMS and device management. It sits inside the copper exit run by Global Networks & Technology, the organisation that runs this competition. WHO ANSWERS is carrier-agnostic, and its production version lives in partner firmware.\n3. On my criteria as CIO, credibility with OIT and Facilities and the risk of embarrassing Rutgers, WHO ANSWERS is the more dangerous entry. It puts a public frame on Rutgers emergency phones at 2 a.m., makes overnight calls to 24/7 numbers on a mere heads-up, and rings a daily probe that could reach RUPD or RUSSECC. It may also assert a Verizon path that our own lines likely do not use. Plug-and-PROVE's embarrassment risks are the regulatory gotcha, the SIA result that would really measure Asterisk, and the IRB timeline. Those are script and protocol edits, not changes to the design.\n4. Both red teams land both pitches at roughly 78-82 if the fixes land. Plug-and-PROVE gets there through edits and one control arm. WHO ANSWERS needs a new detection mechanism, a new value case and Facilities/RUPD approvals inside 18 days.\n\nSCORE AS WRITTEN: 57.5 against 55. Neither pitch is a finals winner yet. Plug-and-PROVE needs to cut the FCC and capacity framing, keep any SIA result off video, open on the customer, and add some honest campus tie, such as a Who Answers pilot co-signed by Facilities for the final.

**What would change my mind.** WHAT WOULD FLIP ME TO WHO ANSWERS (to about 70+). All of these by the video:\n(a) A confirmed answer from OIT on which path Rutgers elevator lines actually use. If it is Verizon business lines served from Piscataway, the campus–Verizon link becomes real.\n(b) One real HELP press on a Rutgers car, pre-announced and approved by Facilities and RUPD, graded live on camera with a challenge-response read-back of the car ID and the time to a human.\n(c) A detection mechanism that works on real two-wire audio with the location message on: challenge-response on test presses, signaling only on real calls.\n(d) The overnight census, the daily ringing probe, the rival-SIM line and the swipe at Facilities removed.\n(e) A reframe as a Verizon cutover-acceptance step: a caller-ID continuity and registered-address check at the migration order, a feature exclusive to the POTSolve channel, and the Cutover Watch rollup.\nA quote from Facilities or the codes office co-signing it would make it the clear winner on campus benefit.\n\nWHAT WOULD SINK PLUG-AND-PROVE. Any of these:\n- No live Verizon box reaching the receiver by Oct 29 (gate K1).\n- The video keeps the docket, 'paused' and regulator gotcha, or publishes an SIA or failure number on 'Verizon's live network' with no control arms.\n- Older adults are filmed without an IRB determination.\n- The Verizon mentor confirms the Voice Gateway self-install already includes an automated alarm-path check, which would collapse the novelty.\n- Rutgers still appears only as a room by the final.

### rutgers_dean

- **F1_install_hero: 55** (I16 F10 C11 Cr3 P15). DEAN / VICE PROVOST VIEW: this is the better engineering project and the weaker video.

IMPACT 16/30. The criticality is real: an alarm or medical household loses its path to help without knowing it. But the script leads with install capacity (technician-hours), which a non-specialist hears as Verizon's operations problem, not a safety one. The VP red team is right that the capacity premise wobbles:
- the Voice Gateway is already a customer self-install;
- 348 technicians for 6 months is small next to one quarter of fiber installs;
- the '46k installed' figure is a running total of customers, not an install rate.
The alarm-dialer segment is also shrinking as dealers move households to cellular communicators. For Smart Campus judges, Rutgers appears only as a room (the ECE bench) plus an OLLI-RU session that probably will not clear IRB in 9 days.

FEASIBILITY 10/15. The bench is squarely within undergrad ECE reach for about $1k, with 20 tests already passing. The risks are fixable:
- K1: activating a Verizon business line is a real single point of failure;
- the 'SIA 0/20' line measures Asterisk, not the box, because app_alarmreceiver does not decode SIA;
- 'measured on Verizon's live network' is confounded by the third-party SIP DID until the three-arm control (LAN baseline, non-Verizon trunk, Verizon box) is added.

CONTENT 11/15. The test runs through Verizon's actual copper-replacement product and its VoLTE/IMS core, and the production path (MDM firmware plus an IMS test responder) is credible. The ThingSpace puck is padding.

CREATIVITY 3/5. An install-time receipt is good systems thinking, but it is incremental: Inseego could ship it in one firmware release.

PRESENTATION 15/30. The receipt-printer hero with the TRUCK NOT NEEDED stamp is a strong, legible prop. But as scripted:
- the first 24 s are two text cards (a guide quote and the Federal Register);
- a non-specialist then hears 'Contact ID', 'kiss-off' and 'SIA', and gets a capacity caption with four numbers and three docket IDs;
- the hero receipt certifies a life-safety line with no battery;
- the tagline jabs at a deregulation Verizon itself sought.
There is no person in danger on screen until 1:30.

STUDENT LEARNING. Excellent if the controls are added: a controlled measurement on a live carrier network with Wilson CIs is publishable undergraduate engineering. The fixes it needs are editorial, not architectural: open on the alarm moment, cut the capacity bar, dockets and SIA, make ALARM the climax, and switch the hero to the Voice Gateway.
- **F2_elevator_hero: 54** (I18 F6 C6 Cr4 P20). DEAN / VICE PROVOST VIEW: this is the better 2-minute video, built on an engineering claim that fails on the first real phone.

IMPACT 18/30. 'Stuck between floors at 2 a.m.: who answers?' is visceral and applies to every building on every campus. Harshly calibrated, though, the case is weaker than the video implies:
- the team's own Chicago re-derivation shows the faults the hero catches automatically (voicemail, old contractor) are about 6 of 6,725 inspections, roughly 0.1%;
- the most common named fault (wrong location or car ID, plus Nashville) is on the answerer's screen, which the tap cannot see;
- no documented case ties an elevator phone failure to a copper cutover;
- Rutgers' exposure to a Verizon path is unverified: fire communicators and blue lights are already off copper, and elevator lines may sit on OIT analog ports or Kings III cellular.

FEASIBILITY 6/15. Both red teams probed answer.py empirically. On a passive 2-wire tap, with the car's own location message or an operator talking to a silent car, a real person is labelled IVR in 20/20 and 25/25 trials. The '100% person-vs-not' figure is an artifact of synthetic data, a red flag of LLM-assisted overclaiming that a Dean will discount. The schedule stacks further risks:
- a used elevator phone arriving by mail, with loop current marginal on an ATA port;
- the tap must survive 90 Vrms ring voltage;
- Facilities, RUPD and answering-point approvals are unlikely within 18 days;
- 40 calls cannot statistically establish the ≥95% gate.
As Vice Provost I would stop the overnight census calls to posted 24/7 numbers (they may forward to RUPD or RUSSECC) and the daily ring-and-hang-up probe.

CONTENT 6/15. The detected faults belong to the owner, contractor or answering point, so the same check on MarketSpark's AT&T SIM gives the same proof, and 'why is this Verizon's?' has no answer. The BPC100 is not marketed for elevators. The production story is either a CDR query or media inspection Verizon would not run in its core, and the live Verizon intercept beat may not even pass through the ATA.

CREATIVITY 4/5. 'The code checks the wire; we check the call' is the freshest framing in the pool.

PRESENTATION 20/30. It has the best cold open, a one-question premise any non-specialist grasps, a clean split screen ('Phone: CONNECTED x4' vs '1 of 4 reached a person') and a memorable closing couplet. Points are lost for:
- eight beats, five sources and two code clauses before 0:47;
- staged faults weighted toward the rarest classes, which implies a false prevalence;
- implying that Verizon's migration causes failures, when none of the staged faults involve the network;
- a rival-SIM line on camera in front of Verizon judges;
- a Rutgers results card that may hold only a walk-audit inventory.

STUDENT LEARNING. Strong campus fieldwork and a good Facilities partnership. But the fix (challenge-response test calls, media analysis only on the 4-wire/IP side, a CDR layer inside Verizon) is a redesign, and it pulls the product toward EN 81-28 test calls and the Kone patent space.

**Winner rationale.** This is a narrow win, inside the noise on Round 1 alone. WHO ANSWERS is the more watchable 2-minute video, and I scored it 5 points higher on Presentation. I still pick Plug-and-PROVE for four reasons.

(1) Engineering rigor. As Dean I cannot reward a hero whose central claim (passive person-vs-voicemail detection on a 2-wire tap) was shown twice, empirically, to fail on realistic audio. Its '100%' comes from synthetic data designed alongside the classifier. Plug-and-PROVE's flaws are measurement-design confounds (the SIP DID leg, the SIA/Asterisk tautology). A three-arm control and dropping SIA from the video fix them in days.

(2) Feasibility for undergrads. Plug-and-PROVE needs a box, a used panel and Asterisk. WHO ANSWERS needs all of Plug-and-PROVE's Verizon-activation risk plus a mailed elevator phone, a tap that survives ring voltage, a loop-current check, and Facilities, RUPD and answering-point approvals in 18 days.

(3) Content and Rounds 2-3. Plug-and-PROVE runs through Verizon's own copper-replacement product and its VoLTE/IMS path, so it survives the Verizon VP's 'why is this ours?'. WHO ANSWERS' faults are carrier-agnostic, and both red teams flagged its Verizon value logic as broken. Plug-and-PROVE's 'break it' poster table, where judges press PROVE and take a receipt home, is the most robust live demo for Feb 3 and Mar 4.

(4) Student learning. A controlled, CI-reported measurement of alarm delivery over a live carrier network is real, publishable undergraduate engineering. The best version of WHO ANSWERS needs an architectural redesign, while Plug-and-PROVE's remaining fixes are editorial:
- cold-open on a keypad that says SENT, then 'did anyone get it?';
- make ALARM the climax;
- cut the capacity bar, the dockets, the Federal Register card and the regulator jab;
- speak only the verified '417k lines vs 46k installed';
- show an all-green receipt;
- reframe the value as self-install fallout.

Condition of the win: Plug-and-PROVE should borrow WHO ANSWERS' storytelling craft for Round 1. It should keep the elevator WHO ANSWERS pilot, rebuilt as a challenge-response test call, as the campus face of the 10-minute final.

**What would change my mind.** I would flip to WHO ANSWERS if by about Nov 3 it does all four of these:
- (a) replaces passive classification with a challenge-response test call ('press 1 and read back the car ID') and publishes a real-line confusion matrix with CIs from 200+ automated bench presses, with the car's location message ON;
- (b) films one Facilities-approved, pre-announced real Rutgers HELP press graded live;
- (c) gets OIT to confirm that at least some Rutgers elevator lines ride Verizon B1 or a Verizon replacement path;
- (d) re-anchors Verizon value on a check only Verizon can run: caller-ID/ANI continuity and the registered-address match at the migration order, as a POTSolve-exclusive feature.
That would lift its Feasibility to about 10 and Content to about 10 while keeping its Presentation lead, for roughly 62+.

Plug-and-PROVE would also lose the top spot, without any change to WHO ANSWERS, if any of these happens:
- K1 fails (no BPC100 or Voice Gateway live on Verizon by Oct 29), leaving no measured Verizon result;
- the Verizon mentor confirms that install visits are not a constraint and that an automated alarm check already exists at install;
- the team ships the video as currently scripted: Federal Register opening, the 1M-lines/7x capacity bar, 'SIA 0/20' on the live network, and the 'when the regulator stops checking' tagline. That would drop its Presentation to about 12 and its total below WHO ANSWERS.

### verizon_business

- **F2_elevator_hero: 59** (I20 F7 C7 Cr4 P21). Speaking as the owner of the POTSolve and MarketSpark life-safety tier: this is the only finalist aimed at my E&PS buyers (universities, hospitals, housing authorities), and the only one with something customers already pay for. Elevator owners pay today for RATH SmartView at $9.99 per device per month and for Wurtec Watch. A migration commissioning receipt saying 'HELP reaches a person, sees the right car, inside 45 s', plus an inspector-ready log, would help win a university RFP. IMPACT 20: it is the most critical problem in the pool and every judge has ridden an elevator. Harsh deductions: its own Chicago data shows the staged faults are the rarest (voicemail plus old contractor is about 6 of 6,725 inspections). Location and ID faults are the real ones, and the passive tap cannot see them. Whether Rutgers elevator lines ride Verizon at all is unverified. FEASIBILITY 7: the red team ran answer.py on two-wire mixed audio, and a real person speaking over the car's location message came back as IVR 20 of 20 times, so the hero as written breaks on the first real phone. Other weak points: a used elevator phone arriving by mail, the 20 mA loop current, Facilities and RUPD approval inside 9 days, an invalid overnight census, and a daily probe that would ring a PSAP. A challenge-response test (key 1 plus the car ID) rescues it cheaply. CONTENT 7: as a product leader I wince at an elevator phone on a BPC100, which is an unsupported configuration (3 AA cells against A17.1's 4 h). POTSolve voice may never touch IMS. The CDR checks are a query, and the new logic lives in a student box. PARTNERS: saying on camera that 'some gateways carry a rival's SIM' calls out MarketSpark in public. Cut it. The fix is a POTSolve-exclusive feature inside Verizon's own 26-228 business-line migrations. PRESENTATION 21: it has the best hook among 40+ videos ('stuck at 2 a.m., press HELP, who answers?'), a clean split screen of 'CONNECTED x4' against '1 of 4 reached a person', and a memorable close ('the code checks the wire, we check the call'). The middle is too dense (five sources before 0:47), and the staged failures on a 'live Verizon line' imply that Verizon's migration causes them. ROUNDS 2-3: the HELP-button poster table is the most engaging in the pool. In Q&A it will hear 'why is this ours?', and it survives only if it has been re-anchored as a Verizon cutover-acceptance check with a registered-address comparison only Verizon can make.
- **F1_install_hero: 56** (I17 F9 C11 Cr3 P16). This is the more honest Verizon-network idea, but it is pitched on the wrong value, to the wrong segment, with sponsor-hostile framing. IMPACT 17: alarm compatibility at swap is a real migration pain, and an independent alarm-format matrix measured on our box is something I would genuinely want. But the hero lever, install capacity, is wrong. Voice Gateway is already a customer self-install, and about 348 technicians for 6 months is noise next to one quarter of Fios net adds. It also compares a running total (46k) with a rate. It is mostly a Consumer and SMB story (Voice Connect homes, OLLI older adults), not my E&PS life-safety tier, and Rutgers is only a bench, which leaves campus ubiquity near zero for the Dean, CIO and Vice Provost. No customer buys it; it is an internal firmware feature Inseego could ship in one release. FEASIBILITY 9: the bench is buildable. Weak points: BPC100 business activation is a single point of failure. The measurement is confounded by the SIP DID and codec, and Asterisk cannot decode SIA, so 'SIA 0/20' measures their own receiver. The OLLI IRB in 9 days is fantasy. In production, 'one button' cannot make a customer's panel dial. CONTENT 11: the best in the pool. It rides production VoLTE and IMS on Verizon's own copper-replacement product and ships as MDM firmware with a Verizon-hosted IMS test responder. The ThingSpace puck is padding. CREATIVITY 3: a TRUCK / FIX BY TEXT verdict receipt is smart operations work, not new. PRESENTATION 16: the printed receipt is a great prop. But the first 24 s are a user-guide disclaimer card and a Federal Register card. The capacity beat crams four numbers and docket IDs into one caption, and the narration mislabels 26-227 as 'home-phone'. It shows 'BATTERY: NONE' next to 'TRUCK NOT NEEDED' and has an alarm keypad 'plugged in'. The tagline 'when the regulator stops checking' jabs at a deregulation Verizon supported. My regulatory team would ask for it to be pulled from public view because objectors could cite it in the pending docket. ROUNDS 2-3: the 'break it' poster is robust and judges take receipts home. Re-pitched as lowering self-install fallout (first-time-right, repeat dispatch within 30 days, care contacts, alarm households confirmed) with a 30-day trial on one batch's self-install kits, it is something I could say yes to.

**Winner rationale.** Round 1 is a 2-minute video, and Impact plus Presentation carry 60 of the 95 points. WHO ANSWERS wins both by enough to outweigh Plug-and-PROVE's real advantages in Content (+4) and Feasibility (+2). It opens on a hook every Verizon and Rutgers judge understands in 7 seconds (trapped at 2 a.m., press HELP, who answers?). It has a visual contrast nobody else will show ('Phone: CONNECTED' four times against one call reaching a person) and campus footage that gives the Rutgers judges a reason to care. Plug-and-PROVE opens on a user-guide disclaimer and a Federal Register card, which lose a tired panel in the first 24 seconds and read to Verizon judges as a regulatory gotcha. From my seat running POTS replacement and life-safety, WHO ANSWERS is also the one aimed at my E&PS customers, through the exclusive CSG POTSolve channel. Owners demonstrably pay for elevator assurance (RATH, Wurtec), and a commissioning receipt at migration is a win theme in university and hospital RFPs, which helps retention in a segment down 4.8%. Plug-and-PROVE is an internal firmware feature for Consumer and SMB boxes that no customer buys and Inseego could ship without students. The win is narrow (59 vs 56) and conditional on fixes that must land before Nov 8. (1) Replace the passive voicemail classifier with a challenge-response test (key 1 plus the car ID, timed against the 45 s benchmark), because the red team showed the current classifier fails on real two-wire audio. (2) Make location and caller-ID change at cutover the hero fault, since the data supports it, and caption the bench 'faults staged; none caused by the network'. (3) Cut the rival-SIM line, the overnight census and the daily PSAP probe. (4) Reposition production as a POTSolve-exclusive feature and a test step inside Verizon's own business-line migrations, comparing the registered dispatchable address Verizon holds. Plug-and-PROVE's Verizon-native backbone (an IMS-hosted test responder, MDM firmware) should be grafted in as the network layer. With those changes it reaches the high 70s; without them it collapses in finals Q&A on 'why is this ours?'.

**What would change my mind.** Any one of these flips the win to Plug-and-PROVE. (a) By Oct 24, OIT says Rutgers elevator phones are on OIT analog/Teams ports or vendor cellular, not Verizon, and Facilities will not allow filming in a car or a pre-announced HELP press. WHO ANSWERS then loses both its campus face and its Verizon tie and becomes a PBX audit. (b) The used elevator phone has not arrived by Oct 26, or Gate A fails on real hardware even with challenge-response, which would force a signaling-only hero (digits, SIT, answer time) that a Verizon judge will call a CDR query. (c) A Verizon mentor confirms that self-install alarm fallout (repeat dispatch, care contacts, alarm failures after the swap) is a top-3 cost driver on Voice Connect/Voice Gateway, and offers a 30-day trial on one migration batch. That would lift F1 Impact to about 22 and Content to about 12. (d) F1 re-cuts the video as recommended: a cold open on a keypad showing 'sent... did anyone get it?', the hero by 0:15, no dockets and no 'regulator stopped checking', only the verified 417k-vs-46k line, and a three-arm controlled bench line with a pass result. That would add about 5 points to Presentation and overtake an un-fixed WHO ANSWERS. Conversely, if WHO ANSWERS films one real, Facilities-approved Rutgers HELP press graded live with the answerer reading back the car ID, its lead widens to about 8 points.


---

## Finalist dossiers and red-team attacks

## F1_install_hero: Plug-and-PROVE: the copper-replacement box proves itself at install, and the truck goes only where the receipt says (F1, install-capacity hero)

**One-liner:** Verizon's own guide for its copper-replacement box says alarm compatibility "is determined by your testing ... at time of install". Since Oct 15, 2026 the FCC no longer asks carriers to show that a replacement works with key applications such as alarms; it only "encourage[s] carriers ... to prevent alarm signaling failures". Plug-and-PROVE puts that test behind one button on Verizon's Voice Connect / Business Phone Connect box (Inseego BPC100). Through Verizon's live VoLTE network it checks four things:
- SIGNAL at this spot;
- VOICE both ways;
- ALARM reached the receiver and was acknowledged (kiss-off);
- BATTERY present.
It then prints TRUCK NOT NEEDED, FIX BY TEXT or TRUCK NEEDED. The pitch is install capacity: Verizon's 2026 exit filings cover about 1M legacy lines (417k verified from the filings plus about 750k from a vendor summary of a third), against about 46k fixed-wireless replacement customers installed nationwide. Pillar 1 (automation).

### Problem
Status labels: [V] verified from a primary source, [S] secondary, [U] unverified.

1) The exit is large and dated, and installs have not kept up.
- [V] Verizon "currently has approximately 46,000 customers using fixed wireless POTS voice replacement services nationwide". Source: July 7, 2026 application (WC 26-170, FL PSC copy) https://www.psc.state.fl.us/library/filings/2026/04315-2026/04315-2026.pdf, repeated in the Aug 10, 2026 application (WC 26-227, RI PUC copy) https://ripuc.ri.gov/sites/g/files/xkgbur841/files/2026-09/26-29-TL%20POTS%20Verizon%20Discontinuance%20Application%20FINAL%20(as%20filed).pdf
- [V] Line counts in the filings:
  - WC 26-170: about 140,000 legacy voice lines in 8 Frontier states, authority on or after Nov 16, 2026 (DA 26-763).
  - WC 26-227: about 277,000 lines in 9 states including NJ, authorized date on or after Oct 23, 2026, removed from automatic grant Sept 25. DA 26-1038: "requires additional time ... not a final determination on the merits". https://docs.fcc.gov/public/attachments/DA-26-1038A1.pdf
- [S] WC 26-252 (CA, CT, DC, IL, MD, MA, MI, NY, PA, WV): about 750,000 locations, on or after Nov 30, 2026, per a vendor summary. https://dataremote.com/newsroom/news/verizon-section-214-application-discontinue-copper-pots-nine-states-dc
- Totals: 417k lines verified, which is 9x the installed base; about 1.17M including the secondary figure, which is 25x.
- WC 26-228 (B1, ISDN BRI, PBX trunk, FX, payphone and key system; NJ listed with no "portions of"): no removal notice in the docket as of Oct 21, authority on or after Oct 23, 2026. https://docs.fcc.gov/public/attachments/DA-26-891A1.pdf
- Fixed wording: "the FCC paused the home-phone exit; the business-line exit drew no pause". Never say "approved". Authority is not a cutoff, because Verizon sends per-customer disconnection letters.

2) The rules stopped checking on Oct 15, 2026.
- [V] FCC 26-19 amendments are effective Oct 15, 2026 (91 FR 62334). https://www.govinfo.gov/content/pkg/FR-2026-10-01/pdf/2026-20192.pdf
- §63.602 is removed. It had included "interoperability with key applications and functionalities".
- The old 63.71(a)(6) safe-use and line-power notice items are gone.
- ¶31 declines AICC's G.711 / RFC 2833 alarm condition: "we encourage carriers to ensure their IP networks are appropriately configured so as to prevent alarm signaling failures". The compatibility requirement "sunset in 2025". AICC's "five million installed [alarm] panels" is quoted in footnote 110. https://docs.fcc.gov/public/attachments/FCC-26-19A1.pdf

3) Verizon's own process leaves the alarm path to the customer. These are Verizon's words: a process gap, not a broken product.
- [V] Voice Connect 2nd gen is the BPC100 (Terms of Service battery table).
- [V] It is "a professionally installed device". https://www.verizon.com/support/residential/homephone/voice-connect
- [V] The technician install confirms only that the "jacks ... are functional". Verizon "will initially verify that adequate coverage is available". Customers "should test any home alarm". https://www.verizon.com/content/dam/verizon/support/consumer/documents/phone/voice-connect-terms-of-service.pdf
- [V] The guide has the customer dial ##21*MDN#, then power-cycle. "If the alarm company responds with a phone call, then your connection is complete. Failure to verify may result in your alarm not working." "Compatibility is determined by your testing of your alarm and/or medical device at time of install." https://www.verizon.com/content/dam/verizon/support/consumer/documents/phone/voice-connect-user-guide-2nd-gen.pdf
- [V] The mailed swap guide's only check is "make a test call". It mentions alarm, medical and ##21 zero times. https://www.verizon.com/content/dam/verizon/support/consumer/documents/phone/voice-connect-upgrade-instructions.pdf
- [V] The Voice Gateway is customer-set-up and "does not monitor the alarm". https://www.verizon.com/support/verizon-voice-gateway/
- [V] "Supports ... Contact-ID. Alarm calls using other central station server protocols are not supported." https://static.inseego.com/us/download/bpc100-user-guide-verizon.pdf
- [V] Backup is 3 AA batteries: 3 h talk, 23 h standby.
- [V] Verizon spokeswoman: "We will have teams that come out and test everything before that copper is disconnected." https://northforksun.com/verizon-plans-to-phase-out-copper-landlines-for-some-north-fork-customers/

4) Why the check must be in-band and at the spot.
- [V] Napco: a receiver can kiss off a corrupt signal. https://tech.napcosecurity.com/faq/details/id/1770
- [V] MarketSpark: devices with full bars still failed because of poor RSRQ. https://www.marketspark.com/understanding-cellular-signal-quality/
- [V] AICC: a communicator swap is a truck roll of up to 3 h, and about 25% of appointments get no access. https://tma.us/wp-content/uploads/2021/05/AICC-Petition-for-Emergency-Relief-5-10-21-FINAL.pdf

UNVERIFIED:
- Verizon's 2026 mix of technician and self installs, and its install checklist.
- Whether MDM reads battery and AC state.
- Whether the business BPC100 firmware has ##21 (the business guide has no ##21 step).
- The 26-228 counts and NJ footprint.
- Truck-roll cost (we use no dollars).
- The 750k figure (secondary).
- OLLI-RU recruitment (its site was unreachable this pass).
- The Kings III mic/speaker quote (site returned 403).
- Ooma's "50%" is a vendor claim.

### Solution
ONE button and ONE receipt on Verizon's own box. The video receipt reads:

  SIGNAL here: GOOD / MOVE 1 m TOWARD WINDOW / NEEDS ANTENNA
  VOICE: CLEAR BOTH WAYS (tones plus 16 DTMF digits intact)
  ALARM: REACHED RECEIVER, ACKNOWLEDGED in [BENCH] s (plus "alarm number registered", only where the firmware has ##21)
  BATTERY: NONE INSTALLED -> 3 AA mailed today
  Verdict: TRUCK NOT NEEDED / FIX BY TEXT / TRUCK NEEDED

Verdict rules:
- TRUCK NOT NEEDED: every line passes, or the only fix is mailed.
- FIX BY TEXT: the customer can fix it and re-run. Examples: move the box toward a window, re-enter the alarm number, insert batteries, move the phone out of the yellow alarm port (Verizon warns this "could stop the device from working").
- TRUCK NEEDED: someone must visit, and the receipt says who. A Verizon technician for no usable signal or an external antenna; the alarm company for an unsupported panel format (SIA, 4/2) or a cellular communicator.

How each check works, bench (what we build) vs production (what Verizon would ship):
- SIGNAL. Bench: RSRP/RSRQ/SINR read beside the box with a field-test app (a labelled proxy) plus the bars on the box's web interface. Production: the box modem through MDM, with thresholds from bench T5, not bars.
- VOICE. Bench: a Pi with an FXO interface on the box's phone port dials our tone/DTMF responder through Verizon VoLTE. Production: a Verizon-hosted IMS test number.
- ALARM. Bench: a real used Contact ID panel dials OUR OWN Asterisk AlarmReceiver; the line tap detects the handshake (1400 then 2300 Hz), a checksum-valid frame and the 1400 Hz kiss-off, and the receiver log confirms decoding. Production: the customer puts the account on test, as today; the box listens passively, reads the alarm-number table where the firmware has one, and flags unregistered numbers or unsupported formats.
- ALARM is install-only, because central stations already supervise the panels' periodic test signals.
- BATTERY. A 10 s AC-pull while dial tone is watched. The bench measures real runtime, which sets the "about X h standby" text.

Never: we never dial 911, a real central station, RUPD dispatch or a medical-alert center without written permission. We use no CPNI and no GPS.

Out of the video:
- Medical, fax, TTY and ##21 jargon go to the poster.
- Medical shows "not tested without a test window"; it never shows "ok".

Already built in /home/user/verizonsmartcampus/prototype/prove:
- install.py: receipt and verdict engine, six simulated scenarios.
- alarm.py: Contact ID encode/decode, handshake and kiss-off detectors.
- capacity.py.
- answer.py.
- Console receipt panel.
- 20 tests pass (run 2026-10-21).

To build: a measure mode that feeds real bench readings into install_proof, a thermal printer, and analyze_prove_lab.py.

Poster and 10-minute final only:
- nightly SIGNAL/VOICE/BATTERY checks with a mains sentinel;
- elevator WHO ANSWERS with network-side checks and no relay on the line (dialed number vs registry, SIP outcome, SIT/voicemail from spectral features, 45 s answer, monthly location confirmation), as a Facilities/RUPD-co-signed pilot;
- Cutover Watch, a per-wire-center rollup on the 1,763-CLLI map with no Rutgers pins;
- SILENT AFTER CUTOVER, a Verizon-internal before/after heartbeat engine under 222(c)(1) with counsel review, calibrated on Lab signatures.

Full dossier: /tmp/claude-0/-home-user-verizonsmartcampus/ac4afb2e-cdc2-53a2-a8f3-1a6a3e0d44b6/scratchpad/gen4/dossier_F1_install_hero.md

### Verizon technology
- The box: Verizon Business Phone Connect / Voice Connect 2nd gen, the Inseego BPC100 [V].
  - $129.99 retail.
  - Cat 4 LTE, HD VoLTE.
  - RJ11 phone port and RJ31 alarm port.
  - 3 AA backup.
  - "Verizon MDM for remote management".
  - https://www.verizon.com/business/shop/products/devices/connected-devices/inseego-business-phone-connect/
- The same test plan applies to the Verizon Voice Gateway (VG10A), which Verizon's 2026 filing names as a fixed-wireless replacement. PROVE is device-agnostic.
- Voice path: Verizon's production VoLTE/IMS core. Every receipt line except BATTERY travels the path a real alarm or 911 call would take.
- ThingSpace self-serve [V]:
  - The PROVE puck reports on its own LTE-M line ($1.50/device/month, data and SMS only), independent of the line under test.
  - The Connectivity Management API (connection history, reachability, callbacks) feeds the console.
  - Device Diagnostics RF data needs LwM2M-certified modules and a Bundled Services Subscription. So the bench reads RF beside the box, and production reads it from the box's modem through MDM.
  - https://thingspace.verizon.com/start/
- Production path: the test plan becomes BPC100 / Voice Gateway firmware pushed through Verizon MDM, plus a Verizon-hosted IMS test-responder number. Results go into the install or order record, and only TRUCK NEEDED creates a dispatch. A per-wire-center rollup (Cutover Watch) is for the final.
- Owners inside Verizon:
  - GN&T Transformation Office, which runs the copper/TDM exit and sits under the same SVP as the competition's Technology Ambassador Office;
  - Verizon Business POTS Replacement;
  - Consumer Voice Connect operations;
  - Inseego (firmware).
- Not claimed: slicing, RedCap or edge. This is the VoLTE/IMS, MDM and ThingSpace stack the copper exit actually runs on.

### Verizon value
Which line it touches:
- Cost of services ($27.8B FY2025): field technician and contractor install visits.
- Verizon's 2026 cost program names "decommission of legacy elements in the network, including copper" (Skiadas, Jan 30, 2026) and "reduced third-party contractor and outsource spend" (Q1 2026) [V].
  - https://www.verizon.com/about/sites/default/files/2026-02/vz_4q25_transcript_013026r.pdf
  - https://www.verizon.com/about/sites/default/files/2026-06/vz_1q26_transcript_042726rm.pdf
- Speed of the exit: copper retirement saved "about $180 million" a year from 36 COs, "in part driven by a reduction in technician dispatches" (Investor Day 2022) [V]. That is Verizon's saving and NOT claimed by us. Never cite "60% fewer dispatches", a 2015 repair figure.

NO DOLLAR FIGURE. The CFO formula is technician-hours avoided × Verizon's own loaded hourly cost.

Capacity math:
- Verified anchors: B = 46,000 installed; L = 417k lines from the filings, or about 1.17M including the secondary 750k.
- Labelled assumptions:
  - A1: f = share of filed lines going to a Verizon fixed-wireless box = 0.30 (range 0.15-0.50).
  - A2: h = 2.0 technician-hours per install including travel.
  - A3: m = 120 productive hours per technician-month.
  - A4: p = share PROVE clears first time = 0.60.
  - A5: x = share that pass after a texted fix = 0.15.
  - A6: W = 6 months after authority. Authority is not a deadline.
- Formulas:
  - installs I = L·f
  - technician-hours today = I·h
  - truck share t = 1−p−x
  - throughput multiplier = 1/t
- Technicians that would have to be dedicated full-time to finish in 6 months:

| Lines filed | f | Installs (× installed base) | Today | With PROVE, 75% no-truck |
|---|---|---|---|---|
| 417k verified | 0.30 | 125,100 (2.7×) | 348 | 87 |
| ≈1.17M | 0.30 | 350,100 (7.6×) | 972 | 243 |
| ≈1.17M | 0.15 | 175,050 (3.8×) | 486 | 122 |
| ≈1.17M | 0.50 | 583,500 (12.7×) | 1,621 | 405 |

- Per 100k filed lines at f = 0.30: 500 technician-months today, 125 with PROVE.
- The multiplier (4× at 75% no-truck) depends only on the pass share. The Rutgers bench and the OLLI-RU study measure that share, which turns A4 and A5 into data.
- Script: scratchpad/gen4/f1_calc/cap.py.
- Honest limits:
  - If most homes go to fiber or mobile (small f), the capacity problem shrinks.
  - If the technician visit exists for the 911 address and liability, PROVE triages visits rather than eliminating them (gate K4).
- Secondary, unquantified value:
  - Retention of alarm and medical households, which were 17% and 24% of landline keepers in a 2014 survey cited in FCC 14-185 (dated).
  - A per-home receipt as evidence for the alarm, power and coverage objections in the paused docket. We do not claim it unblocks anything.
- Repo correction: capacity.py still calls 277k "unverified"; the RI PUC copy of the application verifies it.

### Rutgers primary data
BY NOV 8 (video):

(1) Rutgers PROVE Lab (ECE bench) on Verizon's live network.
- Equipment: one BPC100 on a Verizon business voice line (department or faculty-sponsor account), our own Asterisk AlarmReceiver, and a used Contact ID panel. Protocol: /home/user/verizonsmartcampus/deliverables/PROVE_LAB_BENCH_PROTOCOL.md.
- Minimum runs:
  - T1: Contact ID baseline, 50 events. Delivered n/50, first-try rate, median kiss-off time.
  - T4: SIA and 4/2, 20 events each. Measures the "Contact ID only" footnote.
  - T5: three placements (window, interior, basement-like), 20 events plus 5 calls each, with RSRP/RSRQ/SINR.
  - T6: overnight battery runtime with alkaline AAs; a 5 °C run if time allows.
  - T2/T3 (##21 registered vs not; the mailed-swap test) only if the business firmware has ##21 (gate K2).
- Output: field_data/prove_lab.csv with Wilson 95% CIs.
- The video carries ONE line from it. First choice is the ALARM format line ("Contact ID [x]/50, SIA [y]/20"), a measured confirmation of Verizon's own footnote and so not a gotcha. Backup is BATTERY measured runtime against the rated 23 h.

(2) OLLI-RU older-adult self-install pilot.
- Who: n = 8-12 consenting adults through Rutgers' Osher Lifelong Learning Institute. Recruitment and IRB exempt determination are UNVERIFIED and gated by Oct 30. Fallback: retirees and staff living in retiring NJ wire centers; student testers are never presented as older adults.
- Task: in a mock living room, each participant sets up the BPC100 alone from Verizon's paper guide, then presses PROVE.
- Measures:
  - finished alone and minutes taken;
  - errors (phone in the yellow alarm port, no batteries, antennas off, box in the weak spot);
  - receipt verdict;
  - whether the texted fix worked.
- Output: the measured p and x for the capacity model.
- Limitation, stated: IVR activation is pre-done.

BY FEB 3 (poster):
- Full PROVE Lab matrix:
  - 8-12 used panels (Vista, DSC, Napco, Silent Knight 5104 DACT) × Contact ID / SIA / 4-2;
  - × paths: BPC100 with and without registration, Voice Gateway if obtainable, copper simulator;
  - 50-100 trials each;
  - fax T.30 at 9600 bps, TTY Baudot, and PERS only with the vendor's written test window.
  - Delivered to Verizon first, labelled "tested information, not a warranty". It resolves where Verizon's and Inseego's documents disagree on medical alerts and fax.
- OLLI-RU A/B study, n = 20-30: Verizon guide alone vs guide plus PROVE.
- Consented survey of Rutgers staff in the 62 retiring NJ wire centers: devices on the home line, cordless-only handsets, batteries installed.
- For the final (WHO ANSWERS):
  - a pre-announced elevator HELP audit with Facilities and RUPD on 10-20 cars;
  - a no-permission walk audit of 100+ cars;
  - a sticker census of posted 24/7 numbers;
  - the existing Chicago open-data reclassification: 1,613 of 6,725 maintain/repair inspections cite the emergency phone, including the Oct 9, 2026 "NASHVILLE, TN" citation.

### Demo
VIDEO BEATS (2:00):
1. 0:00-0:12. A lifts a BPC100 from its box. Quote card: "Compatibility is determined by your testing ... at time of install."
2. 0:12-0:24. Federal Register card: §63.602 removed Oct 15, 2026, plus the FCC ¶31 "encourage carriers ... prevent alarm signaling failures" quote.
3. 0:24-0:52. The hero. Hands plug in a corded phone and an alarm keypad and press a big PROVE button. A thermal printer prints SIGNAL here: GOOD / VOICE: CLEAR BOTH WAYS / ALARM: REACHED RECEIVER, ACKNOWLEDGED / BATTERY: NONE, 3 AA MAILED. Stamp: TRUCK NOT NEEDED.
4. 0:52-1:08. The one measured line. Rutgers PROVE Lab footage: the Asterisk receiver log, a live counter, the panel flipped to SIA. Caption: date and n.
5. 1:08-1:30. Capacity. A bar of ≈1M filed lines against a bar of 46k installed. Caption gives the sources and the 26-227 paused / 26-228 no-pause wording, plus "assumption: 30% choose fixed wireless". Then "trucks only for red receipts".
6. 1:30-1:45. An OLLI-RU participant (consented, release signed) sets up alone and holds up her receipt. Caption: n.
7. 1:45-2:00. Production diagram: firmware → Verizon MDM → order record, with ThingSpace. Tagline. A receipt torn off and handed to the camera.
Never shown: Dec 10, "FCC approved", MEDICAL ok, Rutgers pins on any map, or a Verizon logo.

POSTER TABLE (Feb 3), "Break it":
- The rig: a real BPC100 on a Verizon line, a corded phone, a used alarm keypad, the PROVE puck and a receipt printer.
- Judges press PROVE and take their receipt home.
- A "break it" card lists faults; the receipt names each one and its fix:
  - pull the AAs → BATTERY, FIX BY TEXT;
  - plug the phone into the yellow alarm port → FIX BY TEXT, quoting Verizon's own warning;
  - put the box inside a cinder block and steel "basement" enclosure → SIGNAL: MOVE / NEEDS ANTENNA;
  - flip the panel to SIA → ALARM: TRUCK NEEDED, alarm company;
  - where the firmware allows, clear the alarm number → "number not registered".
- Side screen:
  - the Lab matrix;
  - the capacity model with sliders for A1-A5;
  - the poster-only panels: nightly checks, WHO ANSWERS, the Cutover Watch map of 1,763 wire-center CLLIs, and SILENT AFTER CUTOVER.

### 120-second script
PLUG-AND-PROVE, 120 s, about 275 words. A = engineering student, B = business student. [Brackets] are filled only from our bench CSV and study log; two variants are pre-written.

[0:00-0:12] VISUAL: A lifts a Verizon BPC100 out of its box at the Rutgers PROVE Lab. Caption: "Verizon Voice Connect 2nd gen = Inseego BPC100", plus the guide quote.
A: "When Verizon retires a copper phone line, this box takes its place. Verizon's own guide says alarm compatibility 'is determined by your testing at time of install.'"

[0:12-0:24] VISUAL: Federal Register page. Caption: "FCC 26-19, effective Oct 15 2026: §63.602 adequate-replacement test removed. ¶31: 'we encourage carriers ... to prevent alarm signaling failures.'"
B: "And since October fifteenth, the FCC no longer asks carriers to show a replacement works with alarms. It simply encouraged carriers to prevent alarm failures. We built the way to show they did."

[0:24-0:52] VISUAL: Hands plug in a corded phone and an alarm keypad and press PROVE. The printer prints SIGNAL here GOOD / VOICE CLEAR BOTH WAYS / ALARM REACHED RECEIVER, ACKNOWLEDGED / BATTERY NONE, 3 AA MAILED. Stamp: TRUCK NOT NEEDED.
A: "Plug-and-PROVE. Plug in the phone and the alarm panel. Press one button. Through Verizon's live network, PROVE checks the signal at this exact spot, voice in both directions, that the alarm reached the monitoring receiver and got its acknowledgment tone back, and that the backup batteries are in. Then it decides: truck not needed, fix by text, or truck needed."

[0:52-1:08] VISUAL: Lab receiver log scrolling, a live counter, the panel flipped to SIA. Caption: "Measured on Verizon's live network, [date], n=[__]".
B (failure variant): "We measured this at our Rutgers PROVE Lab in ECE. A Contact ID panel got its acknowledgment [__ of 50] times. An SIA panel, a format Verizon's guide says this box doesn't support, [__ of 20]. Verizon's guide is right. PROVE prints it before anyone relies on it."
B (pass variant): "...A Contact ID panel got its acknowledgment [__ of 50] times, in about [__] seconds. That proof shouldn't stop at our bench. It should print in every home."

[1:08-1:30] VISUAL: A bar of ≈1M legacy lines next to a bar of 46k installed. Caption: "140k (WC 26-170) + 277k (WC 26-227) from Verizon filings; ~750k (WC 26-252) per vendor summary. 46k: Verizon filings, Jul/Aug 2026. 26-227 not auto-granted (DA 26-1038); 26-228: no pause notice as of Oct 21, authority on/after Oct 23. Assumption: 30% choose fixed wireless."
A: "Why Verizon cares: its 2026 exit filings cover about a million legacy lines. Today it has about forty-six thousand fixed-wireless replacement customers. The FCC paused the home-phone exit. The business-line exit drew no pause. If even a third choose a box like this, that's about seven times everything installed so far. Every visit costs technician hours. A green receipt doesn't need a truck."

[1:30-1:45] VISUAL: An OLLI-RU participant (consented, release signed) sets the box up alone and holds up her receipt. Caption: "OLLI-RU self-install pilot, n=[__]".
B: "With OLLI-RU, Rutgers' lifelong-learning program, older adults set the box up alone. [__ of __] finished with no truck."
(If the IRB gate fails, use instead: "Next, older adults from OLLI-RU try it alone. That number replaces our biggest assumption.")

[1:45-2:00] VISUAL: Diagram: box firmware → Verizon MDM → order record, with ThingSpace LTE-M. A receipt torn off and handed to the camera. End card: "Plug-and-PROVE · Rutgers PROVE Lab · student concept, not a Verizon product".
A: "In production, it would ship as firmware Verizon pushes through device management, reporting over ThingSpace."
BOTH: "When the regulator stops checking, the carrier that proves wins. Plug-and-PROVE."

### 18-day plan
Roles: HW (bench), SW (code and receipt), RES (IRB, study, sources), VID (film and edit). Budget about $900-1,300.

- Oct 21 (Wed). Lock scope. RES: ask the ECE faculty sponsor to host the Rutgers PROVE Lab and sign for a Verizon business voice line. Draft the IRB exempt application and recruitment script.
- Oct 22 (Thu). HW: rush order:
  - 2× BPC100;
  - a used Contact ID panel and keypad, plus a panel settable to SIA/4-2;
  - HT813 or USB FXO, Pi 5, thermal printer, AC-pull relay;
  - LTE-M kit plus a ThingSpace $1.50 line;
  - AAs and a mini-fridge.
  SW: Asterisk AlarmReceiver on a SIP DID, plus a tone/DTMF responder. RES: submit IRB; the sponsor approaches OLLI-RU.
- Oct 23 (Fri). SW: measure-mode adapters (receiver-log parser, Goertzel kiss-off detector on the line tap, tone-test runner, AC-pull relay). Wire prototype/prove/install.py to real readings and the printer. Check the 26-228 docket on its authority date.
- Oct 24-25. HW: activate the box and run T1 (50 Contact ID events).
- Oct 26. Read Verizon's Q3 call for copper, POTS and install remarks. Run T4 (SIA and 4/2, 20 events each). Dial ##21 and listen for the confirmation tone.
- Oct 27. T5 placement at 3 spots. T6 battery run overnight. GATE K1: is the box live on Verizon?
- Oct 28. If ##21 exists, run T2/T3 swap with box B. T6 at 5 °C. GATE K2.
- Oct 29. Verizon mentor call: technician vs self-install mix, install checklist, MDM battery read, f/h/crew, any automated alarm check. GATE K4 part 1.
- Oct 30. analyze_prove_lab.py with Wilson CIs. Storyboard lock. Build the mock living room and "basement" enclosure. GATE K3: IRB and OLLI permission.
- Oct 31. Two internal dry runs of the study protocol (not data). Console capacity sliders.
- Nov 1-3. OLLI-RU sessions, n target 12. Fold the measured p and x into capacity.py. GATE K5 on Nov 3: pick the one measured receipt line.
- Nov 4. Film the bench, receipt and B-roll; record narration.
- Nov 5. Edit; source captions; capacity graphic labelled "assumptions".
- Nov 6. Red team traces every on-screen number to a URL or CSV. Any failure finding goes to the Verizon mentor first.
- Nov 7. Final cut, AI-use disclosure, SUBMIT.
- Nov 8. Buffer only (11:59 PM deadline).

### Prior art and moat
PRIOR ART (and what it is not):
(1) Verizon's own install process [V].
- The technician confirms jacks and coverage.
- The swap guide's only check is "make a test call".
- The alarm check is "if the alarm company responds with a phone call".
- PROVE automates and receipts the step Verizon already assigns to the customer.
(2) Alarm-industry supervision [V].
- Central stations flag missed periodic test signals.
- Capture communicators on Verizon Cat-M1 (Telguard TG-7-V, Napco StarLink) decode alarms locally and send check-ins.
- These are after the fact and dealer-owned, and they tell Verizon nothing at install. That is why ALARM is install-only.
- Napco: a kiss-off is not proof, so PROVE requires a checksum-valid frame plus the kiss-off.
(3) Managed life-safety POTS replacement [V]: MarketSpark, CSG POTSolve, Ooma AirDial, EPIK, and AVIRE SENTINEL in the UK.
- Technician-led, with power, battery and connectivity monitoring and site surveys.
- SENTINEL excludes lift audio.
- All have per-customer dashboards, none a carrier install verdict.
(4) Self-install placement apps in home broadband [U for Verizon specifics]. SIGNAL here is not novel on its own; the combination with in-band VOICE, ALARM and BATTERY in one dispatch verdict is.
(5) Patents [V].
- Kone US8948348 and US10129390 (registration-based testing, caller-ID test-call receipt) are active: avoid.
- Orona EP2727873 (speech-recognition test) is active: avoid.
- Arris US6748050 (gateway line test with AEC disabled) has expired.
- Verizon/GTE US8630423 (speaker/mic test) has lapsed.
- BT (2020) searched call records for alarm-centre numbers: cite it as precedent.

MOAT, honestly. This is not strong IP; Verizon or Inseego could write this firmware. Our edge:
(a) the test plan and verdict rules mapped to Verizon's own documents and the Oct 15 rule change;
(b) the only public measured matrix of alarm formats, PERS, fax and TTY on Verizon's replacement paths, which resolves where Verizon's and Inseego's documents disagree;
(c) the only measured self-install completion data for the landline-keeping generation (OLLI-RU);
(d) a carrier-side per-wire-center rollup (Cutover Watch, for the final) that no vendor we found offers [U, absence of evidence].
The ask is a 30-day technical trial on one migration batch.

### Risks and kill gates
KILL GATES:
- K1 (Oct 27). Test: a BPC100 is live on a Verizon business voice line and reaches our receiver. If it fails, there is no measured Verizon result. If there is still none by Oct 29, re-decide the hero: show labelled models plus the battery bench, or move to the best non-copper fallback (Fix First, about 62).
- K2 (Oct 28). Test: the retail business BPC100 firmware accepts ##21 (the business guide has no ##21 step; the consumer Voice Connect guide does). If not, drop every registration claim; the ALARM line shows format support and acknowledgment only.
- K3 (Oct 30). Test: IRB exempt determination and OLLI-RU permission. If either fails, the Rutgers beat becomes the PROVE Lab alone, and the study runs for Feb 3. Never present student testers as older adults.
- K4 (Oct 29 to Nov 1). Test: the Verizon mentor confirms install visits are a real constraint and that no automated alarm check exists at install.
  - If most homes go to fiber or mobile, or Verizon already checks automatically: lead with proof at install plus the measured matrix, and drop "capacity" from the hero line.
  - If the visit exists for the 911 address and liability: pitch PROVE as visit triage, not visit elimination.
- K5 (Nov 3). Test: one clean, reproducible measured line (n ≥ 20, CI shown).
  - All pass: use the pass variant.
  - Contact ID fails on good signal: a sensitive finding; tell the mentor first and frame it as "measured so it can be fixed".
  - No clean line: BATTERY runtime is the backup.

OTHER RISKS:
- Gotcha optics. Mitigations: the "Verizon did what the FCC encouraged" framing, contradicting documents shared privately, failures to Verizon first.
- Medical alerts. Inseego's guide says such calls "cannot be made". Excluded from the video; tested only with a vendor's written window.
- Safety. Never dial 911, a real central station or RUPD dispatch.
- Privacy. No CPNI, no device GPS, de-identified study data.
- Legal. The tap is on our own bench line; production tone-listening is a firmware feature for Verizon counsel; no audio is stored.
- Scale. "About 1M" leans on a secondary 750k. The fully verified fallback line is "417k in two filings, 9× what's installed".
- Regulatory wording. "Paused" applies only to 26-227. 26-228 drew no pause, with authority from Oct 23. Never "approved", never "Dec 10".
- Crowding. Other teams may reach copper retirement. Few will have the ##21 step, the Contact-ID footnote, the Oct 15 deletions, a live-network bench and an older-adult study.
- Schedule. Fax, TTY and PERS move to Feb 3.
- The prototype's 5% loss → 60% delivered result and its fleet-day numbers are models, never findings.

### Judge Q&A
1) "Our technicians already test everything before the copper is cut."
- Your spokeswoman said that, and PROVE is that test, automated and receipted.
- Verizon's Voice Connect terms say the technician visit confirms the jacks and coverage at the box, while alarm and medical compatibility "is determined by your testing ... at time of install". The mailed swap guide's only check is "make a test call".
- Green receipts skip the visit; red receipts send the technician with the fault already named.

2) "MDM already sees battery and signal."
- Good: PROVE uses MDM data.
- MDM cannot see whether the panel's alarm reached the receiver and was acknowledged, whether the panel dials a registered number, or whether its format is one the box supports (Contact ID only, per Inseego's guide).
- That in-band part is exactly what the FCC encouraged carriers to get right.

3) "The technician is there for the 911 address and liability."
- Then PROVE triages the visit rather than replacing it.
- Verizon already uses self-install for box swaps and for the Voice Gateway, whose 911 address is the service address given at signup.
- The receipt can print the registered address for the customer to confirm. We never dial 911.
- Skipping the visit is Verizon's policy call; we supply the evidence.

4) "Your capacity numbers are assumptions."
- The anchors are not:
  - 46,000 installed, from Verizon's July and August 2026 filings;
  - 140k + 277k lines, from those filings;
  - the 750k is captioned as secondary.
- The other inputs are labelled. The number that matters, installs per technician-hour = 1/(truck share), depends only on the pass share, which our bench and the OLLI-RU study measure.
- Give us f, hours per install and crew size, and the table fills in.

5) "Isn't this a gotcha about our box?"
- No.
  - Verizon's own guide says Contact ID only and tells customers to test.
  - The FCC removed the showing and encouraged carriers to prevent alarm failures.
  - PROVE is how Verizon does what the FCC encouraged, one receipt per home.
- Every failure we measure goes to Verizon before it goes on a poster.

6) "Why is this Smart Campus? What does Rutgers get?"
- A permanent Rutgers PROVE Lab in ECE that tests life-safety devices over cellular, data nobody publishes.
- A service to older New Jersey residents through OLLI-RU at the moment their landline is replaced.
- In the final, the WHO ANSWERS elevator pilot with Facilities and RUPD.
- Also: Verizon's business-line exit, the line class that elevator phones and alarm dialers ride on, drew no FCC pause, and its authority starts Oct 23.

Backup questions:
- "Medical alerts?" Inseego lists them among calls that "cannot be made". We claim nothing; the receipt reads "not tested" without the monitoring company's window.
- "A kiss-off isn't delivery." Correct (Napco). PROVE requires a checksum-valid frame plus the kiss-off, and the alarm company confirms the test event as it does today.

**Dossier self-estimate:** 76/95

### Red team (verizon_vp): fixable, 64/95

- **fatal**: The 'install capacity' hero rests on a baseline Verizon's own documents contradict, and on numbers that look small next to Verizon's operations.
(1) The 'Today' column treats every fixed-wireless install as a 2-hour truck roll. But Verizon Voice Gateway, which the July and Aug 2026 filings list first among fixed-wireless replacements, is already a customer self-install. Its FAQ has the customer 'disconnect the existing phone connection to the NID (Network Interface Device) outside your home', fit the external antennas, and 'Add your alarm company's phone number in the "Settings" menu'. The lithium AAs 'come with the Voice Gateway'. Verizon already runs a path with no truck.
(2) Scale. The base case is 125k installs over 6 months, about 348 technicians. Verizon added 155k fiber connections net in Q2 2026 alone, and gross installs are higher. A GN&T VP will say install throughput is not the bottleneck.
(3) The 46k is a running total of customers, not an install rate. Setting it against the installs still needed ('seven times everything installed') compares a total with a rate.
(4) In the filing, Verizon puts the 46k next to '115 million wireless connections' and coverage of 95% of households. Verizon's own argument is that mobile and other providers are the replacement, which undercuts f = 0.30. *Fix:* Make the value self-install fallout, not capacity. Fallout is the share of self-installs that end in a truck, a care call or a silent alarm failure. Pitch it as: Verizon already ships boxes with no truck; PROVE makes that safe for alarm households and lets more homes take that path. Metrics a VP already tracks:
- first-time-right rate;
- repeat dispatch within 30 days;
- care contacts per install;
- alarm households confirmed working.
Keep technician-hours × Verizon's loaded cost as a CFO slider on the poster. Remove 'capacity', '7x' and the ≈1M bar from the video.
- **major**: The bench cannot pin its results on Verizon. There is no control arm, and the receiver sits behind a third-party SIP DID. The path is: panel → box → Verizon VoLTE/IMS → PSTN interconnect → SIP DID provider → Asterisk AlarmReceiver.
- The SIP provider's codec and DTMF mode (RFC 2833 vs in-band G.711) are exactly the issue in AICC's ¶31 request.
- Asterisk AlarmReceiver needs in-band ulaw DTMF.
Either can fail an event with Verizon not at fault. A 'Contact ID 41/50' or 'SIA 0/20' result would then go out as 'measured on Verizon's live network' when the DID vendor caused it. A clean pass also says nothing about commercial receivers (Sur-Gard, DMP, Bosch). /home/user/verizonsmartcampus/deliverables/PROVE_LAB_BENCH_PROTOCOL.md has no baseline arm. Its 'One Talk line' receiver option is not something you can terminate on a Pi. *Fix:* Run three arms with the same panel, the same receiver and the same day:
- (A) panel → HT813 FXS → Asterisk on the LAN with G.711 in-band. This is the receiver baseline and must be about 100%.
- (B) panel → a non-Verizon line (department copper, Optimum or Comcast voice) → the same DID. This is the trunk baseline.
- (C) panel → Verizon box → the same DID.
Lock the DID to G.711 with in-band DTMF and write that down. Report C against B with Wilson CIs, and publish only the difference. If possible, add a used commercial receiver, or a monitoring company's test account with its written permission.
- **major**: The production ALARM check is done at the wrong end of the call. A panel always sends a frame with a valid checksum, so checking the checksum at the box only proves what the panel sent.
Napco's FAQ describes a false acknowledgment at the receiver: on a line card that 'also supports 8-bit formats', a corrupt signal 'may be erroneously kissed-off'. The box cannot see that. So in production the receipt can only say 'the receiver acknowledged'. Whether the event was really delivered still depends on the alarm company confirming it, which is the step Verizon already hands the customer.
The Q&A answer ('PROVE requires a checksum-valid frame plus the kiss-off') will be taken apart by any alarm-literate judge. *Fix:* Split the line along the boundary between Verizon and the alarm company.
- ALARM PATH, Verizon's side: the box places a synthetic Contact ID call to a Verizon-run IMS test receiver, which decodes it and acknowledges. That gives ground truth on the part of the path Verizon owns.
- PANEL, the dealer's side: only inside the window the customer starts by pressing PROVE (which also gives consent), the box detects the format (16 DTMF digits means Contact ID; FSK means SIA), checks that the dialed number is registered, and watches for the kiss-off. The receipt then says 'confirm the test event with your alarm company'.
Never claim the box proves delivery.
- **major**: This would embarrass Verizon in a public, regulatory way.
- The first 24 seconds set Verizon's 'determined by your testing' next to 'the FCC no longer asks carriers to show a replacement works with alarms'.
- The captions cite the paused WC 26-227, an open Section 214 proceeding with hundreds of filings, including objections from counties.
- The failure variant would publish 'SIA [x]/20 on Verizon's live network'.
Objectors could cite a video made for Verizon's own competition in that docket, and Verizon's regulatory and legal teams would object to students describing a pending proceeding.
'Home-phone exit' is also wrong: 26-227 covers residential AND business legacy voice. The tagline 'when the regulator stops checking' reads as a jab at a deregulation Verizon supported. *Fix:* Keep docket numbers, §63.602, 'paused' and DA cites out of the video. Open on the customer: 'Verizon already asks every customer to test their alarm. We made it one button and a receipt.'
Put only a pass or neutral measured line on video: Contact ID n/50 with time to acknowledgment, or measured battery runtime. SIA results and contradictions between documents go to the mentor first and onto the poster as tested data. Write a tagline about proof, not about regulators.
- **major**: The hero box is probably last generation, and that choice creates the K1 and K2 risks.
- The filings list Verizon Voice Gateway (formerly Wireless Home Phone) first, and the dossier itself says new Voice Connect installs may ship on it.
- The Gateway has a screen, a Settings menu for alarm numbers (no ##21 guesswork), 24 h standby, and external antennas the customer fits.
- The retail business BPC100 may lack ##21 (K2). It also needs a business voice account (K1) while Rutgers has a hiring freeze and is reviewing every vendor contract. *Fix:* This week, buy a Voice Gateway on a team member's or the sponsor's consumer postpaid line (check orderability) and make it the hero. Keep the BPC100 as the second arm.
In production, PROVE is a Settings-menu item on the Gateway's own screen, and the result also goes out as an SMS or My Verizon card. Use the thermal printer as a prop only.
- **major**: The demo and the study leave out the steps that actually justify the truck.
- Verizon's terms say the technician confirms the 'jacks ... are functional'. That is inside-wire work: isolating the line at the NID, the house jacks, and the alarm panel's RJ31X. The RJ31X is usually hard-wired at the demarc, often in a basement far from the window where the signal is.
- The video shows hands 'plug in ... an alarm keypad'. Keypads are not plugged into the phone line; the panel's dialer connects through the RJ31X cord. An alarm judge will catch it.
- The OLLI-RU mock room has no NID, and IVR activation is done in advance, so the two hardest self-install steps are never measured. *Fix:* Add a WIRING line: GR-909-style metallic line tests from the box's line interface. Foreign voltage means the NID is not isolated; the tests also cover REN and resistive faults. That puts the technician's job on the receipt. Whether the BPC100 or Gateway exposes these tests is [U]; emulate them on the bench.
Give the mock room a real NID enclosure and an RJ31X, and have the demo connect the RJ31X cord, not a keypad.
In the OLLI study, measure NID isolation and activation as separate steps.
- **minor**: The OLLI-RU timeline is not realistic. In 9 days it needs an IRB determination with a faculty PI and CITI training, OLLI recruitment, consent and photo releases. And n = 8-12 with no NID and no activation produces weak p and x even if it happens. The A/B comparison that actually matters only arrives Feb 3. *Fix:* Make the PROVE Lab the video's Rutgers beat by default, and request the IRB determination today. Run the OLLI A/B (guide alone vs guide plus PROVE, with NID and activation, n = 20-30) for Feb 3, and present it as the data behind fallout reduction.
- **minor**: Pillar 1 claims 'AI-driven', but the verdict is hand-written rules plus Goertzel tone detectors. The 2026-27 brief asks for AI-driven automation. *Fix:* Fit a model to the T5 bench data that maps the box modem's RSRQ/SINR to the probability of alarm delivery, with CIs. That model becomes the SIGNAL threshold. Add an LLM fix-by-text assistant that turns a failed receipt into one plain instruction and reads the customer's reply. Lead with 'automation' and keep the AI claim modest.
- **minor**: Some of the Content is padding, and the signal proxy is weak.
- The ThingSpace LTE-M puck has no role in a production install test; it reads as ticking a Verizon-technology box.
- A phone's field-test app measures through a different modem, antenna and band set, so it is a poor stand-in for the box's own RF. *Fix:* Make the Verizon technology:
- the box modem's KPIs through Verizon device management;
- an IMS test-responder number and test receiver;
- integration with the order and dispatch system.
On the bench, read RSRP/RSRQ/SINR from the box's own admin page. Use ThingSpace only for the poster's nightly checks.
- **minor**: The hero receipt shows 'BATTERY: NONE, 3 AA MAILED' and then 'TRUCK NOT NEEDED'. That certifies a life-safety line with no backup power. The Voice Gateway also ships with lithium AAs, so the scenario looks invented. *Fix:* Show an all-green hero receipt, or one FIX BY TEXT, a re-run, then green. Keep the battery fault for the poster's 'break it' card.
- **minor**: Partner overlap and a weak moat.
- Inseego or the Gateway's maker could ship this firmware in one release cycle.
- Alarm dealers are moving dialer households to cellular communicators (Napco StarLink; Telguard TG-7-V on Verizon Cat-M1), so fewer homes will use the box's alarm port.
- MarketSpark and POTSolve already do signal site surveys. *Fix:* Lead with what Verizon cannot get from Inseego: a controlled measured matrix and self-install fallout data. The ask is a 30-day trial on one migration batch's self-install kits, with PROVE vs control.
- **minor**: The capacity numbers are dressed up. The 750k is 'locations' taken from a vendor blog; the video multiplies it by an assumed 30% and speaks the result as 'about seven times everything installed'. *Fix:* If any line count appears, use only the verified 417k from the two filings, with no multiplier on screen. Leave the sensitivity table with its sliders to the poster.

**What it must become:** PROVE: the self-install receipt for Verizon's copper-replacement boxes.\n\nDrop the 'install capacity' story. Verizon already self-installs Voice Gateway (the customer disconnects the NID and enters the alarm number in Settings), and the base-case install volume is small next to one quarter of Fios net adds. Pitch PROVE as what makes the no-truck path safe and lets more homes use it. The value is lower self-install fallout:\n- first-time-right rate;\n- repeat dispatch within 30 days;\n- care contacts per install;\n- alarm households confirmed working.\nPriced as avoided visits and calls × Verizon's own loaded cost, with the capacity math as a poster slider.\n\nHero device: Voice Gateway, which is current, has a screen and is consumer-orderable. BPC100 is the second arm. PROVE is a menu item on the box, and the receipt is the screen plus an SMS or My Verizon card. The printer is a prop only.\n\nThe receipt has five lines, with a clear boundary between Verizon and the alarm company:\n- WIRING: GR-909-style line test showing the NID is isolated and the house jacks work. This is the job the technician does today.\n- SIGNAL: the box modem's RSRQ/SINR against thresholds learned from bench data.\n- VOICE: two-way tones and DTMF integrity to a Verizon IMS test responder.\n- ALARM PATH: the box places a synthetic Contact ID call to a Verizon-run test receiver, which proves Verizon's side with ground truth. Inside the customer-started window only, the box also reads the panel's format, checks the registered number and watches for the kiss-off, then tells the customer 'confirm with your alarm company'.\n- BATTERY.\nThe verdict says who visits, if anyone: nobody, a Verizon technician, or the alarm company.\n\nRutgers data:\n- A three-arm controlled PROVE Lab: receiver baseline, non-Verizon trunk baseline, and the Verizon box, with the DID locked to G.711 in-band and Wilson CIs. Ideally add a used commercial receiver or a monitoring company's test account with written permission.\n- The video carries one pass or neutral measured line. Failures go to the mentor first.\n- The OLLI-RU A/B, with a real NID and activation, comes on Feb 3.\n\nVideo: no dockets, no §63.602, no 'paused', no failure numbers. Open with 'Verizon already asks every customer to test their alarm. We made it one button.' Close with the ask: a 30-day trial on one migration batch's self-install kits, measuring fallout against a control group.\n\nFor the final, a network-native stretch: the IMS test receiver as a network function across every replacement path, including Fios Digital Voice, rolled up per wire center.\n\nIf these fixes land, I'd estimate about 78-82 out of 95; as written, about 64.

### Red team (rival_and_feasibility): fixable, 69/95

- **major**: The first-choice measured line for the video, "Contact ID [x]/50, SIA [y]/20", proves nothing. I checked Asterisk's app_alarmreceiver.c: it decodes only Ademco DTMF formats (Contact ID, Express 4+1, Express 4+2, High Speed, Super Fast), and it forces G.711. It does not decode SIA FSK or pulse 4/2. So "SIA 0/20" measures our own receiver, not the BPC100. Any ECE judge who asks "what receiver did you use?" will collapse the measured beat, and calling it "Verizon's guide is right" turns a tautology into a public claim about Verizon's box. Also, "4/2" is ambiguous: Express 4+2 is DTMF and Asterisk does decode it. *Fix:* Drop SIA and 4/2 from the Nov 8 video. Make the measured line Contact ID through the BPC100 at three placements, giving n/50 delivered, first-try rate and kiss-off time, with the box's own bars plus RSRQ/SINR at each spot. That is the "full bars still fail" claim measured on Verizon's box, and it sets the SIGNAL threshold. Move T4 to Feb 3 with a used multi-format receiver (e.g. a Sur-Gard line card) and a copper or line-simulator control, so an SIA failure can be attributed to the box.
- **major**: "Measured on Verizon's live network" is confounded. The real chain is: panel → BPC100 DTMF handling → VoLTE/AMR or RFC 4733 events → Verizon IMS interconnect → a third-party carrier → our SIP DID provider → Asterisk DTMF detection. Contact ID's 50-60 ms digits are exactly what VoIP legs mangle, which is why AICC asked for G.711 with RFC 2833 disabled. A 44/50 result could be caused by VoIP.ms or Twilio and still get publicly blamed on Verizon. Separately, the bench protocol suggests One Talk as the receiver line, and One Talk does not expose SIP credentials to Asterisk. *Fix:* Add three controls and report the difference between the BPC100 path and the controls, not an absolute. (1) LAN baseline: panel → HT813 FXS → Asterisk on the LAN with no carrier. (2) Non-Verizon path: the same panel through a different line to the same DID. (3) Dual taps: one at the panel side of the RJ31 port and one at the receiver, plus an Asterisk log of whether digits arrived in-band or as RFC 2833 events. Show the control row on screen for 2 s. Run Asterisk on a cloud VM with a public IP, not behind the campus firewall.
- **major**: The capacity hero ("the truck goes only where the receipt says") may be wrong for Verizon's go-forward box. The VG10A Voice Gateway, which Verizon names in the same filings, is customer-set-up. It ships with 4 AAs pre-inserted, shows battery and AC icons and a "two bars" check on screen, and has a Signal Optimization screen and a Security-alarm number list. Even at face value, 348 dedicated technicians for six months (417k × 0.3) is small next to Verizon's wireline field force. A GN&T judge can answer "we don't send trucks" or "that's not our bottleneck", and K4, the mentor call, only happens on Oct 29, after the hardware is bought and the name is locked. *Fix:* Move the mentor questions to an email on Oct 22, before ordering. The three questions: install mix (technician vs mailed), VG10A vs BPC100 share of new installs, and whether any automated alarm check exists. Demote capacity from the title to one of three values. Retitle around the alarm proof, e.g. "Plug-and-PROVE: every copper migration ends with proof the alarm still reaches someone". Keep TRUCK NOT NEEDED as the verdict, but pitch it as triage ("trucks only for red receipts, with the fault already named"), not as a headcount crisis.
- **major**: Three of the four receipt lines already exist in Verizon's own process. SIGNAL: the VG10A has a bars check and a Signal Optimization screen. BATTERY: Verizon's Voice Connect FAQ already says "unplug the device from AC power... If the device powers off, the batteries are dead or not installed", and VG10A batteries come pre-inserted. VOICE: "make a test call". Yet the hero shot's money moment is BATTERY: NONE → 3 AA MAILED → TRUCK NOT NEEDED, the least novel line. Only ALARM is genuinely missing: the VG10A guide says it "does not detect or respond to alarm events". *Fix:* Make ALARM the visual and spoken climax: "your panel's test reached the receiver, the code was valid, and the acknowledgment came back". SIGNAL should show RSRQ/SINR against a measured threshold rather than bars. Collapse BATTERY and VOICE into a single small line. In Q&A, concede openly that "the screen already shows bars and battery; it cannot hear the alarm handshake".
- **major**: The "one button" is false for ALARM in production. A PROVE button on the box cannot make a customer's panel dial. A valid test still needs the customer, or the alarm company, to put the account on test and trigger the panel's communicator test, which is the manual step that exists today. The video shows hands pressing PROVE and getting "REACHED RECEIVER", which implies automation that does not exist outside the bench. On the bench, it also only works because a relay trips a zone. *Fix:* Show the real production flow on camera. The customer presses the keypad's communicator test (or the alarm company triggers it remotely). The box listens passively and verifies the handshake, a checksum-valid frame and the kiss-off against the real central station. Make the production trigger a handset star code (the same pattern as ##21), so no new hardware button is implied. Caption the bench receiver as "our test receiver, not a central station".
- **major**: "FIX BY TEXT" is aimed at the wrong household. The people keeping copper for alarms and medical devices are disproportionately the ones without a texting phone. Their only phone may be the line being replaced, and the dossier itself flags cordless-only handsets. An elder-care or human-factors judge will catch this immediately. *Fix:* Speak the result and the fix through the corded handset on the line that was just installed (an IMS announcement or the box's own voice prompt). Write it to the order record, and with consent text a named family member or caregiver. Rename the verdict "FIX AND RE-RUN". The thermal printer stays as the demo prop for "the record".
- **major**: The facts in the narration are not as defensible as the captions. "Its 2026 exit filings cover about a million legacy lines" depends on a vendor blog for 64% of the total, and adds lines (140k, 277k) to locations (750k, "or 2.7%"). "If a third choose a box... seven times" uses that secondary number. "The FCC paused the home-phone exit" mislabels WC 26-227, which covers "residential AND business legacy TDM-based voice" (DA 26-890). A GN&T or regulatory judge will correct it live. *Fix:* Narrate only verified numbers: "Two of Verizon's 2026 filings alone cover 417,000 legacy lines, nine times the 46,000 fixed-wireless replacement customers it reports." Caption the 750k as "a third filing, as reported: ~750,000 locations", and try to get a state PUC courtesy copy of WC 26-252 (MD, PA, NY, MA). If the docket is mentioned at all, say "the FCC paused Verizon's nine-state legacy-voice application; a separate business-services application drew no pause". Better still, keep it out of the video.
- **major**: The regulatory story contradicts itself and is sensitive for Verizon. In the same 2 minutes, B says "the FCC no longer asks" and A says "the FCC paused" the exit. Judges will ask which it is. The tagline "when the regulator stops checking" puts a deregulation Verizon and USTelecom sought in front of Verizon executives. Opening with a quote of Verizon's own disclaimer, then reminding them their application was pulled, reads as a gotcha however politely it is framed. *Fix:* Anchor on Verizon's own promise instead. Its customer letters (FL PSC copy of the WC 26-170 application) say the replacement "supports essential services like 911, alarm systems and many medical devices", and footnote 38 of that application says the key-applications list "sunset in 2025, so Verizon does not address them here". The pitch becomes "PROVE makes Verizon's promise checkable in every home". Keep the Oct 15 deletion and ¶31 for Q&A and the poster, and cut the Federal Register card from the video.
- **major**: The OLLI-RU study is unlikely to meet the Nov 1-3 slot and would mislead even if it did. A Rutgers exempt determination usually takes weeks. Students need CITI training and a faculty PI, and identifiable video of participants pushes the protocol toward expedited review. If it does run, the task is sanitized (IVR activation pre-done, no ##21, no alarm-company test) and OLLI members are an active, educated, self-selected group. With n = 8-12 the Wilson CI is about ±25 points, so the claimed 1/(1−p−x) multiplier spans roughly 2× to 10×. It does not "turn A4/A5 into data". *Fix:* For Nov 8, run a usability session under a not-human-subjects-research (product usability) determination with 3-5 consented volunteers, and report counts only ("4 of 5 finished alone"), not p. Move the A/B study (n = 20-30, full task including the alarm test) to Feb 3. In the video, say "usability session", never "study shows". The fallback narration is fine, but script it as a visual of the bench, not as an apology.
- **major**: K1 is a single point of failure and the fallback score drop is huge (to about 62). A BPC100 needs a Verizon Business line, and a department line at Rutgers goes through central wireless and procurement, so 5 days to activation is optimistic. The bench device is the 2022 business BPC100, whose firmware has no ##21 step. Students probably cannot buy the VG10A, so the video quotes the consumer guide over business firmware while the go-forward consumer box goes untested. *Fix:* Start two activation channels on Oct 22 and order a second BPC100 so one is always live. State plainly on screen: "tested on Verizon Business Phone Connect (BPC100), the hardware inside 2nd-gen Voice Connect; the test plan is device-agnostic". Ask the mentor for a loaner VG10A for the Feb 3 poster.
- **minor**: Pillar 1 claims "AI-Driven" automation, but the engine is threshold if/else (install.py). A professor will say there is no AI. The bench's SIGNAL thresholds also come from a phone field-test app beside the box, which has a different modem, antenna and possibly band. "MOVE 1 m TOWARD WINDOW" cannot be derived from a single-point reading, since multipath swings RSRP ±5-10 dB over 1 m. *Fix:* Either claim Pillar 2 (Verizon's own cost program names copper decommissioning and contractor spend), or add one small learned component: a logistic model from the box's own RSRP/RSRQ/SINR to Contact ID delivery probability, fit on T5, with CI. Read signal from the box's admin UI where it is exposed. Replace the directional advice with "weak here → try a spot on an outside wall, press again".
- **minor**: Liability optics. A Verizon-issued "ALARM: ACKNOWLEDGED, TRUCK NOT NEEDED" receipt looks like a warranty. Verizon's guide currently says "Verizon is not responsible for unsuccessful alarm responses". Verizon counsel and judges will ask who is liable when a green home's alarm fails in March. *Fix:* Word it as a timestamped test record, never a guarantee: "Tested 14:02 Oct 30; panel test acknowledged by receiver". Pitch it as evidence that the test Verizon's terms already require actually happened, which lowers dispute risk rather than raising it. Label poster results "tested information, not a warranty" (already planned).
- **minor**: A safety gap in the bench. A used panel from eBay may still hold the previous owner's central-station number and account. Powering it up with a line attached can send AC-loss, tamper or low-battery events to a real monitoring company, and possibly trigger a dispatch to the previous owner's address. A Contact ID panel with SIA or fire zones adds more risk. *Fix:* Factory-default every panel (hardware or installer default) before it is ever connected to a line. Verify the dial-out number is our DID, with the panel on the LAN baseline first. Write this into PROVE_LAB_BENCH_PROTOCOL.md §4 and have the faculty sponsor sign off.
- **major**: Several things will break on stage at the Feb 3 poster and the Mar 4 live demo. LTE reattach and IMS re-registration after the steel "basement" box can take minutes, so the next judge's "good" case prints TRUCK NEEDED. Panels lock into comm-failure trouble after a failed call and back off between retries. Flipping to SIA needs multi-step installer programming at the keypad. Asterisk behind Rutgers NAT/firewall (RUWireless Secure is off Jan 5, 2027) blocks inbound SIP and RTP. Each full check takes 30-90 s while judges wait. *Fix:* Use two pre-programmed panels (one Contact ID, one SIA) on an A/B switch. Replace the shield box with SMA step attenuators on the BPC100's external antennas so recovery is instant and repeatable. Add a scripted trouble-reset. Put Asterisk on a cloud VM and the bench on its own LTE/5G uplink. Keep a second activated box and a recorded run as fallback. Show a live progress bar per line so the wait reads as the product working.
- **minor**: Presentation: the first 24 s of a video scored out of 30 are two text cards (a guide quote and the Federal Register). The 1:08-1:30 capacity beat packs four numbers and three docket IDs into one caption. Neither the hero nor the stakes appear before 0:24, and in a stack of 40 videos judges decide early. The "no Verizon logo" rule also conflicts with filming a Verizon-branded box, and "Rutgers PROVE Lab" names a unit the Dean (a judge) never created. *Fix:* Cold-open on the stakes: a keypad shows the alarm "sent" and a beat of silence asks "did anyone get it?". Bring the hero in by 0:15. Keep one number on screen per beat. Blur or own the box branding consistently with the rules. Say "our bench in Rutgers ECE (Prof. X)" until the department approves a lab name.
- **major**: Smart Campus fit is thin. The hero is a national Verizon consumer and SMB process with no campus object. If K3 fails, Rutgers appears only as a room, and the Rutgers judges (Dean, CIO, Vice Provost) score Impact and ubiquity on the campus too. Uniqueness is not the issue: no crowd idea is near POTS replacement, and ##21, the Contact-ID footnote and the Oct 15 deletions need live research. The risk is that judges see a niche feature for a $129 box. *Fix:* Make the Rutgers link concrete and true. (1) The ECE bench publishes the only measured alarm-over-Verizon-box data. (2) New Jersey is one of the nine states in Verizon's pending legacy-voice application, so Rutgers retirees and OLLI members are among the households that will get Verizon's letters (do not claim specific wire centers). (3) Keep WHO ANSWERS (elevators) as the 10-minute final's campus pilot. Size the stakes with AICC's "five million installed panels" (quoted in FCC 26-19 fn 110).

**What it must become:** VERDICT: FIXABLE. As written I score it about 69 out of 95; the dossier's own estimate is 76. Done as below, I think it reaches about 78-80.

UNIQUENESS: Real. None of the 40+ crowd concepts touch POTS replacement. The ##21 step, Inseego's Contact-ID footnote, the Oct 15 deletion of §63.602 and the 46k-installed figure all need live, post-cutoff research. The danger is not duplication; it is judges reading this as a niche feature.

WHAT IT MUST BECOME: "Plug-and-PROVE: every copper migration ends with proof the alarm still reaches someone."

1. ANCHOR ON VERIZON'S OWN PROMISE, NOT ON THE FCC.
- Verizon's customer letters (WC 26-170, FL PSC copy) say the replacement "supports essential services like 911, alarm systems and many medical devices".
- Its device documents leave that to the customer: "Compatibility is determined by your testing ... at time of install". The VG10A guide says the box "does not detect or respond to alarm events".
- PROVE makes the promise checkable in every home. This is the opposite of a gotcha.
- Oct 15, ¶31 and footnote 38 ("the key-applications list sunset in 2025, so Verizon does not address them here") go to Q&A and the poster. Drop "paused" and "the regulator stopped checking" from the video.

2. THE ALARM LINE IS THE HERO.
- The receipt's climax: the panel's own test reached the receiver, the frame was checksum-valid, and the kiss-off came back, with the time.
- SIGNAL reports the box's own RSRQ/SINR against a measured threshold, never bars.
- VOICE and BATTERY shrink to one small line, conceding that the screen already shows bars and battery.

3. THE PRODUCTION FLOW IS HONEST.
- The trigger is a handset star code, the same pattern as ##21.
- The customer or the alarm company runs the panel's communicator test. The box firmware listens passively against the real central station.
- The result is spoken back through the corded handset ("fix and re-run", not "fix by text"), written to the order record, and texted to a caregiver only with consent.
- Only red receipts create a dispatch, with the fault named.
- The printer is a demo prop for "the record". The receipt is worded as a timestamped test record, never a warranty.

4. ONE DEFENSIBLE MEASURED LINE BY NOV 8.
- Contact ID through a live BPC100 at window, interior and basement spots: n/50 delivered, first-try rate, kiss-off time, RSRQ/SINR, and Wilson CIs.
- Three controls: a LAN baseline (HT813 to Asterisk, no carrier), a non-Verizon path, and dual taps with a log of whether digits arrived in-band or as RFC 2833 events. Report the BPC100 result as a delta against the controls.
- No SIA or 4/2 claims until Feb 3, when a multi-format receiver and a line-simulator control are in place.
- Fit a small logistic model from signal readings to delivery probability. That is the honest "AI" in the pitch, or claim Pillar 2 instead (Verizon's cost program names copper decommissioning).

5. VALUE WITH NO SOFT NUMBERS IN THE NARRATION.
- Spoken line: "Two 2026 filings alone cover 417,000 legacy lines, nine times the 46,000 fixed-wireless replacement customers Verizon reports."
- The 750k is captioned as reported locations.
- "Trucks only for red receipts" is pitched as triage, with the 1/(truck share) formula filled in from Verizon's own numbers.
- The mentor answers the install-mix, VG10A-share and existing-alarm-check questions on Oct 22, before any hardware is ordered.

6. RUTGERS.
- The ECE bench, under a faculty name, publishes the only measured alarm-over-Verizon-box data.
- Run a 3-5 person OLLI-RU usability session under a not-human-subjects-research determination, reporting counts, not p. The A/B study (n = 20-30, full task including the alarm test) goes to Feb 3.
- Say it plainly: New Jersey is one of the nine states in Verizon's pending application, so these are our neighbours.
- WHO ANSWERS (elevators) stays as the final's campus pilot.

7. VIDEO.
- Cold-open on a keypad that says the alarm was "sent", then silence: "did anyone get it?"
- The hero appears by 0:15: plug in, star code or button, the panel's test, the receipt with ALARM featured.
- Then the measured line with its control row, the verified 417k-vs-46k line, the Rutgers beat, and the production path through MDM firmware, an IMS test number and ThingSpace.

8. POSTER AND STAGE.
- Two pre-programmed panels (Contact ID and SIA) on an A/B switch.
- SMA step attenuators instead of the steel box, so recovery is instant.
- Asterisk on a cloud VM; the bench on its own LTE/5G uplink, never eduroam.
- A second live box and a recorded fallback.
- Every used panel factory-defaulted before it touches a line.

## F2_elevator_hero: WHO ANSWERS: every elevator HELP call, proven to reach a person (F2, the campus-first alternative with elevator HELP as the single video hero)

**One-liner:** The elevator code's automatic check watches the line and is written so it never has to place a call. WHO ANSWERS grades the call itself where the elevator line meets Verizon's copper-replacement voice path, with nothing installed in the car. For every HELP press it checks the number dialed against the owner's registry, whether a person picked up (or voicemail, a menu or a "not in service" recording), the seconds to a human voice against the code's 45-second redirect, and whether the answerer sees the right building and car.

### Problem
The code checks the wire, not the call (verified):
- ASME A17.1 2.27.1.1.6(a): line verification "shall not require activation of the two-way communication link(s)". A failure may take up to 24 h to annunciate (Interpretations 13-319 and 13-343). https://cstools.asme.org/csconnect/FileUpload.cfm?View=yes&ID=61439
- A17.1-2022, verbatim from the reprint at https://www.ashb.com/wp-content/uploads/2024/08/IS-2024-115.pdf:
  - 2.27.1.1.3(i): "shall not be transmitted to an automated answering system... answered by authorized personnel".
  - 2.27.1.1.2: redirect if "not acknowledged ... within 45 s".
  - (f): location and elevator number "on demand".
  - The guide's owner test fails if "the operator cannot ID the elevator without aid from the caller."
- Caveat: NJ holds existing cars to the edition in force at installation (N.J.A.C. 5:23-12.2(b)), so the 45 s rule is a benchmark for older cars, not a duty.
- Elevator phones do not detect recordings. Viking K-1600-EHFA call-progress detection hangs up on busy, silence and similar, but documents no voicemail or intercept detection. https://vikingelectronics.com/products/k-1600-ehfa/

Chicago inspections (verified and re-derived from https://data.cityofchicago.org/resource/22u3-xenr.json, queried 2026-10-21):
- Since Jan 2023, 6,725 inspections drew an elevator maintain/repair violation (EV1110/EV1111). Both counts were re-queried live.
- About 24-25% of those inspections (1,613-1,721 depending on the keyword filter) mention the emergency phone. That is 7.6% of the 23,025 violations.
- CORRECTION: it is not "24% of maintenance violations", and it is not a per-car failure rate.
- Of 1,721 phone-cited inspections, 72% name no fault type. Among those that do, route or location faults (346) outnumber "dead" (78) about 4 to 1.
- CORRECTION: "dominate" holds only within that subset.
- Within the route and location group: 105 programmed to 911 instead of a 24 h service (a Chicago rule; at Rutgers, RUSSECC may be the correct answerer); 169 location or car-ID message missing or wrong; 4 voicemail; 2 previous or wrong maintenance provider.
- Oct 9, 2026, verbatim: "VERIFY THAT OPERATOR HAS CORRECT ADDRESS ... FREIGHT STATES 920 S FRANKLIN BUT THEIR PROPMT IS STATING THAT THE CALL IS COMING FROM NASHVILLE, TN." The cause (a calling-number lookup) is UNVERIFIED.

Riders and scale:
- News12, published May 25, 2026 (verified from page metadata): a trapped Farmingdale NY tenant says HELP reached voicemail, "nobody can help you right now". This is her account; the line type is unknown and nothing ties it to copper. https://newyork.news12.com/trapped-between-floors-fairfield-fieldstone-apartments-tenant-says-elevators-emergency-help-button-failed
- FDNY: 27,247 occupied-elevator emergencies in 2025, re-verified through the API at https://data.cityofnewyork.us/resource/8m42-w767.json.
- CORRECTION: drop "98.5% via the phone". The PHONE alarm source (26,850) is how FDNY dispatch was notified, not the elevator phone.

The migration moment:
- Ooma AirDial director at BOMA 2024 (verified quote, buildings.com, Jul 16, 2024; vendor claim): "about 50% of them don't work at the time we go to replace them". Note this is about lines found broken before replacement. https://buildings.com/industry-news/article/55126180/facing-the-copper-sunset-8-tips-to-choose-a-pots-replacement-boma-2024
- Kings III's "microphone, speaker, or wiring" admission is UNVERIFIED (search index only; the site returns 403). Keep it off screen: our check does not test the car speaker either.
- DA 26-1042 (Sep 28, 2026): Verizon's own NG911 testing caught MLTS 911 calls going to the wrong center. Use it as the "testing catches wrong answerers" precedent, never as a gotcha. https://docs.fcc.gov/public/attachments/DA-26-1042A1.pdf

Rules:
- FCC 26-19, effective Oct 15, 2026, removed 47 CFR 63.602, including "interoperability with key applications and functionalities". 63.602 never named elevator phones. https://www.govinfo.gov/content/pkg/FR-2026-10-01/pdf/2026-20192.pdf
- WC 26-228 (Verizon NJ B1, PBX trunk and key-system lines) is authorized "on or after October 23, 2026". Per the docket, no removal notice as of Oct 21. Never say "approved".
- WC 26-227 was pulled from auto-grant (DA 26-1038).
- Piscataway copper: "on or after December 10, 2026". No countdown, and no Rutgers pins on a map.

Channel:
- Verizon's POTS Replacement page hands elevator and fire lines to CSG POTSolve ("exclusive to Verizon", an ATA on a Verizon wireless business internet plan) and MarketSpark (dual SIMs across Verizon, AT&T and T-Mobile).
- It advertises no line test or end-to-end test.

Rutgers:
- The Aug 2026 elevator standard names Avire, Wurtec and Kings III and requires a Communications Failure jewel, but does not say who answers.
- The Facilities call center is open 7:00-4:30; RUSSECC is the 24/7 PSAP. Who answers HELP is UNVERIFIED.
- Rutgers is its own construction AHJ under a DCA MOU.
- NJ inspects at most yearly and keeps no entrapment statistic.
- Fire communicators (2020) and blue lights (2023) are already off copper. Which elevator lines ride Verizon is UNVERIFIED.

### Solution
Checks:
- Number dialed vs the owner's registry, on every press (digits on the line, or the SIP Request-URI on the network side). Catches the old contractor, stale numbers and misprogramming.
- Who picked up: person, voicemail, IVR, intercept, busy, no answer or fax. On real calls, SIT tones and SIP final responses by default. On test presses, spectral features of the first ~10 s of the answerer's audio (prototype/prove/answer.py). Nothing is recorded or transcribed.
- Seconds to a human voice vs the 45 s redirect benchmark.
- Location the answerer sees: monthly, about 10 s of the answerer's time by agreement, plus the HELP audit. Also a fingerprint of the phone's own location message vs the one recorded at commissioning.
- Car mic audio present at the port, on test presses only.
- Daily pre-answer probe that the answerer number still rings rather than returning SIT, vacant or busy. Released before answer, by agreement.
- Gateway registration, RF and battery from Verizon device management (the baseline, not our claim).

What happens on a failure:
- Tickets route to the party that can fix it: Verizon (RF, registration, gateway), the elevator contractor (dialing program, location message, mic), the answering point (no person, slow, wrong label) or Facilities (registry).
- A hash-chained evidence log (ledger.py) serves as voluntary inspector documentation, never a compliance claim.
- Pilot-gated: if a real HELP call reaches a machine or no person within 45 s, the owner's designated on-call gets a text. We never dial 911.

Where it runs. There is no series relay anywhere:
1. Signaling-only checks in Verizon's voice network for lines whose owners opt in (One Talk, Business Phone Connect, Business Digital Voice).
2. The same logic as firmware in partner gateways (POTSolve's ATA already sees every digit and sample).
3. A listen-only, high-impedance, transformer-coupled tap on the gateway's analog port in the machine room. It cannot go off-hook, and it reports over its own ThingSpace LTE-M line. It also baselines a line on copper before the move.

Out of scope: the car speaker (the optional in-car add-on, installed by a licensed mechanic, stays out of the video), Deaf text and video (OEMs ship it), and 911.

Built today (20 of 20 tests pass):
- answer.py classifier: 100% exact on clean synthetic audio, 95.4% under stress, 100% person-vs-not in both. Synthetic only; real-line calibration is Gate A.
- Console "Who answers?" panel, triage and ledger.
- Fix before filming: answer.py's default registry number is RUPD's published 732-932-7211. Change it to a 555 number and never dial it.

Full dossier: /tmp/claude-0/-home-user-verizonsmartcampus/ac4afb2e-cdc2-53a2-a8f3-1a6a3e0d44b6/scratchpad/gen4/dossier_F2_elevator_hero.md

### Verizon technology
Path under test: Verizon's copper-replacement voice.
- Bench: a Business Phone Connect (Inseego BPC100, $129.99, Cat-4 LTE with HD VoLTE on Verizon's IMS core).
- The BPC100 is a bench stand-in only. Verizon does not market it for elevators; real elevator lines go to the life-safety partners, CSG POTSolve ("exclusive to Verizon", ATA plus LTE router with battery on a Verizon wireless business internet plan) and MarketSpark.
- On camera, the "not in service" verdict is Verizon's real intercept (SIT plus recording) on our own cancelled line, classified live. That answers the "not Verizon's network" critique that sank HangUp.

ThingSpace: the tap's own self-serve LTE-M line ($1.50-$6 a month), Connectivity Management API callbacks for verdicts and tickets, and Device Diagnostics.

One Talk ("starts at $20 per line"): hosts the test responder and the daily pre-answer probe.

Production placement:
- Signaling checks inside Verizon's voice network for lifeline lines whose owners opt in: dialed number, SIP final responses (404/410, 486, 408/480), answer time, and SIT event detection (a standard SBC feature, e.g. AudioCodes).
- The same logic as firmware in partner gateways.
- Honest caveat: POTSolve rides Verizon LTE data through an ATA, and whose voice switch carries those calls is UNVERIFIED. For those lines the checks sit in the gateway or partner platform, not necessarily Verizon's IMS.

Not claimed: network slicing, RedCap, or any customer-record access for students.

Roadmap for the poster and finals only:
- Cutover Watch: per-wire-center lifeline health before and after cutover, with I32 SILENT AFTER CUTOVER as its engine.
- Plug-and-PROVE: install-time proof for Voice Connect/BPC100 home boxes.

### Verizon value
10-K anchor (Verizon 2025 10-K): Business segment $29,069M (-1.6%); Enterprise & Public Sector $13,534M (-4.8% from $14,218M); Business Markets & Other $13,581M (+3.7%).
- University, hospital and government elevator lines sit in E&PS; small property owners sit in Business Markets.
- From Q1 2026 Verizon no longer reports these sub-lines (8-K, Mar 13, 2026).
- Verizon discloses no life-safety line count or revenue, and we invent none.

Three levers:
1. Retention at a forced migration. Verizon's own life-safety channel is multi-carrier: MarketSpark ships dual SIMs including AT&T and T-Mobile, Ooma AirDial is certified on all three carriers, and the Talkaphone blue-light retrofit kit ships AT&T-only SIMs. Measured proof on the Verizon path is a reason to make Verizon primary.
2. Lower cutover risk. The home-phone exit (WC 26-227) is under extended FCC review over whether emergency users can still call for help. Per-line before/after evidence answers that objection class. Verizon's own 2022 figure of about $180M a year from 36 central offices shows why exit speed matters; it is not a saving we claim.
3. An assurance add-on in the life-safety tier, priced against market anchors: RATH SmartView Hub at $9.99 per device per month, and Wurtec Watch at "less than $1/day".

CFO formula, all inputs labeled ASSUMPTIONS for a Verizon mentor to replace:
  value = L x s x r x 12 + L_a x p x 12 + N x c
- L: lifeline lines in the migration footprint
- s: share flipped to Verizon-primary by proof
- r: Verizon revenue per line per month (UNVERIFIED; One Talk's "starts at $20" is the only public anchor)
- L_a: lines taking the add-on; p: add-on price
- N: escalations or repeat dispatches avoided; c: cost per escalation (UNVERIFIED)

Scale check, arithmetic on an assumption and not a forecast: 10,000 lines retained at an assumed $20 a month is $2.4M a year, small next to E&PS's $13.5B.

Honest summary: this is retention and risk reduction, not a growth line. Its edge over the box hero is giving GN&T judges a Rutgers-proven method for the riskiest line class in the copper exit.

### Rutgers primary data
Ground rules: this is a joint fix with Facilities and OIT, never a critique.
- No HELP press without pre-announcement.
- Never call 911, RUPD or RUSSECC dispatch lines.
- No people in photos and no personal data.
- Results are reported in aggregate; building-level findings go to Facilities first.

BY NOV 8:
1. Walk audit. No permission needed; public areas only; no presses. Target 100+ cars, minimum 60, across Busch, Livingston, College Ave and Cook/Douglass.
   - Per car: phone vendor and model, posted instructions, whether the Communications Failure jewel is lit now, whether a car ID is posted (NJ requires one retroactively under 5:23-12.12), and whether a visual or text display is present.
   - Output: the first inventory of Rutgers elevator phones.
2. Posted-number census, about 40 buildings (lobbies, refuge areas, garages, pools, lab corridors).
   - Photograph every posted emergency or after-hours number and classify it by carrier and switch from public LERG-derived data (localcallingguide.com).
   - After an emailed heads-up to Facilities, call only numbers that advertise 24/7 and are not dispatch lines, with a 15-second honest script.
   - Record: person, voicemail, recording or no answer; seconds to a person; whether they knew the building.
   - If Facilities objects, keep only the photos and classification.
3. Bench dataset on a real Verizon line.
   - At least 40 real calls to four destinations (a person, voicemail, a real Verizon intercept on our own cancelled line, and our own "old contractor" IVR), giving a confusion matrix on real audio.
   - A "green light" experiment: antenna off, mains off, battery out and a wrong programmed number. Record whether and when the phone's own line monitor or jewel notices, against the tap. No assumed outcome; any Verizon-relevant finding goes to Verizon privately first.
4. Done: our re-derivation of the Chicago and NYC open data.
5. Filed now: a request to Facilities and RUPD for a pre-announced HELP audit on 10-20 cars (run only if they agree), plus an OPRA backup for each elevator phone's line type, carrier and programmed destination.

BY FEB 3:
1. Pre-announced HELP audit on 30-50 cars with Facilities, RUPD/RUSSECC and the answering point. This is the first NJ dataset of its kind.
   - Per car: who answers, seconds to answer, and whether the answerer identifies building and car without asking (the ASME/Kings III owner test).
   - Redirect behavior is tested on 3 cars at most, and only by agreement.
2. Registry and Gate A: which Rutgers elevator lines ride Verizon copper or Verizon replacements.
3. Tap pilot on 1-3 cars, only with Facilities, the elevator contractor and the Rutgers codes office.
   - For 4-6 weeks it grades routine maintenance test presses and real calls.
   - Signaling only on real calls until Rutgers counsel reviews.
4. Lab matrix: elevator phone models x Verizon paths (BPC100, One Talk, and POTSolve if lent). Measures call completion, digit integrity, location message and answer detection.
5. A joint Facilities and OIT memo: "what we checked together, what we fixed".

### Demo
VIDEO BEATS (2:00):
1. Rutgers car interior, filmed with Facilities' OK; HELP not pressed.
2. The Chicago Oct 9, 2026 "NASHVILLE, TN" record and the News12 May 2026 voicemail quote.
3. The A17.1 2.27.1.1.6(a) clause, then the dark Communications Failure jewel.
4. A one-caption FCC Oct 15 change ("key applications" showing removed).
5. HERO, the bench:
   - a real hands-free elevator phone on a live Verizon line, with the listen-only box in a mock machine room;
   - four presses to four destination cards;
   - split screen: "Phone: CONNECTED x4" against "WHO ANSWERS: 1 of 4 reached a person";
   - verdicts: VOICEMAIL / NOT IN SERVICE (live Verizon intercept) / "OLD CONTRACTOR" MENU / PERSON 6 s with the label confirmed.
6. Rutgers results card, filled only from collected data and shared with Facilities first.
7. Verizon channel graphic: POTS Replacement, then POTSolve and MarketSpark, with tickets routed to owners and a small "Roadmap: Cutover Watch" tile.
8. End card: "Student concept. Not a Verizon product."

POSTER TABLE (Feb 3):
- Hardware:
  - an acrylic car operating panel with a real HELP button and a Communications Failure jewel, wired to a real elevator phone;
  - a Verizon BPC100;
  - the listen-only tap with its ThingSpace LTE-M modem;
  - a receipt printer.
- Judges press HELP and pick a destination card: a teammate at the table, voicemail, number not in service, or the "old contractor" menu.
- Three fault switches: location message says Nashville, answerer slow (55 s), antenna off.
- The phone always says connected; WHO ANSWERS prints the verdict within about a minute and routes the ticket.
- Side panels: Rutgers HELP-audit aggregate, the Chicago chart, and the roadmap tiles (the Plug-and-PROVE box and the Cutover Watch map).

### 120-second script
A = engineering, B = business. About 265 words at about 150 wpm. Bracketed items are filled only from collected data.

[0:00-0:07] VISUAL: Inside a Rutgers elevator (Facilities OK, HELP not pressed); finger over HELP. Caption "Rutgers. 2:00 a.m."
A: "You're stuck between floors at two in the morning. You press HELP. Who answers?"

[0:07-0:20] VISUAL: Chicago violation record, Oct 9, 2026, with "...THE CALL IS COMING FROM NASHVILLE, TN" highlighted; then News12, May 25, 2026: "We're sorry, nobody can help you right now." Source captions.
B: "On October ninth, a Chicago inspector cited an elevator phone whose operator was told the call came from Nashville, Tennessee. In May, a trapped New York tenant says HELP reached voicemail."

[0:20-0:33] VISUAL: Clause "shall not require activation of the two-way communication link(s)" (ASME A17.1 2.27.1.1.6(a)); close-up of the dark Communications Failure jewel.
A: "Elevator code checks the wire, not the call. Its automatic check works without ever placing one, so this light stays dark even when HELP reaches a recording."

[0:33-0:47] VISUAL: Copper pair, then Verizon life-safety gateway, Verizon LTE, answering point. Caption "Since Oct 15, 2026, FCC rules no longer require the 'interoperability with key applications' showing (former 47 CFR 63.602)."
B: "And these lines are leaving copper, including onto Verizon's network. Since October fifteenth, federal rules no longer ask a carrier to show its replacement works with key applications. The move is the moment to check."

[0:47-1:11] VISUAL: Bench with the elevator phone on a live Verizon line and the listen-only box in a mock machine room. Four presses, four destination cards. Split screen "Phone: CONNECTED" x4 vs verdicts: VOICEMAIL FAIL / NOT IN SERVICE (Verizon intercept) FAIL / "OLD CONTRACTOR" MENU FAIL / PERSON 6 s, "Demo Building, Car 2" confirmed PASS.
A: "WHO ANSWERS listens where the elevator line meets Verizon's network, with nothing in the car. It checks the number dialed, tells a person from voicemail or a recording, times the answer against the code's forty-five seconds, and confirms the answerer sees the right building and car."
B: "Four presses. The phone said 'connected' four times. One reached a person."

[1:11-1:29] VISUAL: Walk-audit footage (panels and signs only, no people); results card. Caption "Rutgers walk audit and posted-number census, Oct 22-Nov 3, 2026, shared with Rutgers Facilities first."
A: "At Rutgers we've audited [M] elevators and called [K] posted twenty-four-hour numbers overnight: [RESULT: '[X] reached a recording or no one, not a person.' OR, if none: 'every one reached a person, and now we'll keep it that way through the move.']"
B: "We share every finding with Facilities and OIT first, so it becomes a fix."

[1:29-1:50] VISUAL: Verizon POTS Replacement, then "life-safety: CSG POTSolve ('exclusive to Verizon') and MarketSpark (dual SIM: Verizon, AT&T, T-Mobile)"; tickets route to Verizon / contractor / answering point; corner tile "Roadmap: Cutover Watch".
B: "Verizon hands elevator lines to partners, and some of those gateways carry a rival's SIM too. Proof that HELP reaches a person is a reason to keep the lifeline on Verizon. It can run in Verizon's voice network and in the gateways its partners already install."

[1:50-2:00] VISUAL: End card "WHO ANSWERS", team names, "Student concept. Not a Verizon product."
A: "The code checks the wire." B: "We check the call." BOTH: "WHO ANSWERS."

NEVER SAY: "Dec 10", "the FCC approved", "Verizon's boxes fail", the Kings III quote, "98.5%", "24% of violations", or any Rutgers building name next to a failure.

### 18-day plan
D1 (Oct 21-22), all:
- Order a used hands-free elevator phone (Viking K-1600 class or RATH; about $150-300, price UNVERIFIED), a BPC100 ($129.99) plus a Verizon line, a One Talk line, a Raspberry Pi 5, a USB audio interface, a telecom isolation transformer and parts, a ThingSpace self-serve LTE-M modem ($1.50/mo) and acrylic for the panel.
- Email Facilities and RUPD (HELP audit request plus census heads-up) and file the OPRA request.
- Change answer.py's placeholder registry number (RUPD's published number) to a 555 number.

D2-5 (Oct 22-25), business pair: walk audit on 4 campuses, photographs of posted numbers, LERG classification script.

D3-7 (Oct 22-27), engineering pair: bench build.
- The elevator phone on the BPC100.
- The listen-only tap: high-impedance bridge, off-hook voltage sense, Goertzel DTMF.
- Port answer.py from synthetic to streaming audio.
- Four destinations: a teammate, voicemail, our own cancelled line for a real Verizon intercept, and our own Asterisk "old contractor" IVR.

D6 (Oct 26): read Verizon's Q3 results for any copper or POTS statement.

D7-8 (Oct 27-28): GATE A and GATE B.
- Gate A: at least 40 real calls, person-vs-not at least 95%, intercept and voicemail correct.
- Run the green-light fault-injection experiment.
- Gate B: the tap's leakage and ring-voltage safety test.

D8-10 (Oct 28-30):
- Census calls after the Facilities heads-up; compile the Rutgers results.
- GATE C (Oct 30): a Rutgers number in hand, or a Facilities HELP audit approved.
- DECISION: F2 hero, or revert to the box hero.

D11-13 (Oct 31-Nov 3): filming, covering the car interior (Facilities OK), bench presses, walk-audit B-roll, and graphics (clause, Chicago record, FCC caption, channel diagram).

D14-16 (Nov 4-6): edit, caption every number, and run GATE D, a claims check of every number against the dossier. Add the Responsible AI disclosure.

D17-18 (Nov 7-8): buffer and submit.

Budget: about $700-1,200 (estimates; Verizon line plan prices UNVERIFIED).

### Prior art and moat
ALREADY EXISTS:
- Line or path supervision, the code baseline:
  - A17.1 2.27.1.1.6 automatic line verification;
  - Viking LV-1K daily dial-tone test;
  - RATH line checks every 10 min to 23 h;
  - JANUS line presence;
  - Kings III 30-day check-in (UNVERIFIED);
  - AVIRE SENTINEL (UK managed lift-line migration) monitors connection and battery and excludes lift audio units;
  - AirDial, MarketSpark and POTSolve supervise power, battery and signal.
- In-unit audio self-tests: 2N LiftIP "Speaker test", SafeLine, Esse-Ti EP1847500 (2007).
- Test calls through the real path:
  - EN 81-28 (Europe), at least every 3 days;
  - Kone US8948348 (registration monitoring, to about 2030);
  - Kone US10129390 (receiver-side caller-ID test-call processing, to about 2034);
  - Orona EP2727873 (speech-recognition test diversion).
  Our design avoids receiver-side caller-ID test processing and speech recognition, and needs a freedom-to-operate review before commercial use.
- Answering-machine detection in outbound dialers is decades old, and SIT detection is a standard SBC feature. Our classifier applies known signal processing; it is not an invention.
- Location messages and Deaf text/video already ship from RATH, Viking, Wurtec, Otis, Schindler and MAD.

NOT FOUND ANYWHERE (absence of evidence from fetched sources, not proof):
1. Grading the far end of each HELP call from the originating side: dialed number vs registry, person vs machine, seconds against 45, and the label the answerer sees. A monitoring center sees only calls that reach it; calls to the old contractor, a vacant number or voicemail never do.
2. A carrier-side, per-wire-center rollup across a copper exit.
3. A measured NJ HELP audit.

MOAT: thin as technology, and we claim none. The value to Verizon is that its partner channel ships the check first; CSG, MarketSpark, AVIRE or Kings III adding it is the success case for Verizon. Our defensible assets:
- the Rutgers datasets (walk audit, posted-number census, HELP audit, lab matrix);
- the open-data re-derivation (Chicago and NYC);
- bench results on the Verizon path.

### Risks and kill gates
KILL GATES:
- A (Oct 28): at least 40 real calls on the live Verizon BPC100 line with person-vs-not at least 95%, and a real Verizon intercept and real voicemail classified correctly. Else claim signaling-only checks (digits, SIT, answer time) and cut the person-vs-voicemail line.
- B (Oct 28): bench measurement that the tap cannot draw loop current, survives ring voltage, and cannot short the line if it fails. Else bench and video only, with no pilot hardware on any Rutgers line.
- C (Oct 30): walk audit at least 60 cars and census at least 25 numbers, or a Facilities-approved HELP audit on at least 10 cars. Else revert to the box hero (Plug-and-PROVE) and keep a 20 s elevator beat.
- D (Nov 6): every on-screen number traced to the dossier, and nothing from the never-say list. Else cut the line.
- E (Dec-Jan): registry or OPRA shows elevator line types and carriers. If none ride Verizon, present Rutgers as the pilot site and lead the poster national-first.
- F (before any real-call audio analysis): Rutgers counsel approves features-only analysis of the answerer side. Else signaling only on real calls and media on test presses only.

OTHER RISKS:
- No documented US case ties an elevator phone failure to a copper cutover. Claim only that the move is when nobody is checking.
- Rutgers results may be all-pass. Then Rutgers is the control group ("keep it that way through the move"): weaker for the video, better for the relationship.
- Facilities, RUPD or the answering point may decline the HELP audit. Never publish building-level failures.
- Direct Verizon revenue is small, and elevator hardware belongs to partners.
- POTSolve voice may not touch Verizon's IMS, so some production checks belong in partner firmware.
- The 45 s redirect binds only cars installed under newer A17.1 editions. Call it a benchmark, not a violation.
- The copper topic is crowded internally (14 of 14 lenses) and possibly among other teams. Differentiate with the Rutgers data and the live Verizon bench.
- The NJ wiretap reading is ours, not counsel's.
- The Kings III quote is unverified and stays off screen.
- Never test 911, RUPD or RUSSECC lines.

### Judge Q&A
1) "Monitoring companies and Verizon's partners already test these lines, and our techs test at install. What's new?"
They test line, power and signal. The code's own check is written so it never needs a call. A monitoring center sees only the calls that reach it, so a phone dialing the old contractor, a cancelled number or voicemail never shows up there. We grade the far end of every HELP call from the originating side. On our bench the phone said "connected" four times and one call reached a person.

2) "That's a Raspberry Pi on a phone line, not Verizon's network."
The box is the prototype. Production runs where Verizon already is:
- signaling checks in Verizon's voice network for owner-opted-in lines (dialed number, final response, answer time, and SIT detection, a standard SBC feature);
- the same logic as firmware in the partner gateways Verizon sells.
On camera, "not in service" is Verizon's real intercept on a live Verizon line.

3) "Where's the money? Elevator lines are a rounding error."
Agreed that direct revenue is small, and we invent no dollars. The value is three things:
- keeping lifelines on Verizon when its own partner channel carries rival SIMs;
- per-line evidence for the objection class now holding the home-phone exit under FCC review;
- an add-on priced against market anchors (SmartView Hub $9.99 per device per month).
Every formula input is labeled, and we want a Verizon mentor's numbers.

4) "Are you listening to emergency calls?"
No:
- On real calls the default is signaling only: digits, answer time, final response, tones.
- Audio features run only on pre-announced test presses, and only on the answerer's side, never the rider's.
- Nothing is recorded or transcribed.
- Any real-call audio analysis waits for Rutgers counsel.
- We never call 911, and students never see customer records.

5) "Does Rutgers even have this problem?"
[Our data.] If we found failures, Facilities has them and they are being fixed. If none, Rutgers is the control group, and the risk arrives when each line moves. Rutgers' Aug 2026 elevator standard names three phone vendors but not who answers, and the Facilities call center closes at 4:30, which is why we built it with Facilities.

6) "You're putting a device on a life-safety line. Would an inspector allow that?"
Round 1 is bench only. The production version adds no device: it is firmware in the gateway already on the line. The retrofit box can only listen, cannot go off-hook, and is built so a failure cannot short the line. A pilot happens only with Facilities, the elevator contractor and Rutgers' own codes office, which inspects Rutgers elevators under its DCA agreement.

**Dossier self-estimate:** 74/95

### Red team (verizon_vp): fixable, 66/95

- **fatal**: The Verizon value case fails on its own logic. Every failure the hero catches comes from programming or the answering point, not the transport: voicemail, a vacant number, the old contractor's menu, a wrong label on the answerer's screen. A MarketSpark dual-SIM gateway running the same check gets an identical result on AT&T. So 'proof that HELP reaches a person' gives an owner no reason to make Verizon primary, and lever 1 (retention) falls apart. Lever 2 is mismatched: the WC 26-227 objections that hold the exit are residential (medical alert, 911, rural coverage). Elevator lines are B1 business lines in 26-228, which drew no pause, so elevator evidence unblocks nothing. Lever 3's add-on revenue goes to CSG, MarketSpark or Kings III. Verizon's direct take is a $1.50-$6 LTE-M line. A GN&T VP will ask 'why is this ours?' in the first 10 seconds of Q&A. *Fix:* Re-anchor the value on a cost line GN&T owns: lifeline lines are the lines a field team cannot cut blind, so they keep a wire center open. Do labeled arithmetic on Verizon's own 2022 figure ($180M/yr from 36 COs is about $0.4M per CO per month, an average and not a saving we claim). Then make the proof exist only on Verizon's path: built from Verizon's own call records and its POTSolve-exclusive channel. The claim becomes 'the lifeline you migrate with Verizon arrives with a receipt', not 'HELP works better on Verizon'.
- **fatal**: The person-vs-machine classifier, which carries the hero, only works on its own synthetic template. Its 'person' rule needs speech, then at least 2 s of silence. I probed answer.py, 25 trials per case, script at /tmp/claude-0/-home-user-verizonsmartcampus/ac4afb2e-cdc2-53a2-a8f3-1a6a3e0d44b6/scratchpad/gen4/vp_probe.py. Every realistic case came back IVR, i.e. FAIL: (a) an operator who hears a silent car and keeps talking ('Hello? Can you hear me? If you can't speak, press a button'), 25/25 IVR; (b) a recorded 'this call may be recorded' preamble followed by a live person, 25/25 IVR; (c) a 2-wire tap where the car phone's own location message overlaps the greeting, 25/25 IVR; (d) the trapped rider talking into the operator's pause, 25/25 IVR; (e) an intercept with no SIT tones, 25/25 IVR. Test presses happen with an empty, silent car, which is exactly when real operators keep talking. So the product raises false alarms on healthy answerers. Separately, a high-impedance voltage bridge on a 2-wire loop hears both directions summed. It cannot isolate 'the answerer's audio' as the dossier claims. The '100% person-vs-not' figure is an artifact of the synthetic data. *Fix:* Run media checks only where the directions are separate: the 4-wire/RTP side inside the gateway ATA, or a Verizon One Talk test leg. On test calls, replace the 'pause after greeting' rule with a challenge-response. The call announces 'test call, press 1 and the car ID', and a person responds within N seconds while a machine does not. ASME Interpretation 13-1022 allows automated testing. For the retrofit tap, add a clamp-on current sensor and use V+I as a hybrid, or demote the tap to bench-only. Rebuild Gate A on real answerer behavior: teammates must not be coached to pause, and include recorded preambles and talk-to-silence greetings.
- **major**: The 'production runs in Verizon's network' story is either trivial or impossible. Dialed number vs registry, answer time and release cause (404/410, 486, 408/480) are already in every Verizon CDR. A VP will call that a query, not a product. The part that is actually new, person vs voicemail, cannot come from signaling: voicemail answers with 200 OK exactly like a person. And Verizon will not run media inspection on customers' emergency calls in its core. So the novel logic lives in a student box or partner firmware, and Content credit reduces to a BPC100 plus an LTE-M telemetry line. 'SIT detection by default on real calls' is media analysis too, so it sits behind the same counsel gate the dossier puts on audio. *Fix:* Claim the CDR layer honestly as the Verizon-native production piece: an opt-in Lifeline flag; real calls checked from records only, with zero hardware and no media; consented use under 222(c)(1). Add the check only Verizon can do: compare the E911/registered dispatchable address Verizon holds for each BPC100, One Talk or POTSolve lifeline line against the owner's building and car registry. Tie it to DA 26-1042, where missing location misrouted calls, framed as Verizon doing it right. Person-vs-machine becomes a scheduled challenge-response test call originated from Verizon's side.
- **major**: The video's lead anecdote and the biggest fault classes in the team's own data are the ones the automation cannot see. 'NASHVILLE, TN' appeared on the answerer's screen, probably from a caller-ID or ANI lookup. The tap never sees that screen. WHO ANSWERS catches it only through a cooperative monthly 10-second human confirmation, which is today's manual test with a form. Chicago's named faults are mostly location/car ID (169) and dialing 911 (105). The three automated FAIL verdicts staged on camera (voicemail, not in service, old contractor) total about 6 of 6,725 inspections (4 voicemail, 2 old contractor, about 0 vacant), roughly 0.1%. '1 of 4 reached a person' is staged drama built on the rarest faults. *Fix:* Re-weight the demo to match the data. Make location the hero fault: the answerer's challenge-response returns the car ID, and it is compared with the registry and with Verizon's registered address. Show dialed-vs-registry as the second fault and voicemail as one of four at most. Caption the bench 'faults staged by the team; none caused by the network'. Say on screen that the Nashville-type fault is caught by the scheduled answerer confirmation, not by passive listening.
- **major**: Rutgers may have no Verizon exposure for elevator lines. OIT runs 'Analog, Emergency' voice over Rutgers-owned copper. The main numbers sit on PAETEC/Windstream. Fire communicators (2020) and blue lights (2023) are already off copper. Kings III, named in the standard, sells its own cellular phones and dispatch. Elevator phones could plausibly sit on OIT analog ports of the Cisco/Teams system or on vendor cellular. In that case 'where the elevator line meets Verizon's copper-replacement voice path' does not exist at Rutgers, and the campus half becomes a PBX audit. Gate E (Dec-Jan) answers this after the video is already locked. *Fix:* By Oct 24, ask OIT one question: are elevator phones on OIT analog ports, a Verizon B1 or vendor cellular? Write the script to be true under all three answers: 'every elevator line is moving: off copper, off the old campus system, to new contractors, and the move is when nobody checks.' Treat the Teams Phone and Cisco migration and contractor changes as 'move' events too. Never show the Verizon path as Rutgers' path until the registry or the OPRA response confirms it.
- **major**: The video risks embarrassing the sponsor. The beats run: FCC 'no longer asks a carrier to show its replacement works', then 'these lines are leaving copper ... onto Verizon's network', then a Verizon line where 3 of 4 calls fail. That implies Verizon's migration causes failures, yet none of the staged faults involves the network. GN&T leadership pushed for the 26-19 deregulation, so 'the rules stopped checking' reads as a jab at Verizon's regulatory win in a Verizon-run contest. 'Some of those gateways carry a rival's SIM' points at a channel weakness on camera. The bench elevator phone sits on a BPC100, which Verizon does not market for elevators: 3 AA cells, 3 h talk against A17.1's 4 h standby power, and Inseego says it cannot place medical-alert calls. A VP sees an unsupported configuration of Verizon's product in a public video. The 'green light' experiment is openly hunting for a BPC100 defect. *Fix:* Recast the FCC beat with 26-19 para 31: 'the FCC now trusts carriers to get this right: we encourage carriers to... Here is how Verizon proves it.' Add a 'staged faults' caption. Call the BPC100 'a Verizon voice line on our bench' and say production rides POTSolve. Drop the rival-SIM line from the video and keep it for Q&A. Frame the green-light experiment as validating the gateway's own supervision, and share it with Verizon before publishing anything.
- **major**: The posted-number census is invalid and reputationally dangerous. (a) Calls come from a student cellphone, so no answerer could 'know the building'. The location metric is meaningless. (b) The 24/7 numbers posted at Rutgers elevators are most likely KONE, Otis or TK dispatch (Rutgers' own vendors) or after-hours lines that forward to RUPD/RUSSECC. Overnight survey calls to emergency dispatch read as prank-calling emergency services to a CIO and a Verizon VP. (c) LERG data from localcallingguide gives the block holder, not the current carrier, because of number portability. Network-planning judges will catch 'classify by carrier from LERG' at once. The daily 'pre-answer probe' also rings an answering point every day and abandons the call, which emergency centers treat as an operational burden. *Fix:* Cut the overnight census calls. Keep the photo-and-numbering census, labeled 'block holder (LERG), not current carrier', or buy LRN/LNP dips. Take answerer data only from the pre-announced HELP audit, or from numbers whose owners agreed in writing. Replace the ringing probe with a number-status/LRN lookup, which needs no call.
- **major**: Partners and existing practice cover much of the space. Where Kings III or an OEM center (OTISLINE) is the answerer, the center is staffed by definition and runs periodic auto-test calls into itself. The old-contractor and voicemail failures barely exist there. EN 81-28 has required test calls through the real path to the rescue service every 3 days for about 20 years. Answering-machine detection and SBC SIT detection are commodities. The real addressable segment is owner-answered phones (security desks, campus police, front desks) and contractor-change events, which is far narrower than 'every HELP call'. *Fix:* Name the segment and the trigger: owner-answered fleets (universities, hospitals, housing authorities) at contractor changes, line migrations and PBX moves. Position the check as the US equivalent of the EN 81-28 test call, made answerer-aware and logged. Leave the 'nobody does this' framing out of the video.
- **minor**: The on-camera 'live Verizon intercept', the one beat that answers the 'not Verizon's network' critique, may not happen. On VoLTE an ATA such as the BPC100 often turns a SIP 404/410 into a local reorder tone at the FXS port instead of passing the network announcement through. Mobile-network intercepts frequently carry no SIT, and the probe shows that a SIT-less intercept classifies as IVR, not 'NOT IN SERVICE'. Newly cancelled numbers may also be held in aging with varying behavior. *Fix:* On day 2 or 3, call a known-vacant number from the BPC100 and record exactly what reaches the port before any filming. Add reorder-cadence detection. Label the verdict with whatever the port actually receives ('network: number not in service' vs 'box: reorder'). If the intercept does not come through, say so and use the SIP/CDR release cause as the Verizon-network evidence.
- **minor**: The video is too dense. Eight beats and five sources (Chicago, News12, the ASME clause, the FCC CFR caption, the channel diagram) land before the Rutgers number, two code clauses sit in the first 47 seconds, and every number needs a caveat. The Dean and Vice Provost will not absorb it. The 'AI' in Pillar 1 is a hand-tuned 7-class threshold tree, and a technical judge will notice. *Fix:* Use five beats: elevator cold open, one Chicago record, one press with two screens ('Phone: CONNECTED' vs 'Answer: voicemail / wrong car'), the Rutgers number, the Verizon ask. Move the code and FCC text to the poster. Either train a small model on the Gate A real-call features and the challenge-response timing, or call it automation instead of AI.
- **minor**: Schedule and safety slack is thin. A used elevator phone ships by mail. Facilities must approve filming inside a car, and a HELP audit needs RUPD, RUSSECC and the answering point, which is unlikely within 18 days. Gate B needs a proper isolation design for 90 Vrms ring on top of 48 VDC battery. Gate C falls back to the walk audit, the only Rutgers data with no permission risk, so the Rutgers card may hold only vendor counts and lit jewels. *Fix:* Request the filming and HELP-audit approvals on day 1. Make the lit Communications Failure jewel count plus the vendor and car-ID inventory the guaranteed Rutgers number. Report any lit jewel to Facilities the same day and say so in the video. Treat the HELP audit as Feb 3 poster data, not video data.

**What it must become:** To win, this has to become a Verizon cutover-acceptance check that keeps the elevator as its human face: 'SAME ANSWER: every lifeline Verizon moves arrives with proof that HELP still reaches the right person.'

(1) Hero object and place: unchanged. A Rutgers elevator cold open, then one press on the bench with two screens, 'Phone: CONNECTED' vs 'Answer: voicemail' or 'Answerer sees: wrong car'. Caption the bench 'faults staged; none caused by the network'.

(2) Product, three layers, with no media on real calls and no box in the machine room:
- (a) Before a lifeline line moves (copper B1 to POTSolve, One Talk or BPC100), Verizon's own records give the line's baseline: where HELP calls go and how fast they are answered. This is consented CPNI use, run inside Verizon; students never touch it.
- (b) The replacement must reproduce that baseline on a scheduled test call originated from Verizon's side (One Talk). It must reach the same answerer number, get a challenge-response ('test call, press 1 and the car ID') from a live person within 45 s, and match the E911/registered dispatchable address Verizon holds for the gateway against the owner's building and car registry. That last check is the fault class behind 'Nashville' and DA 26-1042, and only Verizon holds the record.
- (c) After cutover: a monthly re-proof, plus a record-only watch on real calls for an unregistered dialed number, a vacant-number response or no answer within 45 s, with tickets routed to Verizon, the contractor, the answering point or Facilities.
The machine-room tap becomes bench-only proof that the same logic belongs in POTSolve firmware ('exclusive to Verizon'). That makes the receipt a Verizon-only asset, which is the honest reason to stay Verizon-primary.

(3) Fix the classifier: replace 'pause after greeting' with challenge-response timing, run media only on the 4-wire/RTP side, and calibrate Gate A on real answerer behavior: talk-to-silence greetings, preambles, intercepts with no SIT.

(4) Value in GN&T's own terms: lifeline lines are the lines field teams cannot cut blind, so they hold central offices open. Show labeled arithmetic on Verizon's $180M from 36 COs (about $0.4M per CO-month, an average and not our saving). The receipt replaces a second visit and becomes the per-line record a regulator or owner asks for. Drop the rival-SIM retention claim and the $9.99 add-on from the video.

(5) Rutgers: ask OIT by Oct 24 which path the elevator lines take. The guaranteed number is the walk audit (vendors, posted car IDs, lit Communications Failure jewels, each reported to Facilities the same day). The pre-announced HELP audit with Facilities is poster data. No overnight census calls, and LERG is labeled 'block holder'.

(6) Politics: open the FCC beat with 26-19 para 31 ('we encourage carriers...') and close with 'Verizon proves it'. Never imply the migration caused a failure.

Done this way, it combines the best emotional story in the pool with a GN&T-owned cost line and a check only Verizon can run, for an estimated 78-80. As written, it is a well-researched student box that a VP can dismiss as 'carrier-agnostic, synthetic-only, and partly a CDR query', at about 66.

### Red team (rival_and_feasibility): fixable, 67/95

- **fatal**: The hero classifier cannot work on a passive 2-wire tap. A bridge on the gateway's analog port hears both directions added together. Viking's own K-1600-EHFA page says the phone 'can be programmed to automatically deliver a digital announcement to identify the location' when the call is answered, so the first seconds after answer are the phone's own speech. I ran answer.py's classify() with that mixing (script: /tmp/claude-0/-home-user-verizonsmartcampus/ac4afb2e-cdc2-53a2-a8f3-1a6a3e0d44b6/scratchpad/gen4/redteam_f2/two_wire_mix.py). A real person answering while the car plays a 5-7 s location message was labelled IVR 20 of 20 times. A person with the rider talking over the greeting was labelled correctly 9 of 20 times. A person behind a 3 s hold message was labelled IVR 19 of 20 times. Voicemail stayed correct. The 100% and 95.4% figures come from a generator and thresholds that were designed together on far-end-only audio. Gate A will fail on the first day the real phone is connected. *Fix:* Classify far-end media only where the directions are already separate: gateway or ATA firmware, or the IP side. On the bench, use an open ATA or SIP leg you control alongside the BPC100 path. Otherwise cancel the commissioned location message by template and grade only after it ends. On test presses, replace passive person detection with a challenge-response: the answerer keys 1 or reads back the car ID. Measure 'seconds to first human acknowledgement' over the whole 45 s+ window, not a class label from the first 10 s. Keep the location message ON in every bench test. Never show the synthetic 100% again.
- **major**: 'For every HELP press it checks whether a person picked up' contradicts the dossier's own default of signaling only on real calls. SIP 200 OK and answer time look the same for voicemail, an IVR, an ACD queue and a person. On real calls the system can catch only a wrong dialed number, vacant/SIT, busy and no answer. It cannot catch voicemail, a slow human or a wrong label. A professor reading the one-liner, the script and judge answer 4 side by side will see the contradiction. *Fix:* Say it precisely: 'every scheduled test press is graded end to end; every real press is checked for route and answer.' Full grading of real calls waits for Rutgers counsel (Gate F). Rewrite the one-liner and the 0:47 narration to match.
- **major**: Code-permitted automation would be graded as a failure. ASME Interpretation 13-1022 says automated routing may 'validate and expedite emergency calls prior to establishing two-way voice communications'. Answer 6 lists voicemail and answering machines as automated answering systems, but says a PBX routing the call to the next available person is not one. An IVR or queue front-end in the first 10 s is therefore not a violation. The demo's '"OLD CONTRACTOR" MENU = FAIL' teaches judges the wrong rule and would false-alarm compliant monitoring centers. *Fix:* Use one rule: FAIL only if no human acknowledges within the benchmark window, or the call ends at voicemail, an intercept or a wrong number. Make the old-contractor card fail on the registry mismatch, not on 'menu'. Cite 13-1022 on the poster to show code fluency.
- **major**: The demo dramatizes the rarest faults in your own evidence. Re-running chi_recount.py on the 1,754-row comment pull gives 4 inspections naming voicemail or an answering machine (2 are the same building, re-cited) and 2 naming the previous provider, out of 6,725 inspections, about 0.1%. 72-73% are generic 'repair emergency phone', most likely car hardware, and WHO ANSWERS does not test the speaker. The most common named fault is the location or ID message (168-169, plus Nashville), which the tap cannot check automatically. The script's 'voicemail' regex also matches RECORDING, which inflates the count to 10 with location-recording citations. Counts drift between filters (1,613 vs 1,721 inspections; 313 vs 346 route/location). With 3 of 4 hero cards machine-answered, a faculty judge will infer a prevalence the data does not support. *Fix:* Lead with identity and location faults and say plainly that voicemail and old-contractor faults are rare in Chicago (6 of 6,725 inspections). Fix the regex and publish one count with its filter. Rebalance the bench cards toward location: 'person answers, but sees the wrong building', '2 a.m. voicemail at the right number', 'old contractor (registry mismatch)'.
- **major**: The location check is not automated. In code, check_call() receives label_shown as a string argument, and the console is a canned replay of synthetic results. In production, the monthly check needs the answering center to press 1. The Nashville text in the Chicago record is the operator's prompt, which a machine-room tap can never see. On camera, 'Demo Building, Car 2 confirmed PASS' will be a teammate saying it, and Verizon engineers will ask how the box knows what the operator's screen shows. *Fix:* Make the mechanism real and tied to migration. Build your own Asterisk 'monitoring center' that looks up the building by caller ID, as receiver-side test processing does (Kone US10129390). Then move the bench line to a gateway with a new number: the screen shows UNKNOWN or a wrong city. Add an ANI-continuity check (old vs new number at cutover), which Verizon's migration order can actually run. Label the answerer read-back as a cooperative protocol, not automation.
- **major**: The Verizon value argument does not follow. The faults detected (wrong number, voicemail, unstaffed or slow answerer, wrong label) belong to the owner, contractor or answering point and say nothing about the carrier. The same check on MarketSpark's AT&T SIM yields the same proof, so 'proof keeps the lifeline on Verizon' is a non sequitur. The production placement also mostly misses Verizon's network. POTSolve voice rides Verizon LTE data to a voice platform whose identity is UNVERIFIED. The Verizon voice products in the plan (BPC100, One Talk) are not marketed for elevators. So the real product is CSG or MarketSpark firmware, and Content (15) drops. At $2.4M a year per 10k lines, network-planning judges will call it a partner feature. *Fix:* Make it a Verizon process and exclusive feature. (a) Add a before/after test step to Verizon's own migration of business lines (WC 26-228, authorized on or after Oct 23; Verizon's spokesperson says 'teams ... test everything before that copper is disconnected'). (b) Enforce ANI continuity or registry notice at the migration order. (c) Offer it as a POTSolve-exclusive feature, so retention comes from exclusivity, not from 'proof'. (d) Add Cutover Watch as the rollup for Global Networks & Technology. Value = fewer failed cutovers and repeat visits. Keep the CFO formula, but put avoided failed cutovers first.
- **major**: Nothing Rutgers collects by Nov 8 measures elevator HELP. The walk audit is an inventory. The posted-number census calls building signage numbers, not elevator programming, and LERG shows who holds a number block, not today's carrier (ports, forwarding). 'Called [K] posted twenty-four-hour numbers overnight' next to an elevator invites 'did you press one Rutgers HELP button?', and the answer is no. Overnight calls to 24/7 lines may forward to RUPD or RUSSECC, breaking your own rule. Grading staff answer behaviour may need an IRB determination. An OPRA request for programmed destinations is likely to be withheld as security information. Facilities, RUPD and contractor approval in 9 days under a hiring freeze is unlikely, so Gate C will probably be met only by the proxy data. *Fix:* Put all the relationship capital into one ask: a Facilities-approved, pre-announced HELP press on 1-3 cars, ideally at night, filmed and graded live (n=1 of real HELP beats n=40 posted numbers). Cut the overnight census, or limit it to numbers Facilities approves in writing, and never present it as elevator data. Request an IRB 'not human subjects' determination this week. Present the walk audit as 'the first inventory', not as evidence of failure.
- **major**: The 18-day hardware path has several single points of failure. A used elevator phone shipped in 3-7 days lands on top of Gate A (Oct 28). The Viking spec needs '24VDC / 20mA minimum' loop current, which can be marginal on an ATA FXS port. The BPC100 needs Verizon Business account activation. The 'old contractor' Asterisk needs a public number (DID). A just-cancelled wireless number may play 'customer unavailable' rather than an intercept with SIT tones. 40 calls at about 10 per class is too few: 38 of 40 correct has a 95% confidence interval of roughly 83-99%, which cannot show '≥95%'. Midterms take people away. *Fix:* Order today with expedited shipping and two different phone models. Measure loop current on the first evening. Keep a 555-01XX or unassigned-number intercept as a fallback. Automate presses with a bench relay across the HELP contacts to get 200+ calls overnight. Publish the confusion matrix with confidence intervals. If the phone has not arrived by Oct 26, switch to the box hero without debate.
- **major**: What breaks on stage at the Feb 3 poster: a hands-free speakerphone in a loud hall sends crowd noise onto the same two wires, and the teammate 'person' answering beside the table hears background talk, which skews the person/IVR labels. VoLTE in a crowded indoor venue can be slow or fail. Each press-and-verdict cycle takes 30-60 s, so four destinations outlast a judge's visit. The 'Nashville' fault switch changes the phone's message, while Chicago's case was the operator's screen, and a judge who read the record will catch the conflation. *Fix:* Test signal in the venue in January. Put the person answerer in a quiet room on a headset. Give each judge one press. Keep a recorded fallback clip of each verdict. Rename the fault switch 'caller ID changed at cutover' and make it drive the Asterisk center's screen.
- **major**: The daily pre-answer probe would ring a 24/7 emergency answering point and hang up every day. At a PSAP such as RUSSECC, abandoned calls are routinely called back, so this creates daily phantom-call work. One Talk cannot place a call and release it before answer. *Fix:* Drop it. Use number-status and registry checks that do not ring anything, plus cooperative scheduled test calls the answering point opts into.
- **minor**: The FCC 63.602 beat (13 s) is not causal. The removal is real and effective Oct 15 (WCB DA 26-1061), but 63.602 never covered elevator phones. The dossier also admits no documented case links an elevator phone failure to a copper cutover, and none of the bench failures are caused by migration as shown. Judges will read it as copper bolted onto an elevator story. *Fix:* Shrink it to one caption, or replace it with the migration mechanism you can show (caller ID or dialing program changes when the line moves). Spend the 13 s on the real Rutgers press.
- **minor**: Installing the tap is not 'nothing installed': it is a non-listed device attached to a partner gateway's port on an emergency circuit. That may void the listing or warranty, may count as altering emergency signaling (minor work) under the NJ code, and reading dialed digits on real calls raises pen-register and NJ wiretap questions beyond 'features only'. *Fix:* Keep the tap bench-only. The pilot goes through the gateway partner's firmware or the Rutgers codes office. Get counsel review before reading digits or audio on any real call.
- **minor**: Uniqueness is fine: no crowd entry touches elevators, and the A17.1 clause plus the Oct 2026 Chicago record plus WC 26-228 need live research. The real competitive risk is the judges, not rival teams. A network-planning panel scores this as a partner accessory, and a CIO judge may hear 'Rutgers HELP may ring voicemail at 2 a.m.' as criticism of her office. *Fix:* Co-present with Facilities and OIT, for example a quote from Facilities or the codes office on the poster, and frame every Verizon element as a cutover-process step, not a gadget.

**What it must become:** WHO ANSWERS must stop being a passive voicemail detector and become the before-and-after receipt for each elevator line that leaves copper.

(1) Hero: one real, Facilities-approved, pre-announced HELP press on a Rutgers car at night, graded live on screen. It shows the number dialed vs the registry, seconds to the first human acknowledgement, and the answerer reading back the car ID. Even 1-3 real cars beat any proxy census.

(2) Bench: the same elevator phone moves from a 'copper' line to a Verizon gateway, and the receipt shows what the move changed:
- the calling number, so a caller-ID-keyed answering screen (your Asterisk 'monitoring center') shows UNKNOWN or a wrong city. This makes the Nashville case mechanistic and ties failure to migration honestly;
- the dialing program;
- whether the location message survives;
- loop current against the phone's 20 mA minimum;
- answer time.

(3) Detection that works on real hardware:
- test presses use a challenge-response (answerer keys 1 or reads back the car ID) and 'time to human' over the full window;
- real calls are signaling only (digits, SIT/SIP, answer time);
- any spectral classification runs on far-end media in gateway firmware or on the IP side, never on a 2-wire bridge. It must be tested with the location message on;
- an IVR or queue front-end is not a failure (ASME 13-1022);
- publish a real-line confusion matrix with confidence intervals over 200+ automated bench presses.

(4) Verizon: a test step inside Verizon's own business-line migrations (WC 26-228), plus a caller-ID continuity check at the migration order, a POTSolve-exclusive feature, and a Cutover Watch rollup for Global Networks & Technology. Value is fewer failed cutovers and repeat visits, plus retention through exclusivity, not 'proof keeps lifelines on Verizon'.

(5) Numbers discipline:
- lead with identity and location faults (about 10% of phone-cited Chicago inspections, plus Nashville);
- state that voicemail and old-contractor faults are rare (6 of 6,725 inspections);
- drop the synthetic 100%;
- cut the FCC beat to one caption;
- drop overnight calls to posted numbers unless Facilities signs off in writing, and never present them as elevator data.

Done this way it scores about 78-82. As written, the first real phone on the bench breaks the hero claim.
