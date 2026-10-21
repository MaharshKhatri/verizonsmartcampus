# Generation 6: v3 review (three returning judges, a film editor, a RAN/VoLTE engineer) and the v4 response

Full reviewer outputs: the scratchpad files `gen6_judges.json` and `gen6_specialists.txt` (agent transcripts). This file records the scores, the converging findings and what v4 changed.

## Scores
| Reviewer | v1 | v2 | v3 | v3 under row 2 / row 3 | Ceiling |
|---|---:|---:|---:|---|---:|
| Verizon GN&T executive (video #37 of 40) | 66 | 70 | 73 | 65 / 61 | 80 |
| Rutgers Vice Provost (non-specialist) | 67 | 71 | 76 | 69 / 64 | 84 |
| Rival team captain | 68 | 71 | 74 | 67 / 62 | 80 |

The film editor estimated Presentation at 18-20/30 as written and 24-26/30 with the edit decision list. The RAN engineer said: "the instinct is right, but the method can't support the claim yet".

## What all five agreed on (and v4's response)
1. **"Test call" meant two things.** At 0:22 it was the alarm's call; at 0:56 it was a voice call. → v4 uses "alarm test" and "phone call", never mixed.
2. **The bench beat showed Verizon's box failing alone first, and "did the same" meant overlapping CIs.** → Both carriers' rows appear from the first frame. "Same pattern" now requires delta's CI to sit above 0 on both boxes, the other box must be confirmed on carrier VoLTE, and the mentor must give written OK, cleared with whoever owns the open WC 26-227 proceeding.
3. **Verizon technology dropped out of the narration.** → "over Verizon's LTE network" is spoken again; "via Verizon device management" is a caption.
4. **The scale line regressed.** "Hundreds of thousands more" was heard as more boxes, and the truck-roll line was only arithmetic. → v4 uses three plain lines: 46,000 on these boxes; 5 million dial-out panels (AICC); a pocket tap costs less in parts than one truck roll.
5. **The trial could not power its own primary endpoint.** It needs about 3,200 installs per arm, against a 3,000-9,000 alarm-household estimate. → The primary endpoint is now the **catch rate**: alarm failures PROVE flags that a plain phone call passed, about ±3 points at 300 installs. Repeat dispatch is a secondary estimate.
6. **The demo staged a window move against an attenuator.** → The dial is turned back on camera, captioned "Signal turned up · like moving nearer a window".
7. **A Phase 1 passive tap was shown with Phase 2 behaviour** (speaking through the handset, reading the box's SINR, a status-screen icon). → v4 states Phase 1 honestly: it listens, reads box diagnostics or a labelled proxy, speaks through the technician's phone, and prints or texts the receipt. Phase 2 is labelled as not built.
8. **Rows 2 and 3 changed one sentence, while the rest of the cut still assumed the gap.** → A new **row 1b** (T2: the alarm number is not registered, the phone call is clear, the alarm fails) is sponsor-safe without a second carrier. Every row now lists every line it changes.
9. **The hook overclaimed.** Panels with periodic tests do find out eventually. → "may not learn it can't get through". Q&A #19 covers periodic tests.
10. **No person at stake.** → ARMED STAY, a cane by the door and a night light under a bedroom door (set dressing, nobody filmed).

## RAN engineer: method fixes (bench protocol T0/T5; code in progress)
- **Primary estimand, delta:** A90_voice − A90_alarm in dB, on each box against its own dropout point, with a cluster-bootstrap CI. It describes the alarm format's fragility, not the network.
- **Rig:**
  - The box sits inside the shield box, with an RSRP slope check (1.0 ± 0.15 dB/dB) and PCI/EARFCN logged at 1 Hz.
  - A 2-channel programmable attenuator.
  - A 90 s dwell plus a throwaway call after each step.
- **Trials:**
  - 20 voice and 20 alarm trials per 1 dB step near the edge, interleaved in random order, on two days, alternating boxes.
  - Setup failures are a separate curve.
  - P.862.1 in both directions plus blinded keywords, with a 3.5 sensitivity check.
- **T0:** how the box carries DTMF (in-band or RFC 4733), with ##21 on and off. It predicts which failure stage to expect.
- **Controls and logging:** freeze the receiver and trunk settings; re-decode with four decoders; a difference-in-differences against each box's own 0 dB rows; a tap-loading check.
- **Codes and stages:** two account codes, one with repeated adjacent digits and one without, to catch the concealment signature. `fail_stage` and trace-join columns.
- **Model honesty:**
  - `alarm.py` zeroes lost frames with no concealment, so it predicts ~23% alarm failure at 1% loss. That is QCI 1's design budget, so the result is implausible.
  - The "10 dB" bar is now labelled a worst-case placeholder.
  - Concealment and Gilbert-Elliott burst models are being added, with speech run through the same path.
- **Signal bar:** `load_rows` must drop voice, SIA, unregistered and other-box rows; fit one bar per box; use a cluster bootstrap; add a ceiling term.

## The best new ideas
- **Film editor: the sound signature.** The kiss-off tone, real bench audio, becomes the motif: a missing tone in the cold open and at the failure, ringing out at the fix, and alone at the end. "Every judge will have heard 39 music beds; none will have heard a missing tone."
- **RAN engineer: one RAN-native number.** Delta is a margin Verizon can apply to the address-level indoor coverage predictions already used to qualify homes for fixed wireless. That flags alarm homes near the edge before install, without customer data. Trial timestamps also let Verizon join its own eNB/IMS traces.
