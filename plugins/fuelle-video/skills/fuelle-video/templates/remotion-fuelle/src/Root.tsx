import React from "react";
import { Composition } from "remotion";
import { W, H, FPS } from "./brand";
import timeline from "./timeline.json";
import { FuelleVideo } from "./Video";
import { Showcase, SHOWCASE_FRAMES } from "./Showcase";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="FuelleReel" component={FuelleVideo} width={W} height={H} fps={FPS}
      durationInFrames={Math.round(timeline.duration * FPS)} defaultProps={{ safe: false, withAudio: true }} />
    <Composition id="FuelleReelSafe" component={FuelleVideo} width={W} height={H} fps={FPS}
      durationInFrames={Math.round(timeline.duration * FPS)} defaultProps={{ safe: true, withAudio: false }} />
    <Composition id="EffectsShowcase" component={Showcase} width={W} height={H} fps={FPS} durationInFrames={SHOWCASE_FRAMES} />
  </>
);
