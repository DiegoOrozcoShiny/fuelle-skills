import React from "react";
import { AbsoluteFill } from "remotion";
import { SAFE, W, H } from "../brand";

/** Solo para storyboard/QA: pinta en rosa la zona que tapa la interfaz de Instagram/TikTok. */
export const SafeOverlay: React.FC = () => {
  const f = "rgba(255,0,80,0.28)";
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <svg width={W} height={H}>
        <rect x={0} y={0} width={W} height={SAFE.y0} fill={f} />
        <rect x={0} y={SAFE.y1} width={W} height={H - SAFE.y1} fill={f} />
        <rect x={0} y={SAFE.y0} width={SAFE.x0} height={SAFE.y1 - SAFE.y0} fill={f} />
        <rect x={SAFE.x1} y={SAFE.y0} width={W - SAFE.x1} height={SAFE.y1 - SAFE.y0} fill={f} />
        <rect x={SAFE.x0} y={SAFE.y0} width={SAFE.x1 - SAFE.x0} height={SAFE.y1 - SAFE.y0}
          fill="none" stroke="#FF0050" strokeWidth={3} strokeDasharray="12 12" />
      </svg>
    </AbsoluteFill>
  );
};
