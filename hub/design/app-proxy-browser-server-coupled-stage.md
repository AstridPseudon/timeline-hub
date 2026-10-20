# Inactive browser host + repaired proxy coupled stage

Completed on the assigned App worktree. **Inactive; activation remains HOLD.** Read PLAN first and followed the existing local transport agreement; no settled decision changed.

## Exact inputs and result

| Input | Committed ref | Applied scope |
| --- | --- | --- |
| Current App base | `7bb885b638838588a0dff81b64b7c34960ac07f3` | Preserve current main, root/provider/render, generated client, root Composition 0.0.8 and current ordinary CORS |
| Approved browser host | `be27b45066947e920cda8da67991976b432ccb33` | Three-path host/test/decoder extraction delta |
| Final repaired server | `66fc28fafabcc074c688e7a7b50b296df41fc70f` | Six-path server delta, including the committed Vite nomination repair |

The server ref was observed only after its harness commit and DONE. It supersedes the reviewed, defective `a81e8ddd3e5b5d57154c53fbb8f1d6d78a4af9c0`. Applied working-tree patches only; no commit/merge/checkout/ref mutation or push. All six server paths are byte-equal to the final committed repair; all three browser paths are byte-equal to the approved browser commit. Only the normal-repo coupled test is additional.

**Final tested source tree: `7e1ba6f2c485705bec39b51074b9a2f510fc63cf`.** Ten changed repository files. Net **+1,971 lines**: product/declarations **+658** (+687/-29, including 18 declaration lines), tests **+1,313**. Product consists of the imported server +387 and browser/decoder +271. Tests: imported server 617, imported browser 353, new coupled fixture 343. No new product abstraction was needed.

## What the new test proves

`scripts/runtime-operation-host-integration.test.mjs` loads the actual production `RuntimeOperationHost`, handwritten/generated client, shared decoder and existing receipt fixture through a private Vite SSR loader. It composes the real Vite operation admission/options and prefix with the real pinned discovery proxy and a raw synthetic HTTP upstream. The launch-policy loader reads actual `/runtime-config/v1/workspace.json`; it is not mocked. Its private config uses the existing production aliases and operation/config/ordinary route shapes, without importing the full application startup configuration.

Ten cases cover negotiation; task admission and task/managed-output/media/object/HEAD reads; exact original UTF-8 commit bytes and key; normal receipt/canonical-closure decoding; endpoint and credential file rotation with the old binding pinned; a new equal-actor/realm binding sending the original request; late fixture ACK rejection; disposal during health/handshake/realm/task/object socket waits; synchronous browser retirement; remote DELETE followed by observed 410; server shutdown during pending commit; wrong-realm negotiation refusal; malformed receipt refusal without latest-read fallback; exact public frozen API; forbidden origin, duplicate mixed-case Connection nominations, nominated private handle and alternative proxy paths refusing without ordinary fallback. The unchanged server tests additionally retain expiry, incomplete acquisition, backpressure, streaming/upload retirement and dispatch fences.

All original browser 244 cases and the 25 independent probes retain their original positive assertions. The independent probes were copied under this worker's notes with import paths redirected to this worktree; their three requester-interface probes continue to use the review's frozen requester context only. Original server 16 cases and all 136 neighboring behaviors remain present; the repaired server adds three cases. No existing behavior was weakened, skipped, deleted or reclassified. Package/lock, generated/client code, baseline CORS helper and existing neighboring test sources were byte-checked unchanged against the base. Main chat/New/Make Main behavior passes in the central lane.

## Exact verification

In the following commands, `ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch` and `W=$ORCH/workers/app-m2-proxy-browser-server-coupled-stage`; repository commands run from the assigned worktree.

Final central request and wait:

```sh
$ORCH/bin/request-test app-m2-proxy-browser-server-coupled-stage proxy-browser-host-coupled-integration
$ORCH/bin/wait-test app-m2-proxy-browser-server-coupled-stage-proxy-browser-host-coupled-integration-1020105558-7656 0
```

**Exit 0, 53 seconds, 363 passing cases, zero failures/skips/cancellations.** Run ID: `app-m2-proxy-browser-server-coupled-stage-proxy-browser-host-coupled-integration-1020105558-7656`. [Summary](../tests/app-m2-proxy-browser-server-coupled-stage-proxy-browser-host-coupled-integration-1020105558-7656/summary), [full log](../tests/app-m2-proxy-browser-server-coupled-stage-proxy-browser-host-coupled-integration-1020105558-7656/log.txt), [tree](../tests/app-m2-proxy-browser-server-coupled-stage-proxy-browser-host-coupled-integration-1020105558-7656/snap).

The authorized named suite was added to the shared `tests/suites.conf`. Exact service commands, sequentially joined with `&&`:

```sh
python3 $ORCH/managers/app/notes/central-standard8-snapshot.py
node --test --test-concurrency=1 scripts/runtime-discovery-proxy-operation.test.mjs scripts/runtime-operation-host-integration.test.mjs scripts/dev-local-workspace.test.mjs
env TSX_DISABLE_CACHE=1 node --import tsx --test --test-concurrency=1 scripts/astrid-project-chat-runtime.test.ts scripts/astrid-project-chat.test.ts
node --require $ORCH/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/paired/objectCachePolicy.test.ts src/integrations/runtime/operationHost.test.ts src/integrations/runtime/timelineCommit.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts src/integrations/runtime/client.runtimeOrigin.test.ts src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/dataProvider.parity.test.ts src/integrations/runtime/workspaceRuntimeConfig.test.ts
```

Counts: **90 Node cases** (19 server + 10 new coupled + 61 launcher), **12 chat**, **261 Vitest across 9 files** (244 browser/neighbor cases plus 17 object-cache policy cases). This includes all original server 16 + neighbor 136/browser 244 cases, with overlap between lanes counted once in the 363 total.

Direct socket-free commands and results:

```sh
node --require $ORCH/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/runtime/operationHost.test.ts src/integrations/runtime/timelineCommit.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts src/integrations/runtime/client.runtimeOrigin.test.ts src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/dataProvider.parity.test.ts src/integrations/runtime/workspaceRuntimeConfig.test.ts
node --require $ORCH/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config $W/notes/review.config.ts --configLoader=runner --no-cache --maxWorkers=1
node --test --experimental-test-isolation=none --test-name-pattern='^pure:' scripts/runtime-discovery-proxy-operation.test.mjs
node node_modules/eslint/bin/eslint.js config/vite/runtimeProxy.ts config/vite/vite.config.ts src/integrations/runtime/operationHost.ts src/integrations/runtime/operationHost.test.ts src/integrations/runtime/dataProvider.ts scripts/runtime-operation-host-integration.test.mjs scripts/runtime-discovery-proxy.mjs scripts/runtime-discovery-proxy-operation.test.mjs scripts/dev-local-workspace.mjs --max-warnings 0
node node_modules/eslint/bin/eslint.js scripts/runtime-operation-host-integration.test.mjs --max-warnings 0
node --check scripts/runtime-operation-host-integration.test.mjs
git diff --check
```

Results respectively: **244/8 files pass**, **25/1 file pass** (including the original 80 propagation intervals), **7 pure pass**, both lint commands/syntax/whitespace **exit 0**. Logs are in worker `notes/{targeted,independent,pure,lint}.log`. The final central run repeats the relevant 244 against the whole composed source tree.

Two superseded central attempts are reported honestly: `...-1020105344-20696`, tree `60ce84266eebf6a692178e70b06e95bea3d135a5`, 80 pass/10 fail because the new SSR fixture omitted the existing SDK alias; `...-1020105449-22267`, tree `a1975744b3447261653a642a9676d8fdaaca3eaa`, 89 pass/1 fail because the new assertion incorrectly expected `admitTask().data.task_id` rather than the existing generated `admitTask().task_id`. Corrected only the new loader/assertion. The first request also preceded correction of the new private-handle-nomination assertion from 410 to the repair's existing fail-closed 400. No product repair or original-test expectation change was required. Final run above supersedes both.

## Decisions, limits and next steps

Used private Vite SSR to exercise the real TypeScript host and dependency graph while keeping the normal repository socket test executable by Node. Reused the existing launch policy and receipt fixture, with no second acceptance model, journal, schema, identity format or deduplication ledger. No blocker remains for this inactive coupled stage.

**The upstream is a synthetic socket fixture, explicitly NOT Runtime acceptance.** Fixed fixture receipts do not prove semantic acceptance, backend idempotency/deduplication, lost-ACK recovery, restart durability, undo, native capture or storage/outbox behavior. The fixture request is used for byte transport, not as a semantically accepted Runtime command. Node fetch is not Chrome: an immediate native-fetch adapter supplies browser-like Origin/Fetch Metadata and resolves same-origin relative URLs. Actual browser policy/behavior remains open. Silent remote expiry is locally unobservable until a response; browser/server retirement are separate HTTP processes, and handed-off work can already have accepted. Retirement is not rollback.

The official current Runtime tuple is still pending. Real Runtime acceptance/exact receipt replay/restart, requester/outbox/claim/native capture, and actual browser qualification remain **OPEN**. Recommended next step: independent review/integration of this inactive composition, followed by those gates on the supported frozen tuple before activation. No root/provider activation, automatic requester, outbox change, root12/pin/UI activation, hosted/paired support or wider authority was added. Only the existing decoder extraction changes provider implementation.

No full suite, build, browser, project tsc, install or external network run. Every socket test ran centrally. Direct tests used a worker-owned node_modules symlink to read-only `/tmp/app-m2-coherent-deps8/node_modules`; the central setup replaces only its own snapshot symlink after verifying the existing root8 package. Shared dependencies, shared caches and venvs were not modified. New Vite caches live in per-fixture temporary directories and are removed; Vitest is cache-free/runner-loaded with one worker and Node files are sequential. No build output/temp files remain in the worktree. No KEEP.
