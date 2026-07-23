A trimmed, presentation-grade code block on the deep ink-3 ground — highlight the one line that matters with `highlight`.

```jsx
<CodeBlock>
  <CodeLine><span style={{ color: "var(--code-keyword)" }}>def</span> run_subagent(task):</CodeLine>
  <CodeLine indent={1}>resp = client.messages.create(</CodeLine>
  <CodeLine indent={2}>
    system=SUBAGENT_SYSTEM,<span style={{ color: "var(--code-comment)" }}> # cached prefix</span>
  </CodeLine>
  <CodeLine highlight indent={1}>
    <span style={{ color: "var(--code-keyword)" }}>return</span> resp.content[<span style={{ color: "var(--code-number)" }}>0</span>].text
  </CodeLine>
</CodeBlock>
```

- Color syntax by wrapping spans in the `--code-*` tokens. Keep snippets short — trim to the teaching lines.
- Use exactly one `highlight` line per block (the point you're making).
