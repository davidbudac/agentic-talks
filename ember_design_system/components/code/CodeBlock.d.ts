import * as React from "react";

export interface CodeBlockProps {
  /** A sequence of <CodeLine> children. */
  children: React.ReactNode;
  style?: React.CSSProperties;
}

export interface CodeLineProps {
  children: React.ReactNode;
  /** Paint the coral key-line highlight (background wash + left border). */
  highlight?: boolean;
  /** Indent level — each step ≈ 2 monospace chars. */
  indent?: number;
  style?: React.CSSProperties;
}

/** The deck's code-slide ground. Color tokens inside spans: --code-keyword / -string / -number / -comment. */
export function CodeBlock(props: CodeBlockProps): JSX.Element;
export function CodeLine(props: CodeLineProps): JSX.Element;
