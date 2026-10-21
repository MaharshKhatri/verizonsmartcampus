# PROVE Lab bench protocol: one real, measured result before Nov 8

**Why:** every judge persona said the same thing. The pitch is only as strong as one failure (or one clean pass) measured on Verizon's real copper-replacement box. Verizon's own documents disagree about what this box supports:

| Topic | Inseego BPC100 guide | Verizon documents |
|---|---|---|
| Medical alerts | "cannot be made" | Voice Connect guide: supports "most" |
| Personal monitoring | | Voice Connect ToS: "not compatible with ... personal monitoring services" |
| Fax | User guide lists fax support (an Inseego quick-start sheet reportedly says otherwise; unverified) | Verizon recommends 9600 bps, ECM off |

Only a bench can settle it. Everything below is safe, legal and doable by two students in a week. **Never dial 911. Never send test signals to a real central station or medical-alert company without its written OK.** We run our own receiver.

## 1. Bill of materials (about $1,200-2,000; order Oct 22)
| Item | Why | Est. cost |
|---|---|---|
| Verizon Business Phone Connect, Inseego BPC100, on a Verizon business voice line (a department or faculty account) | The real box Verizon ships to homes as 2nd-gen Voice Connect | $129.99 + line ($20-35/mo) |
| A second BPC100, or a used T2050 (1st-gen Voice Connect) | Swap test: do ##21 registrations survive a box swap? | $40-130 |
| Raspberry Pi 5 + USB sound card + FXO/ATA (Grandstream HT813 or Obi) | Our own "central station" and test responder: Asterisk AlarmReceiver, SpanDSP fax, tone/echo responder | $150-200 |
| A second phone line for the receiver: a One Talk line or any SIP DID routed to the Pi | The number the alarm panel dials | $5-20/mo |
| Used alarm panel with a Contact ID dialer (DSC PowerSeries / Honeywell Vista 20P) + keypad + 16 V transformer | Real alarm traffic | $60-150 (eBay) |
| Optional: a panel that can be set to SIA or 4/2 | Tests the "Contact ID only" footnote | $60 |
| Used PERS base (Philips Lifeline / MobileHelp landline unit), only if it can be pointed at our own receiver number | Medical-alert path, if programmable; otherwise skip | $30-80 |
| Old fax machine or USB fax modem | Fax claims | $30 |
| Corded analog phone, butt-set or RJ11 splitter, line tap with isolation transformer | Listening and DTMF | $40 |
| ThingSpace self-serve LTE-M dev kit (nRF9160 DK or similar) + $1.50/mo plan | PROVE reporting path, independent of the line under test | $150 |
| Phone with a field-test app (Android: Network Cell Info / NetMonster) | RSRP/RSRQ/SINR at each placement | (own) |
| **Another carrier's LTE voice line with an RJ11 port**: preferably an unlocked LTE-to-FXS voice gateway with an AT&T or T-Mobile SIM, one prepaid month | The second-network control at matched SINR. It is the only thing that lets the video show the weak-spot counters without implying Verizon's box is worse. AT&T's own wireless home-phone base says it does not support home security systems, so use it only as a last resort and say so on the poster. | $80-200 + $20-30/mo |
| **2-channel USB-programmable attenuator** (0-60 dB or more, 0.5-1 dB steps; or two identical units driven by one script), plus SMA cables, bulkhead adapters and two small antennas | Repeatable, software-logged "weak spot" for the sweep (T5). Inseego lists "2 SMA connectors for external antennas" on the BPC100, so both MIMO branches are attenuated within 0.5 dB of each other. | $200-450 (used) |
| Relay board (4-channel) for the Pi | Fires panel test events unattended and switches the line between the panel and the HT813 FXO for voice trials, so the sweep can run overnight | $15 |
| **RF shield box** (tabletop) with SMA bulkheads and filtered RJ11/power feedthroughs | The box sits **inside** with its antennas outside, so it hears only what passes the attenuator. Before each session, an RSRP-vs-dial slope check proves there is no leakage. | $150-400 (used) |
| Harvard-sentence recordings (8 s, P.56 level −26 dBov) plus an open-source ITU-T P.862.1 scorer | The objective "clear" rule (MOS-LQO ≥ 3.0 both ways and ≥ 9/10 keywords), pre-registered. The mentor may rescore the WAVs with P.863. | $0 |
| **Pocket PROVE tap** (Raspberry Pi Zero 2 W or Pi 5, USB sound card, isolated line-recording adapter, RJ11 splitter, USB-C battery, small case) | The Phase 1 ask, built and filmed: our decoder on a real line | $85-170 |
| Lithium and alkaline AA, a kill-a-watt or USB power meter, a stopwatch | Battery runtime | $25 |

## 2a. Control arms (required: report differences, not absolutes)
The call path is long: panel -> box -> Verizon VoLTE/IMS -> interconnect -> our SIP DID provider -> Asterisk. Any leg can mangle 50-60 ms DTMF digits, so a raw "44/50" proves nothing about Verizon. Run three arms with the same panel and receiver on the same day:
- **(A) LAN baseline:** panel -> HT813 FXS -> Asterisk on the LAN (G.711, in-band DTMF). It must be about 100%; otherwise our receiver is the problem.
- **(B) Non-Verizon path:** the same panel through a different carrier's line to the same DID.
- **(C) Verizon box:** panel -> BPC100 / Voice Gateway -> the same DID.
- **Dual taps:** record at the panel's line side and at Asterisk, so a failure can be placed on a leg.
- **Receiver limits:** Asterisk AlarmReceiver decodes Ademco DTMF formats (Contact ID, 4+1/4+2) only. It cannot decode SIA FSK or pulse 4/2, so never report SIA or 4/2 "failures" from it.
- **Signal:** read RSRP/RSRQ/SINR from the box's own admin page where available. A phone beside the box is only a labelled proxy.
- **Hero device:** if orderable, test Verizon's current Voice Gateway (VG10A, customer self-install, alarm numbers in Settings) as the hero and the BPC100 as the second arm. State on screen which device was tested.
- **Stage reliability:** for the poster and the final, use SMA step attenuators on the box antennas (instant, repeatable "bad signal"), two pre-programmed panels on an A/B switch, a scripted trouble-reset, and Asterisk on a cloud VM.

## 2. Tests (each produces a row in `field_data/prove_lab.csv`)
Columns: `test_id, date, utc_start, box, firmware, placement, atten_db, pci, earfcn, band, rsrp_dbm, rsrq_db, sinr_db, sinr_p10, tx_power, device, format, account, registered_21, dtmf_transport, call_trial, pesq_up, pesq_down, listener_keywords, setup_ok, answer_s, blocks_sent, fail_stage, delivered, kissoff_s, attempts_used, wav_panel, wav_receiver, pcap, notes`.
- `fail_stage` ∈ {setup, drop, no_handshake_at_panel, digits_bad_at_receiver, no_kissoff_sent, kissoff_not_heard, none}.
- `delivered` means "the receiver logged a valid event and sent a kiss-off". On screen it is always "confirmed", never "delivered".
- The test line's number stays out of the published CSV. The mentor gets it, with the UTC start of every trial, so Verizon can pull its own eNB/IMS traces for the same calls if it chooses.

### T0. How does the box carry the panel's digits? (half a day, before T1)
The mechanism decides what "alarm fails before voice" can mean.
- **In-band:** DTMF goes through AMR-WB/EVS, and failures show up as digits garbled at the receiver.
- **RFC 4733 telephone-events:** the box detects the digits and sends events, which a gateway regenerates downstream. Failures then sit in call setup and in hearing the handshake and kiss-off.

**How to tell them apart.** Run 50 Contact ID events at 0 dB with dual taps. For each digit, compare the panel side with the receiver side: on-time, inter-digit gap, level and frequency offset.
- Regenerated digits have constant durations and levels that don't track the panel's.
- In-band digits track the panel's timing and show 20 ms frame ripple.

Repeat with ##21 on and off, and ask the mentor which mode the box uses. Record the result in the `dtmf_transport` column.

**Instrument and receiver controls, run on arm A before T1:**
- **Tap loading:** 20 events with the tap connected and 20 with it removed, logging the panel-side DTMF level. Proceed only if they don't differ.
- **Receiver configuration:** freeze `alarmreceiver.conf` and the trunk's DTMF mode, and publish both.
- **Trunk:** lock it to G.711u, 20 ms packets and in-band DTMF, or record whatever the provider forces. Capture a pcap of every call.
- **Re-decoding:** re-decode receiver-side audio offline with Asterisk default, Asterisk relaxdtmf, SpanDSP and `alarm.decode_dtmf`, and report delta under each.
- **Difference-in-differences:** analyse each box against its own 0 dB rows from the same session, so the DID and interconnect legs cancel out.

### T1. Alarm through the box, number registered (baseline)
- **Setup:** program the panel to dial our receiver number. On the BPC100, dial `##21*<receiver number>#`, then power-cycle.
- **Run:** trigger 50 events (panic, burglary, test 602), spaced 60 s apart.
- **Record:** whether each event was delivered (Asterisk AlarmReceiver logs the event with a valid checksum), the time to kiss-off, and the number of attempts.

### T2. Alarm, number NOT registered
- Run T1 again after clearing the registration (`##22*#` then `##268#`, per Verizon's guide).
- **Compare** first-try delivery and total delivery against T1.
- **This is the "Failure to verify may result in your alarm not working" claim, measured.**

### T3. The swap test (the money shot if it fails)
- **Step 1:** register the number on Box A and confirm T1 passes.
- **Step 2:** follow Verizon's own swap guide word for word: move the line to Box B and activate via 1-800-Verizon IVR as instructed. Do **not** re-enter ##21, because the guide never says to.
- **Step 3:** run 20 events.
- **Outcomes:**
  - If delivery degrades or fails: the receipt beat is "The phone works. The alarm doesn't."
  - If registrations survive (they may be stored in the network or on the SIM): report that honestly. The beat becomes "we checked; it survives", and the receipt still proves it per home.

### T4. Alarm format
- Switch the panel to SIA and then to 4/2, and repeat 20 events each, registered.
- **Measures:** Inseego's "Contact ID only" footnote.

### T5. Signal sweep: how much more margin does alarm data need than voice? (the bench beat)
This section was revised after a RAN/VoLTE engineering review. The earlier design could produce a "gap" artefact: 3 voice calls vs 10 alarms per step, a blocked monotone order, setup failures counted as alarm failures, and SINR compared across two modems.

**Pre-registered before any run** (also committed to the repo with a timestamp):
- **Primary estimand, delta**, computed on each box separately:
  - A90_voice is the attenuation at which the voice-clear rate falls to 90%;
  - A90_alarm is the attenuation at which the alarm-confirmed rate falls to 90%;
  - **delta = A90_voice − A90_alarm, in dB.**
  - Both curves are logistic fits against attenuation measured from that box's own dropout point (A_edge). The 95% CI comes from a cluster bootstrap over (date, step).
  - **A gap exists on a box only if the CI's lower bound is above 0 dB.** The video's sentence is "the alarm needed [delta] dB more signal than a clear call".
- **What "clear" means.** ITU-T P.862.1 MOS-LQO (narrowband, 8 kHz, implementation and version named) ≥ 3.0 in **both** directions, **and** a blinded listener gets ≥ 9 of 10 keywords. Also report the result at a 3.5 threshold. The mentor is asked to rescore the same WAVs with P.863 (POLQA).
- **Comparison set.** Only answered calls enter the voice-vs-alarm comparison. Setup failures and drops form a third curve, reported on its own.

**Rig check, before every session.** The box sits inside the shield box with the antenna outside. SMA runs through bulkheads to a 2-channel programmable attenuator, and RJ11 and power enter through filtered feedthroughs.
- Step 0 → max in 5 dB steps. The box's RSRP must fall 1.0 ± 0.15 dB per dB until the noise floor, and the box must lose service at maximum attenuation. Discard any step beyond the point where the slope flattens, because there the room is leaking in.
- Log PCI, EARFCN, RSRP, RSRQ and SINR at 1 Hz. If the serving cell or band changes during a step, rerun the step. Lock the band if the box allows it, and say so.

**Sweep design.**
- **Scout:** 5 dB steps until the box can't register or fails 3 of 3 call setups. That point is A_edge.
- **Fine:** 1 dB steps from A_edge − 12 to A_edge − 1, plus anchors at 0 dB and A_edge − 20.
- **Dwell:** after each change, wait 90 s and place one throwaway call. Start trials only if PCI and EARFCN are unchanged and IMS is registered. Use the in-call median of the 1 Hz readings.
- **Per fine step:** 20 voice and 20 alarm trials, interleaved in a randomized V/A order.
  - Voice trials: Asterisk originates through the HT813's FXO port into the box's phone port (a relay switches between the panel and the FXO). It plays 8 s two-sentence files at a P.56 active level of −26 dBov and records both ends digitally. One sentence starts 0.5 s after answer and is scored separately, because answer clipping hits alarms first.
  - Alarm trials: events fired unattended from a Pi-driven relay on a test zone, so runs can continue overnight.
- **Order:** randomize step order within each session. Alternate the two boxes step by step, with the panel on an A/B relay. Repeat the whole sweep on a second day. Budget: about 12 steps × 40 trials × 50 s, roughly 7 h per box per pass.
- **Registration:** register the receiver DID with ##21. Voice trials go to a second registered DID that Asterisk routes to a play/record context; first check the box accepts two alarm numbers, otherwise alternate one DID by time slot. At three steps (0 dB, A_edge − 6, A_edge − 3), run a 2 × 2 of {registered, unregistered} × {speech, Contact ID}, 20 trials each. That shows what ##21 changes.
- **Two accounts:** alternate events between an account with repeated adjacent digits (1111) and one with none anywhere in the 16 digits. If edge failures concentrate on the repeated-digit account, that is the signature of concealment smearing in-band tones.

**The other carrier's box must be a real VoLTE control.** Confirm it is IMS-registered on the carrier's VoLTE with a dedicated voice bearer, from its diagnostics or the carrier. If it runs SIP over best-effort data instead, it is not a VoLTE control: say so on the poster and keep the cross-carrier line out of the video. Overlapping CIs are never described as "the same". "Same pattern" means a gap (CI above 0) on both boxes.

**Placements (realism).** Also run 20 events at three real spots: window, interior room, basement. This ties the sweep's margin to real homes.

**Analysis.** `scripts/analyze_prove_lab.py` prints:
- delta with its CI and the gap verdict, per box;
- the setup and drop curve;
- per-step tables with Wilson CIs and fail-stage counts;
- the learned signal bar per box (filtered n);
- a secondary matched-SINR table, labelled non-standard across modems.

Rehearse on `field_data/demo_sweep_SYNTHETIC.csv`, which has a known injected delta. Never show synthetic numbers as results.

### T6. Battery
- **Run 1:** unplug AC with fresh alkaline AAs. Log the minutes until the LED goes red and until the box powers off (standby, nothing connected). Then repeat with a 3-minute call every 30 minutes.
- **Run 2:** repeat with lithium AAs.
- **Compare with Verizon's stated figures:** 23 h standby, 3 h talk.
- **Cordless check:** confirm that a cordless phone base dies with AC even while the box is on battery.

### T7. Fax and TTY
- **Fax:** send 10 one-page faxes at 9600 bps with ECM off (Verizon's settings) to our SpanDSP receiver. Record success and retries.
- **TTY:** if a TTY is available, send 10 Baudot test strings to a TTY echo and record the character error rate.
- **Why:** measures fax at Verizon's recommended settings on this box.

### T8. Medical alert (only if the device can be pointed at our own receiver)
- Same as T1, with the PERS base on the black RJ11 port per Verizon's guide.
- **If the unit can only reach its vendor's center:** stop. Write to the vendor for a test window. Never trigger a real dispatch.

## 3. Analysis
Run `python3 scripts/analyze_prove_lab.py field_data/prove_lab.csv`. It reports:
- the confirmed rate with a 95% CI per device × path × placement;
- the first-try rate;
- the kiss-off time;
- the T5 sweep: per-step tables, gap steps and the matched-SINR comparison;
- the learned signal bar (SINR for 90% first-try confirmation, with a bootstrap CI). This is the "[N] bench alarm tests" number in the video.

Whole-call recordings from the tap can be checked one by one with `python3 -m prototype.prove.tap call.wav`.

The output table becomes the **Rutgers PROVE Lab matrix** on the poster, and the source of the one line on the video receipt.

## 4. Ethics and safety
- **FACTORY-DEFAULT EVERY USED PANEL BEFORE IT TOUCHES A LINE.** A panel bought used can still hold the previous owner's central-station number and account. Powered on with a live line, it can send AC-loss, tamper or low-battery events to a real monitoring company and trigger a dispatch to a stranger's home.
  - Hardware- or installer-default it, with the phone line disconnected.
  - Program our DID as the only dial-out number.
  - Prove it on the LAN baseline arm (A) first.
  - The faculty sponsor signs off before any panel is connected to a carrier line.
- Use our own receiver numbers only. No real central station, PSAP or medical-alert center unless it has agreed in writing and a test window is booked.
- No customer lines. No CPNI. The BPC100 is on a Rutgers department or faculty business account.
- Results go to the Verizon mentor first if they show a failure. Frame it as "we measured this so it can be fixed", never as a gotcha.
- Publish nulls. A clean pass on T3 is still a result.

## 5. Timeline
| Date | Step |
|---|---|
| Oct 22 | Order (rush shipping); faculty sponsor signs for the business line |
| Oct 24-25 | Bench assembled. T0 (how the box carries DTMF), tap-loading and receiver controls on arm A; then the T1 baseline |
| Oct 26-28 | T2, T3, T4 |
| Oct 27-28 | The other carrier's box activated and checked for carrier VoLTE; shield box, 2-channel attenuator and RSRP slope check; P.862.1 scorer checked on arm A |
| Oct 29-31 | T5 sweep on both boxes, T6 (the battery runs overnight), T7 |
| Nov 1-3 | Analysis; pick the one receipt line for the video |
| Nov 4-7 | Film the bench beat; final cut |
