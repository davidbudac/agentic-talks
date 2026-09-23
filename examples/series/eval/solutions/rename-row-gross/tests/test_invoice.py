import unittest
from decimal import Decimal

from invoicing.invoice import gross, invoice_totals, gross_for_row
from invoicing.money import MoneyError


class GrossTests(unittest.TestCase):
    """The three tests from the talk 02 fixture, unchanged in meaning."""

    def test_supplied_rate(self):
        self.assertEqual(gross("100", "0.21"), Decimal("121.00"))

    def test_zero_rate(self):
        self.assertEqual(gross("100", "0"), Decimal("100.00"))

    def test_round_once_half_up(self):
        self.assertEqual(gross("0.50", "0.21"), Decimal("0.61"))

    def test_negative_rate_rejected(self):
        with self.assertRaises(MoneyError):
            gross("100", "-0.1")


class TotalsTests(unittest.TestCase):
    def test_multi_line_rounds_once(self):
        lines = [("3", "0.333"), ("1", "0.001")]
        totals = invoice_totals(lines, "0.21")
        self.assertEqual(totals["net"], Decimal("1.00"))
        self.assertEqual(totals["gross"], Decimal("1.21"))
        self.assertEqual(totals["tax"], Decimal("0.21"))
        self.assertEqual(totals["net"] + totals["tax"], totals["gross"])

    def test_gross_for_row_uses_row_currency(self):
        row = {"net": "99.99", "tax_rate": "0.0825", "currency": "USD"}
        self.assertEqual(gross_for_row(row), Decimal("108.24"))


if __name__ == "__main__":
    unittest.main()
