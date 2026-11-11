import React from "react";
import { useCurrentFrame } from "remotion";
import { rand } from "../anim";

/** PAPER CUT — capas de papel recortado con borde rasgado que entran con movimiento stop-motion (12 fps) y sombra dura. */
export type PaperLayer = { node: React.ReactNode; color: string; x: number; y: number; w: number; h: number; from: "left" | "right" | "bottom"; delay: number; seed?: number };
const torn = (seed: number) => {
  const pts: string[] = []; const n = 18;
  for (let i = 0; i <= n; i++) pts.push(`${(i / n) * 100}% ${rand(seed + i) * 3}%`);
  for (let i = 0; i <= n; i++) pts.push(`${100 - rand(seed + 50 + i) * 2}% ${(i / n) * 100}%`);
  for (let i = n; i >= 0; i--) pts.push(`${(i / n) * 100}% ${100 - rand(seed + 100 + i) * 3}%`);
  for (let i = n; i >= 0; i--) pts.push(`${rand(seed + 150 + i) * 2}% ${(i / n) * 100}%`);
  return `polygon(${pts.join(",")})`;
};
export const PaperCut: React.FC<{ layers: PaperLayer[] }> = ({ layers }) => {
  const frame = useCurrentFrame();
  const f12 = Math.floor(frame / 2.5) * 2.5; // stop-motion
  return (<>{layers.map((l, i) => {
    const p = Math.min(1, Math.max(0, (f12 - l.delay) / 10));
    const e = 1 - Math.pow(1 - p, 3);
    const off = (1 - e) * 1200;
    const dx = l.from === "left" ? -off : l.from === "right" ? off : 0; const dy = l.from === "bottom" ? off : 0;
    const jit = p < 1 ? (rand(f12 + i) - 0.5) * 3 : (rand(Math.floor(frame / 6) + i) - 0.5) * 1.2;
    return (
      <div key={i} style={{ position: "absolute", left: l.x + dx, top: l.y + dy, width: l.w, height: l.h, transform: `rotate(${jit}deg)`, filter: "drop-shadow(10px 10px 0 rgba(15,15,15,.85))" }}>
        <div style={{ width: "100%", height: "100%", background: l.color, clipPath: torn(l.seed ?? i * 31) }}>{l.node}</div>
      </div>);
  })}</>);
};
