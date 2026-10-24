**P3 9310 is a predicate mismatch, not a missing POST. No source or test changes were warranted.**

- Request wait: trace time **46177.850–136190.395 ms**. Drag: **(181, 494.484375) → (341, 494.484375)**, 12 steps.
- Independently counted **one `/commit` POST**, HTTP **200**, `accepted`; total resource duration **15470.162 ms**. The two network streams are identical, not separate requests.
- The request contains one `doc.patch`, changing only `parent/clips/id:f2-app-clip/at`, **0 → 5**. It retains **25 request reads and 25 step reads**.
- Canonical reply has `at: 5`. History grows **2 → 3**, with exactly one matching accepted publication and head.
- The wait requires `clip.move`, so it misses this request. The reset-precondition validator also assumes `clip.move`.

Current P2 parent likewise has a confirmed **POST 200** before its `atomic` versus `fields` assertion. Historical no-POST findings do not describe either retained current parent path.

Source tracing confirms `useTimelineState → useTimelineSave → capture/handoff → localSaveSession → RuntimeDataProvider.commitTimeline`. The independent whole-path report’s possible lost-basis mechanism is **not demonstrated in 9310**.

Validation: **382 tests passed across 11 files**. Exact Vitest invocations used:

```bash
NODE_OPTIONS="--import=$TMPDIR/preload.cjs" /opt/node20/bin/node node_modules/vitest/vitest.mjs run --config "$TMPDIR/current.config.mjs" --configLoader runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/lib/timeline-data.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/time-grid-conformance.test.ts src/tools/video-editor/hooks/useClipDrag.test.tsx src/tools/video-editor/hooks/useTimelineCommit.test.tsx src/tools/video-editor/hooks/useTimelinePersistence.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/localSaveSession.replayProtocol.test.ts src/tools/video-editor/commands/useTimelineCommandsService.persistence.test.tsx src/tools/video-editor/hooks/useTimelineSave.test.tsx
```

**375 passed.** The commands-service selector had the wrong directory; its correct path ran separately:

```bash
NODE_OPTIONS="--import=$TMPDIR/preload.cjs" /opt/node20/bin/node node_modules/vitest/vitest.mjs run --config "$TMPDIR/current.config.mjs" --configLoader runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx
```

**7 passed.** All three `tsc --noEmit --incremental false` configurations passed serially under `/home/user/work/.app-tsc.lock`. Scoped ESLint with `--max-warnings 0` and `git diff --check` passed. Worktree remains clean.

No RED→GREEN repair claim is made. The mounted control uses controlled transport; P3’s later restart/undo sequence remains unverified. Proof should align the exact oracles with the demonstrated guarded patch path before another pair run. No browser/backend/full/build run occurred.

Task-named commit message and `DONE` created.