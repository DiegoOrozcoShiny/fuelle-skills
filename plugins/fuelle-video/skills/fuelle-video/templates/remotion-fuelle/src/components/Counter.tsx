import React from "react";
import { C, FONT } from "../brand";

/** Contador grande (estilo del video de referencia): etiqueta pequeña gris + número Sora 800. */
export const Counter: React.FC<{ x: number; y: number; label: string; value: string | number; color?: string; dark?: boolean }> = ({
  x, y, label, value, color, dark = true,
}) => (
  <div style={{ position: "absolute", left: x, top: y }}>
    <div style={{ fontFamily: FONT.text, fontWeight: 600, fontSize: 24, letterSpacing: 3, textTransform: "uppercase", color: dark ? C.grayOnDark : C.grayOnLight }}>{label}</div>
    <div style={{ fontFamily: FONT.display, fontWeight: 800, fontSize: 110, lineHeight: 1.05, color: color ?? (dark ? C.marfil : C.carbon) }}>{value}</div>
  </div>
);
