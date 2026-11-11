import React from "react";
import { useCurrentFrame } from "remotion";
import { C, FONT, SAFE, POSTER_COMPRESS } from "../brand";
import { snap } from "../anim";

/** COVER STORY — portada de revista brutalista: cabecera gigante, sujeto encima de las letras, titulares de portada que entran a golpes. */
export const CoverStory: React.FC<{ masthead: string; subject: React.ReactNode; coverLines: string[]; issue?: string; dark?: boolean; mastheadSize?: number }> = ({
  masthead, subject, coverLines, issue = "N.º 01 · 2026", dark = false, mastheadSize = 300,
}) => {
  const frame = useCurrentFrame();
  const m = snap(frame, 0, 3), s = snap(frame, 6, 3);
  const ink = dark ? C.marfil : C.carbon;
  return (<>
    <div style={{ position: "absolute", left: SAFE.x0, top: SAFE.y0 + 10, fontFamily: FONT.text, fontWeight: 600, fontSize: 24, letterSpacing: 4, color: ink }}>{issue}</div>
    <div style={{ position: "absolute", left: SAFE.x0, top: SAFE.y0 + 40, fontFamily: FONT.display, fontWeight: 800, fontSize: mastheadSize, lineHeight: 0.85,
      color: ink, transform: `scaleX(${POSTER_COMPRESS}) translateY(${(1 - m) * -60}px)`, transformOrigin: "left top", opacity: m }}>{masthead}</div>
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, transform: `translateY(${(1 - s) * 120}px)`, opacity: s }}>{subject}</div>
    {coverLines.map((l, i) => {
      const k = snap(frame, 12 + i * 6, 2);
      return k > 0 ? (
        <div key={i} style={{ position: "absolute", left: i % 2 ? undefined : SAFE.x0, right: i % 2 ? 1080 - SAFE.x1 : undefined, top: 900 + i * 120,
          background: i === 0 ? C.naranja : C.carbon, color: i === 0 ? C.carbon : C.marfil, fontFamily: FONT.display, fontWeight: 800, fontSize: 40,
          padding: "10px 18px", border: `5px solid ${C.carbon}`, maxWidth: 420, textTransform: "uppercase" }}>{l}</div>) : null;
    })}
    <div style={{ position: "absolute", right: 1080 - SAFE.x1, top: SAFE.y1 - 230, width: 150, height: 80, background: `repeating-linear-gradient(90deg, ${ink} 0 4px, transparent 4px 7px, ${ink} 7px 9px, transparent 9px 14px)` }} />
  </>);
};
