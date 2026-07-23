import React from "react";

function Panel({ label, title, body, tone = "light" }) {
  const dark = tone === "dark";
  return (
    <div
      style={{
        background: dark ? "var(--ink)" : "var(--paper-2)",
        border: dark ? "none" : "2px solid var(--line-card)",
        borderRadius: "var(--radius-xl)",
        padding: "38px 42px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {label ? (
        <div
          style={{
            fontFamily: "var(--font-mono)",
            fontWeight: 600,
            fontSize: "var(--fs-eyebrow)",
            letterSpacing: "var(--track-label)",
            color: dark ? "var(--coral)" : "var(--coral-ink)",
            marginBottom: 20,
          }}
        >
          {label}
        </div>
      ) : null}
      {title ? (
        <div
          style={{
            fontFamily: "var(--font-display)",
            fontWeight: 700,
            fontSize: "var(--fs-title)",
            letterSpacing: "-0.02em",
            color: dark ? "var(--on-dark)" : "var(--text-strong)",
            marginBottom: 14,
          }}
        >
          {title}
        </div>
      ) : null}
      <div
        style={{
          fontFamily: "var(--font-body)",
          fontWeight: 400,
          fontSize: "var(--fs-body)",
          lineHeight: 1.5,
          color: dark ? "var(--on-dark-muted)" : "var(--text-muted)",
          textWrap: "pretty",
        }}
      >
        {body}
      </div>
    </div>
  );
}

/** Two side-by-side panels — Ember's compare pattern. Left cream, right ink by default. */
export function DualPanel({ left, right, gap = 48, style = {} }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap, ...style }}>
      <Panel tone="light" {...left} />
      <Panel tone="dark" {...right} />
    </div>
  );
}
