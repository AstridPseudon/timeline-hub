Confirmed and repaired the **cancelled-bootstrap restart deadlock**. Only the two assigned files changed.

The production hook’s cleanup cancelled its pending verified read but left `started=true`. On rerun, the guard returned because no saved session existed. Resolving valid history afterward could not create a session.

**Historical attribution remains UNKNOWN.** The actual18800 evidence shows cancellation after approximately 679 ms; it does not identify the changed dependency. The reproduction uses a legitimate asset-resolver replacement as a controlled trigger.

The repair invalidates cancelled startup generations, permits same-owner restart, and retires any in-flight claim before replacement. Verified-basis, identity, head, closure and durable-request guards remain intact.

Validation:

- **RED before repair:** genuine mounted-hook reproduction failed with `ownerId === undefined`.
- **GREEN:** **176/176 tests across seven files**, including all 65 prior hook cases and 13 added cases.
- Added coverage includes deferred basis/identity success and failure, stale capture rejection, claim disposal, unmount, changed scope/head, verification failure, and exact durable-owner/request/key recovery.
- Root, App and Node TypeScript checks: **PASS**.
- Scoped ESLint and `git diff --check`: **PASS**.

Exact principal test commands:

```bash
NODE_OPTIONS="--require=$TMPDIR/vitest-dirname.cjs" /opt/node22/bin/node node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/vitest.config.mjs" --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx \
  -t 'restarts a cancelled pending verified read'
```

```bash
NODE_OPTIONS="--require=$TMPDIR/vitest-dirname.cjs" /opt/node22/bin/node node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/vitest.config.mjs" --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx \
  src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx \
  src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
  src/tools/video-editor/commands/localSaveSession.test.ts \
  src/tools/video-editor/commands/localSaveSession.v2.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts
```

```bash
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 bash -c \
'/opt/node22/bin/node node_modules/typescript/bin/tsc --noEmit -p tsconfig.json &&
 /opt/node22/bin/node node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json &&
 /opt/node22/bin/node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json'

/opt/node22/bin/node node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/hooks/useTimelineSave.ts \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0

git diff --check
```

The private config imports the repository config and redirects caches into `$TMPDIR`; a private preload supplies its required `__dirname`. Initial config-loading attempts failed before test collection.

Source binding:

| Source | Git blob |
|---|---|
| Actual384 hook | `c004ec66e4d941cb6a645c6384cc196f11d281c5` |
| Assigned f8 hook before repair | `e87a3706bcf4e207dd6198b28e20b78e22b6cf43` |
| Repaired hook | `e79e083dbca9d67fbc0c66051a365ad59b897ff5` |
| Final hook tests | `2b38f9b8b491d893229ec689cc8245e81fd838eb` |

Base remains `f8b15af0a66ed14e7711a4bb7f1ed5b62b4988b5`. Its display-projection repair and pre-existing P1-chain changes differ from actual384; this work does not requalify that historical run. Protected bodies, harness, diagnostics, manifests and all files outside ownership remain unchanged from f8.

Fixtures control provider responses and Web Locks, using the real hook/session/outbox with fake IndexedDB. No browser, backend, HTTP, full-suite, P1, P2 or P3 run occurred. An already-entered cancelled claim can leave an empty record; it is disposed before replacement and cannot append stale intents.

No blockers. Commit message and `DONE` written. Next: independent Luna review, then orchestrator authorization for one changed run; P2/P3 remain on hold.