// Ember palette — mirrors the CSS variables in the slide decks' :root /.slide scopes.
export type ThemeName = "light" | "dark";

export interface Theme {
  bg: string;
  cardBg: string;
  cardBorder: string;
  midFill: string;
  midStroke: string;
  text: string;
  muted: string;
  faint: string;
  accent: string; // --s-accent (coral-ink on light, coral on dark)
  coral: string;
  onHot: string; // text on coral fills
  line: string;
  lineStrong: string;
  outerFill: string;
  positive: string;
  warning: string;
  bar: string;
}

export const themes: Record<ThemeName, Theme> = {
  light: {
    bg: "#f4efe6",
    cardBg: "#efe7d8",
    cardBorder: "#d8ccb6",
    midFill: "#e3d9c6",
    midStroke: "#cbbfa9",
    text: "#16130e",
    muted: "#5c5446",
    faint: "#a39684",
    accent: "#b9361a",
    coral: "#ff5c35",
    onHot: "#16130e",
    line: "#ddd2bf",
    lineStrong: "#cbbfa9",
    outerFill: "#ffe9e2",
    positive: "#3fb950",
    warning: "#d9a441",
    bar: "#ddd0ba",
  },
  dark: {
    bg: "#16130e",
    cardBg: "#1c1812",
    cardBorder: "#3a342a",
    midFill: "#1c1812",
    midStroke: "#3a342a",
    text: "#f4efe6",
    muted: "#cabfac",
    faint: "#8a7f6d",
    accent: "#ff5c35",
    coral: "#ff5c35",
    onHot: "#16130e",
    line: "#2c281f",
    lineStrong: "#3a342a",
    outerFill: "rgba(255,92,53,.10)",
    positive: "#3fb950",
    warning: "#d9a441",
    bar: "#46402f",
  },
};
