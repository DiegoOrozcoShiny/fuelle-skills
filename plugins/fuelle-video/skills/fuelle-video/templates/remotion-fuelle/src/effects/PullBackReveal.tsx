import React from "react";
import { useCurrentFrame, AbsoluteFill, interpolate, Easing } from "remotion";
import { steps } from "../anim";

/** PULL-BACK REVEAL — empieza en un detalle (zoom fuerte) y se aleja por saltos hasta revelar la composición completa. */
export const PullBackReveal: React.FC<{ fx: number; fy: number; startScale?: number; durationInFrames: number; stepped?: boolean; children: React.ReactNode }> = ({
  fx, fy, startScale = 3.2, durationInFrames, stepped = true, children,
}) => {
  const frame = useCurrentFrame();
  let p = interpolate(frame, [0, durationInFrames], [0, 1], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  if (stepped) p = steps(p, 5);
  const s = startScale + (1 - startScale) * p;
  return <AbsoluteFill style={{ transform: `scale(${s})`, transformOrigin: `${fx}px ${fy}px` }}>{children}</AbsoluteFill>;
};
