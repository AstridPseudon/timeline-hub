Implemented raw clip preservation for moves with unchanged metadata/duration and reuse of the original scheduled capture at interaction end. Handoff/outbox guards remain unchanged.

Ready and delayed-identity mounted cases produce one capture, intent, and request, retaining child closures and causal reads with zero legacy saves. Invalidated original reads still refuse.

Validation:

```bash
A2_FIXTURE="$TMPDIR/a2-source-fixture.json" /opt/node20/bin/node node_modules/vitest/vitest.mjs run --config "$TMPDIR/a2-vitest.config.mts" --configLoader runner --no-cache
```

Retained witness: parent **2 failed/1 passed** → candidate **3 passed**.

```bash
/opt/node20/bin/node node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/a2-controls.config.mts" --configLoader runner --no-cache \
  src/tools/video-editor/lib/timeline-data.test.ts \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/lib/time-grid-conformance.test.ts \
  src/tools/video-editor/hooks/useClipDrag.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommit.test.tsx \
  src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
  src/tools/video-editor/commands/localSaveSession.v2.test.ts \
  src/tools/video-editor/commands/localSaveSession.replayProtocol.test.ts
```

**273 passed across nine files**, including stale-head, wrong-source, and extra-field refusal controls.

```bash
for config in tsconfig.json tsconfig.app.json tsconfig.node.json; do
  flock /tmp/timeline-app-tsc.lock /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p "$config"
done
```

All three passed.

```bash
/opt/node20/bin/node node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/lib/timeline-data.ts \
  src/tools/video-editor/lib/timeline-data.test.ts \
  src/tools/video-editor/hooks/useTimelinePersistence.ts \
  src/tools/video-editor/hooks/useTimelinePersistence.test.tsx --max-warnings 0
git diff --check
```

Both passed. Commit message and `DONE` created; no blockers.

Historical 13583’s internal ordering and actual Runtime acceptance/adoption remain unverified. Recommended next step: independent review and integration.