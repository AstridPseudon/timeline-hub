# Runtime connector lifetime — bounded direct-client contract

2026-10-20; rt-m2-connector-lifetime. PLAN and all four App requester fence/host reviews read. **Handwritten Runtime wrapper implemented; default browser automatic requester remains unsupported/inactive.** No wire/OpenAPI/generated-client change.

**Where the lifetime lives today.** Runtime `packages/typescript/src/generated.ts:73` captures base/token/optional Transport but has no retirement. App `src/integrations/runtime/client.ts:245,388,417,424,506` caches negotiation and awaits session/health without an operation dispatch lifetime. Contrary to the task's source-location hint, `git grep` finds no discovery proxy/launch scripts in Runtime: `scripts/runtime-discovery-proxy.mjs`, `dev-local-workspace.mjs`, and `astrid-project-chat.ts` are App-owned. App proxy `currentRuntime` reads endpoint/token on every dispatch and replaces Authorization. A Runtime-only browser adapter cannot bind those hidden selections honestly.

**Exact API, exported from `@astrid/runtime-client`.** In handwritten `src/operation-handle.ts`:
```ts
interface OperationIdentity { actorId: string; realmId: string }
interface OperationConnection { baseUrl: string; token: string }
class OperationHost {
  bind(connection: OperationConnection): OperationHandle;
  dispose(): void;
}
class OperationHandle {
  constructor(connection: OperationConnection);
  readonly client: WorkspaceClient;
  negotiate(name: string, version: string, scopes: string[]): Promise<OperationIdentity>;
  readonly getRecoverableIdentity: () => Promise<OperationIdentity>;
  readonly isCurrentIdentity: (expected: OperationIdentity) => boolean;
  readonly retire: () => void;
}
class OperationRetiredError extends Error {}
```

**Who calls what.** A DIRECT credential-owning connector creates one host and calls `bind` before selecting a base/credential/transport or reconnecting; this synchronously retires its previous handle, even if constructing the replacement fails. Owner cleanup calls `dispose` (terminal). It negotiates each handle exactly once; renegotiation requires a new binding. App adapters, when a supported owner exists, must close recovery, task admission/get, managed/object/media reads and transmit over that SAME `handle.client`, and supply the handle's bound identity callback. Separate caller checks still enforce App schema/product-role/expected-instance policies. Native capture must remain under the same owner and is not supplied here.

**Fence.** Each handle captures scalar base/token and the fetch function once. Its generated WorkspaceClient always calls a handwritten guarded Transport: synchronous active assertion immediately before dispatch, then assertions after fetch and body awaits. Ambient cookies are omitted and redirects refused. Retire is irreversible; old negotiation/ACK completion cannot revive it. Failed negotiation, fetch/body errors, 401/403 or 5xx retire the handle. Semantic 409 remains the normal generated ApiError. Identity becomes available only after health/handshake/realm agree and requested scopes are granted; returned/public handshake snapshots cannot authorize or revive a retired handle. An already dispatched request may still be accepted remotely: preserve uncertain exact request bytes/key and retry with a NEW negotiated handle. Equal actor/realm renewal is allowed; the wrapper adds no generation to Runtime idempotency scope and never changes request bytes/key.

**Honest boundary and handoff.** This is a local owned lifetime, not synchronous knowledge of remote revocation/restart. The dispatch function must itself dispatch directly; an async or credential-reselecting proxy/fetch adapter is unsupported. No token is exposed to the browser, proxy is changed, or production caller is activated. Runtime remains final per-request/receipt authority. Generated files remain generator output byte-for-byte. The only cross-owner contract is the local typed handle above. Making the current hidden-credential browser proxy support it would require its App owner to establish a real pinned lifetime/dispatch binding; this task proposes no endpoint, auth service, journal or protocol field. Keep the existing missing-port refusal until that distinct path is designed and qualified.

**Evidence.** `packages/typescript/test/operation-handle.test.mjs`: 16 in-process node:test cases cover fixed connection across negotiation/task/read/transmit, stale-after-await dispatch, base/credential/transport/reconnect/dispose retirement, late negotiation/ACK, equal-identity exact retry, received auth/unavailable/disconnect retirement, fail-closed negotiation, and preserved semantic conflict. Receipt is an opaque transport fixture; real Runtime acceptance/replay and App/native/browser composition are not qualified. Public package declarations compile. Central `ts-client-check` result is recorded in the worker report.
