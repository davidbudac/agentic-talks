import unittest

from invoicing.fixtures import FixtureError, load_invoices, load_invoices_text

from .helpers import INVOICES_CSV

HEADER = "invoice_id,customer,net,tax_rate\n"


class LoadTests(unittest.TestCase):
    def test_reference_file(self):
        rows = load_invoices(INVOICES_CSV)
        self.assertEqual(len(rows), 12)
        self.assertEqual(rows[0]["customer"], "North, Ltd")
        self.assertEqual(rows[2]["customer"], "Line\nbreak")
        self.assertEqual({row["currency"] for row in rows}, {"EUR", "CZK", "GBP", "USD"})

    def test_defaults_for_optional_columns(self):
        rows = load_invoices_text(HEADER + "A-1,Acme,10.00,0.2\n")
        self.assertEqual(rows[0]["currency"], "EUR")
        self.assertEqual(rows[0]["terms"], "net 30")


class ValidationTests(unittest.TestCase):
    def test_missing_column(self):
        with self.assertRaises(FixtureError):
            load_invoices_text("invoice_id,customer,net\nA-1,Acme,10\n")

    def test_duplicate_id(self):
        with self.assertRaisesRegex(FixtureError, "duplicate"):
            load_invoices_text(HEADER + "A-1,Acme,1,0\nA-1,Acme,2,0\n")

    def test_bad_amount_reports_line(self):
        with self.assertRaisesRegex(FixtureError, "line 2"):
            load_invoices_text(HEADER + "A-1,Acme,ten,0\n")


if __name__ == "__main__":
    unittest.main()
