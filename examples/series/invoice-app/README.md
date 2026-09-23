# invoice-app

A small invoicing toolkit used as the shared example in talks 03–07. It grows
out of the talk 02/03 fixture (`examples/v2/invoice/`): the same `gross()` rule
and the same `export_invoices()` contract, plus the modules a real repository
accumulates around them. Python standard library only; nothing to install.

```sh
python3 -m unittest                                # all tests, from this directory
python3 -m invoicing report data/invoices.csv      # totals per customer and currency
python3 -m invoicing export data/invoices.csv      # five-column CSV
python3 -m invoicing due data/invoices.csv --today 2026-09-24
python3 tools/invoice_mcp.py                       # the same commands as an MCP server (stdio)
```

| Module | What it does |
|---|---|
| `invoicing/money.py` | Decimal parsing, currency exponents, ROUND_HALF_UP, formatting, allocation |
| `invoicing/invoice.py` | `gross()`, line and invoice totals, rounding once |
| `invoicing/customers.py` | Unicode customer names: normalising, sorting, matching, truncating |
| `invoicing/dates.py` | Issue dates (ISO and dotted) and payment terms |
| `invoicing/fixtures.py` | Loading and validating CSV fixtures |
| `invoicing/export.py` | The talk 03 CSV export |
| `invoicing/report.py` | Plain-text totals per customer and currency |
| `invoicing/cli.py` | `python3 -m invoicing` |
| `tools/invoice_mcp.py` | Minimal stdio MCP server exposing the CLI commands |

Open work is in `backlog/`. `data/legacy-export.csv` is a file from the old
accounting tool that the loader cannot read yet (see the backlog).

This is a synthetic teaching fixture, not a tax calculator for production:
tax rates are example inputs supplied by the caller.
