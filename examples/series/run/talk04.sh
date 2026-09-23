#!/usr/bin/env bash
# Talk 04: what subagents do to the lead's context, and what caching does to the bill.
#
# (b) cache: the same short prompt twice, back to back, in the same repo copy
#     (same cwd, so the same system prompt). Reads cache_creation vs cache_read
#     from the first API call and the session totals (slides 29, 31, 32).
#     CACHE_WAIT_S=N adds a third run after N seconds (e.g. 360 to pass the
#     5-minute TTL; Claude Code on a subscription uses a 1-hour TTL for the main
#     conversation, so expect that one to still hit unless N > 3600).
# (a) survey: one lead agent surveys invoice-app twice in fresh copies: reading
#     every file itself (Agent tool denied), then fanning out Explore subagents
#     over four areas. Captures the lead's context at the end, tool output that
#     entered the lead, total tokens across agents, wall-clock, cost, and each
#     subagent's "Done (N tool uses · Xk tokens · Ys)" line (slides 8, 11, 12, 14,
#     17, 34). Runs (b) first so (a) cannot warm its cache.
#
# Usage: run/talk04.sh [--dry-run] [--yes] [--only survey|cache]
# Environment: MODEL (default claude-sonnet-5), CACHE_WAIT_S (default 0),
#   MAX_TURNS (default 30), MAX_BUDGET_USD, CLAUDE_BIN, RESULTS_ROOT, ISOLATE
set -euo pipefail
MAX_TURNS="${MAX_TURNS:-30}"
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'; }
parse_common_args "$@"

ONLY=""
set -- "${REST_ARGS[@]+"${REST_ARGS[@]}"}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --only) ONLY="${2:?--only needs survey or cache}"; shift 2 ;;
    *) die "unknown argument: $1" ;;
  esac
done
CACHE_WAIT_S="${CACHE_WAIT_S:-0}"
do_cache=1; do_survey=1
[[ "$ONLY" == survey ]] && do_cache=0
[[ "$ONLY" == cache ]] && do_survey=0

SURVEY_TASK="Survey this repository for a new maintainer. For each module in invoicing/ and tools/, report its purpose in one line, its public functions, which other modules of the package it imports, and one risk or likely bug you notice. Finish with a single table of at most 15 rows. Do not edit any files."
INLINE_PROMPT="$SURVEY_TASK Read the files yourself; do not delegate to subagents."
FANOUT_PROMPT="$SURVEY_TASK Delegate the reading: in a single message, use the Agent tool to start four Explore subagents in parallel, one per area: (1) invoicing/money.py and invoicing/invoice.py, (2) invoicing/customers.py and invoicing/report.py, (3) invoicing/dates.py, invoicing/fixtures.py and invoicing/export.py, (4) invoicing/cli.py and tools/invoice_mcp.py. Give each a self-contained task and ask for at most 10 lines back. Do not read the source files yourself; build the table from their reports."
CACHE_PROMPT="Read invoicing/money.py and answer in one sentence: which rounding mode does round_money use? Do not read any other file."

require_claude
results_dir talk04
sessions=0
[[ $do_cache -eq 1 ]] && sessions=$((sessions + 2 + (CACHE_WAIT_S > 0 ? 1 : 0)))
read -r c_lo c_hi c_cap <<< "$(estimate_line "$MODEL" "$sessions")"
survey_lines=()
if [[ $do_survey -eq 1 ]]; then
  # A survey reads ~15 files; the fan-out adds four subagents. Budget ~3-6 sessions' worth.
  read -r s_lo s_hi s_cap <<< "$(estimate_line "$MODEL" 5)"
  survey_lines=("Survey: inline vs 4 Explore subagents, 2 sessions, est. \$$s_lo-\$$s_hi, ~3-8 minutes")
fi
confirm_plan \
  "Talk 04 · subagents and caching (model $MODEL)" \
  "$( [[ $do_cache -eq 1 ]] && echo "Cache: same prompt x2 back to back$( [[ $CACHE_WAIT_S -gt 0 ]] && echo ", then once more after ${CACHE_WAIT_S}s" ), est. \$$c_lo-\$$c_hi, ~1-2 minutes + wait" || echo "Cache: skipped")" \
  "${survey_lines[@]+"${survey_lines[@]}"}"

if [[ $do_cache -eq 1 ]]; then
  say "── cache: same prompt, same directory"
  setup_repo talk04-cache lean
  build_claude_cmd "$CACHE_PROMPT" "$MODEL"
  run_session "$REPO" "$RESULTS_DIR/cache-1"
  run_session "$REPO" "$RESULTS_DIR/cache-2"
  if [[ $CACHE_WAIT_S -gt 0 ]]; then
    say "   waiting ${CACHE_WAIT_S}s before the third run"
    [[ $DRY_RUN -eq 0 ]] && sleep "$CACHE_WAIT_S"
    run_session "$REPO" "$RESULTS_DIR/cache-3-after-${CACHE_WAIT_S}s"
  fi
fi

if [[ $do_survey -eq 1 ]]; then
  say "── survey: inline (Agent tool denied)"
  setup_repo talk04-inline lean
  build_claude_cmd "$INLINE_PROMPT" "$MODEL"
  run_session "$REPO" "$RESULTS_DIR/survey-inline"

  say "── survey: fan out to subagents"
  setup_repo talk04-fanout lean
  DISALLOWED_TOOLS="WebFetch,WebSearch"
  ALLOWED_TOOLS="$ALLOWED_TOOLS,Agent"
  build_claude_cmd "$FANOUT_PROMPT" "$MODEL" --forward-subagent-text
  run_session "$REPO" "$RESULTS_DIR/survey-subagents"
fi

summarise_talk talk04
