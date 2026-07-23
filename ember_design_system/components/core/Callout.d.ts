import * as React from "react";

export interface CalloutProps {
  /** Optional bold heading in coral-ink (e.g. "Most common failure mode"). */
  title?: React.ReactNode;
  /** The aside body. */
  children: React.ReactNode;
  style?: React.CSSProperties;
}

/** Coral-wash callout with a 6px left border, for the one caveat that must not be missed. */
export function Callout(props: CalloutProps): JSX.Element;
