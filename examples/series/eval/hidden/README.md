Hidden acceptance tests, one module per task. The agent never sees them: the
checker runs them against the agent's copy of invoice-app after the run
(`python3 -m unittest discover -s hidden -p test_<task>.py`, cwd = the copy).
