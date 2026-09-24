#!/usr/bin/env python3
"""Lab 5 helpers: build the judge prompt, parse the judge's reply, compare with humans.

  judge.py system                          the judge's system prompt
  judge.py prompt SAMPLE.txt               the user prompt for one sample (rubric + diff + message)
  judge.py parse CLAUDE_OUTPUT.json        scores from `claude -p --output-format json` (exit 1 if unusable)
  judge.py compare RESULTS_DIR [--human CSV] [--authors JSON] [--sample]
                                           agreement, bias and the self-preference check;
                                           writes summary.md and export.json in RESULTS_DIR

Standard library only. The rubric is lab5/rubric.md; the diff is lab5/change.diff.
"""
import argparse
import csv
import itertools
import json
import math
import re
import statistics
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import labkit  # noqa: E402

LAB5 = labkit.LAB_DIR / "lab5"
CRITERIA = ("accuracy", "why", "scope", "format", "overall")

SYSTEM = ("You are a strict, consistent grader of git commit messages. You score one message at a "
          "time against the rubric you are given. You do not know who wrote the message. "
          "Reply with one JSON object and nothing else.")


def build_prompt(sample_path):
    rubric = (LAB5 / "rubric.md").read_text(encoding="utf-8")
    diff = (LAB5 / "change.diff").read_text(encoding="utf-8")
    message = Path(sample_path).read_text(encoding="utf-8").strip()
    keys = ", ".join(f'"{c}": <1-5>' for c in CRITERIA)
    return (f"# Rubric\n\n{rubric.strip()}\n\n# The change (unified diff)\n\n```diff\n{diff.strip()}\n```\n\n"
            f"# The commit message to grade\n\n```text\n{message}\n```\n\n"
            f"Score the commit message against the rubric. Integers only. Reply with exactly this JSON "
            f'shape and nothing else: {{{keys}, "reason": "<one sentence>"}}')


def extract_scores(text):
    """Find the JSON object with the scores in the judge's reply (tolerates code fences and prose)."""
    candidates = re.findall(r"\{[^{}]*\}", text or "", re.S)
    for chunk in candidates:
        try:
            data = json.loads(chunk)
        except ValueError:
            continue
        if not isinstance(data, dict) or "overall" not in data:
            continue
        scores = {}
        for key in CRITERIA:
            value = data.get(key)
            if isinstance(value, str) and value.strip().isdigit():
                value = int(value.strip())
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                break
            scores[key] = value
        else:
            scores["reason"] = str(data.get("reason", ""))[:300]
            return scores
    return None


def parse_output(path):
    raw = labkit.load_json(path)
    if raw is None:  # stream-json or junk: take the last result event
        raw = labkit.result_event(labkit.load_events(path))
    if not isinstance(raw, dict) or not raw:
        return None, {}
    text = raw.get("result")
    structured = raw.get("structured_output")
    scores = extract_scores(json.dumps(structured)) if isinstance(structured, dict) else None
    scores = scores or extract_scores(text)
    tokens = labkit.usage_totals(raw)
    meta = {"turns": int(raw.get("num_turns") or 0), "cost_usd": float(raw.get("total_cost_usd") or 0.0),
            "duration_s": round((raw.get("duration_ms") or 0) / 1000, 1),
            "model": next(iter(raw.get("modelUsage") or {}), None), **tokens}
    return scores, meta


def read_human(csv_path):
    scores = {}
    path = Path(csv_path)
    if not path.is_file():
        return scores
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            sample = (row.get("sample") or "").strip()
            value = (row.get("overall") or "").strip()
            if sample and value.isdigit() and 1 <= int(value) <= 5:
                scores[sample] = {k: int(row[k]) for k in CRITERIA if (row.get(k) or "").strip().isdigit()}
    return scores


def read_authors(path):
    data = labkit.load_json(path, {}) or {}
    items = data.get("samples", data) if isinstance(data, dict) else data
    return {item["id"]: item.get("author") for item in items if isinstance(item, dict) and "id" in item}


def ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return out


def pearson(x, y):
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return None
    mx, my = statistics.mean(x), statistics.mean(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    return num / den if den else None


def spearman(x, y):
    return pearson(ranks(x), ranks(y))


def fisher_ci(r, n):
    if r is None or n < 4 or abs(r) >= 1:
        return (None, None)
    z = math.atanh(r)
    half = 1.96 / math.sqrt(n - 3)
    return (round(math.tanh(z - half), 2), round(math.tanh(z + half), 2))


def self_preference(pairs):
    """pairs: [(author, human, judge)]. Gap = judge - human; returns gaps and a permutation p-value."""
    gaps = {"model": [j - h for a, h, j in pairs if a == "model"],
            "human": [j - h for a, h, j in pairs if a == "human"]}
    if not gaps["model"] or not gaps["human"]:
        return None
    observed = statistics.mean(gaps["model"]) - statistics.mean(gaps["human"])
    all_gaps = [j - h for _, h, j in pairs]
    k = len(gaps["model"])
    extreme = total = 0
    for chosen in itertools.combinations(range(len(all_gaps)), k):
        rest = [g for i, g in enumerate(all_gaps) if i not in chosen]
        diff = statistics.mean(all_gaps[i] for i in chosen) - statistics.mean(rest)
        total += 1
        extreme += abs(diff) >= abs(observed) - 1e-9
    return {"gap_model": round(statistics.mean(gaps["model"]), 2),
            "gap_human": round(statistics.mean(gaps["human"]), 2),
            "difference": round(observed, 2), "p_value": round(extreme / total, 3), "splits": total}


def compare(results_dir, human_csv, authors_json, sample=False):
    results_dir = Path(results_dir)
    human = read_human(human_csv)
    authors = read_authors(authors_json)
    pair = labkit.pair_id()
    judges = {}  # model alias -> sample -> scores
    runs = []
    for parsed in sorted(results_dir.glob("judge/*/*.json")):
        if parsed.name.endswith(".raw.json"):
            continue
        data = labkit.load_json(parsed, {}) or {}
        alias = parsed.parent.name
        sid = parsed.stem
        if data.get("scores"):
            judges.setdefault(alias, {})[sid] = data["scores"]
        meta = data.get("meta") or {}
        runs.append({"v": 1, "pair": pair, "lab": "lab5", "variant": alias, "task": sid, "run": 1,
                     "passed": None, "turns": meta.get("turns", 0),
                     "input_tokens": meta.get("input_tokens", 0), "output_tokens": meta.get("output_tokens", 0),
                     "cache_read_tokens": meta.get("cache_read_tokens", 0),
                     "cache_write_tokens": meta.get("cache_write_tokens", 0),
                     "cost_usd": round(meta.get("cost_usd", 0.0), 6), "duration_s": meta.get("duration_s", 0.0),
                     "model": meta.get("model") or data.get("model") or alias})
    md = ["# Lab 5 · judge model vs your scores", ""]
    if sample:
        md += ["**SYNTHETIC judge scores (sample-results/), not a real judge run.**", ""]
    export = [] if sample else list(runs)
    if not human:
        md += [f"No hand scores found in {human_csv}. Fill in the `overall` column (1-5) first; "
               "the judge's scores are below either way.", ""]
    for index, (alias, scores) in enumerate(sorted(judges.items())):
        rows, pairs = [], []
        for sid in sorted(scores, key=lambda s: int(re.sub(r"\D", "", s) or 0)):
            j = scores[sid]["overall"]
            h = human.get(sid, {}).get("overall")
            author = authors.get(sid, "?")
            rows.append([sid, author, h if h is not None else "-", j,
                         (f"{j - h:+d}" if h is not None else "-"),
                         " ".join(f"{c[:3]}{scores[sid][c]}" for c in CRITERIA[:-1]),
                         scores[sid].get("reason", "")[:70].replace("|", "/")])
            if h is not None:
                pairs.append((author, h, j))
                if index == 0 and author in ("human", "model"):
                    export.append({"v": 1, "pair": pair, "lab": "lab5", "kind": "judge", "sample": sid,
                                   "human": h, "judge": j, "author": author})
        md += [f"## Judge: {alias}", "",
               labkit.md_table(["Sample", "Author", "You", "Judge", "Judge - you", "Judge per criterion", "Judge's reason"], rows), ""]
        if len(pairs) >= 3:
            hs, js = [p[1] for p in pairs], [p[2] for p in pairs]
            exact = sum(h == j for h, j in zip(hs, js))
            within = sum(abs(h - j) <= 1 for h, j in zip(hs, js))
            rho = spearman(hs, js)
            lo, hi = fisher_ci(rho, len(pairs))
            bias = statistics.mean(j - h for h, j in zip(hs, js))
            md += [f"- Exact agreement: {exact}/{len(pairs)}; within one point: {within}/{len(pairs)}",
                   f"- Spearman rank correlation: {rho:.2f}" if rho is not None else "- Spearman: n/a (no variation)",
                   (f"  - rough 95% CI (Fisher z, n={len(pairs)}): {lo} to {hi}" if lo is not None else ""),
                   f"- Mean bias (judge - you): {bias:+.2f} points", ""]
            sp = self_preference(pairs)
            if sp:
                md += ["### Self-preference check", "",
                       f"- Judge minus you, on model-written samples: {sp['gap_model']:+.2f}",
                       f"- Judge minus you, on human-written samples: {sp['gap_human']:+.2f}",
                       f"- Difference: {sp['difference']:+.2f} points (positive = the judge likes model-written text more than you do)",
                       f"- Permutation test over all {sp['splits']} ways to split the samples into two groups: "
                       f"p = {sp['p_value']}", ""]
    md += ["## What 8 samples can and cannot show", "",
           "- Can: the workflow (rubric, blind hand scores, judge, compare), gross disagreements worth reading,",
           "  and the direction of a bias to investigate with more data.",
           "- Cannot: establish agreement or self-preference. With 4 samples per group the smallest possible",
           "  permutation p-value is 2/70 ≈ 0.03 (two-sided), a Spearman of 0.7 on 8 samples has a 95% CI of",
           "  roughly -0.01 to 0.94, and one pair is one rater. Quality and authorship are confounded unless the",
           "  samples were balanced (see lab5/authors.json).",
           "- The board pools ~10 pairs: that adds raters (how much humans agree with each other and with the",
           "  judge), not samples. Self-preference needs many samples per author, ideally from several model",
           "  families and several judges.",
           "- Check lab5/authors.json: unless your facilitator replaced them, the 'human' samples are stand-ins",
           "  written by Claude in a human style, which makes this a demo of the method, not evidence."]
    text = "\n".join(md)
    (results_dir / "summary.md").write_text(text + "\n", encoding="utf-8")
    (results_dir / "export.json").write_text(
        "[\n" + ",\n".join(labkit.compact(r) for r in export) + "\n]\n", encoding="utf-8")
    for record in export:
        problems = labkit.validate(record)
        if problems:
            print(f"warning: export record does not validate: {problems}", file=sys.stderr)
    print(text)
    return 0


def main(argv):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("system")
    sub.add_parser("prompt").add_argument("sample")
    sub.add_parser("parse").add_argument("output")
    p = sub.add_parser("compare")
    p.add_argument("results_dir")
    p.add_argument("--human", default=str(LAB5 / "my-scores.csv"))
    p.add_argument("--authors", default=str(LAB5 / "authors.json"))
    p.add_argument("--sample", action="store_true")
    args = parser.parse_args(argv[1:])
    if args.command == "system":
        print(SYSTEM)
    elif args.command == "prompt":
        print(build_prompt(args.sample))
    elif args.command == "parse":
        scores, meta = parse_output(args.output)
        print(json.dumps({"scores": scores, "meta": meta}, ensure_ascii=False))
        return 0 if scores else 1
    elif args.command == "compare":
        return compare(args.results_dir, args.human, args.authors, args.sample)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
