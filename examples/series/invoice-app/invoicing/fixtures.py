"""Load invoice rows from CSV fixtures.

A fixture row is a plain dict with string values, the same shape the export
and report modules take. Required columns: invoice_id, customer, net and
tax_rate. Optional columns: currency (default EUR), issue_date and terms.
"""
import csv
import io
from pathlib import Path

from .money import DEFAULT_CURRENCY, MoneyError, normalise_currency, to_decimal

REQUIRED_COLUMNS = ("invoice_id", "customer", "net", "tax_rate")
OPTIONAL_COLUMNS = {"currency": DEFAULT_CURRENCY, "issue_date": "", "terms": "net 30"}


class FixtureError(ValueError):
    """A fixture file that cannot be used, with the line number if known."""


def parse_invoices(handle) -> list:
    """Parse CSV text from an open file or any iterable of lines."""
    reader = csv.DictReader(handle)
    header = reader.fieldnames or []
    missing = [column for column in REQUIRED_COLUMNS if column not in header]
    if missing:
        raise FixtureError(f"missing column(s): {', '.join(missing)}")
    rows, seen = [], set()
    for row in reader:
        line = reader.line_num
        record = {key: (value if value is not None else "") for key, value in row.items() if key}
        for column, default in OPTIONAL_COLUMNS.items():
            if not record.get(column):
                record[column] = default
        invoice_id = record["invoice_id"].strip()
        if not invoice_id:
            raise FixtureError(f"line {line}: empty invoice_id")
        if invoice_id in seen:
            raise FixtureError(f"line {line}: duplicate invoice_id {invoice_id}")
        seen.add(invoice_id)
        try:
            to_decimal(record["net"])
            to_decimal(record["tax_rate"])
            record["currency"] = normalise_currency(record["currency"])
        except MoneyError as exc:
            raise FixtureError(f"line {line}: {exc}") from exc
        record["invoice_id"] = invoice_id
        rows.append(record)
    return rows


def load_invoices(path) -> list:
    """Load a fixture file from disk."""
    with open(Path(path), newline="", encoding="utf-8") as handle:
        return parse_invoices(handle)


def load_invoices_text(text: str) -> list:
    """Convenience for tests: parse fixture rows from a string."""
    return parse_invoices(io.StringIO(text, newline=""))
