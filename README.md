# Agentic talks

Two zero-build HTML slide decks on how coding agents actually work — a beginner
intro and a developer follow-up. Same template, same aesthetic. The key concepts
are illustrated by short looping animations rendered with
[Remotion](https://www.remotion.dev/) (in `assets/anim/`, sources in `remotion/`),
so keep those folders next to the `.html` files.

Author: **David Budáč / ČSOB** · English

- **[`agentic-ai.html`](agentic-ai.html)** — *Intro to Agentic AI* (Claude Code for
  beginners). Model / harness / agent, the loop, context, permissions, memory & MCP. 36 slides.
- **[`agentic-engineering.html`](agentic-engineering.html)** — *Agentic Engineering*
  (basics for developers). One thread — the context window — runs through: the machine
  (model / harness / client) → foundations → model × effort (incl. Fable) → loops &
  verifiers → skills & plugins. 43 slides. **No live demos.**

## View it

- **Locally:** open either `.html` file in any modern browser (macOS:
  `open index.html` opens the chooser). `index.html` is a small chooser page
  linking both decks.
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

## Live demo (agentic-ai deck only, optional)

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
| `agent-loop` | the agent loop (propose → run → result → repeat) | intro s10 |
| `stateless` | no memory: every call re-sends the whole history | intro s6 · eng s12 |
| `next-token` | next-token prediction with sampled probabilities | eng s6 |
| `quality` | quality vs. context fill — context rot / the dumb zone | intro s22 · eng s17 |
| `kv-cache` | KV caching: cached prefix + fresh tail, append-only | eng s15 |
| `subagents` | delegation: messy work inside, tiny summary back | intro s25 |

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
| `agentic-ai.html` | *Intro to Agentic AI* deck — beginners. |
| `agentic-engineering.html` | *Agentic Engineering* deck — developers (no live demo). |
| `index.html` | Chooser page linking both decks (GitHub Pages root). |
| `assets/anim/` | Rendered concept animations (MP4 loops) embedded by both decks. |
| `remotion/` | Remotion project — sources for the animations. |
