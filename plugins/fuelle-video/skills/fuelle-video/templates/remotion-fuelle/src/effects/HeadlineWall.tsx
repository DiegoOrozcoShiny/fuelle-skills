import React from "react";
import { useCurrentFrame } from "remotion";
import { C, FONT, POSTER_COMPRESS } from "../brand";

/** HEADLINE WALL — muro de titulares repetidos en filas que corren en direcciones alternas; una fila destacada en naranja. */
export const HeadlineWall: React.FC<{ words: string[]; highlightRow?: number; rows?: number; size?: number; speed?: number; dark?: boolean; top?: number }> = ({
  words, highlightRow = 3, rows = 9, size = 170, speed = 6, dark = true, top = 0,
}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left: 0, top, width: 1080, overflow: "hidden" }}>
      {Array.from({ length: rows }).map((_, r) => {
        const word = words[r % words.length];
        const dir = r % 2 ? 1 : -1;
        const off = ((frame * speed * dir) % 1400) - 700;
        const color = r === highlightRow ? C.naranja : dark ? (r % 3 === 0 ? C.marfil : "#3A3A3A") : (r % 3 === 0 ? C.carbon : "#D8CFC0");
        return (
          <div key={r} style={{ whiteSpace: "nowrap", fontFamily: FONT.display, fontWeight: 800, fontSize: size, lineHeight: 0.9, color,
            transform: `translateX(${off}px) scaleX(${POSTER_COMPRESS})`, transformOrigin: "left" }}>
            {Array.from({ length: 6 }).map(() => word + " ").join("")}
          </div>
        );
      })}
    </div>
  );
};
