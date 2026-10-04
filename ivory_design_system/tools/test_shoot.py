"""Exercise launcher failures without starting Chrome or triggering crash dialogs."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SHOOT = Path(__file__).with_name("shoot.sh")
FAKE_CHROME = '''#!/usr/bin/env python3
import os, pathlib, sys
log = pathlib.Path(os.environ["CALL_LOG"])
with log.open("a") as f:
    f.write(" ".join(sys.argv[1:]) + "\\n")
calls = len(log.read_text().splitlines())
if calls == int(os.environ.get("FAIL_AT", "0")):
    sys.exit(134)
if "--dump-dom" in sys.argv:
    print('<section data-deck-slide="1"></section><section data-deck-slide="2"></section><section data-deck-slide="3"></section>')
elif os.environ.get("NO_OUTPUT") != "1":
    for arg in sys.argv[1:]:
        if arg.startswith(("--screenshot=", "--print-to-pdf=")):
            pathlib.Path(arg.split("=", 1)[1]).write_bytes(b"test artifact")
'''


class ShootTests(unittest.TestCase):
    def run_shoot(self, *, explicit=False, pdf=False, **env):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chrome = root / "chrome"
            chrome.write_text(FAKE_CHROME)
            chrome.chmod(0o700)
            deck = root / "deck.html"
            deck.write_text("<section></section>" * 3)
            log = root / "calls"
            args = ["bash", str(SHOOT)]
            if pdf:
                args += ["--pdf"]
            args += [str(deck), str(root / "output")]
            if explicit:
                args += ["1", "3"]
            result = subprocess.run(args, env={**os.environ, "CHROME": str(chrome),
                "CALL_LOG": str(log), **env}, capture_output=True, text=True)
            return result, log.read_text().splitlines()

    def test_count_crash_stops_before_screenshots(self):
        result, calls = self.run_shoot(FAIL_AT="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(calls), 1)

    def test_screenshot_crash_stops_remaining_slides(self):
        result, calls = self.run_shoot(explicit=True, FAIL_AT="2")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(calls), 2)

    def test_missing_image_stops_remaining_slides(self):
        result, calls = self.run_shoot(explicit=True, NO_OUTPUT="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(calls), 1)

    def test_success_captures_every_slide(self):
        result, calls = self.run_shoot()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(calls), 4)

    def test_pdf_crash_reports_failure(self):
        result, calls = self.run_shoot(pdf=True, FAIL_AT="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
