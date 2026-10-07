# Ivory conversion report

Completed 17 sibling decks, 282 slides, on `design/ivory-technical`. Each deck has its own commit. The original 30-slide Ivory example was retained. No push was performed. All 138 protected source/content/media hashes match the initial manifest; pre-existing edits and untracked work were neither staged nor committed.

## Per-deck delivery and content removals

Each name links to the detailed report, including its inventory, content comparison, screenshot paths and parent acceptance. Slide numbers below refer to source/result position. **No unfit slide and no unavailable or unconverted media were found in any of the 17 decks.** The image-background clashes are documented separately below.

| Deck | Slides | Commit | Source text/whitespace removed |
|---|---:|---|---|
| [cost-and-context](cost-and-context/report.md) | 17 | `eaafc96` | 01: title dot `.` |
| [ai-toolbox](ai-toolbox/report.md) | 31 | `8ec0225` | 01: title dot and `chat → agent → toolbox ↺` |
| [agentic-ai](agentic-ai/report.md) | 26 | `5841956` | 01: title dot and `model → harness → agent ↺`; 02: one blank code line |
| [subagents-prompt-caching](subagents-prompt-caching/report.md) | 21 | `f18cd4f` | 01: title dot |
| [orchestrating-agents](orchestrating-agents/report.md) | 19 | `8844de3` | 01: title dot |
| [measuring-what-works](measuring-what-works/report.md) | 19 | `97c0f46` | 01: title dot; 06, 11, 17: blank code separator lines |
| [best-practices](best-practices/report.md) | 30 | `6b29524` | 01: title dot |
| [working-smarter](working-smarter/report.md) | 44 | `dfdfc73` | 01: title dot; 06, 10, 39, 41: blank code separator lines |
| [agentic-engineering-reference](agentic-engineering-reference/report.md) | 10 | `d8c992b` | None |
| [ai-toolbox-reference](ai-toolbox-reference/report.md) | 22 | `7d9f7b2` | 06: `⚠`; 17: `🛡` and `⚔`; 18: `⚠` |
| [agentic-ai-reference](agentic-ai-reference/report.md) | 13 | `b6af6d2` | None |
| [subagents-prompt-caching-reference](subagents-prompt-caching-reference/report.md) | 4 | `2f8224e` | 01: title dot |
| [cost-and-context-reference](cost-and-context-reference/report.md) | 4 | `96a2227` | 01: title dot |
| [orchestrating-agents-reference](orchestrating-agents-reference/report.md) | 4 | `d004ffe` | 01: title dot |
| [measuring-what-works-reference](measuring-what-works-reference/report.md) | 5 | `ea70991` | 01: title dot; 05: one blank code line |
| [best-practices-reference](best-practices-reference/report.md) | 5 | `8877872` | 01: title dot |
| [working-smarter-reference](working-smarter-reference/report.md) | 8 | `9c3ea39` | 01: title dot |

Across all decks, handwritten slide numbers were removed from `.snum` and replaced by runtime numbering. This is additional to the per-deck decoration/whitespace removals above. No instructional prose was rewritten or moved into speaker notes. Slide order, `data-label`, `data-origin-slide`, raw `data-speaker-notes`, and link targets are preserved. Links between decks retain original filenames.

Other visible differences are documented per slide in the linked reports: title metadata moved into the Ivory anatomy with an “Author” label on main decks; generated row/card/code counters; reference banners combined into header crumbs with a middle-dot separator; six displayed URL lines on Agentic Engineering reference slide 10, matching the finished example. Line breaks, nonbreaking spaces and extractor joins between term/definition elements explain other comparison differences. Agentic AI reference slide 03 incorporates the same three statistics into its table, with the same wording and values. Blank-line removals in the table above remove whitespace only.

## Visual review: the three weakest slides in each deck

These are accepted design compromises, not overflow findings. Sparse openers and equal cards follow the existing components; dense slides retain their source content. Some static video captures and PDFs show early animation frames.

| Deck | Three weakest slides and why |
|---|---|
| cost-and-context | 12: sparse opening video frame; 11: short paired cards; 17: plain source rows |
| ai-toolbox | 07: sparse stateless opening frame; 30: uneven source columns; 28: busy connection diagram |
| agentic-ai | 06: airy conversation diagram; 18: sparse video opening frame; 25: dense sources |
| subagents-prompt-caching | 12: sparse KV-cache opening frame; 04: sparse subagents opening frame; 18: generated code numbers alongside numbered steps |
| orchestrating-agents | 03: sparse paired cards; 19: plain source rows; 06: wrapped table text |
| measuring-what-works | 09: sparse paired cards; 19: plain source rows; 12: repeated unknown-result cells have no single visual focus |
| best-practices | 17: generated code numbers alongside numbered steps; 07: sparse paired cards; 29: short full-width rows |
| working-smarter | 21: sparse opening video frame; 08: dense 40px table; 02: uneven schedule columns |
| agentic-engineering-reference | 01: sparse opener; 02: unequal card text heights; 09: generated code numbers alongside numbered steps |
| ai-toolbox-reference | 02: tight ten-row glossary; 06: mixed definition lengths; 14: dense eleven-row cheat sheet |
| agentic-ai-reference | 07: dark saturated screenshot dominates; 03: dense table with 20px stat labels; 12: dense thirteen-row sources table |
| subagents-prompt-caching-reference | 01: sparse unequal opener cards; 04: short bottom-aligned cards; 03: airy rows |
| cost-and-context-reference | 01: sparse opener; 03: airy rows; 02: wrapped table row under two-line heading |
| orchestrating-agents-reference | 01: sparse opener; 03: small code, duplicate numbering and blank line; 02: airy linked rows |
| measuring-what-works-reference | 01: sparse opener; 03: source equation alignment and blank lines; 04: airy rows |
| best-practices-reference | 01: sparse opener; 05: airy three-link list; 02: denser wrapped right column |
| working-smarter-reference | 01: sparse opener; 03: airy rows; 02: wrapped table row |

## Media and Stateless

All relevant deck videos use the Ivory variants. Existing MP4 files were not changed or re-rendered. SVG diagrams were redrawn with the existing Ivory diagram classes, orthogonal connections and coordinates matching their figure zones; the detailed inventories identify each conversion.

Agentic AI reference images 06 (Lovable), 07 (Higgsfield), and 08 (HyperFrames) retain their original files. They are contained without distortion at 828 × 517.5 in an 828 × 562 figure. All three dark screenshots visibly contrast with the Ivory ground; slide 07 is the strongest clash. They were not recolored or replaced.

Stateless was committed separately as `07a9c9b`: `remotion/src/Stateless.tsx`, the `stateless-ivory` registration in `Root.tsx`, the new MP4 and verification evidence. It uses the Ivory fonts/theme and radius/stroke helpers; the model outline is the sole clay element. Composition remains 1200 × 900, 30fps, 300 frames. Render command from `remotion/`:

```sh
npx remotion render stateless-ivory ../assets/anim/stateless-ivory.mp4
```

New-render stills at frames [45](stateless/ivory-45.png), [135](stateless/ivory-135.png), and [265](stateless/ivory-265.png) were opened and inspected. Before/after light and dark stills at all three frame positions are byte-identical (six comparisons). TypeScript `noEmit` passed. This samples legacy rendering; it does not prove byte identity for every frame of either full composition. Native Ivory ground is exactly `#FAF9F5`; decoding the compressed MP4 rounds blue up one level, as in the existing subagents Ivory render. [Verification data](stateless/verification.json).

## Shared design-system changes

No new deck component was needed. Two additive corrections were necessary and were committed separately; the design-system version is now **1.1**. No changes were made to `deck-stage.js` or `deck.js`.

- `331727d`: image containment on `.fig > img`, kitchen-sink sample 27, its approved screenshot and documentation. Existing 26-slide regression: **24/26 exactly identical**. Sample 1 differed by 16 pixels and sample 14 by one pixel, all by one RGB level. An old-stylesheet control reproduced nearly all variation; no layout regression was found. The differing images and new sample were opened. [Full report and metrics](ivory-1.1/report.md).
- `1dfdc80`: notes-panel clearance using existing spacing tokens, a fixed heading and scrollable body; kitchen-sink sample 28 and four approved screenshots. Full resumed regression: **24/27 existing samples exactly identical (23/26 original samples)**. Sample 1 differed by 15 one-level pixels; video samples 20/21 differed by 53/6038 pixels inside the video regions only. Non-video content on those two samples was exact. The differing images and new sample were opened. These are rasterization/video-timing deviations, so the requested strict identity of all original 26 images was **not achieved**. [Full report and metrics](notes-panel-fix/report.md).

Both regressions completed with clean console logs and matching kitchen-sink PDF counts (27 and 28). The appended PDF pages were rendered and opened. Original approved screenshots were not overwritten. Notes scrolling was additionally tested in one Chrome session at 1920 × 1080 and 1280 × 720: the body ends 22px above controls, the panel remains within 38vh, and the last sentence is reachable. The previously obscured notes in Measuring What Works reference 03 and Agentic AI reference 06 were recaptured and inspected. [Scroll measurements](notes-panel-fix/scroll-check.json).

## Verification and interruption history

Each deck received two complete screenshot look-and-fix passes; delegated workers opened both passes, and the parent independently opened every final slide plus corrected recaptures. Each deck also has an inspected notes-panel and presenter-window shot, a PDF with the same page count as its source, and clean recorded console checks. Final [aggregate static verification](final-verification.json) confirms 17 decks/282 slides, unchanged metadata and link targets, exactly the three required includes, empty `.snum`, no inline style/script or legacy theme classes, and committed outputs matching working copies.

The screenshot runner now stops on the first failed Chrome invocation (`525271e`). Chrome capture was run sequentially outside the restricted sandbox to avoid the earlier sandbox startup crash loop. Later signal-9 failures interrupted Working Smarter pass 2 and the notes-panel regression. Work stopped and was resumed after user authorization; remaining captures were completed and opened. Memory pressure is a possible explanation, not a confirmed diagnosis. The Working Smarter worker initially masked a failed capture exit through a pipeline and ran PDF/notes/presenter afterward; this procedural exception and the parent's completed recovery are preserved in its report. No automatic retry loop remains in the capture script.

## What was not checked

- Physical projector appearance, other browsers/operating systems, and external URL availability.
- Every PDF page visually: all PDF page counts were checked, but only selected rendered pages were opened; Working Smarter PDF pages were not opened. Slide PNG review covers all slides.
- Every frame of each embedded video, or all 300 legacy Stateless frames; legacy identity was checked at three positions per theme.
- Every notes panel and presenter position in every deck, or a full keyboard/control interaction suite. The required per-deck sample shots and the shared long-note scrolling checks were completed.
- A repeat of all 282 deck screenshots after the final shared notes-only stylesheet correction. The full kitchen-sink regression and affected notes views were checked instead.
- Strict pixel identity for all original kitchen-sink screenshots: the exact exceptions are reported above.
- A confirmed operating-system diagnosis of the signal-9 terminations. Sequential rendering completed after authorized resumption.

Per-deck PNGs, PDFs and Chrome logs are referenced under `/tmp` in the reports and may be removed by the operating system. The content audits, reports, stateless stills, protected-file manifest, regression metrics and newly approved kitchen-sink images are committed in the repository. The root design status table is updated; replacement of original filenames remains a later user operation.
