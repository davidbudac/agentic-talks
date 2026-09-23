#!/usr/bin/env bash
# Check the whole kit without calling Claude. Safe to run any time; costs nothing.
#
#   run/selftest.sh [--keep]
#
# 1. bash -n on every script, unit tests in invoice-app and talk03/start.
# 2. Checkers: reference solutions pass, the untouched repo fails.
# 3. Every runner's --dry-run, and each printed command parses as bash.
# 4. Every runner end to end with CLAUDE_BIN=lib/fake_claude.py (synthetic
#    transcripts, reference solutions copied in), then summarise.py.
# Results go to a temp dir (deleted unless --keep); nothing lands in results/.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
series="$(cd "$here/.." && pwd)"
keep=0; [[ "${1:-}" == --keep ]] && keep=1
export PYTHONDONTWRITEBYTECODE=1
tmp="$(mktemp -d "${TMPDIR:-/tmp}/series-selftest.XXXXXX")"
[[ $keep -eq 1 ]] || trap 'rm -rf "$tmp"' EXIT
fail=0
ok() { printf '  ok   %s\n' "$*"; }
bad() { printf '  FAIL %s\n' "$*"; fail=1; }

echo "1. syntax and unit tests"
for f in "$here"/*.sh "$here"/lib/common.sh "$series"/eval/run-claude*; do
  bash -n "$f" && ok "bash -n ${f#$series/}" || bad "bash -n $f"
done
for f in "$here"/*.py "$here"/lib/*.py "$series"/eval/checkers/hidden-tests "$series"/talk03/check.py "$series"/invoice-app/tools/invoice_mcp.py; do
  python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$f" && ok "python syntax ${f#$series/}" || bad "syntax $f"
done
(cd "$series/invoice-app" && python3 -m unittest -q 2>&1 | tail -1 | grep -q OK) && ok "invoice-app unit tests" || bad "invoice-app unit tests"
(cd "$series/talk03/start" && python3 -m unittest -q 2>&1 | tail -1 | grep -q OK) && ok "talk03/start unit tests" || bad "talk03/start unit tests"

echo "2. checkers"
for sol in "$series"/eval/solutions/*/; do
  task="$(basename "$sol")"
  good="$tmp/chk-good-$task"; base="$tmp/chk-base-$task"
  cp -R "$series/invoice-app" "$good"; cp -R "$sol". "$good/"; cp -R "$series/invoice-app" "$base"
  "$series/eval/checkers/hidden-tests" --repo "$good" --task "$task" >/dev/null && ok "$task: solution passes" || bad "$task: solution fails"
  "$series/eval/checkers/hidden-tests" --repo "$base" --task "$task" >/dev/null && bad "$task: untouched repo passes" || ok "$task: untouched repo fails"
done
mkdir -p "$tmp/t03-good" "$tmp/t03-broken"
cp "$series/talk03/start/"*.py "$tmp/t03-good/"; cp "$series/../v2/invoice/after/"*.py "$tmp/t03-good/"
cp "$tmp/t03-good/"*.py "$tmp/t03-broken/"
sed -i.bak "s/'gross'\]/'total']/" "$tmp/t03-broken/export.py" && rm -f "$tmp/t03-broken/export.py.bak"
python3 "$series/talk03/check.py" "$tmp/t03-good" >/dev/null && ok "talk03: reference after/ accepted" || bad "talk03: reference rejected"
python3 "$series/talk03/check.py" "$tmp/t03-broken" >/dev/null && bad "talk03: broken copy accepted" || ok "talk03: broken copy rejected"
python3 "$series/talk03/check.py" "$series/talk03/start" >/dev/null && bad "talk03: start accepted" || ok "talk03: start (no export) rejected"
find "$series/talk03" -name __pycache__ -prune -exec rm -rf {} +

echo "3. dry runs"
export RESULTS_ROOT="$tmp/results"
for runner in talk03 talk04 talk05 talk06 talk07; do
  out="$tmp/dry-$runner.txt"
  if "$here/$runner.sh" --dry-run > "$out" 2>&1; then
    n=0
    while IFS= read -r line; do
      printf '%s\n' "${line#+ }" | bash -n 2>/dev/null || { bad "$runner: printed command does not parse: ${line:0:80}"; continue; }
      n=$((n + 1))
    done < <(grep '^+ ' "$out")
    ok "$runner --dry-run ($n commands parse)"
  else
    bad "$runner --dry-run failed (see $out)"
  fi
done
"$here/record.sh" 06-s23 --dry-run >/dev/null 2>&1 && ok "record.sh --dry-run" || bad "record.sh --dry-run"
[[ -d "$RESULTS_ROOT" ]] && bad "dry runs created $RESULTS_ROOT" || ok "dry runs wrote no results"

echo "4. fake end-to-end runs"
sol="$series/eval/solutions"
mkdir -p "$tmp/t03-overlay"; cp "$series/../v2/invoice/after/export.py" "$series/../v2/invoice/after/test_export.py" "$tmp/t03-overlay/"
export CLAUDE_BIN="$here/lib/fake_claude.py"
export FAKE_OVERLAY_MAP="Acceptance contract=$tmp/t03-overlay;backlog/004=$sol/report-customer-filter;backlog/001=$sol/export-currency-column;backlog/002=$sol/export-due-date-column;backlog/006=$sol/fix-date-parser;backlog/005=$sol/fixtures-bom"
run_fake() { local name="$1"; shift; if env "$@" > "$tmp/fake-$name.txt" 2>&1; then ok "fake $name"; else bad "fake $name (see $tmp/fake-$name.txt)"; fi; }
run_fake talk03 RUNS=1 "$here/talk03.sh" --yes
run_fake talk04 "$here/talk04.sh" --yes
run_fake talk05 "$here/talk05.sh" --yes
run_fake talk06 "$here/talk06.sh" --yes
if command -v uvx >/dev/null 2>&1 || command -v smevals >/dev/null 2>&1; then
  run_fake talk07 "TASKS=fix-date-parser fixtures-bom jpy-rounding" RUNS=2 "$here/talk07.sh" --yes
else
  bad "talk07 skipped: neither smevals nor uvx on PATH"
fi
python3 -c "import json,glob,sys; m=json.load(open(glob.glob(sys.argv[1])[0])); sys.exit(m['second_merge']!='conflict')" "$RESULTS_ROOT/talk06/*/merge.json" \
  && ok "talk06 overlap pair conflicts at merge" || bad "talk06 conflict not detected"
python3 "$here/summarise.py" --results "$RESULTS_ROOT" > "$tmp/summarise.txt" && ok "summarise.py: $(cat "$tmp/summarise.txt")" || bad "summarise.py"

echo
if [[ $fail -eq 0 ]]; then echo "selftest passed"; else echo "selftest FAILED"; fi
[[ $keep -eq 1 ]] && echo "kept: $tmp"
exit $fail
