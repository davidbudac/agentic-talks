# Ember Design System

A warm, high-contrast **presentation & dev-tool aesthetic** — near-black "ink", cream "paper", and a single vivid coral accent, set in Space Grotesk + IBM Plex. Built for engineering decks, technical explainers, and the kind of product/marketing surfaces that sit next to them.

Ember was extracted from the **"Subagents & Prompt Caching"** engineering deep-dive deck (`Subagents and Prompt Caching.dc.html`, in this same project) — its direction was "bold dev-tool." This system captures that language so it can be reused for new presentations and projects.

> **Note on the name:** there is no external company here — "Ember" names the aesthetic itself (warm coral-on-cream). Reuse it as a standalone style.

---

## Sources

- **`Subagents and Prompt Caching.dc.html`** — the canonical reference deck (39 slides) this system is derived from. Open it to see every pattern in motion.
- **`scratchpad.md`** — the original visual-system notes (palette, type scale, rhythm rules).
- No external Figma / codebase / brand guidelines were provided; all tokens were measured from the deck.

---

## Content fundamentals

**Voice — plain, direct, technically literate, quietly warm.** Explains hard ideas without dumbing them down, then lands a short punchy summary. Second person ("you", "your machine"). Active voice. Em-dashes for asides — used freely.

- **Titles** are short and declarative, often with a turn or contrast: *"Read it once — not every time"*, *"Your desk stays clear"*, *"Subagents live in the harness"*, *"Caching you'll never notice"*. Sentence case, never Title Case.
- **Eyebrows** are tiny category labels above the title: *"The big idea"*, *"Where it actually happens"*, *"In Claude Code"*. Set in mono, UPPERCASE, coral, wide tracking.
- **Body** is sentence case, calm and concrete. Bold (`--text-strong`) is used sparingly to pin one key word; coral is used for the single most important term in a sentence.
- **Mono labels** (lowercase or UPPERCASE) annotate diagrams and data: `reads all`, `cache read`, `WITHOUT SUBAGENT`, `200 tok`.
- **Numbers earn their place.** Token counts, prices, durations appear only when they teach something; no decorative stats.
- **No emoji.** Status is shown with restrained glyphs instead: `✓ ✕ → ↑ ↓ ↻ ▸ ⏺ ⎿ •`. A filled dot `●` marks a spotlighted item ("● HAPPENS HERE").

---

## Visual foundations

**Palette — warm tri-tone.** Everything is built from three anchors and the ramps between them:
- **Ink** `#16130e` — a warm brown-black. Dark surfaces and all text on light.
- **Paper** `#f4efe6` — warm cream. Light surfaces and all text on dark.
- **Coral** `#ff5c35` — the one accent. Eyebrows, emphasis, highlights, the spotlight ring.
Neutrals are warm (cream/taupe/brown), never cool grays. Use **at most the light/dark pair** as backgrounds in any one artifact; coral is an accent, not a background. Avoid bluish-purple gradients and cool grays entirely — they break the warmth.

**Type.**
- **Space Grotesk** — display & numerals. Headings 56–88px, hero 132px, section numerals a massive 200px. Tight tracking (`-0.025em` to `-0.03em`), line-height ~0.9–1.05.
- **IBM Plex Sans** — body, 28–40px, weight 400–500, line-height ~1.5, `text-wrap: pretty`.
- **IBM Plex Mono** — eyebrows, labels, code, data. Eyebrows UPPERCASE with `0.1em` tracking.

**Rhythm.** Slides alternate **light and dark** backgrounds for cadence; section dividers are always dark with a giant coral numeral. Two background colors max (the ink/paper pair). Dark "hero" slides are reserved for section openers, big diagrams, and code/terminal views.

**Layout.** Slide frame is 1920×1080 with generous padding (110px sides; 96/84 top/bottom, or 88/80 when a diagram needs room). Standard slide stack: **eyebrow → title → short subtitle → content area (`flex:1`)**, sometimes closing with a full-width takeaway bar. Groups use flex/grid with explicit `gap`, never inline-flow spacing.

**Cards & surfaces.**
- On light: sunk cream `#efe7d8` fill, `1.5–2px` border in `#cbbfa9`/`#d8ccb6`, radius 12–18px.
- On dark: raised `#1c1812` fill, `1.5–2px` border `#3a342a`.
- Compare layouts pair one **dark** and one **cream** card side by side.
- Diagram "tiles" can carry a `--stack-shadow` to read as "one or more".

**Borders over shadows.** Ember is mostly flat: structure comes from borders and the palette. Drop shadows are rare — only floating surfaces (the terminal window) get `--shadow-terminal`. The signature emphasis is the **coral ring** (`--ring-accent`) plus a `● HAPPENS HERE` pill — used to spotlight one element in a diagram.

**Signature motifs.**
- **Coral quarter-circle** bleeding off a corner of title/closing slides (a 280–300px circle clipped by the slide edge).
- **Section numeral** — 200px coral Space Grotesk `01 / 02 / 03`, with a `120×4px` coral accent bar under the section title.
- **Callout** — `#ffe9e2` wash with a `6px` coral left border and `0 12px 12px 0` radius, for "most common failure mode" style asides.
- **Code block** — `#0e0c08` background, mono, with warm syntax colors and a coral left-border highlight on the key line.
- **Terminal window** — `#14110c` body, `#1d1810` title bar, three macOS traffic-light dots, mono content; used to show "what you'd see in Claude Code."

**Motion.** The deck itself is static (slide cuts). When animating in other media, keep it restrained: short fades/slides, gentle easing, no bounce. Hover/press for interactive surfaces: darken coral slightly or drop opacity to ~0.9; press shrinks ~1–2%. Never neon glows.

---

## Iconography

Ember uses **no icon library and no emoji.** Iconographic meaning is carried by:
- **Unicode glyphs** in the type itself: `✓ ✕ → ↑ ↓ ↻ ▸ ◀ ●` for status, flow, and spotlight.
- **Box-drawing / CLI glyphs** `⏺ ⎿ •` to recreate the Claude Code transcript look (mono, with a broad monospace fallback so they always render).
- **Built shapes**, not drawn icons: bars (`3px` radius rectangles) stand in for content/tokens; dashed-border boxes represent disposable/private contexts; arrowheads are CSS border triangles.

If a future surface needs a true icon set, add a CDN line here (Lucide or Phosphor match the geometric/utilitarian tone) and document it — do not hand-draw SVGs or introduce emoji.

---

## Index / manifest

- **`styles.css`** — link this one file. Imports all tokens + fonts.
- **`tokens/`** — `colors.css`, `typography.css`, `spacing.css`, `effects.css`, `fonts.css`.
- **`guidelines/`** — foundation specimen cards (Colors, Type, Spacing, Brand) shown in the Design System tab.
- **`components/`** — reusable React primitives:
  - `core/` — `Eyebrow`, `Chip`, `AccentBar`, `Callout`
  - `code/` — `CodeBlock`, `TerminalWindow`
  - `slide/` — `DualPanel`, `StatTile`
- **`slides/`** — slide archetype starting points (Title, Section divider, Compare, Diagram, Code, Takeaways) as standalone HTML.
- **`SKILL.md`** — makes this system usable as a Claude Code / Agent skill.

> **Sharing:** to let your org view this as a design system, open the **Share** menu and set the file type to **Design System**.
