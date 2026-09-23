import csv
import io
import unittest

from invoicing.export import export_invoices

ROWS = [
    dict(invoice_id="A-1", customer="North, Ltd", net="100.00", tax_rate="0.21",
         issue_date="2026-09-01", terms="net 30"),
    dict(invoice_id="A-2", customer="Eom", net="0.50", tax_rate="0.21",
         issue_date="2026-08-20", terms="end of month"),
    dict(invoice_id="A-3", customer="Undated", net="10", tax_rate="0"),
]


def parse(text):
    return list(csv.reader(io.StringIO(text, newline="")))


class Hidden(unittest.TestCase):
    def test_header(self):
        self.assertEqual(parse(export_invoices([])),
                         [["invoice_id", "customer", "net", "tax_rate", "gross", "due_date"]])

    def test_values(self):
        out = parse(export_invoices(ROWS))[1:]
        self.assertEqual([r[5] for r in out], ["2026-10-01", "2026-08-31", ""])
        self.assertEqual([r[4] for r in out], ["121.00", "0.61", "10.00"])
