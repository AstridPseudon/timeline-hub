# App proxy operation lifetime proposal review

2026-10-20; worker `app-m2-proxy-lifetime-proposal-review`.

**Verdict: HOLD implementation and activation pending Runtime/orchestrator agreement on escalation `app-20261020T1002Z-proxy-operation-local-contract.md`. The proposed same-origin-only shape is technically sound within its explicitly stated local-lifetime boundary.** I found no architectural counterexample requiring a different transport, listener, Runtime `/v1` field, browser product credential or persisted lifetime. This is a design review, not qualification of an implementation. The 09:32 instruction explicitly requires agreement before building; no such agreement was present in the reviewed escalation/App INBOX. The rejected Runtime wrapper is not qualified evidence.

Read PLAN first, App INBOX 09:19/09:32/09:36/09:38, the exact pending [App proposal](app-proxy-operation-lifetime.md), [Runtime independent rejection](runtime-connector-operation-review.md), [Runtime direct-owner design](runtime-connector-lifetime.md), [real-host audit](app-requester-real-host-binding.md), and the 10:02 escalation. No settled decision was changed.

## Source checked

Assigned App HEAD is `667498cc49b4ec2b1ccd3a515eb87311c5126c93`, the prepared main refresh over integration `18becfbede00038830b97e63345445eeef54fa42`; local `origin/main` is `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa`. This is not the proposal worker's main-only baseline. Proxy, launcher, chat, connection, cache and bridge-origin helper paths compared below remain byte-identical to 44f; `client.ts` also contains existing integration additions. Requester source is not present in this assigned tree: I read its exact `a103f3ca2e8e66f2837a85c0ddd007962eca66ac` version using `git show`, not a moving checkout. No source was edited or upstream behavior restored/removed.

Runtime door source was read at the proposal's `642eef7467a6b766480df3f34e7377e8d755fe92` and compared to observed Runtime HEAD `c0dcd3871d78c405184506eb6735565592498c77`: `runtime_protocol/door.py` is unchanged. Rejected wrapper source was read at `e8c3e926219f7a35839996bf79b8790b762857c6`. No Runtime tree was modified.

## Findings and contract assessment

| Requirement | Finding |
| --- | --- |
| Pin negotiation, task, read and transmit | **Satisfied by the proposed design, unimplemented.** Current `scripts/runtime-discovery-proxy.mjs:46,58,120,129,131` reselects endpoint/token per request and independently rereads config. The replacement must capture scalar endpoint **and** bearer from one parsed selection, plus metadata, once per handle. The private injected `Transport` must carry health/handshake/realm, admit/get task, managed-output pagination, media selection, object reads if used, and raw exact commit. Pinning only one scalar or using a second client would fail. |
| No rediscovery fallback | **Dedicated prefix is necessary.** `O = /runtime-config/v1/operation`; `POST O`, `DELETE O`, and `O/runtime` + original `/v1/...` suffix can be consumed entirely by the existing App proxy. Missing/unknown/retired handles on the data prefix fail closed; never call `currentRuntime`, ordinary `/api/runtime`, reconnect or an automatic retry there. A header alone on the ordinary path would permit stripped-header fallback. Runtime receives the original method/path/query/body/key and the pinned bearer, never the handle. |
| Browser retirement before rebind, including failed acquisition | **Sufficient if old callbacks close over their binding.** Retire/detach old locally before any await, before constructing/replacing transport, and before requesting a new handle; failed replacement leaves old false. Server replacement retires the supplied predecessor before discovery/credential reads, even on snapshot failure/capacity refusal. Late acquire A after B/dispose may only be cleaned up, never installed. A facade whose old callback dynamically reads `host.current` would violate the contract. |
| Final dispatch and body fences | **Necessary and sufficient for the two owned boundaries.** Existing `client.ts:357,388,506` awaits session and pre-write health after requester entry checks. Browser active assertion must be immediately before the captured fetch invocation, after fetch/body awaits, and before publishing identity/results. Server active assertion must be immediately before `requestHttp`, after any preceding await, and in header/body forwarding callbacks; register/abort owned requests and streams. `incoming.pipe(upstream)` alone (`runtime-discovery-proxy.mjs:160`) is not a retirement fence. Failures retire irreversibly; 410 must retire locally before requester error classification can turn it into a permanent refusal. |
| Cached response / raw managed-fetch bypass | **Explicitly excluded by the proposal; preserve that exclusion.** All control/data fetches, not just create, require `cache:'no-store'`, `mode:'same-origin'`, `credentials:'omit'`, `redirect:'error'`, and owned cancellation. All bound replies, including errors, require no-store at every hop. Existing `objectCachePolicy.mjs:10` does not match the new prefix, as verified by a pure probe, but that is not itself a no-store implementation. Use private-client `listManagedOutputs/getProjectMediaSelection/getObject/headObject` (`client.ts:633,799,851,856`); never fetch a URL from `objectContentUrl` (`:860`), playback caches, a data provider's second client, or an arbitrary managed-output URL to establish requester authority. Ordinary playback keeps its existing immutable/Range/ETag policy. |
| Negotiation authority | **Proposal explicitly repairs the rejected pattern.** No public client/session/handshake object escapes. Validate actual nonempty string authority fields, string arrays with exact scope membership, supported digests, capability, actor role and realm agreement, and retain private scalar copies through every await. The generated `json<T>` is only a cast (`generated.ts:90`); private `AstridRuntimeClient` alone does not add every required runtime type check. Failed negotiation retires. No parallel negotiation/scopes framework or generated-client edit is needed. |
| Expected-instance / launch policy | **Must preserve the proposal's stated restriction.** `client.ts:465-482` checks the selected launch identity; `:339-354` checks the instance before writes. Do not set the sole expected identity from each fresh acquisition's returned metadata. Otherwise launch instance I1 can silently become I2 after reconnect merely because POST returned I2; negotiating against that self-selected expectation trivially passes. Retain the existing launch/observed instance fence and compare fresh selection against it. Equal actor/realm is retry scope, not restart permission. This is an implementation trap, not a request for a new Runtime acceptance precondition. |
| Outbox/claim/storage fences | **Remain independently required.** At requester `a103...:130-146,199-206,222-239,257-263`, authorization and claim checks run around callbacks and inside outbox mutations. A transport fence cannot replace them. Native capture is still separately missing and must be tied to the same owner before/after its await. No new generation/lease field belongs in the outbox. |
| Equal-actor/realm exact retry | **Compatible with the unchanged Runtime identity.** A new negotiated handle can send the original UTF-8 bytes and original Idempotency-Key for the original saved scope; old callbacks/ACKs remain retired. Do not call generated serialization with a parsed/rebuilt command or recapture approval/IDs. Runtime `timeline_commit_store.py:32-40` hashes operation/path/authenticated publisher/body and scopes by project/timeline; `server.py:306` supplies the authenticated actor. Stripping the local handle leaves that identity unchanged. Actual accepted receipt replay has not been exercised here. |

The accepted-response adapter remains required. `dataProvider.ts:369-371` constructs another client; instantiating it solely to decode a result would violate the one-client ownership. Its `commitTimeline` and `acceptedCommitResult` (`:678-695,734-770`) already reject previews, validate the canonical closure/receipt and avoid regressing known state on a late ACK. Extract only the reusable validation/decoding needed by raw exact transmission, preserving the corresponding tests and checks. Do not copy a second acceptance model or export its stateful provider cache as transport authority.

## Security details that must survive implementation

**Use exact configured admission, not the bridge helper by itself.** `config/vite/astridProxySecurity.ts:9-28` compares a parsed loopback origin's host to the received Host. Pure probes show it accepts an origin-shaped value with a path (`http://127.0.0.1:17335/not-an-origin`) and rejects the legitimate browser Origin when the downstream Host has changed to proxy port 17336. Therefore it is only a reusable sub-check. At Vite require the one configured App Origin and App Host; at the discovery proxy independently require that same App Origin and the configured **proxy** Host. Preserve Origin/Fetch Metadata across Vite's `changeOrigin`; do not replace Origin with a proxy origin or strip it as the historical bridge does. An omitted Origin is permitted only for GET/HEAD with `Sec-Fetch-Site: same-origin` plus exact Host; an explicit foreign/null/duplicate Origin always refuses. This follows proposal line 46 and does not require expanding existing bridge admission.

**The new Vite rule cannot reuse the ordinary authenticated forwarding rule.** `config/vite/vite.config.ts:88-95` installs `/api/runtime` plus the workspace-config path. `runtimeProxy.ts:24-25` rewrites the former and may inject a startup token. The new rule must forward only the agreed control/data prefix unchanged, with no static token injection or object-cache override, and reject unsupported descendants rather than reach the ordinary catch-all. The proxy must validate the suffix before building its fixed upstream request: origin-form `/v1/...` only, including refusal of encoded traversal/separators/absolute targets. Strip the handle, browser credential/cookie headers, Host and hop-by-hop headers, including Connection-nominated fields; only the pinned bearer reaches Runtime. Restrict response headers, suppress Set-Cookie and prevent secret-bearing exception/log serialization. Browser-side redirect refusal is necessary; do not add redirect-following upstream code.

The opaque handle is a local capability even though it is not the product bearer. The proposed 32-byte random value in a header, memory-only registry, no URLs/storage/telemetry, bounds and cleanup are appropriate. A finite control-body limit/time limit is sufficient; no configurable resource-management framework is needed. This does not defend against malicious same-origin script or arbitrary local processes; the proposal correctly excludes those threats.

**Hosted support remains absent.** Real `runtime_protocol/door.py:61-65,275-294,522-609` has a closed path/header classifier, exact Host/hosted Origin admission, per-request `_product_token`, and internal dispatch. It neither accepts this local prefix/header nor pins a handle's product credential. The same-origin App proxy cannot repair that path. Refuse unsupported absolute-door/paired transport before acquisition, keep hosted automatic requesting inactive, and do not add CORS/relay bypasses. Main's connection/auth/URL changes remain intact.

## Explicit synchronization limit and counterexample

No stronger invalidation guarantee is proved by this proposal or by the direct wrapper. A concrete allowed ordering is:

1. Browser binding A is live and invokes fetch for an exact commit using A's handle.
2. Before that HTTP request reaches the proxy, the browser rebinds, immediately retires A and sends DELETE/replacement.
3. The earlier commit reaches the proxy **before** DELETE/replacement; the server entry is still active, so it dispatches to A's fixed upstream/bearer. Runtime may accept it.
4. Server receives retirement, aborts owned work; the browser rejects/ignores A's result and retains the uncertain exact request for fresh-binding retry.

This is not a stale selection of B or a browser ACK. It disproves “no upstream invocation after browser retirement” across two processes, even if both flags and every body fence are implemented correctly. Proposal lines 65-72 explicitly admit this ordering. The enforceable properties are no browser invocation after **browser** retirement, no new upstream invocation after **server** retirement, fixed old authority for already-dispatched work, and no old-result consumption. Runtime/orchestrator must explicitly accept that boundary; if it requires the stronger ordering, **HOLD on correctness** and return that contradiction, rather than claiming HTTP abort or a browser cached flag solves it. No new journal, SSE stream or polling loop supplies that guarantee.

Similarly, silent external credential revocation/server expiry/port reuse cannot synchronously flip a browser boolean. Fixed endpoint+bearer prevents adopting a *newly discovered* host/credential, but does not create an expected-instance precondition at Runtime acceptance. The proposal states this honestly and preserves existing received-failure/instance checks. This review does not infer a stronger guarantee from them.

## Rejected Runtime wrapper

Read the exact rejected source and independent report; do not cite its historical 16/33 green tests as qualification. At `operation-handle.ts:81-91`, public `client.handshakeInfo` aliases the object retained through the realm await; mutation there can establish a forged actor/scope. At `:84-88`, string `scopes` can pass substring `.includes`, and equal numeric digests pass truthy equality. At `:31-38`, capturing global fetch cannot fence a wrapper which awaits internally before invoking its underlying transport. These findings remain material even though the proposal uses its small host/retire API pattern. A private client, type validation and scalar copies address the first two in the proposed App shape. The App proxy must own its real final Node dispatch; a captured browser function alone cannot qualify hidden work. A repaired direct wrapper is a separate Runtime deliverable and is not a dependency to import into the browser.

## Smallest necessary patch and optional parts to leave out

Implement only after the agreement below:

- `scripts/runtime-discovery-proxy.mjs` and its existing `.d.mts`: one validated snapshot helper, small memory-only registry, exact local control/data routing, retirement and tracked request/stream cleanup, final dispatch fences. Leave ordinary `currentRuntime` forwarding semantics alone.
- `scripts/dev-local-workspace.mjs`: pass exact admission origins/hosts and retire entries on owned-service shutdown. Keep its existing local/hosted selection and server-only credential handling.
- `config/vite/vite.config.ts` / `runtimeProxy.ts`: dedicated no-token routing/admission at the existing listener. Reuse helpers only where their semantics actually fit.
- One small handwritten browser owner/handle module in `src/integrations/runtime`, using the existing injected Transport and private identity store; narrow task/read/recovery/transmit callbacks. Small extraction of the existing accepted-result decoder if needed. Hook activation/native capture is a later qualified unit.
- Adjacent meaningful tests in the normal proxy/client/requester suites; listening/browser lanes only via central service on the final tree.

The 128-entry/60-second idle numbers are policy choices for owner agreement, not new protocol semantics. A cap plus bounded abandoned-handle cleanup is necessary; configurable lease classes, keepalive channels, persisted registries, generations, renewal APIs, LRU/eviction frameworks or a second session manager are not. Keep one idle policy with no expiry during a flowing request and the existing connection/idle timeouts. POST's returned selection metadata is useful for policy comparison but never authentication authority. No chat change is required: `scripts/astrid-project-chat.ts:45-77` intentionally reselects discovery between registry calls and preserves explicit endpoint/token fallback. Preserve main's rename/Main selection and all existing positive ordinary/chat recovery tests. No generated/OpenAPI/client pin, outbox schema, producer, gateway, listener, browser secret or `/v1` wire change is necessary.

## Remaining agreement and next step

Runtime/orchestrator should ACK or correct, in the existing 10:02 escalation:

1. The exact same-origin-only `O` control/data prefix, `X-Astrid-Operation-Handle`, status/error shape and stripping before unchanged Runtime `/v1` dispatch.
2. Immutable endpoint+bearer per entry; retire-before-reselection even on failed acquire; no fallback; equal actor/realm exact retry without changing Runtime idempotency identity or launch-instance policy.
3. The two-process synchronization limit above and the distinction between a locally live binding and arbitrary unobservable remote revocation.
4. Hosted door/paired automatic requesting remains unsupported; any later door implementation is Runtime-owned and separately reviewed.
5. Simple cap/idle cleanup and the concrete stale-acquire/negotiation/dispatch/body/storage/ACK tests in proposal lines 101-112.

After agreement, implement that bounded unit on the refreshed integration, add the adversarial controls above and run adjacent main-suite tests. Require the real Vite→proxy→Runtime chain through the central service before calling it supported. Automatic activation still needs the approved native capture/producer, same-store requester composition and frozen supported tuple with real admission, lost ACK/restart/exact retry, reload/undo/redo and zero legacy traffic. No connector-only fixture can close those requirements. This review task itself is complete, not blocked; downstream work is held for the existing agreement.

## Executed verification and limits

Only pure in-process diagnostics of **existing production helpers** were executed. Source and log are under [worker notes](../workers/app-m2-proxy-lifetime-proposal-review/notes/proxy-contract-probes.test.mjs). They implement no operation registry, transport or fake acceptance engine; importing the proxy module does not run its `isMain` listener. Synthetic file fixtures were created inside this worker's notes and removed by `finally`.

Exact test command from `/home/user/work/wt/app-m2-proxy-lifetime-proposal-review`:

```sh
node --experimental-strip-types /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-proxy-lifetime-proposal-review/notes/proxy-contract-probes.test.mjs > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-proxy-lifetime-proposal-review/notes/proxy-contract-probes.log 2>&1
```

**Exit 0: 6 passed, 0 failed/skipped/cancelled/todo.** Three diagnostics demonstrate hidden credential/upstream changes and independently read snapshot mismatch; one preserves ordinary immutable caching while showing the new prefix does not match it; two establish the bridge helper's actual admission limits. These are observations of current code, not passing tests of the unimplemented contract. Historical App 202-test and Runtime 16/33-test results were read, not rerun or adopted as qualification.

Read-only verification, all exit 0, output empty:

```sh
git diff --exit-code 44f0b9ca9d0247d909f86f56955a04ef6c18a2aa HEAD -- scripts/runtime-discovery-proxy.mjs scripts/dev-local-workspace.mjs scripts/astrid-project-chat.ts config/vite/runtimeProxy.ts config/vite/astridProxySecurity.ts src/integrations/runtime/connection.ts
git -C /home/user/work/runtime diff --exit-code 642eef7467a6b766480df3f34e7377e8d755fe92 c0dcd3871d78c405184506eb6735565592498c77 -- runtime_protocol/door.py
git diff --check
git diff --exit-code 667498cc49b4ec2b1ccd3a515eb87311c5126c93
git status --porcelain=v1 --untracked-files=all
```

No product/main-suite implementation tests, full/central suite, build, tsc, install, browser, server/listener/socket, native capture or actual receipt acceptance/replay was run. No dependencies, symlinks, caches, venvs, refs or branches were changed. No git commit/merge/rebase/checkout/push. No build output/temp files were left in the worktree; all deliverables are this requested report and the assigned worker directory. No KEEP is needed.
