# Agentic talks

Zero-build HTML slide decks — a general-audience tool landscape, a beginner
intro to agentic AI, a developer follow-up, engineering deep dives, a workshop
on working smarter with agents, a Claude Design product tour, a graph
engineering deep dive, and a hands-on evals workshop. Same
template, same aesthetic. The
key concepts are illustrated by short looping animations rendered with
[Remotion](https://www.remotion.dev/) (in `assets/anim/`, sources in `remotion/`),
so keep those folders next to the `.html` files.

Author: **David Budáč** · English

- **[`ai-toolbox.html`](ai-toolbox.html)** — *The AI Toolbox* (a field guide for
  everyone — no coding background assumed). The big three labs (Claude app / Code /
  Cowork / Design, ChatGPT / Codex, Gemini / Notebook / Flow) → what agents can do →
  the wider tool landscape by category (app builders, video, HyperFrames, avatars,
  voice, music, images, decks, copy, research, automation) → five real-world stories →
  plugging AI into Excel / PowerPoint & co. (connectors, MCP). Pricing runs through
  every tool slide (September 2026 snapshot). 59 slides. **No live demos.**
- **[`agentic-ai.html`](agentic-ai.html)** — *Intro to Agentic AI* (Claude Code for
  beginners). Model / harness / agent, the loop, context, permissions, memory & MCP. 43 slides.
- **[`agentic-engineering.html`](agentic-engineering.html)** — *Agentic Engineering*
  (basics for developers). Told as an evolution story — each chapter fixes the previous
  one's limitation: the predictor → thinking → hands (tool calls) → the loop → the bill
  → split the work (routing & subagents) → make it stick (CLAUDE.md, skills, plugins).
  One thread throughout: the context window. 60 slides. **No live demos.**
- **[`subagents-prompt-caching.html`](subagents-prompt-caching.html)** — *Subagents &
  Prompt Caching* (engineering deep dive, for developers & IT admins). Subagent
  architecture and the four context crossings → parallel fan-out and its integration
  constraint → the caching mechanism (exact-match prefixes, breakpoints, TTL & eviction)
  and its economics → where the two reinforce each other → what's allowed under a
  subscription vs an API key. 41 slides, ~30 min. **No live demos.**
- **[`cost-and-context.html`](cost-and-context.html)** — *Cost & Context* (WIP,
  ~30-min deep dive, for engineers already running Claude Code daily). What
  agents really cost — three pricing meters, subscriptions vs API vs Bedrock,
  a which-plan-for-which-team table → efficient work with context: the context
  lifecycle, CLAUDE.md hygiene, `/doctor`, `/clear` vs `/compact`. 29 slides.
  **Live bloated-vs-lean demo.**
- **[`orchestrating-agents.html`](orchestrating-agents.html)** — *Orchestrating
  Agents* (WIP, ~30-min deep dive, for experienced devs). A map of the
  orchestration ecosystem (dashboards, worktrees, backlog-driven fleets) → the
  three failure modes of parallel agents → sandboxing before unattended runs →
  skills & plugins for teams and a per-capability MCP-vs-CLI heuristic. 32 slides.
- **[`measuring-what-works.html`](measuring-what-works.html)** — *Measuring What
  Works* (WIP, ~30-min deep dive, for experienced devs). A minimal eval loop you
  can start this week → pass^k, smevals and cost per accepted task to pick a
  model → reading traces for wasted turns and real cost, with the OTel GenAI
  span anatomy. 21 slides. **Live eval demo.** Doubles as the teaser for the
  half-day evals workshop (`workshops/evals/`), whose Lab 6 takes over routing,
  harnesses and open models.
- **[`evals-workshop.html`](evals-workshop.html)**: *Evals, Hands On* (WIP until
  the dry run; half-day hands-on workshop for about 20 Java developers in
  pairs, each on their own Claude Code Pro or Max plan). The practical side of
  talk 07: eight labs on one Java/Maven repo. Setup check, then guess and measure
  (lean vs bloated CLAUDE.md), variance with pass@k and pass^k, break and harden
  a grader, read the traces, test a judge model against people, route Haiku vs
  Sonnet by cost per accepted task, and take an eval home. Results pool on a
  live room board. 50 slides with a lab tracker in every header, a time box on
  every "Do this" slide (**T** starts or pauses it) and facilitator notes on
  every slide. Everything else lives in [`workshops/evals/`](workshops/evals/):
  the lab kit (`lab/`), the facilitator run sheet
  ([`FACILITATOR.md`](workshops/evals/FACILITATOR.md)), the participant sheet
  ([`HANDOUT.md`](workshops/evals/HANDOUT.md)) and the board source (`board/`).
- **[`claude-design.html`](claude-design.html)** — *Claude Design* (WIP,
  ~30-min product deep dive, no code or design background needed — any paid
  Claude plan). The full tour behind deck 01's two teaser slides: the
  chat-and-canvas interface, four starting points, the design-system/brand
  feature (`/design-sync`), plans & shared usage → the craft (the iteration
  loop, briefing, the three refinement channels, example briefs to steal, a
  live five-minute build, pitfalls) → sharing, exports, and the Claude Code
  handoff round trip. 25 slides. **Live demo included.**
- **[`ai-graph-engineering.html`](ai-graph-engineering.html)** — *AI Graph
  Engineering* (~30-min deep dive, for experienced devs). Which graph
  people actually mean — knowledge graph, retrieval graph (GraphRAG), workflow
  graph, GNN → the honest GraphRAG scoreboard (where it wins, where plain RAG
  wins, the null-query collapse) → graph memory vs markdown → code graphs vs
  agentic grep → subagents, hooks & workflows as a graph runtime → a decision
  table. 33 slides.

## Revised editions of talks 01–03

Open **[the v2 chooser](first-three-v2.html)** to compare the new decks with the preserved originals.

| Talk | New edition | Focus |
|---|---|---|
| 01 · The AI Toolbox | [28 slides](ai-toolbox-v2.html) | Task-based selection, a downloadable report and two sourced stories |
| 02 · Intro to Agentic AI | [26 slides](agentic-ai-v2.html) | One invoice task, permissions before launch and evidence at four checkpoints |
| 03 · Agentic Engineering | [32 slides](agentic-engineering-v2.html) | An export contract, verification, recovery and measuring accepted work |

The new editions use the existing Ember stage and locally bundled fonts. Navigate with arrows or Space; **N** shows notes, **P** opens the presenter window, **F** toggles fullscreen. Direct links use `#8` for slide 8. The thumbnail rail is hidden by default to give the slides the full viewport.

- [Detailed review and implementation plans](reviews/first-three-v2/PLAN.md)
- [Source review](reviews/first-three-v2/SOURCES.md) and [validation results](reviews/first-three-v2/VALIDATION.md)
- [Toolbox handout](reviews/first-three-v2/TOOLBOX-HANDOUT.md) and [worked report](examples/v2/review-report.html)
- [Invoice demo, tests and prepared fallback](examples/v2/invoice/README.md)
- New slide maps and speaker notes: `reviews/first-three-v2/*-v2-map.md` and `*-v2-notes.md`

Regenerate the revised files with `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_first_three_v2.py`. Slide content is authored in that script; generated HTML remains static. The builder checks the original deck hashes before deriving each new shell. It does not overwrite the original decks.

Browser checks use `scripts/qa_first_three_v2.cjs` with Playwright and installed Chrome. Run it from the repository root; it starts and closes its own temporary localhost server (including byte-range support for video checks). If Playwright is not on Node's module path, set `PLAYWRIGHT_MODULE` to its installed directory. QA screenshots go to `/private/tmp/agentic-talks-v2-qa` by default; set `QA_OUTPUT` to use another directory.

## View it

- **Locally:** open any `.html` deck in a modern browser (macOS:
  `open index.html` opens the chooser). `index.html` routes the reader to the
  right deck by audience — non-technical (01) → developers new to agents (02) →
  developers going deeper (03) → devs & IT admins on internals (04) → devs
  levelling up on cost, orchestration & measurement (05–07, WIP) → anyone
  making visual work with Claude Design (08, WIP) → devs weighing up graphs
  (09), plus the hands-on evals workshop (WIP), with
  self-identification bullets per deck and a
  one-question fallback for the undecided.
- **Online:** if GitHub Pages is enabled, the repo's Pages root serves the chooser.

## Navigate

- **Keyboard:** `↑` `↓` / `←` `→` / `Space` / `PageUp` `PageDown` / `Home` `End`
- **Touch:** swipe up/down
- **Mouse:** scroll, or click the nav dots on the right

## Edit in the browser

The deck has a built-in editor (no build step):

- Press **`E`** (or hover the top-left corner) to toggle edit mode, then click any text.
- Edits **auto-save** to `localStorage`.
- Bottom-right: **↺ Reset** (restore original) · **⬇ Export** (download a clean copy with edits baked in).

## What's covered

**The AI Toolbox** — pricing literacy (subscription / credits / per-seat / API) ·
chatbot vs agent, the loop, no memory (condensed core) · the big three labs plan by
plan (Cowork, Claude Design, ChatGPT Work, Gemini Notebook, Veo/Flow) · product churn ·
a week of real tasks · the wider landscape with a leader per category · the fine print
(licences, public tiers, provenance, credit budgeting) · five documented stories
(Project Vend, the superbug result, CFA/IMO, the security double, the Super Bowl
twist) · connectors & MCP, Claude/ChatGPT × Office, M365 Copilot & Gemini Workspace,
Zapier MCP.

**Intro to Agentic AI** — model / harness / agent · the agent loop · reasoning /
"thinking" · current SOTA models & harnesses · pricing (subscriptions vs API) ·
context (context rot, caching, compaction, sub-agents) · permissions & safety ·
memory (CLAUDE.md, skills, plugins) · APIs, CLIs & MCP · how to work with it well.

**Agentic Engineering** — the machine (model / harness / client + a client-server
sequence diagram) · next-token prediction & attention · context as the program ·
statelessness, token cost & KV caching (with cache-lifetime economics) · the "dumb
zone" · interactive projects to go build/see an LLM · model × reasoning-effort routing
and Fable techniques (advisor & orchestrator patterns) · the agentic ladder · loops &
verifiers (spiralling, reward-hacking) · dynamic workflows · skills & plugins.
A single **context** thread ties the sections together (🧵 markers throughout).

**Cost & Context · Orchestrating Agents · Measuring What Works** *(decks 05–07,
WIP)* — what agents really cost (tokens, subscriptions, Bedrock) · efficient
context work (CLAUDE.md, `/doctor`, `/clear` vs `/compact`) · orchestration,
sandboxing, skills & plugins, MCP vs CLI · evals, traces & picking a model by
cost per accepted task (the teaser for the hands-on evals workshop).

**Claude Design** *(WIP)* — what it is (Anthropic Labs, April 2026, beta) ·
chat left / canvas right · four starting points (text, DOCX/PPTX/XLSX, web
capture, codebase) · the design-system feature & `/design-sync` · plans &
shared usage · the craft: iterate (judge iteration 4, not 1), brief like a
creative director, chat vs inline comments vs direct editing, briefs to steal
· pitfalls · sharing, exports (PPTX/PDF/HTML/Canva/zip) & the Claude Code
handoff round trip. Facts verified September 2026.

## Live demo (agentic-ai deck, optional; decks 05 and 08 also have live demos)

The *Intro to Agentic AI* deck is built to run alongside a live agent. There's a **🔴 LIVE** anchor
slide right after the hook, and **🔴 LIVE** callback markers on the loop,
thinking, and context slides. A presenter quick-reference is in an HTML comment
at the top of `agentic-ai.html`.

- Before the talk, start Claude Code on a real task in **Auto** mode (the
  default on paid plans since Aug 2026 — a classifier approves routine actions)
  or **accept-edits** mode, so it won't block on a prompt mid-talk — which also
  demos the permissions slides.
- Good tasks (~3–8 min, several tool calls): *"add a `/health` endpoint with a
  test, then run the tests"* or *"find & fix why test X fails."* Avoid anything
  that finishes in ~20s or needs a login.

## Concept animations (Remotion)

The most important concepts are animated with Remotion; the decks embed the
rendered MP4s as muted loops that restart whenever you land on their slide:

| Animation | Concept | Used on |
|-----------|---------|---------|
| `agent-loop` | the agent loop (propose → run → result → repeat) | toolbox s6 · intro s10 · eng s17 |
| `stateless` | no memory: every call re-sends the whole history | toolbox s7 · intro s6 · eng s14 |
| `next-token` | next-token prediction with sampled probabilities | eng s4 |
| `quality` | quality vs. context fill — context rot / the dumb zone | intro s22 · eng s28 |
| `kv-cache` | KV caching: cached prefix + fresh tail, append-only | eng s26 |
| `subagents` | delegation: messy work inside, tiny summary back | intro s25 · eng s29 · cost s20 |
| `context-lifecycle` | fixed overhead stamped into every turn; only the conversation grows | cost s14 |
| `progressive-disclosure` | a skill's how-to loads on trigger; CLAUDE.md is paid every turn | orch s16 |
| `graph-hops` | vector top-k pulls look-alikes; graph traversal walks edges to the answer | graph s6 |

To tweak or re-render: `cd remotion && npm i`, then `npx remotion studio` to
preview or `npx remotion render <composition-id> ../assets/anim/<id>.mp4` to
re-export (composition ids are listed in `remotion/src/Root.tsx`; each exists
in the deck's light/dark theme variant as needed). The fonts are bundled
locally in `remotion/public/fonts` (OFL latin subsets), so renders work
offline — no Google Fonts fetch at render time.

## Customize

All styling is driven by CSS variables in the `:root` block of `agentic-ai.html`
(`--card` is the accent color; `--font-*` set the typography). The Remotion
animations read the same palette from `remotion/src/theme.ts`.

## Notes

- Facts (model names, prices) in the revised decks 01–03 and decks 04–09 were
  **re-checked against primary sources in September 2026** (see `review-decks-01-02.md`
  and `reviews/first-three-v2/`). This space moves fast, so re-check the primary sources (see the deck's final two
  "Sources" slides) before reusing.

## Files

| File | Purpose |
|------|---------|
| `ai-toolbox-v2.html`, `agentic-ai-v2.html`, `agentic-engineering-v2.html` | Current editions of talks 01–03 (the landing page links these). |
| `ai-toolbox.html`, `agentic-ai.html`, `agentic-engineering.html` | Earlier editions of talks 01–03, kept at their original URLs. |
| `subagents-prompt-caching.html` | *Subagents & Prompt Caching* deck — engineering deep dive (no live demo). |
| `cost-and-context.html` | *Cost & Context* deck — what agents really cost and how to spend context well (WIP). |
| `orchestrating-agents.html` | *Orchestrating Agents* deck — orchestration tools and failure modes, skills & plugins, MCP vs CLI (WIP). |
| `measuring-what-works.html` | *Measuring What Works* deck — evals, traces & judging changes by evidence (WIP). |
| `claude-design.html` | *Claude Design* deck — ~30-min product deep dive on Anthropic's visual-creation tool (WIP, live demo, no code needed). |
| `ai-graph-engineering.html` | *AI Graph Engineering* deck — knowledge/retrieval/workflow graphs and when either pays. |
| `evals-workshop.html` | *Evals, Hands On*: slides for the half-day evals workshop (WIP until the dry run). |
| `workshops/evals/` | The workshop's lab kit (`lab/`), facilitator guide, participant handout, live board source and the talk 07 archives. |
| `graph-engineering-ai-llms.md`, `deck09-facts.md` | Research note and sourced fact sheet behind deck 09. |
| `review-decks-01-02.md` | Fact-check of decks 01 and 02 (Sep 2026) with the per-slide change plan and its status. |
| `archive/` | Earlier editions of decks 04–09 (as of commit `abd9eed`, with their original animations) and `archive/index.html`, which lists the earlier edition of every deck. |
| `index.html` | Landing page routing readers to the right deck by audience (GitHub Pages root). |
| `assets/anim/` | Rendered concept animations (MP4 loops) embedded by the decks. |
| `remotion/` | Remotion project — sources for the animations. |
