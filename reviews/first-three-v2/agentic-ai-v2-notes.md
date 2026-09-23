# Agentic AI · v2 speaker notes

Navigation: arrows / Space; Home / End; N notes; P presenter window; F fullscreen. Direct links use # followed by the physical slide number.

## 1. Agentic AI

The audience knows files and tests but has not used a coding agent. The invoice task is small on purpose, so you can follow every step in front of them.

## 2. One failing test, one bounded task

These values come from the checked-in fixture. The 21% rate is a teaching input, not tax advice. Getting this one input right is only the first check.

## 3. Set the boundaries before you start

Show the real workspace and permission settings. Leave approval prompts on for anything outside the task, and do not switch to bypass mode to save time on stage. A separate folder keeps the work scoped, but it is not a security sandbox.

## 4. Give it the outcome and the checks

The full prompt is in examples/v2/invoice/README.md. Before the talk, copy before/ to a throwaway directory. Start the agent now, after the boundaries slide, and read each approval request before you accept it. If you cannot run live, use the prepared checkpoints.

## 5. Four places to stop and look

We chose these four stops for teaching; a real agent may take a different path. If it finishes early, walk through the completed trace. If it stalls, switch to the prepared fixtures and tell the audience you have switched.

## 6. The model chooses; the harness executes

The agent is the two together, iterating on a task. The model never runs Python itself: it asks, and the harness runs the tool. The word harness earns its place because it explains why the same model behaves differently in different products.

## 7. The agent repeats that exchange

If the live run has made a tool call, show it now. Use the animation to connect model, harness and tool, and describe only what it shows; do not narrate an imagined live result. The failure output comes next.

## 8. Checkpoint 1 · the failure is evidence

This is the prepared fallback, run from before/. The real output also has test names and tracebacks; the slide shows an excerpt. Ask the room what the agent should read next. If the live output differs, say how, rather than claiming it matches.

## 9. A tool call leaves something you can inspect

Show the file-read entry in the live trace, or open before/invoice.py. Providers format tool calls differently. The evidence is the result the harness returned; the model saying it read the file proves nothing.

## 10. Checkpoint 2 · the code explains the failure

The excerpt drops the type annotations and docstring; the full source is in before/invoice.py. A zero rate changes nothing, so that test passes even with the bug. The two nonzero cases fail, and that pattern points at the unused tax_rate.

## 11. Context is what the model can use now

Context covers more than the latest message. Products may retrieve or summarise earlier material, so do not say every request resends every previous token, or that the product stores nothing between turns.

## 12. Too much context hides what matters

There is no universal 40% or 50% threshold. When quality drops depends on the model, the task and the content. Leaving out a file the agent needs can hurt as much as loading material it does not.

## 13. When a session loses the thread

Describe compaction as a summary that can drop details, and go no further. Caching changes reused computation and billing; it will not bring back a dropped fact. Subagents come up in talks 03 and 04, so skip them here.

## 14. Verify against evidence, whatever the reasoning says

Reasoning can help the model with the task, but the text you see is not a faithful record of why it acted; Anthropic’s research on reasoning reports found models leave things out. Keep it practical: review the evidence and do not accept a confident explanation in its place.

## 15. Checkpoint 3 · inspect the change

A simplified diff: before/ has no total variable, which only appears in after/invoice.py. Open the real diff and confirm the rate comes from the argument. A fix that hard-codes 121 or weakens the tests fails review.

## 16. Checkpoint 4 · check more than one case

Prepared result from running python3 -m unittest test_invoice -v in after/. The three cases cover the fixture’s stated behaviour, which falls well short of real billing rules. The export tests belong to talk 03.

## 17. Passing tests are part of the review

If you ran live, open the agent’s real output. An agent can report success after skipping a command or editing a test. You, the reviewer, decide whether the evidence is enough.

## 18. If it goes wrong, interrupt early

If the changes are wrong, read the diff, then go back to a checkpoint you understand or restore the throwaway copy. Do not reach for a reset command that could wipe unrelated work. Retrying the same prompt with no new information rarely helps.

## 19. Rules in a file load into every session

Use the file your harness reads: CLAUDE.md for Claude Code, AGENTS.md for tools that support it. The model reads these instructions, but they do not enforce access. Some products also keep memory notes, so check what gets loaded.

## 20. Put recurring procedures in a skill

A release checklist makes a good example. A skill is a set of instructions, with supporting files if it needs them. How it loads and gets invoked depends on the harness. Leave plugin packaging for a later talk.

## 21. Tools can reach outside the repo

MCP standardises part of how assistants connect to outside tools and data. You still need authentication, and connecting a system does not make access to it safe. Our demo has no reason to reach outside the repo.

## 22. Start with one approved agent

Model choice can wait until people can pick a task and judge the result. Availability and account features change, so send people to the product documentation for setup.

## 23. Your first session, in five steps

Go back to the invoice task and ask the room to match each step to what the agent did. This routine is the takeaway; stop teaching after it.

## 24. Try the fixture, then a task of your own

Take questions. The fixture is small enough to read end to end. For a first real task, pick work you already understand and can check.

## 25. Reference · operating an agent

These are Claude Code documents; other harnesses differ. Check the current documentation for exact controls.

## 26. Reference · context and evidence

Sources for the concepts in this talk. The fixture and its test results are our own evidence and say nothing about any provider.
