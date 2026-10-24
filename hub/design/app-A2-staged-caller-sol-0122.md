Implemented the A2/A4 staged-caller migration. Only `VideoEditorProvider.tsx` and a new focused staging test changed.

Production path is now:

`VideoEditorProvider staged drain → Runtime generation/variant lookup → getProjectMediaSelection → createTimelineCommands(store).addClip({ preparedAsset }) → prepared-media preview → A2 save/outbox`

The exact returned selection is preserved. Runtime’s captured variant ID supplies the asset alias; generation, variant, asset, and object mismatches are refused before placement. No new operation, executor, manifest, or media-authority bypass was added.

| Former behavior | Current evidence |
|---|---|
| Transaction `dryRun/apply` placement | Prepared-media facade; descriptor execution spies remain uncalled |
| Once-only staging and timeline-end placement | URL/queue deduplication; ordered placements at 2s and 7s |
| Selection, registry, metadata and notices | Mounted assertions preserve them; four identity refusals leave state untouched |
| Unmount/retry | Pending item survives selection completion after unmount and succeeds on remount |

All existing assertions remain unchanged. D31 remains **397 lines / 40 assertions**, with its helpers untouched.

Final validation: **279 tests passed across nine files; zero failures/skips**.

```bash
/opt/node20/bin/node --import "$TMPDIR/dirname-preload.mjs" \
  node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/vitest-fixture.config.mts" \
  --configLoader=runner --no-cache --maxWorkers=2 \
  src/tools/video-editor/contexts/VideoEditorProvider.test.tsx \
  src/tools/video-editor/contexts/VideoEditorProvider.staging.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
  src/tools/video-editor/hooks/useTimelineCommit.test.tsx \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx \
  src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.test.ts \
  src/tools/video-editor/commands/media.test.ts \
  src/tools/video-editor/commands/runner.test.ts
```

The persistence test used exact qualified blob `40bcffb9f228141bba773c570f6a8451c2d60b0c` through a private `$TMPDIR` overlay. It was **not imported into this branch**.

These also passed:

```bash
NODE_OPTIONS=--max-old-space-size=4096 \
flock -w 60 /home/user/work/.app-tsc.lock bash -c 'set -e; set -x;
  /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.json --noEmit --incremental false;
  /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --incremental false;
  /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit --incremental false'

/opt/node20/bin/node node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/contexts/VideoEditorProvider.tsx \
  src/tools/video-editor/contexts/VideoEditorProvider.staging.test.tsx \
  --max-warnings 0

git diff --check
```

Save/outbox and v2 contract code remain untouched. Authority remains limited to existing qualified operations: ordinary image addition and after-anchor video duplication. Tests use in-memory transports; no full suite, browser, backend, HTTP service, or shared-dependency mutation occurred.

Remaining runner references: `useTimelineState`’s exposed validate/dryRun/apply API, `useTimelineHistory` inversion, retained media helpers and exports. Recommend retiring these in their assigned cuts.

Source: `fb27e554a9ba47e58ae4ae617581ec99e8fb6876`  
Base tree: `fb370ea04fd0543969729346016cf0bd5b464d01`  
Final worktree tree: `44e96686afcacbbe8287d262ce66a7bc577afcb0`

No blockers. Conventional A2/A4 `commit-msg` and empty `DONE` were written; no commit or push was run.