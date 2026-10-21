# Nov 8 video: "Sent isn't received" (PROVE), 2:00

**Two speakers:** A (engineering) and B (business). About 270 words.

**Rules for the cut** (from the Gen 4 judge panel):
- **Opening.** Open on the stakes, not on text cards. One number on screen per beat.
- **Content we leave out.** No docket numbers, rule sections, "paused" or "the regulator stopped checking" in the video; those belong in Q&A and on the poster. Never imply Verizon's network causes failures.
- **Numbers.** [Brackets] are filled only from `field_data/prove_lab.csv` (bench) or the usability log. Every number spoken is verified.
- **The hero receipt is green**, or goes FIX → re-run → green. It is a timestamped test record, never a guarantee.
- **Device.** Show the box's branding consistently and name the device tested ("Verizon Voice Gateway" or "Business Phone Connect / BPC100").

| Time | Visual | Audio |
|---|---|---|
| 0:00-0:10 | Night. A hallway alarm keypad chirps; its display reads **COMM OK / SENT**. Hold two beats of silence. On screen: *Sent. But did anyone get it?* | (silence, then) **A:** "When a copper phone line goes away, the alarm panel on it keeps dialing. Now it dials through a new box." |
| 0:10-0:25 | The hero device on the PROVE Lab bench at Rutgers ECE: Verizon's copper-replacement box, the panel on its alarm port, a corded phone. | **B:** "This is the box Verizon installs when the copper goes. Verizon already asks every customer to test their alarm when it goes in. We made that test one button, with a receipt." |
| 0:25-0:55 | A hand presses the keypad's communicator test. A console shows three ticks: **handshake heard → message valid → acknowledged**. A thermal receipt prints (lines below). Then the box is moved to a basement corner and re-run: **ALARM: no acknowledgement at this spot.** The handset speaks: "Move the box one metre toward a window and press PROVE again." Re-run: green. | **A:** "PROVE listens to the alarm's own test call through Verizon's network. Did the receiver answer? Was the message intact? Did the acknowledgement come back? It also checks the signal at this exact spot, voice both ways, and the backup batteries. If something's wrong, the phone itself tells you the fix." |
| 0:55-1:15 | Bench B-roll: three labelled cables (STRAIGHT WIRE / OTHER CARRIER / VERIZON BOX) into one receiver, and a live counter. On screen: **[n/50] acknowledged on Verizon's box** (one number). | **B:** "In our Rutgers PROVE Lab we measured it. Same panel, same receiver, three paths: straight wire, another carrier, and Verizon's box. On Verizon's box: [n of 50] acknowledged, [x] seconds on average. And where the signal is weak, alarm data fails before voice does." |
| 1:15-1:38 | One bar: **46,000**, then one bar: **417,000**. Then four icons: first-time-right, no repeat visit, no care call, alarm confirmed. | **A:** "Verizon reports about forty-six thousand fixed-wireless replacement customers today. Its 2026 filings cover four hundred seventeen thousand more lines. Every self-install that ends in a green receipt is a truck that doesn't roll, a call that doesn't come, and an alarm household that stays with Verizon." |
| 1:38-1:52 | Roadmap card: the PROVE icon on the box, then on an elevator HELP button. | **B:** "Our ask: put PROVE in one migration batch's self-install kits for thirty days, against a control group. Next, with Rutgers Facilities: the same proof for elevator HELP buttons." |
| 1:52-2:00 | The receipt is torn off and handed to camera. End card: **PROVE · Rutgers PROVE Lab (ECE) · student concept, not a Verizon product.** | **Both:** "Sent isn't received. PROVE." |

## The hero receipt (what prints on camera)
```
PROVE · test record            Oct [30] 2026 14:02
------------------------------------------------
SIGNAL here   GOOD  (box modem RSRQ [x] dB, SINR [x] dB)
VOICE         CLEAR BOTH WAYS
ALARM         Test reached receiver · message valid ·
              acknowledged in [x.x] s
BATTERY       Installed · runs on battery with AC off
------------------------------------------------
GREEN: no visit needed
Test record, not a guarantee. Your alarm company
also confirms the test on its side.
```

## Pre-written variants (choose after the bench, Nov 1-3)
- **Pass (expected):** use the script as written.
- **The swap test (T3) shows lost alarm-number registrations:**
  - Add one beat at 0:55: "And after a box swap done exactly by the guide, the alarm registration didn't come back. PROVE caught it."
  - Send the result to the Verizon mentor first.
  - Frame it as "a step the swap guide can add", never as a failure.
- **No live Verizon box by Oct 29 (Gate K1 fails):**
  - Film the LAN-baseline arm and say: "Next week this runs on Verizon's box."
  - Move the 46k/417k beat earlier.
  - Expect a lower score. The panel said a simulation-only video loses its top spot.

## Shot list (Nov 4-6)
1. Keypad SENT close-up in a dark hallway (any campus building with permission, or the lab).
2. Box on the bench, hands, receipt printing (macro).
3. Basement-corner re-run. Use the lab's SMA step attenuator for a repeatable "weak spot".
4. Three-path bench wide shot with the counter.
5. Elevator HELP button B-roll: public car, no people, no panel opened.
6. Two speakers, one take each per line, with a clean room tone.
