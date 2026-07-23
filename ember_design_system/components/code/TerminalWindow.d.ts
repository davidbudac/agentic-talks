import * as React from "react";

export interface TerminalWindowProps {
  /** Title-bar text — typically the working directory, e.g. "claude — ~/acme-api". */
  title?: string;
  /** Monospace transcript content. */
  children: React.ReactNode;
  style?: React.CSSProperties;
}

/** Terminal chrome (traffic lights + title bar + mono body) for Claude Code transcript mockups. */
export function TerminalWindow(props: TerminalWindowProps): JSX.Element;
