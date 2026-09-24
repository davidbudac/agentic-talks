#!/usr/bin/env bash
# Facilitator dry run: run labs 1, 2, 5 and 6 once for real, then replace the
# SYNTHETIC set in sample-results/ with the real data.
#
#   ./record-facilitator-run.sh --dry-run     the plan and every command, no calls
#   ./record-facilitator-run.sh               asks once, then runs everything
#   ./record-facilitator-run.sh --yes         no question (for a scripted rehearsal)
#
# Budget: the same as one pair's full workshop, ~18 agent sessions plus 8 judge
# calls (see README.md), about 45-90 minutes. Before you start, score the lab 5
# samples by hand in lab5/my-scores.csv (and ideally replace the four stand-in
# "human" samples with real ones, see lab5/authors.json).
#
# Results go to results/facilitator-<ts>/ (kept, gitignored). Afterwards
# sample-results/ holds: export.jsonl (the facilitator pair's board lines),
# traces/ (the most and the least wasteful transcript from labs 1-2),
# lab5-judge/ and lab5-human-scores.csv, and a README that says REAL, with the
# date. Read the transcripts before you commit them: they contain full file
# contents of the lab repo (nothing else of yours, as runs are isolated).
#
# Environment: PAIR (default facilitator), LITE, OPUS=1, MODEL, HAIKU_MODEL,
#   MAX_TURNS, MAX_BUDGET_USD, ENGINE, CLAUDE_BIN, KEEP_SYNTHETIC=1 (keep
#   sample-results/ untouched; just run the labs)
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//'; }
parse_common_args "$@"
export PAIR="${PAIR:-facilitator}"
export RESULTS_ROOT="${FACILITATOR_RESULTS:-$LAB_DIR/results/facilitator-$(timestamp)}"
flags=(--yes)
[[ $DRY_RUN -eq 1 ]] && flags=(--dry-run)

say "Facilitator run: labs 1, 2, 5 and 6 as pair '$PAIR' into $RESULTS_ROOT"
plan_line "labs 1-2 (sonnet)" sonnet $(( LITE == 1 ? 4 : 10 ))
plan_line "lab 6 (haiku)" haiku $(( LITE == 1 ? 2 : 6 ))
plan_line "lab 6 sonnet top-ups (about)" sonnet 2
plan_line "lab 5 judge calls" judge 8
if [[ $DRY_RUN -eq 0 && $ASSUME_YES -eq 0 ]]; then
  [[ -t 0 ]] || die "not a terminal; re-run with --yes"
  read -r -p "This calls Claude ~20 times and uses your plan. Proceed? [y/N] " answer
  [[ "$answer" == y || "$answer" == Y || "$answer" == yes ]] || die "cancelled"
fi

[[ $DRY_RUN -eq 1 ]] || "$LAB_DIR/predict.sh" "${PREDICTION:-lean}" >/dev/null
"$LAB_DIR/lab1.sh" "${flags[@]}"
"$LAB_DIR/lab2.sh" "${flags[@]}"
"$LAB_DIR/lab5.sh" "${flags[@]}"
"$LAB_DIR/lab6.sh" "${flags[@]}"
if [[ $DRY_RUN -eq 1 ]]; then
  say "then: rebuild sample-results/ from $RESULTS_ROOT (export.jsonl, traces/, lab5-judge/, README.md)"
  exit 0
fi
if [[ "${KEEP_SYNTHETIC:-0}" == 1 ]]; then
  say "KEEP_SYNTHETIC=1: sample-results/ left as it is. Real results: $RESULTS_ROOT"
  exit 0
fi

python3 - "$RESULTS_ROOT" "$SAMPLE_DIR" "$LAB_DIR" <<'PY'
import json, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
root, sample, lab = (Path(p) for p in sys.argv[1:])
sys.path.insert(0, str(lab / "lib"))
import labkit, traces

lines = []
for path in labkit.export_files(root):
    lines += labkit.read_export(path)
if not any(l.get("kind") is None for l in lines):
    sys.exit("no runs recorded; sample-results/ left unchanged")
(sample / "export.jsonl").write_text("".join(labkit.compact(l) + "\n" for l in lines), encoding="utf-8")

transcripts = sorted(p for lab_name in ("lab1", "lab2") for p in (root / lab_name).glob("*/runs/**/transcript.jsonl")
                     if p.stat().st_size)
reports = [traces.analyse(p) for p in transcripts]
reports = [r for r in reports if r["api_calls"]]
tdir = sample / "traces"
shutil.rmtree(tdir, ignore_errors=True)
tdir.mkdir()
if reports:
    reports.sort(key=lambda r: sum(w["cost"] for w in r["waste"]))
    picks = [reports[-1]] + ([reports[0]] if len(reports) > 1 else [])
    for r in picks:
        name = f"facilitator-{r['variant'] or 'run'}-{r['task'] or 'task'}.jsonl"
        shutil.copy(r["path"], tdir / name)
jdir = sample / "lab5-judge"
shutil.rmtree(jdir, ignore_errors=True)
runs5 = sorted((root / "lab5").glob("*/judge"))
if runs5:
    shutil.copytree(runs5[-1], jdir, ignore=shutil.ignore_patterns("*.raw.json"))
import os
scores = Path(os.environ.get("SCORES") or lab / "lab5" / "my-scores.csv")
if scores.is_file():
    shutil.copy(scores, sample / "lab5-human-scores.csv")
stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
(sample / "SOURCE").write_text(f"REAL: facilitator run {stamp}, pair {lines[0].get('pair')}, from {root.name}\n")
readme = sample / "README.md"
text = readme.read_text(encoding="utf-8") if readme.is_file() else "# Sample results\n"
marker = "<!-- source -->"
note = (f"{marker}\n**Current contents: REAL data from a facilitator run on {stamp}** "
        f"(pair `{lines[0].get('pair')}`, {sum(1 for l in lines if l.get('kind') is None)} runs). "
        "The synthetic generator is kept for reference; rerun it to go back to the synthetic set.\n")
text = text.split(marker)[0].rstrip() + "\n\n" + note
readme.write_text(text, encoding="utf-8")
print(f"sample-results/ now holds real data: {len(lines)} lines, {len(list(tdir.glob('*.jsonl')))} traces")
PY
say "Review sample-results/ (git diff) before committing it."
