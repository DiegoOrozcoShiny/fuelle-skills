import React, { useEffect, useState } from "react";
import { AbsoluteFill, Sequence, Audio, staticFile, useVideoConfig, continueRender, delayRender } from "remotion";
import timeline from "./timeline.json";
import { fontsReady } from "./fonts";
import { Background } from "./components/Background";
import { CropMarks } from "./components/CropMarks";
import { Subtitle } from "./components/Subtitle";
import { SafeOverlay } from "./components/SafeOverlay";
import { SCENES } from "./scenes";

export type Scene = { id: string; start: number; end: number; bg: "dark" | "light"; effect?: string };
export type VideoProps = { safe?: boolean; withAudio?: boolean };

/** Composición principal: lee timeline.json (escenas + subtítulos alineados a la voz) y monta cada escena en su Sequence. */
export const FuelleVideo: React.FC<VideoProps> = ({ safe = false, withAudio = true }) => {
  const { fps } = useVideoConfig();
  const [handle] = useState(() => delayRender("fonts"));
  useEffect(() => { fontsReady.then(() => continueRender(handle)); }, [handle]);
  const scenes = timeline.scenes as Scene[];
  return (
    <AbsoluteFill>
      {scenes.map((s) => {
        const Comp = SCENES[s.id];
        const from = Math.round(s.start * fps), dur = Math.round((s.end - s.start) * fps);
        return (
          <Sequence key={s.id} from={from} durationInFrames={dur} name={s.id}>
            <Background dark={s.bg === "dark"} />
            {Comp ? <Comp durationInFrames={dur} /> : null}
            <CropMarks dark={s.bg === "dark"} />
          </Sequence>
        );
      })}
      <Subtitle subs={timeline.subtitles} dark={true} />
      {safe && <SafeOverlay />}
      {withAudio && timeline.mix ? <Audio src={staticFile(timeline.mix)} /> : null}
    </AbsoluteFill>
  );
};
