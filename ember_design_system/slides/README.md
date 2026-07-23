# Ember — slide archetypes

Standalone 1280×720 slide starting points, in the Ember language. Each is plain HTML linking `../styles.css`, so you can copy one into a new deck and edit text in place. They also seed new designs via the **Starting Points** picker.

| File | Archetype | Background |
|---|---|---|
| `title.html` | Deck opener — coral quarter-circle, hero title | ink |
| `section-divider.html` | Part marker — giant coral numeral + rule | ink |
| `compare.html` | Two-up tradeoff — cream + ink panels | paper |
| `diagram.html` | Three-beat flow with arrows | paper |
| `code.html` | Code walkthrough, one coral key line | ink |
| `takeaways.html` | Numbered 2×2 recap grid | ink |

**Rhythm:** alternate ink and paper backgrounds; reserve ink for section dividers, big diagrams, and code. Keep to the ink/paper pair — coral is an accent only.

**Building a full deck?** Drop these `<section>`s into the `deck-stage.js` shell (see `Subagents and Prompt Caching.dc.html` in this project) at 1920×1080 — multiply every size here by 1.5 to return to slide-native scale, or just use the deck's slides directly as reference.
