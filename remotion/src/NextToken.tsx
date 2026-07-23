import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { themes, ThemeName } from "./theme";
import { fontB, fontD, fontM } from "./fonts";
import { loopFade, prog, pulse } from "./helpers";

// Next-token prediction: prompt → model → probability bars → the winner is
// sampled and lands in the blank. One cycle, soft loop.

const CANDIDATES = [
  { word: "passing", p: 0.62, y: 62, w: 74, kind: "coral" },
  { word: "failing", p: 0.28, y: 102, w: 34, kind: "warn" },
  { word: "green", p: 0.06, y: 150, w: 10, kind: "dim" },
  { word: "red", p: 0.04, y: 198, w: 7, kind: "dim" },
];

export const NextToken: React.FC<{ theme: ThemeName }> = ({ theme }) => {
  const t = themes[theme];
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const barFill = (kind: string) =>
    kind === "coral" ? t.coral : kind === "warn" ? t.warning : t.cardBg;

  // the sampled word flies from its bar into the blank
  const fly = prog(frame, 122, 150);
  const flyX = 252 + (52 - 252) * fly;
  const flyY = 58 + (134 - 58) * fly;

  return (
    <AbsoluteFill style={{ backgroundColor: t.bg }}>
      <svg
        viewBox="0 0 400 250"
        width="100%"
        height="100%"
        style={{ opacity: loopFade(frame, durationInFrames) }}
      >
        {/* prompt box */}
        <rect x={14} y={98} width={132} height={50} rx={9} fill={t.midFill} stroke={t.midStroke} strokeWidth={1.5} />
        <text x={80} y={120} fontSize={12.5} textAnchor="middle" fill={t.text} fontFamily={fontB} fontWeight={600}>
          "The tests
        </text>
        <text x={80} y={138} fontSize={12.5} textAnchor="middle" fill={t.text} fontFamily={fontB} fontWeight={600}>
          are{" "}
          {fly >= 1 ? (
            <tspan fill={t.accent} fontWeight={700}>
              passing"
            </tspan>
          ) : (
            <tspan fill={t.faint}>___"</tspan>
          )}
        </text>
        {/* arrow prompt → model */}
        {(() => {
          const draw = prog(frame, 14, 30);
          return (
            <g>
              <path
                d="M148 123 L 162 123"
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
                opacity={prog(frame, 26, 32)}
                transform="translate(162 123)"
              />
            </g>
          );
        })()}
        {/* model — pulses while "deciding" */}
        {(() => {
          const scale = 1 + 0.05 * pulse(frame, 30, 62);
          return (
            <g transform={`translate(200 123) scale(${scale}) translate(-200 -123)`}>
              <circle cx={200} cy={123} r={34} fill={t.coral} />
              <text x={200} y={120} fontSize={12} textAnchor="middle" fill={t.onHot} fontFamily={fontB} fontWeight={600}>
                MODEL
              </text>
              <text x={200} y={136} fontSize={9.5} textAnchor="middle" fill={t.onHot} fontFamily={fontB} fontWeight={600}>
                next?
              </text>
            </g>
          );
        })()}
        <path
          d="M234 118 C 250 100, 250 80, 300 60"
          fill="none"
          stroke={t.lineStrong}
          strokeWidth={1.5}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - prog(frame, 40, 56)}
        />
        {/* candidate bars grow in, staggered */}
        {CANDIDATES.map((c, i) => {
          const from = 48 + i * 10;
          const grow = prog(frame, from, from + 26);
          const picked = c.word === "passing";
          // non-winners dim once sampling starts
          const dimmed = !picked ? 1 - 0.6 * prog(frame, 106, 122) : 1;
          if (grow === 0) return null;
          return (
            <g key={c.word} opacity={dimmed}>
              <text
                x={252}
                y={c.y}
                fontSize={12}
                fill={c.kind === "dim" ? t.muted : t.text}
                fontFamily={fontB}
                fontWeight={600}
                opacity={fly > 0 && picked ? 1 - fly : 1}
              >
                {c.word}
              </text>
              <rect
                x={312}
                y={c.y - 10}
                width={c.w * grow}
                height={12}
                rx={3}
                fill={barFill(c.kind)}
                stroke={c.kind === "dim" ? t.cardBorder : "none"}
                strokeWidth={c.kind === "dim" ? 1.5 : 0}
              />
              <text x={252} y={c.y + 14} fontSize={10} fill={t.muted} fontFamily={fontM} fontWeight={500} opacity={prog(frame, from + 18, from + 28)}>
                {c.p.toFixed(2)}
              </text>
              {/* sampling ring around the winner */}
              {picked ? (
                <rect
                  x={246}
                  y={c.y - 16}
                  width={146}
                  height={34}
                  rx={7}
                  fill="none"
                  stroke={t.coral}
                  strokeWidth={2}
                  opacity={pulse(frame, 100, 130)}
                />
              ) : null}
            </g>
          );
        })}
        {/* the word in flight */}
        {fly > 0 && fly < 1 ? (
          <text x={flyX} y={flyY} fontSize={12.5} fill={t.accent} fontFamily={fontB} fontWeight={700}>
            passing
          </text>
        ) : null}
        {/* closing caption */}
        <text
          x={200}
          y={232}
          fontSize={12.5}
          textAnchor="middle"
          fill={t.accent}
          fontFamily={fontD}
          fontWeight={700}
          opacity={prog(frame, 158, 176)}
        >
          sample · append · repeat
        </text>
      </svg>
    </AbsoluteFill>
  );
};
