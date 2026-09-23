#!/usr/bin/env bash
# Talk 06: parallel agents in worktrees, the merge-conflict failure mode, and
# one capability measured as an MCP server and as a CLI.
#
# merge (slide 13): two headless agents work at the same time on two backlog
#   issues, each in its own git worktree and branch of one fresh repo copy. The
#   runner commits each branch, merges both into main and records whether the
#   second merge conflicts. PAIR=overlap (default) runs 001 + 002, which both add
#   a sixth column to export.py; PAIR=clean runs 003 + 005, which touch
#   different files (the control).
# mcp (slide 30): the same question answered through tools/invoice_mcp.py (a
#   stdlib MCP server loaded with --mcp-config) and through `python3 -m
#   invoicing` (Bash only). Records /context tokens before the first call,
#   tokens and cost for the task, wall-clock and whether the answer is right.
#   Nothing is installed: the server is a Python file in the repo.
#
# Usage: run/talk06.sh [--dry-run] [--yes] [--only merge|mcp]
# Environment: PAIR=overlap|clean, MODEL (default claude-sonnet-5), MAX_TURNS
#   (default 25), MAX_BUDGET_USD, CLAUDE_BIN, RESULTS_ROOT, ISOLATE
set -euo pipefail
MAX_TURNS="${MAX_TURNS:-25}"
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; }
parse_common_args "$@"

ONLY=""
set -- "${REST_ARGS[@]+"${REST_ARGS[@]}"}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --only) ONLY="${2:?--only needs merge or mcp}"; shift 2 ;;
    *) die "unknown argument: $1" ;;
  esac
done
do_merge=1; do_mcp=1
[[ "$ONLY" == merge ]] && do_mcp=0
[[ "$ONLY" == mcp ]] && do_merge=0

PAIR="${PAIR:-overlap}"
case "$PAIR" in
  overlap) ISSUES=(001-export-currency-column 002-export-due-date-column); CHECKS=(export-currency-column export-due-date-column) ;;
  clean) ISSUES=(003-jpy-zero-decimals 005-legacy-export-bom); CHECKS=(jpy-rounding fixtures-bom) ;;
  *) die "PAIR must be overlap or clean" ;;
esac
CHECKER="$SERIES_DIR/eval/checkers/hidden-tests"
QUESTION="What is the total gross amount in EUR across all invoices in data/invoices.csv, and which customer has the largest EUR gross total? Reply with the total and the customer name only."

require_claude
results_dir talk06
n_sessions=$(( (do_merge ? 2 : 0) + (do_mcp ? 2 : 0) ))
read -r lo hi cap <<< "$(estimate_line "$MODEL" "$n_sessions")"
confirm_plan \
  "Talk 06 · parallel agents + MCP vs CLI (model $MODEL)" \
  "$( [[ $do_merge -eq 1 ]] && echo "Merge: 2 agents in parallel worktrees on ${ISSUES[0]} + ${ISSUES[1]} (PAIR=$PAIR), then git merge both" || echo "Merge: skipped")" \
  "$( [[ $do_mcp -eq 1 ]] && echo "MCP vs CLI: /context x2 (no model turn) + the same question x2" || echo "MCP vs CLI: skipped")" \
  "Model sessions: $n_sessions, est. \$$lo-\$$hi (cap \$$cap); time ~3-8 minutes"

git_quiet() { git -C "$@" >/dev/null 2>&1; }

if [[ $do_merge -eq 1 ]]; then
  setup_repo talk06-merge lean
  MAIN="$REPO"
  pids=()
  start_ms="$(now_ms)"
  for index in 0 1; do
    issue="${ISSUES[$index]}"
    wt="$WORKDIR/wt-${issue%%-*}"
    say "── worktree for $issue"
    say "+ git -C $(printf '%q' "$MAIN") worktree add -q -b task-${issue%%-*} $(printf '%q' "$wt")"
    git -C "$MAIN" worktree add -q -b "task-${issue%%-*}" "$wt"
    build_claude_cmd "Implement backlog/$issue.md. Work only in this directory and do not commit. Run python3 -m unittest before you finish." "$MODEL"
    if [[ $DRY_RUN -eq 1 ]]; then
      run_session "$wt" "$RESULTS_DIR/agent-$issue"
    else
      run_session "$wt" "$RESULTS_DIR/agent-$issue" &
      pids+=($!)
    fi
  done
  if [[ ${#pids[@]} -gt 0 ]]; then
    say "   two agents running in parallel…"
    for pid in "${pids[@]}"; do wait "$pid" || true; done
  fi
  end_ms="$(now_ms)"

  if [[ $DRY_RUN -eq 0 ]]; then
    for index in 0 1; do
      issue="${ISSUES[$index]}"; wt="$WORKDIR/wt-${issue%%-*}"; out="$RESULTS_DIR/agent-$issue"
      save_repo_state "$wt" "$out"
      "$CHECKER" --repo "$wt" --task "${CHECKS[$index]}" > "$out/check.json" || true
      git_quiet "$wt" add -A
      git_quiet "$wt" commit -m "Backlog $issue (agent)" || true
    done
    first="task-${ISSUES[0]%%-*}"; second="task-${ISSUES[1]%%-*}"
    first_merge=clean; second_merge=clean; conflicted=""
    git_quiet "$MAIN" merge --no-ff --no-edit "$first" || first_merge=conflict
    if ! git_quiet "$MAIN" merge --no-ff --no-edit "$second"; then
      second_merge=conflict
      conflicted="$(git -C "$MAIN" diff --name-only --diff-filter=U | tr '\n' ' ')"
      git -C "$MAIN" diff > "$RESULTS_DIR/merge-conflict.diff" || true
      git_quiet "$MAIN" merge --abort || true
    fi
    python3 - "$RESULTS_DIR/merge.json" "$PAIR" "$first" "$second" "$first_merge" "$second_merge" \
      "$conflicted" "$start_ms" "$end_ms" <<'PY'
import json, sys
path, pair, first, second, m1, m2, conflicted, start, end = sys.argv[1:]
json.dump({"pair": pair, "first": first, "second": second, "first_merge": m1, "second_merge": m2,
           "conflicted_files": conflicted.split(), "parallel_wall_s": round((int(end) - int(start)) / 1000, 1)},
          open(path, "w"), indent=2)
PY
    say "   merge $first: $first_merge · merge $second: $second_merge ${conflicted:+(conflicts: $conflicted)}"
  else
    say "+ git -C $(printf '%q' "$MAIN") merge --no-ff --no-edit task-${ISSUES[0]%%-*}"
    say "+ git -C $(printf '%q' "$MAIN") merge --no-ff --no-edit task-${ISSUES[1]%%-*}   # conflict expected for PAIR=overlap"
  fi
fi

if [[ $do_mcp -eq 1 ]]; then
  setup_repo talk06-mcp lean
  MCP_JSON="$WORKDIR/mcp.json"
  python3 - "$MCP_JSON" "$REPO/tools/invoice_mcp.py" <<'PY'
import json, sys
json.dump({"mcpServers": {"invoicing": {"type": "stdio", "command": "python3", "args": [sys.argv[2]]}}},
          open(sys.argv[1], "w"), indent=2)
PY
  NO_FILES="Read,Glob,Grep,Edit,Write,Agent,WebFetch,WebSearch"

  say "── MCP path"
  # Same tool list on both paths (only the MCP server differs), so /context compares like with like.
  # Bash stays in the tool list but is not allowed here, so dontAsk denies it.
  ALLOWED_TOOLS="mcp__invoicing"; DISALLOWED_TOOLS="$NO_FILES"
  build_claude_cmd "/context" "$MODEL" --mcp-config "$MCP_JSON"
  run_session "$REPO" "$RESULTS_DIR/mcp-context"
  build_claude_cmd "Use the invoicing MCP tools to answer. $QUESTION" "$MODEL" --mcp-config "$MCP_JSON"
  run_session "$REPO" "$RESULTS_DIR/mcp-task"

  say "── CLI path"
  ALLOWED_TOOLS="Bash(python3 -m invoicing),Bash(python3 -m invoicing *)"; DISALLOWED_TOOLS="$NO_FILES"
  build_claude_cmd "/context" "$MODEL"
  run_session "$REPO" "$RESULTS_DIR/cli-context"
  build_claude_cmd "Use the command-line tool python3 -m invoicing (see --help) to answer. $QUESTION" "$MODEL"
  run_session "$REPO" "$RESULTS_DIR/cli-task"

  if [[ $DRY_RUN -eq 0 ]]; then
    for kind in mcp cli; do
      python3 - "$REPO" "$RESULTS_DIR/$kind-task" <<'PY'
import json, sys, unicodedata
from decimal import Decimal
from pathlib import Path
repo, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo))
from invoicing.fixtures import load_invoices
from invoicing.report import grand_totals, summarise
entries = summarise(load_invoices(repo / "data" / "invoices.csv"), currency="EUR")
total = grand_totals(entries)["EUR"]
top = max(entries, key=lambda e: e["gross"])["customer"]
answer = ""
for line in (out / "transcript.jsonl").read_text(encoding="utf-8").splitlines():
    try:
        event = json.loads(line)
    except ValueError:
        continue
    if event.get("type") == "result":
        answer = event.get("result") or ""
norm = lambda s: unicodedata.normalize("NFC", s).replace(",", "").casefold()
correct = norm(f"{total:.2f}") in norm(answer) and norm(top) in norm(answer)
json.dump({"correct": correct, "expected_total_eur": f"{total:.2f}", "expected_customer": top,
           "answer": answer[:500]}, open(out / "check.json", "w"), indent=2, ensure_ascii=False)
print(f"   {out.name}: {'right' if correct else 'wrong'} answer")
PY
    done
  fi
fi

summarise_talk talk06
