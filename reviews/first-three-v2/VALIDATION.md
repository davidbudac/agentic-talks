# Validation — first three talks v2

22 September 2026. The new decks contain 28, 26 and 32 slides respectively.

## Completed checks

| Check | Result |
|---|---|
| Original three decks | SHA-256 matches the pre-edit snapshots |
| Pre-existing edits in `.claude/launch.json` and `cost-and-context.html` | SHA-256 matches the pre-edit snapshots; excluded from this commit |
| Reproducible generation | Rebuilding produces identical new HTML files |
| Slide structure | Unique IDs, nonempty labels and speaker notes; sequential numbering |
| Local resources | Referenced files, media, posters and fonts exist |
| Inline JavaScript | Extracted scripts pass `node --check` |
| Chrome at 1280×720 | All 86 slides rendered and captured; no clipped text or content outside the slide |
| Chrome at 1920×1080 | All 86 slides rendered and captured; no clipped text or content outside the slide |
| Navigation | Home, arrows and Space; fresh-load `#8` deep link |
| Notes and presenter | Notes match the deep-linked slide; presenter previews open and navigation updates the main deck |
| Reduced motion | Media stays paused unless explicitly started |
| Play/pause controls | Buttons tested with real clicks; accessible state follows playback |
| Normal-motion media | Active loop plays; leaving its slide pauses it |
| Offline file loading | All three decks load from `file://` with local fonts and working deep links |
| Chooser and worked report | Rendered at 1280px and 390px widths; no horizontal overflow |
| Invoice `before/` fixture | 3 tests, 2 expected failures; exit 1 |
| Invoice/export `after/` fixture | 5 tests pass; exit 0 |
| Exported CSV | Customer strings and totals checked after parsing, including comma, quotes and newline |
| Copy | Under 60 visible words per new slide; model-price grids and guaranteed-success claims removed |

## Visual review

Reviewed all slides in the [contact sheets](contact-sheets/), plus full-size views of the prompt, acceptance table, media slide, chooser and worked report. The new decks keep the original Ember palette and type families with more space and less text. Diagram video controls sit below the video so they do not cover labels. Video token counts are explicitly illustrative.

The browser report is [browser-results.json](browser-results.json). Full-resolution screenshots were generated in `/private/tmp/agentic-talks-v2-qa`; contact sheets are retained in the repository.

## Test interpretation

The first layout probe reported font ascenders extending beyond short heading line boxes. Those boxes do not clip their content. The final probe checks slide bounds, actual clipping ancestors and overflowing constrained containers; it does not treat visible glyph overhang as hidden text.

Video requests cancelled on navigation are recorded separately from failures. The final QA server supports byte ranges so media seeking can be checked against decoded frames. This is an improvement to the test setup, not a claim that a completed download proves playback.

## Boundaries

- Browser rendering was checked in installed Chrome; this is not a physical-projector or all-browser certification.
- The optional live agent was not run against a paid service. The checked-in before/after fixtures and their test results are the prepared fallback, clearly labelled on slides and in notes.
- Product/source review covers the retained claims and links in the v2 editions. It does not validate every feature, plan, account setting or claim in the preserved originals and later decks.
- The invoice code is a small teaching fixture with explicit assumptions, not production billing software.
- Commit and push publish to the current branch. No merge to another branch or independent live-site deployment is implied.
