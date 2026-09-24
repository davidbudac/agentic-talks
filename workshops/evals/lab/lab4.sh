#!/usr/bin/env bash
# Lab 4 · read the traces (30 min, no model calls).
#
#   ./lab4.sh             trace-report over your lab 1 and lab 2 transcripts
#                         (falls back to the two SYNTHETIC sample traces if you have none)
#   ./lab4.sh --sample    only the sample traces
#   ./lab4.sh --dry-run   list the transcripts it would read
#
# Writes results/lab4/<ts>/trace-report.md (and .json). Then open the flagged
# transcripts and decide, per flag, whether it is really waste. A CLAUDE.md or
# prompt change that removes it is your candidate for the next eval run.
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; }
parse_common_args "$@"

transcripts=()
if [[ $USE_SAMPLE -eq 0 ]]; then
  while IFS= read -r f; do transcripts+=("$f"); done < <(
    find "$RESULTS_ROOT/lab1" "$RESULTS_ROOT/lab2" -name transcript.jsonl -size +0 2>/dev/null | sort)
fi
if [[ ${#transcripts[@]} -eq 0 ]]; then
  [[ $USE_SAMPLE -eq 1 ]] || say "No lab 1/2 transcripts yet: using the SYNTHETIC sample traces."
  while IFS= read -r f; do transcripts+=("$f"); done < <(find "$SAMPLE_DIR/traces" -name '*.jsonl' | sort)
fi
say "Lab 4 · trace report over ${#transcripts[@]} transcript(s); no model calls."
if [[ $DRY_RUN -eq 1 ]]; then
  for f in "${transcripts[@]}"; do say "  $f"; done
  say "+ python3 lib/traces.py --md results/lab4/TIMESTAMP/trace-report.md TRANSCRIPTS..."
  exit 0
fi
results_dir lab4
python3 "$LIB_DIR/traces.py" --md "$RESULTS_DIR/trace-report.md" --json "$RESULTS_DIR/trace-report.json" "${transcripts[@]}"
say "Saved: $RESULTS_DIR/trace-report.md"
