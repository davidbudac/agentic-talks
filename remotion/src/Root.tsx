import React from "react";
import { Composition } from "remotion";
import { AgentLoop } from "./AgentLoop";
import { Stateless } from "./Stateless";
import { NextToken } from "./NextToken";
import { QualityCurve } from "./QualityCurve";
import { KvCache } from "./KvCache";
import { Subagents } from "./Subagents";
import "./index.css";

const FPS = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* deck 1 · slide 10 (dark) */}
      <Composition
        id="agent-loop-dark"
        component={AgentLoop}
        durationInFrames={240}
        fps={FPS}
        width={1152}
        height={912}
        defaultProps={{ theme: "dark" as const }}
      />
      {/* deck 1 · slide 6 (dark) + deck 2 · slide 12 (light) */}
      <Composition
        id="stateless-dark"
        component={Stateless}
        durationInFrames={300}
        fps={FPS}
        width={1200}
        height={900}
        defaultProps={{ theme: "dark" as const }}
      />
      <Composition
        id="stateless-light"
        component={Stateless}
        durationInFrames={300}
        fps={FPS}
        width={1200}
        height={900}
        defaultProps={{ theme: "light" as const }}
      />
      {/* deck 2 · slide 6 (light) */}
      <Composition
        id="next-token-light"
        component={NextToken}
        durationInFrames={200}
        fps={FPS}
        width={1200}
        height={750}
        defaultProps={{ theme: "light" as const }}
      />
      {/* deck 1 · slide 22 (dark) + deck 2 · slide 17 (light) */}
      <Composition
        id="quality-dark"
        component={QualityCurve}
        durationInFrames={260}
        fps={FPS}
        width={1056}
        height={624}
        defaultProps={{ theme: "dark" as const }}
      />
      <Composition
        id="quality-light"
        component={QualityCurve}
        durationInFrames={260}
        fps={FPS}
        width={1056}
        height={624}
        defaultProps={{ theme: "light" as const }}
      />
      {/* deck 2 · slide 15 (light) */}
      <Composition
        id="kv-cache-light"
        component={KvCache}
        durationInFrames={290}
        fps={FPS}
        width={1200}
        height={600}
        defaultProps={{ theme: "light" as const }}
      />
      {/* deck 1 · slide 25 (light) */}
      <Composition
        id="subagents-light"
        component={Subagents}
        durationInFrames={270}
        fps={FPS}
        width={1176}
        height={756}
        defaultProps={{ theme: "light" as const }}
      />
    </>
  );
};
