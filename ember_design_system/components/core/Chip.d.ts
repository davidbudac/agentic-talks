import * as React from "react";

export interface ChipProps {
  children: React.ReactNode;
  /**
   * solid   — coral fill, ink text (default; the spotlight pill)
   * outline — coral border on transparent (light surfaces)
   * neutral — ink fill, paper text (data tokens on light)
   * ghost   — raised dark pill, for on-dark surfaces
   */
  variant?: "solid" | "outline" | "neutral" | "ghost";
  style?: React.CSSProperties;
}

/** Monospace pill. Use for diagram labels, token counts, and "● HAPPENS HERE" markers. */
export function Chip(props: ChipProps): JSX.Element;
