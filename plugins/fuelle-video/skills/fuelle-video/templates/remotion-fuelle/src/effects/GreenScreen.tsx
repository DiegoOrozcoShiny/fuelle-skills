import React from "react";
import { OffthreadVideo, staticFile } from "remotion";
import { C } from "../brand";

/**
 * GREEN SCREEN — persona/objeto grabado en verde, recortado y compuesto sobre la escena de marca.
 * Pre-proceso (FFmpeg), ver references/effects.md:
 *   ffmpeg -i in.mp4 -vf "chromakey=0x00FF00:0.13:0.06,despill=green" -c:v libvpx-vp9 -pix_fmt yuva420p public/footage/sujeto.webm
 * Estilo brutalista: contorno tipo recorte de papel (marfil) + sombra dura.
 */
export const GreenScreen: React.FC<{ src: string; x: number; y: number; width: number; outline?: string; shadow?: string; startFrom?: number }> = ({
  src, x, y, width, outline = C.marfil, shadow = C.carbon, startFrom = 0,
}) => (
  <div style={{ position: "absolute", left: x, top: y, width, transform: "translate(-50%,-100%)",
    filter: `drop-shadow(5px 0 0 ${outline}) drop-shadow(-5px 0 0 ${outline}) drop-shadow(0 5px 0 ${outline}) drop-shadow(0 -5px 0 ${outline}) drop-shadow(14px 14px 0 ${shadow})` }}>
    <OffthreadVideo src={staticFile(src)} transparent startFrom={startFrom} style={{ width: "100%" }} />
  </div>
);
