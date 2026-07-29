import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { themes, ThemeName } from "./theme";
import { fontB, fontD, fontM } from "./fonts";
import { loopFade, prog, pulse } from "./helpers";

// Progressive disclosure: a CLAUDE.md line is paid on every turn of every
// session; a skill keeps only its one-line description in context and loads
// the full instructions on the turn that actually triggers it.

const COLS = [112, 192, 272, 352]; // turn column centers
const COL_W = 72;
const TRIGGER_TURN = 2; // 0-based: turn 3 fires the skill
const TURN_FROM = (i: number) => 26 + i * 44;

export const ProgressiveDisclosure: React.FC<{ theme: ThemeName }> = ({ theme }) => {
  const t = themes[theme];
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const laneA = 56; // CLAUDE.md lane top
  const laneB = 144; // skill lane top
  const BOX_H = 62;

  return (
    <AbsoluteFill style={{ backgroundColor: t.bg }}>
      <svg
        viewBox="0 0 420 250"
        width="100%"
        height="100%"
        style={{ opacity: loopFade(frame, durationInFrames) }}
      >
        {/* turn headers */}
        {COLS.map((cx, i) => (
          <text key={i} x={cx} y={36} fontSize={10} textAnchor="middle" fill={t.faint} fontFamily={fontM} fontWeight={500} opacity={prog(frame, TURN_FROM(i), TURN_FROM(i) + 12)}>
            turn {i + 1}
          </text>
        ))}

        {/* lane labels */}
        <text x={8} y={laneA + 30} fontSize={10.5} fill={t.text} fontFamily={fontD} fontWeight={700} opacity={prog(frame, 4, 18)}>
          CLAUDE.md
        </text>
        <text x={8} y={laneB + 30} fontSize={10.5} fill={t.text} fontFamily={fontD} fontWeight={700} opacity={prog(frame, 4, 18)}>
          skill
        </text>

        {/* lane A: full text present in every turn */}
        {COLS.map((cx, i) => {
          const from = TURN_FROM(i);
          const p = prog(frame, from, from + 16);
          if (p === 0) return null;
          return (
            <g key={i} opacity={p}>
              <rect x={cx - COL_W / 2} y={laneA} width={COL_W} height={BOX_H} rx={7} fill={t.midFill} stroke={t.midStroke} strokeWidth={1.2} />
              <rect x={cx - COL_W / 2 + 7} y={laneA + 9} width={COL_W - 14} height={BOX_H - 18} rx={4} fill={t.coral} opacity={0.9} />
              <text x={cx} y={laneA + BOX_H / 2 + 3.5} fontSize={8.5} textAnchor="middle" fill={t.onHot} fontFamily={fontB} fontWeight={600}>
                full text
              </text>
            </g>
          );
        })}
        <text x={COLS[3] + COL_W / 2 + 6} y={laneA + BOX_H / 2 - 2} fontSize={11} fill={t.muted} fontFamily={fontB} fontWeight={600} opacity={prog(frame, TURN_FROM(3) + 16, TURN_FROM(3) + 30)}>
          paid
        </text>
        <text x={COLS[3] + COL_W / 2 + 6} y={laneA + BOX_H / 2 + 12} fontSize={11} fill={t.muted} fontFamily={fontB} fontWeight={600} opacity={prog(frame, TURN_FROM(3) + 16, TURN_FROM(3) + 30)}>
          ×4
        </text>

        {/* lane B: description sliver every turn, full load only on trigger */}
        {COLS.map((cx, i) => {
          const from = TURN_FROM(i);
          const p = prog(frame, from, from + 16);
          if (p === 0) return null;
          const isTrigger = i === TRIGGER_TURN;
          const loadP = isTrigger ? prog(frame, from + 20, from + 38) : 0;
          return (
            <g key={i} opacity={p}>
              <rect x={cx - COL_W / 2} y={laneB} width={COL_W} height={BOX_H} rx={7} fill={t.midFill} stroke={isTrigger ? t.coral : t.midStroke} strokeWidth={isTrigger ? 1.6 + pulse(frame, from + 16, from + 44) : 1.2} />
              {/* one-line description — always present, nearly free */}
              <rect x={cx - COL_W / 2 + 7} y={laneB + 9} width={COL_W - 14} height={6} rx={3} fill={t.coral} opacity={0.9} />
              {/* full instructions load only when triggered */}
              {isTrigger && loadP > 0 ? (
                <g opacity={loadP}>
                  <rect x={cx - COL_W / 2 + 7} y={laneB + 21} width={COL_W - 14} height={(BOX_H - 30) * loadP} rx={4} fill={t.coral} opacity={0.9} />
                  <text x={cx} y={laneB + BOX_H / 2 + 10} fontSize={8} textAnchor="middle" fill={t.onHot} fontFamily={fontB} fontWeight={600} opacity={loadP > 0.8 ? 1 : 0}>
                    full how-to
                  </text>
                </g>
              ) : null}
            </g>
          );
        })}
        {/* description callout on the first skill box */}
        <text x={COLS[0]} y={laneB - 6} fontSize={8.5} textAnchor="middle" fill={t.faint} fontFamily={fontM} fontWeight={500} opacity={prog(frame, TURN_FROM(0) + 14, TURN_FROM(0) + 28)}>
          description only
        </text>
        {/* trigger callout */}
        <g opacity={prog(frame, TURN_FROM(TRIGGER_TURN) + 18, TURN_FROM(TRIGGER_TURN) + 32)}>
          <text x={COLS[TRIGGER_TURN]} y={laneB + BOX_H + 17} fontSize={9.5} textAnchor="middle" fill={t.accent} fontFamily={fontM} fontWeight={600}>
            ▲ triggered — loads now
          </text>
        </g>
        <text x={COLS[3] + COL_W / 2 + 6} y={laneB + BOX_H / 2 - 2} fontSize={11} fill={t.muted} fontFamily={fontB} fontWeight={600} opacity={prog(frame, TURN_FROM(3) + 16, TURN_FROM(3) + 30)}>
          paid
        </text>
        <text x={COLS[3] + COL_W / 2 + 6} y={laneB + BOX_H / 2 + 12} fontSize={11} fill={t.muted} fontFamily={fontB} fontWeight={600} opacity={prog(frame, TURN_FROM(3) + 16, TURN_FROM(3) + 30)}>
          ×1
        </text>

        {/* closing rule */}
        <text x={210} y={246} fontSize={13} textAnchor="middle" fill={t.accent} fontFamily={fontD} fontWeight={700} opacity={prog(frame, 236, 254)}>
          same knowledge — paid every turn vs. paid on trigger
        </text>
      </svg>
    </AbsoluteFill>
  );
};
