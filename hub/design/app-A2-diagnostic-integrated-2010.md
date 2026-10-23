# A2 diagnostic source integrated qualification

## Scope and disposition

This is a source-integrated qualification of the App A2 mounted-save diagnostics at merged commit `ba8583b8292790e9d5651504f755762e35c74dab`, tree `6b702ef409f216af31f34f982a3393efedb19370`. It makes no semantic, source-port, request-body, transport, P1-cause, or GO claim.

The merge has first parent `be890a1fa5d6db02e4964522aa356f88f115a22a` and second parent `201044ee605abf3e79c4e6418d2144c7a9365680` (the reviewed independent source). The exact five current blobs are:

| file | blob |
| --- | --- |
| `src/tools/video-editor/hooks/useTimelinePersistence.ts` | `5783f6a717371de9de176c774a4c1dcaf36e46cf` |
| `src/tools/video-editor/hooks/useTimelineSave.test.tsx` | `210b54012e6801306614adb547c30456b92d1172` |
| `src/tools/video-editor/hooks/useTimelineSave.ts` | `0372dafa80a727a86ac9d614b550217305dca56c` |
| `src/tools/video-editor/lib/timeline-diagnostics.save.test.ts` | `a4de292d171015a85db8ec8fbdfca2b9b9352914` |
| `src/tools/video-editor/lib/timeline-diagnostics.ts` | `db1f02a7f71727c381706face3594af33e05fd41` |

`git diff be890a1fa5d6db02e4964522aa356f88f115a22a..HEAD` contains only those five paths. The merge is conflict-free in the resulting tree. Collector `b221388d30b76798b58ee0510c1a4b3c77e982a5` and popup `17324ed4b741237fe425638d86617d2be8224b72` are both preserved ancestors. The D26 branch `a9d72ff50c` was not merged, altered, stopped, or resubmitted; its pinned base remains `be890a1fa5`.

## Source contract check

The production caller uses the actual mounted save path:

`useTimelineSave` capture callback → original verified basis read → real handoff capture → existing LocalSaveSession/outbox → actual prepared-display adoption and adopted-read callback.

The diagnostic emitter is explicitly opt-in, allowlisted, bounded, guarded, and observational. It reads named own data properties, preserves unknown/null state, does not retain or serialize App objects, and rethrows no diagnostic failure into the save path. Existing save/reply/error semantics and callback/effect dependency behavior are unchanged. The existing D26 test, P1 bodies, Gate-5 blob, schemas, pins, locks, generated files, and dependencies were not touched.

## Verification

Available local runtime: `/opt/node20/bin/node --version` → `v20.20.0`; shared dependency realpath: `/home/user/work/app/node_modules`.

Passed targeted Vitest, exit 0, 3 files / 128 tests:

```sh
PATH=/opt/node20/bin:/usr/bin:/bin /opt/node20/bin/node --import 'data:text/javascript,globalThis.__dirname=process.cwd()+"/config/testing"' node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/lib/timeline-diagnostics.save.test.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelinePersistence.test.tsx
```

Passed Node TAP command, exit 0:

```sh
PATH=/opt/node20/bin:/usr/bin:/bin /opt/node20/bin/node --import tsx --test tests/e2e/local/p1-diagnostic-safety.test.ts
```

Observed TAP counts were exactly: `TAP version 13`; one file-level subtest named `tests/e2e/local/p1-diagnostic-safety.test.ts`; `1..1`; `# tests 1`; `# pass 1`; `# fail 0`; cancelled/skipped/todo all 0. The file contains 16 `node:test` declarations, but that source count is not substituted for the emitted TAP count. The requested Node v20.19.4 and the prior OPS1956 16-test TAP shape were not locally reproducible because the available runtime is v20.20.0; this is an evidence caveat, not a source change.

Passed all three serialized typechecks, exit 0, under `flock -w 600 /home/user/work/.app-tsc.lock` with `NODE_OPTIONS=--max-old-space-size=4096`:

```sh
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --pretty false
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit --pretty false
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.json --noEmit --pretty false
```

Passed scoped ESLint with zero warnings and `git diff --check`, exit 0:

```sh
/opt/node20/bin/node node_modules/eslint/bin/eslint.js src/tools/video-editor/lib/timeline-diagnostics.ts src/tools/video-editor/hooks/useTimelineSave.ts src/tools/video-editor/hooks/useTimelinePersistence.ts src/tools/video-editor/lib/timeline-diagnostics.save.test.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0 --report-unused-disable-directives
git diff --check
```

No full suite, browser, HTTP, live service, seed, preflight, body, benchmark, or D26 run was requested. The worktree is clean and no tracked changes were introduced by this qualification.

## Follow-up

If acceptance requires the exact historical environment/count, rerun only the same targeted commands through the owner’s Node v20.19.4 / OPS1956 harness. Do not alter or rerun the pinned D26 test as part of that follow-up.
