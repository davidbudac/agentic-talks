# Ivory 1.1 image containment

The existing figure image rule stretched images to the full figure dimensions. Added `.fig>img{object-fit:contain;object-position:center}` so source proportions are preserved, matching the existing video behavior and section 7. No runtime changes.

Added kitchen-sink example 27 using a byte-identical copy of the approved stateless frame 135, its screenshot, and documentation. Original 26 sample counters retain their historical total for comparison; the appended sample shows 27 / 27. Original approved screenshots are unchanged.

## Verification

- Full 27-slide capture: `CHROME_LOG=/tmp/ivory11-ks.log ivory_design_system/tools/shoot.sh ivory_design_system/kitchen-sink.html /tmp/ivory11-ks`.
- Pixel comparison: 24 of the original 26 samples are exactly identical. Slide 1 differs by 16 pixels and slide 14 by 1 pixel, each by one RGB level only. Thus the result is visually unchanged, but **not strictly pixel-identical on all 26**. Metrics are in `regression.json`.
- Old-stylesheet control: slide 1 already differs from its approved image by 15 pixels (one level), and slide 14 by the same one pixel. New versus old slide 14 is exactly identical; slide 1 differs by three one-level text-edge pixels. This isolates existing rasterization variation; no layout or color-token regression was found. Parent opened the differing slides and the new sample.
- PDF: `/tmp/ivory11-kitchen-sink.pdf`, 27 pages, 1440 × 810 pt. Parent opened rendered page 27 and checked image proportions and layout.
- Console: no CONSOLE entries in the capture, control or PDF logs. All Chrome operations ran sequentially outside the restricted sandbox and completed successfully.
- Agentic AI reference image slides 6–8 recaptured and opened: their 1600 × 1000 images now occupy 828 × 517.5 within the 828 × 562 figure, centered without distortion. The source screenshots remain unchanged and visibly contrast with the Ivory background.

No existing MP4, source deck, deck-stage.js, or deck.js was changed. This is a scoped media correction; other component layouts were not modified.
