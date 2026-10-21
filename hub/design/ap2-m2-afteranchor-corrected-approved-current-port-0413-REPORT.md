# After-anchor corrected current port report

## Result

Ported the approved dormant after-anchor seam onto current App integration.

Changed exactly:

- `src/tools/video-editor/commands/parentAfterAnchorCapture.ts` — dormant helper.
- `src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts` — corrected refusal/positive coverage.
- `src/tools/video-editor/commands/parentClipAddCapture.ts` — minimal helper/selection/ordering/mirror seam required by the dormant helper.

The three worktree blobs match frozen approved donor `72cd82ae1e6ad11fd8de3f08beee85154a0af589` byte-for-byte. Donor tree: `7742222511ed705b5dddcb46c2b578700774ac9f`. Donor parent: approved recorder repair `0fa122179fdd15ba18f6c37346308049edb52cd5`.

The independent 0407 assertion-conversion review approved this exact correction: two former `it.fails` cases became one-to-one atomic missing/null refusals plus equivalent positive numeric-hold window/transition coverage, with the open compatibility requirement retained.

Current base and hub are identical: `5d36b0e53ff0d17ef045e226a6e6ca7584322858`. The donor is not an ancestor, so no merge-forward was performed; worker rules prohibit local merge/checkout and the branch already equals the latest observed `hub/tl/integration`.

Delta from current base: 3 files; 512 new lines in the two new dormant helper/test files, plus the donor seam's 40 insertions / 18 deletions in `parentClipAddCapture.ts`. No other product files changed.

## Contract preserved

- Four complete Agent command/record/bundle/replay parity cases, six refusals, and the sub-0.05 positive duration floor remain covered.
- Missing and null hold now refuse atomically with the exact positive-hold schema error; each has an equivalent positive numeric-hold window/transition success assertion.
- Zero hold remains refused.
- The Main-compatible missing/null-hold acceptance requirement remains explicitly open.
- No `it.fails` marker remains.
- The helper remains dormant: no live `afterClipId`, UI, Provider, session, pin, generated artifact, or activation change.
- The test explicitly asserts that the command has no `afterClipId` field.

## Verification

Passed:

```text
TMPD=$(mktemp -d "$PWD/.afteranchor-tmp.XXXXXX")
trap 'find "$TMPD" -mindepth 1 -delete; rmdir "$TMPD"' EXIT
TMPDIR="$TMPD" PARENT_AFTER_PARITY_OUTPUT="$TMPD/parity.json" ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/parentClipSwapCapture.test.ts src/tools/video-editor/commands/clipMovePrimitives.test.ts src/tools/video-editor/commands/commitSession.parentMedia.test.ts src/tools/video-editor/services/parentMediaCommands.test.ts
# 4 files, 47 tests passed

TMPDIR="$TMPD" ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/media.test.ts
# 2 files, 83 tests passed
```

Frozen Agent parity:

```text
# Vitest parentAfterAnchorCapture.test.ts: 1 file, 8 tests passed
# Python checker against frozen Agent 3b3208c43903b770010de0649691cfa566447822:
# 4 complete commands/records/bundles and deterministic replay matches,
# 6 refusals, zero-duration floor matched
```

```text
./node_modules/.bin/eslint src/tools/video-editor/commands/parentAfterAnchorCapture.ts src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.ts --max-warnings 0
# passed

./node_modules/.bin/tsc -p .afteranchor-tsconfig.json --noEmit --pretty false
# passed; temporary config removed

git diff --check
# passed
```

Repository-wide `./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false` was also attempted and failed on unrelated existing errors in Composition exports, timeline config typing, `clipScalarGesture.ts`, and other files outside this port. None referenced the three changed paths. No browser, HTTP, live socket, native Door, or full suite was run.

## Handoff

The harness must materialize the final commit SHA after committing this worktree; no commit was created in the worker because `.git` is read-only. The worktree is ready for remote merge with the exact donor delta above.

Recommended next step: have the merge queue apply this bounded three-file port onto current integration, then keep the helper dormant until Agent resolves the open Main-compatible missing/null-hold schema requirement.

