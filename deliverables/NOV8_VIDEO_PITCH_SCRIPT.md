# Nov 8 video: "Sent isn't received" (PROVE), 2:00 (v5: v4 plus the Gen 7 first-viewing test)

**Two speakers:** A (engineering) and B (business). **Spoken words:** 226 from the speakers plus 12 in PROVE's voice prompt, 238 in total (`scripts/count_script_words.py`). After subtracting the silences and tones, every beat stays at 142 wpm or less. The cut ends at 1:59.8.

**The sound signature.** The film's motif is the alarm's own "got it": the 0.8 s, 1400 Hz kiss-off tone the receiver sends back, recorded for real from the line tap.
- **Cold open:** we hear the panel's digits, then silence where the tone should be.
- **The failure:** the music cuts to zero for the same silence, under the overlay **SENT ✓ · CONFIRMED ✗**.
- **The fix:** the tone rings out at full level.
- **The end:** it plays one last time, alone, under "Sent isn't received".

Score the music pad in F major: 1400 Hz is about F6, so the tone lands as a resolution.

**Rules for the cut**
- **Plain words for a first-time viewer.** These come from the Gen 7 first-viewing test, where three lay viewers scored v4 at 6.5-7.5/10.
  - Say "landline", not "copper", aloud.
  - Say "pocket tester", not "tap" (which sounds like a wiretap).
  - Say "repair-truck visit", not "truck roll".
  - Keep "dB", "SINR", "batch" and "Phase" off screen.
  - Name the speakers in lower thirds.
- **Two words, never mixed.**
  - The panel's call is the **alarm test**.
  - An ordinary voice call is a **phone call**.
  - Never say "test call" for both.
- **On-screen text.**
  - Captions are 6 words or fewer, one at a time, at least 54 px.
  - One number per card.
  - Capture the console full frame with OBS.
  - One corner bug from 0:27 to 1:21: **LAB DEMO · our receiver plays the alarm company · weak signal made on purpose**.
- **What stays out of the video.**
  - Docket numbers, rule sections, and "the regulator stopped checking".
  - Any implication that Verizon's network causes failures.
  - Verizon's box shown failing alone. Both carriers' boxes are on screen together, from the first frame of the bench beat.
- **Numbers.** [Brackets] are filled only through `scripts/analyze_prove_lab.py` on `field_data/prove_lab.csv`. Every spoken number is verified (sources in `research/sources/`).
- **Receipts.** Say "receipt", never "guarantee". The receipt never says "delivered".
- **Names.**
  - [Device] is the box actually tested.
  - Say "Its guide" only if that box's guide is saved in `research/sources/` with its test language. Otherwise say "Verizon's guide for these boxes".
  - Say "our bench at Rutgers" until the sponsor approves the name "Rutgers PROVE Lab".
  - Say "we're proposing ... to Facilities" until Facilities agrees in writing.
  - Label anything not built "Concept". No invented UI on Verizon's box.
- **Mix.**
  - All voice recorded in one session on one mic.
  - Loudness −16 LUFS integrated, true peak −1 dBTP.
  - Tones 6-8 dB under the voice; music 26-30 dB under the voice.
  - Device audio taken from the tap, band-passed 300-3400 Hz.
  - SRT closed captions.

| Time | Visual | Audio |
|---|---|---|
| 0:00-0:05 | **Cold open, no voice.** Extreme close-up of the keypad LCD reading **ARMED STAY** (check it is the panel's real text), with the red ARMED light lit and a slow push-in. A bedroom night light glows down the hall (someone is home). Text, one line at a time, 96 px or larger: *An alarm, calling for help* at 0:00.5, **Sent ✓** at 0:02.9, **Received?** at 0:03.9. | Room tone. At 0:00.6, the receiver's handshake (two short tones). From 0:01.0 to 0:02.8, the panel's 16-digit burst. From 0:02.8 to 0:04.8, silence where the "got it" should be. No music. |
| 0:05-0:15 | Close-up of an old wall jack with the phone cord pulled out (generic, no brand). Then a wide shot of the keypad, its red light the only glow. No text. A low pad enters. | **A:** "When a landline is replaced, an alarm can stop getting through, and no one may notice until the night it calls for help." |
| 0:15-0:27 | B on camera with a hand on the box. Then **one caption at a time**: lower third *[Name] · Rutgers ECE* (0:15-0:18); the guide page with *determined by your testing* highlighted, full frame for 3 s (0:19-0:22); B clips the tester onto the box's alarm port, captioned *PROVE = our pocket tester* (0:23-0:27). | **B:** "This is Verizon's [Voice Connect] box, a landline replacement. Its guide asks alarm owners to test. Our pocket tester turns that into one check with a receipt." |
| 0:27-1:00 | A finger presses PROVE on the tester, then the keypad's TEST (with its real beep). Jump cut to a clock icon labelled **ALARM TEST**. Full-frame console: **Picked up ✓** (handshake chirp), **Full code sent ✓** (1 s of digits). Then a 1.5 s freeze with the overlay **SENT ✓ · CONFIRMED ✗** and the music cut to zero. The tech's phone shows the prompt and speaks it, captioned *PROVE, on the tech's phone · as Verizon's guide suggests*. A hand turns the attenuator dial back, captioned *Signal turned up · like moving nearer a window*. The alarm test is re-run: **the "got it" tone rings out at full level**, and three green ticks. The receipt prints, in macro. | **A:** "While the alarm sends its test over Verizon's LTE network, PROVE checks three things. Did the alarm company pick up? Did the panel send its full code? Did the 'got it' come back?" **PROVE voice:** "Signal too weak for alarms. Try nearer a window, then test again." **A:** "Alarms talk in beeps, and weak signal breaks beeps before voices. PROVE learned from our lab tests how strong is enough." Caption under the last line: *Learned from [N] lab alarm tests*. |
| 1:00-1:21 | At the weak-spot dial setting, B lifts the handset. The far end says, clearly: "Can you hear me? Loud and clear." Then a big two-row card, **both rows at once**, with icons rather than tables: **Verizon box: 📞 ✓ [k]/20 · 🔔 [m]/20** and **Another carrier's box: 📞 ✓ [k']/20 · 🔔 [m']/20**. Each column lights as it is spoken. Full-screen card at 1:18: **A clear call isn't proof.** | **B:** "On our bench at Rutgers, at one weak signal, phone calls on two carriers' boxes sounded clear [k of 20] times. Alarms got through about [m] of 20 on both. It's the weak signal, not the carrier. A clear call isn't proof." |
| 1:21-1:36 | Card 1: **5,000,000**, with *alarm panels that still dial a phone line · alarm industry, to the FCC*. Card 2: the tester beside a repair truck, captioned **Tester < one truck visit**. | **A:** "Five million alarm panels still dial out over phone lines, and each one moved to a box like this should get this check. A pocket tester costs less than one repair-truck visit." |
| 1:36-1:54 | A two-shot of both speakers at the bench, with a lower third for A: *[Name] · Rutgers ECE*. B holds up the tester, and its receipt lands on A's phone (Phase 1, real). Captions, one at a time: *Ask: 30-day trial* · *Then: built into the box* (over a close-up of the box, no invented UI) · *Proposed: Rutgers elevator HELP phones* (over an empty public elevator car, slow push in to the HELP button). The music lifts and stops dead at 1:53.5. | **B:** "Our ask: a thirty-day trial, technicians carrying this tester on alarm installs, counting the failures it catches that a phone-call check would pass. Then a software update puts it in the box. At Rutgers, we're proposing the same proof for elevator HELP phones." |
| 1:54-2:00 | B pushes the receipt at the lens, and focus pulls to the line **confirmed 2.6 s**. **The "got it" tone plays alone.** End card, held 4 s, 10 words or fewer: **PROVE** above *Rutgers ECE student concept · results shared with Verizon first*. | **B:** "Sent isn't received." **A:** "PROVE it." |

**If Facilities agrees in writing before Nov 4,** B's last sentence becomes "At Rutgers, Facilities will walk through [N] elevator HELP phones with us." The caption becomes *[N] Rutgers elevator HELP phones · with Facilities*. If Facilities gives only a count, keep "proposing" and put the count in the caption.

**Phase 1 vs Phase 2, kept honest on screen.**
- **Phase 1** is the pocket tester (the "tap" in the technical documents). It listens, reads signal from the box's own diagnostics (or a proxy phone on the same attenuated path, labelled), speaks through the technician's phone, and prints or texts the receipt.
- **Phase 2** is box firmware. Spoken prompts through the handset and automatic battery checks arrive with Phase 2, which is never shown as built.

## The receipt (32 columns, thermal printer on the tap; macro shot)
```
PROVE · test record
Oct [30] 2026 14:02
--------------------------------
SIGNAL (box)   above alarm bar
VOICE (resp.)  clear both ways
ALARM (tap)    picked up
               full code sent
               confirmed [x.x] s
BATTERY        installed
--------------------------------
GREEN: all checks passed
       no visit requested
Test record, not a guarantee.
Confirm the test with your
alarm company, as today.
```
Print only the lines measured on that run, with the verdict line in double height. Where each line comes from:
- **SIGNAL:** the box's own reading;
- **VOICE:** a call to the PROVE test responder;
- **ALARM:** the line tap;
- **BATTERY:** a check that batteries are installed, which the technician confirms in Phase 1.

## Decision table (lock on Nov 3; build every variant of beats 0:27 and 1:00 on Nov 1-2)
| Bench result (from `analyze_prove_lab.py`) | Demo fault | A at 0:27 (model line) and PROVE voice | B at 1:00 | Cold open and end |
|---|---|---|---|---|
| **Row 1.** All four hold: (a) delta's 95% CI is above 0 on **both** boxes (`analyze_prove_lab.py`); (b) the other carrier's box is confirmed on carrier VoLTE; (c) Verizon's box gets 20/20 at strong signal; (d) the mentor has given a written OK, cleared with whoever owns the open WC 26-227 proceeding. | Weak signal (attenuator) | As written | As written | As written |
| **Row 1b.** No row-1 signal gap, but T2 shows that with the alarm number **not registered**, phone calls are clear and alarms fail. This is a setup step Verizon's own guide covers, so it is sponsor-safe without a second carrier. | Number not registered (##21 cleared) | A replaces the beeps sentence with: "PROVE also learned from our lab tests how strong the signal must be." PROVE voice: "This box doesn't have your alarm company's number yet. Enter it as the guide shows, then test again." | "On our bench at Rutgers, with the alarm number not registered, a phone call sounded clear [k of 20] times. The alarm got through [m of 20]. Registered: [20 of 20]. A clear call isn't proof." The card shows one box with two rows: *not registered* and *registered*. | As written |
| **Row 2.** A gap on Verizon's box only, the other box isn't a VoLTE control, or Verizon's box is below 20/20 at strong signal, and T2 doesn't qualify. | Film the failure only at a dial setting where **both** boxes failed (from the per-step tables); otherwise use the battery fault. | A drops the beeps sentence: "PROVE learned from our lab tests how much signal an alarm needs." | "On our bench at Rutgers, PROVE learned from [N] alarm tests how much signal an alarm needs. Below that line, the receipt says: move the box. A clear call isn't proof." No counters. | As written |
| **Row 3.** No gap on either box, and T2 passes. | Battery or signal floor (both fail below dropout) | A's model line as in row 2 (the beeps sentence is dropped). | "On our bench at Rutgers, alarms held up as well as calls. What failed was setup: [the signal floor, the batteries]. PROVE catches those before anyone leaves." | The cold open ends on **Sent ✓ Received ✓**, then cuts to the empty wall jack. The end line stays. |
| The swap test (T3) loses alarm registrations | Unchanged | Unchanged | Only with the mentor's written OK: "After a box swap, PROVE flagged a step the swap guide could add. It's already with Verizon." | Unchanged |
| **K1 fails (no live Verizon box by Oct 29)** | The full fallback script below | | | |

Never use `alarm.py`'s synthetic audio as the failure sound in any row. The executive summary's lay box, Q&A 11c and poster panel 2 change with the row; see `ACTION_PLAN.md` for the Nov 3 checklist.

### K1 fallback script (complete, 2:00)
- **0:00-0:27:** as above, with "a box like this" in place of the device name and "Verizon's guide for these boxes".
- **0:27-1:00:** the demo on the other carrier's LTE voice box. Corner bug: *Another carrier's line · Verizon's box next*.
- **1:00-1:21 (B):** "On a wireless home-phone line in our lab, phone calls stayed clear [k of 20] times while the alarm got through [m of 20]. A clear call isn't proof. Next, this runs on Verizon's box."
- **1:21-2:00:** as above.
- Expect about 60/95 (judge estimate). The live box is worth roughly 8-15 points.

## Shoot plan
- **Nov 1-2:** build every decision-table variant of the graphics from the synthetic CSV, so Nov 3 is a number swap.
- **Nov 4, bench:**
  - the keypad (fit EOL resistors so the panel arms; check the ARMED STAY text) and the hall set dressing;
  - the 0:27 demo, with 5 or more takes each of the failure and the pass;
  - the 1:00 inserts (record the far-end "Can you hear me? Loud and clear." through the real path);
  - the receipt macro;
  - the OBS captures;
  - the clean dual-tap audio of a failed and a passed alarm test.
- **Nov 5:**
  - B on camera at 0:15;
  - the two-shot at 1:37;
  - the receipt push;
  - the copper-jack insert;
  - all voice-over in one session.
- **Nov 6:** elevator B-roll (a public car, no people, nothing opened), and pickups.
- **Nov 7:**
  - mix and export (H.264 1080p at 16 Mbps or more, with 1-2% grain on the cold open);
  - check on a 13-inch laptop at 50% brightness;
  - upload by 6 pm.
