#!/usr/bin/env bash
# Flag wasted work in Claude Code stream-json transcripts (no model calls).
#
#   ./trace-report.sh [--md OUT.md] TRANSCRIPT.jsonl...
#   ./trace-report.sh results/lab2/*/runs/*/*/*/*/transcript.jsonl
#   ./trace-report.sh sample-results/traces/*.jsonl
#
# Flags re-reads of the same file, repeated identical tool calls, blind retries
# after a failure and restated plans, with the tokens each put into the context
# and an estimated cost. See lib/traces.py for the method.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
case "${1:-}" in -h|--help|"") sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;; esac
exec python3 "$here/lib/traces.py" "$@"
