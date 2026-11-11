import React from "react";
import { useCurrentFrame } from "remotion";

/** DOODLE BOIL — trazos dibujados a mano que "hierven" (line boil): el desplazamiento cambia cada `every` cuadros. Envolver elementos SVG. */
export const DoodleBoil: React.FC<{ width: number; height: number; strength?: number; every?: number; id?: string; children: React.ReactNode; style?: React.CSSProperties }> = ({
  width, height, strength = 4, every = 3, id = "boil", children, style,
}) => {
  const frame = useCurrentFrame();
  const seed = Math.floor(frame / every) % 5;
  return (
    <svg width={width} height={height} style={{ position: "absolute", left: 0, top: 0, ...style }}>
      <filter id={`${id}${seed}`} filterUnits="userSpaceOnUse" x={0} y={0} width={width} height={height}>
        <feTurbulence type="turbulence" baseFrequency="0.035" numOctaves={2} seed={seed + 1} result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale={strength} xChannelSelector="R" yChannelSelector="G" />
      </filter>
      <g filter={`url(#${id}${seed})`}>{children}</g>
    </svg>
  );
};

/** Trazo que se dibuja (stroke-dashoffset) para usar dentro de DoodleBoil. */
export const DrawPath: React.FC<{ d: string; length: number; progress: number; color: string; width?: number }> = ({ d, length, progress, color, width = 8 }) => (
  <path d={d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="square" strokeDasharray={length} strokeDashoffset={length * (1 - progress)} />
);
