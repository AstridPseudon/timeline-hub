# App parent-delete opaque eligibility fix

Status: complete source-only correction on `a84f1c0c890113bf93f9a5213f9f340a877fa288`.

## Change

Removed the delete-session check that interpreted `resolvedConfig.clips[*].app.canonical` as parent/occurrence ownership authority. Parent eligibility remains bounded by the authenticated session scope/head closure, exactly one known display clip binding, and the existing `captureClipDelete(bundle, 'parent/clip:<id>')` raw-parent validation. The native executor still owns the complete-row guard and all existing unsupported ownership/dependency checks.

Added a durable-session regression with authored `app.canonical = {ownerRef: 'opaque-owner', clipRef: 'literal', rawClipId: 'literal'}`. It proves the opaque value remains byte-for-byte in `parent/clip:x::`, while only `x` is deleted. The two existing synthetic projected-ID negatives now use non-exact display IDs, preserving no-suffix-parsing/no-occurrence-broadening coverage without treating authored `app.canonical` as authority.

Only these allowlisted files changed:

- `src/tools/video-editor/commands/commitSession.ts`
- `src/tools/video-editor/commands/commitSession.clipDelete.test.ts`

`useClipEditing.test.ts` is byte-identical to base, including the grouped-delete assertion at line 261.

## Verification

Focused reviewed delete cohort, using the required private runner/preload, `--configLoader=runner --no-cache --maxWorkers=1`: **17 files, 493 passed, 0 failed**. This is the reviewed 492-test cohort plus the D1 regression.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipDeleteCapture.test.ts src/tools/video-editor/commands/clipDeleteGesture.test.ts src/tools/video-editor/commands/commitSession.clipDelete.test.ts src/tools/video-editor/hooks/useTimelineOps.clipDelete.test.ts src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/lib/keyboard-delete.test.ts src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
```

Scoped ESLint passed:

```sh
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.clipDelete.test.ts
```

`git diff --check` passed. `node scripts/quality/check-known-failures.mjs` reports 3 existing authorized markers and 0 forbidden markers. No shared dependency/cache files changed.

## Decisions and limits

- Kept the existing raw closure and display head/identity checks; did not add suffix parsing, occurrence selectors, catch-and-snapshot fallback, or any native semantic change.
- The synthetic occurrence/unaddressable test inputs were corrected to exercise exact display-ID rejection, because continuing to reject arbitrary authored `app.canonical` would violate D1’s opaque-namespace requirement.
- `commitSession.ts` overlaps the separately planned Main 44f refresh; the fix is a narrow delete-block/import delta and should be reconciled explicitly rather than merged wholesale.
- Prior reviewed native parity, exact whole-row guards/after/inverse/ordering, literal/proto-key, and original grouped-delete evidence is preserved by this delta; native parity was not regenerated here.

Not run, per brief: full suite, build, browser, live socket, project typecheck, install, real Runtime/Agent pair, activation/deletion claim, reload/undo/retry/zero-legacy journey, and standalone native inverse-redo boundary. Those remain separate qualification work.

