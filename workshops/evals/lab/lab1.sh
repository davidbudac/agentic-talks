#!/usr/bin/env bash
# Lab 1 · guess, then measure (35 min): lean vs bloated CLAUDE.md on the Java repo.
#
#   ./predict.sh lean|bloated      first: which CLAUDE.md will be cheaper per passing run?
#   ./lab1.sh [--dry-run] [--yes]
#
# 2 tasks x 2 variants x 1 run = 4 sessions (LITE=1: 1 task, 2 sessions).
# ROLE=a runs only the lean half, ROLE=b only the bloated half, so a pair can
# split the sessions across both partners' laptops and subscriptions (set the
# same PAIR on both). Results: results/lab1/<ts>/ with export.json for the board.
#
# Environment: TASKS (default "fix-date-parser jpy-rounding"), MODEL, LITE, ROLE,
#   PAIR, MAX_TURNS, MAX_BUDGET_USD, ENGINE, CLAUDE_BIN, RESULTS_ROOT, ISOLATE
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; }
parse_common_args "$@"

if [[ "$LITE" == 1 ]]; then TASKS="${TASKS:-fix-date-parser}"; else TASKS="${TASKS:-fix-date-parser jpy-rounding}"; fi
read -r -a task_list <<< "$TASKS"
for t in "${task_list[@]}"; do [[ -f "$EVAL_DIR/tasks/$t.yaml" ]] || die "no such task: $t"; done
case "$ROLE" in a) variants=(lean) ;; b) variants=(bloated) ;; *) variants=(lean bloated) ;; esac
n=$(( ${#task_list[@]} * ${#variants[@]} ))

require_claude
pick_engine
results_dir lab1
prediction="$(python3 -c 'import sys; sys.path.insert(0, sys.argv[1]); import labkit; print(labkit.latest_prediction() or "")' "$LIB_DIR")"
confirm_plan \
  "Lab 1 · guess, then measure: lean vs bloated CLAUDE.md ($(model_alias "$MODEL"): $MODEL)" \
  "Tasks: $TASKS   Variants: ${variants[*]}   Runs per cell: 1" \
  "$(plan_line "Expected ($(model_alias "$MODEL"))" "$(model_alias "$MODEL")" "$n")" \
  "Your prediction: ${prediction:-none yet -- run ./predict.sh lean|bloated first}"

if [[ -z "$prediction" && $DRY_RUN -eq 0 ]]; then
  warn "no prediction recorded. The point of lab 1 is to guess first: ./predict.sh lean|bloated"
fi

for variant in "${variants[@]}"; do
  run_cells lab1 "$variant" "$MODEL" "$variant" 1 "${task_list[@]}"
done
finish_lab lab1
