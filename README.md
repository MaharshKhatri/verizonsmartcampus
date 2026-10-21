# PROVE: sent isn't received

A Rutgers entry for the **2026-27 Verizon Smart Campus Innovation Challenge**.

When Verizon retires a copper line, the home or business gets a replacement box on Verizon's wireless network. Alarm panels, medical alerts and elevator HELP buttons keep dialing through that box. Verizon's own guide says alarm compatibility "is determined by your testing ... at time of install". A keypad that says "sent" cannot tell whether anyone received the message.

**PROVE makes every lifeline Verizon moves arrive with proof that it still reaches someone.**
- **What it checks:** the alarm's own test call through Verizon's live network (handshake, valid message, acknowledgement), the signal at the box's exact spot judged on its worst season, voice both ways, and battery backup.
- **What it prints:** a spoken and printed test record, either GREEN, FIX AND RE-RUN, or VISIT NEEDED.
- **On campus:** a Rutgers PROVE Lab bench, plus an elevator "Who answers?" pilot for the finals.

> Student concept. Not a Verizon product. Prototype results are simulations labelled as such until the bench measures them. We never dial 911.

## Quick start (Python 3.10+ with numpy)

```bash
python3 -m prototype.prove.export          # build console data (~1 min)
open prototype/prove/console/index.html    # offline console (any browser)
python3 -m prototype.prove.server          # live rig mode at http://localhost:8766
python3 -m unittest discover -s tests      # 60 tests
python3 scripts/analyze_prove_lab.py field_data/prove_lab.csv   # bench results with Wilson CIs (after the bench runs)
```

## Start here

| Path | What it is |
|---|---|
| [`deliverables/`](deliverables/) | Nov 8 video script, 2-page executive summary, judge Q&A bible, action plan, bench protocol, outreach kit |
| [`STATE.json`](STATE.json) | Current champion, verified facts, honest negatives, kill gates |
| [`EVOLUTION_LOG.md`](EVOLUTION_LOG.md) | Four generations: Circadian, Last Copper, then PROVE, and why each changed |
| [`IDEA_LEADERBOARD.md`](IDEA_LEADERBOARD.md) | Gen 3 and Gen 4 tournaments; five-judge finals |
| [`research/06_gen4_verification.md`](research/06_gen4_verification.md) | 22 verified research answers with sources |
| [`research/sources/`](research/sources/) | Primary texts: Verizon notice and device guides, FCC orders, eCFR rule versions, the 2026 wire-center dataset |
| [`research/07`-`10`](research/) | 60 Gen 4 ideas, founder contender, four-persona screen, finalists, red teams and judges |
| [`prototype/prove/`](prototype/prove/) | PROVE engine: `alarm.py`, `install.py`, `migration.py`, `answer.py`, `acoustic.py`, `supervisor.py`, `triage.py`, `ledger.py`, `fleet.py`, `capacity.py`, `signal_model.py`, `console/` |

## Earlier generations (kept as an engineering bench)

Circadian (Gen 1-2) was retired after a Gen 3 red-team kill; its code under `prototype/engine`, `prototype/dashboard` and `CFO_10K_MODEL.py` remains, and its deliverables are in `deliverables/archive_circadian/`.

### Circadian quick start (Gen 1-2, archived)

```bash
python3 scripts/build_all.py          # train, simulate 8 scenarios + ablations, run the CFO model, write dashboard data (~2 min)
open prototype/dashboard/index.html   # offline replay (any browser, no server)
python3 prototype/server.py           # live mode at http://localhost:8765: inject crowds/faults, type slice requests
python3 -m unittest discover -s tests # verification suite
python3 CFO_10K_MODEL.py --print      # financial model only
```

### Circadian files

| Path | What it is |
|---|---|
| [`deliverables/`](deliverables/) | **Start here.** 2-minute video script, 2-page executive summary, 25-question judge Q&A, action plan |
| [`RESEARCH_DOSSIER.md`](RESEARCH_DOSSIER.md) | Verified facts, the corrections ledger for the original brief, "safe to say" numbers |
| [`research/`](research/) | Four sourced research files (SEC/10-K, RAN energy + standards, competition + Rutgers, market + pricing) |
| [`IDEA_LEADERBOARD.md`](IDEA_LEADERBOARD.md) | 13 theses scored on the CEO rubric and the official rubric; red team; synthesis |
| [`CFO_10K_MODEL.py`](CFO_10K_MODEL.py) → [`FINANCIAL_PROJECTION.md`](FINANCIAL_PROJECTION.md), [`verizon_10k_sensitivity.csv`](verizon_10k_sensitivity.csv) | Pilot + national model mapped to 10-K lines; bear/base/bull, Monte Carlo, tornado |
| [`prototype/engine/`](prototype/engine/) | Digital twin, forecaster, planner, HVAC, triage, slicing, ledger (standard library only) |
| [`prototype/dashboard/index.html`](prototype/dashboard/index.html) | Command center (single file, works offline) |
| [`prototype/server.py`](prototype/server.py) | Live engine API for the dashboard |
| [`tests/`](tests/) | Verification suite |
| [`PROMPT.md`](PROMPT.md), [`STATE.json`](STATE.json), [`EVOLUTION_LOG.md`](EVOLUTION_LOG.md), [`scripts/evolve_loop.sh`](scripts/evolve_loop.sh) | The multi-generation research protocol and its state |

### How the Circadian engine works

```
truth (timetable x per-building bias x random attendance + noise + unannounced crowds)   <- never seen
   │
   ├── device counts, k ≥ 20 (Wi-Fi indoors, carrier/DAS at venues) + timetable/ticketing prior
   │        └── Forecaster (ridge regression per building type x horizon, P90 from residuals)
   │                 ├── Planner: latency-aware deepest-safe sleep (5 radio modes), slice reservations,
   │                 │            measured-load floor, SLA guard, bandit-learned safety margins
   │                 ├── HVAC: setback / pre-condition / ventilation by headcount / demand response
   │                 └── Student app: quiet spots, crowds in 30 min, connection quality
   ├── Triage: intent-aware fault detection, naive-Bayes diagnosis, remote playbooks, outage compensation
   └── Ledger: kWh, congestion, truck rolls, tickets, slices -> Verizon 10-K lines
```

**The experiment that matters:** *today's practice* (a traffic-history AI with learned margins **plus the operator's manual event mode**) and *Circadian* share one planner, one set of radios, one SLA guard and one margin learner; only the forecast differs. On ordinary days they tie, and the repo says so. On event days event mode protects quality by locking venue radios on for hours; Circadian keeps the same quality and saves more (game day: 65% vs 58% of venue radio energy). Over a campus year that is only ~0.3% of radio energy: the money is the B2B product.

**Evidence and ablations** (dashboard Evidence tab, `prototype/out/evidence.json`): efficient frontier, event-mode comparison, forecast error vs today's AI and vs simple rules, HVAC with and without a forecast, sensing ablation (Wi-Fi / carrier / both), bus-feed ablation, fault-storm Monte Carlo.

## Honesty notes
- Radio counts in the twin are a representative deployment, not Verizon's inventory, and absolute savings versus always-on are inflated by an idealised layout. Only *relative* results (Circadian vs today's practice) feed the financial model.
- Indoors, campus Wi-Fi is the better sensor; Verizon-only counts are worse than the timetable there. Verizon's counts matter at venues and outdoors.
- HVAC kWh come almost entirely from ventilation by headcount; the forecast's job is comfort-safe setback.
- Sleep-mode savings come from published sources (research/02); wake latencies are conservative estimates (no vendor publishes them).
- Every financial input is tagged with a source or marked `est`. Base 5-year NPV is +$3.4M and depends on network pull-through; software alone is NPV-negative.
- An independent red team audited Generation 1; two claims were retracted (EVOLUTION_LOG.md).

## Running the evolutionary loop locally
`PROMPT.md` is a multi-generation research protocol. `scripts/evolve_loop.sh` runs Claude Code once per generation, resuming from `STATE.json`, and checkpoints each generation as a local git commit. It stops on a non-zero exit (e.g. usage limit), a `STOP` file, or `MAX_GENERATIONS`. It passes `--dangerously-skip-permissions` by default, so run it in a container or VM, or override with `PERMISSION_FLAGS="--permission-mode acceptEdits"`.
