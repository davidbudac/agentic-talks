import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Fonts are bundled in remotion/public/fonts (OFL-licensed latin subsets),
// so renders work offline — no fonts.gstatic.com fetch at render time.
const load = (family: string, slug: string, weights: number[]) =>
  weights.map((weight) =>
    loadFont({
      family,
      url: staticFile(`fonts/${slug}-${weight}.woff2`),
      weight: String(weight),
    }),
  );

const WEIGHTS = [400, 500, 600, 700];
load("Space Grotesk", "space-grotesk", WEIGHTS);
load("IBM Plex Sans", "ibm-plex-sans", WEIGHTS);
load("IBM Plex Mono", "ibm-plex-mono", WEIGHTS);

// Same roles as the decks' --font-d / --font-b / --font-m
export const fontD = "Space Grotesk";
export const fontB = "IBM Plex Sans";
export const fontM = "IBM Plex Mono";
