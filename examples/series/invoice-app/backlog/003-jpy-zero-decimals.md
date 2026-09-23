# 003 · Support JPY, which has no minor unit

**Requested by:** sales (new customer in Osaka) · **Size:** small

`round_money("1234.5", "JPY")` raises `MoneyError: unknown currency`. Yen has
no minor unit, so amounts round to whole yen.

## Acceptance criteria

- `round_money("1234.5", "JPY") == Decimal("1235")` (still ROUND_HALF_UP).
- `format_money("1234.5", "JPY") == "1,235 JPY"` (no decimal point).
- `allocate("100", 3, "JPY")` returns `[34, 33, 33]` as Decimals.
- `gross("1000", "0.10", "JPY") == Decimal("1100")`.
- Tests cover it; `python3 -m unittest` passes.

## Notes

Likely files: `invoicing/money.py`, `tests/test_money.py`.
