#!/usr/bin/env bash
# Make a fresh, disposable copy of invoice-app with its own git history.
#
#   lib/setup-repo.sh DEST [--claude-md lean|bloated|none]
#
# Copies workshops/evals/lab/invoice-app to DEST (which must not exist or be
# empty), leaving out build output, installs the chosen CLAUDE.md variant from
# claude-md/ as DEST/CLAUDE.md, then runs `git init` and commits a baseline.
# The repository in this project never contains a nested .git.
set -euo pipefail
lab="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
app="$lab/invoice-app"
usage() { sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; }

dest="" variant="lean"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --claude-md) variant="${2:?--claude-md needs lean, bloated or none}"; shift 2 ;;
    --claude-md=*) variant="${1#*=}"; shift ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
    *) dest="$1"; shift ;;
  esac
done
[[ -n "$dest" ]] || { usage >&2; exit 2; }
case "$variant" in lean|bloated|none) ;; *) echo "unknown CLAUDE.md variant: $variant" >&2; exit 2 ;; esac
if [[ -e "$dest" && -n "$(find "$dest" -mindepth 1 -maxdepth 1 2>/dev/null | head -1)" ]]; then
  echo "refusing to overwrite non-empty $dest" >&2
  exit 1
fi
mkdir -p "$dest"
(cd "$app" && tar --exclude ./target --exclude ./.git -cf - .) | (cd "$dest" && tar -xf -)
if [[ "$variant" != none ]]; then
  cp "$lab/claude-md/$variant.md" "$dest/CLAUDE.md"
fi
printf 'target/\n' > "$dest/.gitignore"
git -C "$dest" init -q -b main
git -C "$dest" config user.name "Lab Kit"
git -C "$dest" config user.email "lab-kit@example.invalid"
git -C "$dest" config commit.gpgsign false
git -C "$dest" add -A
git -C "$dest" commit -q -m "Baseline for the lab run (CLAUDE.md: $variant)"
echo "$dest"
