import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { themes, ThemeName } from "./theme";
import { fontB, fontD } from "./fonts";
import { loopFade, prog, pulse } from "./helpers";

// The agent loop: ① model proposes → ② harness runs it → ③ result back → ④ repeat.
// Four stages of 60 frames each; the cycle is seamless.

const STAGE = 60;

interface Node {
  x: number;
  y: number;
  w: number;
  h: number;
  lines: string[];
  hot?: boolean;
}

const NODES: Node[] = [
  { x: 140, y: 14, w: 200, h: 60, lines: ["① Model proposes", "an action"] },
  { x: 332, y: 160, w: 138, h: 60, lines: ["② Harness", "runs it"], hot: true },
  { x: 140, y: 306, w: 200, h: 60, lines: ["③ Result back", "to the model"] },
  { x: 10, y: 160, w: 138, h: 60, lines: ["④ Repeat", "until done"] },
];

// Clockwise arcs, arc i goes from node i to node i+1.
const ARCS = [
  "M344 64 A 160 160 0 0 1 452 156",
  "M452 224 A 160 160 0 0 1 344 316",
  "M136 316 A 160 160 0 0 1 28 224",
  "M28 156 A 160 160 0 0 1 136 64",
];

// Arrowhead positions/rotations at each arc's end.
const HEADS: { x: number; y: number; r: number }[] = [
  { x: 452, y: 156, r: 65 },
  { x: 344, y: 316, r: 155 },
  { x: 28, y: 224, r: 245 },
  { x: 136, y: 64, r: 335 },
];

export const AgentLoop: React.FC<{ theme: ThemeName }> = ({ theme }) => {
  const t = themes[theme];
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const stage = Math.floor(frame / STAGE) % 4;
  const inStage = frame % STAGE;

  return (
    <AbsoluteFill style={{ backgroundColor: t.bg }}>
      <svg
        viewBox="0 0 480 380"
        width="100%"
        height="100%"
        style={{ opacity: loopFade(frame, durationInFrames) }}
      >
        {/* dim base arcs */}
        {ARCS.map((d, i) => (
          <path
            key={`base-${i}`}
            d={d}
            fill="none"
            stroke={t.lineStrong}
            strokeWidth={1.5}
          />
        ))}
        {/* active arc draws over its stage */}
        {ARCS.map((d, i) => {
          const draw =
            i === stage
              ? prog(inStage, 8, 44)
              : i === (stage + 3) % 4
                ? 1 // previous arc stays lit while it fades
                : 0;
          const fade = i === (stage + 3) % 4 ? 1 - prog(inStage, 0, 24) : 1;
          if (draw === 0) return null;
          return (
            <path
              key={`hot-${i}`}
              d={d}
              fill="none"
              stroke={t.coral}
              strokeWidth={2.8}
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - draw}
              opacity={fade}
            />
          );
        })}
        {/* arrowheads pop when their arc completes */}
        {HEADS.map((h, i) => {
          const on =
            i === stage
              ? prog(inStage, 40, 50)
              : i === (stage + 3) % 4
                ? 1 - prog(inStage, 0, 24)
                : 0;
          if (on === 0) return null;
          return (
            <path
              key={`head-${i}`}
              d="M0,-5 L9,0 L0,5 Z"
              fill={t.coral}
              opacity={on}
              transform={`translate(${h.x} ${h.y}) rotate(${h.r})`}
            />
          );
        })}
        {/* nodes; node (stage+1)%4 lights up as the arc reaches it, node stage is active */}
        {NODES.map((n, i) => {
          const cx = n.x + n.w / 2;
          const cy = n.y + n.h / 2;
          const isActive = i === stage;
          const arriving = i === (stage + 1) % 4 ? prog(inStage, 44, 58) : 0;
          const activeAmt = isActive
            ? Math.max(prog(inStage, 0, 10), 1) - prog(inStage, 46, 60) * 0.35
            : arriving * 0.65;
          const scale = 1 + 0.05 * activeAmt + 0.02 * pulse(inStage, 0, 26) * (isActive ? 1 : 0);
          const stroke = isActive || arriving > 0 ? t.coral : n.hot ? t.coral : t.cardBorder;
          const strokeW = isActive ? 3 : 1.5;
          return (
            <g key={`node-${i}`} transform={`translate(${cx} ${cy}) scale(${scale}) translate(${-cx} ${-cy})`}>
              <rect
                x={n.x}
                y={n.y}
                width={n.w}
                height={n.h}
                rx={12}
                fill={n.hot ? t.coral : t.cardBg}
                stroke={stroke}
                strokeWidth={strokeW}
              />
              {isActive ? (
                <rect
                  x={n.x - 5}
                  y={n.y - 5}
                  width={n.w + 10}
                  height={n.h + 10}
                  rx={16}
                  fill="none"
                  stroke={t.coral}
                  strokeWidth={2}
                  opacity={0.35 * (1 - prog(inStage, 40, 60))}
                />
              ) : null}
              {n.lines.map((line, li) => (
                <text
                  key={li}
                  x={cx}
                  y={n.y + 26 + li * 19}
                  fontSize={15}
                  textAnchor="middle"
                  fill={n.hot ? t.onHot : t.text}
                  fontFamily={fontB}
                  fontWeight={600}
                >
                  {line}
                </text>
              ))}
            </g>
          );
        })}
        {/* center label with a soft breathing pulse */}
        <g opacity={0.85 + 0.15 * Math.sin((frame / durationInFrames) * Math.PI * 8)}>
          <text x={240} y={185} fontSize={16} textAnchor="middle" fill={t.accent} fontFamily={fontD} fontWeight={700}>
            THE
          </text>
          <text x={240} y={206} fontSize={16} textAnchor="middle" fill={t.accent} fontFamily={fontD} fontWeight={700}>
            LOOP
          </text>
        </g>
      </svg>
    </AbsoluteFill>
  );
};
