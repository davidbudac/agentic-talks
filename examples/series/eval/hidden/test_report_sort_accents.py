import unittest

from invoicing.customers import sort_key
from invoicing.fixtures import load_invoices
from invoicing.report import build_report, summarise


class Hidden(unittest.TestCase):
    def test_entries_sorted_accent_insensitively(self):
        entries = summarise(load_invoices("data/invoices.csv"))
        names = [e["customer"] for e in entries]
        self.assertEqual(names, sorted(names, key=sort_key))
        self.assertLess(names.index("Čapek & syn s.r.o."), names.index("Zeta Analytics"))
        self.assertLess(names.index("Élodie Durand"), names.index("Müller GmbH"))

    def test_same_customer_two_currencies_sorted_by_currency(self):
        rows = [
            dict(invoice_id="1", customer="Acme", net="1", tax_rate="0", currency="USD"),
            dict(invoice_id="2", customer="Acme", net="1", tax_rate="0", currency="EUR"),
            dict(invoice_id="3", customer="Ábel", net="1", tax_rate="0", currency="EUR"),
        ]
        order = [(e["customer"], e["currency"]) for e in summarise(rows)]
        self.assertEqual(order, [("Ábel", "EUR"), ("Acme", "EUR"), ("Acme", "USD")])

    def test_table_order(self):
        text = build_report(load_invoices("data/invoices.csv"))
        self.assertLess(text.index("Élodie"), text.index("Zeta"))
