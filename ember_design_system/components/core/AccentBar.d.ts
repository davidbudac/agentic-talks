import * as React from "react";

export interface AccentBarProps {
  /** Bar length. Default 120px (--accent-bar-w). */
  width?: string | number;
  /** Bar thickness. Default 4px (--bw-accent). */
  height?: string | number;
  /** Default coral. */
  color?: string;
  style?: React.CSSProperties;
}

/** The short coral rule that anchors a section title. */
export function AccentBar(props: AccentBarProps): JSX.Element;
