import React from "react";

/** Big-number stat tile — a value in Space Grotesk over a quiet label. */
export function StatTile({ value, label, tone = "dark", accent = false, style = {} }) {
  const dark = tone === "dark";
  return (
    <div
      style={{
        background: dark ? "var(--ink)" : "var(--paper-2)",
        borderRadius: "var(--radius-lg)",
        padding: "34px 38px",
        ...style,
      }}
    >
      <div
        style={{
          fontFamily: "var(--font-display)",
          fontWeight: 700,
          fontSize: 80,
          lineHeight: 1,
          letterSpacing: "-0.02em",
          color: accent ? "var(--coral)" : dark ? "var(--on-dark)" : "var(--text-strong)",
        }}
      >
        {value}
      </div>
      <div
        style={{
          marginTop: 10,
          fontFamily: "var(--font-body)",
          fontWeight: 400,
          fontSize: "var(--fs-body-sm)",
          color: dark ? "var(--on-dark-muted)" : "var(--text-muted)",
        }}
      >
        {label}
      </div>
    </div>
  );
}
