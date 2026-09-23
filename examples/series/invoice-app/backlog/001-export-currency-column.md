# 001 · Add a currency column to the CSV export

**Requested by:** finance · **Size:** small

Finance imports the export into a spreadsheet that holds EUR, CZK, GBP and USD
invoices side by side. Without a currency the gross column is ambiguous.

## Acceptance criteria

- `export_invoices(rows)` writes a sixth column, `currency`, after `gross`.
- The value is the row's `currency`, upper-case; rows without one get `EUR`.
- The header is still written for empty input (now six columns).
- Everything else in the export contract stays: order, quoting, the gross rule.
- Tests cover the new column; `python3 -m unittest` passes.

## Notes

Likely files: `invoicing/export.py`, `tests/test_export.py`.
