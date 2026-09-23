#!/usr/bin/env bash
# Record a terminal session for a fallback slide.
#
#   run/record.sh SLIDE [--dry-run] [-- COMMAND ...]
#   run/record.sh --list
#
# SLIDE is one of the fallback slots below. Uses asciinema when installed
# (.cast), otherwise macOS/BSD `script -r` (.typescript, converted to .cast with
# lib/typescript2cast.py). Recordings go to examples/series/results/recordings/.
# With no COMMAND it runs the slide's suggested command, or opens an
# interactive shell in a fresh invoice-app copy for demos you drive by hand.
# Recording itself never calls Claude; what you run inside it might.
#
# Turn a recording into a video for the slide:
#   agg rec.cast rec.gif --font-size 20 --theme monokai      # brew install agg
#   ffmpeg -i rec.gif -movflags faststart -pix_fmt yuv420p \
#          -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" rec.mp4
#   asciinema play rec.cast                                     # replay in a terminal
#   script -p rec.typescript                                    # replay without asciinema
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
usage() { sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; list_slots; }

list_slots() {
  cat <<'EOF'

Slots (talk-slide: what to capture · how):
  05-s25  Cost & Context · rehearsal of the bloated-vs-lean run · runs run/talk05.sh (spends usage)
  06-s9   Orchestrating · Symphony ticket -> PR run · manual: Symphony + Codex + Linear are outside this kit;
          opens a shell, start Symphony there. Screen-record the Linear board too (Cmd+Shift+5).
  06-s23  Orchestrating · write a skill, then watch it fire · opens a shell in a fresh repo copy with
          demo-skill/backlog-issue/SKILL.md ready to paste into .claude/skills/; run `claude`, ask "do 003".
  07-s18  Measuring · the recorded eval run · runs a small run/talk07.sh (3 tasks x 2 runs, spends usage)
  07-s28  Measuring · a local Gemma 4 / Qwen 3.6 run · manual: opens a shell; e.g. `ollama run gemma4:12b`
          on a task from backlog/ (the kit does not install Ollama or models).
  07-s33  Measuring · /voice dictation · terminal text only; audio and the hold/tap UI need a screen
          recording (Cmd+Shift+5 with the microphone on). Opens `claude` in a fresh repo copy.
  08-s18  Claude Design · the five-frame live build · NOT a terminal: Claude Design is a web app.
          Screen-record the browser (Cmd+Shift+5) or take five screenshots; this script only prints that.
EOF
}

parse_common_args "$@"
set -- "${REST_ARGS[@]+"${REST_ARGS[@]}"}"
[[ "${1:-}" == --list ]] && { list_slots; exit 0; }
SLOT="${1:-}"
[[ -n "$SLOT" ]] || { usage; exit 2; }
shift
user_cmd=()
if [[ "${1:-}" == -- ]]; then shift; user_cmd=("$@"); fi

setup_demo_repo() {
  setup_repo "record-$SLOT" lean
  [[ $DRY_RUN -eq 0 ]] && KEEP_WORKDIRS=1   # the recording may reference it; remove by hand afterwards
  return 0
}

case "$SLOT" in
  05-s25)
    confirm_plan "Record 05-s25: runs run/talk05.sh inside the recording (2 model sessions, see its estimate)"
    default_cmd=("$RUN_DIR/talk05.sh" --yes) ;;
  07-s18)
    confirm_plan "Record 07-s18: runs a small run/talk07.sh inside the recording (3 tasks x 2 variants x 2 runs = 12 sessions)"
    default_cmd=(env "TASKS=fix-date-parser fixtures-bom jpy-rounding" RUNS=2 "$RUN_DIR/talk07.sh" --yes) ;;
  06-s9|07-s28)
    setup_demo_repo
    default_cmd=(bash -c "cd $(printf '%q' "$REPO") && exec \${SHELL:-bash} -i") ;;
  06-s23)
    setup_demo_repo
    mkdir -p "$REPO/../skill-to-paste"
    cp "$SERIES_DIR/demo-skill/backlog-issue/SKILL.md" "$REPO/../skill-to-paste/SKILL.md"
    say "Skill to paste: $REPO/../skill-to-paste/SKILL.md → $REPO/.claude/skills/backlog-issue/SKILL.md"
    default_cmd=(bash -c "cd $(printf '%q' "$REPO") && exec \${SHELL:-bash} -i") ;;
  07-s33)
    setup_demo_repo
    default_cmd=(bash -c "cd $(printf '%q' "$REPO") && exec $(printf '%q' "$CLAUDE_BIN")") ;;
  08-s18)
    say "08-s18 (Claude Design) needs a browser screen recording, not a terminal one:"
    say "  1. Open Claude Design, paste the brief from slide 16, run the five steps from slide 17."
    say "  2. Cmd+Shift+5 → Record Selected Portion, or take one screenshot per step (5 frames)."
    say "  3. Replace the five drawn stand-ins on claude-design.html slide 18."
    exit 0 ;;
  *) die "unknown slot $SLOT (run/record.sh --list)" ;;
esac
[[ ${#user_cmd[@]} -gt 0 ]] && default_cmd=("${user_cmd[@]}")

out_dir="$RESULTS_ROOT/recordings"
stamp="$(timestamp)"
if command -v asciinema >/dev/null 2>&1; then
  file="$out_dir/$SLOT-$stamp.cast"
  rec=(asciinema rec --overwrite -c "$(printf '%q ' "${default_cmd[@]}")" "$file")
else
  file="$out_dir/$SLOT-$stamp.typescript"
  rec=(script -q -r "$file" "${default_cmd[@]}")
fi
say "Recording $SLOT → $file"
say "+ $(printf '%q ' "${rec[@]}")"
if [[ $DRY_RUN -eq 1 ]]; then
  exit 0
fi
mkdir -p "$out_dir"
"${rec[@]}" || warn "recorded command exited non-zero"
if [[ "$file" == *.typescript ]]; then
  cols="$(tput cols 2>/dev/null || echo 120)"; rows="$(tput lines 2>/dev/null || echo 34)"
  python3 "$RUN_DIR/lib/typescript2cast.py" "$file" "${file%.typescript}.cast" --cols "$cols" --rows "$rows"
fi
say "Next: agg ${file%.*}.cast ${file%.*}.gif && ffmpeg -i ${file%.*}.gif -movflags faststart -pix_fmt yuv420p -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' ${file%.*}.mp4"
