#!/usr/bin/env bash
# Lab 5 · judge model (30 min): score 8 commit messages by hand, then with a judge.
#
#   1. Read lab5/HANDOUT.md and lab5/rubric.md; fill in lab5/my-scores.csv by hand
#      (do not open lab5/authors.json yet).
#   2. ./lab5.sh [--dry-run] [--yes]     judge all 8 samples, compare with your scores
#   3. ./lab5.sh --sample                no model calls: synthetic judge scores
#
# 8 judge calls, each one turn with no tools (~2-5k tokens, about 1% of an
# agent session). Reports exact / within-one agreement, Spearman correlation,
# the judge's bias, and the self-preference check (judge minus you, for
# model-written vs human-written samples), with what 8 samples can't show.
# JUDGE_MODELS="claude-sonnet-5 claude-haiku-4-5" adds a second judge (16 calls).
#
# Environment: JUDGE_MODELS (default MODEL; LITE=1: HAIKU_MODEL), SCORES
#   (default lab5/my-scores.csv), PAIR, CLAUDE_BIN, RESULTS_ROOT, ISOLATE
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'; }
parse_common_args "$@"
LAB5_DIR="$LAB_DIR/lab5"
SCORES="${SCORES:-$LAB5_DIR/my-scores.csv}"
if [[ "$LITE" == 1 ]]; then JUDGE_MODELS="${JUDGE_MODELS:-$HAIKU_MODEL}"; else JUDGE_MODELS="${JUDGE_MODELS:-$MODEL}"; fi
read -r -a judge_models <<< "$JUDGE_MODELS"
samples=()
while IFS= read -r f; do samples+=("$f"); done < <(find "$LAB5_DIR/samples" -name 's*.txt' | sort -V)
[[ ${#samples[@]} -gt 0 ]] || die "no samples in $LAB5_DIR/samples"
scored="$(python3 -c 'import sys; sys.path.insert(0, sys.argv[1]); import judge; print(len(judge.read_human(sys.argv[2])))' "$LIB_DIR" "$SCORES")"

if [[ $USE_SAMPLE -eq 1 ]]; then
  RESULTS_DIR="$(mktemp -d "${TMPDIR:-/tmp}/lab5-sample.XXXXXX")"
  trap 'rm -rf "$RESULTS_DIR"' EXIT
  cp -R "$SAMPLE_DIR/lab5-judge" "$RESULTS_DIR/judge"
  human="$SCORES"
  if [[ "$scored" == 0 ]]; then
    human="$SAMPLE_DIR/lab5-human-scores.csv"
    say "No hand scores in $SCORES yet; using the SYNTHETIC ones in $human."
  fi
  python3 "$LIB_DIR/judge.py" compare "$RESULTS_DIR" --human "$human" --sample
  exit 0
fi

n=$(( ${#samples[@]} * ${#judge_models[@]} ))
require_claude
results_dir lab5
confirm_plan \
  "Lab 5 · judge model: ${#samples[@]} samples x ${#judge_models[@]} judge(s): ${judge_models[*]}" \
  "$(plan_line "Expected: $n judge calls (no tools, 1 turn)" judge "$n")" \
  "Hand scores found in $(basename "$SCORES"): $scored of ${#samples[@]}"
if [[ "$scored" == 0 && $DRY_RUN -eq 0 ]]; then
  warn "you have not scored any sample by hand yet; the comparison needs lab5/my-scores.csv (overall column)."
fi
for jm in "${judge_models[@]}"; do
  jargs=(--model "$jm" --out "$RESULTS_DIR/judge")
  [[ $DRY_RUN -eq 1 ]] && jargs+=(--dry-run)
  "$LAB_DIR/judge.sh" "${jargs[@]}" "${samples[@]}" || warn "some judge replies could not be parsed"
done
[[ $DRY_RUN -eq 1 ]] && exit 0
python3 "$LIB_DIR/judge.py" compare "$RESULTS_DIR" --human "$SCORES"
say ""
say "Saved: $RESULTS_DIR/summary.md and export.json"
say "Paste to the board: ./export-results.sh --lab lab5 --latest"
