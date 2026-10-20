# PRIVATE392 current post-build App proof

## Result

**BLOCKED before HTTP/Door test collection.** The exact unmocked App consumer
case and named integration registration were composed, but the one permitted
central run stopped in `npm run build:hosted`. No App request, Runtime Door
request, or private392 assertion ran; there is no HTTP response evidence to
report.

The earlier missing `theme-api.fallback.tsx` build failure is not present in
this run. The existing causal repair source (`bc9dad558`,
`app-m2-gate35-retired-alias-setup-causal-fix`) removes stale Vite aliases and
does not restore fallback files.

Sanitized central failure:

```text
src/tools/video-editor/compositions/playerEvaluation.ts (3:2):
"clipOpacity" is not exported by
"@banodoco/timeline-composition/dist/evaluation.js"
code: MISSING_EXPORT
```

This is an existing shared Composition package/artifact mismatch. I did not
modify the shared install, package, fallback sources, provider, schema, or
Runtime pin.

## App delta

- Added `tests/integration/runtimePrivate392Consumer.test.ts`, copied exactly
  from the reviewed unmocked Door driver source `85ae206b`.
- Registered it in
  `config/testing/vitest.runtime-restore.integration.config.ts`.
- The driver uses App generic patch capture, the command session, IndexedDB
  outbox, and `RuntimeDataProvider`; the transport sends through the real
  authenticated `DirectHarness` Door. It retains guards for merge/replace,
  original absence, opaque values, lost acknowledgement/reload/exact retry,
  disjoint rebase, guarded undo, stale refusal, and zero legacy POSTs.
- Exact tuple guards are retained: Agent `1303ce6b` with `e010` and schema392,
  Runtime `f8da4b6d`, and the reviewed artifact/schema digests.

## Checks

- `node_modules/.bin/eslint tests/integration/runtimePrivate392Consumer.test.ts config/testing/vitest.runtime-restore.integration.config.ts --ext ts --max-warnings 0` — PASS.
- `node_modules/.bin/tsc --noEmit --pretty false` — PASS.
- `node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts` — 3 files / 30 tests PASS.
- `git diff --check` — PASS.
- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d` — FAILS at preflight because this current integration worktree's existing `runtime.lock.json` pins source `2c4ac180…`/artifact `6f000…`, while the exact private392 driver requires `f8da4b6d…`/artifact `52df…`. The no-pin rule forbids changing it here.
- Central named suite, one run only: `ap2-m2-private392-real-app-door-consumer-gate`, request `ap2-m2-private392-current-postbuild-app-proof-ap2-m2-private392-real-app-door-consumer-gate-1020230652-28265` — FAIL, exit 1, 27s, hosted build `MISSING_EXPORT` before Vitest collection/HTTP.

## Next step

The shared Composition package/artifact owner must provide a current package
whose public evaluation export includes `clipOpacity` (or reconcile the
current App consumer to the approved package source). Then rerun this existing
named suite once on the same exact tuple. Do not restore the retired fallback,
change the Runtime pin/schema/provider/store, or activate the private family
until the actual HTTP evidence passes.
