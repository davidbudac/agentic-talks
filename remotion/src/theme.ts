// Ember palette — mirrors the CSS variables in the slide decks' :root /.slide scopes.
export type ThemeName = "light" | "dark" | "ivory";

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
  // --- style switches (light/dark values reproduce the original hard-coded look) ---
  radiusScale: number; // multiplies every corner radius (0 = squared off)
  strokeScale: number; // multiplies every stroke width
  strokeHot: string; // accent colour for strokes (arrows, active outlines)
  flow: string; // colour of static (non-highlighted) arrows
  dot: string; // the "result travelling back" marker
  onPositive: string; // text on `positive` fills
  hotFilled: boolean; // true: highlighted nodes are filled `coral`; false: outlined only
  flat: boolean; // true: no halos, no translucent fills
  bold: number; // heading weight
  monoWeight: number; // mono label weight
  upperLabels: boolean; // mono captions in uppercase
  monoTracking: number; // letter-spacing (px, svg user units) on mono labels
  caption: string; // closing caption colour
  captionWeight: number;
  quiet: string; // secondary accent-ish labels ("THE LOOP", "delegate")
  geistGlyphs: boolean; // "01" instead of circled digits; avoid glyphs missing from Geist (✓ →)
}

// Helpers: identity for light/dark (scale 1), squared/thin for ivory.
export const rad = (t: Theme, r: number): number => r * t.radiusScale;
export const sw = (t: Theme, w: number): number => w * t.strokeScale;

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
    strokeHot: "#ff5c35",
    onPositive: "#ffffff",
    radiusScale: 1,
    strokeScale: 1,
    flow: "#ff5c35",
    dot: "#3fb950",
    flat: false,
    hotFilled: true,
    bold: 700,
    monoWeight: 500,
    upperLabels: false,
    monoTracking: 0,
    geistGlyphs: false,
    caption: "#b9361a",
    captionWeight: 700,
    quiet: "#b9361a",
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
    strokeHot: "#ff5c35",
    onPositive: "#16130e",
    radiusScale: 1,
    strokeScale: 1,
    flow: "#ff5c35",
    dot: "#3fb950",
    flat: false,
    hotFilled: true,
    bold: 700,
    monoWeight: 500,
    upperLabels: false,
    monoTracking: 0,
    geistGlyphs: false,
    caption: "#ff5c35",
    captionWeight: 700,
    quiet: "#ff5c35",
  },
  // "Ivory Technical": ivory ground, slate ink, one clay accent. Flat, squared, hairlines.
  ivory: {
    bg: "#FAF9F5",
    cardBg: "#FAF9F5", // boxes are outlined, not filled
    cardBorder: "#141413",
    midFill: "#FAF9F5",
    midStroke: "#141413",
    text: "#141413",
    muted: "#5E5D59",
    faint: "#87867F",
    accent: "#C6613F", // clay for text
    coral: "#D97757", // clay for fills
    onHot: "#141413",
    line: "#C9C3B4",
    lineStrong: "#C9C3B4",
    outerFill: "#F0EEE6",
    positive: "#141413", // light/dark: green "cached" fill -> slate
    warning: "#141413", // light/dark: amber (runner-up bar, churn gauge) -> slate
    bar: "#C9C3B4",
    strokeHot: "#C6613F", // clay for strokes
    flow: "#141413",
    dot: "#C6613F",
    onPositive: "#FAF9F5",
    radiusScale: 0,
    strokeScale: 0.55,
    flat: true,
    hotFilled: false,
    bold: 600,
    monoWeight: 400,
    upperLabels: true,
    monoTracking: 0.6,
    geistGlyphs: true,
    caption: "#141413", // one clay element per figure: captions are slate
    captionWeight: 500,
    quiet: "#5E5D59",
  },
};
