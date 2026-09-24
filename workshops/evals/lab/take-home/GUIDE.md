# Take it home: three tasks from your own Java repo

The workshop suite measured an invented invoice app. Your numbers mean more on
your own code. This guide turns three tasks from your repository's history
into an smevals suite you can run on your laptop or in CI. Budget an afternoon.

## 1. Pick three tasks you already solved

Search `git log` for small, finished pieces of work with tests:

| Kind | Look for | Why |
|---|---|---|
| Bug fix | A commit that fixed a bug and added a test | Clear pass/fail; the fix is your reference |
| Small feature | An issue closed by one PR, 50 to 300 lines | Tests the agent's reading of a spec |
| Refactor | A rename or move with many callers | Tests completeness, not cleverness |

Each should take a person under an hour. Skip anything that needs network
access, secrets or a database the agent cannot start.

For each task note two commits: the **base** (the parent of the fix, where the
work had not been done) and the **fix** (the known-good result).

## 2. Write the task

Copy `template/eval/` next to your repository (or into it, see section 6) and
edit `tasks/*.yaml`:

- `name`: a short id, also the folder name under `hidden/`.
- `base_ref`: the base commit, **quoted** (`"a1b2c3d"`), or YAML may read a
  numeric-looking hash as a number.
- `prompt`: the issue text as a colleague would have received it. Do not
  paste the solution, and do not mention the hidden tests. End with the
  command that must pass, e.g. `Run ./mvnw -q test before you finish.`

## 3. Hide the acceptance tests

Take the tests the fix commit added or changed, and turn them into
`hidden/<task>/Hidden<Something>Test.java`: same package as the code under
test, class name starting with `Hidden`. Keep them outside the agent's copy:
the runner deletes `eval/` from its clone, and the checker copies the hidden
files in only when grading.

Tests that only pass with the exact reference implementation are too strict.
Test behaviour the issue asked for, plus anything that must not change.

## 4. Check the checker, both ways

```sh
git worktree add /tmp/base <base_ref>   && eval/checkers/maven-hidden-tests --repo /tmp/base --task example-bugfix   # must FAIL
git worktree add /tmp/fix  <fix commit> && eval/checkers/maven-hidden-tests --repo /tmp/fix  --task example-bugfix   # must PASS
```

A checker that passes on the base measures nothing; one that fails on the real
fix will fail every agent. Lab 3 showed a third check: write one plausible
wrong solution and make sure it fails too.

The checker runs Maven offline (`-o`). Prefetch once with
`./mvnw dependency:go-offline`, or set `MAVEN_OFFLINE=0`.

## 5. Run it

```sh
export REPO_DIR=/path/to/your/repo          # or REPO_URL=git@...
for round in 1 2 3; do                      # smevals 0.2.0 has no -n: one call per round
  uvx --from smevals==0.2.0 smevals run eval -c default -m claude-sonnet-5 -g --runs-dir runs || true
done
uvx --from smevals==0.2.0 smevals report eval --runs-dir runs --by-task
```

`ci/run-evals.sh` does the same loop and prints, per task, passes out of k,
pass@k (at least one run passed) and pass^k (every run passed), the overall pass
rate, and Claude Code's cost estimate per accepted task. Use k of at least 3:
one run per task tells you almost nothing about an agent that passes 60 % of
the time.

Compare variants the way the labs did: a second config with a different
CLAUDE.md or `-m claude-haiku-4-5`, the same tasks, the same k. Decide on the
cost per accepted task, not the pass rate or the cost alone.

## 6. Put it in CI (optional)

- `ci/github-actions.yml`: manual and weekly runs, uploads `runs/`, fails the
  job below a pass-rate threshold.
- `ci/run-evals.sh`: the same for Jenkins, GitLab CI or cron. Exit code 1 means
  below threshold.

CI has no subscription login, so it needs `ANTHROPIC_API_KEY`, billed per
token. Three tasks, k = 3, Sonnet: expect roughly 9 sessions at a few tens of
cents each; `MAX_BUDGET_USD` caps every session. If `eval/` is committed to the
repository, the runner removes it from the agent's copy (`HIDE_PATHS`).

## Files

```
template/eval/
├── eval.yaml
├── tasks/example-{bugfix,feature,refactor}.yaml   # name, base_ref, prompt
├── configs/default.yaml                           # runner + default model
├── graders/default.yaml                           # the checker, pass threshold 1.0
├── checkers/maven-hidden-tests                    # copies hidden tests in, runs Maven
├── hidden/<task>/Hidden*Test.java                 # you write these
└── run-claude                                     # one headless Claude Code session
ci/github-actions.yml, ci/run-evals.sh
```
