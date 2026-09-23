# Agentic Engineering · v2 speaker notes

Navigation: arrows / Space; Home / End; N notes; P presenter window; F fullscreen. Direct links use # followed by the physical slide number.

## 1. Agentic Engineering

The audience knows model, harness, tools and context from talk 02. This talk is about making the process repeatable. Each chapter takes one way the invoice-export workflow fails and fixes it.

## 2. Repeated work is harder than the demo

Aim for work you can accept on evidence and recover when it fails. Maximum autonomy is not the goal. One good transcript says little about how the next run will go.

## 3. The example: invoice CSV export

An excerpt from the reference CSV; the full file also has a customer name with a newline in it. The implementation assumes validated rows. Production validation and spreadsheet formula handling are separate requirements that we leave out.

## 4. Recap: the system you are engineering

Keep this to one slide. You control what information the system receives, what it may do, and how you check the results.

## 5. Problem 1 · “Add export” leaves too much open

Ask the room what they would need before they could review an export. This is a contract problem before it is a model problem, and more reasoning effort will not settle an ambiguous request.

## 6. Write the acceptance contract first

These four requirements are the ones the checked-in fixture implements. We kept the set small so every line is testable. Say plainly that production requirements are missing; this is not a billing system.

## 7. Decide how much structure the task needs

These are options, and nobody has to climb from one to the next. A workflow can contain agent-driven stages. Pick the simplest one that meets the contract and lets you explain the result.

## 8. Make the stages and ownership visible

The workflow for our export. Name one person who owns integration and acceptance. The next slides cover what evidence and recovery look like at each gate.

## 9. Problem 2 · a green command can mislead

An exit code tells you the command finished without an error. Whether the tests cover the contract is a separate question. No prompt can stop an agent from satisfying a weaker check; independent checks and review are how you catch it.

## 10. Give every claim a check

The reference test uses a comma, embedded quotes and a newline. Parsing the file with Python’s CSV reader tests the serialisation in a way that eyeballing the text cannot. Formula-like input stays outside this fixture’s contract.

## 11. Put the calculation in code with an explicit rule

When the calculation is specified, write it as code. The agent can read and change that code; you verify it against the stated rounding rule. This is the reference fix from talk 02, and the exporter reuses it.

## 12. Inspect the tests and the file they produce

Prepared result from after/: three invoice tests and two export tests. We generated the CSV with the same code and parsed it during validation. It is neither a benchmark nor a recorded agent run.

## 13. Keep acceptance separate from implementation

A second model can help review, but it may share the first one’s blind spots. Where it matters, keep acceptance checks where the implementing agent cannot edit them. In this workflow a person makes the call.

## 14. Problem 3 · the useful facts get buried

Do not describe attention as a fixed budget split equally between tokens. Irrelevant material can make retrieval worse and distract the model; how much depends on the model and the task.

## 15. Give each stage the context it needs

This split is our design; no harness does it for you. Each fresh stage needs enough context to keep earlier decisions, and a short handoff helps only if it carries the facts that matter.

## 16. Write a handoff note before restarting

A handoff note for the reference fixture. It keeps file references and open scope questions and leaves out pages of tool output. The new session should check the note against the files before relying on it.

## 17. Caching and compaction solve different problems

Billing rules, cache lifetimes and the handling of reasoning all vary by provider and model. Do not claim that requests must be byte-identical, that caches stay warm indefinitely, or that thinking is always kept or always stripped. Talk 04 covers the mechanics.

## 18. Problem 4 · retries consume the budget

Set a limit so a retry loop cannot keep editing forever. A flaky tool, a misunderstanding and an unmet requirement each need a different response.

## 19. Set a retry policy before the run

A policy sketch, not a setting you switch on. Pick the actual numbers for your environment. When a run stops, it should keep the evidence it gathered and report the task as unfinished.

## 20. Record a baseline you can return to

A branch or worktree isolates edits. It does nothing for credentials or network access, so isolate the environment separately when you need to. Do not reset a shared workspace that has uncommitted changes; you may destroy unrelated work.

## 21. Problem 5 · cheap tokens can buy costly work

Neither bigger nor smaller models are always cheaper. Compare the whole process on representative tasks with the same acceptance criteria. Subscription limits and API charges measure different things.

## 22. Measure the cost per accepted task

The numbers are invented to show the arithmetic; they measure no real model. Both setups spend one dollar of model and tool cost per accepted task. Add review time, as problem 5 says, and B is cheaper: ten accepted tasks for 15 minutes of review against six for 40. Keep failures, latency and review time visible as their own numbers too, so one total cannot hide them.

## 23. Change one dial and measure again

Put common tasks and failure-prone cases in the set, and run each enough times to see the variation. Rerun the trial when the model, prompt or tools change. Any ranking of named models you get is temporary.

## 24. Problem 6 · one agent carries too much

Delegation helps when an investigation can be split off, or when running work in parallel saves time. It costs coordination, handoffs and money, and this small export does not need it. The 80k and 200 token counts in the animation are illustrative; nobody measured them on this example.

## 25. Delegate an outcome with a boundary

A reviewer brief for the same export. Check the reviewer’s findings before you act on them; a short conclusion with no evidence does not count.

## 26. Parallel work still needs integration

Read-only reviews combine easily; parallel edits to the same files do not. Give independent edits their own worktrees, then run the tests again on the combined result.

## 27. Problem 7 · useful lessons disappear

A solved task rarely deserves a permanent note. Keep what will change how the next task goes, and prune stale instructions every so often. Plugin distribution can wait.

## 28. Write one small procedure people can inspect

An example skill body; a real package would add provider-specific files. Make the procedure readable and useful before you share it. It cannot enforce permissions or guarantee a complete review.

## 29. The complete workflow has a way back

Walk the invoice export through once. This rail folds Inspect and Plan from the earlier workflow into Contract. When new evidence overturns a decision, go back to the stage that made it. If the budget runs out, keep the partial result and mark it incomplete. The run succeeds when a reviewer accepts the evidence against the contract.

## 30. Improve one workflow this week

This is the one action to leave with. Push for a small change to a workflow people already run, before anyone adds fleets of agents or a plugin marketplace.

## 31. Go deeper where your work needs it

Take questions. The later decks have not been revised: they keep their own dates, some are still in progress, and nobody has rechecked their product claims for this edition.

## 32. Reference · workflows and evaluation

Sources for the design distinctions. The workflow, the retry table and the cost comparison are our teaching designs; none is a measured production result. SOURCES.md and VALIDATION.md record the evidence for this edition.
