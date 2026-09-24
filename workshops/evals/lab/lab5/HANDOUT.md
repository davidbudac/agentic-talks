# Lab 5 · A model as the judge (30 min)

Some output has no test. Nobody can assert that a commit message is good, yet
agents write them all day. The usual answer is an LLM judge: a model scores the
output against a written rubric. Before you trust one, measure how well it
agrees with you, and whether it favours text written by models.

The artefact: eight commit messages for one change, the currency column added
to the CSV export (`lab5/change.diff`).

## 1. Read the rubric (3 min)

`lab5/rubric.md`: four criteria (`accuracy`, `why`, `scope`, `format`), each
1 to 5, plus a holistic `overall`. The judge gets exactly this text.

## 2. Score by hand first (12 min)

Read `lab5/change.diff`, then each of `lab5/samples/s1.txt` … `s8.txt`. Agree a
score as a pair and fill in `lab5/my-scores.csv` (whole numbers 1 to 5, every
cell). Do **not** open `lab5/authors.json` yet: it says which samples are
labelled human and which model, and knowing that changes how you score.

## 3. Run the judge (3 min)

```sh
./lab5.sh --dry-run      # the exact claude -p commands, nothing is called
./lab5.sh                # judge all eight, then compare with your sheet
LITE=1 ./lab5.sh         # Haiku as the judge: cheaper, and a second opinion
./lab5.sh --sample       # no model calls: synthetic judge scores, to see the output
./judge.sh lab5/samples/s3.txt   # judge a single message, JSON out
```

`judge.sh` sends the rubric, the diff and one message to `claude -p`, with no
tools, and asks for JSON scores. Each sample is judged in a separate call, so
the judge never compares samples with each other.

## 4. Read the agreement (5 min)

`lab5.sh` prints, for `overall`:

- **exact agreement**: share of samples where you and the judge gave the same score;
- **within one**: share where you differ by at most one point;
- **Spearman correlation**: do you and the judge rank the samples the same way;
- **bias**: the judge's mean score minus yours. Positive means a lenient judge.

Look at the samples with the largest disagreement and read them again. Is the
judge wrong, or were you? Did it catch the false claims in any message?

## 5. Self-preference (5 min)

Now open `lab5/authors.json`. `lab5.sh` also splits the gap (judge minus human)
by author. If the judge is more generous to model-written messages than you
are, and not to human ones, that is the pattern called self-preference: models
tend to rate text from their own model family higher.

## 6. What eight samples can and cannot show (2 min)

Be honest about the numbers:

- Eight samples, four per group, cannot establish self-preference or agreement
  statistically. A Spearman correlation of 0.7 on n = 8 has a 95 % confidence
  interval of roughly -0.01 to 0.94: consistent with almost anything.
- You are one pair of raters. The board pools about ten pairs, which adds
  raters, not samples: it tells you how much people disagree about these eight
  messages, not how the judge behaves on messages in general.
- Every sample was written by Claude while the kit was built. The "human"
  samples are stand-ins in human style unless your facilitator replaced them
  with real ones. Without real human text, a self-preference test compares
  Claude with Claude.
- Quality was spread across both groups on purpose; in real data, style and
  quality are tangled together, and a judge preferring "model" text may just
  prefer tidier text.

What the lab can show: the workflow (rubric, blind human scores, judge, compare),
gross disagreements worth a second look, and the direction of any bias to
investigate with a larger, real sample. For a real decision, score 50 to 100
outputs by hand, from several people, before you let a judge gate anything.
