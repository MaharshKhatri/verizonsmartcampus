# Judge Q&A bible (PROVE)

Answer in two sentences, then offer the evidence. Never argue against the sponsor. Every claim below has a source in `research/06_gen4_verification.md` or `research/sources/`.

## Verizon (strategy, network planning, business)
**1. "Our technicians already test everything before the copper is cut."**
Then PROVE is that test, automated and receipted, so it also happens on mail-in swaps and self-installs. Verizon's Voice Connect terms say a technician visit confirms the jacks and coverage at the box. Alarm and medical compatibility "is determined by your testing ... at time of install", and the swap guide's only check is "make a test call".

**2. "Device management already sees battery and signal."**
Good. PROVE uses that telemetry. What telemetry cannot see is whether the alarm's message reached the receiver intact and was acknowledged. That in-band proof is the part the FCC encouraged carriers to get right.

**3. "Why is this ours? Inseego could ship it."**
The firmware is the easy part. The Verizon-only pieces are:
- the measured matrix from our bench;
- a Verizon-hosted IMS test receiver;
- the migration-batch rollup (Cutover Watch);
- the order and dispatch integration.
Each green receipt keeps an alarm household on Verizon at a moment when it could pick cable VoIP.

**4. "The technician visit is also for the 911 address and liability."**
Then PROVE triages the visit rather than replacing it. The receipt can show the registered service address for the customer to confirm. Verizon already self-installs the Voice Gateway, whose 911 address is the service address given at signup. Whether to skip a visit is Verizon's policy call; we supply the evidence.

**5. "What's the money?"**
We don't invent dollars. Value = avoided visits and avoided care contacts × Verizon's own loaded costs, on four KPIs it already tracks:
- first-time-right;
- repeat dispatch within 30 days;
- care contacts per install;
- alarm households confirmed working.
Verizon reports about 46,000 fixed-wireless replacement customers, and two 2026 filings cover about 417,000 more lines. The 30-day trial against a control group gives the real number.

**6. "Isn't this a gotcha about our box?"**
No. Verizon's own guide already tells customers to test their alarm, and we made that one button. Every failure we measure goes to the Verizon mentor before any poster.

**7. "Alarm companies are moving panels to cellular communicators."**
True, and good. PROVE is for the households still using the box's alarm port, which is exactly where Verizon carries the risk. As that number shrinks, the same engine covers voice, signal and battery, and elevator HELP lines.

**8. "A kiss-off isn't proof of delivery."**
Correct, which is why PROVE requires three things: the handshake, a checksum-valid message and the kiss-off. The alarm company also confirms the test event on its side, as it does today.

**9. "Does it work with SIA or 4/2 panels?"**
Inseego's guide says the box supports Contact ID only. We report what we measured. Our lab receiver decodes Contact ID only, so we make no claims about SIA.

**10. "Medical alerts?"**
Verizon's documents differ on medical-alert support, so we claim nothing. The receipt reads "not tested" unless the monitoring company books a test window. We never trigger a real dispatch.

**11. "What about the FCC?"**
On the record: in FCC 26-19 the Commission declined alarm-compatibility conditions and "encourage[s] carriers ... to prevent alarm signaling failures". PROVE is how a carrier shows it did, home by home. It is voluntary and Verizon-led, not a compliance claim.

## Rutgers (CIO, Dean, Vice Provost)
**12. "Why is this Smart Campus? What does Rutgers get?"**
- A Rutgers PROVE Lab in ECE that publishes measured alarm-over-carrier data nobody else has.
- A usability service for older New Jersey residents at the moment their landline is replaced.
- In the final, an elevator HELP pilot co-signed by Facilities, using a challenge-response test call.

**13. "Are Rutgers' own lines at risk?"**
We are not claiming that:
- Rutgers moved fire communicators off phone lines in 2020 and blue lights in 2023.
- Its main voice service runs on its own system.
- Which elevator lines ride which carrier is OIT's to confirm, and we asked.
Rutgers is the proving ground, not a countdown.

**14. "Where's the AI?"**
Three places, each with its error rate:
- **A learned SIGNAL threshold.** A logistic model maps the box modem's SINR/RSRQ to the probability that an alarm is delivered on the first try, with bootstrap CIs (`prototype/prove/signal_model.py`). On modelled data it gives about 10 dB SINR for 90% first-try delivery (CI 8.6-11.5). It is refit on bench data, and that refit is the number we would quote.
- **Fault triage** that routes each failure to its owner. Routing accuracy is 92% in simulation and 87% when our symptom assumptions are wrong by ±15 points.
- **Plain-language fix instructions** for each failed line. These are rule-based today; an LLM rephrasing step is planned, not built.

**15. "Isn't the 'who answers' detector the part that failed?"**
Yes, and we say so. Passive detection works on clean audio but fails on a 2-wire line when the car plays its location message: 0% of real people recognised with an 8-second message. So the test call uses challenge-response ("press 1 and read back the car ID"), which a machine never does.

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
