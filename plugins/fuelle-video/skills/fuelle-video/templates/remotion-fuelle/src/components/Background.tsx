import React from "react";
import { AbsoluteFill } from "remotion";
import { C, W, H } from "../brand";

/** Fondo brutalista: color plano + textura de concreto (feTurbulence) + retícula visible de 60 px. */
export const Background: React.FC<{ dark: boolean; grid?: boolean; texture?: boolean; seed?: number }> = ({
  dark, grid = true, texture = true, seed = 3,
}) => {
  const base = dark ? C.carbon : C.marfil;
  const line = dark ? "#1A1A1A" : "#E9E2D5";
  const lines: React.ReactNode[] = [];
  if (grid) {
    for (let x = 0; x <= W; x += 60) lines.push(<rect key={`x${x}`} x={x} y={0} width={1} height={H} fill={line} />);
    for (let y = 0; y <= H; y += 60) lines.push(<rect key={`y${y}`} x={0} y={y} width={W} height={1} fill={line} />);
  }
  return (
    <AbsoluteFill style={{ backgroundColor: base }}>
      <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
        {texture && (
          <>
            <filter id={`conc${seed}`}>
              <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={3} seed={seed} />
              <feColorMatrix type="matrix" values={dark
                ? "0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0"
                : "0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.07 0"} />
            </filter>
            <rect width={W} height={H} filter={`url(#conc${seed})`} />
          </>
        )}
        {lines}
      </svg>
    </AbsoluteFill>
  );
};
