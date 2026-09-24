#!/usr/bin/env bash
# Lab 3 · break the grader (40 min, no model calls).
#
#   ./lab3.sh            set up lab3-work/ (first time) and show the steps
#   ./lab3.sh check      run the weak checker and YOUR checker against four
#                        implementations: yours, the reference and two cheats
#   ./lab3.sh answer     the same, plus the answer-key checker (for the debrief)
#   ./lab3.sh reset      delete lab3-work/ and start again
#   --dry-run            print what would run; --yes is accepted and ignored
#
# The task is export-currency-column. lab3-work/repo/ is your copy of the app:
# write a WRONG implementation there that the weak checker still passes.
# lab3-work/checker/ starts as a copy of the weak checker (checker.conf and
# tests/*.java): strengthen it (run the own suite, add hidden JUnit tests, add a
# property check) until your wrong one and both cheats fail while the reference
# passes. Every check writes results/lab3/<ts>/matrix.md.
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'; }
parse_common_args "$@"
action="${REST_ARGS[0]:-setup}"
say "Lab 3 · break the grader: no model calls (0 sessions, 0 tokens, \$0). Each check runs Maven offline, ~5-10 s."
WORK="${LAB3_WORK:-$LAB_DIR/lab3-work}"
TASK=export-currency-column

setup() {
  if [[ -d "$WORK/repo" ]]; then
    say "lab3-work/ already exists (./lab3.sh reset to start again)."
  elif [[ $DRY_RUN -eq 1 ]]; then
    say "+ lib/setup-repo.sh $WORK/repo --claude-md none"
    say "+ cp -R lab3/weak $WORK/checker"
  else
    mkdir -p "$WORK"
    "$LIB_DIR/setup-repo.sh" "$WORK/repo" --claude-md none >/dev/null
    cp -R "$LAB_DIR/lab3/weak" "$WORK/checker"
    say "Created lab3-work/repo (your copy of invoice-app) and lab3-work/checker (a copy of the weak checker)."
  fi
  cat <<'TXT'

Steps (see lab3/README.md):
  1. Read lab3/weak/: what does it actually check?
  2. Partner A: in lab3-work/repo, make CsvExport pass the weak checker while being WRONG
     (the task: a sixth column "currency" after gross, upper case, EUR by default).
  3. ./lab3.sh check       -> your wrong one should pass "weak"
  4. Partner B: strengthen lab3-work/checker/ (checker.conf, tests/*.java) until
     "mine" fails your wrong one and both cheats, and passes the reference.
  5. Swap roles: B cheats against A's checker. Repeat ./lab3.sh check.
  6. Debrief: ./lab3.sh answer
TXT
}

impl_dir() {  # impl_dir NAME -> prints a scratch copy of that implementation
  local name="$1" dir="$SCRATCH/$1"
  mkdir -p "$dir"
  case "$name" in
    yours) (cd "$WORK/repo" && tar --exclude ./target --exclude ./.git -cf - .) | (cd "$dir" && tar -xf -) ;;
    reference) (cd "$APP_DIR" && tar --exclude ./target -cf - .) | (cd "$dir" && tar -xf -); cp -R "$EVAL_DIR/solutions/$TASK/." "$dir/" ;;
    *) (cd "$APP_DIR" && tar --exclude ./target -cf - .) | (cd "$dir" && tar -xf -); cp -R "$LAB_DIR/lab3/cheats/$name/." "$dir/" ;;
  esac
  printf '%s' "$dir"
}

check() {
  local with_answer="$1"
  [[ -d "$WORK/repo" ]] || { setup; [[ $DRY_RUN -eq 1 ]] && return 0; }
  local checkers=("weak:$LAB_DIR/lab3/weak" "mine:$WORK/checker")
  [[ "$with_answer" == 1 ]] && checkers+=("answer-key:$LAB_DIR/lab3/answer-key")
  local impls=(yours reference cheat-1-header-only cheat-2-hardcoded-eur)
  if [[ $DRY_RUN -eq 1 ]]; then
    for impl in "${impls[@]}"; do for c in "${checkers[@]}"; do say "+ lab3/checker.sh ${c#*:} <$impl>"; done; done
    return 0
  fi
  results_dir lab3
  SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/lab3.XXXXXX")"
  trap 'rm -rf "$SCRATCH"' EXIT
  local header="| Implementation |" rule="|---|" rows=() impl c dir out verdict note
  for c in "${checkers[@]}"; do header="$header ${c%%:*} |"; rule="$rule---|"; done
  say "Running $(( ${#impls[@]} * ${#checkers[@]} )) checks (about 5-10 s each)..."
  for impl in "${impls[@]}"; do
    dir="$(impl_dir "$impl")"
    local row="| $impl |"
    for c in "${checkers[@]}"; do
      if out="$("$LAB_DIR/lab3/checker.sh" "${c#*:}" "$dir")"; then verdict=PASS; else verdict=fail; fi
      note="$(printf '%s' "$out" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("notes","")[:60])
except Exception: print("")')"
      row="$row $verdict ($note) |"
      printf '%s\n' "$out" > "$RESULTS_DIR/${impl}--${c%%:*}.json"
    done
    rows+=("$row")
    say "  $row"
  done
  {
    echo "# Lab 3 · checker matrix"
    echo
    echo "$header"
    echo "$rule"
    printf '%s\n' "${rows[@]}"
    echo
    echo "Goal: 'weak' passes everything (that is the problem). 'mine' should pass only the reference."
    echo "A checker that fails the reference is wrong too: it would reject a correct agent."
  } > "$RESULTS_DIR/matrix.md"
  say ""
  cat "$RESULTS_DIR/matrix.md"
  cp -R "$WORK/checker" "$RESULTS_DIR/your-checker"
}

case "$action" in
  setup) setup ;;
  check) check 0 ;;
  answer) check 1 ;;
  reset) if [[ $DRY_RUN -eq 1 ]]; then say "+ rm -rf $WORK"; else rm -rf "$WORK"; say "Removed lab3-work/."; fi ;;
  *) usage >&2; exit 2 ;;
esac
