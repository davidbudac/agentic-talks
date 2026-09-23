#!/usr/bin/env bash
# Talk 03, slide 22: measure the model + tool cost per ACCEPTED task.
#
# The same task (add the CSV export to the talk 03 start state: invoice.py with
# the fixed gross(), no export yet) runs RUNS times under two setups. After each
# run, hidden acceptance tests (talk03/hidden/, never shown to the agent) and
# the attempt's own tests decide "accepted". Reports accepted runs, cost,
# cost per accepted task, turns and time per setup.
#
# Usage: run/talk03.sh [--dry-run] [--yes]
#
# Environment:
#   VARIANT=models    (default) MODEL_A vs MODEL_B, both with the acceptance contract
#   VARIANT=contract  one MODEL, prompt without (A) vs with (B) the contract
#   MODEL_A=claude-haiku-4-5  MODEL_B=claude-sonnet-5  MODEL=claude-sonnet-5
#   RUNS=5            attempts per setup (the slide's illustration uses 10)
#   plus MAX_TURNS, MAX_BUDGET_USD, CLAUDE_BIN, RESULTS_ROOT, ISOLATE (see lib/common.sh)
set -euo pipefail
MAX_TURNS="${MAX_TURNS:-15}"
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; }
parse_common_args "$@"

VARIANT="${VARIANT:-models}"
RUNS="${RUNS:-5}"
T03="$SERIES_DIR/talk03"
CONTRACT_PROMPT="$(cat "$T03/prompts/contract.txt")"
BARE_PROMPT="$(cat "$T03/prompts/bare.txt")"

case "$VARIANT" in
  models)
    MODEL_A="${MODEL_A:-claude-haiku-4-5}"; MODEL_B="${MODEL_B:-claude-sonnet-5}"
    LABEL_A="$MODEL_A + contract"; LABEL_B="$MODEL_B + contract"
    PROMPT_A="$CONTRACT_PROMPT"; PROMPT_B="$CONTRACT_PROMPT"; PKEY_A=contract; PKEY_B=contract ;;
  contract)
    MODEL_A="$MODEL"; MODEL_B="$MODEL"
    LABEL_A="$MODEL, no contract"; LABEL_B="$MODEL + contract"
    PROMPT_A="$BARE_PROMPT"; PROMPT_B="$CONTRACT_PROMPT"; PKEY_A=bare; PKEY_B=contract ;;
  *) die "VARIANT must be models or contract" ;;
esac

require_claude
results_dir talk03
read -r lo_a hi_a cap_a <<< "$(estimate_line "$MODEL_A" "$RUNS")"
read -r lo_b hi_b cap_b <<< "$(estimate_line "$MODEL_B" "$RUNS")"
confirm_plan \
  "Talk 03 · cost per accepted task (slide 22)" \
  "Setup A: $LABEL_A · Setup B: $LABEL_B · $RUNS runs each, interleaved ($((RUNS * 2)) sessions)" \
  "Task: add export_invoices() to talk03/start; accepted = hidden tests + own tests pass" \
  "Estimated cost: A \$$lo_a-\$$hi_a, B \$$lo_b-\$$hi_b (hard cap \$$(python3 -c "print(f'{$cap_a+$cap_b:.2f}')"))" \
  "Estimated time: $((RUNS * 2))-$((RUNS * 2 * 3)) minutes, sequential"

if [[ $DRY_RUN -eq 0 ]]; then
  python3 - "$RESULTS_DIR/plan.json" "$VARIANT" "$RUNS" "$MAX_TURNS" \
    "$LABEL_A" "$MODEL_A" "$PKEY_A" "$LABEL_B" "$MODEL_B" "$PKEY_B" <<'PY'
import json, sys
path, variant, runs, turns, la, ma, pa, lb, mb, pb = sys.argv[1:]
json.dump({"variant": variant, "runs": int(runs), "max_turns": int(turns),
           "setups": {"A": {"label": la, "model": ma, "prompt": pa},
                      "B": {"label": lb, "model": mb, "prompt": pb}}},
          open(path, "w"), indent=2)
PY
fi

prepare_start() {
  new_workdir "talk03-$1"
  REPO="$WORKDIR/repo"
  mkdir -p "$REPO"
  cp "$T03/start/"*.py "$REPO/"
  git -C "$REPO" init -q -b main
  git -C "$REPO" -c user.name="Demo Kit" -c user.email=demo-kit@example.invalid add -A
  git -C "$REPO" -c user.name="Demo Kit" -c user.email=demo-kit@example.invalid -c commit.gpgsign=false commit -q -m baseline
}

for i in $(seq 1 "$RUNS"); do
  for setup in A B; do
    if [[ $setup == A ]]; then model="$MODEL_A"; prompt="$PROMPT_A"; else model="$MODEL_B"; prompt="$PROMPT_B"; fi
    out="$RESULTS_DIR/runs/$setup-$i"
    say "── run $i/$RUNS · setup $setup ($model)"
    prepare_start "$setup-$i"
    build_claude_cmd "$prompt" "$model"
    run_session "$REPO" "$out"
    if [[ $DRY_RUN -eq 0 ]]; then
      save_repo_state "$REPO" "$out"
      python3 "$T03/check.py" "$REPO" > "$out/check.json" || true
      python3 -c "import json,sys; r=json.load(open(sys.argv[1])); print('   accepted' if r['accepted'] else '   rejected: ' + r.get('reason',''))" "$out/check.json"
    else
      say "+ python3 $(printf '%q' "$T03/check.py") $(printf '%q' "$REPO") > $(printf '%q' "$out/check.json")"
    fi
  done
done

summarise_talk talk03
