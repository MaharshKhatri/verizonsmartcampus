# Action plan: Oct 21 → Nov 7 submission (PROVE)

Gates decide the cut. Owners: A (engineering lead), B (business lead), C (bench), D (video).

| Date | Who | Task | Gate / output |
|---|---|---|---|
| Oct 21-22 | B | Email the faculty sponsor (ECE/WINLAB) and the Verizon mentor (five questions, `OUTREACH_KIT.md` §10). Request a not-human-subjects / usability determination for the older-adult session. | Sponsor yes |
| Oct 22 | C | Order the bench (`PROVE_LAB_BENCH_PROTOCOL.md` §1). Start **two** activation channels for a Verizon box line (department business line + one consumer Voice Gateway if orderable). | **K1 starts** |
| Oct 23-25 | C | Assemble the receiver (Asterisk AlarmReceiver on a cloud VM with a G.711 DID). Factory-default the used panels. Run the LAN baseline arm (A). | Arm A ≈100% |
| Oct 24-26 | A | Fit the signal → delivery model on the first T5 data; wire the receipt to real bench logs; add the spoken fix prompt. | Code PR |
| Oct 26-28 | C | Arms B (other carrier) and C (Verizon box): T1, T2, T3 (swap). | **Gate: ##21 beat in or out by Oct 28** |
| Oct 29 | All | **K1 decision:** a live Verizon box by today, or use the fallback cut. | Go / fallback |
| Oct 29-31 | C | T5 placement (with attenuators), T6 battery (runs overnight). | CSV complete |
| Oct 30-Nov 1 | B | Usability session: 3-5 volunteers, counts only. Elevator sticker census (public cars, no permission needed). | "x of N finished alone" |
| Nov 1-3 | A+B | Analysis with CIs. Pick the one measured line for the video. Send any failure to the Verizon mentor first. | Locked numbers |
| Nov 4-6 | D | Film per the shot list. Two-speaker voice-over. Captions. | Rough cut |
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
