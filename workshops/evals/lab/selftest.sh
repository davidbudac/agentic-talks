#!/usr/bin/env bash
# Check the whole lab kit without calling Claude. Costs nothing; ~5-8 minutes
# (mostly Maven). Needs the Maven dependencies once (./check-setup.sh).
#
#   ./selftest.sh [--keep] [--quick]
#
# 1. bash -n on every script, Python syntax, the Java build and tests.
# 2. Checkers: every reference solution passes, the untouched repo fails; in
#    lab 3 the weak checker passes both cheats, while the answer key and the
#    eval checker fail them and pass the reference.
# 3. Every runner's --dry-run; each printed '+ ' command parses as bash; no
#    results written.
# 4. Every runner end to end with CLAUDE_BIN=lib/fake_claude.py (reference
#    solutions copied in for some runs, not for others), then trace-report,
#    judge parsing, export-results.sh and schema validation, and
#    record-facilitator-run.sh into a scratch copy of sample-results/.
# Everything goes to a temp dir (deleted unless --keep); the repo is left as it was.
# --quick skips the per-task checker loop in step 2 (the slowest part).
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
keep=0 quick=0
for a in "$@"; do case "$a" in --keep) keep=1 ;; --quick) quick=1 ;; esac; done
export PYTHONDONTWRITEBYTECODE=1
tmp="$(mktemp -d "${TMPDIR:-/tmp}/lab-selftest.XXXXXX")"
[[ $keep -eq 1 ]] || trap 'rm -rf "$tmp"' EXIT
fail=0
ok() { printf '  ok   %s\n' "$*"; }
bad() { printf '  FAIL %s\n' "$*"; fail=1; }
copy_app() { mkdir -p "$1"; (cd "$here/invoice-app" && tar --exclude ./target -cf - .) | (cd "$1" && tar -xf -); }
score() { python3 -c 'import json,sys; print(json.loads(sys.stdin.read() or "{}").get("score"))'; }
TASKS="fix-date-parser fixtures-bom jpy-rounding report-sort-accents export-currency-column rename-customer-field"

echo "1. syntax, build and unit tests"
scripts=("$here"/*.sh "$here"/lib/*.sh "$here"/lab3/checker.sh "$here"/eval/run-claude "$here"/eval/run-claude-lean
         "$here"/eval/run-claude-bloated "$here"/eval/checkers/hidden-tests "$here"/invoice-app/mvnw)
for f in "$here"/take-home/template/eval/run-claude "$here"/take-home/template/eval/checkers/* "$here"/take-home/ci/*.sh; do
  [[ -f "$f" ]] && scripts+=("$f")
done
n=0
for f in "${scripts[@]}"; do
  if bash -n "$f" 2>/dev/null; then n=$((n + 1)); else bad "bash -n ${f#$here/}"; fi
done
ok "bash -n: $n scripts"
for f in "$here"/lib/*.py "$here"/sample-results/*.py; do
  python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$f" || bad "python syntax ${f#$here/}"
done
ok "python syntax: lib/*.py, sample-results/*.py"
copy_app "$tmp/build"
if (cd "$tmp/build" && ./mvnw -q -o -B test > "$tmp/build.log" 2>&1); then
  ok "invoice-app: ./mvnw -q -o test passes ($(cat "$tmp"/build/target/surefire-reports/*.txt | grep -o 'Tests run: [0-9]*' | awk '{s+=$3} END {print s}') tests)"
else
  bad "invoice-app tests (see $tmp/build.log)"
fi
[[ "$(cat "$here/eval/checkers/own-tests-min")" == "$(cat "$tmp"/build/target/surefire-reports/*.txt | grep -o 'Tests run: [0-9]*' | awk '{s+=$3} END {print s}')" ]] \
  && ok "own-tests-min matches the untouched repo" || bad "eval/checkers/own-tests-min does not match the test count"

echo "2. checkers"
if [[ $quick -eq 0 ]]; then
  for task in $TASKS; do
    good="$tmp/good-$task"; copy_app "$good"; cp -R "$here/eval/solutions/$task/." "$good/"
    [[ "$("$here/eval/checkers/hidden-tests" --repo "$good" --task "$task" | score)" == 1.0 ]] \
      && ok "$task: reference solution passes" || bad "$task: reference solution fails"
    [[ "$("$here/eval/checkers/hidden-tests" --repo "$here/invoice-app" --task "$task" | score)" == 0.0 ]] \
      && ok "$task: untouched repo fails" || bad "$task: untouched repo passes"
  done
fi
ref="$tmp/l3-reference"; copy_app "$ref"; cp -R "$here/eval/solutions/export-currency-column/." "$ref/"
[[ "$("$here/lab3/checker.sh" "$here/lab3/weak" "$ref" | score)" == 1.0 ]] && ok "lab3: weak checker passes the reference" || bad "lab3: weak fails the reference"
[[ "$("$here/lab3/checker.sh" "$here/lab3/answer-key" "$ref" | score)" == 1.0 ]] && ok "lab3: answer key passes the reference" || bad "lab3: answer key fails the reference"
for cheat in "$here"/lab3/cheats/*/; do
  name="$(basename "$cheat")"; dir="$tmp/l3-$name"; copy_app "$dir"; cp -R "$cheat." "$dir/"
  [[ "$("$here/lab3/checker.sh" "$here/lab3/weak" "$dir" | score)" == 1.0 ]] && ok "lab3: weak checker passes $name (as designed)" || bad "lab3: weak checker rejects $name"
  [[ "$("$here/lab3/checker.sh" "$here/lab3/answer-key" "$dir" | score)" == 0.0 ]] && ok "lab3: answer key fails $name" || bad "lab3: answer key passes $name"
  [[ "$("$here/eval/checkers/hidden-tests" --repo "$dir" --task export-currency-column | score)" == 0.0 ]] \
    && ok "lab3: eval checker fails $name" || bad "lab3: eval checker passes $name"
done

echo "3. dry runs"
export RESULTS_ROOT="$tmp/dry-results" LAB3_WORK="$tmp/dry-lab3" CLAUDE_BIN="$here/lib/fake_claude.py" PAIR=selftest
for runner in lab1 lab2 lab3 lab4 lab5 lab6 record-facilitator-run; do
  out="$tmp/dry-$runner.txt"
  if "$here/$runner.sh" --dry-run > "$out" 2>&1; then
    n=0
    while IFS= read -r line; do
      printf '%s\n' "${line#+ }" | bash -n 2>/dev/null || { bad "$runner: printed command does not parse: ${line:0:90}"; continue; }
      n=$((n + 1))
    done < <(grep '^+ ' "$out")
    grep -q 'sessions\|model calls' "$out" && ok "$runner --dry-run ($n commands parse, plan printed)" || bad "$runner --dry-run printed no plan"
  else
    bad "$runner --dry-run failed (see $out)"
  fi
done
LOCAL_MODEL=qwen3-coder "$here/lab6.sh" --local --dry-run > "$tmp/dry-local.txt" 2>&1 && ok "lab6 --local --dry-run" || bad "lab6 --local --dry-run"
[[ -e "$RESULTS_ROOT" || -e "$LAB3_WORK" ]] && bad "dry runs wrote files" || ok "dry runs wrote nothing"

echo "4. fake end-to-end runs"
export RESULTS_ROOT="$tmp/results" LAB3_WORK="$tmp/lab3-work" FAKE_PASS_RATE=0.75
sol="$here/eval/solutions"
export FAKE_OVERLAY_MAP="InvoiceDates.parse=$sol/fix-date-parser;legacy-export.csv=$sol/fixtures-bom;Support JPY=$sol/jpy-rounding;code-point order=$sol/report-sort-accents;sixth column=$sol/export-currency-column;Rename the Invoice record=$sol/rename-customer-field"
run_fake() { local name="$1"; shift; if env "$@" > "$tmp/fake-$name.txt" 2>&1; then ok "fake $name"; else bad "fake $name (see $tmp/fake-$name.txt)"; fi; }
run_fake predict "$here/predict.sh" bloated
if command -v uvx >/dev/null 2>&1 || command -v smevals >/dev/null 2>&1; then
  run_fake "lab1 (smevals)" ENGINE=smevals "$here/lab1.sh" --yes
else
  bad "smevals not available (uvx missing): lab1 runs with ENGINE=direct only"
fi
run_fake "lab2 (direct engine)" ENGINE=direct "$here/lab2.sh" --yes
run_fake "lab2 LITE ROLE=a" ENGINE=direct LITE=1 ROLE=a "$here/lab2.sh" --yes
run_fake "lab3 setup" "$here/lab3.sh"
cp "$here/lab3/cheats/cheat-2-hardcoded-eur/src/main/java/com/example/invoicing/CsvExport.java" \
   "$LAB3_WORK/repo/src/main/java/com/example/invoicing/CsvExport.java"
run_fake "lab3 answer" "$here/lab3.sh" answer
grep -q '| yours | PASS' "$tmp/fake-lab3 answer.txt" && ok "lab3 matrix: the cheat you wrote passes weak" || bad "lab3 matrix row"
run_fake lab4 "$here/lab4.sh"
grep -q 're-read' "$tmp/fake-lab4.txt" && ok "lab4 trace-report flags re-reads in fake runs" || bad "lab4 found no re-reads"
run_fake "lab4 --sample" "$here/lab4.sh" --sample
grep -q 'blind retry | 1' "$tmp/fake-lab4 --sample.txt" && grep -q 'restated plan | 1' "$tmp/fake-lab4 --sample.txt" \
  && ok "trace-report flags all four kinds in the sample trace" || bad "trace-report sample flags"
run_fake lab5 ENGINE=direct SCORES="$here/sample-results/lab5-human-scores.csv" "$here/lab5.sh" --yes
grep -q 'Spearman' "$tmp/fake-lab5.txt" && ok "lab5 compares judge with hand scores" || bad "lab5 comparison missing"
run_fake "lab5 --sample" "$here/lab5.sh" --sample
printf '{"type":"result","result":"Scores:\\n```json\\n{\\"accuracy\\": 4, \\"why\\": 3, \\"scope\\": 5, \\"format\\": 4, \\"overall\\": 4, \\"reason\\": \\"ok\\"}\\n```","num_turns":1,"total_cost_usd":0.01}' > "$tmp/judge-out.json"
[[ "$(python3 "$here/lib/judge.py" parse "$tmp/judge-out.json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["scores"]["overall"])')" == 4 ]] \
  && ok "judge.py parses a fenced JSON reply" || bad "judge.py parse"
printf '{"type":"result","result":"I would rate it highly.","num_turns":1}' > "$tmp/judge-bad.json"
python3 "$here/lib/judge.py" parse "$tmp/judge-bad.json" >/dev/null 2>&1 && bad "judge.py accepted a reply without scores" || ok "judge.py rejects a reply without scores"
run_fake lab6 ENGINE=direct "$here/lab6.sh" --yes
python3 - "$RESULTS_ROOT" <<'PY' && ok "lab6 reused sonnet runs from labs 1-2" || bad "lab6 reuse"
import json, sys, glob
data = json.load(open(sorted(glob.glob(sys.argv[1] + "/lab6/*/reused.json"))[-1]))
sys.exit(0 if data else 1)
PY
run_fake "lab6 OPUS=1 REUSE=0 LITE=1" ENGINE=direct OPUS=1 REUSE=0 LITE=1 "$here/lab6.sh" --yes
"$here/export-results.sh" > "$tmp/export.jsonl" 2> "$tmp/export.err" && ok "export-results.sh: $(wc -l < "$tmp/export.jsonl" | tr -d ' ') lines" || bad "export-results.sh (see $tmp/export.err)"
"$here/export-results.sh" --validate "$tmp/export.jsonl" > "$tmp/validate.txt" && ok "exported lines validate: $(tail -1 "$tmp/validate.txt")" || bad "schema validation: $(tail -3 "$tmp/validate.txt")"
python3 - "$tmp/export.jsonl" <<'PY' && ok "export covers lab1, lab2, lab5, lab6, predictions and judge lines" || bad "export coverage"
import json, sys
lines = [json.loads(l) for l in open(sys.argv[1])]
labs = {l["lab"] for l in lines if "kind" not in l}
kinds = {l.get("kind") for l in lines}
sys.exit(0 if labs >= {"lab1", "lab2", "lab5", "lab6"} and {"prediction", "judge"} <= kinds
         and any(l["passed"] is False for l in lines if "kind" not in l) and any(l["passed"] for l in lines if "kind" not in l) else 1)
PY
"$here/export-results.sh" --sample | "$here/export-results.sh" --validate - > /dev/null && ok "sample-results export validates" || bad "sample export"
printf '{"v":1,"pair":"x","lab":"lab3","variant":"lean","task":"t","run":1,"passed":true,"turns":1,"input_tokens":1,"output_tokens":1,"cache_read_tokens":1,"cache_write_tokens":1,"cost_usd":0.1,"duration_s":1,"model":"m","extra":1}\n' \
  | "$here/export-results.sh" --validate - > /dev/null && bad "validator accepted a bad line" || ok "validator rejects a bad line"
sample_copy="$tmp/sample-copy"; cp -R "$here/sample-results" "$sample_copy"
run_fake "record-facilitator-run" ENGINE=direct SAMPLE_DIR="$sample_copy" FACILITATOR_RESULTS="$tmp/facilitator" \
  SCORES="$here/sample-results/lab5-human-scores.csv" "$here/record-facilitator-run.sh" --yes
grep -q '^REAL' "$sample_copy/SOURCE" && [[ -n "$(find "$sample_copy/traces" -name 'facilitator-*.jsonl')" ]] \
  && "$here/export-results.sh" --validate "$sample_copy/export.jsonl" > /dev/null \
  && ok "record-facilitator-run replaced the synthetic set (in a scratch copy)" || bad "record-facilitator-run output"

echo "5. repo left clean"
leftovers="$(cd "$here" && find . \( -name target -o -name results -o -name lab3-work -o -name __pycache__ -o -name .pair \) -not -path './take-home/*' 2>/dev/null || true)"
[[ -z "$leftovers" ]] && ok "no target/, results/, lab3-work/, .pair or __pycache__ in the kit" || bad "left behind: $leftovers"

echo
if [[ $fail -eq 0 ]]; then echo "selftest passed"; else echo "selftest FAILED"; fi
[[ $keep -eq 1 ]] && echo "kept: $tmp"
exit $fail
