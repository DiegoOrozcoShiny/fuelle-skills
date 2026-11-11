import React from "react";
import { C, BORDER, HARD_SHADOW } from "../brand";

/** Bloque brutalista: borde grueso + sombra dura desplazada, sin radio ni desenfoque. */
export const BrutBlock: React.FC<{
  x: number; y: number; w: number; h: number;
  fill?: string; border?: string; shadow?: string; shadowOffset?: number; borderWidth?: number;
  style?: React.CSSProperties; children?: React.ReactNode;
}> = ({ x, y, w, h, fill = C.marfil, border = C.carbon, shadow = C.carbon, shadowOffset = HARD_SHADOW, borderWidth = BORDER, style, children }) => (
  <div style={{
    position: "absolute", left: x, top: y, width: w, height: h, boxSizing: "border-box",
    background: fill, border: `${borderWidth}px solid ${border}`,
    boxShadow: shadowOffset ? `${shadowOffset}px ${shadowOffset}px 0 0 ${shadow}` : undefined,
    ...style,
  }}>{children}</div>
);
