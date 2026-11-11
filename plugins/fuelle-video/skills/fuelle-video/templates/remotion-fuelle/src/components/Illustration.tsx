import React from "react";
import { Img, staticFile } from "remotion";

/**
 * Ilustración rasterizada (PNG con alfa) generada por scripts/illus.py en public/illus/.
 * Sombra dura brutalista con drop-shadow sin desenfoque.
 */
export const Illustration: React.FC<{
  src: string; x: number; y: number; width: number; rotate?: number; scaleX?: number; scaleY?: number;
  shadow?: string; shadowOffset?: number; anchor?: "center" | "bottom" | "top-left";
}> = ({ src, x, y, width, rotate = 0, scaleX = 1, scaleY = 1, shadow, shadowOffset = 12, anchor = "center" }) => {
  const tr = anchor === "center" ? "translate(-50%,-50%)" : anchor === "bottom" ? "translate(-50%,-100%)" : "";
  return (
    <Img src={staticFile(src)} style={{
      position: "absolute", left: x, top: y, width,
      transform: `${tr} rotate(${rotate}deg) scale(${scaleX},${scaleY})`,
      transformOrigin: anchor === "bottom" ? "50% 100%" : "50% 50%",
      filter: shadow ? `drop-shadow(${shadowOffset}px ${shadowOffset}px 0 ${shadow})` : undefined,
    }} />
  );
};
