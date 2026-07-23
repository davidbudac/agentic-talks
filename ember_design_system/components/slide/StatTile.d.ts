import * as React from "react";

export interface StatTileProps {
  /** The headline number/value, e.g. "5 min", "486,500". */
  value: React.ReactNode;
  /** Quiet caption under the value. */
  label: React.ReactNode;
  /** Surface tone. Default "dark". */
  tone?: "light" | "dark";
  /** Render the value in coral. */
  accent?: boolean;
  style?: React.CSSProperties;
}

/** A single big-number tile (TTL values, token counts, headline metrics). */
export function StatTile(props: StatTileProps): JSX.Element;
