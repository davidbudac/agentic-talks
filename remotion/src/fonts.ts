import { loadFont as loadGrotesk } from "@remotion/google-fonts/SpaceGrotesk";
import { loadFont as loadPlexSans } from "@remotion/google-fonts/IBMPlexSans";
import { loadFont as loadPlexMono } from "@remotion/google-fonts/IBMPlexMono";
import { loadFont as loadGeist } from "@remotion/google-fonts/Geist";
import { loadFont as loadGeistMono } from "@remotion/google-fonts/GeistMono";
import type { ThemeName } from "./theme";

const grotesk = loadGrotesk();
const plexSans = loadPlexSans();
const plexMono = loadPlexMono();

// Same roles as the decks' --font-d / --font-b / --font-m
export const fontD = grotesk.fontFamily;
export const fontB = plexSans.fontFamily;
export const fontM = plexMono.fontFamily;

export interface Fonts {
  fontD: string;
  fontB: string;
  fontM: string;
}

// Geist is only requested when an "ivory" composition asks for it, so
// light/dark renders never wait on (or change because of) the extra fonts.
let ivoryFonts: Fonts | null = null;
const getIvoryFonts = (): Fonts => {
  if (!ivoryFonts) {
    const geist = loadGeist("normal", { weights: ["400", "500", "600"], subsets: ["latin"] });
    const geistMono = loadGeistMono("normal", { weights: ["400", "500"], subsets: ["latin"] });
    ivoryFonts = {
      fontD: geist.fontFamily,
      fontB: geist.fontFamily,
      fontM: geistMono.fontFamily,
    };
  }
  return ivoryFonts;
};

export const fontsFor = (theme: ThemeName): Fonts =>
  theme === "ivory" ? getIvoryFonts() : { fontD, fontB, fontM };
