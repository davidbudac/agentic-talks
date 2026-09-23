import os
import tempfile
import unittest

from invoicing.fixtures import load_invoices


class Hidden(unittest.TestCase):
    def test_legacy_file(self):
        rows = load_invoices("data/legacy-export.csv")
        self.assertEqual(rows[0]["invoice_id"], "L-2031")
        self.assertEqual(len(rows), 3)

    def test_bom_and_plain_files(self):
        text = "invoice_id,customer,net,tax_rate\nB-1,Müller GmbH,1.00,0.19\n"
        with tempfile.TemporaryDirectory() as scratch:
            for encoding in ("utf-8-sig", "utf-8"):
                path = os.path.join(scratch, f"{encoding}.csv")
                with open(path, "w", encoding=encoding, newline="") as handle:
                    handle.write(text)
                rows = load_invoices(path)
                self.assertEqual(rows[0]["invoice_id"], "B-1")
                self.assertEqual(rows[0]["customer"], "Müller GmbH")
