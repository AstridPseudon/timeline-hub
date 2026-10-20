# App parent split production-ingress follow-up review

## Verdict

**HOLD** for the exact staged source SHA `1a2ca700d761e3b4d6595f5b2415841db2f7762e`, reviewed against `d1111fd3b05acac5c72f656cd62faae5e60466be`.

The stage is otherwise bounded and structurally sound: 9 files, `+324/-34` total; `+108/-30` product (`+78` net); `+216/-4` tests. No product files were changed by this review.

## Blocking line-level counterexample

`src/tools/video-editor/commands/commitSession.ts:329-332` supplies only `bundle.parent.clips` to `supportsParentClipSplit`. `src/tools/video-editor/commands/clipSplitGesture.ts:17-46` checks the selected raw rows, registry media, timing, relations, and neighbor transitions, but never checks that the authored `parent.clips` and `parent.config.clips` mirrors agree.

The native primitive rejects this shape in the unchanged `clipSplitCapture.ts:60-63` collection-owner check. The following read-only probe against the reviewed SHA produced:

```text
{"eligible":true,"nativeCaptureError":"divergent parent clip mirrors","legacyWriterNextId":"clip-a-1792491379560","legacyClipCount":3}
```

The probe changed only the non-target config mirror row (`clip-b.at = 99`). Thus the old `splitClipAtPlayhead` writer remains a positive 3-clip operation, but `useClipSplitting.ts:30-38` takes the new native branch, catches the native refusal, and never reaches its established writer at lines 39-41. This violates the stage's conservative-eligibility comment and the requirement that unsupported positive paths remain on their old writer. The exact fix should make the eligibility predicate reject divergent mirrors (or share the native collection-owner check); it must not add fallback after native capture failure.

## What passed / what is supported

- Independent targeted Vitest replay from an isolated source snapshot: **19 files, 725/725 tests passed**, with `--configLoader=runner --no-cache --maxWorkers=1` and the shared dependency tree left read-only.
- The tested selected, context-time, and single-clip playhead paths reach one capture/finish/submit; SDK routing uses the same session; exact retry/reload recovery retains the reserved ID and request bytes.
- Native split goldens and source-window/speed/frame behavior remain unchanged from the approved source primitive. The implementation uses the existing `canSplitClipAtTime` helper and the native `from`/`speed` calculation.
- Group, multi-clip, occurrence, text/animation/relation/transition, opaque `app.canonical`, and absent-port controls preserve their established routing in the reviewed tests. No display-ID inference, second queue/compiler/session, or global ID journal was added.
- Capture/finish/submit exceptions are caught visibly and do not call the snapshot writer; the staged tests prove the clean-save refusal retains the draft. The specific divergent-mirror probe also shows the native failure path is refusal-only, not fallback.

## Exact verification

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split-production-ingress-stage/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipSplitCapture.test.ts src/tools/video-editor/commands/clipSplitGesture.test.ts src/tools/video-editor/commands/commitSession.split.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts src/tools/video-editor/commands/authoringBundle.sharedOpaqueRemap.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/lib/keyboard-delete.test.ts src/integrations/runtime/opaqueRootWriters.test.tsx src/tools/video-editor/lib/timeline-patch.test.ts
# exit 0; 19 files, 725 passed

git diff --check d1111fd3b05acac5c72f656cd62faae5e60466be 1a2ca700d761e3b4d6595f5b2415841db2f7762e
# exit 0
```

The eligibility/native/legacy counterexample was run from a temporary archive of the reviewed SHA with `node --import tsx`; it exited 0 and emitted the JSON above. The temporary archive was removed. The assigned review worktree is clean.

## Activation limits and future-main note

Until the guard correction is qualified, do not activate this ingress stage or claim writer retirement. Continue retaining the established group, multi, occurrence, unsupported, and compound writers. Actual Runtime/Agent acceptance, browser gestures/reload, zero legacy HTTP observation, full suite, build, project typecheck, install, and live socket behavior remain unverified by this review.

Future main `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa` does not contain the source session files; the target is an add/modify delta relative to that main. Compose it only after a narrow rebase that preserves main's newer infrastructure and rerun the targeted guards. No KEEP marker was created.
