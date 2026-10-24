Fixed the demonstrated save defect in `contract-metadata.ts`: D62 generated digest `867f…` was missing from `supportsFullV2Commit()`, blocking `doc.patch` dispatch before transport. Added that exact digest and a mounted split regression using real generated metadata, the durable outbox, and generated transport.

Retained run `13564` used App `bc0b…`, Agent `57779274…`, Runtime `8b32…`; later base `6d74…` has the same defective gate. Historical passing `18792` used accepted digest `35c2…`. The trace confirms local splitting; its 503s concern chat/discovery.

Validation:

```bash
ASTRID_CHECKOUT=/home/user/work/agent node \
  --require /tmp/w-91e2b6d1a3/vitest-dirname.cjs \
  node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --no-cache --configLoader=runner \
  src/tools/video-editor/hooks/useTimelineSave.currentContract.test.tsx \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
  src/tools/video-editor/commands/localSaveSession.test.ts \
  src/tools/video-editor/commands/localSaveSession.contract.test.ts \
  src/tools/video-editor/commands/localSaveSession.v2.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts
```

**227/227 passed across seven files.** The preload supplies `__dirname` required by the existing config. Removing only the added digest reproduces oldRED: the focused mounted test rejects flush as unacknowledged. Restoring it produces newGREEN.

Additional checks:

- `node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit` — PASS.
- `node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit` — PASS.
- No `tsconfig.e2e.json` exists. Available `tests/e2e/fake-runtime/tsconfig.json` failed with four missing `ImportMeta.env` typings; `node node_modules/typescript/bin/tsc -p tests/e2e/fake-runtime/tsconfig.json --noEmit --types vite/client,node` — PASS. Scope is fake-runtime only.
- Separate focused-test TypeScript config, including repository ambient declarations — PASS.
- `node node_modules/eslint/bin/eslint.js src/integrations/runtime/contract-metadata.ts src/tools/video-editor/hooks/useTimelineSave.currentContract.test.tsx` — PASS.
- `node --check scripts/testing/d66-plain-stack.mjs` — PASS.
- Six original spec SHA256 hashes unchanged against base and retained failing snapshot; `git diff --check` — PASS.

The fix retains the existing strict capability checks. Originals, readiness predicates, launcher, generated files, and request authority are unchanged.

**Next:** Luna core-source review, then merge and have the manager submit exactly one current-head P1:

```bash
R=$("$ORCH/bin/request-test" integration:app d66-plain-p1-three-products) &&
  "$ORCH/bin/wait-test" "$R"
```

No browser/full/service run was submitted. Current P1 remains unverified. Commit message and `DONE` written; no Git mutations or push.