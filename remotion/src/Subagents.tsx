import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { themes, ThemeName, rad, sw } from "./theme";
import { fontsFor } from "./fonts";
import { cubicAt, loopFade, prog, pulse } from "./helpers";

// Sub-agents: the main agent delegates, each sub-agent churns through messy
// work in its own context, and only a tiny summary travels back up.

const SUBS = [
  { x: 20, arrow: "M170 64 C 120 100, 90 130, 78 166", pts: [[170, 64], [120, 100], [90, 130], [78, 166]] as [number, number][] },
  { x: 155, arrow: "M210 64 L 210 166", pts: [[210, 64], [210, 98], [210, 132], [210, 166]] as [number, number][] },
  { x: 290, arrow: "M250 64 C 300 100, 330 130, 342 166", pts: [[250, 64], [300, 100], [330, 130], [342, 166]] as [number, number][] },
];

export const Subagents: React.FC<{ theme: ThemeName }> = ({ theme }) => {
  const t = themes[theme];
  const { fontB, fontD, fontM } = fontsFor(theme);
  const lab = (x: string) => (t.upperLabels ? x.toUpperCase() : x);
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: t.bg }}>
      <svg
        viewBox="0 0 420 270"
        width="100%"
        height="100%"
        style={{ opacity: loopFade(frame, durationInFrames) }}
      >
        {/* main agent */}
        {(() => {
          const scale = 1 + 0.04 * (pulse(frame, 4, 30) + pulse(frame, 196, 226));
          return (
            <g transform={`translate(210 38) scale(${scale}) translate(-210 -38)`}>
              <rect
                x={135}
                y={14}
                width={150}
                height={48}
                rx={rad(t, 10)}
                fill={t.hotFilled ? t.coral : t.cardBg}
                stroke={t.hotFilled ? "none" : t.midStroke}
                strokeWidth={t.hotFilled ? 0 : sw(t, 1.5)}
              />
              <text x={210} y={43} fontSize={15} textAnchor="middle" fill={t.hotFilled ? t.onHot : t.text} fontFamily={fontB} fontWeight={600}>
                MAIN AGENT
              </text>
            </g>
          );
        })()}
        {/* delegate arrows, staggered */}
        {SUBS.map((s, i) => {
          const from = 26 + i * 8;
          const draw = prog(frame, from, from + 22);
          if (draw === 0) return null;
          const [hx, hy] = s.pts[3];
          return (
            <g key={i}>
              <path d={s.arrow} fill="none" stroke={t.flow} strokeWidth={sw(t, 2.5)} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
              <path d="M-4.5,-8 L0,0 L4.5,-8 Z" fill={t.flow} opacity={prog(frame, from + 18, from + 24)} transform={`translate(${hx} ${hy})`} />
            </g>
          );
        })}
        <text x={t.flat ? 100 : 96} y={108} textAnchor={t.flat ? "end" : "start"} fontSize={12} fill={t.quiet} fontFamily={fontD} fontWeight={t.bold} opacity={prog(frame, 34, 50)}>
          delegate ↓
        </text>
        {/* sub-agents with churn gauges */}
        {SUBS.map((s, i) => {
          const appear = prog(frame, 48 + i * 8, 62 + i * 8);
          const churn = prog(frame, 70 + i * 6, 176);
          const tokens = Math.round(80 * churn);
          if (appear === 0) return null;
          return (
            <g key={i} opacity={appear}>
              <rect x={s.x} y={170} width={110} height={70} rx={rad(t, 10)} fill={t.midFill} stroke={t.midStroke} strokeWidth={sw(t, 1.5)} />
              <text x={s.x + 55} y={192} fontSize={13} textAnchor="middle" fill={t.text} fontFamily={fontB} fontWeight={600}>
                sub-agent
              </text>
              {/* its own context gauge, filling up with messy work */}
              <rect x={s.x + 12} y={204} width={86} height={10} rx={rad(t, 3)} fill="none" stroke={t.cardBorder} strokeWidth={sw(t, 1.2)} />
              <rect x={s.x + 13} y={205} width={84 * churn} height={8} rx={rad(t, 2.5)} fill={t.warning} />
              <text x={s.x + 55} y={230} fontSize={10} textAnchor="middle" fill={t.muted} fontFamily={fontM} fontWeight={t.monoWeight} letterSpacing={t.monoTracking}>
                {lab(churn > 0 ? `${tokens}k tokens` : "own context")}
              </text>
            </g>
          );
        })}
        {/* tiny summaries travel back up the arrows */}
        {SUBS.map((s, i) => {
          const p = prog(frame, 190 + i * 6, 218 + i * 6);
          if (p <= 0 || p >= 1) return null;
          const [x, y] = cubicAt(1 - p, s.pts[0], s.pts[1], s.pts[2], s.pts[3]);
          return <circle key={i} cx={x} cy={y} r={5} fill={t.dot} />;
        })}
        {t.flat ? (
          // two lines, centred in the free lane between the middle arrow and the right-hand curve
          <g opacity={prog(frame, 200, 216)} fill={t.muted} fontSize={11} fontFamily={fontB} fontWeight={500} textAnchor="middle">
            <text x={264} y={140}>↑ tiny</text>
            <text x={264} y={154}>summary back</text>
          </g>
        ) : (
          <text x={310} y={150} fontSize={11} textAnchor="middle" fill={t.muted} fontFamily={fontB} fontWeight={500} opacity={prog(frame, 200, 216)}>
            ↑ tiny summary back
          </text>
        )}
        {/* closing caption */}
        <text x={210} y={262} fontSize={12} textAnchor="middle" fill={t.caption} fontFamily={fontD} fontWeight={t.captionWeight} opacity={prog(frame, 226, 244)}>
          80k tokens burned inside — a 200-token answer out
        </text>
      </svg>
    </AbsoluteFill>
  );
};
