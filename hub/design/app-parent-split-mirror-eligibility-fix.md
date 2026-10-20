# Parent split mirror eligibility correction

Completed against reviewed base `1a2ca700d761e3b4d6595f5b2415841db2f7762e` in the assigned App worktree. No commits, merges, checkouts, pushes, integration edits or KEEP marker.

## Change and decision

Exported the existing native collection-owner validator as typed `parentClipSplitRows(parent: AuthoredBundle['parent'])`. Native capture and session preflight now call that same implementation. Preflight returns false on its collection refusal, before capture or ID allocation; the existing positive writer remains available. No second collection policy, normalization, new writer, command fields, session, protocol or upstream change.

The exact non-target counterexample (`parent.config.clips[1].at = 99` with unchanged `parent.clips`) is now in permanent selected/context-menu/keyboard/SDK tests: eligibility false, existing writer called once, three output clips, unchanged resolved neighbor, zero capture and zero native commit. Native capture still refuses this divergent input; it was not made supported.

Added 17 read-only native/helper cases covering matching/divergent/empty mirrors, missing/null/scalar collections, missing/null/array/scalar config owner, invalid rows and ambiguous identity. Missing and explicit null owners keep native's distinct behavior. Six session cases prove native capture/preflight agreement and no preflight preview, outbox intent, request or input mutation. Four mounted ingress counterexamples complete the 27 new cases. The original 725 tests remain unchanged, including goldens, opaque raw-parent metadata, grouping/multi/occurrence controls, actual capture-refusal draft retention, one reserved ID, exact retry and restart recovery. No fallback was added after capture.

## Exact diff relative to reviewed base

Five files, **+97/-8**, net **+89**. Product: two files **+7/-8**, net **-1**. Tests: three files **+90/-0**.

| File | Added | Removed |
| --- | ---: | ---: |
| commands/clipSplitCapture.ts | 3 | 3 |
| commands/commitSession.ts | 4 | 5 |
| commands/clipSplitCapture.test.ts | 34 | 0 |
| commands/commitSession.split.test.ts | 26 | 0 |
| hooks/useTimelineCommandSession.split.test.tsx | 30 | 0 |

Paths above are under `src/tools/video-editor/`.

## Exact verification commands and results

All commands ran in `/home/user/work/wt/app-m2-parent-split-mirror-eligibility-fix`. Node v22.22.0, Vitest 4.1.5, Composition 0.0.12; read-only `/tmp/app-coherent-deps12/node_modules` via only this worktree's own symlink. Runner only supplies the config directory's `__dirname`. Every Vitest command used runner loading, disabled cache and one worker. Shared dependency trees, links and caches were not modified. Original `/home/user/work/app/node_modules` symlink restored after testing.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split-mirror-eligibility-fix/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx -t 'non-target mirror diverges'
# Before product fix: exit 1, four new regression cases fail because eligible=true; 19 unselected.

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split-mirror-eligibility-fix/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipSplitCapture.test.ts src/tools/video-editor/commands/commitSession.split.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx
# Intermediate: exit 1, 113 passed / 4 failed. New routing tests reached the existing writer;
# their new neighbor assertion incorrectly expected raw at=99 instead of existing derived at=5.
# Corrected only that new assertion to compare the complete unchanged resolved neighbor.

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split-mirror-eligibility-fix/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipSplitCapture.test.ts src/tools/video-editor/commands/clipSplitGesture.test.ts src/tools/video-editor/commands/commitSession.split.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts src/tools/video-editor/commands/authoringBundle.sharedOpaqueRemap.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/lib/keyboard-delete.test.ts src/integrations/runtime/opaqueRootWriters.test.tsx src/tools/video-editor/lib/timeline-patch.test.ts
# Final: exit 0, 19 files / 752 tests passed, 51.80s. Original 725 + 27 new.

node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/clipSplitCapture.ts src/tools/video-editor/commands/clipSplitCapture.test.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.split.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx --max-warnings 0
# Exit 0, no output/warnings.

git diff --check 1a2ca700d761e3b4d6595f5b2415841db2f7762e
# Exit 0.

git diff --numstat 1a2ca700d761e3b4d6595f5b2415841db2f7762e
# Exact counts above.
```

Logs: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split-mirror-eligibility-fix/notes/{counterexample-before,focused,targeted,lint}.log`.

## Remaining activation limits and next step

No blockers in this task. Request orchestrator review of this narrow correction before activating the ingress stage. Unsupported/divergent, group, multi, occurrence and compound paths retain their established writers until their replacements qualify; no writer-retirement claim. Actual capture/finish/submit errors still retain the draft visibly and never fall back afterward.

Runtime/Agent acceptance, browser gestures/reload, live sockets, zero legacy HTTP observation, full suite, build, project typecheck and installation remain unverified and were not run, as directed. No root/upstream composition was attempted; any future-main composition still needs its own qualified integration. No build output or temporary files remain in the worktree.
