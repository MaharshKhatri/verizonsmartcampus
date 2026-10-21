# PROVE Lab bench protocol: one real, measured result before Nov 8

**Why:** every judge persona said the same thing. The pitch is only as strong as one failure (or one clean pass) measured on Verizon's real copper-replacement box. Verizon's own documents disagree about what this box supports:

| Topic | Inseego BPC100 guide | Verizon documents |
|---|---|---|
| Medical alerts | "cannot be made" | Voice Connect guide: supports "most" |
| Personal monitoring | | Voice Connect ToS: "not compatible with ... personal monitoring services" |
| Fax | User guide lists fax support (an Inseego quick-start sheet reportedly says otherwise; unverified) | Verizon recommends 9600 bps, ECM off |

Only a bench can settle it. Everything below is safe, legal and doable by two students in a week. **Never dial 911. Never send test signals to a real central station or medical-alert company without its written OK.** We run our own receiver.

## 1. Bill of materials (about $1,000-1,700; order Oct 22)
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
| **Two 0-60 dB SMA step attenuators** (manual rotary or digital, 1-2 dB steps), ganged, plus SMA cables and two small antennas | Repeatable "weak spot" for the sweep (T5). Inseego lists "2 SMA connectors for external antennas" on the BPC100, so attenuate both MIMO ports by the same amount. A box with internal antennas goes in the RF shield box below. | $120-300 |
| **RF shield box** (tabletop, with SMA pass-through) and a small external antenna | Puts a box with internal antennas under the attenuator's control | $100-300 (used) |
| Harvard-sentence recording plus open-source ITU-T P.862 (PESQ) scorer | The objective "call sounded clear" rule (PESQ ≥ 3.0), pre-registered | $0 |
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
Columns: `test_id, date, box, firmware, placement, atten_db, rsrp_dbm, rsrq_db, sinr_db, device, format, registered_21, attempt, call_trial, pesq, listener_keywords, delivered, kissoff_s, attempts_used, notes`. The `delivered` column means "receiver logged a valid event and sent a kiss-off"; on screen it is always "confirmed", never "delivered".

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

### T5. Signal sweep: voice clear vs alarm confirmed (the bench beat)
**Pre-registered before any run:**
- **What "clear" means:** PESQ (ITU-T P.862, open-source scorer) ≥ 3.0 on a recorded Harvard sentence, or, if PESQ is unavailable, a blinded listener gets ≥ 9 of 10 keywords.
- **What "gap" means:** calls clear in ≥ 90% of trials while alarms are confirmed in < 90%.

**Sweep.** Step the attenuator from 0 dB in 2 dB steps until the box loses service. Do this on **both** boxes: Verizon's, and the other carrier's.
- **At each step:**
  - record the box's own RSRP/RSRQ/SINR, or the phone proxy, labelled as such;
  - run 3 one-minute voice calls (`call_trial=1`, with `pesq` and `listener_keywords`);
  - run 10 Contact ID events (`call_trial=0`).
- **Around the transition:** add steps until there are 20 events per step.
- **Time:** about 6 h per box. Run the two boxes on different days with the same panel and receiver.

**Matched SINR.** The video compares the two boxes at the same box-reported SINR (2 dB bins), not at the same dial setting, because the carriers' bands differ.

**Placements (realism).** Also run 20 events at three real spots: window, interior room, basement. This shows where the sweep's gap shows up in a home.

**Analysis.** `scripts/analyze_prove_lab.py` prints:
- a per-step table for each box with Wilson CIs;
- the gap steps, with their SINR range;
- the matched-SINR comparison ("did the other carrier's box do the same?").

Rehearse it now on `field_data/demo_sweep_SYNTHETIC.csv` (made by `scripts/make_demo_sweep_csv.py`). Never show synthetic numbers as results.

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
| Oct 24-25 | Bench assembled; T1 baseline |
| Oct 26-28 | T2, T3, T4 |
| Oct 27-28 | The other carrier's box activated; attenuator and shield box set up; PESQ scorer checked on arm A |
| Oct 29-31 | T5 sweep on both boxes, T6 (the battery runs overnight), T7 |
| Nov 1-3 | Analysis; pick the one receipt line for the video |
| Nov 4-7 | Film the bench beat; final cut |
