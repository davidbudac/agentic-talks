# 006 · Rename Invoice.customer to customerName

**Requested by:** the team (tidy-up) · **Size:** small

`Report.Entry` calls the field `customerName`; the `Invoice` record calls it
`customer`. Make `Invoice` consistent.

## Acceptance criteria

- The `Invoice` record component `customer` is renamed to `customerName`; the
  component order is unchanged.
- No alias: there is no `customer()` accessor left on `Invoice`.
- Every caller in `src/main/java` and `src/test/java` uses `customerName()`.
- Behaviour does not change. In particular the CSV export header still says
  `customer`: the column name is part of the contract with finance.
- `./mvnw -q test` passes.

## Notes

A mechanical rename. Callers include `CsvExport`, `Report` and several tests.
