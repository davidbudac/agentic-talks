# One example for talks 02 and 03

This is a synthetic teaching fixture, not a tax calculator for production. The rate and rounding rule are explicit example inputs. It uses Python's standard library and needs no API key or network.

## Reproduce the prepared checkpoints

From this repository root:

```sh
(cd examples/v2/invoice/before && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v)
(cd examples/v2/invoice/after && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v)
```

The first command is supposed to fail: 3 tests run, 2 fail because tax is ignored. The second runs the 3 invoice tests and 2 CSV tests; all 5 should pass. `before/` and `after/` are prepared fixtures, not a transcript of an autonomous agent session.

## Optional live demo for talk 02

Copy `before/` into a new disposable directory before the talk. Open your chosen agent in that directory only. Set permissions to require confirmation for actions outside the task. The demo requires no network access, credentials, installation or publication.

Give it this prompt:

> Fix the failing invoice tests. Inspect the code and explain the cause before editing. Apply the supplied tax rate, rounding once to two decimal places using ROUND_HALF_UP. Preserve the tests. Work only in this demo directory; do not install, publish or send anything. Run `python3 -m unittest -v` and show the result and the diff. Ask if the requirement is unclear.

Pause at four checkpoints: the first failure, the file/tool result, the patch, and the final verification. If the live run is unavailable, use the deck's prepared checkpoints. An agent may follow a different sequence or fail; do not claim the prepared results came from the current run.

## Extension for talk 03

The `after/` directory includes a reference `export_invoices(rows)` implementation and CSV tests. Read `export.py` and `test_export.py` with the audience; do not spend the talk building an unrelated application.

Acceptance contract: keep the calculation rule, output the five named columns, quote commas/quotes/newlines, preserve input order and emit a header for empty input. The fixture assumes validated row dictionaries; input validation, spreadsheets interpreting formulas, streaming and production integration are outside its scope.

A reference CSV is in `../invoices.csv`. The slides use a shortened view of it. The exported customer strings and totals are checked by tests.
