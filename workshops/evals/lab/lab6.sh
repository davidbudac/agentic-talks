#!/usr/bin/env bash
# Lab 6 · route by the numbers (35 min): cost per ACCEPTED task, Haiku vs Sonnet.
#
#   ./lab6.sh [--dry-run] [--yes]
#   OPUS=1 ./lab6.sh             also Opus (check your plan includes it)
#   LOCAL_MODEL=qwen3-coder ./lab6.sh --local
#                                also a local model through Ollama (optional, unsupported
#                                by Anthropic; see lab6-routing-notes.md)
#   ./lab6.sh --sample           no model calls: the summary over the synthetic sample set
#
# The same 3 tasks, 2 runs each, per model (LITE=1: 2 tasks, 1 run). Reports
# pass rate, cost per run and cost per accepted task. To stay inside a Pro
# window, Sonnet runs you already have from labs 1-2 (same task, lean CLAUDE.md,
# same MODEL) are reused, so by default this lab costs 6 Haiku sessions plus
# ~2 Sonnet top-ups. REUSE=0 runs everything fresh (12 sessions).
# ROLE=a runs Sonnet (and Opus), ROLE=b runs Haiku (and local).
#
# Environment: TASKS (default "fix-date-parser jpy-rounding report-sort-accents"),
#   RUNS (2), MODEL, HAIKU_MODEL, OPUS_MODEL, OPUS, REUSE (1), LOCAL_MODEL,
#   LOCAL_BASE_URL (http://localhost:11434), LITE, ROLE, PAIR, MAX_TURNS,
#   MAX_BUDGET_USD, ENGINE, CLAUDE_BIN, RESULTS_ROOT, ISOLATE
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'; }
LOCAL=0
args=()
for a in "$@"; do if [[ "$a" == --local ]]; then LOCAL=1; else args+=("$a"); fi; done
parse_common_args "${args[@]+"${args[@]}"}"

if [[ $USE_SAMPLE -eq 1 ]]; then
  exec python3 "$LABKIT" sample-summary lab6
fi
if [[ "$LITE" == 1 ]]; then
  TASKS="${TASKS:-fix-date-parser report-sort-accents}"; RUNS="${RUNS:-1}"
else
  TASKS="${TASKS:-fix-date-parser jpy-rounding report-sort-accents}"; RUNS="${RUNS:-2}"
fi
REUSE="${REUSE:-1}"
read -r -a task_list <<< "$TASKS"
for t in "${task_list[@]}"; do [[ -f "$EVAL_DIR/tasks/$t.yaml" ]] || die "no such task: $t"; done

models=()   # "alias model"
case "$ROLE" in
  a) models=("sonnet $MODEL"); [[ "${OPUS:-0}" == 1 ]] && models+=("opus $OPUS_MODEL") ;;
  b) models=("haiku $HAIKU_MODEL") ;;
  *) models=("haiku $HAIKU_MODEL" "sonnet $MODEL"); [[ "${OPUS:-0}" == 1 ]] && models+=("opus $OPUS_MODEL") ;;
esac
if [[ $LOCAL -eq 1 ]]; then
  [[ -n "${LOCAL_MODEL:-}" ]] || die "--local needs LOCAL_MODEL (for example LOCAL_MODEL=qwen3-coder)"
  [[ "$ROLE" == a ]] || models+=("local $LOCAL_MODEL")
fi

# Sonnet runs to reuse from labs 1-2, per task.
reused_json="{}"
if [[ "$REUSE" == 1 ]] && printf '%s\n' "${models[@]}" | grep -q '^sonnet '; then
  reused_json="$(python3 "$LABKIT" reuse --tasks "${task_list[@]}" --model "$(model_alias "$MODEL")" --want "$RUNS")"
fi
reused_count() { python3 -c 'import json,sys; print(len(json.loads(sys.argv[1]).get(sys.argv[2], [])))' "$reused_json" "$1"; }

require_claude
pick_engine
results_dir lab6
plan=("Lab 6 · route by the numbers: ${#task_list[@]} tasks x $RUNS runs per model" "Tasks: $TASKS")
total=0
for entry in "${models[@]}"; do
  read -r alias model <<< "$entry"
  fresh=0
  for t in "${task_list[@]}"; do
    have=0
    [[ "$alias" == sonnet ]] && have="$(reused_count "$t")"
    (( have > RUNS )) && have=$RUNS
    fresh=$(( fresh + RUNS - have ))
  done
  total=$(( total + fresh ))
  note=""
  [[ "$alias" == sonnet && "$REUSE" == 1 ]] && note=" (reusing $(( ${#task_list[@]} * RUNS - fresh )) from labs 1-2)"
  plan+=("$(plan_line "$alias ($model)$note" "$alias" "$fresh")")
done
plan+=("Total fresh sessions: $total")
[[ $LOCAL -eq 1 ]] && plan+=("Local runs go to ${LOCAL_BASE_URL:-http://localhost:11434} (Ollama); no plan usage, cost exported as 0.0.")
confirm_plan "${plan[@]}"

if [[ $LOCAL -eq 1 && $DRY_RUN -eq 0 ]]; then
  curl -fsS -m 5 "${LOCAL_BASE_URL:-http://localhost:11434}/api/version" >/dev/null 2>&1 \
    || die "no Ollama at ${LOCAL_BASE_URL:-http://localhost:11434} (ollama serve; ollama pull $LOCAL_MODEL)"
fi
if [[ $DRY_RUN -eq 0 ]]; then
  python3 - "$RESULTS_DIR/reused.json" "$reused_json" "$(pair_id)" <<'PY'
import json, sys
path, data, pair = sys.argv[1], json.loads(sys.argv[2]), sys.argv[3]
records = [dict(r, pair=pair) for runs in data.values() for r in runs]
json.dump(records, open(path, "w"))
PY
fi

for round in $(seq 1 "$RUNS"); do
  for entry in "${models[@]}"; do
    read -r alias model <<< "$entry"
    todo=()
    for t in "${task_list[@]}"; do
      have=0
      [[ "$alias" == sonnet ]] && have="$(reused_count "$t")"
      (( round > have )) && todo+=("$t")
    done
    [[ ${#todo[@]} -gt 0 ]] || continue
    say "── round $round/$RUNS: $alias"
    if [[ "$alias" == local ]]; then
      # Claude Code prices local tokens at Anthropic rates, so lift the dollar cap
      # (the turn cap still applies); the export records cost 0.0 for local runs.
      ( export ANTHROPIC_BASE_URL="${LOCAL_BASE_URL:-http://localhost:11434}" ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY=""
        export MAX_BUDGET_USD="${LOCAL_MAX_BUDGET_USD:-50}"
        run_cells lab6 lean "$model" local "$round" "${todo[@]}" )
    else
      run_cells lab6 lean "$model" "$alias" "$round" "${todo[@]}"
    fi
  done
done
finish_lab lab6
