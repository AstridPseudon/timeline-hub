# Vite operation Connection nomination repair

Completed the bounded repair on base commit `a81e8ddd3e5b5d57154c53fbb8f1d6d78a4af9c0`, after reading PLAN and the independent review. Final centrally tested source tree: **`6684d0eeb0cfdbc19a594f70a3a15eb00806e35b`**. The harness supplies the final commit after worker exit; no final commit SHA is claimed here. Ready for orchestrator review; no task blockers. This does not activate the browser host/requester.

| Source | Final lines and change |
| --- | --- |
| `config/vite/runtimeProxy.ts` | Lines 10–23 strip standard hop headers (including legacy Proxy-Connection), browser credentials and all Connection nominations collected from original raw header pairs. Both normalized headers and raw pairs are updated before Vite/http-proxy copies them. Lines 79–85 validate original admission and admission after stripping; nominated private handles refuse with 400, including acquisition/replacement and alternative ordinary paths. Lines 58 and 65–66 remove Vite's default Access-Control-Allow-Origin on operation responses/errors. 21 insertions, 3 deletions. |
| `scripts/runtime-discovery-proxy-operation.test.mjs` | Lines 143–164 add a pure admission/scope regression. Lines 506–537 promote the independent positive stripping regression with its assertions unchanged. Lines 539–617 add actual Node/Vite/proxy/Runtime cases for duplicate raw Connection lines, mixed case, multiple tokens, Expect, nominated Authorization/Cookie/key/handle, invalid original origins/metadata, both request hops, exact normal handle/key/body/path/method, Range and no fallback. 136 insertions, no deletions. |

Only these two repository files changed: **157 insertions, 3 deletions**. No server map, timeout, callback fence, Node discovery proxy, launcher, ordinary proxy implementation, chat, catalog, client, dependency or wire contract change. Ordinary admission bypass remains byte-for-byte behaviorally checked by the added pure test. The pinned Runtime bearer still enters only at the existing discovery-proxy injection after stripping.

| Final file | SHA-256 | Git blob SHA |
| --- | --- | --- |
| `config/vite/runtimeProxy.ts` | `202cc9719b0aba79a298706a9a128a7820ac2a06d4b04d5c3820dbb40f39d9c2` | `c87c3977204444f0735f55a97cc28c5c48f1a3b3` |
| `scripts/runtime-discovery-proxy-operation.test.mjs` | `2f8661b45c98de6e9ba19f8563934ca6a16e57df18aeb8fa12f93eeb7af53ad4` | `a6248e233813bb3000405ab6bb6e3d9b054cb9e1` |

Implementation choices follow the existing contract. Stripping belongs in the existing pre-proxy admission middleware because the installed Vite/http-proxy bypasses its proxyReq event when Expect is present. Reading only the already rewritten outgoing Connection value would reproduce the defect. Original admission is checked before stripping as well: a nominated foreign/null/duplicate Origin or cross-site metadata must never become an admissible absent header. An originally valid Origin-less safe GET/HEAD still follows the existing exact same-origin Fetch Metadata exception. A nominated private handle is refused locally, avoiding an accidental fresh acquisition or ordinary fallback. Idempotency-Key is preserved exactly unless explicitly nominated, when hop semantics remove it. Trusted pinned authorization is injected afterward.

All original **16 operation tests and their helpers** remain byte-identical after removing only the three newly inserted test blocks. All **136 neighbor test sources** remain byte-identical: 61 launcher + 12 chat + 63 Vitest. Nothing was weakened, skipped, disabled, marked expected-failing or rewritten to accept missing behavior.

The independent adversarial source is copied byte-for-byte into this worker's notes, SHA-256 **`57212b7161f7b9b7d5dbb691d383dfef25aa848c13370c652f36a1a2af0b5a48`**. Its manifest checks the repaired snapshot's eight source hashes before imports. The two backpressure/incomplete-acquisition positive tests remain unchanged. Vite bundle SHA-256 remains `bfa94186daff535fefdf286088c1588fad6b02c01ef11cd3b42a6cb3e4c90767`. Shared dependencies were only read.

Final verification (all sockets exclusively central), using `$ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`:

```sh
$ORCH/bin/request-test app-m2-proxy-vite-nomination-fix proxy-operation-integration
$ORCH/bin/wait-test app-m2-proxy-vite-nomination-fix-proxy-operation-integration-1020105025-860 0
$ORCH/bin/request-test app-m2-proxy-vite-nomination-fix proxy-vite-nomination-adversarial-integration
$ORCH/bin/wait-test app-m2-proxy-vite-nomination-fix-proxy-vite-nomination-adversarial-integration-1020105025-31747 0
```

| Final central ID | Actual command | Result |
| --- | --- | --- |
| `app-m2-proxy-vite-nomination-fix-proxy-operation-integration-1020105025-860` | `node --test scripts/runtime-discovery-proxy-operation.test.mjs` | Exit 0, **19 pass / 0 fail / 0 skipped / 0 cancelled**, 5s service wall time. |
| `app-m2-proxy-vite-nomination-fix-proxy-vite-nomination-adversarial-integration-1020105025-31747` | `node --test $ORCH/workers/app-m2-proxy-vite-nomination-fix/notes/proxy-server-independent.test.mjs` | Exit 0, **3 pass / 0 fail / 0 skipped / 0 cancelled**, 3s. Stopped reader filled 10,092,544 bytes, retired with 410 and closed upstream; aborted/timed-out acquires left all 128 slots available. |

Both final `snap` and `summary` files identify tree `6684d0eeb0cfdbc19a594f70a3a15eb00806e35b`. Logs are `tests/<central-ID>/log.txt`, with `summary` and `snap` beside them. Each final lane ran once after the last source edit. A nonblocking wait returned 124 while queued; it was waited again without resubmission.

The first candidate tree `7a1cd037c509b462ec2b13d0194e3dc5769673f2` passed the request stripping checks but exposed a previously unexecuted positive response assertion: default Vite CORS inserted Access-Control-Allow-Origin. Initial central IDs `app-m2-proxy-vite-nomination-fix-proxy-operation-integration-1020104927-12345` (18 pass / 1 fail) and `app-m2-proxy-vite-nomination-fix-proxy-vite-nomination-adversarial-integration-1020104927-30753` (2 pass / 1 fail), both exit 1. The same original assertion was retained, operation-only response stripping was added, and the corrected final tree was qualified above. No failing security assertion was disabled and no global CORS setting was changed.

Direct pure/static commands, exit 0 on final code:

```sh
node --test --experimental-test-isolation=none --test-name-pattern='^pure:' scripts/runtime-discovery-proxy-operation.test.mjs
node node_modules/eslint/bin/eslint.js config/vite/runtimeProxy.ts
node --check scripts/runtime-discovery-proxy-operation.test.mjs
node --check $ORCH/workers/app-m2-proxy-vite-nomination-fix/notes/proxy-server-independent.test.mjs
git diff --check
```

Pure result: **7 pass, 0 fail/skipped/cancelled**. A byte comparison against HEAD confirmed the original 16 operation cases/helpers and all eight neighbor test source files are unchanged.

An optional direct neighbor Vitest attempt used this exact command:

```sh
node --require $ORCH/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/paired/objectCachePolicy.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts src/integrations/runtime/workspaceRuntimeConfig.test.ts src/integrations/runtime/client.runtimeOrigin.test.ts
```

It emitted only the RUN banner and no individual test results, then was interrupted (exit **130**); cause unverified, **no pass evidence claimed**. It was not relaunched. The full 136-neighbor lane was not requested under this brief's socket-lane restriction. Prior neighbor evidence remains the independent review's source-identical `app-m2-proxy-operation-server-proxy-operation-neighbors-integration-1020103059-21846` (136 pass), rather than a claim of final-tree neighbor execution.

No full/build/browser/project-tsc/install/actual activation, local listener, shared cache/dependency/venv mutation, integration-worktree edit, branch/ref change, commit/merge/rebase/checkout/push, build output or temp worktree artifacts. Vite fixtures use removable fixture-local cache directories; the optional Vitest command used runner config loading and disabled caching. Added only one authorized named central entry, `proxy-vite-nomination-adversarial-integration`, to shared `tests/suites.conf`. No KEEP is needed: final central jobs are complete.

Remaining limits match the reviewed operation transport: two-process retirement cannot undo already dispatched acceptance; immutable endpoint/bearer selection cannot synchronously detect revocation/port reuse; fixture Runtime ACKs do not prove real Runtime receipts, retry/restart/undo or same-store requester/outbox composition. The browser-host review is separately APPROVE per this task; it was not rerun here. Next: orchestrator review/land the bounded repair, then perform final coupled supported-tuple qualification before activation. Hosted/paired transport remains outside this agreement.
