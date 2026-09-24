#!/usr/bin/env bash
# Run the eval suite for k rounds, print a summary, fail below a pass-rate threshold.
# Generic CI version (Jenkins, GitLab CI, a cron box); the GitHub Actions workflow
# calls the same script.
#
#   REPO_DIR=. ./run-evals.sh            # from your repo root, eval/ next to it
#
# Environment:
#   EVAL_DIR    the smevals eval folder              (default: eval)
#   RUNS_DIR    where runs are written                (default: runs)
#   ROUNDS      k, runs per task and model            (default: 3)
#   MODEL       model id                              (default: claude-sonnet-5)
#   TASKS       space-separated task names            (default: all)
#   THRESHOLD   minimum pass rate, 0..1               (default: 0.8)
#   SMEVALS     smevals command                       (default: uvx --from smevals==0.2.0 smevals)
#   REPO_URL / REPO_DIR   passed through to run-claude (one is required)
#   ANTHROPIC_API_KEY     CI has no subscription login: use an API key
#
# smevals 0.2.0 has no -n flag, so each round is one `smevals run` call.
set -euo pipefail
EVAL_DIR="${EVAL_DIR:-eval}"
RUNS_DIR="${RUNS_DIR:-runs}"
ROUNDS="${ROUNDS:-3}"
MODEL="${MODEL:-claude-sonnet-5}"
THRESHOLD="${THRESHOLD:-0.8}"
SMEVALS="${SMEVALS:-uvx --from smevals==0.2.0 smevals}"
read -r -a smevals_cmd <<< "$SMEVALS"
task_args=()
for task in ${TASKS:-}; do task_args+=(-t "$task"); done
export REPO_DIR="${REPO_DIR:-}" REPO_URL="${REPO_URL:-}"

round=1
while [ "$round" -le "$ROUNDS" ]; do
  echo "== round $round/$ROUNDS ($MODEL)"
  # smevals exits non-zero when any run grades as fail; that is data, not an error.
  "${smevals_cmd[@]}" run "$EVAL_DIR" -c default -m "$MODEL" ${task_args[@]+"${task_args[@]}"} -g --runs-dir "$RUNS_DIR" || true
  round=$((round + 1))
done

"${smevals_cmd[@]}" report "$EVAL_DIR" --runs-dir "$RUNS_DIR" --by-task > "$RUNS_DIR/report.md" || true
"${smevals_cmd[@]}" report "$EVAL_DIR" --runs-dir "$RUNS_DIR" --json > "$RUNS_DIR/grades.json"

python3 - "$RUNS_DIR/grades.json" "$THRESHOLD" <<'PY'
import json, sys
from collections import defaultdict
from pathlib import Path

rows = json.load(open(sys.argv[1])).get("rows", [])
threshold = float(sys.argv[2])
cells = defaultdict(list)
total_cost = 0.0
for row in rows:
    passed = row.get("outcome") == "pass"
    cells[(row.get("task"), row.get("model"))].append(passed)
    transcript = Path(row.get("run_dir", "")) / "transcript.jsonl"
    if transcript.is_file():
        for line in transcript.read_text(errors="replace").splitlines():
            if '"type":"result"' in line.replace(" ", ""):
                try:
                    total_cost += float(json.loads(line).get("total_cost_usd") or 0)
                except ValueError:
                    pass
print(f"{'task':<28} {'model':<22} passes  pass@k  pass^k")
for (task, model), results in sorted(cells.items()):
    print(f"{task:<28} {model:<22} {sum(results)}/{len(results):<5} {str(any(results)):<7} {all(results)}")
runs = sum(len(r) for r in cells.values())
passes = sum(sum(r) for r in cells.values())
rate = passes / runs if runs else 0.0
print(f"\npass rate {passes}/{runs} = {rate:.2f} (threshold {threshold:.2f})")
print(f"cost ${total_cost:.2f} (Claude Code's estimate); per accepted task "
      + (f"${total_cost / passes:.2f}" if passes else "n/a"))
sys.exit(0 if runs and rate >= threshold else 1)
PY
