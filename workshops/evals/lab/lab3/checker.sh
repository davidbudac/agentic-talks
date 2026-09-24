#!/usr/bin/env bash
# Run one lab 3 checker against one implementation.
#
#   lab3/checker.sh CHECKER_DIR REPO_DIR
#
# CHECKER_DIR holds checker.conf (TEST_FILTER, RUN_OWN_TESTS) and tests/*.java.
# The repo is copied to a scratch dir, the checker's tests are copied into
# src/test/java/com/example/invoicing/, mvnw/.mvn/pom.xml are replaced by the
# pristine ones, and `./mvnw -q -o test` runs. With RUN_OWN_TESTS=0 the repo's own
# tests are deleted from the scratch copy first, so only the checker's tests run.
# Pass = Maven exits 0 and at least one of the checker's tests ran.
# Prints one JSON line (smevals Checker format); exit 0 pass, 1 fail. No model calls.
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
lab="$(cd "$here/.." && pwd)"
checker="${1:?usage: checker.sh CHECKER_DIR REPO_DIR}"
repo="${2:?usage: checker.sh CHECKER_DIR REPO_DIR}"
[[ -f "$checker/checker.conf" ]] || { echo "no checker.conf in $checker" >&2; exit 2; }
TEST_FILTER=""
RUN_OWN_TESTS=1
# shellcheck disable=SC1091
source "$checker/checker.conf"

work="$(mktemp -d "${TMPDIR:-/tmp}/lab3-check.XXXXXX")"
trap 'rm -rf "$work"' EXIT
(cd "$repo" && tar --exclude ./target --exclude ./.git -cf - .) | (cd "$work" && tar -xf -)
rm -rf "$work/.mvn" "$work/target"
cp -R "$lab/invoice-app/.mvn" "$work/.mvn"
cp "$lab/invoice-app/mvnw" "$lab/invoice-app/pom.xml" "$work/"
dest="$work/src/test/java/com/example/invoicing"
[[ "$RUN_OWN_TESTS" == 1 ]] || rm -rf "$work/src/test/java"
mkdir -p "$dest"
classes=""
for f in "$checker"/tests/*.java; do
  [[ -f "$f" ]] || continue
  cp "$f" "$dest/"
  classes="$classes,$(basename "$f" .java)"
done
[[ -n "$classes" ]] || { echo '{"score": 0.0, "notes": "checker has no tests"}'; exit 1; }
mvn_args=(-q -o -B test -DskipTests=false -Dmaven.test.skip=false -Dsurefire.failIfNoSpecifiedTests=false)
[[ -n "$TEST_FILTER" ]] && mvn_args+=("-Dtest=$TEST_FILTER")
rc=0
(cd "$work" && ./mvnw "${mvn_args[@]}") > "$work/mvn.log" 2>&1 || rc=$?
python3 "$lab/lib/surefire_summary.py" "$work/target/surefire-reports" "$rc" "$work/mvn.log" \
  --hidden-classes "${classes#,}" --label checker
