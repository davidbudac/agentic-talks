#!/usr/bin/env python3
"""Summarise a Maven Surefire run as one smevals Checker JSON object.

    surefire_summary.py REPORTS_DIR MVN_EXIT MVN_LOG [--hidden-prefix Hidden] [--min-own N]
                        [--expect-hidden N] [--metrics metrics.json] [--out check.json]

Reads target/surefire-reports/TEST-*.xml. Test classes whose simple name starts
with the hidden prefix count as hidden acceptance tests; the rest are the
repository's own tests. Pass means: Maven exited 0, at least one hidden test
ran (and exactly --expect-hidden if given), none failed, and the own tests ran
at least --min-own times without failures (so deleting tests does not help).

Prints the JSON object ({score, metrics, notes, details}) and exits 0 on pass,
1 on fail. Standard library only.
"""
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SESSION_METRICS = ("cost_usd", "num_turns", "duration_s", "input_tokens", "output_tokens",
                   "cache_read_tokens", "cache_creation_tokens", "total_tokens")


def read_reports(directory: Path):
    suites = []
    for path in sorted(directory.glob("TEST-*.xml")):
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError:
            continue
        name = root.get("name", path.stem[5:])
        failed = []
        for case in root.iter("testcase"):
            problem = case.find("failure")
            if problem is None:
                problem = case.find("error")
            if problem is not None:
                message = (problem.get("message") or problem.text or "").strip().splitlines()
                failed.append(f"{case.get('classname', name).rsplit('.', 1)[-1]}.{case.get('name')}: "
                              f"{message[0][:200] if message else problem.tag}")
        suites.append({
            "class": name.rsplit(".", 1)[-1],
            "tests": int(root.get("tests", 0)),
            "failed": int(root.get("failures", 0)) + int(root.get("errors", 0)),
            "skipped": int(root.get("skipped", 0)),
            "failures": failed,
        })
    return suites


def compile_errors(log_text: str):
    lines = [line for line in log_text.splitlines() if "[ERROR]" in line and ".java" in line]
    return [re.sub(r"^.*?/src/", "src/", line.replace("[ERROR] ", ""))[:220] for line in lines[:8]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", type=Path)
    parser.add_argument("mvn_exit", type=int)
    parser.add_argument("mvn_log", type=Path)
    parser.add_argument("--hidden-prefix", default="Hidden")
    parser.add_argument("--hidden-classes", default="",
                        help="comma-separated simple class names that count as hidden (overrides the prefix)")
    parser.add_argument("--min-own", type=int, default=0)
    parser.add_argument("--expect-hidden", type=int, default=None)
    parser.add_argument("--label", default="hidden", help="what to call the hidden tests in notes")
    parser.add_argument("--metrics", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    suites = read_reports(args.reports) if args.reports.is_dir() else []
    log_text = args.mvn_log.read_text(encoding="utf-8", errors="replace") if args.mvn_log.is_file() else ""
    named = {c.strip() for c in args.hidden_classes.split(",") if c.strip()}
    is_hidden = (lambda s: s["class"] in named) if named else (lambda s: s["class"].startswith(args.hidden_prefix))
    hidden = [s for s in suites if is_hidden(s)]
    own = [s for s in suites if not is_hidden(s)]
    h_tests = sum(s["tests"] for s in hidden)
    h_failed = sum(s["failed"] for s in hidden)
    o_tests = sum(s["tests"] for s in own)
    o_failed = sum(s["failed"] for s in own)
    errors = compile_errors(log_text) if not suites else []

    hidden_ok = h_tests > 0 and h_failed == 0 and (args.expect_hidden is None or h_tests == args.expect_hidden)
    own_ok = o_failed == 0 and o_tests >= args.min_own
    passed = args.mvn_exit == 0 and hidden_ok and own_ok
    if passed:
        notes = f"pass: {h_tests} {args.label} and {o_tests} own tests"
    elif errors or ("COMPILATION ERROR" in log_text and not suites):
        notes = "build failed: " + (errors[0] if errors else "compilation error")
    elif not suites:
        tail = [line for line in log_text.splitlines() if line.strip()][-1:] or ["no test reports"]
        notes = "no tests ran: " + tail[0][:200]
    elif not hidden_ok:
        notes = (f"{args.label} tests: {h_failed} of {h_tests} failed" if h_tests else f"{args.label} tests did not run")
        if args.expect_hidden is not None and h_tests not in (0, args.expect_hidden):
            notes += f" (expected {args.expect_hidden} to run)"
    elif o_tests < args.min_own:
        notes = f"own tests: only {o_tests} ran, expected at least {args.min_own} (were tests removed?)"
    else:
        notes = f"own tests: {o_failed} of {o_tests} failed"

    result = {
        "score": 1.0 if passed else 0.0,
        "metrics": {"hidden_ok": hidden_ok, "own_tests_ok": own_ok, "hidden_tests": h_tests,
                    "hidden_failed": h_failed, "own_tests": o_tests, "own_failed": o_failed,
                    "mvn_exit": args.mvn_exit},
        "notes": notes,
        "details": {"failures": [f for s in suites for f in s["failures"]][:12],
                    "compile_errors": errors},
    }
    if args.metrics and args.metrics.is_file():
        try:
            session = json.loads(args.metrics.read_text(encoding="utf-8"))
        except ValueError:
            session = {}
        for key in SESSION_METRICS:
            if isinstance(session.get(key), (int, float)):
                result["metrics"][key] = session[key]
    text = json.dumps(result, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
