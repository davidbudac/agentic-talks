# 001 · Add a currency column to the CSV export

**Requested by:** finance · **Size:** small

Finance imports the export into a spreadsheet that holds EUR, CZK, GBP and USD
invoices side by side. Without a currency the gross column is ambiguous.

## Acceptance criteria

- `CsvExport.export(invoices)` writes a sixth column, `currency`, after `gross`.
- The value is the invoice's currency code in upper case; an invoice created
  without a currency exports `EUR`.
- The header is still written for empty input (now six columns).
- Everything else in the export contract stays: input order, quoting of commas,
  quotes and line breaks, and the gross rule.
- Tests cover the new column; `./mvnw -q test` passes.

## Notes

Likely files: `CsvExport.java`, `CsvExportTest.java`. `CliTest` checks the
start of the `export` output too.
