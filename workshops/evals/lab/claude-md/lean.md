# invoice-app

## Rules
- Java 21, JUnit 5. Do not add dependencies or plugins to `pom.xml`.
- Money is `BigDecimal`, never `double`. Round once, at the end, with `Money.round` (`HALF_UP` to the currency's minor unit).
- Tax rates are supplied by the caller. Do not add a tax table.
- Never mix currencies in one total.
- Do not edit files in `data/`; they are fixtures other tests depend on.
- The export contract in `CsvExport` is agreed with finance: change columns only when an issue asks for it.

## Commands
- Tests: `./mvnw -q test` from the repository root (must pass before you finish).
- One class: `./mvnw -q test -Dtest=MoneyTest`
- Try it: `./mvnw -q compile && java -cp target/classes com.example.invoicing.Cli report data/invoices.csv`

## Conventions
- Tests live in `src/test/java/com/example/invoicing/<Class>Test.java`; add or update one for every behaviour change.
- British spelling in identifiers that already use it (`normalise`, `summarise`); do not rename them in passing.
- Keep changes small and scoped to the issue; mention anything you noticed but did not fix.
