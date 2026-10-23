# Action plan: Oct 21 → Nov 7 submission (PROVE)

Gates decide the cut. Owners: A (engineering lead), B (business lead), C (bench), D (video).

| Date | Who | Task | Gate / output |
|---|---|---|---|
| Oct 21-22 | B | Email the faculty sponsor (ECE/WINLAB) and the Verizon mentor (six questions plus the on-screen OK, `OUTREACH_KIT.md` §10). Ask Facilities for the elevator count and a one-line OK (§3). Request a not-human-subjects / usability determination for the older-adult session. | Sponsor yes |
| Oct 22 | C | Ask the mentor which DTMF mode the box uses (in-band or RFC 4733). Name the faculty advisor for the end card. Order the bench (`PROVE_LAB_BENCH_PROTOCOL.md` §1), **including the other carrier's wireless home-phone box, the 0-60 dB step attenuator, the RF shield box and the pocket-tap parts**. Start **two** activation channels for a Verizon box line (department business line + one consumer Voice Gateway if orderable). | **K1 starts** |
| Oct 23-25 | C | Assemble the receiver (Asterisk AlarmReceiver on a cloud VM with a G.711 DID). Factory-default the used panels. Run the LAN baseline arm (A). | Arm A ≈100% |
| Oct 24-26 | A | Fit the signal → delivery model on the first T5 data; wire the receipt to real bench logs; add the spoken fix prompt. | Code PR |
| Oct 26-28 | C | Arms B (other carrier) and C (Verizon box): T1, T2, T3 (swap). | **Gate: ##21 beat in or out by Oct 28** |
| Oct 29 | All | **K1 decision:** a live Verizon box by today, or use the fallback cut. | Go / fallback |
| Oct 29-31 | C | T5 sweep on both boxes at matched SINR (pre-registered "clear" = PESQ ≥ 3.0), T6 battery (runs overnight). | CSV complete; gap steps found or not |
| Oct 30-Nov 1 | B | Usability session: 3-5 volunteers, counts only. Elevator sticker census (public cars, no permission needed). | "x of N finished alone" |
| Nov 1-2 | D | Build every decision-table variant (rows 1, 1b, 2, 3) of the graphics for beats 0:27 and 1:00 from the synthetic CSV. | Templates ready |
| Nov 1-3 | A+B | Analysis with CIs (`analyze_prove_lab.py`): delta per box, the gap verdict, the setup curve, the signal bar per box. Pick the decision-table row. Send the sweep to the Verizon mentor; get the on-screen OK in writing, cleared with whoever owns the WC 26-227 docket. | Locked numbers |
| Nov 3 | All | **Row checklist.** Change all of these together: the 0:27 fault and model line, the PROVE voice line, B's 1:00 line and card, the exec summary's lay box, Q&A 11c and poster panel 2's headline. | One consistent story |
| Nov 4-6 | D | Film per the shot list, with both speakers on camera for the ask. Check the cut with `scripts/count_script_words.py` (≤ 255 words, every beat ≤ 150 wpm). | Rough cut |
| Nov 7 | All | Final cut and fact check (every spoken number traced to a CSV row or a source). Submit one day early. | **Submitted** |

## Rounds 2-3 (Feb 3 poster, Mar 4 final)
- **Poster "break it" table:**
  - press PROVE and take the receipt home;
  - attenuator knob for a "weak spot";
  - A/B panel switch;
  - battery pull.
- **Elevator WHO ANSWERS pilot** with Facilities and RUPD: challenge-response test calls on a few cars, caller-ID continuity, time to a person.
- **Older-adult A/B study:** guide alone vs guide + PROVE, n = 20-30, full task.
- **Verizon:** the 30-day trial proposal, with the KPIs filled in by the mentor.
