A3 source repair complete on base `32036b3cc0`. Changed two production files and added `mountedFileDrop.test.tsx`.

- **OldRED:** both mounted drop modes failed before semantic dispatch. Whole-config preview validation rejected retained parent `opaqueClip` metadata and embedded derived `assetEntry` fields.
- **Repair:** imported image drops use the existing row preview and pass their prepared-media basis into A2. Existing handoffs emit `clip.add-media` and `occurrence.add-media`; the dormant occurrence port remains untouched.
- **Strict controls:** changed scope/head, missing/wrong/ambiguous occurrence, missing/duplicate track, missing row, mismatched media, stale registry, authored uploading-looking IDs, and dependent local commands pass. No upload skeleton enters the authoritative payload.

Validation:

```bash
/opt/node20/bin/node --import "$TMPDIR/vitest-preload.mjs" node_modules/vitest/vitest.mjs run \
  src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts \
  src/tools/video-editor/hooks/useExternalDrop.test.tsx \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
  src/tools/video-editor/commands/occurrenceMediaCapture.test.ts \
  src/tools/video-editor/commands/commitSession.placement.test.ts \
  src/tools/video-editor/hooks/mountedFileDrop.test.tsx \
  src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommit.test.tsx \
  src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts \
  src/tools/video-editor/commands/localSaveSession.test.ts \
  --config "$TMPDIR/vitest.config.mjs" --no-cache --configLoader=runner \
  --maxWorkers=1 --no-file-parallelism
```

**219 passed.** Final strengthened mounted regression: **15 passed**. Private configuration supplies Node20’s missing `__dirname`/`navigator`; initial tooling failures were resolved without test changes.

Also passed:

```bash
/opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit
/opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit
/opt/node20/bin/node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/lib/external-drop-utils.ts src/tools/video-editor/hooks/mountedFileDrop.test.tsx --max-warnings=0
git diff --check
```

All six protected E2E SHA256 values match HEAD exactly. Existing expectation bodies are unchanged.

`commit-msg` and `DONE` created. No blockers. Independent review, merge, and original browser journeys remain for the orchestrator. Mounted controls prove transport dispatch using a deliberate invalid-response fixture; Runtime acceptance and browser PASS remain unverified.