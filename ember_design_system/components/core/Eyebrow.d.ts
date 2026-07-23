import * as React from "react";

export interface EyebrowProps {
  /** The label text — keep it short (2–4 words). */
  children: React.ReactNode;
  /** Text color. Defaults to coral; pass a neutral for on-dark variety. */
  color?: string;
  /** Tag to render as. Default "div". */
  as?: keyof JSX.IntrinsicElements;
  style?: React.CSSProperties;
}

/**
 * Ember's signature kicker: uppercase IBM Plex Mono, coral, wide tracking.
 * Always pairs above a Space Grotesk title.
 */
export function Eyebrow(props: EyebrowProps): JSX.Element;
