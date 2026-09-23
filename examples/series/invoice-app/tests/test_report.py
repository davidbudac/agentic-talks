import unittest
from decimal import Decimal

from invoicing.fixtures import load_invoices
from invoicing.report import build_report, grand_totals, summarise

from .helpers import INVOICES_CSV


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.rows = load_invoices(INVOICES_CSV)

    def test_decomposed_names_are_grouped(self):
        muller = [e for e in summarise(self.rows) if e["customer"] == "Müller GmbH"]
        self.assertEqual(len(muller), 1)
        self.assertEqual(muller[0]["invoices"], 2)
        self.assertEqual(muller[0]["gross"], Decimal("1975.52"))

    def test_currency_filter(self):
        entries = summarise(self.rows, currency="czk")
        self.assertEqual({e["currency"] for e in entries}, {"CZK"})
        self.assertEqual(len(entries), 2)

    def test_currencies_are_never_mixed(self):
        totals = grand_totals(summarise(self.rows))
        self.assertEqual(set(totals), {"CZK", "EUR", "GBP", "USD"})
        self.assertEqual(totals["USD"], Decimal("868.24"))


class RenderTests(unittest.TestCase):
    def test_table_has_header_rows_and_totals(self):
        text = build_report(load_invoices(INVOICES_CSV))
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("Customer"))
        self.assertIn("Line break", text)
        self.assertIn("Total EUR", text)
        self.assertIn("58,080.00 CZK", text)


if __name__ == "__main__":
    unittest.main()
