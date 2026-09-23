"""Hidden acceptance tests for the talk 03 trial. The agent never sees this file.

They encode the acceptance contract from examples/v2/invoice/README.md: keep the
calculation rule, output the five named columns, quote commas/quotes/newlines,
preserve input order and emit a header for empty input. No side effects.
"""
import csv
import io
import os
import tempfile
import unittest

from export import export_invoices

HEADER = ["invoice_id", "customer", "net", "tax_rate", "gross"]
ROWS = [
    dict(invoice_id="INV-001", customer="North, Ltd", net="100.00", tax_rate="0.21"),
    dict(invoice_id="INV-002", customer='Studio "A"', net="0.50", tax_rate="0.21"),
    dict(invoice_id="INV-003", customer="Line\nbreak", net="100.00", tax_rate="0"),
]


def parse(text):
    return list(csv.reader(io.StringIO(text, newline="")))


class AcceptanceTests(unittest.TestCase):
    def test_returns_text(self):
        self.assertIsInstance(export_invoices(ROWS), str)

    def test_header_is_the_five_named_columns(self):
        self.assertEqual(parse(export_invoices(ROWS))[0], HEADER)

    def test_empty_input_still_has_header(self):
        self.assertEqual(parse(export_invoices([])), [HEADER])

    def test_quoting_round_trips(self):
        out = parse(export_invoices(ROWS))[1:]
        self.assertEqual([r[1] for r in out], ["North, Ltd", 'Studio "A"', "Line\nbreak"])

    def test_order_is_preserved(self):
        reversed_rows = list(reversed(ROWS))
        out = parse(export_invoices(reversed_rows))[1:]
        self.assertEqual([r[0] for r in out], ["INV-003", "INV-002", "INV-001"])

    def test_calculation_rule_and_format(self):
        out = parse(export_invoices(ROWS))[1:]
        self.assertEqual([r[4] for r in out], ["121.00", "0.61", "100.00"])

    def test_rounds_once_half_up(self):
        rows = [dict(invoice_id="X-1", customer="Half", net="2.50", tax_rate="0.21")]
        self.assertEqual(parse(export_invoices(rows))[1][4], "3.03")

    def test_inputs_are_echoed(self):
        out = parse(export_invoices(ROWS))[1]
        self.assertEqual(out[:4], ["INV-001", "North, Ltd", "100.00", "0.21"])

    def test_no_files_written(self):
        before = os.getcwd()
        with tempfile.TemporaryDirectory() as scratch:
            os.chdir(scratch)
            try:
                export_invoices(ROWS)
                self.assertEqual(os.listdir(scratch), [])
            finally:
                os.chdir(before)


if __name__ == "__main__":
    unittest.main()
