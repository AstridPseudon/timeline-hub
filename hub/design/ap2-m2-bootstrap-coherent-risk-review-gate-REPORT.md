# AP2-M2 bootstrap coherent-risk review gate

## Verdict

**HOLD — no central browser gate was submitted.** The committed donor tree is
not a clean candidate against the latest App HOME. Its bootstrap patch is
reviewable and its focused assertions pass, but the branch is rooted at
`480db7febe624fe4658a75cbdb66ed5de84c2c61` while current `hub/tl/integration`
is `157eef8cf1151db09310153c10856d45d8590c87`. The donor therefore carries
unrelated older App behavior into the tree that a central gate would test.

## Blocking finding

Relative to current HOME, donor `35c5ed018c1983acb522a0e7333de18a271638ea`
(`tree 36c6c7778064b8decd5b41c44d254da96fbf57d3`) reverts current settings
authority work in these out-of-scope paths:

- `src/tools/travel-between-images/components/ShotEditor/**`
- `src/tools/travel-between-images/pages/ShotEditorView.tsx`
- `src/tools/video-editor/commands/shotSetGesture.ts`
- `src/tools/video-editor/commands/shotSetSession.test.ts`
- `tests/e2e/local/shot-name-command.spec.ts`
- `tests/e2e/local/support/harness.ts`

The concrete regression is visible in `ShotEditorView.tsx`: the donor removes
the current captured `shot.set` settings authority and draft-preserving refusal
and restores direct `SettingsAutoDisable` persistence. Current HOME's
`6d298ee02` → `d22c048f4` lineage deliberately routes canonical scalar
settings through native authority and refuses the fallback. This is not part
of bootstrap and cannot be qualified in a mixed stale tree.

Minimal correction: replay only the donor's bootstrap delta onto current
`hub/tl/integration`, preserving HOME's unrelated paths (or otherwise produce
a committed donor whose parent is `157eef8cf`). Re-run the focused 128-test
lane plus scope/lint/types/list checks, then perform a fresh independent review
before the single central bootstrap gate. No source correction was made here.

## Review and evidence

- Read the settled plan, `ap2-m2-bootstrap-scope-gate-repair-REPORT.md`, the
  approved bootstrap port report, and the outbox lifecycle fixture report.
- Reviewed create reservation/retention/cancellation, exact project/timeline
  route checks, pending owner state before create/init ACK, drain after ACK,
  native init capture, opaque/pristine controls, exact retry identity,
  restart/reload recovery, guarded inverse, and zero legacy traffic assertions.
- Donor-only focused Vitest run: **4 files, 128 tests passed**.
- Donor-only `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts`:
  **1 passed**.
- Donor-only Playwright collection of
  `tests/e2e/local/three-products.spec.ts`: **12 tests listed**, including
  exactly one bootstrap title at line 1315.
- `git diff --check hub/tl/integration tl/ap2-m2-bootstrap-scope-gate-repair`:
  **passed**.

No local browser/driver/socket/full/adoption run and no central request was
made. The stale-tree finding is the reason for HOLD, not a product-test
failure.
