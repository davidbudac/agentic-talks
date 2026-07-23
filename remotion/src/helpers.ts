import { Easing, interpolate } from "remotion";

// The decks' --ease: cubic-bezier(.16,1,.3,1)
export const ease = Easing.bezier(0.16, 1, 0.3, 1);

// 0→1 progress between two frames with the deck easing, clamped.
export const prog = (frame: number, from: number, to: number): number =>
  interpolate(frame, [from, to], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

// Fade the whole scene out at the end so the loop restart is soft.
export const loopFade = (frame: number, duration: number, tail = 14): number =>
  interpolate(frame, [duration - tail, duration], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

// One-shot pulse: rises 0→1→0 across [from, to].
export const pulse = (frame: number, from: number, to: number): number => {
  const mid = (from + to) / 2;
  return interpolate(frame, [from, mid, to], [0, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.quad),
  });
};

// Point on a cubic bezier segment.
export const cubicAt = (
  t: number,
  p0: [number, number],
  p1: [number, number],
  p2: [number, number],
  p3: [number, number],
): [number, number] => {
  const u = 1 - t;
  const x =
    u * u * u * p0[0] +
    3 * u * u * t * p1[0] +
    3 * u * t * t * p2[0] +
    t * t * t * p3[0];
  const y =
    u * u * u * p0[1] +
    3 * u * u * t * p1[1] +
    3 * u * t * t * p2[1] +
    t * t * t * p3[1];
  return [x, y];
};
