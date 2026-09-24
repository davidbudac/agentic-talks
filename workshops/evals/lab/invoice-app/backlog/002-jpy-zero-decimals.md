# 002 · Support JPY, which has no minor unit

**Requested by:** sales (new customer in Osaka) · **Size:** small

`Money.round(new BigDecimal("1234.5"), "JPY")` throws
`MoneyException: unknown currency: 'JPY'`. Yen has no minor unit, so amounts
round to whole yen.

## Acceptance criteria

- `Money.round(1234.5, "JPY")` is `1235` and `Money.round(1234.4, "jpy")` is
  `1234`, still `HALF_UP`, with scale 0.
- `Money.format(1234.5, "JPY")` is `"1,235 JPY"` (no decimal point).
- `Money.allocate(100, 3, "JPY")` returns `34, 33, 33` as whole-yen amounts.
- `Invoices.gross(1000, 0.10, "JPY")` is `1100`, and an `Invoice` in `jpy`
  computes the same gross.
- EUR, USD, GBP and CZK behave exactly as before (`48,000.00 CZK`).
- Tests cover it; `./mvnw -q test` passes.

## Notes

Likely files: `Money.java`, `MoneyTest.java`. Check every place that assumes
two decimals, not only the exponent table.
