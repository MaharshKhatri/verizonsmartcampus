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

Verizon told the FCC it has about 46,000 fixed-wireless replacement customers, and two 2026 filings cover about 417,000 more lines. The 30-day trial against a control group gives the real number. Its success rule is pre-registered:
- the primary endpoint is the difference in repeat dispatch, with its 95% CI;
- detecting a 2-point drop from a 10% base takes about 3,200 installs per arm, and we say so up front.

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

**12a. "How many of the 46,000 even have an alarm?"**
No filing says. As a crude range, the alarm committee's 5 million dial-out panels over the FCC's 78 million wireline voice connections is about 6%. Over the 26 million residential connections, it is about 19%. On 46,000 boxes that is roughly 3,000-9,000 households. Verizon can replace the range with an exact count: every box with an alarm number registered via ##21. That is our sixth mentor question.

**12b. "Is the demo running on our box's firmware?"**
No, and the video says so: on our bench PROVE runs on a tap at the box's alarm port. That tap is Phase 1 of the ask, a pocket device for technicians with no change to the box. Phase 2 is firmware. The box already decodes DTMF to dial, and PROVE adds a Contact ID parser and two tone detectors. `tap.compute_budget()` estimates it at about 0.17 million multiply-accumulates per second and 2 KB of detector state. That is an analytic estimate, not yet ported or measured on the box.

**12c. "You dialled in the one attenuation where voice survives and DTMF fails."**
We stepped the attenuator in 2 dB steps across the whole range, on Verizon's box and another carrier's box at matched SINR. "Clear" was fixed before the run: PESQ (ITU-T P.862) of at least 3.0, or a blinded listener getting at least 9 of 10 keywords. `scripts/analyze_prove_lab.py` prints every step and flags the gap steps, where calls are clear but alarms are under 90%. The full sweep is on the poster. If the other carrier's box had not shown the same gap, the number would not be in the video.

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
Three places, each with its error rate:
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
