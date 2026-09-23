import pathlib
import unittest
from decimal import Decimal

import invoicing.invoice as invoice


class Hidden(unittest.TestCase):
    def test_new_name_works(self):
        row = {"net": "99.99", "tax_rate": "0.0825", "currency": "USD"}
        self.assertEqual(invoice.gross_for_row(row), Decimal("108.24"))

    def test_old_name_is_gone_everywhere(self):
        self.assertFalse(hasattr(invoice, "row_gross"))
        hits = [str(p) for folder in ("invoicing", "tests", "tools")
                for p in pathlib.Path(folder).rglob("*.py")
                if "row_gross" in p.read_text(encoding="utf-8")]
        self.assertEqual(hits, [])
