# Talk clarity improvement plan

Status: all nine main decks revised; clarity implementation complete. Updated: 2026-10-03.

Completed: A–J and validation for all revised outputs. Optional live-demo rehearsals remain preparation work, not required for the static teaching paths. See [CHANGES.md](CHANGES.md) for implemented work and [VALIDATION.md](VALIDATION.md) for evidence and limits.

| Batch | Deck | Before | Main now | Optional reference | Status |
|---|---|---:|---:|---:|---|
| 1 | Intro to Agentic AI | 43 | 26 | 13 | Complete |
| 1 | The AI Toolbox | 57 | 31 | 22 | Complete |
| 2 | Agentic Engineering | 60 | 30 | 10 | Complete |
| 3 | Subagents & Prompt Caching | 39 | 21 | 4 | Complete |
| 3 | Cost & Context | 28 | 17 | 4 | Complete |
| 3 | Orchestrating Agents | 32 | 19 | 4 | Complete |
| 3 | Measuring What Works | 31 | 19 | 5 | Complete |
| 3 | Claude Best Practices | 45 | 30 | 5 | Complete |
| 3 | Working Smarter with Agents | 83 | 44 | 8 | Complete |

Counts include covers and source slides. Reference decks have their own covers and duplicate source access. Original positions are mapped in [SLIDE-MAP.md](SLIDE-MAP.md). Work-package slide numbers below refer to the original baseline.

## Scope and baseline

- Branch: `improve/talk-clarity`.
- Baseline: `51f2e9a3479a864bf1901aa9c8e3bfa4961bcac0` (local `main` when work began).
- Nine decks, 418 slides reviewed. Review numbers count every section, including titles and dividers; printed numbers can differ.
- Preserve the Ember visual language, useful diagrams/animations, source attribution, presenter controls, and speaker notes. Rewrite notes when the teaching sequence changes.
- Preserve the pre-existing untracked `workshops/` directory. Do not stage, delete, or modify it.
- Work is local. No publication, push, merge, or production action is included.
- Original slide content remains recoverable from the baseline commit. Record original-to-current positions and the disposition of removed slides.
- Never invent measured results or demo recordings. Missing evidence becomes an explicitly labelled exercise or a documented rehearsal prerequisite.

## Editorial approach

One teaching slide should have one main claim, one example, and one useful consequence. Move catalogues, installation recipes, and secondary evidence into reference material. Retain necessary qualifications beside claims. Keep standalone talks understandable without requiring attendance at earlier talks.

## Work packages

### A. Foundation and tracking

- [x] Inspect working tree and create the requested branch.
- [x] Record baseline, scope, preservation constraints, and this plan before editing decks.
- [x] Add a slide inventory/map and reproducible content-editing workflow.
- [x] Record each implemented batch in `CHANGES.md`; record verification and limitations in `VALIDATION.md`.

### B. Intro to Agentic AI (43 slides)

- [x] Reduce slides 17–27 to a short interface/usage choice; retain detailed landscape material as reference.
- [x] Merge repeated architecture and memory explanations (6–11, 35); introduce vocabulary as needed.
- [x] Use the invoice example throughout, including skills and external tools (36–39).
- [x] Make demo callbacks usable after the live task has finished (4, 12, 14, 30, 33).
- [x] Simplify thinking (14–15) and replace the contradictory 40–50% context rule (29–30).
- [x] Clarify permission boundaries (33–34), distinguish fresh subagents from forks (32), and merge the closing slides (40–41).

### C. The AI Toolbox (57 slides)

- [x] Organize the opening around audience tasks; lead with the deck-building example (22–23).
- [x] Compress foundations and remove the upfront glossary/model catalogue from the spoken path (4–11).
- [x] Consolidate vendor families/pricing (12–20); keep practical choices, move detailed grids to reference.
- [x] Reduce the category catalogue (27–39) to representative examples with task, output, and review condition.
- [x] Keep two relevant stories; integrate them with their lesson (41–45). Correct the science headline wherever retained.
- [x] Teach file creation, in-app editing, and external connections as three routes (47–53).
- [x] Remove unsupported absolutes, merge the close (54–55), and retain source access.

### D. Agentic Engineering (60 slides)

- [x] Compress predictor/attention/reasoning setup (5–12) and repeated harness/payload mechanics (14–18).
- [x] Prioritize verifiers and bounded loops (20–25); remove claims that prompts cannot be gamed.
- [x] Merge context-growth examples, distinguish input volume from billed cost, and fix the cost arithmetic (27–33).
- [x] Replace the oversimplified attention explanation (34).
- [x] Reduce model-specific routing material (37–45) to measurement, role assignment, and escalation.
- [x] Keep one workflow and one skill-system example; move publication recipes to reference (46–58).
- [x] End with durable engineering practices (59).

### E. Subagents & Prompt Caching (39 slides)

- [x] Consolidate repeated helper/context explanations (4–8); preserve the local/cloud map.
- [x] Rename the delegation lifecycle, distinguish fresh contexts from forks, and show a return contract (9–13).
- [x] Correct the single-call code example's scope (16); trim the sample transcript (17).
- [x] Consolidate cache explanations around a shared example (19–26).
- [x] Explain TTL-dependent break-even, warm-up before concurrent reuse, and cache limits (27–33).
- [x] Resolve the subscription-framing contradiction with scoped, dated guidance (35–37).
- [x] Close with isolation versus reuse, not a claim that caching reduces context (39).

### F. Cost & Context (28 slides)

- [x] Replace the purported measured bill with an honest worked example or a real supplied trace (4–6).
- [x] Lead plan selection with the decision, remove research chatter, move detailed grids to reference (7–13).
- [x] Combine repeated context explanations and demonstrate a before/after instruction file (15–20).
- [x] Make the comparison exercise assess correctness as well as tokens (24).
- [x] Replace the empty fallback with useful static teaching material; merge the recaps (25–27).

### G. Orchestrating Agents (32 slides)

- [x] Separate coordination from isolation (4, 10–11).
- [x] Lead with workflow choices, use one ticket lifecycle, and reduce product biographies (5–8, 15).
- [x] Give each failure mode a concrete control (12–14).
- [x] Use one example for rules, skills, tools, and distribution (17–21).
- [x] Consolidate MCP/CLI comparison, represent deferred loading fairly, avoid absolute heuristics (25–29).
- [x] Replace the unmeasured case study with a clearly labelled exercise (30), unless actual evidence becomes available.
- [x] Replace empty fallbacks (9, 23).

### H. Measuring What Works (31 slides)

- [x] Teach evaluation through one task, separating test cases, graders, and repeated-run metrics (4–7).
- [x] Annotate a trace; distinguish suspicious repetition from proven waste and telemetry from hidden reasoning (8–10).
- [x] Provide a concrete rubric/results worksheet; label sample results if illustrative (11–13).
- [x] Replace the model catalogue with measurement-driven configuration choices; move specifications to reference (14–25).
- [x] Correct active-parameter/RAM reasoning and make local hardware claims conditional on measurement (20–22).
- [x] Remove the visible Hlas research TODO, replace empty fallbacks, and close with an evaluation action (27–30).

### I. Claude Best Practices (45 slides)

- [x] Prioritize the opening/closing actions (2, 44) and remove duplicate gotcha examples (6, 10).
- [x] Replace category lists with one verification-skill example (5, 9, 11–12).
- [x] Simplify cache economics and reconcile absolute cache rules with escalation (15–17, 22).
- [x] Simplify effort comparisons and clearly distinguish comparison settings (19–23).
- [x] Reduce secondary statistics; make verification and evaluation instructions concrete (25–29).
- [x] Separate autonomy/handoff templates from delegation examples (31–32).
- [x] Teach two multi-agent patterns; separate cost from containment (36–38).
- [x] Reduce tool-history examples, show the purpose of HTML output, and focus mods on an outcome (40–42).
- [x] Keep commands and source details as reference (43, 45).

### J. Working Smarter workshop (83 slides)

- [x] Apply corresponding corrections from F–H consistently to duplicated material.
- [x] Put participant outputs and timeboxes on the agenda; introduce measurement before optimization.
- [x] Convert context, skill, orchestration and eval demos into exercises with acceptance checks.
- [x] Move alternative-model catalogues to optional reference material.
- [x] Replace six empty fallbacks; label measured versus illustrative evidence honestly.

### K. Series documentation and validation

The checks below now cover all nine revised talks and their reference decks. Batch 1 has its original 184 checks; the remaining seven have 440 checks. See VALIDATION.md for exact evidence and limits.

- [x] Synchronize README and chooser descriptions/counts with actual files; remove missing `claude-design.html` and `deck05-facts.md` references.
- [x] Repair slide numbering and internal slide references after reordering.
- [x] Validate HTML structure, local links/media, unique IDs, speaker notes, script syntax, and whitespace.
- [x] Browser-check 1280×720 and 1920×1080 where tooling is available: content bounds, navigation, notes, media and console errors.
- [x] Inspect representative screenshots at presentation size. Static checks alone do not establish visual quality.
- [x] Record remaining work and evidence gaps explicitly; never mark unperformed checks complete.

## Completion rules

Update checkboxes only when the corresponding work is implemented and reviewed. A batch entry must name the files, old/new slide disposition, substantive corrections, and checks run. Keep missing live evidence and unavailable visual validation visible in the plan and validation report.
