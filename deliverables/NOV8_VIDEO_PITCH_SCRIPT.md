# Nov 8 video: "Sent isn't received" (PROVE), 2:00 (v2, after the Gen 5 fact-check and judge review)

**Two speakers:** A (engineering) and B (business). About 235 spoken words plus a 20-word handset line.

**Rules for the cut**
- **Opening and pacing.** Open on the stakes, never on text cards. One number on screen per beat.
- **What stays out of the video.** No docket numbers, rule sections, "paused" or "the regulator stopped checking"; those belong in Q&A and on the poster. Never imply Verizon's network causes failures. Show any result that falls below the lab baseline to the Verizon mentor first and keep it off screen.
- **Numbers.** [Brackets] are filled only from `field_data/prove_lab.csv` or the usability log. Every spoken number is verified (sources in `research/sources/`).
- **Receipts.** Say "receipt", never "guarantee". The receipt says the receiver picked up, the panel sent its full code, and confirmation came back. It never says "delivered".
- **Names.**
  - Name the device actually tested ("Voice Gateway" or "Business Phone Connect").
  - Say "our PROVE bench in a Rutgers ECE lab" until the sponsor approves the name "Rutgers PROVE Lab".
  - Say "we're proposing ... to Facilities" until Facilities agrees in writing.
- **On-screen labels.** Every staged shot carries a lower third: "Weak spot simulated with an RF attenuator", "Demo printout", "Lab receiver stands in for the alarm company".

| Time | Visual | Audio |
|---|---|---|
| 0:00-0:10 | Night. An armed alarm keypad glows **READY** in a dark hallway. On screen: *The copper's gone. This alarm hasn't called anyone since.* | **A:** "When a copper phone line goes away, the alarm panel on it doesn't find out until the night it has to call for help. For many homes, that call now goes through a new box." |
| 0:10-0:25 | The device on the bench, with the alarm panel on its alarm port and a corded phone. Caption: device name. | **B:** "This is [Verizon's Voice Gateway], one of the boxes Verizon uses to replace copper. Its guide already asks customers with an alarm to test it when the box goes in. We turned that test into one guided check, with a receipt." |
| 0:25-0:58 | Two presses on camera: PROVE, then the keypad's TEST. The console shows **picked up → full code sent → confirmation ✗** and the line *Panel: sent ✓ · Confirmation: none*. Lower third: *Weak spot simulated with an RF attenuator.* The handset speaks. The box goes nearer the window and the test is re-run: three green ticks. The receipt prints last (lower third: *Demo printout · in production, on the box's status screen and by text*). | **A:** "PROVE is built to ship as a firmware update through Verizon's device management. It listens to the alarm's own test call over Verizon's LTE voice network. Did the alarm company's system pick up? Did the panel send its full code? Did the 'got it' come back? It also checks the signal right here, voice both ways, and the batteries." **Handset:** "Signal here is too weak for alarm data. Try the box nearer a window, as Verizon's guide suggests, then run the alarm test again." |
| 0:58-1:16 | Bench: two counters side by side on one box: **TEST CALL: clear [k/k]** and **ALARM: confirmed [m/20]**. Then the window spot: **ALARM [20/20]**. Caption: *Same box, same minute · lab-baseline and second-network controls on the poster.* | **B:** "On our bench in a Rutgers ECE lab we measured why the alarm test matters. At a weak spot, the test call sounded clear [k of k] times. The alarm got through [m of 20]. Near the window, [20 of 20]. A clear call isn't proof." |
| 1:16-1:24 | Optional, only with a usability determination and signed release: a volunteer's hands set up the box; their voice. | **B:** "In our usability session, [k of n] older-adult volunteers set it up alone." *(Omit the beat if not cleared; the music carries.)* |
| 1:24-1:42 | Card 1: **46,000** *homes and businesses on these boxes today (Verizon, summer 2026 FCC filings)*. Card 2: **417,000** *more lines still on copper in two of Verizon's 2026 filings · replacements include fiber, mobile and boxes like this*. Four icons captioned *what the trial measures*. | **A:** "Verizon told the FCC this summer it has about forty-six thousand homes and businesses on these boxes. Two of its 2026 filings cover four hundred seventeen thousand more lines still on copper. Every green receipt is a chance to skip a repeat visit and a help-desk call, and to keep an alarm household with Verizon. The trial measures how often." |
| 1:42-1:54 | The PROVE icon on the box, then over elevator HELP B-roll (public car, no people). Caption: *illustration: no Rutgers line tested*. | **B:** "Our ask: put PROVE in one migration batch's self-install kits for thirty days, against a control group. Next, we're proposing the same proof to Rutgers Facilities for elevator HELP phones." |
| 1:54-2:00 | The receipt is torn off and handed to camera. End card: **PROVE · built at Rutgers ECE · student concept, not a Verizon product.** | **Both:** "Sent isn't received. PROVE." |

## The receipt (what prints on camera)
```
PROVE · test record                Oct [30] 2026 14:02
------------------------------------------------------
SIGNAL here   GOOD (clear enough for alarm data)
VOICE         CLEAR BOTH WAYS
ALARM         Receiver picked up · full code sent ·
              confirmed in [x.x] s
BATTERY       Installed · keeps working when unplugged
------------------------------------------------------
GREEN: no visit needed
Test record, not a guarantee. Confirm the test
with your alarm company, as you do today.
```
Print "box modem" signal values only if they come from the box itself. Otherwise label them "phone at the box (proxy)", and only on the poster.

## Decision table for the bench beat (lock on Nov 3)
| Bench result | What the video says |
|---|---|
| Weak-spot contrast measured (call clear, alarm short), and the second-network control shows the same | Script as written. On the poster: "the other network did the same". |
| Weak spot not measured by Nov 3 | Replace 0:58-1:16 with: "On our bench, Verizon's box confirmed [n of 50] alarm tests, in line with our lab baseline. Every result went to Verizon before this video." Use this only if the CIs overlap. |
| Verizon arm below the lab baseline | No number on screen. Say: "We measured where it falls short, and those results went to Verizon first." Show it on the poster only with the mentor's OK. |
| Swap test (T3) shows lost alarm registrations | Only with the mentor's written OK, say: "After a box swap, PROVE flagged a step the swap guide could add. It's already with Verizon." |
| **K1 fails (no live Verizon box by Oct 29)** | Use the full fallback script below. |

### K1 fallback script (complete, 2:00)
- **0:00-0:10:** same opening.
- **0:10-0:25 (B):** "Verizon replaces copper with boxes like this. Its guide asks customers with an alarm to test it. We built the check that makes that test answer back."
- **0:25-0:58:** demo on the lab-baseline arm. Lower third: *Lab line, not Verizon's network*.
- **0:58-1:16 (B):** "On a second carrier's wireless line in our lab, at a weak spot the test call sounded clear [k of k] times, while the alarm got through [m of 20]. A clear call isn't proof. Next week this runs on Verizon's box."
- **1:16-2:00:** as above.
- Expect about 60/95 (judge estimate). The live box is worth roughly 8-15 points.

## Shot list (Nov 4-6)
1. Armed keypad READY in a dark hallway (lab or a permitted room).
2. Both presses (PROVE, then keypad TEST) and the console ticks.
3. Weak spot (attenuator, captioned), the handset prompt, the move, then green.
4. Two counters side by side.
5. Receipt printing (macro).
6. Optional: volunteer hands, with the release on file.
7. Elevator HELP B-roll: public car, no people, nothing opened.
8. Two speakers, one clean take per line.
