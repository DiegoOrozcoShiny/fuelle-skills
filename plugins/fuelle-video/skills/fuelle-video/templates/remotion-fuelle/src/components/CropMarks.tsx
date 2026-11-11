import React from "react";
import { AbsoluteFill } from "remotion";
import { C, W, H } from "../brand";

/** Marcas de corte en L (30 px, 2 px, a 40 px del borde) — presentes todo el video. */
export const CropMarks: React.FC<{ dark: boolean }> = ({ dark }) => {
  const col = dark ? C.grayOnDark : C.grayOnLight;
  const m = 40, L = 30, w = 2;
  const corners = [[m, m, 1, 1], [W - m, m, -1, 1], [m, H - m, 1, -1], [W - m, H - m, -1, -1]];
  return (
    <AbsoluteFill>
      <svg width={W} height={H}>
        {corners.map(([x, y, dx, dy], i) => (
          <g key={i} fill={col}>
            <rect x={dx > 0 ? x : x - L} y={dy > 0 ? y : y - w} width={L} height={w} />
            <rect x={dx > 0 ? x : x - w} y={dy > 0 ? y : y - L} width={w} height={L} />
          </g>
        ))}
      </svg>
    </AbsoluteFill>
  );
};
