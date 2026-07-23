import React from "react";

/** Small mono category label that sits above a slide/section title. */
export function Eyebrow({ children, color = "var(--coral)", as = "div", style = {} }) {
  const Tag = as;
  return (
    <Tag
      style={{
        fontFamily: "var(--font-mono)",
        fontWeight: 600,
        fontSize: "var(--fs-eyebrow)",
        letterSpacing: "var(--track-eyebrow)",
        textTransform: "uppercase",
        color,
        ...style,
      }}
    >
      {children}
    </Tag>
  );
}
