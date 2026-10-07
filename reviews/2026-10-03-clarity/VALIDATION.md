# Validation record

Current status: all nine main decks and nine reference decks pass static checks. Batch 1 is unchanged and retains its original browser evidence. The seven follow-up pairs pass 440 checks; see the follow-up section below. Historical statements in the batch-1 section describe that earlier checkpoint.

## Baseline

- Local HEAD: `51f2e9a3479a864bf1901aa9c8e3bfa4961bcac0`.
- Initial working tree: only pre-existing untracked `workshops/`.
- Prior review counted 418 slides across nine decks and inspected their source content.
- Browser automation was unavailable during the review. This is not visual sign-off.

## Batch 1 — passed, 2026-10-03

| Output | Slides | Static checks | Browser checks |
|---|---:|---|---|
| `agentic-ai.html` | 26 | Pass | Pass at both sizes |
| `ai-toolbox.html` | 31 | Pass | Pass at both sizes |
| `agentic-ai-reference.html` | 13 | Pass | Pass at both sizes |
| `ai-toolbox-reference.html` | 22 | Pass | Pass at both sizes |

Static evidence: [static-results.json](static-results.json). The check verifies output hashes, unique IDs, nonempty notes/labels, printed numbering, stale numbered prose references, inline JavaScript syntax, local resource paths and complete original-to-current slide accounting. Seven untouched decks and the shared runtime/styles match the baseline byte-for-byte. `git diff --check` also passes.

Browser evidence: [browser-results.json](browser-results.json). Isolated headless Chrome via Playwright loaded local files at **1280×720 and 1920×1080** with reduced motion. All **184 slide/viewport combinations** passed the checked content bounds. No page exceptions were recorded. Each output passed keyboard Home/Right/End, initial `#3` deep link, current-slide notes, presenter-popup notes, fullscreen entry/exit, and video readiness checks on slides with video.

The checks exposed and verified fixes for incorrect presenter notes on initial deep links and zero-numbered reference covers. Screenshot inspection exposed low-contrast default links; the final outputs use theme-aware underlined links.

Captured 24 representative screenshots under `/private/tmp/agentic-talks-clarity-qa/` (temporary local artifacts). Visually inspected introduction slides 7, 10, 19 and 24; toolbox slides 4, 19 and 24; introduction reference cover; and toolbox reference slides 3 and 20. These cover code, light/dark cards, a close, a reference cover, a table and a two-column reference layout. Final link colours were checked again after the contrast fix.

### Reproduce

From the repository root:

```sh
python3 reviews/2026-10-03-clarity/validate_static.py
PLAYWRIGHT_MODULE=/path/to/installed/playwright node reviews/2026-10-03-clarity/validate_batch1.cjs
git diff --check
```

The browser script requires Chrome and an installed Playwright package; it does not use a personal browser profile or install dependencies. It writes screenshots and browser JSON to the temporary directory above, or to `QA_OUTPUT` when set. Copy the result JSON into this review directory after a successful run.

`apply_batch1.py --write` reproduces the four deck outputs from the baseline. It refuses to overwrite content that differs from the baseline/last recorded output. Normal subsequent editing can happen directly in the HTML; update the manifest and validation workflow deliberately if continuing that way.

### Limits and next checks

- Bounds checks and representative screenshots are not a full accessibility audit or a substitute for rehearsal on the presentation projector.
- Reduced-motion runs check stable layout, not every animated frame, media control or audio track. Live provider/demo execution and timings were not measured.
- External URLs were retained; local resource existence was checked. This batch does not certify all external links or current product claims. Reference catalogues are explicitly dated snapshots and need a factual refresh before reuse as current guidance.
- Other seven decks: unchanged and still queued in the plan. Their previously identified editorial issues remain; they have not been browser-validated in this batch.

## Evidence constraints

- No provider sessions or paid model experiments are authorized or required to edit the talks.
- Do not replace placeholders with invented benchmark results or purported recordings.
- Modern Web Guidance was retrieved after the initial offline/cache attempt, including text-legibility and accessibility guidance. The existing slide canvas and shared design system were retained.

## Follow-up batches 2–3 — passed, 2026-10-03

| Main output | Main slides | Reference slides | Static | Browser |
|---|---:|---:|---|---|
| `agentic-engineering.html` | 30 | 10 | Pass | Both sizes |
| `subagents-prompt-caching.html` | 21 | 4 | Pass | Both sizes |
| `cost-and-context.html` | 17 | 4 | Pass | Both sizes |
| `orchestrating-agents.html` | 19 | 4 | Pass | Both sizes |
| `measuring-what-works.html` | 19 | 5 | Pass | Both sizes |
| `best-practices.html` | 30 | 5 | Pass | Both sizes |
| `working-smarter.html` | 44 | 8 | Pass | Both sizes |

### Current evidence

- [all-static-results.json](all-static-results.json): all 18 deck outputs, 312 slides. Checks hashes, actual counts, labels/notes, numbering, inline JavaScript syntax, local resources, duplicate IDs, absence of unfinished visible copy in the follow-up decks, complete main-slide accounting and mapped origin positions. Independently checks worked cost and growth arithmetic. Batch-1 outputs match their original manifest; shared runtime/styles match the baseline.
- [remaining-browser-results.json](remaining-browser-results.json): 220 follow-up slides at each of **1280×720 and 1920×1080**, totaling **440 slide/viewport checks**. No detected bounds violations, page exceptions or captured console errors. Includes text-range bounds, table cells and content containers as well as element bounds. Keyboard navigation, deep links, current notes, presenter-popup notes, fullscreen and active-slide video readiness passed for all 14 outputs at both sizes.
- [navigation-results.json](navigation-results.json): nine chooser cards have correct counts and existing destinations; no horizontal overflow at 390×844, 1280×720 or 1920×1080. Each of the seven follow-up main decks successfully opens its reference deck and returns through the visible link.
- `git diff --check` passes. The original `workshops/` directory was outside every edit operation. No Git publication or provider experiment was performed.

### Visual inspection

The final browser pass waits for fonts and two animation frames after activation, and disables reveal motion in the test page to inspect final layout. This avoids an initial capture-timing artifact that made one table appear to extend offscreen. A separate settled-layout inspection confirmed its cells and text fit without changing the deck.

Captured 61 representative 1280-wide deck screenshots, three chooser screenshots and additional 1920-wide presentations under `/private/tmp/agentic-talks-remaining-qa/`. Reviewed examples from all seven main decks: engineering model/harness cards and token table; subagent explanation; cost comparison worksheet; orchestration skill structure; measurement worksheet/hardware table; best-practices escalation; workshop acceptance cases. Also inspected reference covers, cache explanation, request anatomy, plugin recipe, cloud-boundary worksheet and the article bibliography. Also reviewed 1920×1080 screenshots of the worked bill, local/cloud map, workshop agenda and grading debrief, plus a mid-animation helper frame. Screenshots are temporary QA artifacts; JSON evidence is retained in this directory.

### Reproduce

```sh
python3 reviews/2026-10-03-clarity/validate_all.py
PLAYWRIGHT_MODULE=/path/to/playwright node reviews/2026-10-03-clarity/validate_remaining.cjs
PLAYWRIGHT_MODULE=/path/to/playwright node reviews/2026-10-03-clarity/validate_navigation.cjs
git diff --check
```

`validate_static.py` now dispatches to the all-batch validator when the remaining-batch manifest exists, rather than incorrectly expecting the seven follow-up decks to remain untouched. The browser scripts use an isolated headless Chrome profile and write only QA artifacts. On this machine the execution sandbox prevented Chrome from starting; the same read-only checks succeeded through the approved escalated tool path.

`apply_batch2.py --write` reproduces Agentic Engineering. `apply_remaining.py --write` reproduces the other six decks from the immutable Git baseline and shared content definitions. Both refuse to overwrite files that differ from the baseline or the last recorded output. They do not publish or commit. The complete slide map is in `SLIDE-MAP.md`; per-batch JSON and baseline hashes make the dispositions auditable.

### Evidence limits and preparation

- This is editorial and browser validation, not measured model-performance evidence. The bill, transcripts, grader outputs and hardware scenarios are explicitly illustrative. `exercise-materials.md` includes the fixtures, expected answers and blank measurement fields.
- Optional live runs need a prepared disposable repository, actual tests, approved credentials, usage capture and rehearsal. The static workshop path requires none of these and has no empty recording placeholders.
- The selected primary docs for cache rules, helper inheritance, authentication, evaluation, skills/plugins, tool interfaces and memory/offloading were checked. This is not a complete current vendor-price, product-feature or external-link audit. Old catalogue claims were removed or replaced by worksheets; batch-1 historical reference catalogues remain dated.
- Reduced-motion layout and sampled media inspection do not certify every animation frame, audio behavior, browser, projector or assistive-technology interaction.
- Subagents now uses the shared Ember renderer and adjacent assets. The original bundled file is preserved in the baseline commit. Retained cache animation price labels are explicitly qualified on the slide as illustrative, not universal rates.
