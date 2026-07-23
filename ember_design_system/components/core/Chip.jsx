import React from "react";

const VARIANTS = {
  solid: { background: "var(--coral)", color: "var(--ink)", border: "none" },
  outline: { background: "transparent", color: "var(--coral-ink)", border: "2px solid var(--coral)" },
  neutral: { background: "var(--ink)", color: "var(--paper)", border: "none" },
  ghost: { background: "var(--ink-2)", color: "var(--on-dark-muted)", border: "2px solid var(--line-dark)" },
};

/** Compact monospace pill for labels, tags, status, and inline data. */
export function Chip({ children, variant = "solid", style = {} }) {
  const v = VARIANTS[variant] || VARIANTS.solid;
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 8,
        fontFamily: "var(--font-mono)",
        fontWeight: 600,
        fontSize: "var(--fs-mono)",
        lineHeight: 1,
        padding: "10px 18px",
        borderRadius: "var(--radius-pill)",
        whiteSpace: "nowrap",
        ...v,
        ...style,
      }}
    >
      {children}
    </span>
  );
}
