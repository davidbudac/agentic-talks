# invoice-app — Project Guide for AI Assistants

> Last big update: March 2026 (Tomas). Please keep this file up to date! Everyone
> should add anything they learn here so the agent knows it next time.

## Table of contents
1. Project history
2. Architecture overview
3. Directory layout
4. Module-by-module guide
5. Design philosophy
6. Rules
7. Commands
8. Conventions and style guide
9. Testing philosophy
10. Notes from past sessions
11. Glossary
12. FAQ

---

## 1. Project history

invoice-app started in 2024 as a single script, `invoice.py`, written for the
Agentic AI intro talk. It had one function, `gross()`, and a famous bug: it
ignored the tax rate. The fix (apply the rate, round once, half up) became the
demo for talk 02. In talk 03 we added `export.py` with an acceptance contract
agreed with finance. Over the summer of 2026 the script grew into a package:
money handling was split out of `invoice.py` into `money.py`, customer name
handling moved to `customers.py` after the Müller incident (see section 10),
dates were added for credit control, and the report and CLI came last. In
August we added a small MCP server in `tools/` so the invoicing commands could
be used from Claude Desktop. The package version is in `invoicing/__init__.py`.

We considered moving to a proper framework (Django was discussed, then
FastAPI), but decided against it because the project is a teaching fixture and
must run anywhere with only Python installed. We also considered using `pandas`
for the report, and `babel` for money formatting, and rejected both for the
same reason. Please do not re-open these discussions.

## 2. Architecture overview

The architecture follows a layered approach. At the bottom sits `money.py`,
which knows nothing about invoices: it parses amounts into `Decimal`, knows the
minor-unit exponent of each currency, and applies the single rounding rule. On
top of it, `invoice.py` implements the calculation: `gross()` takes a net amount
and a tax rate and returns the rounded gross, `line_net()` multiplies quantity by
unit price without rounding, and `invoice_totals()` sums lines exactly and
rounds once at the end so that net + tax = gross always reconciles.

Next to the calculation layer sit two independent helper modules.
`customers.py` handles Unicode customer names: normalising to NFC, collapsing
whitespace, stripping accents for comparison, sorting, matching and truncating
for display without splitting a letter from its accent. `dates.py` parses issue
dates (ISO and the dotted format from the old accounting tool) and computes due
dates from payment terms such as "net 30" and "end of month".

The input layer is `fixtures.py`, which reads CSV files into plain dicts with
string values and validates them: required columns, unique invoice ids, valid
amounts and known currencies. Rows are plain dicts on purpose, so that the
export and report can be tested with literal dicts and no loader.

The output layer has two modules. `export.py` writes the five-column CSV that
finance imports; it is pure and returns a string, the caller decides where it
goes. `report.py` aggregates rows into one entry per customer and currency and
renders a fixed-width text table with a total line per currency. Currencies are
never mixed.

Finally `cli.py` wires everything into `python3 -m invoicing` with three
subcommands, `report`, `export` and `due`, and `tools/invoice_mcp.py` exposes the
same three commands as MCP tools over stdio by calling `cli.main()` and
capturing its output.

Data flows strictly downwards: cli → fixtures → (export | report) → invoice →
money. Nothing imports cli. Nothing in the package does network I/O. The only
filesystem access is in `fixtures.load_invoices()`.

## 3. Directory layout

```
invoice-app/
├── README.md                 # overview and commands
├── .gitignore
├── backlog/                  # open issues as markdown files
│   ├── 001-export-currency-column.md
│   ├── 002-export-due-date-column.md
│   ├── 003-jpy-zero-decimals.md
│   ├── 004-report-customer-filter.md
│   ├── 005-legacy-export-bom.md
│   └── 006-dotted-dates-day-first.md
├── data/
│   ├── invoices.csv          # 12 invoices, 4 currencies, Unicode names
│   └── legacy-export.csv     # from the old accounting tool (BOM, dotted dates)
├── invoicing/
│   ├── __init__.py           # package docstring and version
│   ├── __main__.py           # python3 -m invoicing
│   ├── cli.py                # argparse front end
│   ├── customers.py          # Unicode customer names
│   ├── dates.py              # issue dates and payment terms
│   ├── export.py             # five-column CSV export
│   ├── fixtures.py           # CSV loading and validation
│   ├── invoice.py            # gross(), totals
│   ├── legacy_pdf.py         # PDF invoice rendering (old, being removed)
│   ├── money.py              # Decimal parsing and rounding
│   └── report.py             # text report
├── tests/
│   ├── __init__.py
│   ├── helpers.py
│   ├── test_cli.py
│   ├── test_customers.py
│   ├── test_dates.py
│   ├── test_export.py
│   ├── test_fixtures.py
│   ├── test_invoice.py
│   ├── test_legacy_pdf.py
│   ├── test_mcp_server.py
│   ├── test_money.py
│   └── test_report.py
└── tools/
    └── invoice_mcp.py        # MCP server (stdio)
```

## 4. Module-by-module guide

### money.py
- `to_decimal(value)` accepts Decimal, int and str. Floats raise `MoneyError`.
  Booleans also raise, because `True` is an int in Python.
- `normalise_currency(code)` upper-cases and checks against `CURRENCY_EXPONENTS`.
- `exponent(code)` returns the number of decimals, `quantum(code)` the smallest unit.
- `round_money(amount, code)` is THE rounding function. Use it everywhere.
- `format_money(amount, code)` gives `1,234.50 EUR`.
- `allocate(total, parts, code)` splits an amount so the parts add up exactly
  (largest remainder method). Used for instalment plans.

### invoice.py
- `gross(net, tax_rate, currency="EUR")` — the original function. Negative
  rates raise. Round once.
- `line_net(quantity, unit_price)` — no rounding.
- `invoice_totals(lines, tax_rate, currency)` — returns dict with net, tax,
  gross, currency. tax is computed as gross - net so it always reconciles.
- `row_gross(row)` — gross for a fixture row dict, using its currency.

### customers.py
- `normalise_name` — NFC + whitespace. Keeps case and accents.
- `strip_accents` — NFKD and drop combining marks.
- `sort_key` — accent- and case-insensitive, tie-break on the display name.
- `matches(name, query)` — substring, accent- and case-insensitive.
- `initials(name)` — first two words.
- `display_name(name, width)` — truncate with an ellipsis, grapheme-safe,
  newlines to spaces.

### dates.py
- `parse_date(text)` — ISO or dotted.
- `end_of_month(day)`, `due_date(issue, terms)`, `is_overdue(issue, terms, today)`.
- Terms: "net N", "end of month", "on receipt". Case and extra spaces are fine.

### fixtures.py
- `parse_invoices(handle)`, `load_invoices(path)`, `load_invoices_text(text)`.
- Required columns: invoice_id, customer, net, tax_rate. Optional: currency
  (EUR), issue_date (""), terms ("net 30").
- Raises `FixtureError` with the line number.

### export.py
- `export_invoices(rows) -> str`. Columns: invoice_id, customer, net, tax_rate,
  gross. Header always written. Order preserved. csv module does the quoting.

### report.py
- `summarise(rows, currency=None)`, `grand_totals(entries)`,
  `render_table(entries)`, `build_report(rows, currency=None)`.
- `NAME_WIDTH = 24`.

### cli.py
- `report FILE [--currency]`, `export FILE`, `due FILE [--today]`.
- Exit code 2 on errors, message on stderr prefixed with `error:`.

### legacy_pdf.py
- Renders a PDF invoice using hand-written PDF operators. Being removed in Q3;
  do not add features. Its tests are slow, skip them if needed.

## 5. Design philosophy

We value correctness over cleverness. An invoice that is off by one cent is a
support ticket, a credit note and an unhappy customer, so every amount is a
`Decimal` from the moment it is parsed. We prefer small pure functions that
take plain data and return plain data, because they are easy to test and easy
to explain in a talk. We avoid classes unless there is state to protect. We
prefer explicit arguments over configuration files. We prefer boring code.
When in doubt, write the test first and make it fail for the right reason.

We also value readability for the audience: this code is shown on slides, so
lines should be short, names should be obvious, and docstrings should explain
the why, not just the what. Comments should be rare but meaningful.

## 6. Rules
- Standard library only. Do not install packages or add dependencies.
- Money is `Decimal`, never float. Round once, at the end, with `money.round_money` (ROUND_HALF_UP to the currency's minor unit).
- Tax rates are supplied by the caller. Do not add a tax table.
- Never mix currencies in one total.
- Do not edit files in `data/`; they are fixtures other tests depend on.
- The export contract in `invoicing/export.py` is agreed with finance: change columns only when an issue asks for it.

## 7. Commands
- Tests: `python3 -m unittest` from the repository root (must pass before you finish).
- One module: `python3 -m unittest tests.test_money`
- Try it: `python3 -m invoicing report data/invoices.csv`
- Old way (before the package): `cd examples/v2/invoice/after && python3 -m unittest`
- Verbose tests: `python3 -m unittest -v`
- Run only the fast tests: `python3 -m unittest tests.test_money tests.test_invoice tests.test_customers tests.test_dates tests.test_fixtures tests.test_export tests.test_report tests.test_cli`
- Check the MCP server by hand: `printf '{"jsonrpc":"2.0","id":1,"method":"tools/list"}\n' | python3 tools/invoice_mcp.py`

## 8. Conventions and style guide
- Tests live in `tests/test_<module>.py`; add or update one for every behaviour change.
- British spelling in identifiers that already use it (`normalise_name`, `summarise`); do not rename them in passing.
- Keep changes small and scoped to the issue; mention anything you noticed but did not fix.
- Use four spaces for indentation. No tabs.
- Maximum line length is 100 characters (we are not strict about it).
- Use double quotes for strings, except in the old v2 fixture which uses single quotes.
- Imports: standard library first, then local imports, alphabetical.
- Use f-strings, not `%` formatting or `.format()`.
- Type hints on public functions are nice to have.
- Every module starts with a docstring that explains why it exists.
- Prefer `pathlib.Path` over `os.path`.
- Name tests `test_<behaviour>`, not `test_<function>`.
- Do not use `print` for debugging in committed code.
- Commit messages: imperative mood, under 72 characters, no trailing period.

## 9. Testing philosophy

Tests are the specification. When finance and the code disagree, we write a
test that captures what finance wants and then change the code. We use the
standard `unittest` module because it ships with Python, and we avoid mocks
wherever possible: the functions are pure, so tests call them with literal data.
Fixture files in `data/` are shared by several tests, which is why they must
not be edited casually. When you add a currency or a date format, add at least
one test for the happy path and one for the edge case (rounding boundary, leap
year, empty input).

## 10. Notes from past sessions
- 2026-03-04: The Müller incident. A customer appeared twice in the report
  because one export used a decomposed umlaut. Fixed by `normalise_name`.
- 2026-04-11: Tried `locale.format_string` for money formatting; it depends on
  the machine locale and broke CI on the Mac mini. Reverted. Use format_money.
- 2026-05-19 (Tue): Fixed the flaky test in test_report — it depended on dict
  ordering in an old version. If it flakes again, just rerun it.
- 2026-06-02: The PDF tests take 40 seconds; Petra is looking into it.
- 2026-06-23: Discussed whether gross should round per line or per invoice.
  Decision: per invoice, round once. See the talk 02 slides.
- 2026-07-08: Claude kept trying to install pytest. Don't. unittest is enough.
- 2026-07-30: Remember that GBP rows in data/invoices.csv use 20 % VAT.
- 2026-08-12: Added the MCP server. It has to flush stdout after each line or
  Claude Desktop hangs.
- 2026-08-27: Sales asked about JPY. Not supported yet (see backlog 003).
- 2026-09-01: Someone renamed `summarise` to `summarize` in a branch and broke
  the talk slides. Reverted.

## 11. Glossary
- **Net**: amount before tax.
- **Gross**: amount after tax, rounded once.
- **Tax rate**: a decimal fraction, 0.21 means 21 %.
- **Minor unit**: the smallest currency unit, cent for EUR, haléř for CZK.
- **Quantum**: `Decimal('0.01')` for a two-decimal currency.
- **Fixture**: a CSV file in `data/` used by tests and demos.
- **Terms**: payment terms, e.g. net 30.
- **EOM**: end of month.
- **BOM**: byte order mark, `﻿` at the start of some UTF-8 files.
- **MCP**: Model Context Protocol.

## 12. FAQ
**Why not float?** Because 0.1 + 0.2 != 0.3.
**Why ROUND_HALF_UP and not banker's rounding?** Finance asked for it; it is
what customers expect on paper invoices.
**Why no tax table?** Rates depend on country, product and date. The caller knows.
**Why plain dicts and not dataclasses?** Easier to show on slides and to build
in tests.
**Why is the export a string and not a file?** So it has no side effects and the
tests do not touch the disk.
**Where are the slides?** In the repository root, one HTML file per talk.
