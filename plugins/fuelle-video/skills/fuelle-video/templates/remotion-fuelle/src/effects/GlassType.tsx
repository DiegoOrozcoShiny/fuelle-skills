import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { fitText } from "@remotion/layout-utils";
import { C, FONT, SAFE, SAFE_W, POSTER_COMPRESS } from "../brand";

/** GLASS TYPE — tipografía gigante detrás de un bloque de vidrio esmerilado que se desliza; dentro del vidrio el texto se ve desenfocado. */
export const GlassType: React.FC<{ text: string; y: number; size?: number; dark?: boolean; durationInFrames: number; glassW?: number; glassH?: number; label?: string }> = ({
  text, y, size = 260, dark = true, durationInFrames, glassW = 520, glassH = 380, label,
}) => {
  const frame = useCurrentFrame();
  // el texto nunca sale del área segura: tamaño = min(size, el que cabe en la línea más ancha)
  const fit = Math.min(size, ...text.split("\n").map((l) => fitText({ text: l, withinWidth: SAFE_W / POSTER_COMPRESS, fontFamily: FONT.display, fontWeight: "800" }).fontSize));
  const gx = interpolate(frame, [0, durationInFrames], [SAFE.x0, SAFE.x1 - glassW], { extrapolateRight: "clamp" });
  return (<>
    <div style={{ position: "absolute", left: SAFE.x0, top: y, fontFamily: FONT.display, fontWeight: 800, fontSize: fit, lineHeight: 0.86,
      color: dark ? C.marfil : C.carbon, transform: `scaleX(${POSTER_COMPRESS})`, transformOrigin: "left top", whiteSpace: "pre" }}>{text}</div>
    <div style={{ position: "absolute", left: gx, top: y - 40, width: glassW, height: glassH,
      backdropFilter: "blur(18px) saturate(1.2)", WebkitBackdropFilter: "blur(18px)",
      background: dark ? "rgba(247,243,234,0.10)" : "rgba(255,255,255,0.25)",
      border: `4px solid ${dark ? "rgba(247,243,234,.7)" : C.carbon}`, boxShadow: `14px 14px 0 ${C.naranja}` }}>
      <div style={{ position: "absolute", left: 18, top: 14, width: 120, height: 6, background: "rgba(255,255,255,.7)" }} />
      {label && <div style={{ position: "absolute", left: 22, bottom: 18, fontFamily: FONT.text, fontWeight: 600, fontSize: 24, letterSpacing: 3, color: dark ? C.marfil : C.carbon }}>{label}</div>}
    </div>
  </>);
};
