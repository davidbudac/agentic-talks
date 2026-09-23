#!/usr/bin/env bash
# Talk 05: the same task with a bloated and a lean CLAUDE.md.
#
# For each variant (claude-md/bloated.md, claude-md/lean.md) in a fresh copy of
# invoice-app: first `/context` headless (reads the fixed overhead and the
# CLAUDE.md tokens from context_usage, no model turn), then the task: backlog
# 004 (filter the report by customer), RUNS times, each in a fresh copy.
# Hidden tests decide the outcome.
#
# Fills slide 25 (turns, total tokens, CLAUDE.md tokens per turn, outcome),
# gives slide 24's live numbers a rehearsal baseline, slide 17's overhead from
# /context, and slide 6's per-session bill from the first lean transcript.
#
# Usage: run/talk05.sh [--dry-run] [--yes]
# Environment: MODEL (default claude-sonnet-5), RUNS (default 1 per variant),
#   MAX_TURNS (default 25), MAX_BUDGET_USD, CLAUDE_BIN, RESULTS_ROOT, ISOLATE
set -euo pipefail
MAX_TURNS="${MAX_TURNS:-25}"
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'; }
parse_common_args "$@"

RUNS="${RUNS:-1}"
TASK=report-customer-filter
PROMPT="Implement backlog/004-report-customer-filter.md. Run python3 -m unittest before you finish."
CHECKER="$SERIES_DIR/eval/checkers/hidden-tests"

require_claude
results_dir talk05
read -r lo hi cap <<< "$(estimate_line "$MODEL" $((RUNS * 2)))"
confirm_plan \
  "Talk 05 · bloated vs lean CLAUDE.md (model $MODEL)" \
  "Per variant: /context once (no model turn, ~free), then backlog 004 x $RUNS in a fresh copy" \
  "Sessions that call the model: $((RUNS * 2)), est. \$$lo-\$$hi (cap \$$cap)" \
  "Estimated time: $((RUNS * 2))-$((RUNS * 6)) minutes"

for variant in bloated lean; do
  say "── /context with the $variant CLAUDE.md"
  setup_repo "talk05-context-$variant" "$variant"
  build_claude_cmd "/context" "$MODEL"
  run_session "$REPO" "$RESULTS_DIR/context-$variant"
done

for i in $(seq 1 "$RUNS"); do
  for variant in bloated lean; do
    out="$RESULTS_DIR/task-$variant-$i"
    say "── task run $i/$RUNS with the $variant CLAUDE.md"
    setup_repo "talk05-$variant-$i" "$variant"
    build_claude_cmd "$PROMPT" "$MODEL"
    run_session "$REPO" "$out"
    if [[ $DRY_RUN -eq 0 ]]; then
      save_repo_state "$REPO" "$out"
      "$CHECKER" --repo "$REPO" --task "$TASK" > "$out/check.json" || true
      python3 -c "import json,sys; r=json.load(open(sys.argv[1])); print('   ' + r['notes'])" "$out/check.json"
    else
      say "+ $(printf '%q' "$CHECKER") --repo $(printf '%q' "$REPO") --task $TASK > $(printf '%q' "$out/check.json")"
    fi
  done
done

summarise_talk talk05
