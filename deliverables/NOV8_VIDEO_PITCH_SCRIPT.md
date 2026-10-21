# Nov 8 video: "Sent isn't received" (PROVE), 2:00 (v3, after the Gen 5b rescore)

**Two speakers:** A (engineering) and B (business). **Spoken words**, counted by `scripts/count_script_words.py` from the Audio column:
- **With the optional usability beat:** 234 spoken plus 19 handset, 253 in total.
- **Without it:** 215 plus 19, 234 in total.

Every beat runs at 142 wpm or less.

**Rules for the cut**
- **Opening and pacing.** Open on the stakes. Use at most one short on-screen line. Put one number on screen per beat. Leave at least 4 s with no talking while the ticks resolve. Jump-cut each test call with an on-screen "~15 s test call" timer, never in real time.
- **What stays out of the video.**
  - No docket numbers, rule sections, "paused" or "the regulator stopped checking"; those belong in Q&A and on the poster.
  - Never imply Verizon's network causes failures.
  - Show the weak-spot counters on screen only if the other carrier's box did the same at matched signal (decision table row 1), and only with the Verizon mentor's written OK.
- **Numbers.** [Brackets] are filled only from `field_data/prove_lab.csv` or the usability log. Every spoken number is verified (sources in `research/sources/`).
- **Receipts.** Say "receipt", never "guarantee". The receipt says the receiver picked up, the panel sent its full code, and the confirmation came back. It never says "delivered".
- **Names.**
  - Name the device actually tested ("Voice Gateway" or "Business Phone Connect").
  - Say "our bench at Rutgers" or "our PROVE bench in a Rutgers ECE lab" until the sponsor approves the name "Rutgers PROVE Lab".
  - Say "we're proposing ... to Facilities" until Facilities agrees in writing.
- **One persistent corner bug, 0:22-1:14:** *Bench demo · PROVE tap at the alarm port · lab receiver = alarm company · weak spot = RF attenuator*. It replaces the rotating lower thirds, and the ending card says the rest.

| Time | Visual | Audio |
|---|---|---|
| 0:00-0:10 | Night. An alarm keypad in a dark hallway reads **ARMED AWAY**, its green light steady. One line fades in and out: *The copper's gone. Will this alarm still get through?* | **A:** "When the copper line goes, the alarm panel on it won't find out until the night it calls for help." |
| 0:10-0:22 | The box on the bench, with the alarm panel on its alarm port and a corded phone. Caption: the device name. | **B:** "This is Verizon's Voice Gateway, one of the boxes replacing copper. Its guide asks alarm customers to test. We made that test one guided check, with a receipt." |
| 0:22-0:56 | Two presses on camera: PROVE, then the keypad's TEST. Jump cut with the "~15 s test call" timer. The console shows **picked up ✓ → full code sent ✓ → confirmation ✗**, then *Signal here: below the learned alarm bar*. Lower third over the handset prompt: *Signal bar learned from [N] bench alarm tests*. The handset speaks. The box goes nearer the window and the test is re-run (timer). **4 s with no talking** while three green ticks resolve. The receipt prints last. | **A:** "PROVE listens to the alarm's test call through Verizon's network. Did the alarm company pick up? Did the panel send its full code? Did the 'got it' come back? A model learned from our bench tests checks the signal carries alarm data, not just voice." **Handset:** "Signal here is too weak for alarm data. Move the box nearer a window, then test the alarm again." |
| 0:56-1:14 | Bench: two counters side by side on one box: **TEST CALL: clear [k/k]** and **ALARM: confirmed [m/20]**, then the window spot: **ALARM [20/20]**. Caption: *Weak spot: SINR [x] dB, set with an attenuator · "clear" = PESQ ≥ 3.0 · step [i] of [N] · full sweep on poster*. Then a third counter slides in: **Another carrier's box, same signal: ALARM [m'/20]**. | **B:** "On our bench at Rutgers, at a weak spot the test call sounded clear [k of k] times. The alarm got through [m of 20]. Near the window, [20 of 20]. Another carrier's line did the same. A clear call isn't proof." |
| 1:14-1:22 | Optional, only with a usability determination and signed release: a volunteer's hands follow the spoken fix; the receipt turns green. If not cleared, give these 8 s to the next two beats (no music filler). | **B:** "In our usability session, [k of n] older volunteers followed PROVE's spoken fix to a green receipt without help." |
| 1:22-1:37 | One card: **46,000** *homes and businesses on these boxes (Verizon, summer 2026 FCC filings)*. Small caption under it: *+417,000 more lines in two 2026 filings · replacements include fiber, mobile and boxes like this*. Second line on the same card: **1 point = 10 truck rolls per 1,000 installs**. | **A:** "Verizon told the FCC about forty-six thousand homes and businesses use these boxes, and its 2026 filings cover hundreds of thousands more. Per thousand installs, each point off repeat visits is ten truck rolls saved." |
| 1:37-1:55 | **Both speakers on camera** at the bench. B holds up the pocket PROVE tap (Pi, line tap, battery). Then the PROVE icon on the box's status screen. Then elevator HELP B-roll (public car, no people; caption *proposal: no Rutgers line tested*). | **B:** "Our ask: thirty days on one migration batch, technicians carrying a pocket PROVE tap on alarm installs, versus a control group. Then the same checks as box firmware. And we're proposing the same proof to Rutgers Facilities for elevator HELP phones." |
| 1:55-2:00 | The receipt is torn off and handed to camera. End card: **PROVE · built at Rutgers ECE · student concept, not a Verizon product.** | **Both:** "Sent isn't received. PROVE." |

**If Facilities agrees in writing before Nov 4,** B's last sentence becomes "And Rutgers Facilities has agreed to walk through [N] elevator HELP phones with us." That adds no words.

**If the mentor confirms that device management can count boxes with a registered alarm number** (`OUTREACH_KIT.md` §10, question 6), A's second sentence becomes "Verizon can already count these homes: every box with an alarm number registered." (−5 words)

## The receipt (what prints on camera)
```
PROVE · test record                Oct [30] 2026 14:02
------------------------------------------------------
SIGNAL here   GOOD · above the learned alarm bar
VOICE         CLEAR BOTH WAYS
ALARM         Receiver picked up · full code sent ·
              confirmed in [x.x] s
BATTERY       Installed · keeps working when unplugged
------------------------------------------------------
GREEN: all checks passed · no visit requested
Test record, not a guarantee. Confirm the test
with your alarm company, as you do today.
```
- Print "box modem" signal values only if they come from the box itself. Otherwise label them "phone at the box (proxy)", and only on the poster.
- "No visit requested" is deliberate. Whether to skip a visit is Verizon's policy call (Q&A 4); the receipt only reports that nothing failed.

## Decision table for the bench beat (lock on Nov 3)
| Bench result | What the video says |
|---|---|
| A weak-spot gap was measured (call clear, alarm short), the other carrier's box shows the same gap at matched SINR (overlapping CIs in `analyze_prove_lab.py`'s matched-SINR table), **and** the mentor has given a written OK | Use the script as written. |
| A gap was measured, but the other carrier's box did **not** do the same | Keep the numbers off screen. B says: "On our bench at Rutgers, PROVE found the signal level where alarm data fails before voice does. Those results went to Verizon first." The counters go to the poster only with the mentor's OK. |
| No gap was measured by Nov 3 (alarm as robust as voice at every step) | B says: "On our bench at Rutgers, Verizon's box confirmed [n of 50] alarm tests, and PROVE now knows the signal floor below which neither works." The value claim shifts to install triage (signal, registration, battery). |
| The swap test (T3) shows lost alarm registrations | Only with the mentor's written OK, say: "After a box swap, PROVE flagged a step the swap guide could add. It's already with Verizon." |
| **K1 fails (no live Verizon box by Oct 29)** | Use the full fallback script below. |

### K1 fallback script (complete, 2:00)
- **0:00-0:10:** the same opening.
- **0:10-0:22 (B):** "Verizon replaces copper with boxes like this. Its guide asks alarm customers to test. We built the check that makes that test answer back."
- **0:22-0:56:** the demo on the other carrier's wireless box. Corner bug: *Another carrier's line · Verizon's box next week*.
- **0:56-1:14 (B):** "On a wireless home-phone line in our lab, at a weak spot the test call sounded clear [k of k] times, while the alarm got through [m of 20]. A clear call isn't proof. Next, this runs on Verizon's box."
- **1:14-2:00:** as above.
- Expect about 60/95 (judge estimate). The live box is worth roughly 8-15 points.

## Shot list (Nov 4-6)
1. Keypad reading ARMED AWAY in a dark hallway (lab or a permitted room). Check the display text on the actual panel model.
2. Both presses (PROVE, then keypad TEST), the timer overlay, and the console ticks.
3. The weak spot (attenuator dial in shot), the handset prompt, the move, then green.
4. The counters, including the other carrier's box.
5. The receipt printing (macro).
6. The pocket PROVE tap in a hand (Pi, line tap, battery pack, in a small case).
7. Optional: volunteer hands, with the release on file.
8. Elevator HELP B-roll: a public car, no people, nothing opened.
9. Both speakers on camera for the ask. One clean take per line.
