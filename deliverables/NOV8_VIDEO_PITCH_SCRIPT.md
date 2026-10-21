# Nov 8 video: "Sent isn't received" (PROVE), 2:00 (v4, after the Gen 6 review: three judges, a film editor, a RAN engineer)

**Two speakers:** A (engineering) and B (business). **Spoken words:** 221 from the speakers plus 18 in PROVE's voice prompt, 239 in total (`scripts/count_script_words.py`). After subtracting the silences and tones, every beat stays at 142 wpm or less. The cut ends at 1:59.8.

**The sound signature.** The film's motif is the alarm's own "got it": the 0.8 s, 1400 Hz kiss-off tone the receiver sends back, recorded for real from the line tap.
- **Cold open:** we hear the panel's digits, then silence where the tone should be.
- **The failure:** the music cuts to zero for the same silence, under the overlay **SENT ✓ · CONFIRMED ✗**.
- **The fix:** the tone rings out at full level.
- **The end:** it plays one last time, alone, under "Sent isn't received".

Score the music pad in F major: 1400 Hz is about F6, so the tone lands as a resolution.

**Rules for the cut**
- **Two words, never mixed.**
  - The panel's call is the **alarm test**.
  - An ordinary voice call is a **phone call**.
  - Never say "test call" for both.
- **On-screen text.**
  - Captions are 6 words or fewer, one at a time, at least 54 px.
  - One number per card.
  - Capture the console full frame with OBS.
  - One corner bug from 0:26 to 1:21: **LAB DEMO · our receiver plays the alarm company · weak signal made on purpose**.
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
| 0:00-0:05 | **Cold open, no voice.** Extreme close-up of the keypad LCD reading **ARMED STAY** (check it is the panel's real text), with the red ARMED light lit and a slow push-in. Pull focus to the hall behind it: a cane leaning by the door, and a night light under a bedroom door. No person filmed. Text, one word each, 96 px or larger: **Sent ✓** at 0:02.9, then **Received?** at 0:03.9. | Room tone. At 0:00.6, the receiver's handshake (two short tones). From 0:01.0 to 0:02.8, the panel's 16-digit burst. From 0:02.8 to 0:04.8, silence where the "got it" should be. No music. |
| 0:05-0:15 | Extreme close-up of a hand unplugging a copper phone cord from a wall jack, with the real click. Then a wide shot of the keypad, its red light the only glow. No text. A low pad enters. | **A:** "When the copper line goes, an alarm panel may not learn it can't get through until the night it calls for help." |
| 0:15-0:26 | B on camera clips the pocket tap onto the box's alarm port. Caption: *PROVE = our pocket tap*. Lower third: [Device]. Insert: the guide page with *determined by your testing* highlighted. | **B:** "This is Verizon's [Voice Connect], a copper replacement. Its guide asks alarm customers to test their alarm. We made that one guided check, with a receipt." |
| 0:26-1:03 | A finger presses PROVE on the tap, then the keypad's TEST (with its real beep). Jump cut, with an **ALARM TEST · 15 s** timer running at 8×. Full-frame console: **Picked up ✓** (handshake chirp), **Full code sent ✓** (1 s of digits). Then a 1.5 s freeze with the overlay **SENT ✓ · CONFIRMED ✗**, and the music cut to zero. The tech's phone shows the prompt and speaks it. A hand turns the attenuator dial back, captioned *Signal turned up · like moving nearer a window*. The alarm test is re-run: **the kiss-off tone rings out at full level**, three green ticks. The receipt prints at 32 columns, in macro. | **A:** "While the alarm sends its test over Verizon's LTE network, PROVE checks three things. Did the alarm company pick up? Did the panel send its full code? Did the 'got it' come back?" **PROVE voice:** "Signal here is too weak for alarms. Try nearer a window, as Verizon's guide says, then test again." **A:** "Alarms talk in beeps, and a weak signal breaks beeps before it breaks voices. Our model, trained on bench tests, learned how strong is enough." |
| 1:03-1:21 | At the weak-spot dial setting, B lifts the handset. We hear the far-end sentence clearly ("The birch canoe slid on the smooth planks."). Then a two-row table appears, **both rows at once**: **VERIZON BOX · phone call clear [k]/20 · alarm [m]/20** and **OTHER CARRIER'S BOX · phone call clear [k']/20 · alarm [m']/20**. Each column lights as its number is spoken. One card: **+[X] dB**, captioned *extra signal the alarm needed*. Then a full-screen card at 1:18: **A clear call isn't proof.** | **B:** "On our bench at Rutgers, at one weak signal, phone calls on two carriers' boxes sounded clear [k of 20] times. Alarms got through about [m] of 20 on both. A clear call isn't proof." |
| 1:21-1:37 | Card 1: **46,000**, with *on these boxes today · Verizon FCC filings, 2026*. Card 2: **5,000,000**, with *dial-out alarm panels · alarm industry, to the FCC*. Card 3: the tap beside a truck icon, captioned **Tap parts < one truck roll**. | **A:** "Verizon told the FCC about forty-six thousand homes and businesses use these boxes. Five million alarm panels still dial out over phone lines. A pocket tap costs less in parts than one truck roll." |
| 1:37-1:55 | A two-shot of both speakers at the bench. B holds up the tap, and its receipt lands on A's phone (Phase 1, real). Caption *Ask: 30 days · vs matched batch*. Close-up of the box, captioned *Phase 2: via Verizon device management*. An empty public elevator car, slow push in to the HELP button, captioned *Proposed · Rutgers elevator HELP*. The music lifts and stops dead at 1:54.5. | **B:** "Our ask: thirty days of technicians carrying this pocket tap on alarm installs, counting alarms it catches that a phone call missed. Then a software update puts it in the box. At Rutgers, we're proposing the same proof for elevator HELP phones." |
| 1:55-2:00 | B tears off the receipt and pushes it at the lens, and focus pulls to **GREEN · all checks passed**. **The kiss-off tone plays alone.** End card, held 3 s: **PROVE** above *Rutgers ECE · advisor Prof. [X] · student concept, not a Verizon product · bench results shared with Verizon first*. | **B:** "Sent isn't received." **A (voice-over):** "PROVE." |

**If Facilities agrees in writing before Nov 4,** B's last sentence becomes "At Rutgers, Facilities will walk through [N] elevator HELP phones with us." The caption becomes *Rutgers elevator HELP · with Facilities*.

**Phase 1 vs Phase 2, kept honest on screen.**
- **Phase 1** is the pocket tap. It listens, reads signal from the box's own diagnostics (or a proxy phone on the same attenuated path, labelled), speaks through the technician's phone, and prints or texts the receipt.
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

## Decision table (lock on Nov 3; build every variant of beats 0:26, 1:03 and 1:21 on Nov 1-2)
| Bench result (from `analyze_prove_lab.py`) | Demo fault | A at 0:26 (model line) and PROVE voice | B at 1:03 | Cold open and end |
|---|---|---|---|---|
| **Row 1.** All four hold: (a) delta's 95% CI is above 0 on **both** boxes (`analyze_prove_lab.py`); (b) the other carrier's box is confirmed on carrier VoLTE; (c) Verizon's box gets 20/20 at strong signal; (d) the mentor has given a written OK, cleared with whoever owns the open WC 26-227 proceeding. | Weak signal (attenuator) | As written | As written | As written |
| **Row 1b.** No row-1 signal gap, but T2 shows that with the alarm number **not registered**, phone calls are clear and alarms fail. This is a setup step Verizon's own guide covers, so it is sponsor-safe without a second carrier. | Number not registered (##21 cleared) | A: "...Our model, trained on bench tests, also learned how strong the signal must be." PROVE voice: "This box doesn't have your alarm company's number yet. Enter it as the guide shows, then test again." | "On our bench at Rutgers, with the alarm number not registered, a phone call sounded clear [k of 20] times. The alarm got through [m of 20]. Registered: [20 of 20]. A clear call isn't proof." The table shows one box, two rows: *not registered* and *registered*. | As written |
| **Row 2.** A gap on Verizon's box only, the other box isn't a VoLTE control, or Verizon's box is below 20/20 at strong signal, and T2 doesn't qualify. | Film the failure only at a dial setting where **both** boxes failed (from the per-step tables); otherwise use the battery fault. | A: "...Our model, trained on bench tests, learned how much signal an alarm needs." | "On our bench at Rutgers, PROVE learned from [N] alarm tests how much signal an alarm needs. Below that line, the receipt says: move the box." No counters; cut the +[X] dB card. | As written |
| **Row 3.** No gap on either box, and T2 passes. | Battery or signal floor (both fail below dropout) | A's model line as in row 2. Change "breaks beeps before it breaks voices" to "can break both". | "On our bench at Rutgers, alarms held up as well as calls. What failed was setup: [the signal floor, the batteries]. PROVE catches those before anyone leaves." | The cold open ends on **Sent ✓ Received ✓**, then cuts to the unplugged copper. The end line stays. |
| The swap test (T3) loses alarm registrations | Unchanged | Unchanged | Only with the mentor's written OK: "After a box swap, PROVE flagged a step the swap guide could add. It's already with Verizon." | Unchanged |
| **K1 fails (no live Verizon box by Oct 29)** | The full fallback script below | | | |

Never use `alarm.py`'s synthetic audio as the failure sound in any row. The executive summary's lay box, Q&A 11c and poster panel 2 change with the row; see `ACTION_PLAN.md` for the Nov 3 checklist.

### K1 fallback script (complete, 2:00)
- **0:00-0:26:** as above, with "a box like this" in place of the device name and "Verizon's guide for these boxes".
- **0:26-1:03:** the demo on the other carrier's LTE voice box. Corner bug: *Another carrier's line · Verizon's box next*.
- **1:03-1:21 (B):** "On a wireless home-phone line in our lab, phone calls stayed clear [k of 20] times while the alarm got through [m of 20]. A clear call isn't proof. Next, this runs on Verizon's box."
- **1:21-2:00:** as above.
- Expect about 60/95 (judge estimate). The live box is worth roughly 8-15 points.

## Shoot plan
- **Nov 1-2:** build every decision-table variant of the graphics from the synthetic CSV, so Nov 3 is a number swap.
- **Nov 4, bench:**
  - the keypad (fit EOL resistors so the panel arms; check the ARMED STAY text) and the hall set dressing;
  - the 0:26 demo, with 5 or more takes each of the failure and the pass;
  - the 1:03 inserts;
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
