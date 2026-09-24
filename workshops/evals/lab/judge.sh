#!/usr/bin/env bash
# Score commit messages with a judge model: claude -p against lab5/rubric.md.
#
#   ./judge.sh [--model M] [--out DIR] [--dry-run] SAMPLE.txt...
#   ./judge.sh lab5/samples/s3.txt
#
# One headless call per sample: no tools (--tools ""), one turn, a short system
# prompt instead of Claude Code's default, the rubric, the diff (lab5/change.diff)
# and the message in the prompt. The judge never sees who wrote the message.
# Prints one JSON line per sample: {"sample", "scores": {accuracy, why, scope,
# format, overall, reason}, "meta": {turns, tokens, cost_usd, ...}}. With --out,
# also saves DIR/<model alias>/<sample>.raw.json (Claude's output) and .json.
#
# Environment: JUDGE_MODEL (default MODEL, claude-sonnet-5), JUDGE_BUDGET_USD
#   (0.10 per call), CLAUDE_BIN, ISOLATE
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; }
judge_model="${JUDGE_MODEL:-$MODEL}"
out=""
samples=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --model) judge_model="$2"; shift 2 ;;
    --out) out="$2"; shift 2 ;;
    --dry-run|-n) DRY_RUN=1; shift ;;
    --yes|-y) shift ;;
    -h|--help) usage; exit 0 ;;
    *) samples+=("$1"); shift ;;
  esac
done
[[ ${#samples[@]} -gt 0 ]] || { usage >&2; exit 2; }
require_claude
alias_name="$(model_alias "$judge_model")"
system_prompt="$(python3 "$LIB_DIR/judge.py" system)"
scratch="$(mktemp -d "${TMPDIR:-/tmp}/lab-judge.XXXXXX")"
trap 'rm -rf "$scratch"' EXIT
rc=0
for sample in "${samples[@]}"; do
  [[ -f "$sample" ]] || die "no such sample: $sample"
  sid="$(basename "$sample" .txt)"
  prompt="$(python3 "$LIB_DIR/judge.py" prompt "$sample")"
  cmd=("$CLAUDE_BIN" -p "$prompt" --model "$judge_model" --output-format json --max-turns 1
       --tools "" --system-prompt "$system_prompt" --permission-mode dontAsk
       --max-budget-usd "${JUDGE_BUDGET_USD:-0.10}")
  [[ "$ISOLATE" == 1 ]] && cmd+=(--setting-sources project,local --strict-mcp-config --no-session-persistence)
  if [[ $DRY_RUN -eq 1 ]]; then
    say "+ (cd $(printf '%q' "$scratch") && $(printf '%q ' "${cmd[@]:0:2}")\"<rubric + diff + $sid>\" $(printf '%q ' "${cmd[@]:3}"))"
    continue
  fi
  raw="$scratch/$sid.raw.json"
  (cd "$scratch" && "${cmd[@]}" > "$raw" 2> "$scratch/$sid.err" < /dev/null) || true
  parsed="$(python3 "$LIB_DIR/judge.py" parse "$raw")" || { warn "$sid: could not parse the judge's reply (see ${out:-$scratch}/$alias_name/$sid.raw.json)"; rc=1; }
  line="$(python3 -c 'import json,sys; d=json.loads(sys.argv[2]); d={"sample": sys.argv[1], "model": sys.argv[3], **d}; print(json.dumps(d, ensure_ascii=False))' "$sid" "$parsed" "$judge_model")"
  if [[ -n "$out" ]]; then
    mkdir -p "$out/$alias_name"
    cp "$raw" "$out/$alias_name/$sid.raw.json"
    printf '%s\n' "$line" > "$out/$alias_name/$sid.json"
  fi
  printf '%s\n' "$line"
done
exit $rc
