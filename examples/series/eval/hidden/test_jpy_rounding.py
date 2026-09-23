import unittest
from decimal import Decimal

from invoicing.invoice import gross
from invoicing.money import allocate, format_money, round_money


class Hidden(unittest.TestCase):
    def test_round_to_whole_yen(self):
        self.assertEqual(round_money("1234.5", "JPY"), Decimal("1235"))
        self.assertEqual(round_money("1234.4", "jpy"), Decimal("1234"))

    def test_format_has_no_decimals(self):
        self.assertEqual(format_money("1234.5", "JPY"), "1,235 JPY")

    def test_allocate(self):
        self.assertEqual(allocate("100", 3, "JPY"), [Decimal(34), Decimal(33), Decimal(33)])

    def test_gross(self):
        self.assertEqual(gross("1000", "0.10", "JPY"), Decimal("1100"))

    def test_other_currencies_unchanged(self):
        self.assertEqual(round_money("0.605", "EUR"), Decimal("0.61"))
        self.assertEqual(format_money("48000", "CZK"), "48,000.00 CZK")
