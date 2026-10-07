# Change log

## 2026-10-03 — Baseline and plan

- Created `improve/talk-clarity` from local main at `51f2e9a3479a864bf1901aa9c8e3bfa4961bcac0`.
- Recorded the nine-deck implementation backlog in `PLAN.md`.
- Existing `workshops/` files are outside the edit scope and remain untouched.
- Recorded the plan before editing the decks. No commit or publication performed.

## 2026-10-03 — Batch 1 complete

### Intro to Agentic AI

- `agentic-ai.html`: 43 → 26 slides. Kept one invoice example across the task, request, loop, project rules, skills and external-tool explanations.
- Moved the detailed glossary, product landscape and plan material into `agentic-ai-reference.html` (13 slides, including its cover and sources). Merged repeated memory, thinking and closing explanations.
- Replaced the fixed context-quality curve and contradictory 40–50% advice with task-specific symptoms and recovery choices. Distinguished compaction from caching, and fresh subagents from inherited/forked context.
- Clarified that a Git branch or folder is not a security boundary. Removed the unbounded live-demo instructions; the optional demo uses scoped permissions, with a clearly labelled illustrative invoice trace as a fallback.
- Updated speaker notes to match the shortened teaching sequence. Removed dependencies on the live task still running later in the talk.

### The AI Toolbox

- `ai-toolbox.html`: 57 → 31 slides. Leads with an illustrative quarterly-review workflow and organizes choices around task, output and review.
- Moved detailed vendor/model/plan grids and supporting examples into `ai-toolbox-reference.html` (22 slides, including its cover and sources).
- Shortened six tool categories to a representative task and practical review conditions. Reduced five stories to two in the main talk; replaced the science headline in reference material with a narrower description of hypothesis generation and experimental evidence.
- Replaced categorical claims about brand compliance, licensing and universal connector support with scoped explanations. Taught three integration routes: create a file, edit inside an app, or connect an external system.
- Merged the closing recaps and updated speaker notes.

### Shared presentation and documentation work

- Kept the Ember visual language and shared runtime/styles. Increased main-deck body/code reading sizes and gave new navigation links readable colours on both themes.
- Renumbered slides and removed obsolete numbered cross-references. Preserved source access and added main/reference return links.
- Fixed an existing initialization bug in the four revised outputs: a fresh deep link could show slide 1's presenter notes instead of the active slide's notes.
- Updated `README.md` and the first two chooser cards in `index.html`. Corrected stale counts, removed missing-file documentation, and documented the actual presenter shortcuts and optional-demo setup.
- Added an immutable baseline inventory, output hashes, a complete map of all 100 original slides, and a guarded migration script (`apply_batch1.py`). Removed content remains recoverable at the baseline commit.
- Reference decks explicitly retain their original July/September 2026 snapshot dates; this batch is not a current vendor-price or feature audit.

### Verification and remaining work

- Static checks pass for all four outputs, including local resources, numbering, notes, JavaScript syntax, IDs, manifest hashes and original-slide accounting.
- Browser checks pass for all 92 output slides at both 1280×720 and 1920×1080: 184 slide/viewport checks, no detected bounds violations or page exceptions. Navigation, deep links, notes, presenter popup, fullscreen and active-slide video readiness passed.
- Inspected representative screenshots covering code, card layouts, the close and reference material. Details and limits are in `VALIDATION.md`.
- The other seven decks and shared CSS/runtime match the baseline byte-for-byte. Plan D–J remains outstanding. Existing `workshops/` files were not edited. Nothing has been committed or published.

## 2026-10-03 — Follow-up: batches 2–3 complete

The user requested continuation through all seven remaining decks. All edits stay on `improve/talk-clarity`, uncommitted and unpublished. The four batch-1 deck outputs still match their recorded hashes. Shared runtime/styles and the pre-existing `workshops/` directory were not edited.

| Deck | Original main | Revised main | Optional reference |
|---|---:|---:|---:|
| Agentic Engineering | 60 | 30 | 10 |
| Subagents & Prompt Caching | 39 | 21 | 4 |
| Cost & Context | 28 | 17 | 4 |
| Orchestrating Agents | 32 | 19 | 4 |
| Measuring What Works | 31 | 19 | 5 |
| Claude Best Practices | 45 | 30 | 5 |
| Working Smarter with Agents | 83 | 44 | 8 |

### Agentic Engineering

- Retained the useful prediction, tool-loop, caching and helper animations plus the attention, sequence, context-growth and workflow diagrams. Shortened mechanics, reasoning and routing around one invoice task.
- Replaced an “ungameable” prompt and unbounded loop with a task contract, attempt limit, real acceptance cases, test-integrity review and enforced runtime-budget guidance.
- Separated input growth from billing. Added explicit cache-hit arithmetic ($0.0506 for the illustrative request versus $0.1228 without the hit), with cache-write and whole-task qualifications.
- Replaced the attention-derived “dumb zone” claim and brand hierarchy with contextual evidence, measured configurations and worker/reviewer roles.
- Kept one invoice skill system and moved arithmetic derivations, workflow pseudocode, learning links and publication recipes to reference.

### Subagents & Prompt Caching

- Consolidated helper analogies into a scoped local/cloud map and a delegation lifecycle. Distinguished fresh helpers from forks and required evidence-bearing returns.
- Corrected the single-call example: it did not implement a multi-turn, tool-using subagent. Replaced precise invented transcript statistics with an explicit illustration.
- Taught one shared-prefix example, TTL-sensitive break-even, eligible prior writes, usage inspection and warm-up before parallel reuse. Caching is not context reduction.
- Reconciled subscription/API framing against the current authentication documentation instead of equating unattended execution with a prohibited client.
- Migrated the bundled `x-dc` deck to the existing Ember renderer and presenter controls. This revised file uses the adjacent shared assets like the other decks; it is no longer the old self-contained bundle. The original bundle remains intact in the baseline commit.

### Cost & Context

- Replaced the purported real-session bill with transparent illustrative arithmetic. Removed the claim that output must dominate every bill.
- Put access-route requirements before detailed shopping questions; moved plan/cloud worksheets into reference and removed stale pricing chatter.
- Added before/after instruction content, a correctness-aware comparison procedure and a complete static worksheet. No savings are claimed without runs.

### Orchestrating Agents

- Followed one invoice ticket through ownership, bounded work and review. Separated coordination, edit isolation and actual filesystem/network containment.
- Paired failure modes with controls, and replaced product biographies with workflow requirements plus optional source links.
- Used one verification skill across project rules, procedures, tools and distribution. Replaced both empty demo fallbacks with usable static teaching material.
- Compared MCP and CLI by capability, discovery, errors and complete-task cost, including deferred loading. The former unmeasured case study is now a labelled experiment.

### Measuring What Works

- Defined four invoice acceptance cases, a grader, repeated trials and an explicit results worksheet. Synthetic A/B outputs can be graded without a provider account.
- Distinguished suspicious repetition from demonstrated waste, telemetry from transcripts, and observable output from hidden reasoning.
- Replaced model catalogues and unsupported hardware viability claims with a configuration worksheet and total-weight/KV-cache/offloading explanation.
- Removed the Hlas research TODO and all empty recording placeholders. Local-model and voice sections now have static exercises or measurement designs.

### Claude Best Practices

- Led and closed with three actions. Consolidated repeated gotchas and skill taxonomy into the invoice verification procedure.
- Scoped the retained Anthropic prompt-reduction report; reduced secondary benchmark statistics and qualified “low build, high verify” as a workflow to evaluate.
- Reconciled cache reuse with necessary corrections and escalation. Made evaluation, handoff and acceptance instructions concrete.
- Kept two delegation patterns; separated cost from containment. Explained HTML output by the decision it helps and hooks by the control they enforce.
- Retained article attribution, with the full original bibliography split across readable reference pages and command discovery linked to maintained documentation.

### Working Smarter workshop

- Reordered around measurement before optimization. Added a 210-minute agenda with timeboxes and participant deliverables.
- Reused the corrected companion-deck examples for cost, context, orchestration, skills and evaluation.
- Replaced all six empty recording fallbacks with static exercises: instruction comparison, ticket lifecycle, skill file, grading worksheet, hardware reasoning and voice transcription.
- Added `exercise-materials.md` with synthetic CSV fixtures, facilitator answers, instruction variants, acceptance criteria and a trial worksheet. Optional live runs still require a prepared repository, approved access and rehearsal; the static route is complete.

### Tracking, navigation and validation

- Updated README and all seven relevant chooser destinations; added the previously absent workshop card. Each revised main deck links to its reference deck, with a return link.
- Added guarded, reproducible migrations and per-batch hashes/maps. The complete map accounts for all 418 original slides. Total revised main slides: 237; optional reference slides: 75.
- All 18 deck outputs pass current static validation; the seven follow-up main/reference pairs pass 440 slide/viewport checks at 1280×720 and 1920×1080. Representative screenshots reviewed. See `VALIDATION.md` for methods and limits.
