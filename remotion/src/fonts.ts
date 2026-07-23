import { loadFont as loadGrotesk } from "@remotion/google-fonts/SpaceGrotesk";
import { loadFont as loadPlexSans } from "@remotion/google-fonts/IBMPlexSans";
import { loadFont as loadPlexMono } from "@remotion/google-fonts/IBMPlexMono";

const grotesk = loadGrotesk();
const plexSans = loadPlexSans();
const plexMono = loadPlexMono();

// Same roles as the decks' --font-d / --font-b / --font-m
export const fontD = grotesk.fontFamily;
export const fontB = plexSans.fontFamily;
export const fontM = plexMono.fontFamily;
