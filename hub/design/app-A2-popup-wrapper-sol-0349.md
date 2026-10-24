Implemented the mounted popup → scoped handoff → persisted A2 outbox route. The mounted regression verifies zero legacy save/publish calls and canonical reply adoption.

A minimal context seam was required because the parent handoff rejects projected child edits. Protected files remain unchanged. Missing publication authority produces a concrete basis refusal.

Validation: **340 tests passed across 12 files** using Node 20:

```bash
PATH=/opt/node20/bin:$PATH NODE_OPTIONS=--require=/tmp/w-4643f25d90/dirname.cjs \
node node_modules/vitest/vitest.mjs run \
--config /tmp/w-4643f25d90/vitest.config.mts --configLoader=runner --no-cache --maxWorkers=1 \
src/tools/travel-between-images/components/ShotTimelinePreview.integration.test.tsx \
src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts \
src/tools/travel-between-images/components/ShotTimelinePreview.test.ts \
src/tools/travel-between-images/components/ShotTimelineMediaControls.test.tsx \
src/tools/travel-between-images/pages/LocalTimelineShotBrowser.test.tsx \
src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
src/tools/video-editor/hooks/useTimelineHistory.test.ts \
src/tools/video-editor/hooks/useTimelineHistory.remote-boundary.test.tsx \
src/tools/video-editor/hooks/useTimelineSave.test.tsx \
src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx \
src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx
```

OLDRED: the same runner, restricted to `ShotTimelinePreview.integration.test.tsx -t 'durable A2 handoff'`, failed against original production code with zero A2 commits; passed after restoration of the implementation.

All three checks passed under one serialized lock:

```bash
PATH=/opt/node20/bin:$PATH flock -w 600 /home/user/work/.app-tsc.lock bash -c \
'node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json &&
 node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json &&
 node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json'
```

Scoped `eslint --max-warnings 0` passed for all six changed files. `git diff --check`, allowed-file census, and mounted callgraph census passed. Existing tests were preserved.

No blockers. Browser/backend behavior was not exercised; no full suite ran. `commit-msg` and `DONE` are written; no commit performed. **Next: independent Luna review.**