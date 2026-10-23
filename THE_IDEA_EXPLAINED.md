# PROVE, explained from zero

*For anyone who knows nothing about phones, alarms or this competition. Written Oct 23, 2026.*

---

## 1. The competition in one paragraph
The **Verizon Smart Campus Innovation Challenge** at Rutgers asks student teams to pitch an idea that uses technology to make a campus, and the communities around it, work better. Verizon sponsors it, and Verizon and Rutgers people judge it. There are three rounds:

| Round | Date | Format |
|---|---|---|
| 1 | **Nov 8, 2026** | A **2-minute video** |
| 2 | Feb 3, 2027 | A poster session |
| 3 | Mar 4, 2027 | The finals |

The scoring:

| Category | Points | What it means |
|---|---:|---|
| Impact | 30 | Does it matter, and how much? |
| Feasibility | 15 | Can it actually be done? |
| Content | 15 | Is it substantive and technically sound? |
| Creativity | 5 | Is it original? |
| Presentation | 30 | Is it clear and memorable? |

Roughly 40 teams compete, and most of them will use AI tools like Claude, so plenty of polished but similar pitches are coming.

## 2. Our idea in one sentence
**PROVE is a pocket tester and an AI check that proves a home alarm can still call for help after its old landline is replaced by one of Verizon's new wireless boxes. A phone call sounding fine is not proof the alarm works.**

The tagline: **"Sent isn't received."**

---

## 3. The background, step by step

### 3a. Landlines are being switched off
- **The old network is being retired.** The old phone network runs on copper wires, and phone companies are shutting it down because it is old and expensive. In 2026 Verizon filed notices to retire copper in **1,763 telephone exchanges ("wire centers") across 21 states**. One of them is **Piscataway**, home to Rutgers' Busch and Livingston campuses, on or after **Dec 10, 2026**.
- **What replaces a copper line:**
  - fiber internet phone service;
  - a cell phone;
  - a small **wireless box** (Verizon calls them Voice Connect, Voice Gateway or Business Phone Connect). You plug your old house phone and your alarm into it, and it sends the calls over Verizon's cellular (LTE) network instead of copper.
- **How many lines.** Verizon told the federal regulator (the FCC) this summer that about **46,000** homes and businesses already use these boxes. Two of its 2026 filings cover about **417,000** more lines leaving copper.

### 3b. Many home alarms still "phone home"
- **How a monitored alarm reports.** When a monitored burglar or fire alarm goes off, the alarm panel (the box in a closet with the keypad by the door) dials the alarm company **over the phone line**. It doesn't talk; it **beeps**, in a code called Contact ID. The exchange has three steps:
  1. The alarm company's computer answers with a "ready" tone.
  2. The panel sends a 16-digit code of beeps: who it is and what happened.
  3. The alarm company's computer sends back a short **"got it" tone** (the industry calls it the kiss-off).
- **If the "got it" never arrives,** the panel tries again a few times, and then gives up.
- **How many panels.** The alarm industry told the FCC that about **5 million** alarm panels in the US still dial out over phone lines.

### 3c. The problem nobody is checking
- **Voice and alarms are not the same.** A wireless box built for voice can carry a phone conversation fine while **the alarm's beeps get garbled**, especially where the cell signal is weak (a basement or an inner room). Our ears forgive a choppy call; an alarm receiver does not forgive one wrong beep.
- **Verizon's own instructions put the test on the customer.** The box's guide says alarm compatibility "**is determined by your testing ... at time of install**". It also says "**Failure to verify may result in your alarm not working.**" The guide for swapping boxes says only "**make a test call**".
- **That test can't catch the problem.** A clear test call proves the *voice* works, not the *alarm*. **A clear call isn't proof.**
- **The rules no longer require a check.** In March 2026 the FCC declined to require phone companies to guarantee alarm compatibility during these switches. It only "encourage[d] carriers ... to prevent alarm signaling failures". Since Oct 15, 2026, no federal rule requires a carrier to show, home by home, that the replacement works as well as copper did.
- **So the alarm may have stopped getting through, and nobody finds out until the night it has to call for help.** Many panels do run periodic self-tests, but those surface days later as a confusing trouble beep, after the installer has gone. That is the gap: **sent isn't received.**

---

## 4. The solution: PROVE

### 4a. What it does
At install, the technician (or the customer) presses PROVE, then the alarm's own TEST button. PROVE listens on the line and answers three questions:
1. **Did the alarm company pick up?**
2. **Did the panel send its full code?**
3. **Did the "got it" come back?**

It also checks the **signal** at the box's exact spot, **voice** both ways, and that **batteries** are in (the box has a battery backup for power outages). Then it gives a verdict, spoken aloud and printed as a **receipt**:
- **GREEN: all checks passed.**
- **FIX AND RE-RUN**, with a plain instruction such as "Signal too weak for alarms. Try nearer a window, then test again", "re-enter the alarm number" or "insert batteries".
- **VISIT NEEDED**, naming who must come: Verizon or the alarm company.

The receipt is a **test record, not a guarantee**. The alarm company still confirms the test on its side, as it does today.

### 4b. Where the AI is (the competition's "AI-Driven Automation" pillar)
- **A learned signal bar.** From our lab tests, PROVE learns how strong the cell signal must be for alarm beeps, not just voice, to get through. It is a model fitted to measured data, with a margin of error, not a guess about "bars". It decides GREEN or "move the box".
- **Fault triage.** A second model works out *who* should fix a failure: Verizon's network, the alarm company, the customer's batteries, or a line not yet moved. It is 92% accurate in simulation, and 87% when our assumptions are deliberately wrong.

### 4c. How it ships (two phases)
| Phase | What | Cost | Why it matters |
|---|---|---|---|
| **1. Pocket tester** | A Raspberry Pi (a $15-80 mini-computer) with a safe, isolated clip onto the box's alarm port, a sound card, a battery and a tiny printer. Technicians carry it on alarm installs. | **About $100-200 in parts, less than one repair-truck visit** | Verizon could try it *next quarter* with no change to the box or the network. |
| **2. Built into the box** | The same checks as a software update, pushed through Verizon's device management, for people who install the box themselves. | Engineering time | It scales to every box. The math needs well under 1% of a small chip and about 2 KB of memory (our estimate; not yet tested on the real box). |

### 4d. The Rutgers part
- **A PROVE bench in a Rutgers engineering (ECE) lab** produces measured alarm-over-wireless data that we could not find published anywhere.
- **Elevator HELP phones** are the campus extension, for the finals. Rutgers already made its fire alarms (2020) and blue-light phones (2023) self-reporting. Elevator emergency phones are the lifeline still without routine proof that someone answers. We are *proposing* a pre-announced test to Rutgers Facilities. It would check that someone answers, within the 45-second rule in the elevator safety code, and knows which car is calling.
- **A short usability session with older-adult volunteers** (only with the university's research-ethics sign-off) to see if they can follow PROVE's spoken fix on their own.

---

## 5. The proof: the bench experiment
The single most valuable thing we can have that the other ~39 teams can't is **a real measurement on Verizon's real box.**

**The setup.** A real (used, factory-reset) alarm panel plugs into Verizon's box. The box calls *our own* stand-in alarm-company receiver. We never call 911 or a real alarm company. The box sits inside a metal shield box, and a dial (an "RF attenuator") turns the cell signal down step by step, like moving the box deeper into a basement.

**The measurement.** At each step we make 20 ordinary phone calls and 20 alarm tests, mixed in random order. We score whether each call "sounds clear" with a standard speech-quality score, set *before* we start, and whether each alarm got its "got it". The headline number is **how many extra decibels of signal the alarm needs compared with a clear phone call** (we call it *delta*).

**The fairness control.** We run the identical test on **another carrier's** wireless phone box. If both behave the same, the problem is weak signal plus fragile alarm beeps, **not Verizon**. That matters, because Verizon is the sponsor and we never want to imply its network is bad. Results go to our Verizon mentor *before* anything is published.

**The decision table.** We don't know the result yet, so the script has a version for every outcome:

| Outcome | What the video says |
|---|---|
| **Gap on both boxes** (the expected case) | "At one weak signal, phone calls on two carriers' boxes sounded clear 19 of 20 times. Alarms got through about 9 of 20 on both. It's the weak signal, not the carrier. A clear call isn't proof." |
| **No signal gap, but alarms fail when the alarm number isn't registered in the box** (a setup step in Verizon's own guide) | We show that instead. It is just as strong and completely sponsor-safe. |
| **Gap only on Verizon's box** | No numbers on screen, and the results go privately to Verizon. |
| **No gap at all** | The pitch becomes "PROVE catches setup mistakes before the technician leaves", and we say so honestly. |
| **We can't get a live Verizon box by Oct 29** | A complete backup script runs on the other carrier's box. |

*(The numbers in the table are examples; the real ones come from the bench.)*

---

## 6. The 2-minute video, beat by beat (v5)
| Time | What you see | What you hear |
|---|---|---|
| 0:00 | Dark hallway, alarm keypad reads ARMED STAY. On screen: *An alarm, calling for help*, then **Sent ✓**, then **Received?** | The alarm's real beeps, then **silence** where the "got it" tone should be. |
| 0:05 | A phone cord pulled from an old wall jack. | "When a landline is replaced, an alarm can stop getting through, and no one may notice until the night it calls for help." |
| 0:15 | A student with Verizon's box, Verizon's guide page highlighted, the pocket tester clipped on. | "Its guide asks alarm owners to test. Our pocket tester turns that into one check with a receipt." |
| 0:27 | Press PROVE, press TEST, ticks appear. Freeze on **SENT ✓ · CONFIRMED ✗**, the music cuts out. The phone says "Signal too weak for alarms. Try nearer a window." Signal turned up, re-test, **the "got it" tone rings out**, three green ticks, the receipt prints. | The three questions. "PROVE learned from our lab tests how strong is enough." |
| 1:00 | A student lifts the phone: "Can you hear me? Loud and clear." Then a card: phone calls ✓ on both carriers, alarms only about half. | "...It's the weak signal, not the carrier. **A clear call isn't proof.**" |
| 1:21 | **5,000,000** dial-out alarm panels. A tester next to a repair truck. | "A pocket tester costs less than one repair-truck visit." |
| 1:36 | Both students. The tester. An elevator HELP button. | "Our ask: a thirty-day trial, technicians carrying this tester on alarm installs, counting the failures it catches that a phone-call check would pass. Then a software update puts it in the box. At Rutgers, we're proposing the same proof for elevator HELP phones." |
| 1:54 | The receipt pushed at the camera. The "got it" tone plays alone. | "**Sent isn't received.** PROVE it." |

The sound of the alarm's "got it" tone, and its absence, is the film's signature. No other team will have it.

---

## 7. Why this wins

### Against the rubric
| Category | Points | Why PROVE scores |
|---|---:|---|
| **Impact** | 30 | Millions of alarms and a real, current switch-off (Piscataway, Dec 10). The trial counts the alarm failures caught that a phone-call check would have passed, measurable in one batch of installs. |
| **Feasibility** | 15 | Phase 1 is a $100-200 tester with no network or box changes. Code already runs: a 67-test prototype that decodes real alarm audio. |
| **Content** | 15 | It is built on Verizon's own LTE network, device management and guides. It produces measured data with confidence intervals. |
| **Creativity** | 5 | Nobody else will pitch "your phone call works but your alarm doesn't". |
| **Presentation** | 30 | One simple idea and one memorable line. The silent missing tone is something judges have never heard. |

### Against ~40 AI-assisted teams
- **Most will pitch generic ideas:** smart energy, campus digital twins, AI chatbots, private 5G. Those are easy for AI to write and hard to tell apart.
- **PROVE comes from Verizon's own documents and a federal rule change this month.** It has a **real lab measurement** no AI can make up, and it is designed to *help* the sponsor rather than embarrass it.

### How the judges scored our drafts
We ran repeated simulated judging rounds, each with three judges: a Verizon network executive, a non-technical Rutgers Vice Provost and a harsh rival captain.

| Draft | Scores (out of 95) |
|---|---|
| First draft | 66, 67, 68 |
| Second draft | 70, 71, 71 |
| Third draft | 73, 76, 74 |

Their estimated ceiling with real bench numbers is **about 80-84**. Three lay viewers gave the v4 script 6.5-7.5 out of 10. All three remembered "Sent isn't received", the calls-fine/alarms-fail result and the 5 million figure. v5 fixes where they got lost.

---

## 8. Honest limits (say these before a judge does)
- **The bench result isn't in yet.** Every number in [brackets] in the script waits for it.
- **We don't know how many of Verizon's box customers have alarms.** A crude estimate is 3,000-9,000 of the 46,000. Verizon can count exactly: every box with an alarm number registered.
- **Alarm companies are moving many panels to their own cellular radios.** PROVE is for the homes still plugged into the box, and the same checks cover voice, battery and elevator phones.
- **A "got it" tone means the receiver accepted the message, not that a person acted on it.** That's why the receipt is a test record, not a guarantee.
- **One idea we tested failed:** detecting "who answered" by listening. We say so, and switched to a "press 1 to confirm" test.

---

## 9. What has to happen next (from today, Oct 23)
**Only you, the team, can do these, and they are urgent:**
1. **Faculty sponsor (today).** Email an ECE/WINLAB professor (template in `deliverables/OUTREACH_KIT.md` §1). Their name unlocks the business phone line and the lab.
2. **Order the bench (today, rush shipping).** It was planned for Oct 22, so it is now one day late. The list is in `deliverables/PROVE_LAB_BENCH_PROTOCOL.md` §1 (about $1,200-2,000): Verizon's box on a department business line, a used alarm panel, a Raspberry Pi receiver, another carrier's LTE phone box, a programmable attenuator and a shield box.
3. **Verizon mentor (today).** Send the six questions (`OUTREACH_KIT.md` §10). Ask how the box carries alarm beeps, and whether we may show results on screen.
4. **Research-ethics determination** for the volunteer session, if we want it.
5. **Rutgers Facilities:** an elevator count and a one-line "open to a pre-announced test".
6. **GitHub:** create a `main` branch so the draft pull request can be opened.

**The calendar:**

| Date | Milestone |
|---|---|
| **Oct 29** | Gate: a live Verizon box, or switch to the backup script |
| Oct 29-31 | Run the sweep |
| **Nov 3** | Lock the numbers and pick the decision-table row |
| Nov 4-6 | Film |
| **Nov 7** | Submit, one day early |
| Feb 3 | Poster with a hands-on "break it" table: judges turn the signal knob themselves and take a receipt home |
| Mar 4 | Finals, with the elevator pilot if Facilities agrees |

---

## 10. Where everything lives in the repo
| What | File |
|---|---|
| The video script (v5) | `deliverables/NOV8_VIDEO_PITCH_SCRIPT.md` |
| The 2-page summary for judges | `deliverables/EXECUTIVE_SUMMARY_2PAGE.md` |
| Answers to 21+ tough judge questions | `deliverables/JUDGE_QA_DEFENSE_BIBLE.md` |
| The lab experiment, step by step | `deliverables/PROVE_LAB_BENCH_PROTOCOL.md` |
| Emails to send | `deliverables/OUTREACH_KIT.md` |
| Day-by-day plan | `deliverables/ACTION_PLAN.md` |
| Poster round | `deliverables/FEB3_POSTER_PLAN.md` |
| Checklist so edits don't drop what judges liked | `deliverables/CREDITED_ELEMENTS.md` |
| The working code (alarm decoder, pocket tester, AI signal bar, receipts, analysis) | `prototype/prove/`, `scripts/` |
| Every source document (Verizon guides, FCC orders, notices) | `research/sources/` |
| How we got here (7 generations of research and judging) | `EVOLUTION_LOG.md`, `research/` |
