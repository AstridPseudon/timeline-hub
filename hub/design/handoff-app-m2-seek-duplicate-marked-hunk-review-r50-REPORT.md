# App r50 duplicate marked seek-completion review

## Verdict

**APPROVE** r49 current consumer correction.

Final source SHA: `547da1a555cfe8514bc3f40a263ee56fdafd3d83`  
Final tree: `3bc1b2614e95c1cb7d727c602c7c1bc630a1e33e`

The changed hook consumes every `seekComplete` callback before the ordinary
feedback path. When the timeline-origin latch is set, it clears that latch and
holds the preview-origin guard through the existing RAF; when the latch is
already clear, a duplicate marked callback is still consumed. The later
ordinary frame is accepted normally.

## Required ordering witness

The committed regression covers the rational-fps sequence:

```text
click A=.5, click B=1, ordinary frame15, marked frame30,
duplicate marked frame30, ordinary frame45
```

It retains authored `setCurrentTime` values A/B, asserts no duplicate `setTime`,
asserts the complete `setTime` sequence is exactly `[[45 / fps]]`, and retains
the timeline latch release assertion.

A disposable focused witness additionally placed the duplicate marked callback
after an explicit `performance.now()` jump from 1000 to 1251 (>250 ms), then
sent ordinary frame45 at 1252. It passed with exactly one `setTime(45 / fps)`
and accepted the later ordinary state update. The temporary test was deleted.

## Preservation checks

- `RemotionPreview.tsx` is byte-identical to the e1c0 producer (`aec7b278...`)
  in the final tree; the late same-frame/no-op correction was not changed.
- `TimeRuler.finalSeek.test.tsx` is byte-identical to the e1c0 current source;
  the original assertions at lines 279 and 299 remain intact and pass.
- The r49 diff is limited to `useTimelineSync.ts` and
  `useTimelineSync.test.ts` (12 production lines, 5 test lines).
- No fps/tolerance change, callback/API change, timer/store change, or
  `it.fails` marker was added. No producer, mailbox, TimeRuler, or forwarding
  hunk was edited.

## Commands and results

```text
TMPDIR=/tmp ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/hooks/useTimelineSync.test.ts src/tools/video-editor/components/TimelineEditor/TimeRuler.finalSeek.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx
PASS — 3 files, 16 tests.

TMPDIR=/tmp ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/hooks/__tmp_duplicate_marked_gate.test.ts
PASS — 1 file, 1 test; temporary witness removed afterward.

./node_modules/.bin/eslint src/tools/video-editor/hooks/useTimelineSync.ts src/tools/video-editor/hooks/useTimelineSync.test.ts --max-warnings 0
PASS.

git diff --check HEAD^ HEAD
PASS.
```

The worktree is clean. No browser, actual, full, build, install, graph, or
broad suite was run, per task scope.

## Decision / next step

No product edit was needed: the candidate fixes the distinct Viewing1025
ordering defect and preserves the existing producer and mounted guarantees.
Orchestrator may accept r49 for integration; no further correction is
recommended from this review.
