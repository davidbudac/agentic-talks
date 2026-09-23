# 004 · Filter the report by customer

**Requested by:** account managers · **Size:** small

Account managers want one customer's totals without scrolling the whole table.

## Acceptance criteria

- `python3 -m invoicing report FILE --customer TEXT` shows only customers whose
  name contains TEXT, ignoring case and accents (`--customer muller` finds
  `Müller GmbH`).
- `summarise(rows, currency=None, customer=None)` accepts the same filter.
- It combines with `--currency`.
- The totals footer covers only the customers shown.
- Tests cover it; `python3 -m unittest` passes.

## Notes

`customers.matches()` already does the accent-insensitive comparison.
Likely files: `invoicing/report.py`, `invoicing/cli.py`, their tests.
