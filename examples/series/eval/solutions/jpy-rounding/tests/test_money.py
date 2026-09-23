import unittest
from decimal import Decimal

from invoicing.money import MoneyError, allocate, format_money, round_money, to_decimal


class ToDecimalTests(unittest.TestCase):
    def test_strings_ints_and_decimals(self):
        self.assertEqual(to_decimal(" 1_000.50 "), Decimal("1000.50"))
        self.assertEqual(to_decimal(7), Decimal(7))
        self.assertEqual(to_decimal(Decimal("0.1")), Decimal("0.1"))

    def test_rejects_floats_and_junk(self):
        for bad in (0.1, True, "", "abc", "NaN", "Infinity"):
            with self.subTest(bad=bad), self.assertRaises(MoneyError):
                to_decimal(bad)


class RoundingTests(unittest.TestCase):
    def test_half_up_to_cents(self):
        self.assertEqual(round_money("0.605"), Decimal("0.61"))
        self.assertEqual(round_money("0.604"), Decimal("0.60"))
        self.assertEqual(round_money("-0.605"), Decimal("-0.61"))

    def test_currency_code_is_case_insensitive(self):
        self.assertEqual(round_money("10", "czk"), Decimal("10.00"))

    def test_unknown_currency(self):
        with self.assertRaises(MoneyError):
            round_money("1", "XYZ")

    def test_format(self):
        self.assertEqual(format_money("1234.5", "EUR"), "1,234.50 EUR")
        self.assertEqual(format_money("48000", "CZK"), "48,000.00 CZK")


class AllocateTests(unittest.TestCase):
    def test_parts_add_up_exactly(self):
        parts = allocate("100.00", 3)
        self.assertEqual(parts, [Decimal("33.34"), Decimal("33.33"), Decimal("33.33")])
        self.assertEqual(sum(parts), Decimal("100.00"))

    def test_rejects_zero_parts(self):
        with self.assertRaises(MoneyError):
            allocate("1", 0)


class YenTests(unittest.TestCase):
    def test_whole_yen(self):
        self.assertEqual(round_money("1234.5", "JPY"), Decimal("1235"))
        self.assertEqual(format_money("1234.5", "JPY"), "1,235 JPY")
        self.assertEqual(allocate("100", 3, "JPY"), [Decimal(34), Decimal(33), Decimal(33)])


if __name__ == "__main__":
    unittest.main()
