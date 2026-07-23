import React from "react";

/** Dark code ground (ink-3), monospace, generous leading. Compose with <CodeLine>. */
export function CodeBlock({ children, style = {} }) {
  return (
    <div
      style={{
        background: "var(--code-bg)",
        border: "1.5px solid var(--line-dark-2)",
        borderRadius: "var(--radius-lg)",
        padding: "30px 0",
        fontFamily: "var(--font-mono)",
        fontWeight: 500,
        fontSize: "var(--fs-mono)",
        lineHeight: 1.65,
        color: "var(--code-text)",
        overflow: "hidden",
        ...style,
      }}
    >
      {children}
    </div>
  );
}

/** One line inside a <CodeBlock>. `highlight` paints the coral key-line treatment. */
export function CodeLine({ children, highlight = false, indent = 0, style = {} }) {
  const padLeft = 36 + indent * 16;
  return (
    <div
      style={{
        paddingTop: 2,
        paddingBottom: 2,
        paddingRight: 36,
        paddingLeft: highlight ? padLeft - 3 : padLeft,
        background: highlight ? "rgba(255,92,53,0.12)" : "transparent",
        borderLeft: highlight ? "3px solid var(--coral)" : "3px solid transparent",
        ...style,
      }}
    >
      {children}
    </div>
  );
}
