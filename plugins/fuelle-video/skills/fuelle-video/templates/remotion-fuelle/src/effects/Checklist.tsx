import React from "react";
import { useCurrentFrame } from "remotion";
import { C, FONT, SAFE } from "../brand";
import { snap } from "../anim";

/** CHECKLIST — lista que se marca a golpes: caja brutalista + ✓ naranja estampado (cada ítem a su tiempo, sincronizado con la voz). */
export const Checklist: React.FC<{ items: { text: string; at: number; icon?: React.ReactNode }[]; y: number; dark?: boolean; rowH?: number }> = ({
  items, y, dark = false, rowH = 150,
}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left: SAFE.x0, top: y, width: SAFE.x1 - SAFE.x0 }}>
      {items.map((it, i) => {
        const k = snap(frame, it.at, 2); const c = snap(frame, it.at + 5, 2);
        if (k === 0) return null;
        return (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 28, height: rowH - 22, marginBottom: 22,
            transform: `translateX(${(1 - k) * -40}px)`, background: dark ? "#1C1C1C" : C.marfil, border: `6px solid ${C.carbon}`,
            boxShadow: `12px 12px 0 ${dark ? C.taupe : C.carbon}`, padding: "0 24px" }}>
            <div style={{ width: 84, height: 84, border: `6px solid ${C.carbon}`, background: c ? C.naranja : C.marfil, display: "grid", placeItems: "center",
              transform: `scale(${1 + 0.25 * (c > 0 && c < 1 ? 1 : 0)})` }}>
              {c > 0 && <svg width={56} height={56}><polyline points="6,30 22,46 50,10" fill="none" stroke={C.carbon} strokeWidth={10} /></svg>}
            </div>
            {it.icon}
            <div style={{ fontFamily: FONT.display, fontWeight: 800, fontSize: 44, color: dark ? C.marfil : C.carbon, textTransform: "uppercase" }}>{it.text}</div>
          </div>
        );
      })}
    </div>
  );
};
