import React from "react";

/** The 120×4 coral rule used under section titles (and as a generic divider). */
export function AccentBar({
  width = "var(--accent-bar-w)",
  height = "var(--bw-accent)",
  color = "var(--coral)",
  style = {},
}) {
  return <div style={{ width, height, background: color, borderRadius: 2, ...style }} />;
}
