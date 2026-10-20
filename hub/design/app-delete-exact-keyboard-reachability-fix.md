# App M2 exact Delete keyboard reachability fix

Status: local source fix complete; central two-case browser qualification is pending a fresh source tuple.

## Finding and fix

The focused production target is a `div[role="button"].clip-action`, not an editable input. The keyboard listener's shell containment and editable-target guards therefore accept a real Delete from that element. The first false state was selection ownership: `TimelineEditorCore` and the public `TimelineEditorCoreBody` passed no owner to `userSelectTimelineClip` from the clip's keyboard selection handler. That wrote the ambient timeline selection while the mounted editor read its `agentSelectionOwner`-scoped selection, so `selectedClipIds` was empty and `TimelineEditorShellCore` supplied `hasSelectedClip: false`; `useClipDeletion` was never reached.

Both handlers now pass `marqueeOwner`, preserving the existing owner-scoped selection contract. The regression uses the real role-button clip target and verifies owner-scoped selection. A companion keyboard test dispatches real, bubbling Delete from a focused role-button inside the shell root and verifies the listener prevents the event and calls the delete action.

## Verification

- `git diff --check` — passed.
- Focused pre-fix regression command (the original click-based fixture) — 3 files, 47 tests, 1 failed: owner-scoped selection was empty. This identified the missing owner argument.
- `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split029-source-slice/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.test.tsx src/tools/video-editor/components/TimelineEditorShellCore.test.tsx src/tools/video-editor/hooks/useKeyboardShortcuts.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts` — passed: 4 files, 172 tests.

No full suite, project typecheck, install, local browser, shared dependency, or shared cache write was performed.

## Central handoff

The registered mounted-ready wrapper is pinned to stale App commit/tree `59830d2e`/`bc7ae9f` (and corresponding cache identity), so it was not run against this uncommitted source. After the harness creates the final commit, re-run the same two-case wrapper from `app-m2-delete-mounted-ready-committed-final-gate` with both `TIMELINE_CURRENT013_APP_SHA`/`TIMELINE_CURRENT013_APP_TREE` and `TIMELINE_MAIN574_PUBLIC13_APP_SHA`/`TIMELINE_MAIN574_PUBLIC13_APP_TREE` set to that final App commit/tree, and regenerate the matching `TIMELINE_*_CACHE_ID`/`TIMELINE_TEST_RUN_ID`. Keep the existing Agent, Runtime, public13, vendor, and cache guards unchanged.
