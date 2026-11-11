import React from "react";
import { useCurrentFrame, interpolate, AbsoluteFill } from "remotion";

/** VERTIGO (dolly zoom) — el fondo se agranda mientras el sujeto se mantiene/achica: sensación de vértigo, ansiedad o revelación. */
export const Vertigo: React.FC<{ background: React.ReactNode; subject: React.ReactNode; durationInFrames: number; bgScale?: [number, number]; subjectScale?: [number, number]; fx?: number; fy?: number }> = ({
  background, subject, durationInFrames, bgScale = [1, 1.7], subjectScale = [1, 0.86], fx = 540, fy = 900,
}) => {
  const frame = useCurrentFrame();
  const opt = { extrapolateRight: "clamp" as const };
  const b = interpolate(frame, [0, durationInFrames], bgScale, opt);
  const s = interpolate(frame, [0, durationInFrames], subjectScale, opt);
  return (<>
    <AbsoluteFill style={{ transform: `scale(${b})`, transformOrigin: `${fx}px ${fy}px` }}>{background}</AbsoluteFill>
    <AbsoluteFill style={{ transform: `scale(${s})`, transformOrigin: `${fx}px ${fy}px` }}>{subject}</AbsoluteFill>
  </>);
};
