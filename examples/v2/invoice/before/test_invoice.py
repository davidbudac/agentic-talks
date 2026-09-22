import unittest
from decimal import Decimal
from invoice import gross


class InvoiceTests(unittest.TestCase):
    def test_supplied_rate(self):
        self.assertEqual(gross('100', '0.21'), Decimal('121.00'))

    def test_zero_rate(self):
        self.assertEqual(gross('100', '0'), Decimal('100.00'))

    def test_round_once_half_up(self):
        self.assertEqual(gross('0.50', '0.21'), Decimal('0.61'))


if __name__ == '__main__':
    unittest.main()
