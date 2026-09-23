# 006 · Dotted dates are always day-first

**Requested by:** operations · **Size:** small

`parse_date("05.09.2026")` returns 9 May instead of 5 September. The old
exports are European and always day-first; the month-first fallback in
`dates.parse_date` was a guess and is wrong.

## Acceptance criteria

- `parse_date("05.09.2026") == date(2026, 9, 5)`.
- `parse_date("31.12.2026")` still works.
- `parse_date("12.31.2026")` raises `ValueError` (month 31 does not exist).
- ISO dates behave exactly as before.
- Tests cover it; `python3 -m unittest` passes.

## Notes

Likely files: `invoicing/dates.py`, `tests/test_dates.py`.
