# invoice-app

A small invoicing toolkit in Java 21, the shared example for the evals workshop
labs. It is a port of the Python `examples/series/invoice-app` used in talks
03–07: the same `gross()` rule, the same CSV export contract and the same
latent bugs, written as idiomatic Java. JUnit 5 is the only dependency.

```sh
./mvnw -q test                    # all tests (downloads Maven and JUnit once)
./mvnw -q -o test                 # the same, offline, once dependencies are cached
./mvnw -q test -Dtest=MoneyTest   # one test class
./mvnw -q compile && java -cp target/classes com.example.invoicing.Cli report data/invoices.csv
java -cp target/classes com.example.invoicing.Cli export data/invoices.csv
java -cp target/classes com.example.invoicing.Cli due data/invoices.csv --today 2026-09-24
```

There is no `exec` plugin; run the CLI with `java -cp target/classes` after
compiling.

| Class (`com.example.invoicing`) | What it does |
|---|---|
| `Money` | `BigDecimal` parsing, currency exponents, `HALF_UP` rounding, formatting, allocation |
| `MoneyException` | Amounts or currencies the package cannot handle |
| `Invoice` | The invoice record: id, customer, net, tax rate, currency, issue date, terms |
| `Invoices` | `gross()`, invoice lines and totals that reconcile, rounding once |
| `CustomerNames` | Unicode names: NFC, accent-insensitive matching, `Collator` ordering, safe truncation |
| `InvoiceDates` | ISO and dotted dates, payment terms, due dates |
| `CsvReader` | A small RFC 4180 reader (quotes, embedded line breaks, CRLF) |
| `FixtureLoader` | Loading and validating CSV fixtures into `Invoice` records |
| `FixtureException` | A fixture that cannot be used, with its row number |
| `CsvExport` | The five-column CSV export agreed with finance |
| `Report` | Plain-text totals per customer and currency |
| `Cli` | `report`, `export` and `due` commands |

Fixtures live in `data/`. `data/legacy-export.csv` comes from the old
accounting tool and the loader cannot read it yet. Open work is in `backlog/`,
one Markdown file per issue.

The tests pass, and the code still has defects the tests do not cover. That is
deliberate: the workshop's hidden acceptance tests look for them.

This is a synthetic teaching fixture, not a tax calculator for production. Tax
rates are example inputs supplied by the caller.
