#!/usr/bin/env bash
# Lab 2 · variance (30 min): one task, 3 runs per variant; pass@k and pass^k.
#
#   ./lab2.sh [--dry-run] [--yes]
#   ./lab2.sh --sample          no model calls: the same summary over the synthetic sample set
#
# 1 task x 2 variants x 3 runs = 6 sessions (LITE=1: 2 runs, 4 sessions).
# ROLE=a runs lean only, ROLE=b bloated only (split across two laptops).
# Rounds interleave the variants, so an interrupted lab still has balanced data.
# Every pair's runs go to the board (./export-results.sh --lab lab2 --latest),
# which pools them: that is where the sample gets big enough to mean something.
#
# Environment: TASK (default report-sort-accents), RUNS, MODEL, LITE, ROLE, PAIR,
#   MAX_TURNS, MAX_BUDGET_USD, ENGINE, CLAUDE_BIN, RESULTS_ROOT, ISOLATE
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'; }
parse_common_args "$@"

if [[ $USE_SAMPLE -eq 1 ]]; then
  exec python3 "$LABKIT" sample-summary lab2
fi
TASK="${TASK:-report-sort-accents}"
if [[ "$LITE" == 1 ]]; then RUNS="${RUNS:-2}"; else RUNS="${RUNS:-3}"; fi
[[ -f "$EVAL_DIR/tasks/$TASK.yaml" ]] || die "no such task: $TASK"
case "$ROLE" in a) variants=(lean) ;; b) variants=(bloated) ;; *) variants=(lean bloated) ;; esac
n=$(( RUNS * ${#variants[@]} ))

require_claude
pick_engine
results_dir lab2
confirm_plan \
  "Lab 2 · variance: k = $RUNS runs per variant on one task ($(model_alias "$MODEL"): $MODEL)" \
  "Task: $TASK   Variants: ${variants[*]}" \
  "$(plan_line "Expected ($(model_alias "$MODEL"))" "$(model_alias "$MODEL")" "$n")"

for round in $(seq 1 "$RUNS"); do
  for variant in "${variants[@]}"; do
    say "── round $round/$RUNS: $variant"
    run_cells lab2 "$variant" "$MODEL" "$variant" "$round" "$TASK"
  done
done
finish_lab lab2
