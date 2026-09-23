# invoice-app

## Rules
- Standard library only. Do not install packages or add dependencies.
- Money is `Decimal`, never float. Round once, at the end, with `money.round_money` (ROUND_HALF_UP to the currency's minor unit).
- Tax rates are supplied by the caller. Do not add a tax table.
- Never mix currencies in one total.
- Do not edit files in `data/`; they are fixtures other tests depend on.
- The export contract in `invoicing/export.py` is agreed with finance: change columns only when an issue asks for it.

## Commands
- Tests: `python3 -m unittest` from the repository root (must pass before you finish).
- One module: `python3 -m unittest tests.test_money`
- Try it: `python3 -m invoicing report data/invoices.csv`

## Conventions
- Tests live in `tests/test_<module>.py`; add or update one for every behaviour change.
- British spelling in identifiers that already use it (`normalise_name`, `summarise`); do not rename them in passing.
- Keep changes small and scoped to the issue; mention anything you noticed but did not fix.
