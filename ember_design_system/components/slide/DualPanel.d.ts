import * as React from "react";

export interface PanelSpec {
  /** Small mono kicker, e.g. "YOU PAY" / "YOU WIN WHEN". */
  label?: React.ReactNode;
  /** Space Grotesk panel title. */
  title?: React.ReactNode;
  /** Body copy. */
  body?: React.ReactNode;
  /** Override the default tone ("light" left / "dark" right). */
  tone?: "light" | "dark";
}

export interface DualPanelProps {
  left: PanelSpec;
  right: PanelSpec;
  /** Grid gap in px. Default 48. */
  gap?: number;
  style?: React.CSSProperties;
}

/**
 * The cream-vs-ink comparison block (tradeoffs, do/don't, before/after).
 * @startingPoint section="Slide blocks" subtitle="Two-up cream/ink compare" viewport="1400x520"
 */
export function DualPanel(props: DualPanelProps): JSX.Element;
