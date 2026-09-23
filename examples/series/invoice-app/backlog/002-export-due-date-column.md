# 002 · Add a due date column to the CSV export

**Requested by:** credit control · **Size:** small

Credit control chases late payers from the export. They currently work out
due dates by hand from the issue date and the terms.

## Acceptance criteria

- `export_invoices(rows)` writes a sixth column, `due_date`, after `gross`.
- The value is `dates.due_date(row["issue_date"], row["terms"])` in ISO format
  (`2026-10-01`); rows without an issue date get an empty cell.
- The header is still written for empty input (now six columns).
- Everything else in the export contract stays: order, quoting, the gross rule.
- Tests cover the new column; `python3 -m unittest` passes.

## Notes

Likely files: `invoicing/export.py`, `tests/test_export.py`.
