import React from "react";

const DOTS = ["var(--term-dot-red)", "var(--term-dot-yellow)", "var(--term-dot-green)"];

/** macOS-style terminal window for "what you'd see in Claude Code" views. */
export function TerminalWindow({ title = "claude — ~/project", children, style = {} }) {
  return (
    <div
      style={{
        background: "var(--term-bg)",
        border: "1px solid var(--line-dark-2)",
        borderRadius: "var(--radius-lg)",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        boxShadow: "var(--shadow-terminal)",
        ...style,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 9,
          padding: "15px 20px",
          background: "var(--term-bar)",
          borderBottom: "1px solid var(--line-dark-2)",
        }}
      >
        {DOTS.map((c) => (
          <span key={c} style={{ width: 14, height: 14, borderRadius: "50%", background: c }} />
        ))}
        <span
          style={{
            marginLeft: 14,
            fontFamily: "var(--font-mono)",
            fontWeight: 500,
            fontSize: 22,
            color: "var(--on-dark-faint)",
          }}
        >
          {title}
        </span>
      </div>
      <div
        style={{
          flex: 1,
          padding: "28px 34px",
          fontFamily: "var(--font-mono)",
          fontWeight: 500,
          fontSize: "var(--fs-mono)",
          lineHeight: 1.6,
          color: "var(--code-text)",
        }}
      >
        {children}
      </div>
    </div>
  );
}
