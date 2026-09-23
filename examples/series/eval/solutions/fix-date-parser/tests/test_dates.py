import unittest
from datetime import date

from invoicing.dates import due_date, end_of_month, is_overdue, parse_date


class ParseTests(unittest.TestCase):
    def test_iso(self):
        self.assertEqual(parse_date("2026-09-24"), date(2026, 9, 24))

    def test_dotted_unambiguous(self):
        self.assertEqual(parse_date("31.12.2026"), date(2026, 12, 31))

    def test_rejects_other_formats(self):
        for bad in ("2026/09/24", "24 Sep 2026", ""):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_date(bad)


class TermsTests(unittest.TestCase):
    def test_net_days(self):
        self.assertEqual(due_date("2026-09-01", "net 30"), date(2026, 10, 1))
        self.assertEqual(due_date("2026-07-31", "Net  45"), date(2026, 9, 14))

    def test_end_of_month_handles_leap_years(self):
        self.assertEqual(end_of_month(date(2028, 2, 3)), date(2028, 2, 29))
        self.assertEqual(due_date("2026-08-20", "end of month"), date(2026, 8, 31))

    def test_on_receipt(self):
        self.assertEqual(due_date("2026-09-03", "on receipt"), date(2026, 9, 3))

    def test_unknown_terms(self):
        with self.assertRaises(ValueError):
            due_date("2026-09-03", "whenever")

    def test_overdue(self):
        self.assertTrue(is_overdue("2026-09-01", "net 14", date(2026, 9, 24)))
        self.assertFalse(is_overdue("2026-09-20", "net 30", date(2026, 9, 24)))


class DayFirstTests(unittest.TestCase):
    def test_dotted_is_day_first(self):
        self.assertEqual(parse_date("05.09.2026"), date(2026, 9, 5))

    def test_month_first_rejected(self):
        with self.assertRaises(ValueError):
            parse_date("12.31.2026")


if __name__ == "__main__":
    unittest.main()
