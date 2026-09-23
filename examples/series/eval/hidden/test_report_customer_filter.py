import io
import unittest
from contextlib import redirect_stdout

from invoicing.cli import main
from invoicing.fixtures import load_invoices
from invoicing.report import summarise


def cli(*argv):
    out = io.StringIO()
    with redirect_stdout(out):
        code = main(list(argv))
    return code, out.getvalue()


class Hidden(unittest.TestCase):
    def test_summarise_filter(self):
        rows = load_invoices("data/invoices.csv")
        entries = summarise(rows, customer="muller")
        self.assertEqual([e["customer"] for e in entries], ["Müller GmbH"])
        self.assertEqual(entries[0]["invoices"], 2)

    def test_cli_filter_accents_and_case(self):
        code, out = cli("report", "data/invoices.csv", "--customer", "CAPEK")
        self.assertEqual(code, 0)
        self.assertIn("Capek Consulting", out)
        self.assertIn("Čapek & syn", out)
        self.assertNotIn("Acme", out)
        self.assertNotIn("Total EUR", out)

    def test_combines_with_currency(self):
        code, out = cli("report", "data/invoices.csv", "--customer", "capek", "--currency", "usd")
        self.assertEqual(code, 0)
        self.assertIn("Capek Consulting", out)
        self.assertNotIn("Čapek", out)
