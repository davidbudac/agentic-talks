# invoice-app — Project Guide for AI Assistants

> Last big update: March 2026 (Tomas). Please keep this file up to date! Everyone
> should add anything they learn here so the agent knows it next time.

## Table of contents
1. Project history
2. Architecture overview
3. Directory layout
4. Class-by-class guide
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

invoice-app started in 2024 as a single Python script with one function,
`gross()`, and a famous bug: it ignored the tax rate. The fix (apply the rate,
round once, half up) became the demo for talk 02. In 2025 the Java team asked
for a version they could use in their own onboarding, so Tomas ported it to
Java 17 with Maven, and later to Java 21 when we moved to records everywhere.
The package was `cz.acme.invoice` for a while, then `com.example.invoicing`
after legal asked us not to use a real company name.

We considered Spring Boot (twice), Gradle (see TODO below), Lombok, Joda-Money
and Apache Commons CSV, and rejected all of them because the project is a
teaching fixture and must build with nothing but a JDK and the Maven wrapper.
Please do not re-open these discussions. We also had a PDF renderer for a while
(`LegacyPdfRenderer`), which is being removed.

## 2. Architecture overview

The architecture follows a layered approach. At the bottom sits `Money`, which
knows nothing about invoices: it parses amounts into `BigDecimal`, knows the
minor-unit exponent of each currency, and applies the single rounding rule. On
top of it, `Invoices` implements the calculation: `gross()` takes a net amount
and a tax rate and returns the rounded gross, `Line.net()` multiplies quantity
by unit price without rounding, and `totals()` sums lines exactly and rounds
once at the end so that net + tax = gross always reconciles.

The `Invoice` record is the central data type. It is immutable, validates its
arguments in the compact constructor, normalises the currency code and defaults
the payment terms. It has a `gross()` convenience method that delegates to
`Invoices.gross()`.

Next to the calculation layer sit two independent helper classes.
`CustomerNames` handles Unicode customer names: normalising to NFC, collapsing
whitespace, stripping accents for comparison, ordering with a `Collator`,
matching and truncating for display without splitting a letter from its accent
(it uses `BreakIterator` for that). `InvoiceDates` parses issue dates (ISO and
the dotted format from the old accounting tool) and computes due dates from
payment terms such as "net 30" and "end of month".

The input layer is `CsvReader` plus `FixtureLoader`. `CsvReader` is a small
hand-written RFC 4180 parser (we did not want Commons CSV, see above).
`FixtureLoader` turns its records into `Invoice` objects and validates them:
required columns, unique invoice ids, valid amounts and known currencies.
Errors are `FixtureException` with a row number.

The output layer has two classes. `CsvExport` writes the five-column CSV that
finance imports; it is pure and returns a `String`, the caller decides where it
goes. `Report` aggregates invoices into one `Entry` per customer and currency
and renders a fixed-width text table with a total line per currency. Currencies
are never mixed.

Finally `Cli` wires everything into a command line with three subcommands,
`report`, `export` and `due`. `Cli.run()` takes the output streams as
parameters so tests do not have to capture `System.out`.

Data flows strictly downwards: Cli → FixtureLoader → (CsvExport | Report) →
Invoices → Money. Nothing depends on Cli. Nothing does network I/O. The only
filesystem access is in `CsvReader.read(Path)`.

## 3. Directory layout

```
invoice-app/
├── README.md                     # overview and commands
├── pom.xml                       # Java 21, JUnit 5 only
├── mvnw, mvnw.cmd, .mvn/         # Maven wrapper (do not edit)
├── backlog/                      # open issues as markdown files
├── data/
│   ├── invoices.csv              # 12 invoices, 4 currencies, Unicode names
│   └── legacy-export.csv         # from the old accounting tool (BOM, dotted dates)
└── src/
    ├── main/java/com/example/invoicing/
    │   ├── Cli.java              # command line
    │   ├── CsvExport.java        # five-column CSV export
    │   ├── CsvReader.java        # RFC 4180 reader
    │   ├── CustomerNames.java    # Unicode customer names
    │   ├── FixtureException.java
    │   ├── FixtureLoader.java    # CSV fixtures -> Invoice records
    │   ├── Invoice.java          # the record
    │   ├── InvoiceDates.java     # issue dates and payment terms
    │   ├── Invoices.java         # gross(), lines, totals
    │   ├── LegacyPdfRenderer.java # PDF invoices (old, being removed)
    │   ├── Money.java            # BigDecimal parsing and rounding
    │   ├── MoneyException.java
    │   ├── Report.java           # text report
    │   └── util/
    │       ├── Strings.java      # padding helpers
    │       └── Preconditions.java
    └── test/java/com/example/invoicing/
        ├── CliTest.java
        ├── CsvExportTest.java
        ├── CsvReaderTest.java
        ├── CustomerNamesTest.java
        ├── FixtureLoaderTest.java
        ├── InvoiceDatesTest.java
        ├── InvoicesTest.java
        ├── LegacyPdfRendererTest.java
        ├── MoneyTest.java
        └── ReportTest.java
```

## 4. Class-by-class guide

### Money
- `parse(String)` accepts `" 1_000.50 "`. Blank or non-numeric input throws
  `MoneyException`. There is deliberately no `parse(double)`.
- `normaliseCurrency(code)` upper-cases (with `Locale.ROOT`!) and checks
  against `CURRENCY_EXPONENTS`. `null` means EUR.
- `exponent(code)` returns the number of decimals, `quantum(code)` the smallest unit.
- `round(amount, code)` is THE rounding function. Use it everywhere.
- `format(amount, code)` gives `1,234.50 EUR`.
- `allocate(total, parts, code)` splits an amount so the parts add up exactly
  (largest remainder method). Used for instalment plans.

### Invoice (record)
- Components: `id`, `customer`, `net`, `taxRate`, `currency`, `issueDate`, `terms`.
- Compact constructor: null checks, negative rate check, currency normalised,
  terms default to "net 30".
- `Invoice.of(id, customer, net, taxRate, currency)` for tests.
- `gross()` delegates to `Invoices.gross()`.

### Invoices
- `gross(net, taxRate, currency)`: the original function. Negative rates throw.
  Round once.
- `Line(quantity, unitPrice)`: quantity must be positive; `net()` does not round.
- `totals(lines, taxRate, currency)` returns `Totals(net, tax, gross, currency)`.
  Tax is computed as gross - net so it always reconciles.

### CustomerNames
- `normalise`: NFC + whitespace. Keeps case and accents.
- `stripAccents`: NFKD and drop combining marks.
- `comparator()`: root-locale `Collator` at primary strength, tie-break on the
  normalised name.
- `matches(name, query)`: substring, accent- and case-insensitive.
- `initials(name)`: first two words.
- `displayName(name, width)`: truncate with an ellipsis, grapheme-safe,
  newlines to spaces.

### InvoiceDates
- `parse(text)`: ISO or dotted. Throws `IllegalArgumentException`, never
  `DateTimeException`.
- `endOfMonth(day)`, `dueDate(issued, terms)`, `isOverdue(issued, terms, today)`.
- Terms: "net N", "end of month", "on receipt". Case and extra spaces are fine.

### CsvReader / FixtureLoader
- `CsvReader.read(Path | String | Reader)` returns `List<List<String>>`.
- `FixtureLoader.load(Path)`, `parse(Reader)`, `parseText(String)`.
- Required columns: invoice_id, customer, net, tax_rate. Optional: currency
  (EUR), issue_date (none), terms ("net 30").
- Throws `FixtureException` with the row number (the header is row 1).

### CsvExport
- `export(List<Invoice>)` returns a `String`. Columns: invoice_id, customer,
  net, tax_rate, gross. Header always written. Order preserved. Quoting is done
  by the private `quote()` helper.

### Report
- `summarise(invoices, currency)`, `grandTotals(entries)`, `render(entries)`,
  `build(invoices, currency)`. `Entry(customerName, currency, invoices, net, gross)`.
- `NAME_WIDTH = 24`.

### Cli
- `report FILE [--currency]`, `export FILE`, `due FILE [--today]`.
- Exit code 2 on errors, message on stderr prefixed with `error:`.

### LegacyPdfRenderer
- Renders a PDF invoice using hand-written PDF operators. Being removed in Q3;
  do not add features. Its tests are slow, skip them if needed.

## 5. Design philosophy

We value correctness over cleverness. An invoice that is off by one cent is a
support ticket, a credit note and an unhappy customer, so every amount is a
`BigDecimal` from the moment it is parsed. We prefer small static methods and
immutable records, because they are easy to test and easy to explain in a
workshop. We avoid inheritance, frameworks, annotations processors and
dependency injection. We prefer explicit arguments over configuration files.
We prefer boring code. When in doubt, write the test first and make it fail for
the right reason.

We also value readability for the audience: this code is shown on slides, so
lines should be short, names should be obvious, and Javadoc should explain the
why, not just the what. Comments should be rare but meaningful.

## 6. Rules
- Java 21, JUnit 5. Do not add dependencies or plugins to `pom.xml`.
- Money is `BigDecimal`, never `double`. Round once, at the end, with `Money.round` (`HALF_UP` to the currency's minor unit).
- Tax rates are supplied by the caller. Do not add a tax table.
- Never mix currencies in one total.
- Do not edit files in `data/`; they are fixtures other tests depend on.
- The export contract in `CsvExport` is agreed with finance: change columns only when an issue asks for it.

## 7. Commands
- Full build: `mvn clean install` (make sure Maven 3.8+ is installed).
- Tests: `./mvnw -q test` from the repository root (must pass before you finish).
- One class: `./mvnw -q test -Dtest=MoneyTest`
- One method: `./mvnw -q test -Dtest=MoneyTest#roundsHalfUpToTheMinorUnit`
- Try it: `./mvnw -q compile && java -cp target/classes com.example.invoicing.Cli report data/invoices.csv`
- Skip the slow PDF tests: `./mvnw -q test -Dtest='!LegacyPdfRendererTest'`
- Offline (on the train): `./mvnw -o test`
- Old way (Java 17 branch): `mvn -Pjava17 verify`

## 8. Conventions and style guide
- Tests live in `src/test/java/com/example/invoicing/<Class>Test.java`; add or update one for every behaviour change.
- British spelling in identifiers that already use it (`normalise`, `summarise`); do not rename them in passing.
- Keep changes small and scoped to the issue; mention anything you noticed but did not fix.
- Use four spaces for indentation. No tabs.
- Maximum line length is 120 characters (100 for anything shown on a slide).
- Prefer records for data, `final` classes with a private constructor for utilities.
- Always pass `Locale.ROOT` to `toUpperCase`, `toLowerCase` and `String.format`.
- Imports: no wildcards, static imports only in tests.
- Name tests after the behaviour (`roundsHalfUpToTheMinorUnit`), not the method.
- Use `assertThrows`, never `@Test(expected = ...)` (that is JUnit 4).
- Do not use `System.out.println` for debugging in committed code.
- Commit messages: imperative mood, under 72 characters, no trailing period.

### Conventions (repeated from the old wiki page)
- Put tests next to the code they test, one test class per class.
- Use American spelling for new identifiers; keep British spelling where it exists.
- Always run the full build with `mvn clean install` before committing.
- Use `BigDecimal.valueOf(double)` for constants (it is safer than `new BigDecimal(double)`).
- Keep pull requests under 400 lines.

## 9. Testing philosophy

Tests are the specification. When finance and the code disagree, we write a
test that captures what finance wants and then change the code. We use plain
JUnit 5 with no mocking library: the methods are pure, so tests call them with
literal data. Fixture files in `data/` are shared by several tests, which is
why they must not be edited casually. When you add a currency or a date format,
add at least one test for the happy path and one for the edge case (rounding
boundary, leap year, empty input). Surefire runs with a fixed locale and time
zone (see `pom.xml`) so the tests are deterministic.

## 10. Notes from past sessions
- 2025-11-20: Ported to Java 17. Records need `--enable-preview`? (No, they are
  final since 16. Leaving this note in case someone asks again.)
- 2026-01-15: TODO Tomas: migrate to Gradle. (Postponed, see section 1.)
- 2026-03-04: The Müller incident. A customer appeared twice in the report
  because one export used a decomposed umlaut. Fixed in `CustomerNames.normalise`.
- 2026-04-11: Tried `NumberFormat.getCurrencyInstance()` for money formatting;
  it depends on the machine locale and broke CI on the Mac mini. Reverted.
- 2026-05-19 (Tue): Fixed the flaky test in `ReportTest`; it depended on
  `HashMap` ordering. If it flakes again, just rerun it.
- 2026-06-02: The PDF tests take 40 seconds; Petra is looking into it.
- 2026-06-23: Discussed whether gross should round per line or per invoice.
  Decision: per invoice, round once. See the talk 02 slides.
- 2026-07-08: Claude kept trying to add AssertJ and Mockito. Don't. JUnit is enough.
- 2026-07-30: Remember that GBP rows in data/invoices.csv use 20 % VAT.
- 2026-08-20: Upgraded to Java 21. We still compile with `--release 17` on the
  build server (check before using pattern matching for switch).
- 2026-08-27: Sales asked about JPY. Not supported yet (see backlog).
- 2026-09-01: Someone renamed `summarise` to `summarize` in a branch and broke
  the workshop slides. Reverted.

## 11. Glossary
- **Net**: amount before tax.
- **Gross**: amount after tax, rounded once.
- **Tax rate**: a decimal fraction, 0.21 means 21 %.
- **Minor unit**: the smallest currency unit, cent for EUR, haléř for CZK.
- **Quantum**: `0.01` for a two-decimal currency.
- **Scale**: the number of digits after the decimal point of a `BigDecimal`.
- **Fixture**: a CSV file in `data/` used by tests and demos.
- **Terms**: payment terms, e.g. net 30.
- **EOM**: end of month.
- **BOM**: byte order mark, U+FEFF at the start of some UTF-8 files.
- **Collator**: `java.text.Collator`, locale-aware string comparison.
- **Surefire**: the Maven plugin that runs the tests.

## 12. FAQ
**Why not double?** Because 0.1 + 0.2 != 0.3.
**Why HALF_UP and not HALF_EVEN (banker's rounding)?** Finance asked for it; it
is what customers expect on paper invoices.
**Why no tax table?** Rates depend on country, product and date. The caller knows.
**Why records and not Lombok?** Records are in the language; Lombok is a dependency.
**Why is the export a String and not a file?** So it has no side effects and the
tests do not touch the disk.
**Why `equals` fails on `BigDecimal("1.0")` vs `BigDecimal("1.00")`?** Scale is
part of equality. Use `compareTo` when you mean numeric equality, `equals` in
tests when the scale matters (it usually does for money).
**Can I use `var`?** Yes, for local variables where the type is obvious.
**Where are the slides?** In the repository root, one HTML file per talk.
