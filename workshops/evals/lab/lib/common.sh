# Shared helpers for the lab runners. Source it; do not execute it.
# shellcheck shell=bash
#
# Environment knobs (all optional; README.md has the full table):
#   PAIR            pair id on the shared board (default: .pair file, else a hostname hash)
#   ROLE            both (default) | a | b: split a pair's sessions across two laptops
#   LITE=1          fewer runs in every lab (see README budget table)
#   MODEL           the "workhorse" model            (default claude-sonnet-5)
#   HAIKU_MODEL     the cheap model in lab 6         (default claude-haiku-4-5)
#   OPUS_MODEL      the optional frontier model      (default claude-opus-5-5)
#   MAX_TURNS       --max-turns per session          (default 25)
#   MAX_BUDGET_USD  --max-budget-usd per session     (default 0.75, a hard stop per run)
#   ENGINE          smevals (default when uvx/smevals is available) | direct
#   CLAUDE_BIN      the Claude Code binary           (default: claude on PATH)
#   RESULTS_ROOT    where results go                 (default workshops/evals/lab/results)
#   ISOLATE=0       also load your user settings, user CLAUDE.md, plugins and MCP servers
#   KEEP_WORKDIRS=1 keep the temporary repo copies for inspection

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LIB_DIR="$LAB_DIR/lib"
APP_DIR="$LAB_DIR/invoice-app"
EVAL_DIR="$LAB_DIR/eval"
SAMPLE_DIR="${SAMPLE_DIR:-$LAB_DIR/sample-results}"
LABKIT="$LIB_DIR/labkit.py"
RESULTS_ROOT="${RESULTS_ROOT:-$LAB_DIR/results}"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
MODEL="${MODEL:-claude-sonnet-5}"
HAIKU_MODEL="${HAIKU_MODEL:-claude-haiku-4-5}"
OPUS_MODEL="${OPUS_MODEL:-claude-opus-5-5}"
MAX_TURNS="${MAX_TURNS:-25}"
MAX_BUDGET_USD="${MAX_BUDGET_USD:-0.75}"
ISOLATE="${ISOLATE:-1}"
KEEP_WORKDIRS="${KEEP_WORKDIRS:-0}"
LITE="${LITE:-0}"
ROLE="${ROLE:-both}"
SMEVALS_SPEC="${SMEVALS_SPEC:-smevals==0.2.0}"
export PYTHONDONTWRITEBYTECODE=1
export RESULTS_ROOT SAMPLE_DIR CLAUDE_BIN MAX_TURNS MAX_BUDGET_USD ISOLATE KEEP_WORKDIRS

# Tools the agent may use without asking. Everything else is denied (dontAsk),
# so no session can install packages, fetch URLs or push. ./mvnw may download
# only if the Maven cache is cold; check-setup.sh prefetches it.
ALLOWED_TOOLS="${ALLOWED_TOOLS:-Read,Edit,Write,Glob,Grep,Bash(./mvnw),Bash(./mvnw *),Bash(java *),Bash(cd *),Bash(pwd),Bash(ls),Bash(ls *),Bash(cat *),Bash(head *),Bash(tail *),Bash(wc *),Bash(grep *),Bash(find *),Bash(git status*),Bash(git diff*),Bash(git log*),Bash(git show*)}"
DISALLOWED_TOOLS="${DISALLOWED_TOOLS:-Agent,WebFetch,WebSearch}"
export ALLOWED_TOOLS DISALLOWED_TOOLS

DRY_RUN=0
ASSUME_YES=0
USE_SAMPLE=0
REST_ARGS=()

say() { printf '%s\n' "$*"; }
warn() { printf 'warning: %s\n' "$*" >&2; }
die() { printf 'error: %s\n' "$*" >&2; exit 1; }

case "$ROLE" in both|a|b) ;; *) die "ROLE must be both, a or b (got $ROLE)" ;; esac

# Parse --dry-run / --yes / --sample / --help; other arguments land in REST_ARGS.
parse_common_args() {
  REST_ARGS=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dry-run|-n) DRY_RUN=1 ;;
      --yes|-y) ASSUME_YES=1 ;;
      --sample) USE_SAMPLE=1 ;;
      -h|--help) usage; exit 0 ;;
      *) REST_ARGS+=("$1") ;;
    esac
    shift
  done
}

timestamp() { date -u +%Y%m%dT%H%M%SZ; }

# results_dir LAB -> sets RESULTS_DIR (created unless dry run)
results_dir() {
  RESULTS_DIR="$RESULTS_ROOT/$1/$(timestamp)"
  if [[ $DRY_RUN -eq 0 ]]; then
    mkdir -p "$RESULTS_DIR"
  fi
}

pair_id() { python3 "$LABKIT" pair; }

# Pick the eval engine: smevals through uvx (or on PATH), else the built-in
# direct loop, which writes the same files. ENGINE=direct forces the fallback.
pick_engine() {
  ENGINE="${ENGINE:-auto}"
  SMEVALS_CMD=()
  if [[ "$ENGINE" == auto || "$ENGINE" == smevals ]]; then
    if [[ -n "${SMEVALS:-}" ]]; then
      read -r -a SMEVALS_CMD <<< "$SMEVALS"
    elif command -v smevals >/dev/null 2>&1; then
      SMEVALS_CMD=(smevals)
    elif command -v uvx >/dev/null 2>&1; then
      SMEVALS_CMD=(uvx --from "$SMEVALS_SPEC" smevals)
    fi
    if [[ ${#SMEVALS_CMD[@]} -gt 0 ]] && { [[ $DRY_RUN -eq 1 ]] || "${SMEVALS_CMD[@]}" --version >/dev/null 2>&1; }; then
      ENGINE=smevals
    elif [[ "$ENGINE" == smevals ]]; then
      die "ENGINE=smevals but smevals is not runnable (install uv, or run ./check-setup.sh)"
    else
      ENGINE=direct
    fi
  fi
  [[ "$ENGINE" == smevals || "$ENGINE" == direct ]] || die "ENGINE must be smevals or direct"
}

# model_alias MODEL -> haiku | sonnet | opus | local | the model id
model_alias() {
  case "$1" in
    *haiku*) echo haiku ;;
    *sonnet*) echo sonnet ;;
    *opus*) echo opus ;;
    *) echo "$1" ;;
  esac
}

# estimate KIND N -> prints "tokens_lo tokens_hi usd_lo usd_hi min_lo min_hi" for N sessions.
# KIND: sonnet | haiku | opus | local | judge. From the list prices the decks use
# (Sonnet 5 $2/$10, Haiku 4.5 $1/$5, Opus 5.5 $4/$20 per million input/output
# tokens; cache reads 0.1x, writes 1.25x) and small tasks on this repo: a
# session is ~8-20 API calls over a ~25-35k-token cached prefix, so 0.25-0.6M
# tokens processed, ~90% of them cache reads. A judge call is one turn with no
# tools. Estimates, not meter readings.
estimate() {
  python3 - "$1" "$2" <<'PY'
import sys
kind, n = sys.argv[1], int(sys.argv[2])
table = {  # tokens per session (lo, hi), USD per session (lo, hi), minutes (lo, hi)
    "sonnet": ((250e3, 600e3), (0.15, 0.45), (2, 5)),
    "haiku": ((250e3, 700e3), (0.05, 0.20), (1.5, 4)),
    "opus": ((250e3, 600e3), (0.30, 0.90), (2.5, 6)),
    "local": ((150e3, 500e3), (0.0, 0.0), (5, 20)),
    "judge": ((2e3, 5e3), (0.005, 0.02), (0.1, 0.3)),
}
(tl, th), (ul, uh), (ml, mh) = table.get(kind, table["sonnet"])
print(f"{n*tl/1e6:.2f} {n*th/1e6:.2f} {n*ul:.2f} {n*uh:.2f} {n*ml:.0f} {n*mh:.0f}")
PY
}

# plan_line LABEL KIND N -> one human line for the plan
plan_line() {
  local label="$1" kind="$2" n="$3" tl th ul uh ml mh
  read -r tl th ul uh ml mh <<< "$(estimate "$kind" "$n")"
  printf '  %-34s %3s sessions  ~%s-%sM tokens  ~$%s-%s  ~%s-%s min\n' "$label" "$n" "$tl" "$th" "$ul" "$uh" "$ml" "$mh"
}

# confirm_plan TEXT...: print the plan, then ask unless --yes or --dry-run
confirm_plan() {
  say "────────────────────────────────────────────────────────────────────────"
  local line
  for line in "$@"; do say "$line"; done
  say "Pair: $(pair_id)   Role: $ROLE   Lite: $LITE   Engine: ${ENGINE:-n/a}"
  say "Isolation: $( [[ "$ISOLATE" == 1 ]] && echo 'project settings only (--setting-sources project,local --strict-mcp-config)' || echo 'OFF: your user settings, CLAUDE.md, plugins and MCP load too')"
  say "Caps per session: --max-turns $MAX_TURNS, --max-budget-usd $MAX_BUDGET_USD"
  say "Subscription note: dollar figures are Claude Code's API-price estimates; on Pro/Max the runs use plan usage instead."
  say "Results: ${RESULTS_DIR:-(none)}"
  say "────────────────────────────────────────────────────────────────────────"
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
  read -r -p "This calls Claude and uses your plan. Proceed? [y/N] " answer
  [[ "$answer" == y || "$answer" == Y || "$answer" == yes ]] || die "cancelled"
}

require_claude() {
  [[ $DRY_RUN -eq 1 ]] && return 0
  command -v "$CLAUDE_BIN" >/dev/null 2>&1 || die "Claude Code CLI not found ($CLAUDE_BIN). Install it and sign in (./check-setup.sh), or set CLAUDE_BIN."
}

# run_cells LAB CONFIG MODEL VARIANT ROUND TASK... : one run per task through
# the chosen engine. Every run leaves runs/<task>/<config>/<model>/<ts>/ with
# repo/, transcript.jsonl, metrics.json, labrun.json and check.json.
run_cells() {
  local lab="$1" config="$2" model="$3" variant="$4" round="$5"
  shift 5
  local tasks=("$@") task
  export LAB_NAME="$lab" LAB_VARIANT="$variant" LAB_ROUND="$round"
  if [[ "$ENGINE" == smevals ]]; then
    local task_args=()
    for task in "${tasks[@]}"; do task_args+=(-t "$task"); done
    local cmd=("${SMEVALS_CMD[@]}" run "$EVAL_DIR" -c "$config" -m "$model" "${task_args[@]}" -g --runs-dir "$RESULTS_DIR/runs")
    say "+ $(printf '%q ' "${cmd[@]}")"
    if [[ $DRY_RUN -eq 0 ]]; then
      # smevals exits non-zero when a run grades as fail; that is data, not an error.
      "${cmd[@]}" || true
    fi
  else
    for task in "${tasks[@]}"; do
      say "+ LAB_VARIANT=$variant eval/run-claude-$config  # task $task, model $model, round $round (direct engine)"
      [[ $DRY_RUN -eq 1 ]] && continue
      direct_run "$config" "$model" "$task"
    done
  fi
}

# direct_run CONFIG MODEL TASK: what `smevals run -g` does for one run, without smevals.
direct_run() {
  local config="$1" model="$2" task="$3" run_dir prompt
  run_dir="$RESULTS_DIR/runs/$task/$config/$(printf '%s' "$model" | tr -c 'A-Za-z0-9._-' '-')/$(date -u +%Y-%m-%dT%H-%M-%SZ)-$RANDOM"
  mkdir -p "$run_dir"
  prompt="$(python3 "$LABKIT" task-prompt "$EVAL_DIR/tasks/$task.yaml")"
  printf '%s / %s / %s ... ' "$task" "$config" "$model"
  if (cd "$run_dir" && SMEVALS_RUN_DIR="$run_dir" SMEVALS_TASK="$task" SMEVALS_MODEL="$model" SMEVALS_PROMPT="$prompt" \
        "$EVAL_DIR/run-claude-$config" > "$run_dir/output.txt" 2> "$run_dir/stderr.txt"); then
    say "ok"
  else
    say "harness error (see $run_dir/stderr.txt)"
    return 0
  fi
  [[ -s "$run_dir/stderr.txt" ]] || rm -f "$run_dir/stderr.txt"
  mkdir -p "$run_dir/grades/default"
  (cd "$run_dir/grades/default" && SMEVALS_RUN_DIR="$run_dir" SMEVALS_TASK="$task" \
      "$EVAL_DIR/checkers/hidden-tests" > "$run_dir/grades/default/checker.json" 2>/dev/null) \
    && say "    grade: pass" || say "    grade: fail"
}

# finish_lab LAB: build export.json and the summary for this run
finish_lab() {
  [[ $DRY_RUN -eq 1 ]] && return 0
  python3 "$LABKIT" collect "$1" "$RESULTS_DIR"
  python3 "$LABKIT" summary "$1" "$RESULTS_DIR"
  say ""
  say "Saved: $RESULTS_DIR/summary.md and export.json"
  say "Paste to the board: ./export-results.sh --lab $1 --latest"
}
