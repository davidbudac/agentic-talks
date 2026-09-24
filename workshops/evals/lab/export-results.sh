#!/usr/bin/env bash
# Print your results for the shared board: one compact JSON line per run.
#
#   ./export-results.sh                     every run, prediction and judge score so far
#   ./export-results.sh --lab lab2          one lab (lab1 | lab2 | lab5 | lab6)
#   ./export-results.sh --lab lab2 --latest only that lab's most recent run
#   ./export-results.sh --sample            the SYNTHETIC sample set (board rehearsal)
#   ./export-results.sh | pbcopy            then paste into the board
#   ./export-results.sh --validate FILE     check lines against RESULTS-SCHEMA.md
#
# Reads results/<lab>/<ts>/export.json and results/predictions/. Lines that do
# not validate against the schema are reported on stderr and left out.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
case "${1:-}" in
  -h|--help) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  --validate) shift; exec python3 "$here/lib/labkit.py" validate "${1:--}" ;;
esac
exec python3 "$here/lib/labkit.py" export "$@"
