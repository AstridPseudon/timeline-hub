# App paired seek consumer review

## Verdict

**REQUEST CHANGES.** Candidate `b9a0b4c91fdedfd592d25a7ac0495969758a4d65`, tree
`a9fa172b17b89570fe034b98bf21e2d0d7ec7a01`, fails the required duplicate
marked-completion semantics. After authored B=1 receives
`[1.001,true]`, a second `[1.001,true]` falls through after the guard is
released and can rewrite authored time to 1.001 once the existing 250 ms gate
permits it. Later ordinary `[1.5015]` is accepted. The candidate direct test
does not cover this.

Activation also remains held for HOME's separate 0956 late same-frame producer
finding; producer review/edit was out of scope here. Re-review after that
correction and the consumer regression land.

## Exact identity

- Patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-app-paired-seek-new-consumer-1005.patch`
- Patch SHA-256: `d8a0032cc5f95ab7a9290913a210c6fc6d7bf36b71c1e3e52265499f80621e12`
- Consumer blobs: playback `d33f4a46d82f529011561d4ecd58043954bd856a`; sync `51e5654767cd028c67c1c61a5c7791859535436f`; direct test `3b8b1a19dadc045d1b11b8ea357666cabe64dc74`
- Unchanged producer blobs: `RemotionPreview.tsx` `df6bf5740412f92b6f00e2f81841fb3236c799c2`; mailbox test `ca5238598ccde30b5a786fc9124e40949ac69a5a`
- Producer SHA-256: `3cb8f65809bf45560dbea2971783b7b4047bc0978d43c6605f4b8a1c2e5f3a02`

## Findings

- `src/tools/video-editor/hooks/useTimelineSync.ts:22-28` suppresses a
  marked callback only while `isSyncingFromTimeline` is true. After line 25
  clears it, a duplicate marked callback enters lines 30-40 and line 36 can
  call `setCurrentTime(30/(30000/1001))`. The smallest App-owned correction
  is to consume/suppress `seekComplete` before ordinary feedback even when
  the guard is already false, while clearing the guard when set.
- `useTimelineSync.test.ts:48-62` covers A ordinary frame 15, B marked frame
  30, later ordinary frame 45, and rational fps, but lacks the duplicate true
  after release and does not assert the complete `setTime` sequence.
- Existing mounted `TimeRuler.finalSeek.test.tsx:279,299` fails on this
  candidate: both assertions expect `isSyncingFromPreview.current` true after
  a seek callback, but the producer now marks the callback completion and the
  consumer clears the timeline-origin guard without setting the
  preview-origin guard. I did not rewrite/weaken those original assertions.
- No Viewing-owned forwarding hunk is missing; no unapplied forwarding patch is
  supplied.

## Real mounted route

```
RemotionPreview.tsx:310-320
  frameupdate -> onTimeUpdateRef.current(time, true|undefined)
  -> useVideoEditorPreviewSurface.tsx:109-119 selector
  -> useVideoEditorPreviewSurface.tsx:155-169
     <RemotionPreview onTimeUpdate={onPreviewTimeUpdate}>
  -> TimelineEditorShellCore.tsx:501-504 / PreviewPanel.tsx:161,200
     owned portal into the preview slot
  -> useTimelinePlayback.ts:29-35 -> useTimelineSync.ts:22
```

This is direct prop forwarding; no wrapper drops the second argument. The
type carrier remains optional at `useTimelinePlayback.ts:13`,
`useTimelineState.types.ts:312`, and `useTimelineState.ts:622-634`.
Alternate direct users likewise pass it unchanged:
`PublicAstridEditorParts.tsx:64-72` and
`ShotTimelinePreview.tsx:157,285-289`.

## Retained assertions / limits

Final release, playing/drag, no-op, coalescence, deferred-config, same-frame,
unmount, rational-fps, and source-window producer behavior were not changed by
the consumer patch; prior producer evidence was reused, not re-reviewed.
Mounted surface identity/portal tests passed. The mounted final-seek assertions
above are not green. No full/browser/live-socket/physical/native/Runtime/helper/
original-split/install suite, broad replay, or graph copy was run.

## Commands/results

```
TMPDIR=/tmp ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/hooks/useTimelineSync.test.ts src/tools/video-editor/components/TimelineEditor/TimeRuler.finalSeek.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx
```

Result: 2 files passed, 1 failed; 14 passed, 2 failed. Failures are the
retained TimeRuler assertions at lines 279 and 299.

One temporary focused witness (created then removed):
```
TMPDIR=/tmp ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/__paired-consumer-duplicate-completion.test.ts
```
Result: 1 failed as expected; it observed a second
`setCurrentTime(1.0010000000000001)` for duplicate marked completion.

Passed:
```
./node_modules/.bin/eslint src/tools/video-editor/hooks/useTimelinePlayback.ts src/tools/video-editor/hooks/useTimelineSync.ts src/tools/video-editor/hooks/useTimelineSync.test.ts --max-warnings 0
git diff --check
git status --porcelain=v1
```

Worktree is clean. Recommended next steps: HOME qualifies the granted 0956
producer correction; App repairs marked-completion consumption and adds the
duplicate regression; resolve the two retained mounted assertions without
weakening them; rerun the three focused files.

