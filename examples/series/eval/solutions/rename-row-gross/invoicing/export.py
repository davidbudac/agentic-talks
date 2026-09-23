"""CSV export: the feature talk 03 builds against an acceptance contract.

Contract: keep the calculation rule, output the five named columns, quote
commas, quotes and newlines, preserve input order and emit a header for empty
input. No filesystem or network side effects: the caller decides where the
text goes.
"""
import csv
import io

from .invoice import gross_for_row

EXPORT_COLUMNS = ["invoice_id", "customer", "net", "tax_rate", "gross"]


def export_invoices(rows) -> str:
    """Return a CSV string with a header, including when rows is empty."""
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(EXPORT_COLUMNS)
    for row in rows:
        writer.writerow([
            row["invoice_id"], row["customer"], row["net"], row["tax_rate"],
            str(gross_for_row(row)),
        ])
    return output.getvalue()
