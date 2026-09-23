# 005 · Read the legacy export (UTF-8 with BOM)

**Requested by:** operations · **Size:** small

`python3 -m invoicing report data/legacy-export.csv` fails with
`error: missing column(s): invoice_id`. The old accounting tool writes a UTF-8
byte order mark, so the first header cell is read as `\ufeffinvoice_id`.

## Acceptance criteria

- `load_invoices()` reads files with and without a BOM.
- The first row of `data/legacy-export.csv` loads with `invoice_id == "L-2031"`.
- Files without a BOM behave exactly as before.
- A test covers a BOM file; `python3 -m unittest` passes.

## Notes

Likely files: `invoicing/fixtures.py`, `tests/test_fixtures.py`. The dotted
dates in that file are a separate issue (006).
