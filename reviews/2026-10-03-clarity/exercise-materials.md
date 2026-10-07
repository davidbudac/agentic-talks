# Invoice workflow exercises

These are synthetic teaching fixtures, not measured agent runs. Use them with Cost & Context, Orchestrating Agents, Measuring What Works, or the Working Smarter workshop. No account or paid model call is needed for the static route.

## Task contract

Export invoices as CSV with fields `customer,net,vat,gross`. Use the VAT rate from each order. For this exercise, round VAT half up to two decimal places, then add it to net. Quote fields containing commas. Preserve stored invoice records. Ask before changing the stored schema.

| Case | Customer | Net | Rate | Expected VAT | Expected gross |
|---|---|---:|---:|---:|---:|
| Standard | Acme | 100.00 | 21% | 21.00 | 121.00 |
| Zero VAT | Beta | 100.00 | 0% | 0.00 | 100.00 |
| Rounding | Tiny | 0.05 | 10% | 0.01 | 0.06 |
| CSV escaping | ACME, Ltd | 100.00 | 21% | 21.00 | 121.00 |

Use decimal arithmetic for the monetary checks. This rounding policy belongs to the fictional exercise and is not general tax guidance.

## Exercise 1: grade the output (10 minutes)

Variant A produces the following two rows; no other cases have been run:

```csv
customer,net,vat,gross
Acme,100.00,21.00,121.00
Beta,100.00,21.00,121.00
```

Variant B produces these three rows; the rounding case has not been run:

```csv
customer,net,vat,gross
Acme,100.00,21.00,121.00
Beta,100.00,0.00,100.00
ACME, Ltd,100.00,21.00,121.00
```

For each case, record pass, fail, or not tested. Give the evidence, then propose the next check. Do not score an absent result as a pass. No elapsed time, token use or cost has been measured.

Facilitator key: A passes standard VAT and fails zero VAT; its other cases are not tested. B passes the first two cases, fails CSV escaping because the last row parses into five fields, and has no rounding result. Neither variant meets the contract. The corrected final B row is `"ACME, Ltd",100.00,21.00,121.00`.

## Exercise 2: simplify instructions (10 minutes)

Variant A:

```text
This repository was founded to simplify our invoice reporting.
Always write good code. Follow the style. Make things maintainable.
VAT rates come from each order record, not a fixed default.
Round VAT half up to cents, then add it to net.
Run pytest tests/test_invoice.py tests/test_export.py -q.
Preserve stored invoice records. Ask before schema changes.
On Tuesday we had a broken CI runner; retries helped at the time.
We value quality. Please keep the code clean and clear.
Detailed release and deployment procedures follow in several pages...
```

Propose variant B. Keep the VAT source, rounding policy, verification command and record/schema boundary. Move occasional procedures to a discoverable reference or skill. Remove stale incident notes and duplicated advice. State a regression case for each retained constraint.

With a prepared runtime, compare A and B on identical clean copies of the exercise repository and repeated trials. Record correctness, uncached input, cache writes, cache reads, output, retries, elapsed time and review effort. Without a runtime, mark those fields **not run**; do not infer savings from word count.

## Exercise 3: design a ticket lifecycle (10 minutes)

Write one ticket with: goal, scope, acceptance cases, owner, lease or claim rule, retry budget, return contract and reviewer. Walk through three events: missing VAT rule, duplicate worker claim, and a passing test suite that lacks CSV-escaping coverage. Explain the next state and who owns the decision.

Acceptance: exactly one implementation owner; no invented VAT rule; review catches the missing case; failed or blocked work returns evidence. A worktree separates edits; configured filesystem/network/credential controls provide containment.

## Exercise 4: author the verification skill (10 minutes)

Write a short `SKILL.md` for invoice or CSV changes. Name the trigger, checks, evidence to retain and what to report when a command fails to start. Include the four acceptance cases above. On paper, test its instructions against A and B. With an approved runtime, also test discovery on one relevant request and one unrelated request.

Acceptance: the procedure rejects both synthetic candidates, marks rounding untested and does not mistake syntax validity for correct invoice behavior. A parsed skill file alone does not prove that discovery or execution worked.

## Exercise 5: compare interfaces (10 minutes)

Design a read-only comparison: fetch the invoice ticket through CLI and MCP, with the same data, permissions and expected fields. Record tool discovery/help overhead, errors, all token categories, latency and correctness. Compare cold and warm use. If one interface cannot perform the same task, record the capability difference before comparing cost. No winner is supplied.

## Exercise 6: hardware feasibility (10 minutes)

A hypothetical model has 35 billion total parameters and 3 billion active per token. Four-bit weight storage alone is about 17.5 decimal GB. A machine has 16 GB available memory. Explain why active parameters do not establish fit. List KV cache, runtime buffers, quantization metadata and context/concurrency effects. Offloading may permit execution, but requires measured memory, transfer cost, latency and acceptance results.

## Exercise 7: voice-input boundary (3 minutes)

Intended: “Export the invoices **without changing stored records**.”
Faulty transcript: “Export the invoices, **changing stored records**.”

Repair the instruction before execution and name a check that would detect changed stored records. No microphone is needed.

## Trial worksheet

Copy one row per trial; leave unavailable data marked not measured.

| Case / variant / run | Environment and settings | Acceptance result | Evidence | Token categories | Total cost | Elapsed time | Retries | Review / remaining gaps |
|---|---|---|---|---|---|---|---|---|
| — | — | not run | — | not measured | not measured | not measured | — | — |

Keep failed runs in aggregate costs and success rates. Separate development cases from held-out comparisons. A small sample is exploratory, not a production reliability estimate.

## Facilitator preparation

The static route is complete. For optional live execution, supply a disposable invoice repository with real tests, separate starting copies for variants, approved credentials, an enforced budget and a usage capture method. The slides' `pytest` commands are examples for that project; they are not test commands for this slide repository. Rehearse any live demonstration and keep this static route available. Do not present synthetic outputs as recordings or claim unmeasured savings.
