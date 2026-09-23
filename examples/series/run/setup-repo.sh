#!/usr/bin/env bash
# Make a fresh, disposable copy of invoice-app with its own git history.
#
#   run/setup-repo.sh DEST [--claude-md lean|bloated|none]
#
# Copies examples/series/invoice-app to DEST (which must not exist or be empty),
# installs the chosen CLAUDE.md variant from examples/series/claude-md/ as
# DEST/CLAUDE.md, then runs `git init` and commits a baseline. The repository in
# this project never contains a nested .git; every run starts from a clean copy.
# Also handy for live demos: make two copies, one per CLAUDE.md, one per pane.
set -euo pipefail

SERIES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$SERIES_DIR/invoice-app"

usage() { sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; }

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
cp -R "$APP_DIR"/. "$dest"/
find "$dest" -name __pycache__ -type d -prune -exec rm -rf {} +
if [[ "$variant" != none ]]; then
  cp "$SERIES_DIR/claude-md/$variant.md" "$dest/CLAUDE.md"
fi

git -C "$dest" init -q -b main
git -C "$dest" config user.name "Demo Kit"
git -C "$dest" config user.email "demo-kit@example.invalid"
git -C "$dest" config commit.gpgsign false
git -C "$dest" add -A
git -C "$dest" commit -q -m "Baseline for the demo run (CLAUDE.md: $variant)"
echo "$dest"
