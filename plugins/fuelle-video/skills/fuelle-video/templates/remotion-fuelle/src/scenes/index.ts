import React from "react";
import { S1ChartGrow, S2CouchWall, S3GlassType } from "./ExampleScenes";

export type SceneProps = { durationInFrames: number };
/** Registro de escenas: el agente crea un componente por escena y lo agrega aquí con el mismo id de timeline.json. */
export const SCENES: Record<string, React.FC<SceneProps>> = {
  s1: S1ChartGrow,
  s2: S2CouchWall,
  s3: S3GlassType,
};
