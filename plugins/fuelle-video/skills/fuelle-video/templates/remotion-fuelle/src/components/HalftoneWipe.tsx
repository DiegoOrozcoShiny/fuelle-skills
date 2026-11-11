import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { C, W, H } from "../brand";

/** Transición de semitono: puntos que crecen en diagonal (abajo-izq → arriba-der). mode "in" cubre, "out" descubre. */
export const HalftoneWipe: React.FC<{ durationInFrames: number; mode?: "in" | "out"; color?: string; step?: number }> = ({
  durationInFrames, mode = "in", color = C.naranja, step = 54,
}) => {
  const frame = useCurrentFrame();
  let p = Math.min(1, Math.max(0, frame / durationInFrames));
  if (mode === "out") p = 1 - p;
  const dots: React.ReactNode[] = [];
  for (let gy = -1; gy < H / step + 2; gy++) {
    for (let gx = -1; gx < W / step + 2; gx++) {
      const x = gx * step + (gy % 2 ? step / 2 : 0), y = gy * step;
      const pos = (x + (H - y)) / (W + H);
      const local = Math.min(1, Math.max(0, p * 1.6 - pos * 0.6));
      const r = local * step * 0.82;
      if (r > 0.5) dots.push(<circle key={`${gx}-${gy}`} cx={x} cy={y} r={r} fill={color} />);
    }
  }
  return <AbsoluteFill><svg width={W} height={H}>{dots}</svg></AbsoluteFill>;
};
