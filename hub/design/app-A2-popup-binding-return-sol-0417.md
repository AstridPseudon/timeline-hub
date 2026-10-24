Implemented provider- and mounted-timeline-bound popup handoffs. Forged/copied contexts refuse without fallback. Direct popup capture now requires matching source-head pins; mounted bindings obtain them from verified assembly or acknowledged successors.

Preserved publication-missing refusal, dependent outbox chains, canonical adoption, retry/recovery, and all original assertions. Protected parent-capture and media-command regions are unchanged.

Validation: **351 tests passed across 13 files**—the original exact 12 plus focused context tests. Node 20 runner retained each file’s environment and used private `__dirname`/navigator shims:

```bash
P=src/tools/travel-between-images
H=src/tools/video-editor/hooks
PATH=/opt/node20/bin:$PATH NODE_OPTIONS=--require=$TMPDIR/dirname.cjs \
node node_modules/vitest/vitest.mjs run \
--config $TMPDIR/vitest.config.mts --configLoader=runner --no-cache --maxWorkers=1 \
$P/components/ShotTimelinePreview.integration.test.tsx \
$P/components/shotTimelineDataProvider.a3.test.ts \
$P/components/ShotTimelinePreview.test.ts \
$P/components/ShotTimelineMediaControls.test.tsx \
$P/pages/LocalTimelineShotBrowser.test.tsx \
$H/useTimelinePersistence.test.tsx \
$H/timelineLocalSaveHandoff.test.ts \
$H/useTimelineHistory.test.ts \
$H/useTimelineHistory.remote-boundary.test.tsx \
$H/useTimelineSave.test.tsx \
$H/useTimelineSave.recovery.test.tsx \
$H/useTimelineSave.recovery.persistence.test.tsx \
$H/timelineScopedPersistence.test.tsx
```

All three serialized checks passed:

```bash
PATH=/opt/node20/bin:$PATH flock -w 600 /home/user/work/.app-tsc.lock bash -c \
'node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json &&
 node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json &&
 node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json'
```

Scoped ESLint `--max-warnings 0`, `git diff --check`, and exact six-file scope census passed. No files deleted.

Reproduced forged-context false acknowledgement and missing-head admission before fixing them. Wrong provider/timeline/head, occurrence, and physical-image controls refuse.

The disputed refusal test passes in the whole file but fails in isolation on both untouched `f90` and current source using the same runner. This exposes an existing isolation dependency; assertions remain unchanged. Reviewer runner differences are documented in its log, but are not established as the cause.

No blocker to this scoped fix. No browser/backend/full suite run. `commit-msg` and `DONE` written; no commit performed. Next: fresh independent cumulative review.