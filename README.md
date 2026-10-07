# Agentic talks

Zero-build HTML slide decks — a general-audience tool landscape, a beginner
intro to agentic AI, a developer follow-up, engineering deep dives, a workshop
on working smarter with agents. Same
template, same aesthetic. The
key concepts are illustrated by short looping animations rendered with
[Remotion](https://www.remotion.dev/) (in `assets/anim/`, sources in `remotion/`),
so keep those folders next to the `.html` files.

Author: **David Budáč** · English

- **[`ai-toolbox.html`](ai-toolbox.html)** — *The AI Toolbox* (no coding background
  assumed). Choose a task → inspect an editable result → compare workflows → check
  rights, data and costs → work inside files and connected apps. **31 slides**, no
  live demo. [Optional reference deck](ai-toolbox-reference.html): **22 slides**,
  retaining the July 2026 product/pricing snapshot; verify details before reuse.
- **[`agentic-ai.html`](agentic-ai.html)** — *Intro to Agentic AI* (developers new
  to agents). One invoice example connects the model/harness loop, context,
  permissions, project rules, skills and tools. **26 slides**, optional bounded
  demo with an illustrative trace as the teaching alternative.
  [Optional reference deck](agentic-ai-reference.html): **13 slides**, including
  terminology and the September 2026 product/pricing snapshot.
- **[Agentic Engineering](agentic-engineering.html)** — Model and harness mechanics, bounded verification loops, worked cost arithmetic, context, delegation and reusable checks. **30 slides**.
  [Optional reference](agentic-engineering-reference.html): **10 slides**. No live run required.
- **[Subagents & Prompt Caching](subagents-prompt-caching.html)** — Fresh helpers versus forks, evidence-bearing returns, local/cloud boundaries, cache eligibility, warm-up and break-even arithmetic. **21 slides**.
  [Optional reference](subagents-prompt-caching-reference.html): **4 slides**. No live run required.
- **[Cost & Context](cost-and-context.html)** — A worked bill, access-route decisions, a before/after instruction file and an exercise that checks correctness as well as usage. **17 slides**.
  [Optional reference](cost-and-context-reference.html): **4 slides**. No live run required.
- **[Orchestrating Agents](orchestrating-agents.html)** — One ticket lifecycle, coordination versus containment, verification skills and an MCP/CLI comparison exercise. **19 slides**.
  [Optional reference](orchestrating-agents-reference.html): **4 slides**. No live run required.
- **[Measuring What Works](measuring-what-works.html)** — Invoice acceptance cases, graders, repeated trials, trace interpretation, a scoring worksheet and measured hardware choices. **19 slides**.
  [Optional reference](measuring-what-works-reference.html): **5 slides**. No live run required.
- **[Claude Best Practices](best-practices.html)** — Applied lessons from Anthropic engineering posts: instruction audits, verification skills, cache tradeoffs, measured effort and two delegation patterns. **30 slides**.
  [Optional reference](best-practices-reference.html): **5 slides**. No live run required.
- **[Working Smarter with Agents](working-smarter.html)** — A 210-minute workshop with timeboxes, participant outputs and self-contained invoice exercises. Optional live execution has explicit preparation requirements. **44 slides**.
  [Optional reference](working-smarter-reference.html): **8 slides**. Static exercises work without paid accounts.

## View it

- **Locally:** open any `.html` deck in a modern browser (macOS:
  `open index.html` opens the chooser). `index.html` routes the reader to the
  right deck by audience — non-technical (01) → developers new to agents (02) →
  developers going deeper (03) → devs & IT admins on internals (04) → devs
  levelling up on cost, orchestration & measurement (05–07) → daily Claude Code
  users who want Anthropic's own practices (08, Claude Best Practices) — with
  self-identification bullets per deck and a
  one-question fallback for the undecided.
- **Online:** if GitHub Pages is enabled, the repo's Pages root serves the chooser.

## Navigate

- **Keyboard:** `↑` `↓` / `←` `→` / `Space` / `PageUp` `PageDown` / `Home` `End`
- **Touch:** swipe up/down
- **Mouse:** scroll, or click the nav dots on the right

## Presenter controls

The Ember stage scales a fixed 1920×1080 canvas to the available viewport.
Use **N** for speaker notes, **P** for the presenter window, **F** for fullscreen,
and **R** to return to the first slide. A URL ending in `#3` opens slide 3.
The main decks link to their optional reference decks from the closing slide.

## What's covered

**The AI Toolbox** — an illustrative quarterly-review workflow · choosing by
output · subscriptions and credits · representative examples for apps, video,
voice, images and automation · review checkpoints · two real-world stories ·
three integration routes: create a file, edit inside an app, connect another system.

**Intro to Agentic AI** — an illustrative invoice fix · model / harness / agent ·
tool calls · reasoning and verification · useful context, caching and compaction ·
fresh subagents versus forks · permissions · project rules, skills and external tools.

**Agentic Engineering** — Model and harness mechanics, bounded verification loops, worked cost arithmetic, context, delegation and reusable checks.

**Subagents & Prompt Caching** — Fresh helpers versus forks, evidence-bearing returns, local/cloud boundaries, cache eligibility, warm-up and break-even arithmetic.

**Cost & Context** — A worked bill, access-route decisions, a before/after instruction file and an exercise that checks correctness as well as usage.

**Orchestrating Agents** — One ticket lifecycle, coordination versus containment, verification skills and an MCP/CLI comparison exercise.

**Measuring What Works** — Invoice acceptance cases, graders, repeated trials, trace interpretation, a scoring worksheet and measured hardware choices.

**Claude Best Practices** — Applied lessons from Anthropic engineering posts: instruction audits, verification skills, cache tradeoffs, measured effort and two delegation patterns.

**Working Smarter with Agents** — A 210-minute workshop with timeboxes, participant outputs and self-contained invoice exercises. Optional live execution has explicit preparation requirements.

## Optional beginner demo

Use a prepared, disposable invoice project with scoped file and command access.
Show a failing test, ask for a bounded fix, then inspect the final test output and
diff. Keep relevant permission prompts enabled. The adjacent illustrative trace
can teach the same sequence if a live run is unavailable; it is not a recording or
benchmark result. Later discussion can use the completed transcript.

## Improvement work

The clarity revision is tracked in
[the implementation plan](reviews/2026-10-03-clarity/PLAN.md),
[change log](reviews/2026-10-03-clarity/CHANGES.md),
[slide map](reviews/2026-10-03-clarity/SLIDE-MAP.md), and
[validation record](reviews/2026-10-03-clarity/VALIDATION.md).
All nine main decks and their reference decks have completed the clarity pass.
The workshop and deep dives share [exercise materials](reviews/2026-10-03-clarity/exercise-materials.md).
Work remains local and uncommitted. No live provider benchmark is implied.

## Concept animations (Remotion)

The most important concepts are animated with Remotion; the decks embed the
rendered MP4s as muted loops that restart whenever you land on their slide:

| Animation | Concept | Used on |
|-----------|---------|---------|
| `agent-loop` | model proposes, harness runs, result returns | toolbox, intro, engineering |
| `stateless` | conceptual request-history illustration | toolbox; original asset retained |
| `next-token` | sampled next-token prediction | engineering |
| `kv-cache` | matching-prefix reuse; on-slide caveats qualify the price label | engineering, subagents |
| `subagents` | intermediate work stays in a helper context | intro, engineering, subagents, cost, workshop |
| `quality` | original fixed quality curve | retained asset; omitted from revised teaching paths |
| `context-lifecycle` | original context stack | retained asset; revised talks use scoped examples |
| `progressive-disclosure` | loading supporting instructions when needed | retained asset; revised talks use the invoice skill |

To tweak or re-render: `cd remotion && npm i`, then `npx remotion studio` to
preview or `npx remotion render <composition-id> ../assets/anim/<id>.mp4` to
re-export (composition ids are listed in `remotion/src/Root.tsx`; each exists
in the deck's light/dark theme variant as needed).

## Customize

All styling is driven by CSS variables in the `:root` block of `agentic-ai.html`
(Ember color tokens and `--font-*` set the palette and typography). The Remotion
animations read the same palette from `remotion/src/theme.ts`.

## Notes

- Product claims have different snapshot dates across the series. The October
  clarity edit is not a full refresh of vendor features or prices. Check primary
  sources before quoting historical product details or planning a live demo.

## Files

| File | Purpose |
|------|---------|
| `ai-toolbox.html` | *The AI Toolbox* deck — tool landscape for everyone (no live demo). |
| `agentic-ai.html` | *Intro to Agentic AI* deck — beginners. |
| `agentic-engineering.html` | Agentic Engineering — 30 slides; optional reference has 10. |
| `subagents-prompt-caching.html` | Subagents & Prompt Caching — 21 slides; optional reference has 4. |
| `working-smarter.html` | Working Smarter with Agents — 44 slides; optional reference has 8. |
| `best-practices.html` | Claude Best Practices — 30 slides; optional reference has 5. |
| `ai-toolbox-reference.html` | Optional toolbox catalogue and supporting examples; July 2026 snapshot. |
| `agentic-ai-reference.html` | Optional terminology and product details; September 2026 snapshot. |
| `cost-and-context.html` | Cost & Context — 17 slides; optional reference has 4. |
| `orchestrating-agents.html` | Orchestrating Agents — 19 slides; optional reference has 4. |
| `measuring-what-works.html` | Measuring What Works — 19 slides; optional reference has 5. |
| `agentic-engineering-reference.html` | Optional supporting material for Agentic Engineering. |
| `subagents-prompt-caching-reference.html` | Optional supporting material for Subagents & Prompt Caching. |
| `cost-and-context-reference.html` | Optional supporting material for Cost & Context. |
| `orchestrating-agents-reference.html` | Optional supporting material for Orchestrating Agents. |
| `measuring-what-works-reference.html` | Optional supporting material for Measuring What Works. |
| `best-practices-reference.html` | Optional supporting material for Claude Best Practices. |
| `working-smarter-reference.html` | Optional supporting material for Working Smarter with Agents. |
| `index.html` | Landing page routing readers to the right deck by audience (GitHub Pages root). |
| `assets/anim/` | Rendered concept animations (MP4 loops) embedded by the decks. |
| `remotion/` | Remotion project — sources for the animations. |
