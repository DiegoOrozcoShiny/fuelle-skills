import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame } from "remotion";
import { C, SAFE, FONT } from "./brand";
import { Background } from "./components/Background";
import { CropMarks } from "./components/CropMarks";
import { GiantType } from "./components/GiantType";
import { HalftoneWipe } from "./components/HalftoneWipe";
import * as FX from "./effects";

/** Muestrario de los 17 efectos (3 s cada uno) para revisar el estilo y probar el render. */
const Tag: React.FC<{ n: string }> = ({ n }) => (
  <div style={{ position: "absolute", left: SAFE.x0, top: SAFE.y1 - 70, background: C.naranja, color: C.carbon, fontFamily: FONT.text, fontWeight: 700, fontSize: 28, letterSpacing: 4, padding: "8px 16px", border: `5px solid ${C.carbon}` }}>{n}</div>
);
const Box: React.FC<{ t: string; c?: string }> = ({ t, c = C.marfil }) => (
  <div style={{ width: "100%", height: "100%", background: c, border: `6px solid ${C.carbon}`, boxShadow: `10px 10px 0 ${C.carbon}`, display: "grid", placeItems: "center", fontFamily: FONT.display, fontWeight: 800, fontSize: 30, color: C.carbon }}>{t}</div>
);
const Big: React.FC<{ t: string[]; dark?: boolean }> = ({ t, dark = true }) => <GiantType lines={t} y={SAFE.y0 + 30} dark={dark} maxSize={220} />;
const D = 90;
const DEMOS: [string, React.FC][] = [
  ["ORBIT", () => <FX.Orbit cx={540} cy={900} center={<div style={{ fontFamily: FONT.display, fontWeight: 800, fontSize: 150, color: C.naranja, transform: `scaleX(0.8)` }}>FUELLE</div>} items={["IA", "ROI", "ADS", "CRM", "SEO"].map((t) => <Box key={t} t={t} />)} />],
  ["COUCH WALL", () => <FX.CouchWall tiles={Array.from({ length: 24 }).map((_, i) => <Box key={i} t={`${i + 1}`} c={i % 5 ? "#2A2A2A" : C.taupe} />)} />],
  ["UI WORLD", () => <FX.UIWorld durationInFrames={D} panels={Array.from({ length: 10 }).map((_, i) => ({ node: <Box t={["CTR", "ROI", "LEADS", "CPA", "VENTAS"][i % 5]} c={i % 3 ? C.marfil : C.taupe} />, x: 540 + ((i % 3) - 1) * 300, y: 900 + ((i % 2) * 2 - 1) * 260, z: i * 300, w: 300, h: 220, rotY: (i % 2 ? -1 : 1) * 14 }))} />],
  ["FRAME BREAK", () => <FX.FrameBreak x={180} y={520} w={720} h={800} breakAt={30} background={<div style={{ position: "absolute", inset: 0, background: C.taupe }} />} subject={<Big t={["SAL", "DEL", "MOLDE."]} dark={false} />} />],
  ["DIGITAL ZOOM", () => <FX.DigitalZoom punches={[{ at: 20, scale: 1.35, fx: 300, fy: 700, hold: 30 }, { at: 60, scale: 1.6, fx: 700, fy: 900 }]}><Big t={["MIRA", "ESTO."]} /></FX.DigitalZoom>],
  ["PHONE MOCKUP", () => <FX.PhoneMockup x={540} y={900} durationInFrames={D}>{Array.from({ length: 12 }).map((_, i) => <div key={i} style={{ height: 180, margin: 14, background: i % 2 ? C.taupe : C.carbon }} />)}</FX.PhoneMockup>],
  ["CHECKLIST", () => <FX.Checklist y={520} dark items={[{ text: "Automatiza", at: 8 }, { text: "Mide ROI", at: 26 }, { text: "Ahorra", at: 44 }]} />],
  ["HEADLINE WALL", () => <FX.HeadlineWall words={["VENDE MÁS", "SIN ADIVINAR", "IMPULSO"]} top={260} dark={false} />],
  ["ZOOM-THROUGH CUT", () => <FX.ZoomThroughCut durationInFrames={45} fx={540} fy={760} from={<Big t={["DOLOR"]} />} to={<AbsoluteFill style={{ background: C.marfil }}><Big t={["SOLUCIÓN."]} dark={false} /></AbsoluteFill>} />],
  ["CHART GROW", () => <FX.ChartGrow x={SAFE.x0 + 20} y={800} w={780} h={480} max={100} prefix="$" bars={[{ label: "ENE", value: 30, at: 5 }, { label: "FEB", value: 55, at: 20 }, { label: "MAR", value: 92, at: 35, color: C.naranja }]} />],
  ["PULL-BACK REVEAL", () => <FX.PullBackReveal fx={300} fy={600} durationInFrames={70}><Big t={["EL PANO-", "RAMA", "COMPLETO."]} /></FX.PullBackReveal>],
  ["GREEN SCREEN", () => <div style={{ position: "absolute", left: SAFE.x0, top: 800, color: C.carbon, fontFamily: FONT.text, fontSize: 30, width: 760 }}>Requiere footage con fondo verde → public/footage/sujeto.webm (ver references/effects.md)</div>],
  ["PAPER CUT", () => <FX.PaperCut layers={[{ node: null, color: C.taupe, x: 120, y: 500, w: 840, h: 420, from: "left", delay: 0 }, { node: <Big t={["HECHO", "A MANO."]} dark={false} />, color: C.marfil, x: 80, y: 260, w: 840, h: 700, from: "right", delay: 10 }, { node: null, color: C.naranja, x: 520, y: 1000, w: 380, h: 300, from: "bottom", delay: 22 }]} />],
  ["DOODLE BOIL", () => { const f = useCurrentFrame(); return <FX.DoodleBoil width={1080} height={1920} strength={5}><FX.DrawPath d="M200 1100 C 320 900, 520 1300, 880 820" length={1100} progress={Math.min(1, f / 40)} color={C.naranja} width={14} /><FX.DrawPath d="M300 700 L 760 700 L 760 980 L 300 980 Z" length={1500} progress={Math.min(1, f / 50)} color={C.carbon} width={10} /></FX.DoodleBoil>; }],
  ["VERTIGO", () => <FX.Vertigo durationInFrames={D} background={<FX.HeadlineWall words={["PRESIÓN", "GASTO", "MÁS ADS"]} highlightRow={-1} />} subject={<div style={{ position: "absolute", left: 340, top: 700, width: 400, height: 560, background: C.marfil, border: `8px solid ${C.carbon}`, boxShadow: `16px 16px 0 ${C.naranja}` }} />} />],
  ["COVER STORY", () => <FX.CoverStory masthead="FUELLE" subject={<div style={{ position: "absolute", left: 300, top: 600, width: 480, height: 700, background: C.taupe, border: `8px solid ${C.carbon}` }} />} coverLines={["Vende sin adivinar", "ROI en tiempo real", "Edición 01"]} />],
  ["GLASS TYPE", () => <FX.GlassType text={"VIDRIO\nY CON-\nCRETO."} y={480} size={210} durationInFrames={D} label="GLASS TYPE" />],
];
export const SHOWCASE_FRAMES = DEMOS.length * D + 15;
export const Showcase: React.FC = () => (
  <AbsoluteFill>
    {DEMOS.map(([name, Demo], i) => (
      <Sequence key={name} from={i * D} durationInFrames={D} name={name}>
        <Background dark={i % 2 === 0} />
        <Demo />
        <CropMarks dark={i % 2 === 0} />
        <Tag n={`${String(i + 1).padStart(2, "0")} · ${name}`} />
      </Sequence>
    ))}
    <Sequence from={DEMOS.length * D - 15} durationInFrames={30}><HalftoneWipe durationInFrames={15} /></Sequence>
  </AbsoluteFill>
);
