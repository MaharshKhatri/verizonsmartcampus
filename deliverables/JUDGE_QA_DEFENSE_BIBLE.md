# Judge Q&A bible (PROVE)

Answer in two sentences, then offer the evidence. Never argue against the sponsor. Every claim below has a source in `research/06_gen4_verification.md` or `research/sources/`.

## Verizon (strategy, network planning, business)
**1. "Our technicians already test everything before the copper is cut."**
Then PROVE is that test, automated and receipted, so it also happens on mail-in swaps and self-installs. Verizon's Voice Connect terms say a technician visit confirms the jacks and coverage at the box. Alarm and medical compatibility "is determined by your testing ... at time of install", and the swap guide's only check is "make a test call".

**2. "Device management already sees battery and signal."**
Good. PROVE uses that telemetry. What telemetry cannot see is whether the alarm's test call was answered and acknowledged. The FCC encouraged carriers to prevent alarm signaling failures, and PROVE is how a carrier can show it did, home by home.

**3. "Why is this ours? Inseego could ship it."**
Phase 1 needs no firmware at all: technicians carry a pocket PROVE tap on alarm installs. The firmware in Phase 2 is the easy part. The Verizon-only pieces are:
- the measured results from our bench;
- a proposed Verizon-hosted IMS test receiver;
- the migration-batch rollup (Cutover Watch);
- the order and dispatch integration.
A forced migration is a moment a household can leave, and a green receipt gives an alarm household a reason to stay.

**4. "The technician visit is also for the 911 address and liability."**
Then PROVE triages the visit rather than replacing it. That is why a GREEN receipt says "no visit requested", not "no visit needed". The receipt can show the registered service address for the customer to confirm. The Voice Gateway is already a customer self-install, and its 911 address is the address given at signup. Whether to skip a visit is Verizon's policy call; we supply the evidence.

**5. "What's the money?"**
We don't invent dollars. Value = avoided visits and avoided care contacts × Verizon's own loaded costs, measured on install KPIs:
- first-time-right;
- repeat dispatch within 30 days;
- care contacts per install;
- one new KPI, alarm households confirmed working.
We are asking the mentor which of these Verizon tracks today.

The arithmetic needs no invented costs:
- Per 1,000 alarm installs, each 1-point drop in 30-day repeat dispatch is 10 truck rolls avoided.
- Each 1-point drop in care contacts is 10 calls avoided.

Vendor blogs put a loaded truck roll at $250-1,000, so the low end is $2,500 per point per 1,000 installs. That figure is for scale only.

Verizon told the FCC it has about 46,000 fixed-wireless replacement customers, and two 2026 filings cover about 417,000 more lines. The 30-day trial gives the real number, and its success rule is pre-registered:
- **The primary endpoint is the catch rate:** the share of alarm installs where PROVE flags an alarm failure that a plain phone call passed. It is measurable within one batch (about ±3 points at 300 installs).
- **Repeat dispatch against a matched batch is secondary, an estimate only.** A significance claim on it would take about 3,200 installs per arm, and we say so up front.

A pocket tap costs less in parts ($100-200) than one truck roll at the low end of vendor estimates.

**6. "Isn't this a gotcha about our box?"**
No. Verizon's own guide already asks customers with an alarm to test it, and we turned that into one guided check with a receipt. The customer or the alarm company still starts the panel's test, as they do today. Every result goes to the Verizon mentor before any poster.

**7. "Alarm companies are moving panels to cellular communicators."**
True, and good. PROVE is for the households still on the box's alarm port, which is exactly where the risk sits for Verizon's customers, and for Verizon's reputation with them. As that number shrinks, the same engine still covers voice, signal and battery, and the elevator HELP lines.

**8. "A kiss-off isn't proof of delivery."**
Correct, so the receipt never says "delivered". On Verizon's side, a proposed synthetic Contact ID call to a Verizon-run test receiver, which decodes it, gives ground truth for the part of the path Verizon owns. On the alarm company's side, PROVE reports only that the receiver answered, the panel sent its full code and the acknowledgement came back. It tells the customer to confirm the test event with the alarm company, as today.

**9. "Does it work with SIA or 4/2 panels?"**
Inseego's BPC100 guide says the box supports Contact ID only. Our lab receiver (Asterisk AlarmReceiver) decodes only Ademco DTMF formats such as Contact ID and Express 4+2. It cannot decode SIA or pulse 4/2, so we make no claims about those.

**10. "Medical alerts?"**
Verizon's documents differ on medical-alert support, so we claim nothing. The receipt reads "not tested" unless the monitoring company books a test window. We never trigger a real dispatch.

**11. "What about the FCC?"**
On the record: in FCC 26-19 the Commission declined alarm-compatibility conditions and "encourage[s] carriers ... to prevent alarm signaling failures". PROVE is how a carrier shows it did, home by home. It is voluntary and Verizon-led, not a compliance claim.

**11a. "How many of the 46,000 even have an alarm?"**
No filing says. As a crude range, the alarm committee's 5 million dial-out panels over the FCC's 78 million wireline voice connections is about 6%. Over the 26 million residential connections, it is about 19%. On 46,000 boxes that is roughly 3,000-9,000 households. Verizon can replace the range with an exact count: every box with an alarm number registered via ##21. That is our sixth mentor question.

**11b. "Is the demo running on our box's firmware?"**
No, and the video says so: on our bench PROVE runs on a tap at the box's alarm port. That tap is Phase 1 of the ask, a pocket device for technicians with no change to the box. Phase 2 is firmware. The box already decodes DTMF to dial, and PROVE adds a Contact ID parser and two tone detectors. `tap.compute_budget()` estimates it at about 0.17 million multiply-accumulates per second and 2 KB of detector state. That is an analytic estimate, not yet ported or measured on the box.

**11c. "You dialled in the one attenuation where voice survives and DTMF fails."**
No. We measured the whole curve and report one number, delta: how many more dB of signal Contact ID needs than a clear call.
- **The fit.** Each box is measured from its own dropout point, with logistic fits and a cluster-bootstrap CI.
- **The rig.** The box sits inside a shield box. An RSRP-vs-dial slope check proves the attenuator controls what it hears, and cell ID and band are logged at 1 Hz.
- **The trials.** Steps are 1 dB near the edge, with 20 phone calls and 20 alarm tests per step, interleaved in random order on two days. Setup failures are a separate curve.
- **"Clear" was fixed before the run:** P.862.1 MOS-LQO ≥ 3.0 in both directions, plus ≥ 9 of 10 keywords from a blinded listener, with a 3.5 sensitivity check.
- **When we call it a gap.** A box shows a gap only if delta's CI is above 0. "Same pattern on another carrier" means a gap on both boxes, never just overlapping CIs.

**11d. "Does the box send DTMF in-band through AMR, or as RFC 4733 events?"**
We measured it first (bench test T0): for each digit, we compare timing, level and frequency at the panel and at the receiver, with ##21 on and off. We also asked the mentor. The answer tells us where failures should appear:
- **In-band:** digits garbled at the receiver.
- **RFC 4733:** call setup, or the handshake and kiss-off not being heard.

`fail_stage` is logged for every trial, so the data shows which.

**11e. "Is the other carrier's box even on VoLTE?"**
We check that it is IMS-registered with a dedicated voice bearer. If it runs SIP over best-effort data instead, it isn't a VoLTE control. The poster says so, and the cross-carrier line leaves the video.

**11f. "How does a passive tap speak, or know the signal?"**
It doesn't speak through the handset. In Phase 1 the tap listens to the line. It reads signal from the box's own diagnostics (or a proxy phone on the same attenuated path, labelled as such). Prompts and the receipt go to the technician's phone and a pocket printer. Spoken prompts through the handset and automatic battery checks arrive with Phase 2 firmware, and the video labels that phase as not built.

## Rutgers (CIO, Dean, Vice Provost)
**12. "Why is this Smart Campus? What does Rutgers get?"**
- A PROVE bench in a Rutgers ECE lab, producing measured alarm-over-carrier data we could not find published anywhere.
- A usability session with older-adult volunteers. It measures whether they follow PROVE's spoken fix to a green receipt without help, reported as k of n: 3-5 now, a 20-30 person A/B study by the final.
- For the final, an elevator HELP pilot we are proposing to Facilities, using a challenge-response test call.

**13. "Are Rutgers' own lines at risk?"**
We are not claiming that. Rutgers has already done the right thing for two lifelines:
- In 2020 it moved fire communicators in 450 buildings to dual-path IP/cellular units.
- In 2023 it replaced its blue lights with solar units that report their health daily.

Elevator HELP phones are the lifeline that still has no routine proof that someone answers, and PROVE adds it. Which elevator lines ride which carrier is OIT's to confirm, and we have asked. Rutgers is the proving ground, not a countdown.

**14. "Where's the AI?"**
The go/no-go signal line is learned from our own lab alarm tests, not set by hand: it is how strong the signal must be for an alarm to get through first time nine times in ten, with a margin of error. In detail, AI shows up in three places, each with its error rate:
- **A learned SIGNAL threshold.** A logistic model maps the box modem's SINR to the probability that an alarm is delivered on the first try, with bootstrap CIs (`prototype/prove/signal_model.py`). On modelled data it gives about 10 dB SINR for 90% first-try delivery (CI 8.6-11.5). That figure comes from an assumed worst-case loss model (lost frames zeroed, no concealment), so it is a placeholder, not a prediction. The bench refit is the only number we would quote, and it is labelled "fitted to [N] bench alarm tests on one cell". The video shows it as "Signal bar learned from [N] bench alarm tests".
- **Fault triage** that routes each failure to its owner. Routing accuracy is 92% in simulation and 87% when our symptom assumptions are wrong by ±15 points.
- **Plain-language fix instructions** for each failed line. These are rule-based today; an LLM rephrasing step is planned, not built.

**15. "Isn't the 'who answers' detector the part that failed?"**
Yes, and we say so. Passive detection works on clean audio but fails on a simulated 2-wire tap when the car plays its location message: 0 of 15 simulated answerers were recognised as a person with an 8-second message. So the test call uses challenge-response ("press 1 and read back the car ID"), which a machine never does.

**16. "What did the students learn / build?"**
- Signal processing: matched filters, Goertzel detectors, Contact ID.
- Controlled measurement on a live carrier network, with three arms and CIs.
- Systems: an evidence ledger and a live console.
- Honest reporting of nulls.

## Safety and ethics
**17. "Could your tests trigger a real emergency response?"**
No:
- We never dial 911.
- We use only our own receiver numbers.
- Used panels are factory-defaulted before they touch a line, and the faculty sponsor signs off.
- Elevator tests are pre-announced and run only with Facilities and RUPD agreement.

**18. "Privacy / customer data?"**
None:
- The bench uses a department line.
- No CPNI.
- Usability volunteers give consent and age band only.
- Nothing is recorded on elevator calls.

## Added after the Gen 6 review
**19. "Panels send periodic tests. The alarm company would notice a missed one."**
Many do, daily to monthly. The miss then surfaces days later, as a trouble beep or a late-test flag, after the installer has gone. PROVE moves that discovery to install time, when someone is there to move the box or re-enter the number. That is why the video says the panel "may not" learn.

**20. "Did the IRB review the usability session?"**
Yes. On [date], Rutgers' IRB determined it [not human-subjects research / exempt], ref [#]. Volunteers sign consent and a photo release, and we keep counts and age band only. If the determination isn't on file, the session doesn't run and the video carries no volunteer footage.

**22. "Does your own model even say alarms fail before voice?"**
Partly, and we say exactly how. With codec concealment and bursty loss in the simulation:
- The alarm's first try drops below 90% at about 2% frame loss; voice holds to about 5%.
- The panel's retries rescue most alarms, to about 10%.

So the model predicts that weak signal shows up first as slow, retried confirmations, and PROVE treats "confirmed only after retries" as a warning, not a pass. The bench measures both margins: final and first try. The video uses whichever one the data supports.

**21. "Why should Verizon's network planners care?"**
Because delta is a margin they can apply to the address-level indoor coverage predictions already used to qualify homes for fixed wireless. It flags alarm homes near the edge before install, and PROVE never touches customer data. The mentor gets the test line's number and the UTC start of every trial, so Verizon can pull its own traces for the same calls.
