import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";

/** ORBIT — elementos que giran en elipse 3D alrededor de un centro (logo, palabra, producto). Los de atrás se achican y pasan detrás. */
export const Orbit: React.FC<{
  center: React.ReactNode; items: React.ReactNode[]; cx: number; cy: number;
  rx?: number; ry?: number; turnsPerSecond?: number; itemSize?: number;
}> = ({ center, items, cx, cy, rx = 360, ry = 110, turnsPerSecond = 0.18, itemSize = 160 }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig();
  const base = (frame / fps) * turnsPerSecond * Math.PI * 2;
  const placed = items.map((node, i) => {
    const a = base + (i / items.length) * Math.PI * 2;
    const depth = Math.sin(a); // -1 atrás, 1 adelante
    return { node, x: cx + Math.cos(a) * rx, y: cy + depth * ry, s: 0.72 + 0.28 * (depth + 1) / 2, z: depth };
  });
  const render = (front: boolean) => placed.filter((p) => (p.z >= 0) === front).sort((a, b) => a.z - b.z).map((p, i) => (
    <div key={`${front}-${i}`} style={{ position: "absolute", left: p.x, top: p.y, width: itemSize, height: itemSize,
      transform: `translate(-50%,-50%) scale(${p.s})`, opacity: front ? 1 : 0.85 }}>{p.node}</div>));
  return (<>{render(false)}<div style={{ position: "absolute", left: cx, top: cy, transform: "translate(-50%,-50%)" }}>{center}</div>{render(true)}</>);
};
