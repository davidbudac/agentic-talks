import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { themes, ThemeName } from "./theme";
import { fontB, fontD, fontM } from "./fonts";
import { loopFade, prog, pulse } from "./helpers";

// The context lifecycle of a session: every request re-sends the whole
// window. The fixed overhead (system prompt, CLAUDE.md, tool schemas) is
// stamped identically into every turn; only the conversation grows.

const BAR_X = 74;
const FIXED = [
  { w: 38, label: "sys" },
  { w: 62, label: "CLAUDE.md" },
  { w: 46, label: "tools" },
];
const FIXED_W = FIXED.reduce((a, s) => a + s.w, 0); // 146
const ROWS = [
  { y: 74, from: 14, convW: 42, label: "turn 1" },
  { y: 128, from: 96, convW: 96, label: "turn 2" },
  { y: 182, from: 168, convW: 158, label: "turn 3" },
];
const ROW_H = 36;

export const ContextLifecycle: React.FC<{ theme: ThemeName }> = ({ theme }) => {
  const t = themes[theme];
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: t.bg }}>
      <svg
        viewBox="0 0 420 250"
        width="100%"
        height="100%"
        style={{ opacity: loopFade(frame, durationInFrames) }}
      >
        {/* header */}
        <text x={210} y={22} fontSize={12.5} textAnchor="middle" fill={t.muted} fontFamily={fontB} fontWeight={500} opacity={prog(frame, 2, 16)}>
          one request = the whole window, sent again
        </text>

        {/* column brackets */}
        <g opacity={prog(frame, 210, 228)}>
          <path d={`M${BAR_X} 46 L${BAR_X} 40 L${BAR_X + FIXED_W} 40 L${BAR_X + FIXED_W} 46`} fill="none" stroke={t.faint} strokeWidth={1.4} />
          <text x={BAR_X + FIXED_W / 2} y={34} fontSize={10} textAnchor="middle" fill={t.muted} fontFamily={fontM} fontWeight={500}>
            fixed overhead — resent every turn
          </text>
          <path d={`M${BAR_X + FIXED_W + 8} 46 L${BAR_X + FIXED_W + 8} 40 L${BAR_X + FIXED_W + 170} 40 L${BAR_X + FIXED_W + 170} 46`} fill="none" stroke={t.coral} strokeWidth={1.4} />
          <text x={BAR_X + FIXED_W + 89} y={34} fontSize={10} textAnchor="middle" fill={t.accent} fontFamily={fontM} fontWeight={600}>
            only this grows
          </text>
        </g>

        {ROWS.map((row, i) => {
          const appeared = prog(frame, row.from, row.from + 1);
          if (appeared === 0) return null;
          // turn 1 builds segment by segment; later turns stamp the fixed
          // prefix in one motion — it's the same bytes again.
          const stamp = prog(frame, row.from, row.from + (i === 0 ? 40 : 14));
          const convStart = row.from + (i === 0 ? 44 : 18);
          const convW = row.convW * prog(frame, convStart, convStart + 28);
          const stampPulse = i > 0 ? pulse(frame, row.from, row.from + 22) : 0;
          return (
            <g key={i}>
              <text x={BAR_X - 12} y={row.y + ROW_H / 2 + 4} fontSize={11} textAnchor="end" fill={t.text} fontFamily={fontD} fontWeight={700} opacity={appeared}>
                {row.label}
              </text>
              {/* fixed prefix segments */}
              {FIXED.map((seg, j) => {
                const segX = BAR_X + FIXED.slice(0, j).reduce((a, s) => a + s.w, 0);
                const segP = i === 0 ? prog(frame, row.from + j * 13, row.from + j * 13 + 13) : stamp;
                if (segP === 0) return null;
                return (
                  <g key={j} opacity={segP}>
                    <rect x={segX + 1.5} y={row.y} width={seg.w - 3} height={ROW_H} rx={5} fill={t.midFill} stroke={t.midStroke} strokeWidth={1.2 + stampPulse} />
                    <text x={segX + seg.w / 2} y={row.y + ROW_H / 2 + 3.5} fontSize={8.5} textAnchor="middle" fill={t.muted} fontFamily={fontM} fontWeight={500}>
                      {seg.label}
                    </text>
                  </g>
                );
              })}
              {/* "same bytes" stamp note on later turns */}
              {i > 0 ? (
                <text x={BAR_X + FIXED_W / 2} y={row.y - 5} fontSize={8.5} textAnchor="middle" fill={t.faint} fontFamily={fontM} fontWeight={500} opacity={stampPulse}>
                  ↻ same bytes, billed again
                </text>
              ) : null}
              {/* conversation segment */}
              {convW > 0 ? (
                <g>
                  <rect x={BAR_X + FIXED_W + 3} y={row.y} width={convW} height={ROW_H} rx={5} fill={t.coral} />
                  {convW > 56 ? (
                    <text x={BAR_X + FIXED_W + 3 + convW / 2} y={row.y + ROW_H / 2 + 3.5} fontSize={9} textAnchor="middle" fill={t.onHot} fontFamily={fontB} fontWeight={600}>
                      conversation
                    </text>
                  ) : null}
                </g>
              ) : null}
            </g>
          );
        })}

        {/* growth hint under the last row */}
        <text x={BAR_X + FIXED_W + 170} y={200 + 4} fontSize={13} fill={t.accent} fontFamily={fontB} fontWeight={700} opacity={prog(frame, 200, 214)}>
          …
        </text>

        {/* closing rule */}
        <text x={210} y={242} fontSize={13} textAnchor="middle" fill={t.accent} fontFamily={fontD} fontWeight={700} opacity={prog(frame, 244, 262)}>
          every line of overhead is paid on every turn
        </text>
      </svg>
    </AbsoluteFill>
  );
};
