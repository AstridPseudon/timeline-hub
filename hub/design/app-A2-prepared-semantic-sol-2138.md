Implemented the bounded A2 image-add path. The real shot controls now route new prepared images through persisted `clip.add-media` with unchanged Runtime `args.media`. Missing selection produces an actionable refusal and zero POSTs. Canonical adoption, exact retry, conflict rollback, and dependent trim retention are covered.

Five permitted files changed; old tests and journey bodies remain intact. Commit message and `DONE` written.

Final verification passed:

```bash
TMPDIR=/tmp/w-98a4eb2eac NODE_OPTIONS=--require=/tmp/w-98a4eb2eac/vitest-dirname.cjs node node_modules/vitest/vitest.mjs run --config /tmp/w-98a4eb2eac/vitest-runner.config.mjs --configLoader=runner --no-cache \
src/tools/video-editor/hooks/useTimelineSave.test.tsx \
src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
src/tools/video-editor/hooks/useTimelineCommit.test.tsx \
src/tools/video-editor/commands/localSaveSession.test.ts \
src/tools/video-editor/commands/localSaveSession.v2.test.ts \
src/tools/travel-between-images/components/ShotTimelineMediaControls.test.tsx \
src/tools/video-editor/contexts/VideoEditorProvider.test.tsx \
src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx \
src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx
```

**9 files, 204 tests passed.** The temporary runner imports the repository config and sets a private cache directory; its preload supplies `__dirname`.

```bash
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 bash -c 'for config in tsconfig.app.json tsconfig.node.json tsconfig.json; do node node_modules/typescript/bin/tsc -p "$config" --noEmit || exit; done'
```

**App, Node, root: passed.**

```bash
node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineCommandsService.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0
git diff --check
git diff --name-only
```

**Passed; scope confirmed.**

Scope decision: image adds only. Python requires `row.hold`; the current video preview emits `from`/`to` without it. Video, swap/replacement, ripple, new-track, removal, group, and child-ownership recipes remain unsupported and retain drafts.

No live Runtime/Python acceptance was verified. Tests use synthetic selection and transport fixtures; no request packet was exported or byte-qualified. The immutable `33934817…` packet is unchanged. Next: independent review, then a new Agent witness using authentic Runtime selection/verified-media inputs.

Process deviation: earlier default-loader test runs created and automatically removed config bundles in shared `node_modules/.vite-temp`. It is empty; final runner-loader verification left its timestamp unchanged. Orchestrator should assess qualification impact.