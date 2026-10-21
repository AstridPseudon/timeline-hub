# After-anchor refusal conversion review

Decision: **APPROVE the exact test correction only.** Approved commit
`72cd82ae1e6ad11fd8de3f08beee85154a0af589`, tree
`7742222511ed705b5dddcb46c2b578700774ac9f`. This is a test-only child of the
independently reviewed recorder repair `0fa122179fdd15ba18f6c37346308049edb52cd5`.
It is not approval to activate the dormant App path or to claim missing/null
hold compatibility.

## Exact ledger mapping

- The two former `it.fails.each(['missing', 'null'])` cases are converted
  one-for-one by the same `it.each` values.
- Each missing/null case now asserts the exact App refusal
  `clip.hold must be a finite positive number` and deep equality with the
  pre-capture bundle, proving atomic refusal.
- Each case creates an equivalent fresh positive-hold (`hold: 4`) fixture with
  the same `from: 2`, `to: 6`, and incoming transition, then asserts successful
  capture/finish and preservation of the window and transition.
- The delta has exactly one modified path:
  `src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts`.
  There are no remaining `it.fails`/`test.fails` markers in that test.
- The prior positive, strict record/selection/binding/write/created-ID checks,
  zero-hold refusal, sub-0.05 floor, at_ms refusal, and explicit-null behavior
  are unchanged. No assertion was skipped, weakened, or deleted, and no new
  failure marker was introduced.

The independent recorder0354 verdict remains in force: frozen Agent
`3b3208c43903b770010de0649691cfa566447822` has a positive numeric `hold`
requirement before raw-window derivation; the recorder repair matched four
complete records/replays and six refusals. Main-compatible missing/null-hold
acceptance is therefore still explicitly **OPEN**, and the helper remains
dormant. No App normalization, new wire field, activation, pin, or gate
closure is claimed.

## Verification

Direct candidate test, run from a private archive of the exact approved commit
with the shared `node_modules` installation read-only and `--no-cache`:

```sh
TMPDIR=/tmp/ap2-m2-afteranchor-refusal-conversion-review-0407.V2ADt4/tmp \
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts
```

Result: **1 file passed, 8 tests passed**.

Additional review checks:

```sh
git diff --name-status 0fa122179fdd15ba18f6c37346308049edb52cd5 72cd82ae1
git diff --check 0fa122179fdd15ba18f6c37346308049edb52cd5 72cd82ae1
```

Result: one expected test path modified; diff check passed. The correction
worker's reported focused cohort (47 tests) and neighboring session/media
cohort (82 tests) were consumed, not rerun here. No unchanged recorder review,
build, browser, HTTP, native Door, or full suite was repeated.

## Recommendation

Merge/retain this test correction as the exact conversion. Keep the dormant
after-anchor source and the Main-compatible missing/null-hold requirement OPEN
until Agent resolves the schema/raw-window discrepancy in a separate successor.
