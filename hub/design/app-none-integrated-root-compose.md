# App M2 native-None integrated-root compose

Date: 2026-10-20

## Source

- Actual integration base: `3599fc49ad76dfdd7847ab4c813fc9317a0304eb` / tree `74130f681f6b0c87a7c61cb33d4ae6a092c03046`.
- Applied only the approved cumulative delta `0bc2d8ebbc724c54745276dffa3bd25e869e7d00` / tree `81cee4ec952fede797417cbd52be1b006f7a7d99` versus `b1ef4b9b910ba72375c34cf319692f90d22edc25`.
- Worktree-composed tree, calculated with an isolated temporary index/object store: `84f1ad1a7dfdd508dd78aa4032265c83e85cc681` (uncommitted; harness commit will establish the final commit SHA).
- Frozen pair for the gate: Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a2`, Composition public12 archive SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.

The cumulative delta was applied with `git diff --binary b1ef4b9b9 0bc2d8eb | git apply --reject`; all 33 approved paths applied cleanly and no `.rej`/`.orig` files remain. The current cold-start readiness fix remains present (`initialReadReady`, verified occurrence/registry basis, and late-basis dirty-label coverage). Main17/root changes and scalar owner/project/document/source guards remain present.

## Exact deletion boundary

Only the two portless transition-None fallback writers are removed:

- `ClipTransitionSection.tsx`: missing `onScalarEditStart` no longer calls `onChange({ transition: undefined })`; it visibly refuses with `Transition clear requires an active timeline command session.`
- `BulkClipPanelBody.tsx`: missing `onScalarEditsStart` no longer calls `onChangeDeep(() => ({ transition: undefined }))`; it visibly refuses with `Bulk transition clear requires an active timeline command session.`

Native single and atomic bulk clears remain command-backed and guarded. SET/type-change, duration, reset, and parameter writers remain distinct. No new fallback was added.

## Local evidence

- Vitest targeted controls/session lane: **13 files, 238 passed, 0 failed**. Used worker-owned `private12/tmp`, `private12/cache`, `private12/preload`, `--configLoader=runner`, `--no-cache`, one worker, and no shared cache writes.
- Native transition contract: **1 passed, 0 failed** (`node --test --test-concurrency=1 tests/e2e/local/support/native-transition-clear.contract.test.mjs`).
- Targeted ESLint over all changed TypeScript/TSX/MJS source and tests: passed with no output.
- `git diff --check`: passed.
- No full suite, project TypeScript, install, framePCM, or local browser/socket run was performed.

## Central gate status

The prior old-tree proof was read before any new request. Its exact central TestID was `app-m2-none-actual-candidate-gate-e2e-native-none-81cee4ec-d8749a9e-2c4ac180-rune29e37f2-e2e-integration-1020151010-9311`; preflight/build passed, but the first single case failed before any clear commit and bulk did not run. The trace shows the displayed-basis refusal alert, `Displayed timeline does not match the raw authoring basis`, immediately before the None click. This is the known cold-start initial-basis problem addressed by the integrated root fix, not a reason to weaken the None assertions. The prior report made no qualification claim.

I did not duplicate that unchanged old-tree run. A new composed-tree browser request was not issued because the central allow-list has only the old fixed-tree `e2e-native-none-81cee4ec...` command, whose external strict runner rejects this uncommitted composed tree; no composed-tree suite entry/runner may be added from this worker under the assigned write boundary. Therefore the two actual browser cases, 40/75/77/source/peer/cache guards, short TMP, fresh build, and exact frozen pair remain **unverified on the composed tree**. Stop here rather than treating the old failure or a mismatched runner as product evidence.
