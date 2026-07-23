A faux macOS terminal for showing "what a user sees in Claude Code" — the product view that complements an API code block.

```jsx
<TerminalWindow title="claude — ~/acme-api">
  <div style={{ color: "var(--paper)" }}><span style={{ color: "var(--coral)" }}>&gt;</span> /cost</div>
  <div style={{ display: "flex", justifyContent: "space-between", maxWidth: 560, marginTop: 8 }}>
    <span style={{ color: "var(--on-dark-faint)" }}>cache read</span>
    <span style={{ color: "var(--coral)", fontWeight: 700 }}>486,500</span>
  </div>
</TerminalWindow>
```

- Mark the user's input line with a coral `>`. Use `⏺` (coral) for tool calls and `⎿` (faint) for results to match Claude Code.
- Sits on a light slide as the hero element — pair it with a side rail of plain-language annotations.
