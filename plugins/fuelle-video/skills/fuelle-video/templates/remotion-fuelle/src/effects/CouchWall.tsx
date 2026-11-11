import React from "react";
import { useCurrentFrame } from "remotion";
import { rand } from "../anim";

/**
 * COUCH WALL (muro de tarjetas) — un muro de piezas que se llena a golpes hasta saturar la pantalla
 * y se desplaza lento. Ideal para "saturación", "demasiado contenido", testimonios o portafolio.
 */
export const CouchWall: React.FC<{
  tiles: React.ReactNode[]; cols?: number; tileW?: number; tileH?: number; gap?: number;
  fillFrames?: number; panY?: number; panFrames?: number; seed?: number;
}> = ({ tiles, cols = 4, tileW = 252, tileH = 336, gap = 12, fillFrames = 66, panY = -180, panFrames = 120, seed = 7 }) => {
  const frame = useCurrentFrame();
  const order = tiles.map((_, i) => i).sort((a, b) => rand(a + seed) - rand(b + seed));
  const shown = Math.floor(tiles.length * Math.min(1, Math.pow(frame / fillFrames, 0.8)));
  const visible = new Set(order.slice(0, shown));
  const totalW = cols * tileW + (cols - 1) * gap;
  const dy = (Math.min(frame, panFrames) / panFrames) * panY;
  return (
    <div style={{ position: "absolute", left: (1080 - totalW) / 2, top: -40 + dy }}>
      {tiles.map((t, i) => visible.has(i) ? (
        <div key={i} style={{ position: "absolute", left: (i % cols) * (tileW + gap), top: Math.floor(i / cols) * (tileH + gap), width: tileW, height: tileH }}>{t}</div>
      ) : null)}
    </div>
  );
};
