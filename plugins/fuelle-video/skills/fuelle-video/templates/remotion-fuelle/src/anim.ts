import { interpolate, Easing } from "remotion";

/** Aparición brutalista: 0→1 en `frames` cuadros (2–3 por defecto). */
export const snap = (frame: number, start: number, frames = 3) =>
  interpolate(frame, [start, start + frames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

/** Rampa con easing out cúbico. */
export const ramp = (frame: number, start: number, dur: number) =>
  interpolate(frame, [start, start + dur], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic),
  });

/** Cuantiza un valor 0..1 en pasos (movimiento por saltos, no fluido). */
export const steps = (v: number, n = 6) => Math.floor(v * n) / n;

/** Pseudo-aleatorio determinista (mismo resultado en cada render). */
export const rand = (seed: number) => {
  const x = Math.sin(seed * 12.9898) * 43758.5453;
  return x - Math.floor(x);
};

export const sec = (s: number, fps = 30) => Math.round(s * fps);
