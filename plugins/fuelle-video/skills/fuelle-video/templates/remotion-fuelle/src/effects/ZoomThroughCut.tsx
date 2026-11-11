import React from "react";
import { useCurrentFrame, AbsoluteFill } from "remotion";

/** ZOOM-THROUGH CUT — la cámara entra por un hueco (la "O" de una palabra, una ventana, la pantalla) y aparece la escena siguiente. */
export const ZoomThroughCut: React.FC<{ from: React.ReactNode; to: React.ReactNode; fx: number; fy: number; durationInFrames: number; maxScale?: number }> = ({
  from, to, fx, fy, durationInFrames, maxScale = 40,
}) => {
  const frame = useCurrentFrame();
  const p = Math.min(1, frame / durationInFrames);
  if (p < 1) {
    const s = Math.pow(maxScale, p * p);
    return <AbsoluteFill style={{ transform: `scale(${s})`, transformOrigin: `${fx}px ${fy}px` }}>{from}</AbsoluteFill>;
  }
  const after = frame - durationInFrames;
  const s2 = after < 4 ? 1.12 - 0.03 * after : 1;
  return <AbsoluteFill style={{ transform: `scale(${s2})` }}>{to}</AbsoluteFill>;
};
