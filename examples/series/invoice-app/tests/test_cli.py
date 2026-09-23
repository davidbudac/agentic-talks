import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from invoicing.cli import main

from .helpers import DATA, INVOICES_CSV


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    def test_report(self):
        code, out, _ = run("report", str(INVOICES_CSV))
        self.assertEqual(code, 0)
        self.assertIn("Acme Corp", out)

    def test_report_currency(self):
        code, out, _ = run("report", str(INVOICES_CSV), "--currency", "GBP")
        self.assertEqual(code, 0)
        self.assertIn("Zeta Analytics", out)
        self.assertNotIn("Acme Corp", out)

    def test_export(self):
        code, out, _ = run("export", str(INVOICES_CSV))
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("invoice_id,customer,net,tax_rate,gross"))

    def test_due_marks_overdue(self):
        code, out, _ = run("due", str(INVOICES_CSV), "--today", "2026-09-24")
        self.assertEqual(code, 0)
        self.assertIn("INV-002  2026-09-16  OVERDUE", out)

    def test_missing_file_is_an_error(self):
        code, _, err = run("report", str(DATA / "nope.csv"))
        self.assertEqual(code, 2)
        self.assertIn("error:", err)


if __name__ == "__main__":
    unittest.main()
