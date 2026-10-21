# AP2-M2 parent final acceptance custody review

## Verdict

**APPROVE** exact candidate `6c3d53a281ea326fe274a9d082f5a1e7a3489300`, tree
`0b8cfa7981eb357cf66347daf5042337079247fb`, atop `ae6347d4b987e4c00cf35b80b74c70ba783f2487`.

This review read the complete composed row-local packet once: the parent
consumer join plus the file-drop settlement repair. No production files were
edited in this review.

## Data-safety acceptance

- Prepared native video with missing media selection or missing native command
  carrier returns `false` before any local placement `applyEdit`.
- Native refusal (`{ ok: false }`) preserves its bounded refusal text and does
  not fall back to a local snapshot placement. Native placement and removal
  intent are forwarded unchanged: `forceNewTrack`, `insertAtTop`, and
  `removeClipId`.
- Native rejection propagates through the awaited file placement promise; the
  file-drop catch removes only the temporary skeleton and decrements
  `pendingOpsRef`, then the caller receives refusal and does not seek.
- `handleFileDrop` now collects each image/video/generic placement promise and
  awaits `Promise.all`. Immediate unsupported and oversized refusals create no
  skeleton or pending operation and return no acceptance. Partial acceptance
  remains accepted when any file succeeds; concurrent upload start and cleanup
  remain intact.
- `dispatchTimelineDrop` awaits `handleFileDrop`, and `onTimelineDrop` awaits
  dispatch before invoking `onSeekToTime`. Refused file drops therefore do not
  seek.
- Existing multi-generation, single-generation, and general-asset helper
  propagation remains awaited and false/rejection-aware. No DTO, store, API,
  provider authority, or HOME source was changed.

The expected local `applyEdit` seen on file refusal is skeleton removal only;
there is no local placement fallback. The native refusal tests assert that the
placement path itself never calls `applyEdit`.

## Changed exports and actual live callers

- `handleFileDrop` (`external-drop-utils.ts:275`) is consumed at runtime only
  by `dispatchTimelineDrop` (`useExternalDrop.ts:115`), which is used by the
  mounted `useExternalDrop` hook in `useTimelineState.ts:968`.
- `useExternalDrop` (`useExternalDrop.ts:482`) is mounted by
  `useTimelineState.ts:968`; the `useTimelineState.types.ts` and command
  service references are type/registration consumers, not additional drop
  dispatchers.
- `useAssetManagement` and its changed `UseAssetManagementArgs` /
  `UseAssetManagementResult` contracts are wired by
  `runtime/installedTimelineHostServiceHooks.ts` and
  `runtime/timelineHostServiceHooks.ts`, then invoked through
  `useTimelineState.ts:936`. Its result types are consumed by the external
  drop utility/hook and `usePinnedShotGroups.ts`.

## Current HOME construction handoff

The existing inactive proposal remains the minimal shared construction:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-current-repaired-consumer-join-shared-proposal.patch`

It uses the existing `createTimelineCommands` carrier and provider-bound
`getProjectVerifiedMedia` at the existing `useTimelineState` construction
point. Read-only `git apply --check --whitespace=error` passed against both
this worktree and current HOME `/home/user/work/app`. It is not applied by this
review; HOME should apply it only through the manager's combined approval.

## Checks

Passed:

```text
node --import 'data:text/javascript,globalThis.__dirname=process.cwd()+"/config/testing"' node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/lib/timeline-asset-plans.test.ts
  4 files, 45 tests passed
./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useExternalDrop.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/lib/external-drop-utils.ts
  passed
./node_modules/.bin/tsc --noEmit --pretty false
  passed
git diff --check ae6347d4b987e4c00cf35b80b74c70ba783f2487 HEAD
  passed
bash -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh
  passed
git -C /home/user/work/app apply --check --whitespace=error <shared proposal>
  passed
```

Not run: browser, localhost, live socket, request-test, full suite, or gate
source-pin work, per task scope.

