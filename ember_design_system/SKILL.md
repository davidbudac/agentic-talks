---
name: ember-design
description: Use this skill to generate well-branded interfaces, slides, and assets in the Ember design language — a warm, high-contrast presentation & dev-tool aesthetic (near-black "ink", cream "paper", a single vivid coral accent; Space Grotesk + IBM Plex). Use for production work or throwaway prototypes, mocks, and decks. Contains design guidelines, color/type/spacing tokens, fonts, reusable components, and slide archetypes.
user-invocable: true
---

Read the `readme.md` file within this skill first, then explore the other files.

- **Tokens & CSS:** link `styles.css` (it imports all color/type/spacing/effect tokens + fonts). Everything is driven by CSS custom properties — never hardcode hexes; use `var(--coral)`, `var(--ink)`, `var(--paper)`, etc.
- **Foundations:** `guidelines/` holds specimen cards for colors, type, spacing, and brand motifs.
- **Components:** `components/` has React primitives (`Eyebrow`, `Chip`, `AccentBar`, `Callout`, `CodeBlock`, `TerminalWindow`, `DualPanel`, `StatTile`). Read each `.prompt.md` for usage.
- **Slides:** `slides/` holds 1280×720 archetypes (title, section divider, compare, diagram, code, takeaways) — copy one to start a new deck.

If creating visual artifacts (slides, mocks, throwaway prototypes), copy assets out and produce static HTML files for the user to view. If working on production code, copy the tokens and read the rules here to design fluently in the brand.

When invoked without other guidance, ask the user what they want to build, ask a few focused questions, then act as an expert designer who outputs HTML artifacts **or** production code as needed — always honoring Ember's rules: warm ink/paper backgrounds (the pair only), coral as a single accent, borders over shadows, no emoji, sentence-case titles with mono uppercase eyebrows.
