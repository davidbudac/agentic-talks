# 004 · Dotted dates are always day-first

**Requested by:** operations · **Size:** small

`InvoiceDates.parse("05.09.2026")` returns 9 May instead of 5 September. The
old exports are European and always day-first; the month-first fallback in
`InvoiceDates.parse` was a guess and is wrong.

## Acceptance criteria

- `InvoiceDates.parse("05.09.2026")` is 5 September 2026 and
  `parse("1.2.2027")` is 1 February 2027.
- `parse("31.12.2026")` and ISO dates such as `2026-09-24` still work.
- `parse("12.31.2026")` throws `IllegalArgumentException` (there is no month 31).
- Due dates computed from a dotted issue date follow: `05.09.2026` with net 30
  is due on 5 October 2026.
- Tests cover it; `./mvnw -q test` passes.

## Notes

Likely files: `InvoiceDates.java`, `InvoiceDatesTest.java`.
