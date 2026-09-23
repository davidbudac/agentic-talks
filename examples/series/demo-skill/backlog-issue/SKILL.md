---
name: backlog-issue
description: Work one issue from this repo's backlog/ folder end to end. Use when asked to implement, fix or pick up a backlog item or issue number (for example "do 003" or "pick up the JPY issue").
---

1. Find the issue: `ls backlog/` and read the matching file in full.
2. Restate its acceptance criteria as a checklist before editing anything.
3. Read only the files the issue names; search with grep before opening others.
4. Make the smallest change that meets every criterion, and add or update a test for each.
5. Run `python3 -m unittest` and fix failures until it passes.
6. Reply with the checklist ticked, the files changed and anything you noticed but left alone.
