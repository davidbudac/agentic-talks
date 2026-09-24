#!/usr/bin/env bash
# Block 0 · setup check (15 min). Run it at home a week before (see prework.md)
# and again at the venue. It never calls a model and costs nothing.
#
#   ./check-setup.sh              check everything, prefetch Maven and smevals
#   PAIR=team-name ./check-setup.sh   also save your pair name (same on both laptops)
#   ./check-setup.sh --no-fetch   skip the downloads (Maven dependencies, smevals)
#
# Checks: JDK 21+, the Maven wrapper (downloads Maven 3.9 once), a dependency
# prefetch with `./mvnw -q dependency:go-offline` followed by an OFFLINE test run
# (so venue Wi-Fi does not matter afterwards), python3 3.10+, uv/uvx and smevals,
# Claude Code (`claude --version`) and sign-in (`claude auth status`, which reads
# local credentials and does not call the model), and git.
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
app="$here/invoice-app"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
fetch=1
case "${1:-}" in
  --no-fetch) fetch=0 ;;
  -h|--help) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
esac
pass=0 fail=0 warnings=0
ok() { printf '  [PASS] %s\n' "$*"; pass=$((pass + 1)); }
bad() { printf '  [FAIL] %s\n' "$*"; fail=$((fail + 1)); }
note() { printf '  [WARN] %s\n' "$*"; warnings=$((warnings + 1)); }

echo "Setup check for the evals workshop lab ($(date '+%Y-%m-%d %H:%M'))"
echo

echo "Java and Maven"
if command -v java >/dev/null 2>&1; then
  jv="$(java -version 2>&1 | head -1)"
  major="$(printf '%s' "$jv" | sed -E 's/.*version "([0-9]+).*/\1/')"
  if [[ "$major" =~ ^[0-9]+$ && "$major" -ge 21 ]]; then ok "JDK $major ($jv)"; else bad "JDK 21+ needed, found: $jv"; fi
else
  bad "java not found: install a JDK 21+ (e.g. Temurin 21) and put it on PATH"
fi
if [[ -x "$app/mvnw" ]]; then
  if mv_out="$(cd "$app" && ./mvnw -q -v 2>&1 | head -1)"; then ok "Maven wrapper: $mv_out"; else bad "Maven wrapper failed: $mv_out"; fi
else
  bad "invoice-app/mvnw missing or not executable (chmod +x invoice-app/mvnw)"
fi
if [[ $fetch -eq 1 ]]; then
  if (cd "$app" && ./mvnw -q -B dependency:go-offline > /dev/null 2>&1); then ok "dependencies prefetched (./mvnw -q dependency:go-offline)"; else bad "dependency prefetch failed: run 'cd invoice-app && ./mvnw dependency:go-offline' to see why (proxy? ~/.m2/settings.xml?)"; fi
fi
tmp="$(mktemp -d "${TMPDIR:-/tmp}/lab-setup.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT
(cd "$app" && tar --exclude ./target -cf - .) | (cd "$tmp" && tar -xf -)
if (cd "$tmp" && ./mvnw -q -o -B test > "$tmp/test.log" 2>&1); then
  ok "offline build and tests pass (./mvnw -q -o test)"
else
  bad "offline test run failed (last lines below); run ./check-setup.sh while online"
  tail -5 "$tmp/test.log" | sed 's/^/         /'
fi

echo "Python and smevals"
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
  ok "python3 $(python3 -c 'import platform; print(platform.python_version())')"
else
  bad "python3 3.10+ needed (the lab scripts use it; standard library only)"
fi
if command -v uvx >/dev/null 2>&1; then
  ok "uv $(uv --version 2>/dev/null | awk '{print $2}')"
  if [[ $fetch -eq 1 ]]; then
    if sv="$(uvx --from smevals==0.2.0 smevals --version 2>&1 | tail -1)"; then ok "smevals via uvx: $sv"; else note "smevals did not start ($sv); the labs fall back to ENGINE=direct"; fi
  fi
else
  note "uv not found: install it (https://docs.astral.sh/uv/) for smevals; without it the labs use ENGINE=direct"
fi

echo "Claude Code"
if command -v "$CLAUDE_BIN" >/dev/null 2>&1; then
  ok "claude $("$CLAUDE_BIN" --version 2>/dev/null | head -1)"
  # `claude auth status` reads the stored login and prints JSON; exit 0 when signed in.
  # It makes no model request, so it costs nothing.
  if auth="$("$CLAUDE_BIN" auth status 2>/dev/null)"; then
    summary="$(printf '%s' "$auth" | python3 -c 'import json,sys
try:
    d = json.load(sys.stdin)
    print("%s, plan: %s" % (d.get("authMethod"), d.get("subscriptionType") or "n/a"))
except Exception:
    print("signed in")')"
    ok "signed in ($summary)"
    case "$summary" in *api*|*console*) note "signed in with an API key, not a Pro/Max login: runs are billed per token" ;; esac
  else
    bad "not signed in: run 'claude' once and log in with your Pro or Max account (or: claude auth login)"
  fi
else
  bad "claude not found: install Claude Code (https://code.claude.com/docs/en/setup) and sign in"
fi

echo "Git and pair"
if command -v git >/dev/null 2>&1; then ok "$(git --version)"; else bad "git not found"; fi
if [[ -n "${PAIR:-}" ]]; then
  printf '%s\n' "$PAIR" > "$here/.pair"
  ok "pair name saved to .pair: $PAIR (use the same name on your partner's laptop)"
elif [[ -f "$here/.pair" ]]; then
  ok "pair name: $(cat "$here/.pair")"
else
  note "no pair name yet: PAIR=your-team ./check-setup.sh (otherwise the board shows a hostname hash)"
fi

echo
echo "Result: $pass passed, $fail failed, $warnings warnings"
[[ $fail -eq 0 ]] && echo "You are ready. Nothing above called a model." || echo "Fix the FAIL lines, then run ./check-setup.sh again."
exit $(( fail > 0 ))
