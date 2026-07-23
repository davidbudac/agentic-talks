Tiny uppercase mono kicker that labels the topic of a slide or section — always sits directly above the title.

```jsx
<Eyebrow>Where it actually happens</Eyebrow>
<h2 style={{ font: "700 64px var(--font-display)", letterSpacing: "-0.025em", margin: "14px 0 0" }}>
  Caching lives in the cloud
</h2>
```

- Default color is coral; pass `color="var(--on-dark-faint)"` for a quieter kicker on busy dark slides.
- Keep it to a few words — it is a category, not a sentence.
