import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Fuentes locales (OFL) en public/fonts — no dependen de internet al renderizar.
export const fontsReady = Promise.all([
  loadFont({ family: "Sora", url: staticFile("fonts/Sora-Variable.ttf"), weight: "100 800" }),
  loadFont({ family: "Inter", url: staticFile("fonts/Inter-Variable.ttf"), weight: "100 900" }),
]);
