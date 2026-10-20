# App proxy operation server

Implemented the approved same-origin operation lifetime on base `35dbb0eb12d75dc2c1becf7a9d8ac914758c05c7`. Read PLAN, owner INBOX 10:02, the lifetime proposal, Runtime ACK 10:11, and the independent proposal review before code. No settled decision was changed or contradicted. Final centrally tested App source tree: `e53e49b0da066d583a9672c7ba2f0c2c10a7e9e2`.

## Minimal source change

| File | Change |
| --- | --- |
| `scripts/runtime-discovery-proxy.mjs` | Reuse one validated discovery/credential/catalog snapshot; add one memory-only map, exact control/data admission, pinned Node dispatch, retirement and resource cleanup. Ordinary per-request discovery/cache forwarding remains intact. |
| `scripts/runtime-discovery-proxy.d.mts` | Declare the operation helpers/options and existing workspace-config reader. |
| `scripts/dev-local-workspace.mjs` | Supply the exact local App origin to Vite and the owned discovery-proxy process. |
| `config/vite/runtimeProxy.ts` | Dedicated unchanged-prefix/no-startup-token proxy options and admission middleware for dev/preview; fixed no-store 503 on proxy connection failure. |
| `config/vite/vite.config.ts` | Install that rule/plugin at the existing listeners. |
| `scripts/runtime-discovery-proxy-operation.test.mjs` | Six pure tests and ten socket tests using the production helpers and actual Vite/proxy/upstream chain. |

No browser client/operation host, generated code, requester, outbox, Runtime product code, chat implementation, public package pin or root pin changed. No new listener, journal, renewal, eviction or configurable lease framework. Added only the two named App entries `proxy-operation-integration` and `proxy-operation-neighbors-integration` to the authorized shared `tests/suites.conf`; both include `integration` in their cache names.

## Behavior and limits

- Exact `POST`/`DELETE /runtime-config/v1/operation` and `/runtime/v1/...` forwarding, with one 32-byte random hexadecimal handle in `X-Astrid-Operation-Handle`. Handles are memory-only and never sent upstream, placed in URLs, logged, persisted or added to request identity.
- Each entry captures immutable endpoint scalars, product bearer, selection identity and the actual Node request primitive once. Replacement retires its predecessor before the body await or any new discovery/credential reads, including failed replacement. Missing/expired/unknown handles return 410; malformed requests return 400. No ordinary rediscovery fallback or retry is available on the bound prefix.
- Exact configured Host and App Origin are required at both hops. Origin-less GET/HEAD requires `Sec-Fetch-Site: same-origin`; explicit foreign/null/duplicate origins fail. Reject malformed/absolute/traversing/encoded-separator targets. Strip browser credentials, cookies, handle, Host and hop-by-hop/Connection-nominated headers; add only the pinned bearer. Response headers are restricted, Set-Cookie/redirect Location are withheld, redirects are never followed, and bound/control/error replies are no-store. UTF-8 payload bytes, method/path/query and idempotency keys pass through unchanged. Runtime remains the per-request auth/scope authority.
- Final synchronous active check immediately precedes Node dispatch. Response headers/chunks/end and control-body completion are fenced. Retirement aborts all tracked requests/streams; auth/5xx/I/O failures retire the entry, while 409/422 remain normal semantic responses. `server.close()` retires before shutdown; SIGINT/SIGTERM close owned connections; restart forgets handles.
- Fixed cap: 128 entries, with no active eviction. Idle entries expire after 60 seconds; active flowing requests retain their entry. Existing 10-second connect and 60-second socket-idle timeouts remain; downstream idle timeout also bounds backpressure/stalled consumers. Control bodies are limited to 1024 bytes and the connect-timeout duration. A lost successful acquisition can remain until idle expiry; an aborted/incomplete control request creates no usable entry.
- Honest two-process boundary: browser retirement cannot synchronously retire a server entry before DELETE/replacement HTTP arrives. Already dispatched work may be accepted; retirement is no rollback. Silent external credential replacement does not mutate a captured bearer/endpoint, and remote revocation/port reuse is learned through received failures/negotiation. Snapshot file reads are single reads, not an atomic filesystem transaction.

## Exact verification

Direct, without listeners, exit 0:

```sh
node --test --experimental-test-isolation=none --test-name-pattern='^pure:' scripts/runtime-discovery-proxy-operation.test.mjs
node --check scripts/runtime-discovery-proxy.mjs
node --check scripts/dev-local-workspace.mjs
node --check scripts/runtime-discovery-proxy-operation.test.mjs
node node_modules/eslint/bin/eslint.js config/vite/runtimeProxy.ts
git diff --check
```

Pure result: **6 passed, 0 failed/skipped**; log `workers/app-m2-proxy-operation-server/notes/pure.log`. The default isolated Node runner produced only a file-level result inside the sandbox, so that was not counted as individual-test evidence; the explicit in-process run above and central runs below provide the actual counts.

All sockets/subprocess/listening coverage ran through the central service, with no direct localhost/network execution:

```sh
$ORCH/bin/request-test app-m2-proxy-operation-server proxy-operation-integration
$ORCH/bin/wait-test app-m2-proxy-operation-server-proxy-operation-integration-1020103059-15558 0
$ORCH/bin/request-test app-m2-proxy-operation-server proxy-operation-neighbors-integration
$ORCH/bin/wait-test app-m2-proxy-operation-server-proxy-operation-neighbors-integration-1020103059-21846 1
```

Here `$ORCH` is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`. Exact executed service commands:

```sh
node --test scripts/runtime-discovery-proxy-operation.test.mjs
node --test scripts/dev-local-workspace.test.mjs && env TSX_DISABLE_CACHE=1 node --import tsx --test scripts/astrid-project-chat-runtime.test.ts scripts/astrid-project-chat.test.ts && node --require $ORCH/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/paired/objectCachePolicy.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts src/integrations/runtime/workspaceRuntimeConfig.test.ts src/integrations/runtime/client.runtimeOrigin.test.ts
```

Final results on the same `e53e49...` tree: operation **16 passed, 0 failed/skipped** (5s service wall time); neighbors **61 launcher + 12 chat + 63 Vitest passed, 0 failed/skipped** (54s). Full logs/summaries are under `tests/app-m2-proxy-operation-server-proxy-operation-integration-1020103059-15558/` and `tests/app-m2-proxy-operation-server-proxy-operation-neighbors-integration-1020103059-21846/`.

Coverage includes exact UTF-8/key/auth, endpoint/token rotation with old handle fixed and fresh replacement selected, malformed/forged/missing/duplicate handle and origin/Host/metadata/target refusals, predecessor retirement during a body await and failed selection, concurrent request/stream/upload abort and late ACK suppression, disposal during control/upstream work, restart refusal, silent/stalled/flowing streams, lost acquisition expiry/cap, redirect suppression, and actual Vite no-store/error handling. Original chat rediscovery/rename/Main and ordinary immutable object/Range/ETag/streaming/client identity controls remain passing.

An earlier `c770c126...` tree passed the same operation/neighbor lanes. Final review then identified Vite's default error-shape/no-store gap; a narrow repair and connection-loss assertion justified the final rerun above. No tests were weakened, skipped, disabled or rewritten to encode lost behavior.

No full suite, build, project tsc, install, browser/native capture, actual Runtime receipt acceptance/replay or requester activation was run. Upstream acceptance/ACK bytes in the new socket tests are fixtures, not cross-product qualification. Connect refusal and idle/stream timeouts were exercised; a genuinely stalled TCP connect was not synthesized. Shared dependencies/runtimes/venvs were not modified; Vite uses fixture-local cacheDir, Vitest disables its cache/config bundling, and the final chat lane disables TSX cache. No build output/temp files remain in the worktree. No git commit/merge/rebase/checkout/push or ref changes were performed. No KEEP is needed.

## Decisions, blockers and next steps

No blockers. Kept exact admission in a small shared production helper rather than broadening the bridge origin helper, whose semantics the review found insufficient. Kept ordinary routing unchanged and preserved semantic conflicts; only bound operation auth/unavailable failures retire. Completed the assigned server unit only.

Next: review/land this unit with the separately owned browser host, then separately qualify native capture, same-store requester/outbox composition, actual Runtime acceptance/exact retry/restart/undo and the supported tuple before automatic activation. Hosted/paired operation transport remains unsupported by the agreement.
