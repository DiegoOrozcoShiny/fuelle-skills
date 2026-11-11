import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { C } from "../brand";

/** PHONE MOCKUP — teléfono genérico brutalista (sin marca) con contenido que hace scroll y leve giro 3D. */
export const PhoneMockup: React.FC<{
  x: number; y: number; width?: number; scrollPx?: number; durationInFrames: number; tiltDeg?: number; children: React.ReactNode;
}> = ({ x, y, width = 420, scrollPx = 600, durationInFrames, tiltDeg = 12, children }) => {
  const frame = useCurrentFrame();
  const h = width * 2.05;
  const scroll = interpolate(frame, [8, durationInFrames - 8], [0, scrollPx], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const tilt = interpolate(frame, [0, durationInFrames], [tiltDeg, -tiltDeg / 2]);
  return (
    <div style={{ position: "absolute", left: x, top: y, width, height: h, perspective: 1400 }}>
      <div style={{ width: "100%", height: "100%", transform: `translate(-50%,-50%) rotateY(${tilt}deg)`, background: C.carbon,
        border: `10px solid ${C.carbon}`, outline: `4px solid ${C.marfil}`, boxShadow: `18px 18px 0 ${C.naranja}`, boxSizing: "border-box", position: "relative" }}>
        <div style={{ position: "absolute", top: 10, left: "50%", width: 90, height: 18, transform: "translateX(-50%)", background: C.carbon, zIndex: 2 }} />
        <div style={{ position: "absolute", inset: 0, overflow: "hidden", background: C.marfil }}>
          <div style={{ transform: `translateY(${-scroll}px)` }}>{children}</div>
        </div>
      </div>
    </div>
  );
};
