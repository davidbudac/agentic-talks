#!/usr/bin/env bash
# Talk 07: a minimal eval with smevals. Six tasks from invoice-app, two
# variants, several runs each, scored by hidden tests; reports pass@k and pass^k.
#
# The eval lives in examples/series/eval/ in smevals' layout: tasks/*.yaml,
# configs/{lean,bloated,default}.yaml, graders/default.yaml, checkers/hidden-tests
# and the Runner run-claude (one headless Claude Code session per run on a fresh
# repo copy). smevals is run with `uvx --from smevals==0.2.0 smevals` (nothing
# is installed into the project; uv caches the package), or a `smevals` on PATH.
#
# VARIANT=claude-md (default): configs lean vs bloated, one MODEL.
# VARIANT=models: config default (lean CLAUDE.md), MODEL_A vs MODEL_B.
# Each `smevals run` call without -n executes exactly one run per task and
# model, so the script calls it once per round and variant: variants
# interleave and an interrupted session leaves balanced samples. (The -n
# top-up flag shown on talk 07 slide 9 is on smevals' main branch but not in
# the 0.2.0 release on PyPI, so the kit does not rely on it.) RESUME=<results
# dir> adds rounds to an earlier run's folder.
#
# Fills slide 4 (the task suite with pass/fail), 16 (waste read from real
# traces), 12/13 (the scored sheet), and gives slide 14 real cost per accepted
# task when VARIANT=models.
#
# Usage: run/talk07.sh [--dry-run] [--yes]
# Environment: RUNS (default 3 = k), TASKS (default: all six, space-separated),
#   VARIANT, MODEL (claude-sonnet-5), MODEL_A (claude-haiku-4-5), MODEL_B
#   (claude-sonnet-5), SMEVALS (command), RESUME, MAX_TURNS (default 20),
#   MAX_BUDGET_USD, CLAUDE_BIN, RESULTS_ROOT, ISOLATE
set -euo pipefail
MAX_BUDGET_USD="${MAX_BUDGET_USD:-0.60}"
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,29p' "$0" | sed 's/^# \{0,1\}//'; }
parse_common_args "$@"

EVAL_DIR="$SERIES_DIR/eval"
RUNS="${RUNS:-3}"
VARIANT="${VARIANT:-claude-md}"
ALL_TASKS="$(cd "$EVAL_DIR/tasks" && ls *.yaml | sed 's/\.yaml$//' | tr '\n' ' ')"
TASKS="${TASKS:-$ALL_TASKS}"
if [[ -z "${SMEVALS:-}" ]]; then
  if command -v smevals >/dev/null 2>&1; then SMEVALS="smevals"; else SMEVALS="uvx --from smevals==0.2.0 smevals"; fi
fi
read -r -a SMEVALS_CMD <<< "$SMEVALS"

task_args=()
n_tasks=0
for task in $TASKS; do
  [[ -f "$EVAL_DIR/tasks/$task.yaml" ]] || die "no such task: $task (have: $ALL_TASKS)"
  task_args+=(-t "$task")
  n_tasks=$((n_tasks + 1))
done

case "$VARIANT" in
  claude-md) combos=("-c lean -m $MODEL" "-c bloated -m $MODEL"); VARIANT_DESC="lean vs bloated CLAUDE.md on $MODEL"; est_model="$MODEL" ;;
  models) MODEL_A="${MODEL_A:-claude-haiku-4-5}"; MODEL_B="${MODEL_B:-claude-sonnet-5}"
          combos=("-c default -m $MODEL_A -m $MODEL_B"); VARIANT_DESC="$MODEL_A vs $MODEL_B, lean CLAUDE.md"; est_model="$MODEL_B" ;;
  *) die "VARIANT must be claude-md or models" ;;
esac

require_claude
if [[ -n "${RESUME:-}" ]]; then
  RESULTS_DIR="$RESUME"
else
  results_dir talk07
fi
RUNS_DIR="$RESULTS_DIR/runs"
sessions=$((n_tasks * 2 * RUNS))
read -r lo hi cap <<< "$(estimate_line "$est_model" "$sessions")"
confirm_plan \
  "Talk 07 · minimal eval with smevals ($VARIANT_DESC)" \
  "Tasks ($n_tasks): $TASKS" \
  "k = $RUNS runs per task and variant → $sessions sessions, est. \$$lo-\$$hi (cap \$$cap)" \
  "Estimated time: $sessions-$((sessions * 3)) minutes, sequential (smaller: TASKS=\"fix-date-parser fixtures-bom jpy-rounding\" RUNS=2)" \
  "smevals: ${SMEVALS_CMD[*]}"

if [[ $DRY_RUN -eq 0 ]]; then
  "${SMEVALS_CMD[@]}" --version >/dev/null || die "smevals is not runnable: ${SMEVALS_CMD[*]}"
  python3 - "$RESULTS_DIR/plan.json" "$VARIANT" "$RUNS" "$TASKS" "${SMEVALS_CMD[*]}" <<'PY'
import json, sys
path, variant, runs, tasks, engine = sys.argv[1:]
json.dump({"variant": variant, "k": int(runs), "tasks": tasks.split(), "engine": engine}, open(path, "w"), indent=2)
PY
fi

for round in $(seq 1 "$RUNS"); do
  for combo in "${combos[@]}"; do
    read -r -a combo_args <<< "$combo"
    say "── round $round/$RUNS: $combo"
    cmd=("${SMEVALS_CMD[@]}" run "$EVAL_DIR" "${combo_args[@]}" "${task_args[@]}" -g --runs-dir "$RUNS_DIR")
    say "+ $(printf '%q ' "${cmd[@]}")"
    if [[ $DRY_RUN -eq 0 ]]; then
      "${cmd[@]}" || true   # smevals exits non-zero when any run grades as fail; that is data
    fi
  done
done

if [[ $DRY_RUN -eq 1 ]]; then
  first_task="$(echo "$TASKS" | awk '{print $1}')"
  prompt="$(python3 -c "import re,sys; t=open(sys.argv[1]).read(); m=re.search(r'^prompt: \|\n((?:  .*\n?)+)', t, re.M); print('\n'.join(l[2:] for l in m.group(1).splitlines()))" "$EVAL_DIR/tasks/$first_task.yaml")"
  build_claude_cmd "$prompt" "$MODEL"
  say "Each run executes eval/run-claude, which calls (task $first_task):"
  print_cmd "<run dir>/repo" "<run dir>/transcript.jsonl" "${CMD[@]}"
  say "+ $(printf '%q ' "${SMEVALS_CMD[@]}" report "$EVAL_DIR" --runs-dir "$RUNS_DIR" --json) > $(printf '%q' "$RESULTS_DIR/grades.json")"
  exit 0
fi

"${SMEVALS_CMD[@]}" report "$EVAL_DIR" --runs-dir "$RUNS_DIR" --json > "$RESULTS_DIR/grades.json" || die "no grades found"
"${SMEVALS_CMD[@]}" report "$EVAL_DIR" --runs-dir "$RUNS_DIR" --by-task > "$RESULTS_DIR/smevals-report.md" || true
summarise_talk talk07
say "smevals report: $RESULTS_DIR/smevals-report.md"
