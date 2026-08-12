import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { themes, ThemeName } from "./theme";
import { fontB, fontD, fontM } from "./fonts";
import { loopFade, prog, pulse } from "./helpers";

// Multi-hop retrieval: vector search grabs the chunks that LOOK like the
// question — the graph walks the edges that CONNECT to the answer.

// Same node layout in both panels (panel-local coords).
const N = {
  A: [104, 148] as const, // entity matched by the query
  B: [150, 92] as const,
  C: [216, 56] as const, // the answer, two hops away
  D: [70, 62] as const,
  E: [160, 158] as const, // look-alikes the query pulls by similarity
};
const EDGES: [keyof typeof N, keyof typeof N][] = [
  ["A", "B"],
  ["B", "C"],
  ["A", "D"],
  ["D", "B"],
  ["A", "E"],
];
const QUERY = { x: 8, y: 168, w: 64, h: 30 };
// rays the vector panel shoots at the top-k look-alikes
const TOPK: (keyof typeof N)[] = ["E", "B", "D"];

const Panel: React.FC<{
  t: (typeof themes)["light"];
  frame: number;
  kind: "vector" | "graph";
}> = ({ t, frame, kind }) => {
  const vector = kind === "vector";
  const hop1 = prog(frame, 150, 176); // A→B
  const hop2 = prog(frame, 184, 210); // B→C
  const found = prog(frame, 214, 230);
  return (
    <g>
      {/* chunks / entities — same dots in both panels */}
      {(Object.keys(N) as (keyof typeof N)[]).map((k) => {
        const [x, y] = N[k];
        const isAnswer = k === "C";
        const isTopK = vector && TOPK.includes(k);
        const flash = isTopK ? prog(frame, 58 + TOPK.indexOf(k) * 8, 74 + TOPK.indexOf(k) * 8) : 0;
        const lit = !vector && ((k === "A" && hop1 > 0) || (k === "B" && hop1 >= 1) || (k === "C" && found > 0));
        return (
          <g key={k}>
            <circle
              cx={x}
              cy={y}
              r={12 + (isAnswer && !vector ? 2.5 * found : 0)}
              fill={lit || (isAnswer && !vector && found > 0) ? t.coral : flash > 0.4 ? t.warning : t.cardBg}
              stroke={lit ? t.coral : flash > 0.4 ? t.warning : t.cardBorder}
              strokeWidth={1.6}
              opacity={prog(frame, 6, 22)}
            />
            {isAnswer && (
              <text
                x={x}
                y={y - 20}
                fontSize={10.5}
                textAnchor="middle"
                fill={vector ? t.faint : found > 0 ? t.accent : t.faint}
                fontFamily={fontM}
                fontWeight={500}
                opacity={prog(frame, 24, 38)}
              >
                {!vector && found > 0 ? "✓ the answer" : "the answer"}
              </text>
            )}
          </g>
        );
      })}
      {/* graph panel: the edges exist; vector panel: just chunks in space */}
      {!vector &&
        EDGES.map(([a, b], i) => {
          const [x1, y1] = N[a];
          const [x2, y2] = N[b];
          const isHop = (a === "A" && b === "B") || (a === "B" && b === "C");
          const draw = a === "A" && b === "B" ? hop1 : a === "B" && b === "C" ? hop2 : 1;
          return (
            <g key={i}>
              <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={t.line} strokeWidth={1.4} opacity={prog(frame, 10, 26)} />
              {isHop && draw > 0 && (
                <line
                  x1={x1}
                  y1={y1}
                  x2={x1 + (x2 - x1) * draw}
                  y2={y1 + (y2 - y1) * draw}
                  stroke={t.coral}
                  strokeWidth={2.6}
                />
              )}
            </g>
          );
        })}
      {/* hop labels */}
      {!vector && (
        <>
          <text x={140} y={130} fontSize={10.5} fill={t.accent} fontFamily={fontD} fontWeight={700} opacity={hop1}>
            hop 1
          </text>
          <text x={192} y={82} fontSize={10.5} fill={t.accent} fontFamily={fontD} fontWeight={700} opacity={hop2}>
            hop 2
          </text>
        </>
      )}
      {/* the query box */}
      {(() => {
        const scale = 1 + 0.05 * (vector ? pulse(frame, 30, 56) : pulse(frame, 128, 152));
        const cx = QUERY.x + QUERY.w / 2;
        const cy = QUERY.y + QUERY.h / 2;
        return (
          <g transform={`translate(${cx} ${cy}) scale(${scale}) translate(${-cx} ${-cy})`} opacity={prog(frame, 2, 16)}>
            <rect x={QUERY.x} y={QUERY.y} width={QUERY.w} height={QUERY.h} rx={7} fill={t.coral} />
            <text
              x={cx}
              y={cy + 4}
              fontSize={11.5}
              textAnchor="middle"
              fill={t.onHot}
              fontFamily={fontB}
              fontWeight={600}
            >
              query
            </text>
          </g>
        );
      })()}
      {/* vector: dashed similarity rays to the look-alikes */}
      {vector &&
        TOPK.map((k, i) => {
          const [x, y] = N[k];
          const draw = prog(frame, 34 + i * 8, 56 + i * 8);
          if (draw === 0) return null;
          const x1 = QUERY.x + QUERY.w;
          const y1 = QUERY.y + 8;
          return (
            <line
              key={k}
              x1={x1}
              y1={y1}
              x2={x1 + (x - x1) * draw}
              y2={y1 + (y - y1) * draw}
              stroke={t.warning}
              strokeWidth={1.8}
              strokeDasharray="5 4"
            />
          );
        })}
      {/* graph: query matches entity A first */}
      {!vector &&
        (() => {
          const draw = prog(frame, 132, 150);
          if (draw === 0) return null;
          const x1 = QUERY.x + QUERY.w;
          const y1 = QUERY.y + 8;
          const [x2, y2] = N.A;
          return (
            <line
              x1={x1}
              y1={y1}
              x2={x1 + (x2 - x1) * draw}
              y2={y1 + (y2 - y1) * draw}
              stroke={t.coral}
              strokeWidth={2.2}
            />
          );
        })()}
      {/* panel verdicts */}
      {vector ? (
        <text x={130} y={216} fontSize={11.5} textAnchor="middle" fill={t.muted} fontFamily={fontB} fontWeight={500} opacity={prog(frame, 84, 100)}>
          similar ≠ connected · Recall@5 ≈ 73%
        </text>
      ) : (
        <text x={130} y={216} fontSize={11.5} textAnchor="middle" fill={t.muted} fontFamily={fontB} fontWeight={500} opacity={prog(frame, 232, 248)}>
          follows edges, not likeness · ≈ 88%
        </text>
      )}
    </g>
  );
};

export const GraphHops: React.FC<{ theme: ThemeName }> = ({ theme }) => {
  const t = themes[theme];
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: t.bg }}>
      <svg viewBox="0 0 580 250" width="100%" height="100%" style={{ opacity: loopFade(frame, durationInFrames) }}>
        <text x={140} y={20} fontSize={12} textAnchor="middle" fill={t.accent} fontFamily={fontD} fontWeight={700} opacity={prog(frame, 0, 14)}>
          VECTOR TOP-K
        </text>
        <text x={440} y={20} fontSize={12} textAnchor="middle" fill={t.accent} fontFamily={fontD} fontWeight={700} opacity={prog(frame, 118, 132)}>
          GRAPH TRAVERSAL
        </text>
        <g transform="translate(10 26)">
          <Panel t={t} frame={frame} kind="vector" />
        </g>
        <g transform="translate(310 26)">
          <Panel t={t} frame={frame} kind="graph" />
        </g>
        <line x1={290} y1={30} x2={290} y2={240} stroke={t.line} strokeWidth={1} opacity={prog(frame, 6, 20)} />
      </svg>
    </AbsoluteFill>
  );
};
