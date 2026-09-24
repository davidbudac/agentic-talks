# 003 · Read the legacy export (UTF-8 with BOM)

**Requested by:** operations · **Size:** small

`java -cp target/classes com.example.invoicing.Cli report data/legacy-export.csv`
fails with `error: missing column(s): invoice_id`. The old accounting tool
writes a UTF-8 byte order mark, so the first header cell is read as
`﻿invoice_id`.

## Acceptance criteria

- `FixtureLoader.load(path)` reads files with and without a BOM.
- `data/legacy-export.csv` loads three invoices; the first has id `L-2031`
  and the second is in CZK.
- A file without a BOM gives exactly the same invoices as the same file with one.
- A test covers a BOM file; `./mvnw -q test` passes.

## Notes

Likely files: `CsvReader.java` or `FixtureLoader.java`, and
`FixtureLoaderTest.java`. The dotted dates in that file are a separate issue
(004); do not fix them here.
