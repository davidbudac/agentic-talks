import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { themes, ThemeName } from "./theme";
import { fontB, fontD, fontM } from "./fonts";
import { loopFade, prog } from "./helpers";

// KV caching: turn after turn, everything already sent becomes cached prefix
// (~10× cheaper); only the appended tail is fresh. Append, never rewrite.

// Segment layout inside the bar (x from 30, total usable 340).
const TURNS = [
  { from: 20, newW: 96, label: "turn 1 — all fresh, full price" },
  { from: 110, newW: 98, label: "turn 2 — prefix cached ✓ (~10× cheaper)" },
  { from: 200, newW: 98, label: "turn 3 — cache grows, tail stays small" },
];

export const KvCache: React.FC<{ theme: ThemeName }> = ({ theme }) => {
  const t = themes[theme];
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // width of coral "new" segment per turn + how much prefix is cached (green)
  let cachedW = 0;
  let newX = 30;
  let newW = 0;
  for (let i = 0; i < TURNS.length; i++) {
    const turn = TURNS[i];
    const started = prog(frame, turn.from, turn.from + 1);
    if (started === 0) break;
    // previous new-segment converts to cached at turn start
    const priorTotal = TURNS.slice(0, i).reduce((a, x) => a + x.newW, 0);
    cachedW = interpolate(prog(frame, turn.from, turn.from + 24), [0, 1], [cachedW, priorTotal]);
    newX = 30 + priorTotal;
    newW = TURNS[i].newW * prog(frame, turn.from + (i === 0 ? 0 : 22), turn.from + 60);
  }

  const activeTurn = frame < 110 ? 0 : frame < 200 ? 1 : 2;

  return (
    <AbsoluteFill style={{ backgroundColor: t.bg }}>
      <svg
        viewBox="0 0 400 200"
        width="100%"
        height="100%"
        style={{ opacity: loopFade(frame, durationInFrames) }}
      >
        <text x={20} y={50} fontSize={12} fill={t.muted} fontFamily={fontB} fontWeight={500} opacity={prog(frame, 4, 18)}>
          one turn's input →
        </text>
        {/* bar frame */}
        <rect x={20} y={60} width={360} height={70} rx={10} fill={t.midFill} stroke={t.midStroke} strokeWidth={1.5} opacity={prog(frame, 0, 14)} />
        {/* cached prefix (green) */}
        {cachedW > 0 ? (
          <g>
            <rect x={30} y={70} width={cachedW} height={50} rx={6} fill={t.positive} opacity={0.85} />
            {cachedW > 130 ? (
              <text x={30 + cachedW / 2} y={100} fontSize={12} textAnchor="middle" fill={theme === "dark" ? t.bg : "#ffffff"} fontFamily={fontB} fontWeight={600}>
                cached ✓ ~10× cheaper
              </text>
            ) : cachedW > 40 ? (
              <text x={30 + cachedW / 2} y={100} fontSize={12} textAnchor="middle" fill={theme === "dark" ? t.bg : "#ffffff"} fontFamily={fontB} fontWeight={600}>
                cached ✓
              </text>
            ) : null}
          </g>
        ) : null}
        {/* fresh tail (coral) */}
        {newW > 0 ? (
          <g>
            <rect x={newX} y={70} width={newW} height={50} rx={6} fill={t.coral} />
            {newW > 30 ? (
              <text x={newX + newW / 2} y={98} fontSize={10.5} textAnchor="middle" fill={t.onHot} fontFamily={fontB} fontWeight={600}>
                new
              </text>
            ) : null}
          </g>
        ) : null}
        {/* per-turn caption */}
        {TURNS.map((turn, i) =>
          i === activeTurn ? (
            <text key={i} x={200} y={155} fontSize={11.5} textAnchor="middle" fill={t.muted} fontFamily={fontM} fontWeight={500} opacity={prog(frame, turn.from + 6, turn.from + 20)}>
              {turn.label}
            </text>
          ) : null,
        )}
        {/* closing rule */}
        <text x={200} y={182} fontSize={13} textAnchor="middle" fill={t.accent} fontFamily={fontD} fontWeight={700} opacity={prog(frame, 236, 254)}>
          append, never rewrite — same bytes, cheap forever
        </text>
      </svg>
    </AbsoluteFill>
  );
};
