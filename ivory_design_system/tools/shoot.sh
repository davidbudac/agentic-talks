#!/usr/bin/env bash
# Ivory · screenshot a <deck-stage> deck, one 1920×1080 PNG per slide.
#
#   tools/shoot.sh <deck.html> <out-dir> [first] [last]
#   tools/shoot.sh --pdf <deck.html> <out.pdf>
#
# Writes <out-dir>/NN.png (two digits, 1-based slide number). Without [last]
# the slide count is read from the rendered deck. Without [first] it starts at 1.
#
# Environment:
#   CHROME      Chrome/Chromium binary (default: the macOS Google Chrome path,
#               then google-chrome / chromium on PATH)
#   QUERY       extra query parameters, e.g. QUERY=chrome (notes panel open)
#               or QUERY=pw (presenter window rendered in the page)
#   OFFLINE=1   block all network access (host resolver maps every host to nothing)
#   BUDGET      virtual time budget in ms per shot (default 6000)
#   CHROME_LOG  file to append Chrome's stderr (console messages) to;
#               default: stderr is discarded
#
# Recipe (do not change without re-checking the reference shots):
#   --headless=new, 1920×1080 window, ?_snthumb=1 (deck-stage hides its
#   thumbnail rail), #N selects the slide, a virtual time budget so fonts and
#   videos settle, and NO --disable-gpu: the software path renders the
#   full-range ivory videos as pure white.
set -euo pipefail

die() { echo "shoot.sh: $*" >&2; exit 1; }

usage() {
  sed -n '2,6p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}

pdf=0
if [ "${1:-}" = "--pdf" ]; then pdf=1; shift; fi
[ $# -ge 2 ] || usage

deck=$1; out=$2; first=${3:-1}; last=${4:-}

# ── find Chrome ──────────────────────────────────────────────────────────
if [ -z "${CHROME:-}" ]; then
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "$(command -v google-chrome 2>/dev/null || true)" \
           "$(command -v chromium 2>/dev/null || true)" \
           "$(command -v chromium-browser 2>/dev/null || true)"; do
    if [ -n "$c" ] && [ -x "$c" ]; then CHROME=$c; break; fi
  done
fi
[ -n "${CHROME:-}" ] && [ -x "$CHROME" ] || die "Chrome not found. Install Google Chrome or set CHROME=/path/to/chrome"

# ── deck → file URL ──────────────────────────────────────────────────────
[ -f "$deck" ] || die "deck not found: $deck"
abs="$(cd "$(dirname "$deck")" && pwd)/$(basename "$deck")"
url="file://$(printf '%s' "$abs" | sed -e 's/%/%25/g' -e 's/ /%20/g' -e 's/#/%23/g' -e 's/?/%3F/g')"
query="_snthumb=1${QUERY:+&$QUERY}"

flags=(--headless=new --hide-scrollbars --window-size=1920,1080 "--virtual-time-budget=${BUDGET:-6000}")
[ "${OFFLINE:-0}" = "1" ] && flags+=("--host-resolver-rules=MAP * ~NOTFOUND")
log=/dev/null
if [ -n "${CHROME_LOG:-}" ]; then flags+=(--enable-logging=stderr --v=0); log=$CHROME_LOG; fi

# ── PDF mode ─────────────────────────────────────────────────────────────
if [ "$pdf" = "1" ]; then
  mkdir -p "$(dirname "$out")"
  rm -f "$out"
  "$CHROME" "${flags[@]}" --no-pdf-header-footer "--print-to-pdf=$out" "$url?$query" >/dev/null 2>>"$log" || true
  [ -s "$out" ] || die "Chrome produced no PDF ($out)"
  echo "$out"
  exit 0
fi

# ── slide count ──────────────────────────────────────────────────────────
if [ -z "$last" ]; then
  last=$("$CHROME" "${flags[@]}" --dump-dom "$url?$query" 2>>"$log" \
         | grep -o 'data-deck-slide="[0-9]*"' | sort -u | wc -l | tr -d ' ') || true
  if [ -z "$last" ] || [ "$last" -eq 0 ]; then
    last=$(grep -o '<section[ >]' "$deck" | wc -l | tr -d ' ') || true
  fi
  [ "$last" -gt 0 ] || die "no slides found in $deck"
fi
case "$first$last" in *[!0-9]*) die "first/last must be numbers";; esac
[ "$first" -le "$last" ] || die "first ($first) is after last ($last)"

# ── shoot ────────────────────────────────────────────────────────────────
mkdir -p "$out"
fail=0
for ((n = first; n <= last; n++)); do
  png=$(printf '%s/%02d.png' "$out" "$n")
  rm -f "$png"
  "$CHROME" "${flags[@]}" "--screenshot=$png" "$url?$query#$n" >/dev/null 2>>"$log" || true
  if [ -s "$png" ]; then echo "$png"; else echo "shoot.sh: no screenshot for slide $n" >&2; fail=1; fi
done
exit $fail
