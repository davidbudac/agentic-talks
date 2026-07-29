# Agentic talks

Zero-build HTML slide decks — a general-audience tool landscape, a beginner
intro to agentic AI, a developer follow-up, engineering deep dives, a workshop
on working smarter with agents, and a Claude Design product tour. Same
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
  every tool slide (July 2026 snapshot). 57 slides. **No live demos.**
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
  subscription vs an API key. 39 slides, ~30 min. **No live demos.**
- **[`working-smarter.html`](working-smarter.html)** — *Working Smarter with
  Agents* (WIP, half-day workshop with live demos, for engineers already using
  Claude Code who want to level up). What agents really cost (tokens,
  subscriptions, Bedrock) → efficient context work (CLAUDE.md, evals, traces) →
  orchestration, local open-source models & alternative harnesses. ~85 slides.
- **[`claude-design.html`](claude-design.html)** — *Claude Design* (WIP,
  ~30-min product deep dive, no code or design background needed — any paid
  Claude plan). The full tour behind deck 01's two teaser slides: the
  chat-and-canvas interface, four starting points, the design-system/brand
  feature (`/design-sync`), plans & shared usage → the craft (the iteration
  loop, briefing, the three refinement channels, example briefs to steal, a
  live five-minute build, pitfalls) → sharing, exports, and the Claude Code
  handoff round trip. 25 slides. **Live demo included.**

## View it

- **Locally:** open any `.html` deck in a modern browser (macOS:
  `open index.html` opens the chooser). `index.html` routes the reader to the
  right deck by audience — non-technical (01) → developers new to agents (02) →
  developers going deeper (03) → devs & IT admins on internals (04) → devs
  levelling up on cost, orchestration & measurement (05–07, WIP) → anyone
  making visual work with Claude Design (08, WIP) — with
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
plan (Cowork, Claude Design, agent mode, Gemini Notebook, Veo/Flow) · product churn ·
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

**Working Smarter with Agents** *(WIP)* — what agents really cost (tokens,
subscriptions, Bedrock) · efficient context work (CLAUDE.md, evals, traces) ·
orchestration, local open-source models & alternative harnesses.

**Claude Design** *(WIP)* — what it is (Anthropic Labs, April 2026, beta) ·
chat left / canvas right · four starting points (text, DOCX/PPTX/XLSX, web
capture, codebase) · the design-system feature & `/design-sync` · plans &
shared usage · the craft: iterate (judge iteration 4, not 1), brief like a
creative director, chat vs inline comments vs direct editing, briefs to steal
· pitfalls · sharing, exports (PPTX/PDF/HTML/Canva/zip) & the Claude Code
handoff round trip. Facts verified July 2026.

## Live demo (agentic-ai deck, optional; the WIP workshop deck also has live demos)

The *Intro to Agentic AI* deck is built to run alongside a live agent. There's a **🔴 LIVE** anchor
slide right after the hook, and **🔴 LIVE** callback markers on the loop,
thinking, and context slides. A presenter quick-reference is in an HTML comment
at the top of `agentic-ai.html`.

- Before the talk, start Claude Code on a real task in **auto / accept-edits**
  mode (so it won't block on a prompt mid-talk — which also demos the
  permissions slides).
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

To tweak or re-render: `cd remotion && npm i`, then `npx remotion studio` to
preview or `npx remotion render <composition-id> ../assets/anim/<id>.mp4` to
re-export (composition ids are listed in `remotion/src/Root.tsx`; each exists
in the deck's light/dark theme variant as needed).

## Customize

All styling is driven by CSS variables in the `:root` block of `agentic-ai.html`
(`--card` is the accent color; `--font-*` set the typography). The Remotion
animations read the same palette from `remotion/src/theme.ts`.

## Notes

- Facts (model names, prices) are **verified as of July 2026** and labelled on-slide —
  this space moves fast, so re-check the primary sources (see the deck's final two
  "Sources" slides) before reusing.

## Files

| File | Purpose |
|------|---------|
| `ai-toolbox.html` | *The AI Toolbox* deck — tool landscape for everyone (no live demo). |
| `agentic-ai.html` | *Intro to Agentic AI* deck — beginners. |
| `agentic-engineering.html` | *Agentic Engineering* deck — developers (no live demo). |
| `subagents-prompt-caching.html` | *Subagents & Prompt Caching* deck — engineering deep dive (no live demo). |
| `working-smarter.html` | *Working Smarter with Agents* deck — half-day workshop on cost, context efficiency & orchestration (WIP, live demos). |
| `claude-design.html` | *Claude Design* deck — ~30-min product deep dive on Anthropic's visual-creation tool (WIP, live demo, no code needed). |
| `index.html` | Landing page routing readers to the right deck by audience (GitHub Pages root). |
| `assets/anim/` | Rendered concept animations (MP4 loops) embedded by the decks. |
| `remotion/` | Remotion project — sources for the animations. |
