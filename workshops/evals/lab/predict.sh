#!/usr/bin/env bash
# Lab 1: record your pair's prediction BEFORE running ./lab1.sh.
#
#   ./predict.sh lean       the lean CLAUDE.md will be cheaper per passing run
#   ./predict.sh bloated    the bloated one will (for example, because it explains more)
#
# Writes results/predictions/<ts>.json, which ./export-results.sh sends to the
# board as {"v":1,"pair":...,"lab":"lab1","kind":"prediction","variant":...}.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
case "${1:-}" in
  lean|bloated) exec python3 "$here/lib/labkit.py" predict "$1" ;;
  *) sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 2 ;;
esac
