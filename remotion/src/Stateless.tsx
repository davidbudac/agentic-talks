import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { themes, ThemeName } from "./theme";
import { fontB, fontD, fontM } from "./fonts";
import { loopFade, prog, pulse } from "./helpers";

// The model has no memory: three calls, each re-sending the whole (growing)
// history; after every call the model visibly forgets.

const CALLS = [
  { y: 36, w: 120, label: "call 1: [m1]", from: 0 },
  { y: 118, w: 180, label: "call 2: [m1,m2]", from: 85 },
  { y: 200, w: 232, label: "call 3: [m1,m2,m3]", from: 170 },
];

const ARROWS = [
  { d: "M144 51 C 220 60, 250 110, 258 128", hx: 258, hy: 128, hr: 62 },
  { d: "M204 133 C 235 140, 245 145, 250 148", hx: 250, hy: 148, hr: 25 },
  { d: "M254 212 C 258 207, 261 202, 265 196", hx: 265, hy: 196, hr: -55 },
];

export const Stateless: React.FC<{ theme: ThemeName }> = ({ theme }) => {
  const t = themes[theme];
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: t.bg }}>
      <svg
        viewBox="0 0 400 300"
        width="100%"
        height="100%"
        style={{ opacity: loopFade(frame, durationInFrames) }}
      >
        {/* model — pulses on each incoming call, then "forgets" */}
        {(() => {
          const hit =
            pulse(frame, 30, 62) + pulse(frame, 115, 147) + pulse(frame, 200, 232);
          const scale = 1 + 0.045 * Math.min(hit, 1);
          return (
            <g transform={`translate(312 150) scale(${scale}) translate(-312 -150)`}>
              <circle cx={312} cy={150} r={64} fill={t.coral} stroke={t.coral} />
              <text x={312} y={144} fontSize={17} textAnchor="middle" fill={t.onHot} fontFamily={fontB} fontWeight={600}>
                MODEL
              </text>
              <text x={312} y={166} fontSize={12} textAnchor="middle" fill={t.onHot} fontFamily={fontB} fontWeight={600}>
                forgets all
              </text>
            </g>
          );
        })()}
        {/* the forget flash after each call */}
        {[62, 147, 232].map((at, i) => {
          const o = pulse(frame, at, at + 34);
          if (o === 0) return null;
          return (
            <g key={i} opacity={o}>
              <text x={312} y={70} fontSize={13} textAnchor="middle" fill={t.accent} fontFamily={fontM} fontWeight={500}>
                ✕ wiped
              </text>
            </g>
          );
        })}
        {/* growing calls */}
        {CALLS.map((c, i) => {
          const grow = prog(frame, c.from, c.from + 26);
          if (grow === 0) return null;
          return (
            <g key={i} opacity={prog(frame, c.from, c.from + 10)}>
              <rect
                x={20}
                y={c.y}
                width={c.w * grow}
                height={30}
                rx={6}
                fill={t.midFill}
                stroke={t.midStroke}
                strokeWidth={1.5}
              />
              <text
                x={30}
                y={c.y + 20}
                fontSize={12.5}
                fill={t.muted}
                fontFamily={fontB}
                fontWeight={500}
                opacity={prog(frame, c.from + 10, c.from + 22)}
              >
                {c.label}
              </text>
              {/* re-sent part glows briefly on calls 2 & 3: the history is dragged along */}
              {i > 0 ? (
                <rect
                  x={20}
                  y={c.y}
                  width={CALLS[i - 1].w * grow}
                  height={30}
                  rx={6}
                  fill="none"
                  stroke={t.coral}
                  strokeWidth={2}
                  opacity={pulse(frame, c.from + 6, c.from + 40) * 0.9}
                />
              ) : null}
            </g>
          );
        })}
        {/* arrows call → model */}
        {ARROWS.map((a, i) => {
          const from = CALLS[i].from + 24;
          const draw = prog(frame, from, from + 16);
          if (draw === 0) return null;
          return (
            <g key={i}>
              <path
                d={a.d}
                fill="none"
                stroke={t.coral}
                strokeWidth={2.5}
                pathLength={1}
                strokeDasharray={1}
                strokeDashoffset={1 - draw}
              />
              <path
                d="M0,-4.5 L8,0 L0,4.5 Z"
                fill={t.coral}
                opacity={prog(frame, from + 12, from + 18)}
                transform={`translate(${a.hx} ${a.hy}) rotate(${a.hr})`}
              />
            </g>
          );
        })}
        {/* closing caption */}
        <text
          x={150}
          y={284}
          fontSize={13}
          fill={t.accent}
          fontFamily={fontD}
          fontWeight={700}
          opacity={prog(frame, 246, 266)}
        >
          every call re-sends the whole history
        </text>
      </svg>
    </AbsoluteFill>
  );
};
