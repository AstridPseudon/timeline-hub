# AP2 M2 prepared-video row-local consumer restore

## Result

Restored the native prepared-video consumer in the App-owned
`useAssetManagement` row-local hook. A prepared video carrying the existing
Runtime `mediaSelection` now delegates to the existing `commands.addClip`
facade, preserving the native consumer's existing selection, row, session, and
verified-media fences. The hook does not call the local `prepared-media`
snapshot path for this qualified case.

Unqualified prepared media keeps its existing local behavior. A missing
`commands` carrier or a native `{ ok: false }` result returns visible refusal
(`false`) and does not call `applyEdit`; the imported catalog/registry remains
untouched. No image/audio neighbor, duplicate/group path, new-track path,
`afterClipId`, provider, schema, DTO, pin, session, or `useTimelineState` code
was changed in this worker.

## Source changes

- `src/tools/video-editor/hooks/useAssetManagement.ts`
  - accepts optional `Pick<TimelineCommands, 'addClip'>`;
  - routes only prepared video plus the existing five-field selection to
    `commands.addClip`;
  - allows the prepared-drop result to be `boolean | Promise<boolean>` so the
    native refusal is not mistaken for a successful local write.
- `src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx`
  - adds native delegation/selection identity, missing-carrier refusal, and
    verified-refusal-without-local-fallback coverage.
- `tests/e2e/local/support/run-parent-manual-drop-evidence.sh`
  - durable App-owned copy of the prior evidence-first wrapper; it retains the
    current exact three-path source pins, current App tree guard, selector, and
    bounded evidence-before-cleanup behavior. It is a gate wrapper only; no
    browser/socket/request-test/full run was made here.

The HOME shared construction is intentionally separate and un-applied here:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-prepared-consumer-shared.patch`

It adds the provider-bound `parentMediaRuntime`, constructs the existing
`parentMediaCommands`, and passes that capability to `useAssetManagement` in
`useTimelineState`. Static applicability was verified with:

```text
git -C /home/user/work/app apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-prepared-consumer-shared.patch
PASS (current HOME; no HOME files changed)
```

Handoff request: apply that exact shared construction in HOME, then rerun the
approved parent-drop source/setup preflight and the single named real gate.
Do not add a second provider/session implementation in this row-local branch.

## Evidence wrapper custody

The prior causal report established that the negative 5013 wait was caused by
the missing consumer: current `useAssetManagement` always used local
`prepared-media`, while `useTimelineState` supplied no native media command
service. Its wrapper and diagnostic records are retained under the worker
source path and the wrapper is now published under App test support.

The current checked-in custody driver has 15 executable controls. The earlier
independent inventory reported 16; no source diff proves a sixteenth current
guard, so this report preserves the discrepancy rather than inventing or
dropping a control. The durable wrapper retains the current 15-control source
and current exact tree guard.

The wrapper's syntax and evidence-first cleanup probe passed. It was not used
to launch the real browser gate.

## Verification

Passed:

```text
VITEST_CACHE_DIR="$PWD/.vitest-cache" node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts
2 files, 17 tests passed

./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts
passed

./node_modules/.bin/tsc --noEmit --pretty false
passed

sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh
passed

tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe
passed: evidence copied before disposable-root cleanup

git -C /home/user/work/app apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-prepared-consumer-shared.patch
passed against current HOME

git diff --check
passed
```

Not run: browser, localhost/live socket, central `request-test`, full suite,
or the real parent-drop gate. Those remain blocked by the required HOME shared
construction and independent seam/assertion review.
