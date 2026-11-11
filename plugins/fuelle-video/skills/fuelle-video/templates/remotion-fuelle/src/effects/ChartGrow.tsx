import React from "react";
import { useCurrentFrame } from "remotion";
import { C, FONT } from "../brand";
import { snap, ramp } from "../anim";

/** CHART GROW — barras que suben por golpes (o línea que se dibuja) con valor contando; retícula visible. */
export type Bar = { label: string; value: number; at: number; color?: string; icon?: React.ReactNode };
export const ChartGrow: React.FC<{ bars: Bar[]; x: number; y: number; w: number; h: number; max: number; dark?: boolean; prefix?: string; suffix?: string }> = ({
  bars, x, y, w, h, max, dark = false, prefix = "", suffix = "",
}) => {
  const frame = useCurrentFrame();
  const gap = 36; const bw = (w - gap * (bars.length - 1)) / bars.length;
  const ink = dark ? C.marfil : C.carbon;
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h }}>
      {[1, 2, 3, 4].map((g) => <div key={g} style={{ position: "absolute", left: 0, right: 0, top: h - (h * g) / 5, height: 1, background: dark ? "#2A2A2A" : "#DCD3C4" }} />)}
      <div style={{ position: "absolute", left: 0, right: 0, top: h, height: 6, background: ink }} />
      {bars.map((b, i) => {
        const k = snap(frame, b.at, 3); const v = ramp(frame, b.at, 18);
        const bh = (h * b.value / max) * (0.7 + 0.3 * k) * (k > 0 ? 1 : 0);
        return (
          <div key={i} style={{ position: "absolute", left: i * (bw + gap), width: bw, top: h - bh, height: bh,
            background: b.color ?? ink, border: `6px solid ${C.carbon}`, boxShadow: `12px 12px 0 ${dark ? C.taupe : C.carbon}`, boxSizing: "border-box" }}>
            {k > 0 && <div style={{ position: "absolute", top: -78, width: "100%", textAlign: "center", fontFamily: FONT.display, fontWeight: 800, fontSize: 52, color: ink }}>
              {prefix}{Math.round(b.value * v)}{suffix}</div>}
            {k > 0 && b.icon && <div style={{ position: "absolute", top: 16, left: "50%", transform: "translateX(-50%)" }}>{b.icon}</div>}
            <div style={{ position: "absolute", top: bh + 18, width: "100%", textAlign: "center", fontFamily: FONT.text, fontWeight: 600, fontSize: 24, letterSpacing: 3, color: ink }}>{b.label}</div>
          </div>
        );
      })}
    </div>
  );
};
