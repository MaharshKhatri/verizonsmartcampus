# Circadian: one campus forecast, three paychecks

A Rutgers entry for the **2026–27 Verizon Smart Campus Innovation Challenge** (Rutgers School of Engineering + Verizon). One privacy-safe, 30-minute occupancy forecast per building, built from the registrar timetable, the event calendar and aggregate device counts (campus Wi-Fi indoors, Verizon's network at the stadium, arena and outdoors), pays three parties:

1. **The campus**: ventilation by headcount with comfort-safe setback, demand response and guaranteed network slices, sold by Verizon Business.
2. **Verizon**: event-day energy saving without a manual "event mode" (pre-wake venue radios instead of locking them on), plus triage that runs remote fixes before a truck rolls.
3. **Students**: a crowd and quiet-space navigator and guaranteed service at events.

> Student concept and simulation. Not a Verizon product. All campus activity in the prototype is simulated.

## Quick start (Python 3.10+, no installs)

```bash
python3 scripts/build_all.py          # train, simulate 8 scenarios + ablations, run the CFO model, write dashboard data (~2 min)
open prototype/dashboard/index.html   # offline replay (any browser, no server)
python3 prototype/server.py           # live mode at http://localhost:8765: inject crowds/faults, type slice requests
python3 -m unittest discover -s tests # verification suite
python3 CFO_10K_MODEL.py --print      # financial model only
```

## What's here

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

## How the engine works

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
