import csv
import io
import unittest

from invoicing.export import export_invoices

ROWS = [
    dict(invoice_id="A-1", customer="North, Ltd", net="100.00", tax_rate="0.21", currency="eur"),
    dict(invoice_id="A-2", customer="Line\nbreak", net="0.50", tax_rate="0.21", currency="CZK"),
    dict(invoice_id="A-3", customer="No currency", net="10", tax_rate="0"),
]


def parse(text):
    return list(csv.reader(io.StringIO(text, newline="")))


class Hidden(unittest.TestCase):
    def test_header(self):
        self.assertEqual(parse(export_invoices([])),
                         [["invoice_id", "customer", "net", "tax_rate", "gross", "currency"]])

    def test_values(self):
        out = parse(export_invoices(ROWS))[1:]
        self.assertEqual([r[5] for r in out], ["EUR", "CZK", "EUR"])
        self.assertEqual([r[4] for r in out], ["121.00", "0.61", "10.00"])
        self.assertEqual([r[0] for r in out], ["A-1", "A-2", "A-3"])
        self.assertEqual(out[1][1], "Line\nbreak")
