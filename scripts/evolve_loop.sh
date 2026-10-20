#!/usr/bin/env bash
# Runs the Unbounded Evolutionary Protocol (PROMPT.md) one generation per
# Claude Code invocation, so every generation starts with a fresh context and
# resumes from STATE.json / EVOLUTION_LOG.md on disk.
#
# Stops when any of these happens:
#   - `claude` exits non-zero (e.g. the account usage limit is reached)
#   - a file named STOP exists in the repo root   (touch STOP)
#   - MAX_GENERATIONS generations have run         (0 = unlimited, the default)
#
# Each finished generation is checkpointed as a local git commit (never pushed),
# so a bad generation can be rolled back with `git reset --hard HEAD~1`.
#
# Usage:
#   scripts/evolve_loop.sh
#   MAX_GENERATIONS=3 scripts/evolve_loop.sh
#   PERMISSION_FLAGS="--permission-mode acceptEdits" scripts/evolve_loop.sh
set -u

cd "$(dirname "$0")/.."

MAX_GENERATIONS="${MAX_GENERATIONS:-0}"
PERMISSION_FLAGS="${PERMISSION_FLAGS:---dangerously-skip-permissions}"
AUTO_COMMIT="${AUTO_COMMIT:-1}"
PAUSE_SECONDS="${PAUSE_SECONDS:-2}"

PROMPT='Read PROMPT.md (Section 0 first), STATE.json and the tail of EVOLUTION_LOG.md. Resume the Unbounded Evolutionary Protocol from the current generation: spawn parallel sub-agents, red-team the current champion thesis and the five open weaknesses in STATE.json, upgrade the financial model and the prototype, run `python3 -m unittest discover -s tests` and `python3 scripts/build_all.py` until both pass, then update STATE.json, IDEA_LEADERBOARD.md and EVOLUTION_LOG.md and finish this generation.'

generation=0
while :; do
  if [ -f STOP ]; then
    echo "STOP file found; exiting after ${generation} generation(s)."
    break
  fi
  if [ "$MAX_GENERATIONS" -gt 0 ] && [ "$generation" -ge "$MAX_GENERATIONS" ]; then
    echo "Reached MAX_GENERATIONS=${MAX_GENERATIONS}."
    break
  fi

  echo "=== $(date '+%Y-%m-%d %H:%M:%S') starting loop iteration $((generation + 1)) ==="
  # shellcheck disable=SC2086
  if ! claude -p $PERMISSION_FLAGS "$PROMPT"; then
    echo "claude exited non-zero (usage limit or error); stopping."
    break
  fi

  if [ "$AUTO_COMMIT" = "1" ] && [ -d .git ]; then
    git add -A
    git commit -q -m "Evolution checkpoint $(date '+%Y-%m-%d %H:%M:%S')" || true
  fi

  generation=$((generation + 1))
  sleep "$PAUSE_SECONDS"
done
