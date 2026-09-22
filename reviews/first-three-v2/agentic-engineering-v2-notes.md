# Agentic Engineering — v2 speaker notes

Navigation: arrows / Space; Home / End; N notes; P presenter window; F fullscreen. Direct links use # followed by the physical slide number.

## 1. Agentic Engineering

Assume the audience knows model, harness, tools and context from talk 02. This talk asks how to make the process repeatable. Keep the original evolution structure, but let each chapter solve an engineering failure.

## 2. A passing demo is only the beginning

The goal is not maximum autonomy. It is work that can be accepted with evidence and recovered when it fails. Distinguish repeatable workflows from one successful transcript.

## 3. Keep one example throughout

This is an excerpt from the reference CSV. The complete file also exercises a newline in a customer name. Our implementation assumes validated rows; production validation and spreadsheet formula handling are separate requirements.

## 4. Recap: the system you are engineering

Compress the original prediction, thinking, tools and statelessness chapters to this recap. We can change what information the system receives, what actions it may take and how results are checked.

## 5. Problem 1 · “Add export” leaves too much open

Ask the audience what they would need to review an export. The missing information is a contract problem before it is a model problem. Do not respond to ambiguity by increasing reasoning effort.

## 6. Write the acceptance contract first

These are the requirements implemented by the checked-in reference fixture. For the talk, the set is deliberately small and testable. Label omitted production requirements rather than implying this is a complete billing system.

## 7. Decide how much structure the task needs

This is a design choice, not a maturity ladder. A workflow may contain agent-driven stages. Use the simplest approach that can meet the contract and explain its result.

## 8. Make the stages and ownership visible

This is the workflow for our example. Keep a named owner for integration and acceptance. The next slides show how evidence and recovery change what happens at the gates.

## 9. Problem 2 · a green command can mislead

An exit code is an observation. It does not prove the tests cover the contract. The original deck said a goal prompt could not be gamed; replace that guarantee with independent checks and review.

## 10. Give every claim a check

The reference test includes a comma, embedded quotes and a newline. Parsing with the CSV reader tests serialization rather than eyeballing a text file. Formula-like input remains outside this fixture’s contract.

## 11. Keep the calculation outside the guesswork

Use deterministic code for a specified calculation. Let the agent inspect and change the implementation, but verify against the explicit rounding rule. This is the existing calculation from the reference fix, reused by the exporter.

## 12. Inspect both tests and the artifact

Prepared reference result from after/: three invoice tests and two export tests. The CSV is generated with the same implementation and parsed in validation. This is not a benchmark or a captured agent run.

## 13. Keep acceptance separate from implementation

Another model can help review but can share the same blind spots. Protect important acceptance checks outside the implementation’s control when warranted. Human review still owns the decision for this workflow.

## 14. Problem 3 · the useful facts get buried

Preserve the original context thread without treating attention as a simple fixed budget divided equally between tokens. More irrelevant material can harm retrieval and distract the model; exact behaviour varies.

## 15. Give each stage the context it needs

The table is our proposed design, not an automatic feature of every harness. Fresh stages must receive enough context to preserve decisions. A short handoff is only useful if it contains the necessary facts.

## 16. Store decisions before restarting

This is a handoff example for the reference fixture. Keep file references and unresolved scope, not pages of tool output. A new session should verify the handoff against the files rather than trusting it blindly.

## 17. Caching and compaction solve different problems

Billing rules, cache lifetimes and treatment of reasoning vary by provider and model. Avoid the original blanket claims about byte-identical requests, perpetual warm caches or thinking always being retained/stripped. Detailed mechanics belong in talk 04.

## 18. Problem 4 · retries consume the budget

Do not let a retry loop keep editing indefinitely. Distinguish transient tool failure, misunderstanding and an unmet requirement. Each calls for a different response.

## 19. Set a retry policy before the run

This is a policy sketch, not a provider command. Choose numeric limits for the real environment. A stop should preserve useful evidence and never imply the task succeeded.

## 20. Recovery starts with an inspectable boundary

A branch or worktree isolates edits, not credentials or network access. Use environment isolation separately when needed. Never blindly reset a shared dirty workspace; preserve unrelated changes.

## 21. Problem 5 · cheap tokens can buy costly work

Do not claim stronger or smaller models are always cheaper. Compare the total process on representative tasks and hold acceptance criteria constant. Subscription limits and API charges are different meters.

## 22. Compare accepted work, not headline rates

Hypothetical arithmetic, not measured model performance. Both spend one dollar per accepted task, but B accepts more of the batch and uses less review time. Track failures, latency and human effort separately rather than collapsing them into one misleading number.

## 23. Change one dial and measure again

The set should include common tasks and failure-prone cases. Repeat enough to see variability. Re-evaluate after meaningful model, prompt or tool changes; do not teach a permanent ranking of named tiers.

## 24. Problem 6 · one agent carries too much

Delegation may help when investigation is separable or parallelism saves time. It adds coordination, context handoff and cost. It is not required for this small export fixture. The animation’s 80k/200 token counts are illustrative, not measurements of this example.

## 25. Delegate an outcome with a boundary

This is a reviewer brief for the same example, not an instruction to spawn agents during this revision. Findings must be checked before acting. A short conclusion without evidence is not enough.

## 26. Parallel work still needs integration

Independent read-only reviews are easier to combine than concurrent edits to the same files. Use worktrees for independent edits when appropriate; a shared test run on the integrated result still matters.

## 27. Problem 7 · useful lessons disappear

Avoid turning every solved task into permanent context. Retain what will change future behaviour and periodically remove stale instructions. Plugin distribution is a later concern.

## 28. Write one small procedure people can inspect

This is an example skill body rather than a full provider-specific package. Keep the procedure readable and useful before distributing it. It does not itself enforce permissions or guarantee a complete review.

## 29. The complete workflow has a way back

Trace the invoice export once through the workflow. Return to the relevant stage when new evidence invalidates a decision. On budget exhaustion, preserve a partial result and mark it incomplete. Success is reviewed evidence against a contract.

## 30. Improve one workflow this week

This is the single closing action. Encourage a small change to an existing workflow before adding fleets of agents or a plugin marketplace.

## 31. Go deeper where your work needs it

Questions here. The later decks are existing editions, not revised as part of this work. They retain their own date stamps and some are work in progress. Do not imply their product claims were revalidated in this revision.

## 32. Reference · workflows and evaluation

These sources support the design distinctions. The workflow, retry table and illustrative comparison are teaching designs, not measured production outcomes. Detailed evidence and validation are recorded with this edition.
