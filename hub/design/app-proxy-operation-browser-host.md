# Inactive same-origin browser operation owner

Worker: `app-m2-proxy-operation-browser-host`. Base: `35dbb0eb12d75dc2c1becf7a9d8ac914758c05c7`. PLAN, proposal, Runtime ACK 10:11, independent proposal review, owner INBOX 10:02 and reviewed successor negotiation lessons were read before implementation. No settled decision was changed.

Implemented `src/integrations/runtime/operationHost.ts`; no production caller imports it. The only existing product edit is a pure extraction of `decodeAcceptedTimelineCommit` inside `dataProvider.ts`. The provider still owns its state/cache update and uses the same decoder. No second provider/client, generated change, root pin, outbox edit, proxy/config edit or activation.

## Local API and exact surface

`new RuntimeOperationHost(fetchImpl?)` captures the browser fetch primitive once; there is no bearer constructor. The supplied fetch must dispatch immediately using the supplied target/options; delayed forwarding wrappers and hidden target/credential reselection are unsupported. `bind()`/`reconnect()` synchronously retire the predecessor before their first await; `dispose()` is synchronous and terminal. A successful bind returns a frozen, binding-specific callback object:

- `retire()`, `getRecoverableIdentity()`, synchronous boolean `isCurrentIdentity({actorId, realmId})`;
- private-client `admitTask`, `getTask`, `listManagedOutputs`, `getManagedOutput`, `getProjectMediaSelection`, `getObject`, `headObject` with existing client signatures;
- `transmit(scope: OutboxScope, saved: OutboxRequest)` returns the existing validated `TimelineCommitResult`, rejecting typed semantic errors for the existing failure classifier. Lifetime/auth/connector failures reject without a permanent-refusal status, preserving the unknown-outcome lane.

No session, generated client, mutable handshake, object-content URL, playback cache or direct credential is exposed. Callbacks close over their own binding; old callbacks never follow the host's replacement.

Controls are exactly `POST /runtime-config/v1/operation` with `{}` and optional predecessor `X-Astrid-Operation-Handle`, and best-effort `DELETE` on that path with the retiring handle. Bound requests use `/runtime-config/v1/operation/runtime` plus the original generated `/v1/...` path/query. All fetches use no-store, same-origin mode, omitted credentials, error redirects and an AbortSignal. Cleanup uses a separate signal because retirement has already aborted data requests. Late acquisitions only receive cleanup; they cannot install identity or a replacement client.

The expected policy comes from existing `initializeWorkspaceRuntimeIdentity()` (workspace-config/build launch seam), copied privately and retained across rebind. Fresh acquire metadata is checked against it and never supplies its own expectation. Hosted origin is refused before acquisition. Missing launch identity, including the unbound paired observation path, is refused before acquisition rather than substituting `connected` or acquire metadata. A future path needing observed-only or hosted ownership requires an explicit supported policy/transport seam; this unit does not invent one.

The guarded Transport captures and validates health/handshake/realm bytes immediately after body consumption and before returning bytes to the generated client. It checks actual types, protocol, accepted schema digests and equality, exact all-string scope array, targeted capability, forbidden product actors, expected actor/realm/instance and realm agreement. Only private scalar identity/digest copies survive awaits. Public `handshakeInfo`/cached sessions are not authority. The existing client's compatibility and pre-write instance checks remain; exact raw transmission adds the same instance read through the bound transport. Saved scope/request scalars are copied before awaiting; original UTF-8 body and idempotency key are transmitted without reserialization.

Browser retirement aborts the owned controller, clears negotiated identity immediately and blocks fetch/post-fetch/body/result continuations. Binding is never revived. Acquiring/retired bindings cannot supply a true identity callback. `isCurrentIdentity` proves only this local negotiated lifetime; remote silent invalidation/expiry/revocation is not synchronously observable. Browser and server retirement remain two ordered HTTP processes; already handed-off requests may be accepted, and late responses under a retired owner are ignored. Requester claim, authorization, native capture and in-storage mutation fences remain independently necessary.

## Size and qualification

Product footprint: **259 new lines** in the owner plus **32 added / 20 removed lines** in the existing provider (net **271 product lines**). Direct permanent owner tests: **353 lines / 59 cases**, including 42 negotiation propagation intervals inside the microtask-loop cases. No alternate acceptance model or new package was added.

Final targeted command (read-only `/tmp/app-m2-coherent-deps8/node_modules`, linked only from this worker's own node_modules):

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/runtime/operationHost.test.ts src/integrations/runtime/timelineCommit.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts src/integrations/runtime/client.runtimeOrigin.test.ts src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/dataProvider.parity.test.ts src/integrations/runtime/workspaceRuntimeConfig.test.ts
```

Result: **8 files / 244 tests passed**, exit 0, Vitest 4.1.5, 12.49 seconds. Real handwritten/generated clients are exercised using in-process fetch bytes; the page launch-policy seam is mocked in owner tests. Existing config tests run unchanged alongside them. Owner tests cover fetch/body waits, policy/acquisition waits, cleanup after A/B/disposal, public handshake mutation at assignment and during realm await, malformed types/grants, copied identity, pre-write health retirement, late ACK/equal-identity exact retry, absent managed-output pages, malformed acceptance, scope refusal and hosted refusal. They do not claim that fixture receipts were actually accepted by Runtime.

```sh
node node_modules/eslint/bin/eslint.js src/integrations/runtime/operationHost.ts src/integrations/runtime/operationHost.test.ts src/integrations/runtime/dataProvider.ts --max-warnings 0
git diff --check
```

Both exit 0. No full suite, build, project TypeScript check, dependency installation, sockets or browser runs were performed. Shared dependencies/caches were not written. Existing positive client/session/provider/commit tests remain unchanged. Chat/proxy behavior was not modified or independently qualified here.

Open before activation: compose the separately owned proxy/config implementation; central real-proxy/socket origin/Host/header/expiry/ordering tests; requester/outbox/storage/native capture composition; real Runtime exact acceptance/receipt replay and restart recovery on the frozen current tuple; actual browser qualification. Keep the automatic requester inactive until those gates pass. No implementation blocker remains within this browser-only assignment.
