Hidden acceptance tests, one folder per task. The agent never sees them: the
checker (`../checkers/hidden-tests`) copies them into a scratch copy of the
agent's repo, under `src/test/java/com/example/invoicing/`, and runs
`./mvnw -q -o test`. Class names start with `Hidden`, which is how the checker
tells them apart from the repo's own tests in the Surefire reports.

`../solutions/<task>/` holds a reference fix for every task. It exists to check
the checkers (`./selftest.sh` does), not to feed the agent.
