# App proxy operation server independent review

**HOLD the server unit at `a81e8ddd3e5b5d57154c53fbb8f1d6d78a4af9c0`.** One confirmed end-to-end header-stripping defect remains: Connection-nominated request headers survive the Vite hop and reach Runtime. The operation ownership/retirement implementation otherwise meets the reviewed same-origin server contract within its stated limits. This is a completed read-only review, not a blocked task or automatic-requester approval.

Worker: `app-m2-proxy-server-independent-review`, 2026-10-20. Read PLAN first, then `app-proxy-operation-server.md`, the exact Runtime ACK in `runtime-app-proxy-operation-agreement.md`, App's lifetime proposal, and `app-proxy-lifetime-proposal-review.md`. No settled decision was changed. Browser owner/private identity/negotiation source has a separate review and is not qualified here.

## Confirmed finding: Vite loses Connection nominations before the stripping helper sees them

**Repair location:** reviewed `config/vite/runtimeProxy.ts:46-48`. The operation proxy's `proxyReq` handler removes only Authorization, Cookie and Proxy-Authorization. It ignores the original incoming request and its Connection nominations.

Installed Vite 5.4.21's bundled http-proxy first copies every request header and then replaces the outgoing `connection` value with `close` (`node_modules/vite/dist/node/chunks/dep-BK3b2jBa.js:60054,60075-60084`). It emits `proxyReq` with both the outgoing request and the original incoming request at `:61234-61237`. The custom nominated fields survive that replacement. Downstream, `scripts/runtime-discovery-proxy.mjs:210-214,286-292` correctly strips nominations **it receives**, but those original names are already gone: it receives `Connection: close` alongside the custom fields and forwards them to Runtime.

The new test uses the actual Vite server, production admission/options, production discovery proxy, and a capturing HTTP Runtime fixture. Input:

```http
GET /runtime-config/v1/operation/runtime/v1/tasks
Origin: <exact configured App origin>
X-Astrid-Operation-Handle: <valid acquired handle>
Connection: X-First, Authorization
Connection: X-Second, Cookie
X-First: first-secret
X-Second: second-secret
Authorization: Bearer browser-secret
Cookie: browser=secret
```

Acquisition and forwarding succeed (`201`, then `200`), and the upstream bearer is correctly `Bearer pinned-token`. However, the assertion that the upstream lacks `x-first` fails: **actual `first-secret`, expected `undefined`**. This directly violates the agreed stripping of Connection-nominated headers. The earlier direct-proxy test nominates `X-Leak` without crossing Vite, so its pass does not cover this transformation. The failure proves nominated custom-header leakage; it does not prove a product-bearer leak, authentication bypass or arbitrary foreign-origin access. The subsequent response-header assertions in this new test are not counted as executed because the request-header assertion fails first.

Failing regression: [proxy-server-independent.test.mjs](../workers/app-m2-proxy-server-independent-review/notes/proxy-server-independent.test.mjs), test beginning at line 98, request at lines 121-123, failure at line 127. Source SHA-256: `57212b7161f7b9b7d5dbb691d383dfef25aa848c13370c652f36a1a2af0b5a48`. Installed Vite bundle SHA-256: `bfa94186daff535fefdf286088c1588fad6b02c01ef11cd3b42a6cb3e4c90767`.

**Smallest repair:** use the original incoming request's Connection tokens at the Vite boundary and remove the nominated fields from its outgoing request before transmission; retain the discovery proxy's independent stripping. Preserve exact admission and fail closed if a nominated required local header is removed. No change to ordinary proxy routing, Runtime auth, listener, registry, browser protocol or dependency is needed. Promote this positive regression into the existing operation test file, then qualify the repaired exact tree centrally. No product repair was made in this read-only task.

## Exact source and existing evidence

Compared frozen branch `tl/app-m2-proxy-operation-server`, final harness commit `a81e8ddd3e5b5d57154c53fbb8f1d6d78a4af9c0`, against base `35dbb0eb12d75dc2c1becf7a9d8ac914758c05c7` using `git show/diff`, without checking it out. Its tree is **`e53e49b0da066d583a9672c7ba2f0c2c10a7e9e2`**, exactly matching both original central `snap` and summary records and the new adversarial run. All six changed paths were read in full:

- `scripts/runtime-discovery-proxy.mjs`
- `scripts/runtime-discovery-proxy.d.mts`
- `scripts/dev-local-workspace.mjs`
- `config/vite/runtimeProxy.ts`
- `config/vite/vite.config.ts`
- `scripts/runtime-discovery-proxy-operation.test.mjs`

Diff: 859 insertions, 9 deletions, including the 481-line test file. No browser host, generated client, requester/outbox, chat implementation or package/root pin is changed. Byte hashes of those six paths plus unchanged `package.json` and `objectCachePolicy.mjs` are recorded in [reviewed-source.json](../workers/app-m2-proxy-server-independent-review/notes/reviewed-source.json). The additional central test verifies all eight hashes against its actual snapshot **before importing production modules**. My own worktree remains at `7bb885b63` and unchanged; it is not represented as the reviewed product tree.

Original central evidence was inspected, not rerun:

- `app-m2-proxy-operation-server-proxy-operation-integration-1020103059-15558`: `node --test scripts/runtime-discovery-proxy-operation.test.mjs`; **16 pass, 0 fail/skipped**, exact final tree above.
- `app-m2-proxy-operation-server-proxy-operation-neighbors-integration-1020103059-21846`: **61 launcher + 12 chat + 63 Vitest = 136 pass**, 0 fail/skipped, same final tree. Command: `node --test scripts/dev-local-workspace.test.mjs && env TSX_DISABLE_CACHE=1 node --import tsx --test scripts/astrid-project-chat-runtime.test.ts scripts/astrid-project-chat.test.ts && node --require $ORCH/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/paired/objectCachePolicy.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts src/integrations/runtime/workspaceRuntimeConfig.test.ts src/integrations/runtime/client.runtimeOrigin.test.ts`.

Here and below `$ORCH` is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`.

## Line audit findings beyond the defect

| Area | Actual implementation and evidence |
| --- | --- |
| One immutable selection, no fallback | Proxy `:59-85,183-195` reads each discovery/credential/catalog file once per acquisition, validates selected Astrid identity and real realm root, restricts the endpoint, then freezes hostname/port/token/imported Node `requestHttp` and identity scalars. Bound dispatch at `:291-292` uses only that captured connection. `currentRuntime` occurs solely in the ordinary branch at `:402-408`. Missing/unknown/expired bound handles refuse at `:345-350`; there is no rediscovery/retry path. Snapshot reads are not an atomic multi-file transaction. |
| Retirement ordering | Registry `:163-170,183-185` marks retired and removes the entry before invoking resource cancellation. POST `:364-380` retires before content-type refusal, body await, schema checks, capacity/snapshot selection and their failures. Disposal `:447-450` retires before server close and destroys pending controls. Original body-await, failed-selection, stream/upload/late-ACK and restart tests pass. |
| Actual dispatch and response fences | `:267-292` registers cancellation and performs its active assertion synchronously immediately before the captured Node request, with no await or caller-supplied transport in between. Header `:295`, chunk `:300`, drain `:303` and end `:305` checks fence response publication; retirement unpipes/destroys upstream work and destroys an already-started downstream reply. Control completion/disposal fences are at `:377-384`. Auth/403/5xx/I/O retire; 409/422 preserve semantic responses (`:297,307-319`). |
| Bounds and cleanup | Registry cap/idle arming `:172-201` has 128 slots, no active eviction and no idle expiry while resources are tracked. Dispatch owns connect/upstream-idle/downstream-idle timers at `:285,310-319`; completion releases at `:271-282`. Control input is capped at 1024 bytes and connect-timeout duration (`:225-251`); incomplete/aborted/disposed bodies cannot acquire. The new stopped-reader probe fills buffers with **8,126,464 bytes**, then observes **410 and upstream response close** with a 200ms idle limit. A separate new abort/timeout probe retires the predecessor and proves all 128 slots remain available afterwards. These pass. |
| Exact admission and targets | `:111-145,334-368` uses raw header occurrences, exact configured Origin and hop-specific Host, rejects duplicate/foreign/null origins and duplicate/malformed handles, and permits absent Origin only for GET/HEAD with exact same-origin Fetch Metadata. Control method/body and bound method sets are explicit. Targets are origin-form `/v1/…`; literal/encoded traversal, separators, absolute targets and malformed escapes in the path refuse. No `/v1` control route or CORS allowance is introduced. Existing pure/socket refusals and positive safe-read tests pass. |
| Prefix, routing and startup credentials | Vite config `:91-96,125-146` installs the literal `/runtime-config/v1/operation` rule and admission plugin on existing dev/preview listeners. `runtimeProxy.ts:32-54` has no rewrite, startup bearer or immutable-cache override. Plugin `:58-70` rejects malformed descendants/handle-bearing alternative paths before the catch-all. Launcher `:590,603,711-714` supplies the exact local App origin to both processes and keeps the existing proxy destination; only four launcher lines change. The literal control/data prefix agrees with the browser host's separately documented shape. No gateway rewrite/fallback is added. |
| Headers, payload and errors | Discovery proxy `:210-222,286-305` strips browser credentials/cookies/handle/Host/hop headers and received nominations, adds only its pinned bearer, restricts response headers, suppresses Set-Cookie/Location and uses no-store. Vite emits a fixed no-store error (`runtimeProxy.ts:39-44`); operation paths serialize no caught exception or credential. Bound payload is piped unchanged, with original method/path/query/key, and upstream redirects are never followed. The end-to-end nomination defect above is the exception. |
| Ordinary behavior/Main | Ordinary forwarding `:388-444` retains per-request discovery, payload piping and object-cache policy; `currentRuntime`, chat, cache policy and client implementation are unchanged from the base. Launcher selection, chat rename/Main and ordinary Range/ETag/flowing-stream/client identity controls remain passing in the exact-tree 136-test lane. No passing behavior test was rewritten, weakened, skipped or removed. |

## Verification executed by this review

Direct pure-only run on byte-exact source extracted into this worker's notes (no listeners):

```sh
node --test --experimental-test-isolation=none --test-name-pattern='^pure:' "$ORCH/workers/app-m2-proxy-server-independent-review/notes/source/scripts/runtime-discovery-proxy-operation.test.mjs"
```

**Exit 0: 6 pass, 0 fail/skipped/cancelled.** [Log](../workers/app-m2-proxy-server-independent-review/notes/pure.log).

Added exactly one authorized named central suite, `proxy-server-independent-adversarial-integration`, in `tests/suites.conf`. No duplicate original suite, full suite or local socket run was made. Exact requests:

```sh
$ORCH/bin/request-test app-m2-proxy-operation-server proxy-server-independent-adversarial-integration
$ORCH/bin/wait-test app-m2-proxy-operation-server-proxy-server-independent-adversarial-integration-1020104043-22430 0
```

The first nonblocking wait returned 124 while queued; the second returned **1** with the completed result. Executed central command:

```sh
node --test /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-proxy-server-independent-review/notes/proxy-server-independent.test.mjs
```

**2 pass, 1 fail, 0 skipped/cancelled**, 2s service wall time, exact final `e53e49…` product tree. [Summary](../tests/app-m2-proxy-operation-server-proxy-server-independent-adversarial-integration-1020104043-22430/summary), [full log](../tests/app-m2-proxy-operation-server-proxy-server-independent-adversarial-integration-1020104043-22430/log.txt), [snapshot identity](../tests/app-m2-proxy-operation-server-proxy-server-independent-adversarial-integration-1020104043-22430/snap). The failed assertion remains a positive stripping requirement; it was not changed to accept the leak.

Other exact read-only checks, exit 0: `node --check "$ORCH/workers/app-m2-proxy-server-independent-review/notes/proxy-server-independent.test.mjs"`; `git diff --check`; `git status --porcelain=v1 --untracked-files=all` (empty); `git diff --exit-code 35dbb0eb1 a81e8ddd3 -- config/vite/objectCachePolicy.mjs config/vite/astridProxySecurity.ts scripts/astrid-project-chat.ts scripts/astrid-project-chat-runtime.test.ts src/integrations/runtime/client.ts` (empty).

## Limits and next step

The approved two-process limit remains honest: browser retirement cannot precede delivery of its HTTP retirement notification at the server; previously dispatched work can accept and retirement is not rollback. A pinned hostname/port/bearer is not an absolute Runtime-instance acceptance precondition and cannot synchronously detect silent credential revocation or port reuse. Browser negotiation/expected-instance checks, native capture, same-store requester/outbox composition, actual Runtime receipt acceptance/exact retry/restart/undo and a frozen supported tuple remain separate activation gates. Fixture ACKs and this transport review do not close them. Hosted/paired transport stays unsupported.

No full/build/browser/tsc/install/external-network run; no product edit, direct socket run, shared dependency/cache/venv mutation, branch/ref change, commit/merge/rebase/checkout/push. This review's new Vite cache is fixture-local and removed by cleanup. No worktree build output/temp files or KEEP remain.

Next: repair the Vite nomination boundary with the narrow existing handler change, carry the regression into the normal operation test file, and centrally qualify the repaired exact snapshot before changing this **HOLD** to APPROVE. Independently finish the browser and later cross-product activation gates. No additional protocol decision is required by this finding.
