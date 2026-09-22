# Agentic AI — v2 speaker notes

Navigation: arrows / Space; Home / End; N notes; P presenter window; F fullscreen. Direct links use # followed by the physical slide number.

## 1. Agentic AI

This talk assumes the audience recognises files and tests, but has not used a coding agent. The invoice task is intentionally small so we can follow every stage.

## 2. One failing test, one bounded task

These are the checked-in fixture values. The 21% rate is a supplied teaching input, not advice about tax law. A passing result for this one input is only the first check.

## 3. Set the boundaries before you start

Show the actual workspace and permission settings. Keep approval prompts for anything outside the task. Do not use bypass mode for presentation convenience. A separate folder is convenient scoping; it is not a security sandbox.

## 4. Give it the outcome and the checks

Use the full prompt in examples/v2/invoice/README.md. Before the talk, copy before/ to a disposable directory. Start the agent here only after showing boundaries. Approve necessary actions deliberately. If a live run is unavailable, use the prepared checkpoints.

## 5. We will inspect four checkpoints

These are teaching checkpoints, not a promise that every agent takes the same path. If it finishes early, inspect the completed trace. If it stalls, switch to the prepared fixtures and say so.

## 6. The model chooses; the harness executes

Agent is the combined system when it iterates through a task. The model does not directly execute Python; the harness runs a tool. Harness is a useful term because it explains why the same model behaves differently in different products.

## 7. The agent repeats that exchange

Checkpoint: show a tool call from the live run, if available. Use the animation to connect the three parts; do not narrate a fictitious live result. Our failure output is the next slide.

## 8. Checkpoint 1 · the failure is evidence

Prepared fallback, validated from before/. The actual output also contains test names and tracebacks; this is an excerpt. Ask what the agent should read next. If live output differs, explain the difference rather than claiming it matches.

## 9. A tool call produces something inspectable

Show the file-read entry in the live trace or open before/invoice.py. Tool schemas and message formats vary across providers. The key is that the result—not the model’s claim that it read something—is the evidence.

## 10. Checkpoint 2 · the code explains the failure

The excerpt omits type annotations and the docstring to keep the slide readable. The full source is in before/invoice.py. The passing zero-rate case is consistent with this bug; the failing nonzero cases distinguish it.

## 11. Context is what the model can use now

Context is broader than the latest message. A product may retrieve or summarise previous material. Avoid saying every request literally includes every previous token or that the product has no persistent storage.

## 12. More information is not always more help

Do not teach a universal 40% or 50% threshold. The point at which performance suffers depends on the model, task and content. Missing a necessary file can be as harmful as loading too much irrelevant material.

## 13. When a session loses the thread

Explain compaction only as a summary that can omit details. Caching affects reused computation and billing; it does not restore omitted facts. Subagents are an optional advanced technique covered in later talks.

## 14. Thinking text is not verification

Reasoning can help a model tackle a task, but displayed summaries are not a faithful record of every internal cause. Keep the distinction practical: review evidence instead of accepting a confident explanation.

## 15. Checkpoint 3 · inspect the change

This slide isolates the conceptual change. The actual reference implementation names total only in after/. Check the real diff and confirm the rate comes from the argument. It must not simply return 121 or weaken the tests.

## 16. Checkpoint 4 · test more than the hook

Prepared result: python3 -m unittest test_invoice -v in after/. These cases verify the stated fixture behaviour, not all production financial requirements. The export tests in talk 03 are separate.

## 17. Passing tests are part of the review

Inspect the actual output from the live agent if present. The agent may report success while skipping a command or changing tests. The human reviewer decides whether the evidence is sufficient.

## 18. If it goes wrong, interrupt early

If changes are wrong, inspect a diff and use an understood checkpoint or restore a disposable copy. Do not suggest destructive reset commands that would remove unrelated work. A second identical retry without new evidence is often unhelpful.

## 19. Rules can survive a new session

Use the instruction file your harness reads: CLAUDE.md for Claude Code, AGENTS.md where supported. These are textual instructions, not an access-control boundary. Product memory may also retain notes; inspect what is actually loaded.

## 20. Put recurring procedures in a skill

A release checklist is a better skill example than another agent glossary. Describe a skill as instructions and optional supporting files. Exact loading and invocation are harness-specific. Plugin packaging belongs in a later talk.

## 21. Tools can reach outside the repo

MCP standardises part of the connection between assistants and external tools/data. It does not eliminate authentication or make arbitrary access safe. Our demo has no reason to connect to another system.

## 22. Start with one approved agent

This replaces the landscape tour. Model selection can wait until the audience can identify a task and evaluate its result. Tool availability and account features change; point to product documentation for setup.

## 23. Your first session, in five steps

Return to the opening task and ask the audience to explain each step. The five-step routine is the takeaway. Do not add another glossary or product comparison after it.

## 24. Try the fixture, then a task of your own

Questions and optional practice. The fixture is small enough to inspect fully. For a real task, choose work you already understand and can verify.

## 25. Reference · operating an agent

These are provider-specific references, not a claim that every harness behaves identically. Consult current documentation for exact controls.

## 26. Reference · context and evidence

The sources support the conceptual explanation. The fixture and prepared test results are local evidence, separate from provider claims.
