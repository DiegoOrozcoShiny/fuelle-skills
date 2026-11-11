import React from "react";
import { useCurrentFrame } from "remotion";
import { C } from "../brand";
import { snap, rand } from "../anim";

/** FRAME BREAK — el sujeto rompe el marco: empieza contenido dentro del recuadro y en `breakAt` se sale de él con un golpe. */
export const FrameBreak: React.FC<{
  x: number; y: number; w: number; h: number; background: React.ReactNode; subject: React.ReactNode;
  breakAt: number; popScale?: number; frameColor?: string;
}> = ({ x, y, w, h, background, subject, breakAt, popScale = 1.22, frameColor = C.carbon }) => {
  const frame = useCurrentFrame();
  const k = snap(frame, breakAt, 3);
  const shake = frame >= breakAt && frame < breakAt + 6 ? (rand(frame) - 0.5) * 14 : 0;
  return (
    <div style={{ position: "absolute", left: x + shake, top: y }}>
      <div style={{ position: "absolute", width: w, height: h, overflow: "hidden", border: `8px solid ${frameColor}`, boxShadow: `14px 14px 0 ${frameColor}`, boxSizing: "border-box" }}>
        {background}
        {k === 0 && <div style={{ position: "absolute", inset: 0 }}>{subject}</div>}
      </div>
      {k > 0 && (
        <div style={{ position: "absolute", width: w, height: h, transform: `scale(${1 + (popScale - 1) * k}) translateY(${-40 * k}px)`, transformOrigin: "50% 100%" }}>{subject}</div>
      )}
    </div>
  );
};
