import csv
import io
import unittest
from export import export_invoices


class ExportTests(unittest.TestCase):
    def test_roundtrip_special_characters_and_totals(self):
        rows = [
            dict(invoice_id='INV-001', customer='North, Ltd', net='100.00', tax_rate='0.21'),
            dict(invoice_id='INV-002', customer='Studio "A"', net='0.50', tax_rate='0.21'),
            dict(invoice_id='INV-003', customer='Line\nbreak', net='100.00', tax_rate='0'),
        ]
        result = list(csv.DictReader(io.StringIO(export_invoices(rows))))
        self.assertEqual([r['customer'] for r in result], [r['customer'] for r in rows])
        self.assertEqual([r['gross'] for r in result], ['121.00', '0.61', '100.00'])
        self.assertEqual([r['invoice_id'] for r in result], ['INV-001', 'INV-002', 'INV-003'])

    def test_empty_input_still_has_header(self):
        result = list(csv.reader(io.StringIO(export_invoices([]))))
        self.assertEqual(result, [['invoice_id', 'customer', 'net', 'tax_rate', 'gross']])


if __name__ == '__main__':
    unittest.main()
