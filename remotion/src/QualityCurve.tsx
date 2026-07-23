import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { themes, ThemeName } from "./theme";
import { fontB, fontD, fontM } from "./fonts";
import { cubicAt, loopFade, prog } from "./helpers";

// Quality vs. context fill: the curve droops as the window fills; the last
// stretch is the dumb zone. Used for both "context rot" and "dumb zone" slides.

const SEG1: [number, number][] = [
  [50, 48],
  [150, 54],
  [210, 74],
  [260, 108],
];
const SEG2: [number, number][] = [
  [260, 108],
  [300, 138],
  [350, 170],
  [410, 188],
];

const curvePoint = (p: number): [number, number] => {
  if (p <= 0.5) {
    return cubicAt(p / 0.5, SEG1[0], SEG1[1], SEG1[2], SEG1[3]);
  }
  return cubicAt((p - 0.5) / 0.5, SEG2[0], SEG2[1], SEG2[2], SEG2[3]);
};

export const QualityCurve: React.FC<{ theme: ThemeName }> = ({ theme }) => {
  const t = themes[theme];
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // curve drawing progress (30 → 200), then hold
  const p = prog(frame, 30, 200);
  const [dotX, dotY] = curvePoint(p);
  const zoneOn = prog(frame, 150, 178);

  // zone strips reveal as the dot passes their x-range
  const stripW = (x0: number, w: number) =>
    Math.max(0, Math.min(dotX - x0, w));

  return (
    <AbsoluteFill style={{ backgroundColor: t.bg }}>
      <svg
        viewBox="0 0 440 260"
        width="100%"
        height="100%"
        style={{ opacity: loopFade(frame, durationInFrames) }}
      >
        {/* dumb-zone box fades in when the dot enters it */}
        <g opacity={zoneOn}>
          <rect x={290} y={28} width={120} height={172} rx={8} fill={t.outerFill} stroke={t.coral} strokeWidth={1.5} strokeDasharray="6 5" />
          <text x={350} y={52} fontSize={12} textAnchor="middle" fill={t.accent} fontFamily={fontD} fontWeight={700}>
            THE DUMB ZONE
          </text>
          <text x={350} y={68} fontSize={9.5} textAnchor="middle" fill={t.muted} fontFamily={fontB} fontWeight={500}>
            last stretch of the window
          </text>
          <text x={350} y={150} fontSize={9.5} textAnchor="middle" fill={t.muted} fontFamily={fontB} fontWeight={500} opacity={prog(frame, 178, 198)}>
            forgets · redoes · ignores
          </text>
        </g>
        {/* axes */}
        <line x1={50} y1={24} x2={50} y2={200} stroke={t.lineStrong} strokeWidth={1.5} />
        <line x1={50} y1={200} x2={410} y2={200} stroke={t.lineStrong} strokeWidth={1.5} />
        <text x={24} y={112} fontSize={12} fill={t.muted} fontFamily={fontB} fontWeight={500} transform="rotate(-90 24 112)">
          quality
        </text>
        <text x={230} y={222} fontSize={12} textAnchor="middle" fill={t.muted} fontFamily={fontB} fontWeight={500}>
          context filled →
        </text>
        {/* quality curve, drawn progressively */}
        <path
          d="M50 48 C 150 54, 210 74, 260 108 C 300 138, 350 170, 410 188"
          fill="none"
          stroke={t.coral}
          strokeWidth={2.5}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - p}
        />
        {/* the dot riding the curve */}
        {p > 0 && p < 1 ? <circle cx={dotX} cy={dotY} r={5.5} fill={t.coral} /> : null}
        {/* zone strips under the axis, revealed by the dot's x position */}
        <rect x={50} y={200} width={stripW(50, 110)} height={7} fill={t.positive} />
        <rect x={160} y={200} width={stripW(160, 130)} height={7} fill={t.warning} />
        <rect x={290} y={200} width={stripW(290, 120)} height={7} fill={t.coral} />
        {dotX > 60 ? (
          <text x={60} y={196} fontSize={10} fill={t.positive} fontFamily={fontM} fontWeight={500}>
            sharp
          </text>
        ) : null}
        {dotX > 170 ? (
          <text x={170} y={196} fontSize={10} fill={t.warning} fontFamily={fontM} fontWeight={500}>
            slipping
          </text>
        ) : null}
        {dotX > 300 ? (
          <text x={300} y={196} fontSize={10} fill={t.coral} fontFamily={fontM} fontWeight={500}>
            rot
          </text>
        ) : null}
      </svg>
    </AbsoluteFill>
  );
};
