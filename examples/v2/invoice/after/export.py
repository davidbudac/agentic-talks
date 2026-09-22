"""Small reference export for talk 03. No filesystem or network side effects."""
import csv
import io
from invoice import gross


def export_invoices(rows):
    """Return a CSV string with a header, including when rows is empty."""
    output = io.StringIO(newline='')
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['invoice_id', 'customer', 'net', 'tax_rate', 'gross'])
    for row in rows:
        writer.writerow([
            row['invoice_id'], row['customer'], row['net'], row['tax_rate'],
            format(gross(row['net'], row['tax_rate']), '.2f'),
        ])
    return output.getvalue()
