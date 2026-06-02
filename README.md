# Agentic AI — intro talk

A self-contained, zero-dependency HTML slide deck introducing **agentic AI** to a
general audience — how tools like **Claude Code** and **Codex** actually work.

Author: **David Budáč / ČSOB** · 30 slides · English

## View it

- **Locally:** open [`agentic-ai.html`](agentic-ai.html) in any modern browser
  (macOS: `open agentic-ai.html`).
- **Online:** if GitHub Pages is enabled, the deck is served at the repo's Pages URL
  (the root redirects to the deck).

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

Model / harness / agent · the agent loop · reasoning / "thinking" ·
current SOTA models & harnesses · pricing (subscriptions vs API) ·
context (context rot, caching, compaction, sub-agents) · permissions & safety ·
memory (CLAUDE.md, skills, plugins) · APIs, CLIs & MCP · how to work with it well.

## Live demo (optional, recommended)

The deck is built to run alongside a live agent. There's a **🔴 LIVE** anchor
slide right after the hook, and **🔴 LIVE** callback markers on the loop,
thinking, and context slides. A presenter quick-reference is in an HTML comment
at the top of `agentic-ai.html`.

- Before the talk, start Claude Code on a real task in **auto / accept-edits**
  mode (so it won't block on a prompt mid-talk — which also demos the
  permissions slides).
- Good tasks (~3–8 min, several tool calls): *"add a `/health` endpoint with a
  test, then run the tests"* or *"find & fix why test X fails."* Avoid anything
  that finishes in ~20s or needs a login.

## Customize

All styling is driven by CSS variables in the `:root` block of `agentic-ai.html`
(`--card` is the accent color; `--font-*` set the typography).

## Notes

- Facts (model names, prices) are **verified as of June 2026** and labelled on-slide —
  this space moves fast, so re-check the primary sources (see the deck's final two
  "Sources" slides) before reusing.

## Files

| File | Purpose |
|------|---------|
| `agentic-ai.html` | The presentation (self-contained). |
| `index.html` | Redirect to the deck (for GitHub Pages root). |
| `prez_prompt.txt` | Original brief / topic outline. |
| `my_slides.md` | Earlier scratch notes (unused). |
