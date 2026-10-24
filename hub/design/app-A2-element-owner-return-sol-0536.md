Implemented exact mounted-source binding to the existing editor adapter. Parameter edits now preserve local previews for dependent gestures. Fixed the Inspector’s initial version mismatch.

- **GREEN:** 284 existing tests + 9 real mounted-form tests.
- **RED control:** removing source-identity validation caused all four ownership attack tests to fail.
- Verified dependent edits before ACK, conflict rollback, and missing/copied/forged/stale/foreign/closed-owner refusals before append.
- Three serialized typechecks, scoped ESLint, and diff checking passed.

Commands used with Node20:

```bash
export PATH=/opt/node20/bin:$PATH

node node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/vitest.config.mjs" --configLoader runner --no-cache \
  --maxWorkers 1 --no-file-parallelism \
  src/tools/video-editor/hooks/{useClipEditing.test.ts,timelineLocalSaveHandoff.test.ts,useTimelineSave.test.tsx} \
  src/tools/video-editor/components/PropertiesPanel/{AstridElementParams.test.tsx,ClipEffectsTab.test.tsx,PropertiesPanel.test.tsx} \
  src/tools/video-editor/contexts/VideoEditorProvider.staging.test.tsx \
  src/tools/video-editor/runtime/element-adapter.test.ts \
  src/tools/video-editor/commands/{localSaveSession.recoveryBasis.test.ts,localSaveSession.v2.test.ts}

node node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/vitest.config.mjs" --configLoader runner --no-cache \
  --maxWorkers 1 --no-file-parallelism \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.mounted.test.tsx
```

The ownership RED used the second command with `-t 'copied|forged|wrong editor|stale'`: **4 expected failures**.

```bash
flock -w 600 /home/user/work/.app-tsc.lock bash -c 'set -e;
export PATH=/opt/node20/bin:$PATH;
node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json;
node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json;
node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json'

node node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/hooks/{useClipEditing.ts,useTimelineSave.ts,useTimelineSave.test.tsx,timelineLocalSaveHandoff.test.ts} \
  src/tools/video-editor/contexts/VideoEditorProvider.tsx \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.mounted.test.tsx \
  --max-warnings 0

git diff --check
```

No blockers or cross-owned edits. Commit message and `DONE` written; ready for review. Historical13583’s parameter phase remains unrun. No browser/backend/full suite was run, and these findings are not attributed to the original catalog failure.