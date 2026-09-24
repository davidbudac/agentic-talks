# Lab 3 · Break the grader (40 min, no model calls)

An eval is only as good as its checker. A checker that is too weak passes wrong
work, and every number you compute on top of it (pass rates, cost per accepted
task) is then wrong too. In this lab you attack a weak checker, then fix it.

The task is `export-currency-column`: add a sixth CSV column, `currency`, after
`gross`, upper case, `EUR` when the invoice has none, and keep the rest of the
export contract (order, quoting, the gross rule, a header for empty input).

## What is here

| Path | What |
|---|---|
| `weak/` | The weak checker: `checker.conf` runs only `WeakCurrencyColumnTest`, which checks that the header mentions "currency". It compiles the code and runs one test. Nothing else |
| `cheats/cheat-1-header-only/` | Wrong: the header gains the column, the rows do not |
| `cheats/cheat-2-hardcoded-eur/` | Wrong: every row says `EUR`, whatever the invoice currency |
| `../eval/solutions/export-currency-column/` | The reference solution (with its updated tests) |
| `answer-key/` | A strong checker: the full own suite, the hidden acceptance tests and a seeded property check over 300 random invoices. Do not open it before the debrief |
| `checker.sh` | Runs one checker against one implementation (used by `../lab3.sh`) |

A checker is a folder with `checker.conf` and `tests/*.java`:

```sh
TEST_FILTER=WeakCurrencyColumnTest   # passed to Surefire as -Dtest=...; empty = every test
RUN_OWN_TESTS=0                      # 1 = also run the repo's own tests (src/test/java)
```

Its tests are copied into `src/test/java/com/example/invoicing/` of a scratch
copy of the implementation and run with `./mvnw -q -o test`. Pass means Maven
succeeded and at least one of the checker's tests ran.

## Steps

```sh
./lab3.sh            # creates lab3-work/repo (your app copy) and lab3-work/checker (a copy of weak/)
./lab3.sh check      # matrix: weak + your checker x {yours, reference, cheat-1, cheat-2}
./lab3.sh answer     # the same plus the answer key (debrief)
./lab3.sh reset      # start again
```

1. **(5 min) Read `weak/`.** Write down, before you run anything, what a wrong
   implementation could get away with.
2. **(10 min) Partner A cheats.** Edit
   `lab3-work/repo/src/main/java/com/example/invoicing/CsvExport.java` so the
   weak checker passes while the behaviour is wrong in a way the cheats here
   do not already cover. Ideas: currency in the wrong position, not upper-cased,
   quoting broken for one case, the gross column changed, the empty-input
   header dropped. Run `./lab3.sh check`: your row should say PASS under
   `weak`.
3. **(15 min) Partner B strengthens `lab3-work/checker/`.** Options, from cheap to strong:
   - set `RUN_OWN_TESTS=1` and `TEST_FILTER=`. The repo's own tests now fail
     both cheats, but only because the cheats left the old five-column
     assertions alone. Why is that no defence? (In the eval, the agent edits
     those tests; a cheat that updates them to match itself passes.)
   - add hidden JUnit tests with concrete rows (a CZK invoice, a lower-case
     code, a missing currency, a customer with a comma and a newline);
   - add a property check: generate many invoices from a fixed `Random` seed,
     export, read back with `CsvReader.read`, and assert invariants for every
     row (six cells, input order, `gross` equals `invoice.gross()`, currency
     rule). A fixed seed keeps failures reproducible.

   Goal: under `mine`, the reference is PASS and everything else is fail.
4. **(5 min) Swap.** B cheats against A's checker. Does it hold?
5. **(5 min) Debrief** with `./lab3.sh answer`.

## Questions for the debrief

- A checker that fails the reference is also broken: it would reject a correct
  agent and push your pass rate down. Did yours ever do that?
- Which of your tests would an agent see if they lived in the repo? (That is
  why the eval keeps them in `eval/hidden/` and copies them in only to grade.)
- The eval checker also replaces `pom.xml`, `mvnw` and `.mvn/` with pristine
  copies and requires at least as many own tests as the untouched repo has.
  Which cheats does that stop?
- What is the cost of a false pass in your own team's eval? Of a false fail?

Every `check` writes `results/lab3/<ts>/matrix.md` and a copy of your checker.
