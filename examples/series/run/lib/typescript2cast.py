#!/usr/bin/env python3
"""Convert a BSD/macOS `script -r` recording into an asciicast v2 file.

  typescript2cast.py IN.typescript OUT.cast [--cols 120 --rows 34]

`script -r` writes records of: uint64 length, uint64 seconds, uint32
microseconds, uint32 direction ('s' start, 'o' output, 'i' input, 'e' end),
then `length` bytes. Only output records go into the cast. The result plays in
asciinema and renders to GIF with agg (https://github.com/asciinema/agg).
"""
import argparse
import json
import struct
import sys

HEADER = struct.Struct("<QQII")


def records(data: bytes):
    offset = 0
    while offset + HEADER.size <= len(data):
        length, seconds, micros, direction = HEADER.unpack_from(data, offset)
        offset += HEADER.size
        payload = data[offset:offset + length]
        offset += length
        yield seconds + micros / 1e6, chr(direction & 0xFF), payload


def convert(src: str, dst: str, cols: int, rows: int) -> int:
    data = open(src, "rb").read()
    events = list(records(data))
    if not events:
        raise SystemExit(f"{src}: no records (was it recorded with script -r?)")
    start = events[0][0]
    count = 0
    with open(dst, "w", encoding="utf-8") as out:
        out.write(json.dumps({"version": 2, "width": cols, "height": rows, "timestamp": int(start),
                              "env": {"TERM": "xterm-256color"}}) + "\n")
        for stamp, direction, payload in events:
            if direction != "o" or not payload:
                continue
            out.write(json.dumps([round(stamp - start, 6), "o", payload.decode("utf-8", "replace")]) + "\n")
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("src")
    parser.add_argument("dst")
    parser.add_argument("--cols", type=int, default=120)
    parser.add_argument("--rows", type=int, default=34)
    args = parser.parse_args()
    count = convert(args.src, args.dst, args.cols, args.rows)
    print(f"wrote {args.dst} ({count} output events)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
