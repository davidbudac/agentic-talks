Ivory 1.1 · 2026-10-04

# Ivory: a slide design system for HTML decks

This folder is the whole design system. It has no dependencies, needs no build step and makes no network requests: fonts, scripts and demo media are all inside it. Copy the folder into a project and build decks next to it. This file is the spec.

| Path | What it is |
|---|---|
| `DESIGN.md` | This spec |
| `styles.css` | `@font-face` rules for the bundled fonts, tokens, the slide template, every component, the deck chrome (notes panel, presenter window) and print rules |
| `fonts/` | Geist and Geist Mono as variable woff2 subsets, with their licence (`OFL.txt`, SIL Open Font License 1.1) |
| `deck-stage.js` | `<deck-stage>` web component: scaling, keyboard navigation, thumbnail rail, print. Generic, not Ivory-specific. **Never edit it** |
| `deck.js` | The Ivory deck runtime: slide numbers, video restart, notes panel (N), presenter window (P), fullscreen (F) |
| `template.html` | A minimal starter deck: title slide + one content slide, and a list of which kitchen-sink slide to copy for each component |
| `kitchen-sink.html` | One slide per component. The reference markup and the visual-regression page. Copy from it |
| `demo/` | The two demo videos and the image still used by the kitchen sink |
| `shots/ks-NN.png` | Approved screenshots of the 28 kitchen-sink slides, plus `ks-chrome-notes.png` and `ks-chrome-presenter.png` |
| `tools/shoot.sh` | Screenshots a deck, one 1920 × 1080 PNG per slide, or prints it to PDF |

---

## 1. What Ivory is

Ivory is a light, rigid, low-decoration slide style for technical talks to developers and IT admins, shown on a projector. Its brief, in the words of the person who commissioned it:

- "make it more rigid in the style of OpenAI's presentations which are typically very low on fluff and decorations"
- "more technical and cleaner"
- on type: serif headings "dont really fit the contents of the slides". So Ivory uses one family: Geist 600 for headlines, Geist for body text, Geist Mono for labels, figures and code. No serif anywhere.

Principles that follow from the brief:

1. **One fixed template.** Header, headline, zone and footer sit at the same coordinates on every slide.
2. **Content fills the zone.** Rows share the zone height. Columns and panels run its full height. Nothing floats in the middle of empty space.
3. **Two content sizes:** 30px and 40px. Nothing in between.
4. **One accent (clay), only for the point of the slide.**
5. **No decoration:** no illustrations, icons, textures, shadows, gradients, pills or filled cards. Corner radius is 0–4px (2px in practice). Hairlines separate things.
6. **All slides are light.** There are no dark slides.

---

## 2. Quick start

1. Copy this whole folder into your project, unchanged, as `ivory_design_system/`.
2. Copy `ivory_design_system/template.html` to the project, **next to the folder** (for example `my-project/talk.html`), and rename it. Its paths start with `ivory_design_system/`, so it does not work from inside the folder.
3. Build slides by copying whole `<section>`s from `kitchen-sink.html` (the comment at the top of `template.html` lists which slide shows which component).
4. Open the deck in Chrome or another Chromium browser (double-click the file; no server needed; Chrome is what the screenshots are made with). Screenshot it with `ivory_design_system/tools/shoot.sh` and look at every slide (§10).

Besides the `<deck-stage>` element that holds the slides, a deck needs exactly **three tags**:

```html
<link rel="stylesheet" href="ivory_design_system/styles.css">     <!-- in <head> -->
…
<deck-stage width="1920" height="1080"> …<section class="slide">…</section>… </deck-stage>
<script src="ivory_design_system/deck-stage.js"></script>          <!-- after </deck-stage> -->
<script src="ivory_design_system/deck.js"></script>                <!-- after deck-stage.js -->
```

No font `<link>`, no inline `<script>`, no chrome markup and no `<style>` block are needed.

**Keys** (in the browser): ←/→, Space, PgUp/PgDn move; Home/End jump; number keys go to a slide; R returns to slide 1; **N** toggles the speaker-notes panel; **P** opens the presenter window; **F** toggles fullscreen. The Notes / Present / Fullscreen buttons appear bottom right when the mouse moves. Normal browser view shows deck-stage's thumbnail rail on the left (it hides in fullscreen and on narrow windows); reordering slides in the rail does not edit the file. Print (Cmd/Ctrl-P → Save as PDF) gives one 1920 × 1080 page per slide.

### What `deck.js` does automatically

- **Slide numbers.** Every empty `<span class="snum"></span>` gets its two-digit slide number (`01`, `02`, …). A number written by hand is kept.
- **Total.** If the deck does not set `--deck-total`, deck.js sets it to the number of slides (two digits), so headers read `07 / 30`. To fix it by hand, put `<style>:root{--deck-total:"30"}</style>` in `<head>`.
- **Video restart.** When a slide becomes active, its `<video>` restarts from 0.
- **Presenter aids** (only in a top-level window, not when the deck is embedded in an iframe). It adds the Notes / Present / Fullscreen buttons and the notes panel unless the page already has `.pui-controls` / `.pui-notes`. N shows the active slide's `data-label` and `data-speaker-notes`. P opens a pop-up with the current slide, the next slide, the notes, an elapsed timer (click to reset) and a clock; ←/→ in that window drive the deck. F toggles fullscreen and hides the rail while fullscreen. The presenter window copies the deck's `<head>` stylesheets, so `styles.css` styles it; deck.js adds no styling of its own (only the `--deck-total` line when it sets the total).
- **Screenshot hooks.** `?chrome` in the URL shows the buttons and opens the notes panel; `?pw` renders the presenter window inside the page instead of a pop-up (§10).

---

## 3. Tokens

Rows marked **N** in the first column are **normative**: any implementation of Ivory, in any tool, must use them exactly. The rest are implementation details of `styles.css`.

### Colour

| N | Token | Value | Use |
|---|---|---|---|
| N | `--ivory` | `#FAF9F5` | Slide ground. Also the background of every video or rendered figure |
| N | `--paper` | `#F0EEE6` | Code and terminal panels only (and the notes/presenter chrome) |
| N | `--slate` | `#141413` | Headlines, primary text, diagram strokes, strong rules (1.5px) |
| N | `--body` | `#2E2E2B` | Running text inside cards, rows and tables |
| N | `--ink2` | `#5E5D59` | Secondary text, mono labels, footnote, "before" text |
| N | `--faint` | `#8A877E` | Code line numbers only |
| N | `--rule` | `#C9C3B4` | Every hairline (1px), dim diagram lines, the neutral bar segment |
| N | `--clay` | `#D97757` | The accent for fills and strokes |
| N | `--clay-ink` | `#C6613F` | The accent for text |

### Type

| N | Token | Value | Use |
|---|---|---|---|
| N | `--sans` | Geist | Headlines 600; body 400; bold/emphasis 500 |
| N | `--mono` | Geist Mono | Labels, counters, numbers in tables, code, diagram text. Weights 400 and 500 |
| N | `--reg` / `--lg` | `30px` / `40px` | The two content size steps |
| N | `--lab` | `20px` | Mono labels: 500, uppercase, tracking .08em, line height 24px |
| N | `--foot` | `26px` | Footnote, Geist 400, line height 36px |
| N | headline | 78px / 82px | Geist 600, tracking −.034em, max two lines, max width 1396 |
| N | title `h1` | 176px / .94 | Geist 600, tracking −.055em |
| N | card / term heading | 40px / 1.2 | Geist 600, tracking −.022em |
| N | hero number | 168px / 1 | Geist 500, tracking −.05em |
| | `--sans` fallback | `system-ui, sans-serif` | Only if the font fails to load |
| | `--mono` fallback | `ui-monospace, "SF Mono", Menlo, monospace` | Same |

Numbers use tabular lining figures everywhere (`font-variant-numeric: tabular-nums lining-nums`).

**Bundled fonts.** `styles.css` declares Geist (weights 400–600) and Geist Mono (400–500) from `fonts/` with the same `unicode-range` split Google Fonts uses: latin, latin-ext (e.g. "Budáč"), cyrillic, cyrillic-ext, vietnamese, and for Geist Mono also box-drawing symbols. The files are variable fonts; the declared weight ranges clamp anything else to the nearest end, matching the spec. There is no italic face: `<em>` is synthesised (Ivory uses almost no italics). A few characters are not in the subsets and are drawn by the system fallback font: arrows such as → ← ↺, and math signs such as ≥ ∥. That is expected and looks fine; × · — – “ ” ’ are in Geist.

### Grid and template

| N | Token | Value | Use |
|---|---|---|---|
| N | canvas | 1920 × 1080 | Every slide |
| N | `--margin` | 120px | Left and right margin |
| N | `--col` / `--gutter` / `--step` | 118 / 24 / 142px | 12 columns |
| N | `--gap` | 72px | Headline's last line to the zone top |
| N | `--zone-bottom` | 888px | Zone bottom edge |
| N | hairline / strong rule / stroke | 1 / 1.5 / 2px | Separators / header-row and total rules, axes / diagram boxes and lines |
| N | `--radius` | 2px | Code panels, diagram boxes, buttons. Nothing else is rounded |

---

## 4. The template

**Canvas and grid (N).** The canvas is 1920 × 1080. Side margins are 120px. There are 12 columns of 118px with 24px gutters. Column *n* starts at x = 120 + 142(*n*−1); a span of *n* columns is 142*n* − 24 wide. Useful spans: 2 cols = 260, 4 = 544, 5 = 686, 6 = 828, 7 = 970, 10 = 1396, 12 = 1680.

**Fixed coordinates (N)** (y, measured from the top of the slide):

| y | Element |
|---|---|
| 60–108 | `.slide-head`: mono label left, `NN / TT` right, text top at 64, 1px hairline at 108 |
| 172 | Headline top. Geist 600, 78/82px, tracking −.034em, max width 1396 (10 cols), **max two lines**, balanced |
| 326 or 408 | Zone top = the headline's last line + 72. One line gives 326, two lines give 408 |
| 888 | Zone bottom. Fixed |
| 960 | Footer hairline, 120 → 1800. Drawn on every slide by `.slide::after` |
| 983 | Footnote `.note`: Geist 26/36, `--ink2` |
| 1027 | Source line `.src`: mono 20/24, `--ink2`, one line, ellipsis if too long. It moves to 989 if the slide has no `.note` |

**The zone (N).** `<div class="zone">` is 1680 wide and 562 tall (one-line headline) or 480 tall (two lines). Exactly one component goes inside it, and that component fills it: `height:100%` is built into every component.

**Size steps (N).**

- **40px (`--lg`)** is for few, short items: card text, 2–3 row tables, code panels up to about 6 lines and 64 characters per line. Definition-row terms are always 40px.
- **30px (`--reg`)** is for rows, tables with 3+ rows or 3 columns, split-layout rows, 4 cards, and code with longer lines (up to about 85 characters).

Each component has a default step. Override it with the class `.lg` or `.reg` on the component.

**Footnote rules (N).** One line when a `.src` follows. Otherwise at most two lines. One footnote per slide. No text in the footer other than `.note` and `.src`.

**Slide numbers.** The header shows `NN / TT` (two digits each). Leave `.snum` empty and deck.js fills it (§2), or write `NN` by hand, which wins. The total comes from `--deck-total`, set by deck.js or by hand. If `--deck-total` is unset (no deck.js), only `NN` shows. Numbers are written into the DOM rather than produced by a CSS counter so that rail thumbnails and presenter-window clones, which see one slide at a time, show the right number. Hand-written numbers must be renumbered after reordering slides; empty ones never need it.

---

## 5. The accent rule (N)

Clay marks **the one element that is the point of the slide, and only when there is one.** A slide of equal items carries no clay. Never use clay in a headline, footnote or header label (the title slide's header label is the only exception). Never use more than one clay element per slide. A data series of bars counts as one element.

| Slide (kitchen-sink number) | Clay? | Where |
|---|---|---|
| Three parts: model / harness / client [04] | No | Three equals |
| Agenda [08], numbered steps [11], stage-by-stage workflow [19], sources [25] | No | Equal items |
| Vague vs checkable request [06] | Yes | `.tile.key` on the checkable one |
| Hold constant / Compare table [12] | Yes | `th.key` on Compare |
| Acceptance contract (code) [15] | Yes | `.key` on the `VERIFY:` token |
| Terminal trace [17] | Yes | `.key` on `PASS` |
| Cost with and without cache [14] | Yes | `.bar.key` on the cache-hit bar |
| Agent loop diagram [18] | Yes | The loop path (`.dg-line.key`) |
| Attention diagram [22] | Yes | The predicted token box (`.dg-box.key`) |
| Sequence with growing context [23] | Yes | The context bars, one series (`.dg-fill-key`) |
| Context growth chart [24] | Yes | The short new message segment (`.dg-fill-key`) |
| Title slide [01] | Yes | Audience label in the header |

---

## 6. Component catalogue

Every slide is built the same way. Copy whole slides from `kitchen-sink.html` (slide numbers in brackets).

```html
<section class="slide" data-label="Short label" data-speaker-notes="What to say.">
  <div class="slide-head"><span class="crumb">Section label</span><span class="snum"></span></div>
  <h2>Headline, one or two lines</h2>
  <div class="zone"> …one component… </div>
  <p class="note">Footnote.</p>
  <p class="src">Applied example · <a href="…">supporting documentation</a></p>   <!-- optional -->
</section>
```

- `data-label` is shown in the notes panel and the presenter window; `data-speaker-notes` is the notes text. Every slide has both.
- `.crumb` is the section label (mono, uppercase via CSS; write it in normal case). It is truncated with an ellipsis if too long.

### Title slide [01]

```html
<section class="slide title-slide" data-label="Title" data-speaker-notes="…">
  <div class="slide-head"><span class="crumb">Audience or kicker</span><span class="snum"></span></div>
  <h1>Agentic<br>Engineering</h1>
  <p class="sub">From token prediction to bounded, verified work.</p>
  <div class="meta">
    <div><span class="lab">Author</span><a href="https://example.com">Author Name</a></div>
    <div><span class="lab">Revised</span>October 2026</div>
    <div><span class="lab">Length</span>30 slides</div>
  </div>
</section>
```

- `h1` is 176px/.94 Geist 600. Its last line ends at y 712 and it grows upward. Use at most two lines.
- `.sub` is 38px, `--ink2`, at y 752, 7 columns wide.
- `.meta` has three cells of 4 columns each, under the footer hairline at y 983 (28px Geist, mono label). No `.zone`, no `.note`.
- The header label is clay here and nowhere else.

### Cards: equal items in cells [04, 05, 07]

Use for 2–4 parallel items.

```html
<div class="zone"><div class="cards c3">
  <div class="tile"><span class="lab">01</span><h3>Model</h3><p>Proposes text or a structured tool call.</p></div>
  <div class="tile"><span class="lab">02</span><h3>Harness</h3><p>Builds context, applies permissions and runs tools.</p></div>
  <div class="tile"><span class="lab">03</span><h3>Client</h3><p>The terminal or editor where you inspect and steer.</p></div>
</div></div>
```

- Cells are full height, with a top hairline, vertical hairlines between them and a bottom hairline on the zone edge.
- The label sits at the top. The `h3` and the `p` sit on the bottom edge, and headings line up across cells.
- The column count comes from the number of tiles. `.c2/.c3/.c4` are optional, except that `.c4` drops to 30px.
- Each part is optional: label (mono, e.g. `01` or a name), `h3`, and **one** `p` (use `<br>` for a second line). Default size is 40px; add `.reg` for long text.

### Before / after [06]

```html
<div class="cards c2">
  <div class="tile was"><span class="lab">Before</span><p>…</p></div>
  <div class="tile key"><span class="lab">After</span><p>…</p></div>
</div>
```

`.was` greys the text. `.key` adds a 2px clay top rule and a clay label. Use `.key` only for the side that is the point.

### Rows: bullets, numbered steps, definition rows [08–11]

All rows share the zone height and have hairlines between them.

| Markup | Looks like | Use for |
|---|---|---|
| `<ul class="bul"><li>…</li></ul>` | Text rows, no marker | Unordered points (full width or in a split) |
| `<ol class="bul"><li>…</li></ol>` | `01` label in column 1, text from column 2 | Numbered steps |
| `<ol class="bul def"><li><b>Start:</b> text…</li></ol>` | `01` · 40px term (2 cols) · 30px text from column 4 | Bullets with a bold lead-in |
| `<ol class="bul def wide">…` | Term column is 4 cols wide; text starts at column 6 | **Agenda** (section titles + one-line descriptions) |

- `ul.bul.def` is the same layout without numbers.
- Inline `<b>` in a plain row is 500 slate. Use it for a short lead-in when the list sits in a split.
- In `.def` rows the first `<b>` becomes the term. If the definition contains a link, `<code>` or `<b>`, wrap it: `<li><b>Term</b><span>text with <code>x</code></span></li>`.
- In plain `ol.bul`, start the text right after `<li>` (no newline or space) so it lines up exactly on column 2.
- Use 3–5 rows. Beyond about 5, use a table.

### Tables [12, 13, 14, 26]

```html
<table class="tbl">                 <!-- 2 cols: col 1–6 | col 7–12 -->
  <thead><tr><th>Category</th><th class="key">What to record</th></tr></thead>
  <tbody><tr><td>…</td><td>…</td></tr></tbody>
</table>
```

- The header row holds mono labels with a 1.5px slate rule under it. Body rows share the remaining height and have hairline separators.
- Default size is 30px. `.lg` is 40px and is meant for 2–3 short rows.
- `.c3` makes 3 columns of 4 grid cols each. `.c4` makes 4 columns of 3 each.
- `.num` makes a numeric table: the label column fills, the last column is right-aligned Geist Mono. `<tr class="tot">` is the total row: weight 500 with a 1.5px slate rule above it.
- `th.key` is the only accent a table takes.

### Code panel and terminal trace [15, 16, 17]

Each line is a `<span class="l">` so CSS can number it and spread the lines evenly. Whitespace between the spans is ignored; spaces inside a line are preserved.

```html
<div class="zone"><div class="code">
  <span class="l"><span class="k">GOAL:</span> export invoice net, VAT and gross values to CSV.</span>
  <span class="l"><span class="key">VERIFY:</span> pytest tests/test_export.py -q</span>
  <span class="l">  SKILL.md     indented lines keep their spaces</span>
</div></div>
```

- The panel spans all 12 columns and the full zone height, on `--paper` with 2px radius. Lines are evenly distributed. Line numbers `01…` sit right-aligned in column 1; code starts at column 2.
- Default size is 40px (**about 64 characters per line at most**). Use `.reg` for 30px (**about 85 characters**). Lines longer than that are clipped, so shorten or break them by hand.
- Spans inside a line: `.k` keyword (500), `.c` comment and `.a` arrow (`--ink2`), `.key` the one clay token.
- A terminal trace is the same panel. Align columns with spaces and mute the arrows with `<span class="a">→</span>`.
- A caption such as "Illustrative check, not a real trace:" becomes a `.c` comment line or moves into the footnote.

### Hero figure with to-scale bars [14]

```html
<div class="split even">
  <div class="hero">
    <div class="big">$0.0506</div>
    <div class="bars">
      <div class="bar key" style="--v:.3373"><span class="lab">With the cache hit</span><div class="track"><i></i><b>$0.0506</b></div></div>
      <div class="bar" style="--v:.8187"><span class="lab">Without it</span><div class="track"><i></i><b>$0.1228</b></div></div>
      <div class="axis"><span style="--v:0">$0.00</span><span style="--v:.3333">$0.05</span><span style="--v:.6667">$0.10</span><span style="--v:1">$0.15</span></div>
    </div>
  </div>
  <table class="tbl num">…</table>
</div>
```

- `--v` is value ÷ axis maximum, so the bars are to scale. Pick an axis maximum that leaves room for the value label after the longest bar (`--v` about 0.85 at most).
- `.big` is 168px Geist 500 at the top of the zone. The bars (20px tall) sit on the zone bottom.

### Split: rows + figure [18–21]

```html
<div class="zone"><div class="split">
  <ul class="bul">…3–4 rows…</ul>          <!-- columns 1–5 (686px) -->
  <div class="fig"> svg | video | img </div> <!-- columns 7–12 (828px); column 6 stays empty -->
</div></div>
```

- `.split.even` gives 6 | 6 columns (828 + 24 + 828). Use it for hero + table.
- `.split.flip` puts the wide column first, for a figure on the left.
- Both sides run the full zone height.
- A diagram that would sit above bullets becomes either a split or a full-width figure with the bullets folded into the footnote or the speaker notes.

### Full-width figure [22–24]

```html
<div class="zone"><div class="fig">
  <span class="lab">Illustrative · three requests, including history</span>   <!-- optional caption -->
  <svg viewBox="0 0 1680 440">…</svg>
</div></div>
```

The optional `.lab` caption takes 24px plus a 16px gap at the top of the figure. `.fig` takes one `svg`, `video` or `img`, which fills it.

### Sources and link lists [25]

```html
<div class="links">
  <div class="linkcol">
    <h3>Mechanisms</h3>
    <a href="https://arxiv.org/abs/1706.03762">Attention Is All You Need<span class="u">arxiv.org/abs/1706.03762</span></a>
    …
  </div>
  <div class="linkcol"><h3>Implementation details</h3>…</div>
</div>
```

- Two 6-column lists. The header label has a slate rule; rows share the height; the title is 30px with a mono URL below it.
- Give both columns the same number of links (3–5) so their rows line up.

### Inline text

| Element | Rendering |
|---|---|
| `<a>` | Inherits the text colour. 1.5px `--ink2` underline. Clay on hover |
| `<code>` | Geist Mono at .92em, no background |
| `<b>` / `<strong>` | 500 slate |
| `<span class="key">` | Clay text, for one word that is the point |
| `.mut` | `--ink2` |

### Authoring aids (never ship)

- `.show-grid` on a section overlays the 12 columns, the headline-top and zone-bottom lines, and the zone outline [02, 03]. It is hidden in print.
- `.fig-ph` is a dashed placeholder box for a figure that is not made yet.

### Legacy aliases

`styles.css` accepts a few older class names so imported markup still lays out: `.slide-content` (a wrapper; `display:contents`), `.reveal` (no-op), `.dg-box.hot` = `.key`, `.dg-t.on` = `.key`, `.dg-fill-a/-g/-r` = `-1/-2/-key`, code spans `.o .d` = `.k` and `.g .b` = plain. Do not use them in new slides.

---

## 7. Diagrams, video and other media

### Diagram idiom (N)

Diagrams are engineering figures:

- rectangles with 2px slate strokes, `rx="2"`
- orthogonal connectors (`H`/`V` path segments, no curves, no diagonals)
- small solid arrowheads
- mono labels
- at most one clay element

**Draw at 1:1.** Set `viewBox` to the pixel size the figure gets, so `font-size` in the SVG is real pixels and edges land on the grid:

| Figure position | One-line headline | Two-line headline |
|---|---|---|
| Full width | `0 0 1680 562` | `0 0 1680 480` |
| Full width with `.lab` caption | `0 0 1680 522` | `0 0 1680 440` |
| Split, columns 7–12 | `0 0 828 562` | `0 0 828 480` |

A viewBox drawn for the wrong height still renders, but it scales down and leaves the grid. Place boxes on multiples of 142 (2 cols = 260 wide, then +284 for the next) so they line up with the columns. Keep everything inside the viewBox.

SVG classes (styling comes from CSS, so give elements no `fill`/`stroke`/`font` attributes and no inline `style`):

| Class | Rendering |
|---|---|
| `.dg-box` | Ivory fill, 2px slate stroke |
| `.dg-box.mid` | Secondary component: 1.5px `--ink2` stroke |
| `.dg-box.outer` | Boundary: dashed 1.5px `--ink2`, no fill |
| `.dg-box.key` | Clay stroke: the one key component |
| `.dg-line` | 2px slate connector |
| `.dg-line.dim` | 1.5px `--rule`: lifelines, weak links, replies |
| `.dg-line.dash` | Dashed (8/6) |
| `.dg-line.key` | Clay |
| `.dg-line.axis` | 1.5px slate: chart axis and ticks [24] |
| `.dg-t` | Component name: mono 26px 500 slate, tracking .06em |
| `.dg-t.acc` | Annotation: mono 20px slate |
| `.dg-t.mut` | Annotation: mono 20px `--ink2` |
| `.dg-t.key` | Clay text |
| `.dg-fill-0` | `--rule` bar segment |
| `.dg-fill-1` | `--ink2` bar segment |
| `.dg-fill-2` | Slate bar segment |
| `.dg-fill-key` | Clay bar segment |

Write label text in the case you want shown; component names are UPPERCASE by convention, code tokens keep their case. Position text with `x`, `y`, `text-anchor`. In Geist Mono at 20px, one character plus tracking is about 13.6px wide; at 26px it is about 17px. Use this to check that labels fit.

Arrowheads: one marker per style per slide, with a slide-unique `id` (all slides share one document):

```html
<defs>
  <marker id="s09-a" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L12,6 L0,12 Z"/></marker>
  <marker id="s09-k" class="key" …same…><path d="M0,0 L12,6 L0,12 Z"/></marker>   <!-- clay -->
  <marker id="s09-d" class="dim" …same…><path d="M0,0 L12,6 L0,12 Z"/></marker>   <!-- hairline -->
</defs>
<path class="dg-line" d="M240,88 H339" marker-end="url(#s09-a)"/>   <!-- end 1px short of the target edge -->
```

**Charts** are drawn to scale (state the scale in an SVG comment, e.g. "75px per 1k tokens"). Leave 2px ivory gaps between stacked segments. Use a 1.5px slate axis (`<path class="dg-line axis">`) with 10px ticks and 20px mono tick labels, and a legend row of 20 × 20 swatches with mono labels.

### Video placement [20, 21]

Put the video alone in a `.fig`, normally in the right side of a `.split`:

```html
<div class="fig"><video src="media/next-token.mp4" width="1200" height="750" autoplay muted loop playsinline aria-label="What the animation shows"></video></div>
```

- The video fills the figure box (828 × zone height) with `object-fit: contain`, centred both ways. `width`/`height` are the video's own pixel size.
- **No frame, border or background.** The video's ivory ground merges with the slide.
- deck.js restarts the video when its slide opens; `autoplay muted loop playsinline` keeps it running.
- Images (`<img>`) follow the same rules. As of 1.1, `.fig > img` explicitly uses `object-fit: contain; object-position: center`; both dimensions describe the source, not the figure box. The image is never stretched or cropped.

### Image placement [27]

```html
<div class="fig"><img src="media/still.png" width="1200" height="900" alt="What the image shows."></div>
```

The figure fills the zone, while the image is contained inside it with its natural aspect ratio. Kitchen-sink slide 27 demonstrates a 4:3 still inside the wider split figure. Its demo PNG is frame 135 of the Ivory stateless render. Existing third-party screenshots may have a contrasting background; preserve the file and report the mismatch rather than recoloring its content.

### Making animations and other media match (N)

Anything rendered for a slide (animation, chart image, screenshot frame) follows the slide's rules, so it disappears into the slide:

- **Ground exactly `#FAF9F5`**, full frame, no vignette or border. Check in a screenshot that the edge of the video is invisible.
- Flat, outlined shapes: 2px `#141413` strokes, 2px corner radius, ivory fills. No shadows, gradients, glows, 3D or textures.
- Clay `#D97757` on **one** element (the point), clay text `#C6613F`. Everything else slate `#141413`, `#5E5D59`, hairlines `#C9C3B4`.
- Text in Geist / Geist Mono only (the files in `fonts/`), in the case you want shown; mono for labels.
- Orthogonal connectors and small solid arrowheads, as in the diagram idiom. Motion is functional (something moves because the process moves), not decorative.
- Size it for the box it fills: 828 × 562 (or 828 × 480) for a split figure, 1680 wide for a full-width one; any aspect close to that works because it is contained.

---

## 8. Porting an existing deck to Ivory

This is the procedure for converting a deck written in any other style (another CSS theme, a template with icons and dark slides, a slide tool's export) into Ivory.

### Procedure

1. **Inventory.** List every slide: its number, its label/title, the pattern it uses (title, bullets, bullets with bold lead-ins, numbered steps, two/three/four boxes, before/after, table, numeric table, big number, chart, code, terminal output, diagram, image, video, quote, agenda, sources, section divider), how much text it has, and its links and speaker notes.
2. **Map each pattern to one Ivory component** (table below). Note the slides with no equivalent.
3. **Convert.** Start from `template.html`. Per slide: `.slide-head` with the section label; the headline as `h2` (two lines at most); one component in `.zone`; the footnote as `.note`. Copy text, links and notes verbatim. Pick the size step by the rules in §4. Redraw diagrams at 1:1 with the diagram classes (§7); re-render videos and images to the media rules.
4. **Verify.** Screenshot every slide (§10), open each image, run the checklist, fix, repeat. Then check that the content survived (below).

### Pattern → component

| Pattern in the old deck | Ivory |
|---|---|
| Title / cover slide | Title slide [01] |
| Plain bullets | `ul.bul` [10] |
| Bullets with a bold lead-in | `ol.bul.def` (full width) [09] or `ul.bul` with inline `<b>` (in a split) [19] |
| Numbered steps, process | `ol.bul` [11] |
| Agenda, table of contents | `ol.bul.def.wide` [08] |
| 2–4 boxes / cards / columns of text | `.cards` [04, 05, 07] |
| Callout box, highlighted card | `.tile.key` inside a `.cards` [06] |
| Before / after, vague / precise | `.cards.c2` with `.was` + `.key` [06] |
| Table | `.tbl` (+ `.lg`, `.c3`, `.c4`) [12, 13, 26] |
| Numbers with a total | `.tbl.num` + `tr.tot` [14] |
| One big number, cost comparison | `.hero` in `.split.even` [14] |
| Code block | `.code`, one `<span class="l">` per line [15, 16] |
| Terminal output, log | `.code` with aligned columns and `.a` arrows [17] |
| Bullets + diagram/image side by side | `.split` [18–21] |
| Diagram above bullets | `.split`, or full-width `.fig` with the bullets moved to the footnote or notes |
| Full-width diagram or chart | `.fig` (+ `.lab` caption) [22–24] |
| Video, animation | `.fig > video` [20, 21] |
| Sources, further reading | `.links` [25] |
| Kicker or tag above a headline | The header `.crumb` |

**Patterns with no equivalent** (section dividers, quotes, thank-you slides, glossaries, icon grids, pills/badges, timelines): do not invent a new look. In order of preference: (a) restructure into an existing component (a quote becomes the headline plus a `.note` with the attribution; a glossary becomes `ol.bul.def` or a `.tbl`; a timeline becomes `ol.bul` or a diagram; badges become mono `.lab` labels); (b) fold it into a neighbour (a section divider becomes the next slide's `.crumb`); (c) move it to the speaker notes. If a new component is truly needed, build it from the tokens in `styles.css`, add a slide for it to `kitchen-sink.html`, screenshot it into `shots/`, and document it here.

### Delete

- Every other stylesheet and font `<link>` (Google Fonts, icon fonts, the old theme).
- Every inline `<style>` block and inline `style` on slide elements (exceptions: `--v` on bars and axis ticks; a `--deck-total` line if you want one).
- Dark/light/theme classes on slides, entrance-animation classes, background images, decorative elements (icons, emoji, illustrations, dots, gradients, shadows).
- Any per-deck runtime script that duplicates deck.js: notes panel, presenter window, fullscreen toggle, video restart, slide-number counters, and their markup. Keep scripts that are genuinely slide content (an interactive demo).
- Any other slide engine (reveal.js, an older deck-stage copy). Slides become direct `<section>` children of `<deck-stage>`.

### Content preservation

- **Wording, speaker notes, link targets, slide order and slide labels stay unchanged.** Converting a deck is a design change, not an edit.
- If text does not fit, change the component or the size step, not the words. If it still does not fit (a headline over two lines, a code line over the character limit, a footnote over one line), stop and report the slide rather than rewriting it silently.
- Keep every slide. Keep `data-speaker-notes` byte for byte.
- After converting, compare old and new: extract each slide's visible text, `href`s and notes from both files and diff them; the only expected differences are added mono labels (`01`, `Before`) and removed decoration.

---

## 9. Using Ivory outside plain HTML decks

If the target project uses Slidev, reveal.js, Marp, a React/MDX deck tool or a PPTX generator, implement Ivory in that tool rather than embedding these files.

**Carry over** the normative values and rules: colours, the two font families and their weights, the size steps and type table (§3), the 1920 × 1080 canvas, 12-column grid and fixed coordinates (§4), the zone rules (one component per zone, filling it), the footnote and source-line rules, the accent rule (§5), the component anatomy (§6: hairline rows, full-height cells, mono labels, code panel numbering), the diagram idiom and media rules (§7), and the do/don't list (§11).

**Do not copy** `deck-stage.js` or `deck.js`: they are the runtime for plain HTML decks and will fight the tool's own navigation, scaling, notes and presenter view. Use the tool's equivalents. `styles.css` can be a starting point in CSS-based tools (copy the token block, the `@font-face` rules with `fonts/`, and the component rules whose markup you can reproduce), but check every selector against the tool's DOM.

Tool notes:

- **Canvas.** Make the tool's slide canvas 1920 × 1080 so the coordinates apply unchanged: reveal.js `width: 1920, height: 1080, margin: 0`; Slidev `canvasWidth: 1920` with a 16/9 aspect ratio; Marp a theme with a 1920 × 1080 size.
- **Fonts.** Web-based tools: use `fonts/` and the `@font-face` rules. PowerPoint/Keynote cannot use woff2: install Geist and Geist Mono (TTF/OTF from the Geist project, same SIL OFL licence) or embed them.
- **PPTX.** A 13.333 × 7.5 in slide is 1920 × 1080 at 144 px per inch, so 1px = 0.5pt: 30px → 15pt, 40px → 20pt, 78px → 39pt, 20px labels → 10pt, hairline 1px → 0.5pt. Place text boxes at the fixed coordinates with zero internal padding.

**Acceptance target in every case:** rebuild the kitchen-sink content in the target tool and compare each slide side by side with `shots/ks-NN.png`. Layout, coordinates, sizes and colours should match within a few pixels; the reference screenshots win any disagreement with prose.

---

## 10. Verification

### Screenshots: `tools/shoot.sh`

```sh
ivory_design_system/tools/shoot.sh talk.html /tmp/talk          # every slide → /tmp/talk/01.png …
ivory_design_system/tools/shoot.sh talk.html /tmp/talk 7 9      # slides 7–9
ivory_design_system/tools/shoot.sh --pdf talk.html /tmp/talk.pdf
```

- Writes `<out-dir>/NN.png` at 1920 × 1080. Without `last` it counts the slides by rendering the deck.
- Finds Chrome at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`, then `google-chrome`/`chromium` on `PATH`; set `CHROME=/path/to/chrome` to override. Exits non-zero with a message if Chrome or the deck is missing, or a shot fails.
- Environment options: `QUERY=chrome` or `QUERY=pw` (screenshot hooks, below), `OFFLINE=1` (block all network access), `BUDGET=6000` (virtual time per shot, ms), `CHROME_LOG=/tmp/chrome.log` (keep Chrome's stderr, including console messages).
- The recipe it encodes (do not change it without re-checking `shots/`): `--headless=new`, a 1920 × 1080 window, `?_snthumb=1` (deck-stage's own switch that hides the thumbnail rail; without it the slide is letterboxed next to the rail), `#N` to pick the slide (1-based), a virtual time budget so fonts and videos settle, and **no `--disable-gpu`**: on the software path Chrome renders full-range ivory videos as pure white.
- **Notes panel and presenter window:** `QUERY=chrome tools/shoot.sh kitchen-sink.html /tmp/c 9 9` shows the buttons and the open notes panel (compare `shots/ks-chrome-notes-clear.png`; the original `ks-chrome-notes.png` is retained as the pre-fix baseline); `QUERY=pw tools/shoot.sh kitchen-sink.html /tmp/p 14 14` renders the presenter window in the page (compare `shots/ks-chrome-presenter.png`; the clock and timer differ).
- **Long notes [28]:** `QUERY=chrome tools/shoot.sh kitchen-sink.html /tmp/notes 28 28` exercises scrolling notes. The panel reserves `var(--gap)` (72px) at the bottom for controls. Its heading stays fixed within the panel; only `.pui-nbody` scrolls. Confirm the final sentence remains reachable above the buttons. Compare `shots/ks-chrome-long-notes.png` and `shots/ks-chrome-long-notes-end.png`.
- **Console errors:** run with `CHROME_LOG=/tmp/chrome.log`, then `grep CONSOLE /tmp/chrome.log` should print nothing.
- **Print:** the PDF has one page per slide, 1440 × 810 pt (= 1920 × 1080 px); slides marked `data-deck-skip` are left out. The kitchen sink gives 28 pages. Check the count with e.g. `pdfinfo out.pdf` (poppler) and open a page or two.

### Regression check of the design system itself

The original 26 kitchen-sink slides retain their historical `/ 26` counters so their regression images remain comparable when examples are appended. Image sample 27 retains `/ 27`; added notes sample 28 shows `/ 28`.

After any change to `styles.css`, `deck.js` or the fonts: `tools/shoot.sh kitchen-sink.html /tmp/ks`, then compare each `/tmp/ks/NN.png` with `shots/ks-NN.png` pixel by pixel (e.g. `magick compare -metric AE a.png b.png null:`). Expected: 0 changed pixels, or a handful of anti-aliasing pixels on the title slide; video slides may also differ inside the video box. Open any slide that differs more. Update `shots/` only for intended changes.

### Per-slide checklist

Screenshot every slide and open each image:

1. Header label left, `NN / TT` right, hairline at 108. The headline starts at 172 and is at most 2 lines.
2. The zone starts 72px under the headline and **content reaches 888**: rows and cells end on the bottom hairline, panels touch it.
3. Nothing crosses 888 or the 120px margins. No clipped code lines. No text in the footer except `.note` and `.src`.
4. Only 30px and 40px content text. Labels are mono uppercase.
5. Clay appears on at most one element, and only if that element is the point (§5).
6. Figures are drawn 1:1 with left/right edges on 120/1800 (full) or 972/1800 (split). The video background is invisible.
7. No dark slide, card fill, shadow, icon, pill or rounded box.
8. The footnote is one line (two at most without `.src`).
9. Text is in Geist / Geist Mono, not a fallback font (compare letterforms with `shots/`).

**A slide is not done until its screenshot has been looked at.** Passing markup checks or a clean console is not enough.

---

## 11. Do / don't

**Do**

- Put one component per zone and let it fill the zone.
- Use rows and columns on the 12-column grid, with hairlines between them.
- Use mono for every label, number column, code line and diagram label.
- Write SVGs at 1:1 with grid-aligned boxes, orthogonal lines and slide-unique marker ids.
- Use clay once, for the point, or not at all.
- Keep headlines to one line where possible and two at most. Keep the footnote to one line.
- Give every slide `data-label` and `data-speaker-notes`.
- Leave `.snum` empty (deck.js numbers it), or number by hand and keep it current.
- Keep the folder whole and unchanged; reference it by relative path.

**Don't**

- Add inline `<style>` (beyond an optional `--deck-total` line) or inline `style` on slide elements. The exceptions are `--v` on bars and axis ticks.
- Add font `<link>`s or any other network resource; everything is in the folder.
- Paste notes/presenter/fullscreen scripts or chrome markup into a deck; deck.js provides them.
- Add sizes other than 30/40 for content, or bold whole paragraphs.
- Add filled or tinted boxes (paper is for code panels only), shadows, gradients, icons, emoji, pills, rounded cards, or dark slides.
- Use curved connectors, diagonal arrows, or several clay elements in a diagram.
- Center content vertically in an empty zone, or leave the zone half empty. Pick a component that fills it.
- Put clay in headlines, labels, footnotes or across a set of equal items.
- Edit `deck-stage.js`, or fork `deck.js` per deck.
