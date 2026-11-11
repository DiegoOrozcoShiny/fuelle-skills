import React from "react";
import { fitText } from "@remotion/layout-utils";
import { C, FONT, SAFE, SAFE_W, POSTER_COMPRESS } from "../brand";

/**
 * Palabra(s) gigante(s) tipo póster brutalista. Sora 800 comprimida al 80 %.
 * - accent: índice de la línea en Naranja Impulso (por defecto la última; -1 = ninguna).
 * - Todas las líneas comparten el mismo tamaño (el de la línea más ancha).
 * - Siempre dentro del área segura.
 */
export const GiantType: React.FC<{
  lines: string[]; y: number; dark: boolean; accent?: number; align?: "left" | "center";
  maxSize?: number; lineHeight?: number; width?: number; reveal?: number[]; // reveal: opacidad por línea 0..1
}> = ({ lines, y, dark, accent, align = "left", maxSize = 300, lineHeight = 0.86, width = SAFE_W, reveal }) => {
  const acc = accent === undefined ? lines.length - 1 : accent;
  const sizes = lines.map((l) =>
    fitText({ text: l, withinWidth: width / POSTER_COMPRESS, fontFamily: FONT.display, fontWeight: "800" }).fontSize);
  const size = Math.min(maxSize, ...sizes);
  return (
    <div style={{ position: "absolute", left: SAFE.x0, top: y, width }}>
      {lines.map((l, i) => (
        <div key={i} style={{
          fontFamily: FONT.display, fontWeight: 800, fontSize: size, lineHeight,
          color: i === acc ? C.naranja : dark ? C.marfil : C.carbon,
          transform: `scaleX(${POSTER_COMPRESS})`,
          transformOrigin: align === "left" ? "left top" : "center top",
          textAlign: align, whiteSpace: "nowrap", letterSpacing: "-0.01em",
          width: align === "center" ? width / POSTER_COMPRESS : undefined,
          marginLeft: align === "center" ? -(width / POSTER_COMPRESS - width) / 2 : 0,
          opacity: reveal ? reveal[i] ?? 1 : 1,
        }}>{l}</div>
      ))}
    </div>
  );
};

/** Línea técnica bajo la palabra gigante: regla + etiqueta pequeña + "0X / 0N". */
export const PosterRule: React.FC<{ y: number; left: string; right: string; dark: boolean }> = ({ y, left, right, dark }) => {
  const col = dark ? C.grayOnDark : C.carbon;
  const t: React.CSSProperties = { fontFamily: FONT.text, fontWeight: 600, fontSize: 24, letterSpacing: 3, color: col, textTransform: "uppercase" };
  return (
    <div style={{ position: "absolute", left: SAFE.x0, top: y, width: SAFE_W }}>
      <div style={{ height: 3, background: col }} />
      <div style={{ display: "flex", justifyContent: "space-between", marginTop: 12 }}>
        <span style={t}>{left}</span><span style={t}>{right}</span>
      </div>
    </div>
  );
};
