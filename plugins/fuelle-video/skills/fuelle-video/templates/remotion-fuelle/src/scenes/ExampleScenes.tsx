import React from "react";
import { C, SAFE } from "../brand";
import { GiantType, PosterRule } from "../components/GiantType";
import { Counter } from "../components/Counter";
import { BrutBlock } from "../components/BrutBlock";
import { ChartGrow, CouchWall, GlassType } from "../effects";
import type { SceneProps } from "./index";

export const S1ChartGrow: React.FC<SceneProps> = () => (
  <>
    <Counter x={SAFE.x0} y={SAFE.y0 + 10} label="Ventas" value={120} />
    <GiantType lines={["NO", "SUBEN."]} y={470} dark maxSize={230} />
    <PosterRule y={850} left="Fuelle Studio" right="01 / 03" dark />
    <ChartGrow x={SAFE.x0 + 20} y={980} w={SAFE.x1 - SAFE.x0 - 40} h={300} max={100} dark
      bars={[{ label: "ENE", value: 40, at: 6 }, { label: "FEB", value: 38, at: 18 }, { label: "MAR", value: 41, at: 30, color: C.naranja }]} />
  </>
);

const AdCard: React.FC<{ i: number }> = ({ i }) => (
  <div style={{ width: "100%", height: "100%", background: "#1A1A1A", border: "4px solid #3E3E3E", boxSizing: "border-box", padding: 12 }}>
    <div style={{ height: "55%", background: "#2E2A26" }} />
    <div style={{ marginTop: 14, height: 10, width: `${60 + (i * 13) % 30}%`, background: "#4A4A4A" }} />
    <div style={{ marginTop: 10, height: 8, width: "45%", background: "#3A3A3A" }} />
  </div>
);
export const S2CouchWall: React.FC<SceneProps> = () => (
  <>
    <CouchWall tiles={Array.from({ length: 24 }).map((_, i) => <AdCard key={i} i={i} />)} fillFrames={50} />
    <BrutBlock x={SAFE.x0} y={500} w={SAFE.x1 - SAFE.x0} h={400} fill={C.carbon} border={C.marfil} shadow={C.taupe} borderWidth={4} />
    <GiantType lines={["SATU-", "RADAS."]} y={530} dark maxSize={180} width={SAFE.x1 - SAFE.x0 - 60} />
  </>
);

export const S3GlassType: React.FC<SceneProps> = ({ durationInFrames }) => (
  <GlassType text={"NOSOTROS\nTE ACOM-\nPAÑAMOS."} y={480} size={200} durationInFrames={durationInFrames} label="FUELLE STUDIO" />
);
