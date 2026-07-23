import React from "react";

/** Coral-wash aside with a heavy left border — for failure modes and key asides. */
export function Callout({ title, children, style = {} }) {
  return (
    <div
      style={{
        background: "var(--coral-soft)",
        borderLeft: "var(--bw-callout) solid var(--coral)",
        borderRadius: "0 var(--radius-md) var(--radius-md) 0",
        padding: "32px 40px",
        ...style,
      }}
    >
      {title ? (
        <div
          style={{
            fontFamily: "var(--font-display)",
            fontWeight: 600,
            fontSize: 26,
            color: "var(--coral-ink)",
            marginBottom: 10,
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
          color: "var(--text-muted)",
          textWrap: "pretty",
        }}
      >
        {children}
      </div>
    </div>
  );
}
