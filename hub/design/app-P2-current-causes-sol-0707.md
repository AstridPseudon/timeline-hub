Added [three routed-page controls](/home/user/work/wt/app-P2-current-causes-sol-0707/src/tools/video-editor/contexts/VideoEditorProvider.runtime-elements.test.tsx) using genuine `RuntimeDataProvider`, save lifecycle, adapter and outbox. No product changes.

- **Element:** trace0707 captured a commit POST without a response snapshot. The matching controlled stall is `handoff.flush()` → session transport → `RuntimeDataProvider.commitTimeline()` awaiting its response. Initial owner readiness is not established as the historical cause.
- **Popup ADD:** no commit POST was captured. Its exact pending await remains unknown. Source handoff: `shotTimelineDataProvider.ts:1022–1047` bootstrap, `1053–1063` source-head readiness, `1073–1105` capture/media reads, and `1158–1164` flush.
- Controlled history, commit-response and refresh stalls all complete when released. The commit control verifies durable retention of the exact request and idempotency key. This uses a synthetic native document and controlled fetch responses; it does **not** reproduce an App defect against the original Runtime fixture. No repair RED→GREEN claim is made.

Final targeted command:

```bash
NODE_OPTIONS="--import=$TMPDIR/preload.cjs" /opt/node20/bin/node \
node_modules/vitest/vitest.mjs run \
--config "$TMPDIR/current.config.mjs" --configLoader runner \
--no-cache --maxWorkers=1 --no-file-parallelism \
src/tools/video-editor/contexts/VideoEditorProvider.staging.test.tsx \
src/tools/video-editor/runtime/element-adapter.test.ts \
src/tools/video-editor/runtime/admitted-elements.hosted.test.ts \
src/tools/video-editor/contexts/VideoEditorProvider.runtime-elements.test.tsx \
src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
src/tools/video-editor/commands/localSaveSession.v2.test.ts \
src/tools/video-editor/components/ElementsLibraryPanel.test.tsx
```

**7 files, 108 tests passed.** Initial fixture-development failures were corrected.

These also passed, with typechecks serialized:

```bash
flock -w 600 /home/user/work/.app-tsc.lock /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json
flock -w 600 /home/user/work/.app-tsc.lock /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json
flock -w 600 /home/user/work/.app-tsc.lock /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json
NODE_OPTIONS="--import=$TMPDIR/preload.cjs" /opt/node20/bin/node node_modules/eslint/bin/eslint.js src/tools/video-editor/contexts/VideoEditorProvider.runtime-elements.test.tsx --max-warnings 0
git diff --check
```

No full suite, browser, backend or journey run occurred. Commit message and `BLOCKED` marker written. Next: obtain same-case element response/completion evidence and popup pre-transport phase evidence before selecting a source repair.