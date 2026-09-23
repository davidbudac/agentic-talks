# Shared helpers for the talk runners. Source it; do not execute it.
# shellcheck shell=bash
#
# Environment knobs (all optional):
#   MODEL            model for single-model runs      (default claude-sonnet-5, the model the decks price)
#   MAX_TURNS        --max-turns per headless session (default 20)
#   MAX_BUDGET_USD   --max-budget-usd per session     (default 1.00, a hard stop per run)
#   CLAUDE_BIN       the Claude Code binary           (default: claude on PATH)
#   RESULTS_ROOT     where results go                 (default examples/series/results)
#   ISOLATE=0        also load your user settings, user CLAUDE.md, plugins and MCP servers
#   KEEP_WORKDIRS=1  keep the temporary repo copies for inspection

SERIES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RUN_DIR="$SERIES_DIR/run"
APP_DIR="$SERIES_DIR/invoice-app"
ANALYZE="$RUN_DIR/lib/analyze.py"
RESULTS_ROOT="${RESULTS_ROOT:-$SERIES_DIR/results}"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
MODEL="${MODEL:-claude-sonnet-5}"
MAX_TURNS="${MAX_TURNS:-20}"
MAX_BUDGET_USD="${MAX_BUDGET_USD:-1.00}"
ISOLATE="${ISOLATE:-1}"
KEEP_WORKDIRS="${KEEP_WORKDIRS:-0}"
export PYTHONDONTWRITEBYTECODE=1

# Tools the agent may use without asking. Everything else is denied (dontAsk).
# python3 is allowed because the agent must run the tests it writes; the repo
# copy lives in a temp dir. No pip, no curl, no git push.
ALLOWED_TOOLS="${ALLOWED_TOOLS:-Read,Edit,Write,Glob,Grep,Bash(python3 -m unittest),Bash(python3 -m unittest *),Bash(python3 *),Bash(cd *),Bash(pwd),Bash(ls),Bash(ls *),Bash(cat *),Bash(head *),Bash(wc *),Bash(grep *),Bash(find *),Bash(git status*),Bash(git diff*),Bash(git log*),Bash(git show*)}"
# Denied in every run unless a runner says otherwise (talk 04 re-enables Agent).
DISALLOWED_TOOLS="${DISALLOWED_TOOLS:-Agent,WebFetch,WebSearch}"

DRY_RUN=0
ASSUME_YES=0
WORKDIRS=()

say() { printf '%s\n' "$*"; }
warn() { printf 'warning: %s\n' "$*" >&2; }
die() { printf 'error: %s\n' "$*" >&2; exit 1; }

# Parse --dry-run / --yes / --help; leaves other args in REST_ARGS.
parse_common_args() {
  REST_ARGS=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dry-run|-n) DRY_RUN=1 ;;
      --yes|-y) ASSUME_YES=1 ;;
      -h|--help) usage; exit 0 ;;
      *) REST_ARGS+=("$1") ;;
    esac
    shift
  done
}

timestamp() { date -u +%Y%m%dT%H%M%SZ; }
now_ms() { python3 -c 'import time; print(int(time.time() * 1000))'; }

# results_dir TALK -> sets RESULTS_DIR (created unless dry run)
results_dir() {
  RESULTS_DIR="$RESULTS_ROOT/$1/$(timestamp)"
  if [[ $DRY_RUN -eq 0 ]]; then
    mkdir -p "$RESULTS_DIR"
  fi
}

cleanup_workdirs() {
  if [[ "$KEEP_WORKDIRS" == 1 ]]; then
    [[ ${#WORKDIRS[@]} -gt 0 ]] && say "kept work dirs: ${WORKDIRS[*]}"
    return 0
  fi
  local dir
  for dir in "${WORKDIRS[@]+"${WORKDIRS[@]}"}"; do
    [[ -n "$dir" && -d "$dir" ]] && rm -rf "$dir"
  done
  return 0
}
trap cleanup_workdirs EXIT

# new_workdir LABEL -> sets WORKDIR to a fresh temp dir registered for cleanup.
# (Not a $(...) function: the cleanup list must live in this shell.)
new_workdir() {
  WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/series-$1.XXXXXX")"
  WORKDIRS+=("$WORKDIR")
}

# setup_repo LABEL VARIANT -> sets REPO to a fresh invoice-app copy with git history.
# Runs in dry-run mode too: it is local, free, and makes the printed paths real.
setup_repo() {
  new_workdir "$1"
  REPO="$WORKDIR/repo"
  "$RUN_DIR/setup-repo.sh" "$REPO" --claude-md "$2" >/dev/null
}

# build_claude_cmd PROMPT MODEL [extra args...] -> sets the CMD array
build_claude_cmd() {
  local prompt="$1" model="$2"
  shift 2
  MODEL_SHOWN="$model"
  CMD=("$CLAUDE_BIN" -p "$prompt"
       --model "$model"
       --output-format stream-json --verbose
       --max-turns "$MAX_TURNS"
       --max-budget-usd "$MAX_BUDGET_USD"
       --permission-mode dontAsk
       --allowedTools "$ALLOWED_TOOLS")
  if [[ -n "$DISALLOWED_TOOLS" ]]; then
    CMD+=(--disallowedTools "$DISALLOWED_TOOLS")
  fi
  if [[ "$ISOLATE" == 1 ]]; then
    # Project settings and the repo's CLAUDE.md load; your ~/.claude settings,
    # user CLAUDE.md, plugins and MCP servers do not, so runs are comparable.
    CMD+=(--setting-sources project,local --strict-mcp-config --no-session-persistence)
  fi
  CMD+=("$@")
}

# print_cmd CWD OUT CMD...: the exact command as one line of valid bash.
# Printed in full for --dry-run (or VERBOSE=1); real runs save it as command.sh.
print_cmd() {
  local cwd="$1" out="$2"
  shift 2
  local quoted line
  quoted="$(printf '%q ' "$@")"
  line="(cd $(printf '%q' "$cwd") && ${quoted% } > $(printf '%q' "$out"))"
  if [[ $DRY_RUN -eq 1 || "${VERBOSE:-0}" == 1 ]]; then
    say "+ $line"
  else
    say "  claude -p … --model ${MODEL_SHOWN:-?} → $(dirname "$out")"
  fi
  LAST_CMD_LINE="$line"
}

# run_session WORKDIR OUTDIR: run the CMD array in WORKDIR, saving
# OUTDIR/transcript.jsonl, OUTDIR/stderr.txt and OUTDIR/meta.json.
# Never fails the script: a non-zero exit (max turns, budget) is data.
run_session() {
  local cwd="$1" out="$2"
  print_cmd "$cwd" "$out/transcript.jsonl" "${CMD[@]}"
  if [[ $DRY_RUN -eq 1 ]]; then
    return 0
  fi
  mkdir -p "$out"
  printf '#!/usr/bin/env bash\n# Exact command this run used.\n%s\n' "$LAST_CMD_LINE" > "$out/command.sh"
  local start end rc=0
  start="$(now_ms)"
  (cd "$cwd" && "${CMD[@]}" > "$out/transcript.jsonl" 2> "$out/stderr.txt" < /dev/null) || rc=$?
  end="$(now_ms)"
  python3 - "$out/meta.json" "$start" "$end" "$rc" "$cwd" <<'PY'
import json, sys
path, start, end, rc, cwd = sys.argv[1:]
json.dump({"wall_ms": int(end) - int(start), "exit_code": int(rc), "workdir": cwd,
           "started_ms": int(start)}, open(path, "w"), indent=2)
PY
  [[ -s "$out/stderr.txt" ]] || rm -f "$out/stderr.txt"
  if [[ $rc -ne 0 ]]; then
    warn "session exited $rc (see $out); continuing"
  fi
  return 0
}

# save_repo_state REPO OUTDIR: diff against the baseline and the test result
save_repo_state() {
  local repo="$1" out="$2"
  [[ $DRY_RUN -eq 1 ]] && return 0
  mkdir -p "$out"
  git -C "$repo" add -A >/dev/null 2>&1 || true
  git -C "$repo" diff --cached --stat HEAD > "$out/diffstat.txt" 2>/dev/null || true
  git -C "$repo" diff --cached HEAD > "$out/diff.patch" 2>/dev/null || true
  git -C "$repo" reset -q >/dev/null 2>&1 || true
  (cd "$repo" && python3 -m unittest > "$out/tests.txt" 2>&1) && echo pass > "$out/tests.status" || echo fail > "$out/tests.status"
}

# Rough per-session cost for small tasks on this repo, from the list prices the
# decks use (Sonnet 5 $2/$10, Opus 5.5 $4/$20, Haiku 4.5 $1/$5, Fable 5.1 $10/$50
# per million input/output tokens; cache reads 0.025-0.1x input). A session here
# is ~6-15 turns over a ~20-40k-token cached prefix. Subscription users spend plan
# usage instead; the dollar figure is then Claude Code's estimate.
per_session_cost() {
  case "$1" in
    *haiku*) echo "0.02 0.10" ;;
    *opus*) echo "0.10 0.50" ;;
    *fable*|*mythos*) echo "0.25 1.25" ;;
    *) echo "0.05 0.25" ;;
  esac
}

# estimate_line MODEL SESSIONS -> "low high cap" in USD
estimate_line() {
  local model="$1" n="$2" lo hi
  read -r lo hi <<< "$(per_session_cost "$model")"
  python3 -c "import sys; n=int(sys.argv[1]); print(f'{n*float(sys.argv[2]):.2f} {n*float(sys.argv[3]):.2f} {n*float(sys.argv[4]):.2f}')" "$n" "$lo" "$hi" "$MAX_BUDGET_USD"
}

# confirm_plan TEXT...: print the plan, then ask unless --yes or --dry-run
confirm_plan() {
  say "────────────────────────────────────────────────────────────"
  local line
  for line in "$@"; do say "$line"; done
  say "Isolation: $( [[ "$ISOLATE" == 1 ]] && echo 'project settings only (--setting-sources project,local --strict-mcp-config)' || echo 'OFF: your user settings, CLAUDE.md, plugins and MCP load too')"
  say "Caps: --max-turns $MAX_TURNS, --max-budget-usd $MAX_BUDGET_USD per session"
  say "Results: ${RESULTS_DIR:-(none)}"
  say "────────────────────────────────────────────────────────────"
  if [[ $DRY_RUN -eq 1 ]]; then
    say "DRY RUN: printing commands only; nothing calls Claude."
    return 0
  fi
  if [[ $ASSUME_YES -eq 1 ]]; then
    return 0
  fi
  if [[ ! -t 0 ]]; then
    die "not a terminal; re-run with --yes to confirm the spend"
  fi
  local answer
  read -r -p "This calls Claude and spends usage. Proceed? [y/N] " answer
  [[ "$answer" == y || "$answer" == Y || "$answer" == yes ]] || die "cancelled"
}

require_claude() {
  if [[ $DRY_RUN -eq 1 ]]; then
    return 0
  fi
  command -v "$CLAUDE_BIN" >/dev/null 2>&1 || die "Claude Code CLI not found ($CLAUDE_BIN). Install it and sign in, or set CLAUDE_BIN."
}

# summarise_talk TALK: build summary.json/summary.md for this run and print the short version
summarise_talk() {
  [[ $DRY_RUN -eq 1 ]] && return 0
  python3 "$ANALYZE" summarise "$1" "$RESULTS_DIR"
  say ""
  say "Saved: $RESULTS_DIR/summary.md"
  say "Refresh the slide map: python3 $RUN_DIR/summarise.py"
}
