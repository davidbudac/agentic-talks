import unittest
from datetime import date

from invoicing.dates import due_date, parse_date


class Hidden(unittest.TestCase):
    def test_day_first(self):
        self.assertEqual(parse_date("05.09.2026"), date(2026, 9, 5))
        self.assertEqual(parse_date("1.2.2027"), date(2027, 2, 1))

    def test_still_parses_unambiguous_and_iso(self):
        self.assertEqual(parse_date("31.12.2026"), date(2026, 12, 31))
        self.assertEqual(parse_date("2026-09-24"), date(2026, 9, 24))

    def test_month_first_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_date("12.31.2026")

    def test_due_date_from_dotted(self):
        self.assertEqual(due_date("05.09.2026", "net 30"), date(2026, 10, 5))
