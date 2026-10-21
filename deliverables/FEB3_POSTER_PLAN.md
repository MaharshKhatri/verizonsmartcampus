# Feb 3 poster round: plan (PROVE)

**Goal:** a judge walks up, presses PROVE, breaks it, fixes it, and leaves holding a receipt, in under 3 minutes. The poster backs every claim the Nov 8 video made, including the ones the video could only caption ("full sweep on poster", "another carrier's line did the same").

## 1. Layout (48 × 36 in landscape; read left to right in about 90 s)
| Panel | Headline | Content |
|---|---|---|
| 1. The gap | **A clear call isn't proof.** | One photo: the box, an alarm keypad reading ARMED AWAY, and a corded phone. Three short lines from Verizon's own guide ("determined by your testing ... at time of install"; "may result in your alarm not working"; the swap guide's "make a test call"). One sentence quoting the FCC's "encourage carriers" language. Sources as QR codes, not docket numbers. |
| 2. The sweep (hero figure) | **Written after the data.** Row 1: *Alarm data needed [X] dB more signal than a clear call*. Otherwise the measured null. | **X axis:** dB of attenuation above each box's own dropout point, with the box's RSRP on a top axis. **Y axis:** share of trials. Per box, three curves with Wilson CIs and the fitted logistics: phone call clear (P.862.1 ≥ 3.0 both ways + keywords), alarm confirmed, and call setup OK. Delta is marked as a bracket with its bootstrap CI. Small multiples: Verizon's box and the other carrier's box side by side, same axes. The caption gives the pre-registered rules, n per step, and the DTMF transport found in T0. *Built from `analyze_prove_lab.py`; the mentor approves before printing.* |
| 3. How PROVE checks | **Picked up · full code sent · confirmed** | A timeline of one real tap recording (`tap.py`): the handshake, 16 DTMF digits with the checksum, the kiss-off, each with its time. A small inset of the learned signal bar: the logistic curve, the 90% point with its CI, and "n = [N] bench alarm tests". |
| 4. The receipt | **A test record, not a guarantee** | The real printed receipt, mounted. The three verdicts (GREEN / FIX AND RE-RUN / VISIT NEEDED) with their spoken fix lines. The hash-chain ledger in one diagram: "every receipt can be checked, none can be quietly edited". |
| 5. The ask | **Phase 1: a pocket tap, no firmware** | A photo of the tap with its bill of materials and cost. The two-phase table. The pre-registered success rule, including the power statement (about 3,200 installs per arm to detect a 2-point drop). "1 point = 10 truck rolls per 1,000 installs." |
| 6. Rutgers | **The lifeline still without proof** | Fire communicators (2020) and blue lights (2023) are already self-reporting. Elevator HELP phones are next: the Facilities walk-through status, the sticker-census counts (no locations), and the WHO ANSWERS challenge-response diagram. The usability result: "k of n followed the spoken fix without help". |
| Footer | | Honest negatives (the passive detector failed; any arm below baseline). "Student concept, not a Verizon product." Team, faculty sponsor, QR code to the repo and the live console. |

## 2. The "break it" table (live, on the table under the poster)
| Station | What the judge does | What they see |
|---|---|---|
| **A. Press PROVE** | Presses PROVE, then the keypad TEST. | Three ticks on the console. The receipt prints and they keep it. |
| **B. Weak spot** (labelled *live: it may pass*) | Turns the attenuator knob to the marked band. | In the gap band, alarms fail only some of the time, so this station is honest about chance. Voice still sounds fine on the handset. When the ALARM line goes to "confirmation ✗", the PROVE phone speaks the fix. They turn the knob back and get green. Each morning a 15-minute 1 dB scout at the venue sets the band where alarm confirmation is lowest while voice is still clear. |
| **C. Forget the number** | Flips the A/B switch to a panel whose alarm number is not registered (##21 cleared). | FIX AND RE-RUN: "re-enter the alarm number". |
| **D. Pull the battery** | Pulls the box's AA tray and unplugs AC. | BATTERY: FIX ("insert batteries"). The receipt shows the battery check is real, not a guess. |
| **E. Tamper with a receipt** | Edits one receipt in the browser ledger demo. | The hash chain breaks at that receipt, in red. |

## 3. Stage reliability (the demo must never depend on the hall's signal)
- **Receiver:** Asterisk on a cloud VM, with a backup on the Pi. A pre-recorded tap WAV for each station can be replayed through `tap.py` if the live line drops, labelled "recorded on [date]".
- **Signal:** the box sits inside the RF shield box and hears only what passes the attenuator. Its antenna is outside, so the hall's signal still sets the starting point; we recalibrate the dial each morning. If the hall has no usable Verizon coverage, station B runs on recorded calls through `tap.py`, labelled as such, and station A runs on the other carrier's box with a banner saying so.
- **Spares:**
  - two pre-programmed panels;
  - spare AAs;
  - a printed copy of the hero figure;
  - a phone hotspot for the console.
- **Rehearsal:** the full 3-minute walk-up, run 10 times by someone outside the team, before Jan 30.

## 4. What must be true by Feb 3
| Item | Owner | Due |
|---|---|---|
| The T5 sweep on both boxes, including the matched-SINR table, approved by the mentor for printing | C + B | Dec 15 |
| Learned signal bar refit with n ≥ 200 bench alarm tests, with its CI | A | Dec 20 |
| Usability: n = 8-12, Part 2 (spoken fix), counts only | B | Jan 15 |
| Facilities: elevator count and walk-through status, in writing | B | Jan 15 |
| Poster print-ready (an outside reader reads it in 90 s and repeats the claim) | D | Jan 27 |
| Break-it table rehearsed 10× | All | Jan 30 |

## 5. Judge questions the poster must answer without us speaking
1. "Is this Verizon's fault?" Panel 2 shows the same margin on the other carrier's box, and states that the number describes the alarm format, not the network.
2. "Is the AI real?" Panel 3 shows the learned bar with its n and CI.
3. "What does Verizon do on Monday?" Panel 5 gives Phase 1, the tap, the cost and the success rule.
4. "Why Rutgers?" Panel 6 covers the elevator HELP phones, the bench and the volunteers.
