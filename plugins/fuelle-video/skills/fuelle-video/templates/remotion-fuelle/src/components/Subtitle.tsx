import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { C, FONT, SAFE } from "../brand";

export type Sub = { start: number; end: number; text: string };

/** Subtítulo de la locución: bloque carbón con borde y sombra dura, centrado al fondo del área segura. */
export const Subtitle: React.FC<{ subs: Sub[]; dark: boolean }> = ({ subs, dark }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const cur = subs.find((s) => t >= s.start && t < s.end);
  if (!cur) return null;
  return (
    <div style={{ position: "absolute", left: SAFE.x0, width: SAFE.x1 - SAFE.x0, bottom: 1920 - SAFE.y1 + 8, display: "flex", justifyContent: "center" }}>
      <div style={{
        maxWidth: SAFE.x1 - SAFE.x0 - 40, background: C.carbon, color: C.marfil,
        border: `3px solid ${dark ? C.marfil : C.carbon}`, boxShadow: `8px 8px 0 0 ${dark ? C.taupe : C.naranja}`,
        fontFamily: FONT.text, fontWeight: 600, fontSize: 30, lineHeight: 1.3, padding: "12px 24px", textAlign: "center",
      }}>{cur.text}</div>
    </div>
  );
};
