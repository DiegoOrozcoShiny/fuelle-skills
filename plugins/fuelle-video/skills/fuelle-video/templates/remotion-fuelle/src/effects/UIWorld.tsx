import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

/** UI WORLD — la cámara vuela dentro de un espacio 3D lleno de paneles de interfaz (dashboards, métricas, chats). */
export type UIPanel = { node: React.ReactNode; x: number; y: number; z: number; w: number; h: number; rotY?: number };
export const UIWorld: React.FC<{ panels: UIPanel[]; travel?: number; durationInFrames: number; perspective?: number }> = ({
  panels, travel = 1600, durationInFrames, perspective = 1100,
}) => {
  const frame = useCurrentFrame();
  const camZ = interpolate(frame, [0, durationInFrames], [0, travel], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, perspective, perspectiveOrigin: "50% 45%", overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, transformStyle: "preserve-3d", transform: `translateZ(${camZ}px)` }}>
        {panels.map((p, i) => (
          <div key={i} style={{ position: "absolute", left: p.x, top: p.y, width: p.w, height: p.h,
            transform: `translate(-50%,-50%) translateZ(${-p.z}px) rotateY(${p.rotY ?? 0}deg)`, transformStyle: "preserve-3d" }}>{p.node}</div>
        ))}
      </div>
    </div>
  );
};
