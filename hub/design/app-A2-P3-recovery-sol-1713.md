**A2-P3: no production defect established; P3 remains NO-GO.** No worktree files changed.

The source/harness mismatch is concrete:

- [useTimelineSave.ts:362](/home/user/work/wt/app-A2-P3-recovery-sol-1713/src/tools/video-editor/hooks/useTimelineSave.ts:362) automatically recovers the sole scoped owner.
- Production renders no `Recover saved edits` control. P3 waits for that control at [three-products.spec.ts:1755](/home/user/work/wt/app-A2-P3-recovery-sol-1713/tests/e2e/local/three-products.spec.ts:1755).
- Passing P1 arms its observer before reload and holds the automatic retry across restart.
- Recovery implementation is byte-identical between this worktree, failed P3 snapshot `db9f088…`, and passing P1 snapshot `0e580cf…`.

Retained P3 proves pending A and dependent B persisted, reload preserved their bytes, and reopen reached the same realm with a new Runtime instance. **Post-reopen retry, B acceptance/merge, undo and final readbacks remain NOTRUN.** The missing fact is the reopened owner’s bootstrap/claim outcome and retry activity during the button wait. The retained artifacts do not establish those.

Existing production-path tests verify exact pending body/key replay, ownership fencing, dependent chaining, canonical adoption, conflict/invalid retention and authoritative history/undo handling. These use local fixtures; they do not qualify the live P3 journey.

Validation used Node 20, private runner config/cache and an existing-pattern `__dirname` preload. Commands below use brace expansion for the exact tested file sets:

```bash
T=(
src/tools/video-editor/commands/{localSaveSession,localSaveSession.v2,localSaveSession.contract,localSaveSession.lifecycle,localSaveSession.ownerRecovery,localSaveSession.recoveryBasis,localSaveSession.replayProtocol,localSaveSession.trackLabelRefusal,commitOutbox}.test.ts
src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts
src/tools/video-editor/hooks/{useTimelineSave,useTimelineSave.recovery,useTimelineSave.recovery.persistence}.test.tsx
)

ASTRID_CHECKOUT=/home/user/work/agent /opt/node20/bin/node \
  --require "$TMPDIR/a2-p3/preload.cjs" node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/a2-p3/vitest.config.mts" --configLoader runner \
  --no-cache --maxWorkers=1 --no-file-parallelism "${T[@]}"

/opt/node20/bin/node --import tsx --test \
  tests/e2e/local/support/gate5-fault-order.test.mjs
```

Results: **266/266 PASS across 13 files**, no skips; fault-order **3/3 PASS**.

```bash
flock -w 600 /home/user/work/.app-tsc.lock /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json
flock -w 600 /home/user/work/.app-tsc.lock /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json
flock -w 600 /home/user/work/.app-tsc.lock /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json

/opt/node20/bin/node node_modules/eslint/bin/eslint.js "${T[@]}" \
  src/tools/video-editor/hooks/{useTimelineSave,timelineLocalSaveHandoff}.ts \
  src/tools/video-editor/commands/{localSaveSession,commitOutbox}.ts \
  src/integrations/runtime/dataProvider.ts --max-warnings 0

git diff --check
```

All three serialized TypeScript checks, scoped ESLint and diff check **PASS**.

The initial filtered replay run passed four assertions but exited 1 because the skip guard rejected 91 filtered-out tests. The complete-file run above resolved that without changing guards. Two earlier config-loading attempts failed before collection on `__dirname`.

No production oldRED/newGREEN repair or new regression was warranted by the evidence. No browser/full/service run, dependency mutation, original-spec edit or contract change occurred. Commit message and empty `DONE` were written.

Recommended next step: authorize the P3 owner to align recovery observation with the automatic production path while preserving exact-request, dependent-edit, restart and undo assertions, then obtain live proof.