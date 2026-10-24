Implemented A2 track display projection: **6 files, +81/−12 lines; nothing deleted**.

Both production load paths and the bridge baseline now use the existing sanitizer on a separate display copy. The session/outbox retains the complete raw canonical basis. Strict serialization, capture/media guards, VIDEO behavior, and IMAGE `intent: {}` remain unchanged.

Two existing caller tests now verify opaque tracks, nulls/absence, one `clip.add-media` with no track patch, canonical adoption, dependent trim, refusal, and exact retry.

Validation:

- **RED:** mounted IMAGE accepted case failed before the fix; no clip reached preview.
- **GREEN:** **188 passed across 9 files**, including all 65 mounted-save tests.
- Root/App/Node TypeScript checks and scoped ESLint: **passed**.
- `git diff --check`, six-file scope audit, serializer/capture source comparisons, and test identity checks: **passed**.

Exact final test command:

```bash
NODE_OPTIONS="--require=$TMPDIR/vitest-dirname.cjs" node node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/vitest.config.mjs" --configLoader runner --no-cache --maxWorkers 1 \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx \
  src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.test.ts \
  src/tools/video-editor/commands/media.test.ts \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/lib/timeline-data.test.ts \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
  src/tools/video-editor/hooks/useTimelineCommit.test.tsx \
  src/tools/video-editor/commands/localSaveSession.test.ts \
  src/tools/video-editor/commands/localSaveSession.v2.test.ts
```

```bash
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 bash -c 'node node_modules/typescript/bin/tsc --noEmit -p tsconfig.json && node node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json && node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json'

node node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/lib/timeline-data.ts \
  src/tools/video-editor/lib/timeline-domain.ts \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts \
  src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.ts \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx \
  src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.test.ts \
  --max-warnings 0

git diff --check
```

The immutable input remains **8,957 bytes**, SHA-256 `e61c49fe584c416aa6df63156950b2158b4f72ae626460491ca9cdbce863b01d`.

Evidence is App transport-fixture routing and preservation, **not live provider acceptance**. Standalone historical-input replay failed during module loading (`@astrid/packs`, then Vite `virtual:`). Its child-occurrence guard remains unchanged. No backend/browser/full suite, dependency changes, or Git mutations occurred.

Recommend independent review, then the separately owned live witness. Commit message and `DONE` are written.