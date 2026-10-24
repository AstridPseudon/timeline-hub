Implemented precise recovery refusal: malformed recovery publishes `error`, and later edits and flushes preserve the original failure cause. Failed claims release before another attempt; repairing the authoritative stored basis permits exact replay.

Mapping: explicit retry uses `recover(ownerId)`. Undo uses the real `TimelineLocalSaveHandoff`: `canUndo()` is false, its existing unsettled-history guard rejects without sending, and the precise session error remains intact. No session undo flag/API was added.

Validation on Node **v20.20.0**, with private cache and config runner:

```bash
NODE_OPTIONS=--require="$TMPDIR/vitest-preload.cjs" /opt/node20/bin/node node_modules/vitest/vitest.mjs run --config "$TMPDIR/vitest.config.mjs" --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/commands/localSaveSession.recoveryBasis.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts
```

**100 passed.** Covers exact corrupted-byte retention, no projection/adoption/send, repaired replay, and pending/active double-claim refusal.

```bash
NODE_OPTIONS=--require="$TMPDIR/vitest-preload.cjs" /opt/node20/bin/node node_modules/vitest/vitest.mjs run --config "$TMPDIR/vitest.baseline.config.mjs" --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/commands/localSaveSession.recoveryBasis.test.ts
```

Exact `5ad7907e86` production-source overlay: **7 failed, 1 positive passed**, as required.

```bash
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 bash -c '/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json && /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json && /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json'
```

**All three passed.**

```bash
/opt/node20/bin/node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/localSaveSession.ts src/tools/video-editor/commands/localSaveSession.recoveryBasis.test.ts src/tools/video-editor/commands/commitSession.test.ts --max-warnings 0
git diff --check
git diff 5ad7907e86 --name-only
```

**Passed; exact original three-file scope, no outside changes.** No full/browser/backend/service suites run. No blockers or plan deviations.

Commit message and empty `DONE` written. Next: dispatch independent review **`app-A2-recovery-basis-return-review-0240`**.