# V4 D16 independent no-weakening review — FAIL

## Verdict

**FAIL. Not merge approval; the known targeted failure remains unresolved.**

The candidate is test-only and the diff is small, but it does not preserve the
original test's semantic coverage. The preserved targeted run also fails on the
required exact path assertion.

## First-return findings

1. **The baseline/declaration was changed, weakening the protected scenario.**
   At the actual base, the original test starts from the fixture's legacy
   `parent/clips/id:card/app/astrid/on` declaration with no persisted
   `word_anchors`, captures the authored selection locally with `pick`, accepts
   the source-window edit at the current head, and then replays the captured
   selection against the original base. That is the stale-intervening-window
   behavior under test, including the `conflict` classification.

   The candidate instead accepts the selected authored anchor first, creating a
   durable `word_anchors.on`, and then submits the window edit at that new head.
   It therefore tests the earlier direct invalidation of an already-bound
   anchor, not stale replay of the unbound legacy seed. The added assertions for
   the selected word and source facts do not restore the lost legacy baseline or
   stale-base request. D16's earlier-refusal allowance does not authorize
   replacing that protected baseline.

   Minimal first return: restore the original setup and captured-command/base
   request, retain the original no-write/head assertions, and add only the
   required structured-path assertion for that original legacy case. Do not
   add a fixture, waive the path, or change the expected refusal to make the
   failed run pass.

2. **The path assertion is for the replacement scenario, not the original one.**
   `parent/clips/id:card/app/astrid/word_anchors/on` is the path of the newly
   authored bound reference. For the original legacy declaration, the required
   document path is
   `parent/clips/id:card/app/astrid/on`; the candidate's copied bound-anchor
   path cannot establish that original reference path.

3. **The real provider has a structured-path gap, confirmed independently.**
   The preserved first trace returns `reason=invalid_anchor`,
   `status=invalid`, and `path=[]`. The correct origin is:

   - `astrid/sdk/timeline/_timing_evaluators.py:564-598`,
     `_bound_words`, raises `TimingCompileError` for the excluded word at line
     598;
   - `astrid/sdk/timeline/native_word_anchor.py:378-381`,
     `compile_recorded`, catches it and raises `CommandError(...,
     kind='invalid_anchor')` without a `ref` or `path`;
   - `astrid/sdk/timeline/commit.py:1161-1174` propagates the empty
     `CommandError.path`; `_commit_errors.py:74-80` serializes it as `[]`.

   This is a production/provider owner handback, not a reason to weaken the
   test or route around the empty path.

## Evidence

- Candidate: `2f332a036db66aaaf16dc8262254809bc597b0d4`.
- Actual base: `3e4261e9694c7bd7c1b5fada9bf01d91007bcc80`.
- Diff: one test file, 9 insertions and 5 deletions.
- Preserved first targeted log: **FAIL — 1 failed, 53 deselected in 1.53s**;
  failure is the exact path assertion, with actual `[]`.
- `ruff check --no-cache tests/editing_conformance/test_native_word_anchor.py`:
  **PASS**.
- `git diff --check 3e4261e9694c7bd7c1b5fada9bf01d91007bcc80..2f332a036db66aaaf16dc8262254809bc597b0d4`:
  **PASS**.
- Typecheck: **N/A**, expectation-only test adaptation.
- No targeted behavior rerun was performed; the preserved first failure was
  reused as required. No full/native14/browser/heavy suite was run.

## Delivery behavior change

Source-window edits that would orphan an already-authored word anchor are
refused at edit time as `invalid_anchor`/`invalid`, with no head write. This
review does not claim that behavior is qualified because the exact structured
path is currently missing and the adaptation replaced the original stale
legacy scenario.

## Scope and next steps

No product, test, fixture, recipe, generated, pin, package, assertion, or
deletion changes were made by this review. The Agent provider owner should add
the correct legacy-field path at the actual error origin, then the manager
should return the test adaptation with the original legacy/stale-replay
baseline restored and run one fresh targeted check.
