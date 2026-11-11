import React from "react";
import { useCurrentFrame, AbsoluteFill } from "remotion";
import { snap } from "../anim";

/** DIGITAL ZOOM — "punch-in" seco (2 cuadros) hacia un punto, con destello de líneas de escaneo y desfase RGB en el golpe. */
export type Punch = { at: number; scale: number; fx: number; fy: number; hold?: number };
export const DigitalZoom: React.FC<{ punches: Punch[]; children: React.ReactNode }> = ({ punches, children }) => {
  const frame = useCurrentFrame();
  let scale = 1, fx = 540, fy = 960, glitch = 0;
  for (const p of punches) {
    const k = snap(frame, p.at, 2);
    const out = p.hold !== undefined ? snap(frame, p.at + p.hold, 2) : 0;
    const v = k * (1 - out);
    if (v > 0) { scale = 1 + (p.scale - 1) * v; fx = p.fx; fy = p.fy; }
    if (frame >= p.at && frame < p.at + 3) glitch = 1;
  }
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <AbsoluteFill style={{ transform: `scale(${scale})`, transformOrigin: `${fx}px ${fy}px`, filter: glitch ? "drop-shadow(6px 0 0 rgba(255,106,0,.7)) drop-shadow(-6px 0 0 rgba(42,91,255,.6))" : undefined }}>
        {children}
      </AbsoluteFill>
      {glitch === 1 && <AbsoluteFill style={{ background: "repeating-linear-gradient(0deg, rgba(0,0,0,.18) 0 2px, transparent 2px 6px)" }} />}
    </AbsoluteFill>
  );
};
