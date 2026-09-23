#!/usr/bin/env python3
"""Accept or reject one talk 03 attempt.

Usage: python3 check.py WORKDIR

Accepted means both: the hidden acceptance tests pass against the attempt's
export.py/invoice.py, and the attempt's own tests (python3 -m unittest) pass.
Prints one JSON line and exits 0 when accepted, 1 when not.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HIDDEN = Path(__file__).resolve().parent / "hidden" / "test_acceptance.py"


def run_unittest(cwd, *args):
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    proc = subprocess.run([sys.executable, "-m", "unittest", *args], cwd=cwd, env=env,
                          capture_output=True, text=True, timeout=120)
    summary = re.search(r"Ran (\d+) tests?", proc.stderr)
    failed = re.search(r"FAILED \(([^)]*)\)", proc.stderr)
    return {
        "ok": proc.returncode == 0,
        "ran": int(summary.group(1)) if summary else 0,
        "failures": failed.group(1) if failed else "",
        "tail": proc.stderr.strip().splitlines()[-12:],
    }


def check(workdir: Path) -> dict:
    result = {"workdir": str(workdir), "has_export": (workdir / "export.py").is_file()}
    if not result["has_export"]:
        result.update(accepted=False, reason="export.py missing")
        return result
    with tempfile.TemporaryDirectory() as scratch:
        for source in workdir.glob("*.py"):
            if not source.name.startswith("test_"):
                shutil.copy2(source, scratch)
        shutil.copy2(HIDDEN, scratch)
        hidden = run_unittest(scratch, "test_acceptance")
    own = run_unittest(workdir)
    result.update(hidden=hidden, own_tests=own)
    result["accepted"] = hidden["ok"] and own["ok"]
    if not result["accepted"]:
        result["reason"] = "hidden acceptance tests failed" if not hidden["ok"] else "own tests failed"
    return result


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    result = check(Path(argv[1]).resolve())
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
