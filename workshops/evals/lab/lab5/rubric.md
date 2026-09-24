# Rubric: commit message for a code change

You are grading one git commit message written for the diff shown with it.
Read the diff first, then the message. Grade the message only, not the code.
Score each criterion from 1 to 5. The anchors below describe 1, 3 and 5; use
2 and 4 for messages in between. Judge what is written, not what the author
probably meant.

## accuracy: does it say what the diff actually does?
- **5**: Every claim matches the diff. The changes that matter to a reader are
  named (here: the new sixth column, its position after `gross`, how its value
  is chosen, and the updated tests). Nothing is invented.
- **3**: Broadly right, but vague about a change that matters, or one minor
  claim is imprecise.
- **1**: Wrong, or claims something the diff does not do (a file, a test, a
  behaviour that is not there), or so vague it could describe any change.

## why: does it explain the reason?
- **5**: States the motivation in a sentence a future maintainer can use
  (here: consumers of the export could not tell which currency an amount is in).
  Mentions the consequence for users of the output if there is one (a changed
  header).
- **3**: A reason is hinted at or implied, but not stated.
- **1**: No reason at all, or a reason that restates the what ("to add a column").

## scope: is the level of detail right?
- **5**: Concise. Says what a reviewer needs and stops. No filler, no
  restating the diff line by line, no speculation about future work.
- **3**: Somewhat padded or somewhat thin; a reader has to skim or guess.
- **1**: A wall of text, a bullet list of every line changed, or a single word.

## format: does it follow git conventions?
- **5**: Imperative subject line ("Add ..."), at most 72 characters, no trailing
  full stop; a blank line; a body wrapped at about 72 characters.
- **3**: One convention broken (past tense, long subject, no blank line,
  unwrapped body).
- **1**: Several conventions broken, or not recognisable as a commit message.

## overall: would you accept this message in review as written?
A holistic judgement, not the average of the four scores. A single false claim
can make an otherwise polished message a 2.
- **5**: Accept as is.
- **3**: Accept after a small edit.
- **1**: Ask for a rewrite.
