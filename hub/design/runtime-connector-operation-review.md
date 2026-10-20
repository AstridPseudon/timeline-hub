# REJECT — Runtime connector operation lifetime

Reviewed **e8c3e926219f7a35839996bf79b8790b762857c6** (`tl/rt-m2-connector-lifetime`) against **6023cfb10307b4c0004642b5fa1995d72ba4f6d1**, 2026-10-20. The four changed files are `packages/typescript/src/index.ts`, `src/operation-handle.ts`, `test/operation-handle.test.mjs`, and `test/public-api.mts`. **Do not approve this source yet:** public handshake state can become identity authority during negotiation, and malformed negotiation fields are accepted. There is also a required source-level restriction for fetch wrappers that defer upstream dispatch. These are local wrapper findings, not claims of server authorization bypass or real receipt acceptance.

PLAN, the 09:19Z orchestrator redirect, `design/runtime-connector-lifetime.md`, the implementation worker report/log, App's real-host-binding audit, final-boundary repair, synchronous-fence review and preceding independent-fence review were read. No settled decision was changed. The direct credential-owner boundary is appropriate; browser automatic requester activation remains unsupported.

## Concrete findings

**1. P1 — A public mutable handshake snapshot can establish a different actor and add an ungranted scope.**

Candidate `operation-handle.ts:81–91` retains the result of generated `WorkspaceClient.handshake`, awaits `getRealm`, then validates and adopts that result. Generated `generated.ts:126` stores the *same object* in public mutable `client.handshakeInfo`. During the realm wait, a consumer of that public snapshot can change `actor_id` and mutate `scopes`; the wrapper then treats those changes as authenticated negotiation data.

Executed counterexample: the handshake returns actor `authenticated-actor`, realm `realm`, and **no granted scopes**, while `negotiate` requests `projects:write`. Hold the realm response, set `handle.client.handshakeInfo.actor_id = "forged-actor"`, push `projects:write` into its scopes, and release the realm response. Negotiation **succeeds** with `{actorId:"forged-actor",realmId:"realm"}` and `isCurrentIdentity` returns **true** for that forged identity. The expected fail-closed assertion fails. The inherited test mutates the public snapshot only *after* negotiation, so it misses this interval.

This is a supported public-property aliasing error; it does not require modifying private fields or replacing client methods. It contradicts the stated rule that public handshake snapshots cannot authorize a lifetime. Preserve the authenticated parsed values independently of public mutable snapshots throughout negotiation, including the realm await, and add the counterexample to the existing suite. No new endpoint, auth service or journal is needed.

**2. P2 — Negotiation validation accepts hostile field types instead of failing closed.**

At `operation-handle.ts:84–88`, `handshake.scopes.includes(scope)` is used without an array/type check. A response with `scopes: "not-projects:write-granted"` satisfies a request for `projects:write` by **substring matching**, and negotiation succeeds. Separately, health and handshake with `schema_digest: 42` also succeed: the code checks truthiness and equality, not the required string type. Both fail-closed assertions fail in execution. Generated JSON parsing performs a TypeScript cast, not runtime validation (`generated.ts:91`), so its declared DTO types do not protect this boundary.

Validate the negotiation fields actually used for authority and compatibility before adopting them: nonempty strings for identifiers/digests and an array of strings for scopes, with exact scope membership. Keep product actor-role, supported-schema and expected-instance policies in the caller as already designed; this finding does **not** ask the wrapper to acquire those policies or expand its API. Missing scopes with a nonempty request already reject and retire correctly; that passing control does not cover the string case.

**3. P2 — Explicitly restrict the captured global fetch to immediate direct dispatch in the exported source contract.**

`operation-handle.ts:21` excludes credential-reselecting proxies, but `:31–38` captures *whatever* function is currently installed as `globalThis.fetch`. There is no custom-fetch argument. Capturing a function reference cannot fence an upstream request that this function defers internally. An executed diagnostic installs a wrapper that waits before forwarding `/v1/tasks/task`, binds and negotiates the handle, starts the read, retires the handle during the wrapper wait, then releases it. The underlying direct fixture is called **after retirement**; only the response is refused with `OperationRetiredError`.

The design document already excludes such adapters, so this is a demonstrated unsupported-path boundary and a source-contract omission, not a failure of the intended native/direct case. Add an explicit exported-source restriction that captured fetch must forward immediately with the supplied fixed target/credential/options; wrappers that await before forwarding and hidden credential/upstream proxies cannot qualify this fence. Keep the browser path inactive. Do not attempt to infer arbitrary function behavior or introduce a protocol to fix it in this patch.

## Verified working boundaries and limits

| Boundary | Verified behavior |
| --- | --- |
| One generated client and actual dispatch | Constructor captures scalar base/token and one fetch function. The generated client builds Authorization from the captured token and routes health, handshake, realm, task, object/managed reads and commit through the same guarded Transport. No extra transport await precedes the guarded call to the captured function. Mutating the input connection or replacing global fetch later does not reselect them. |
| Bind, reconnect, dispose | `OperationHost.bind` retires its previous handle before replacement construction, including failed construction and equal actor/realm renewal. `dispose` is terminal. Old callbacks close over the retired instance. `isCurrentIdentity` remains false until negotiation succeeds and after retirement; returned identity copies cannot revive it. |
| Async continuations | Transport asserts before each dispatch, after fetch resolves, and after response-body await. Each later generated request re-enters this guard. A separate promise-propagation control retires after handshake completion but before `open` resumes: no realm dispatch occurs. Late negotiation/ACK cases in the inherited suite refuse. Failure catches retire irreversibly. These facts do not turn the public handshake alias above into safe negotiation data. |
| Received failures | 401, 403, all statuses >=500, network failure and body-read failure retire in source. The inherited executions cover 401/403/503/disconnect. A fatal HTTP response is retired before body consumption, so a retired-lifetime error can replace its generated ApiError; original status preservation is not promised. A semantic 409 keeps the binding active and retains the generated ApiError. |
| Recovery | `getRecoverableIdentity` requires a negotiated promise and checks retirement before and after awaiting it. Successful private identity is a local owned-lifetime observation, not proof of arbitrary remote revocation. Public post-negotiation handshake mutation does not change that private identity. Finding 1 concerns its initial establishment. |
| Request retry | The inherited equal-identity/new-token case preserves both commit bodies and original idempotency key. No lifetime generation is sent. Generated `commitTimeline` serialization is unchanged. Runtime's unchanged `timeline_commit_store.py:32–40` hashes operation/path/publisher/body and scopes by project/timeline; `server.py:306` derives publisher from authenticated actor. No token or new local lifetime enters that identity. Actual accepted receipt replay was **not run**. |
| Cookie, redirect and proxy policy | This new opt-in direct wrapper supplies `credentials:"omit"` and `redirect:"error"`. The existing generated default fetch, door, App proxy and production callers are unchanged. Thus no existing browser policy is relaxed or activated; the new wrapper's explicit options are stricter than the generated default's implicit fetch defaults. The hidden-token App proxy still reselects upstream/token per request and replaces Authorization; neither a nonempty browser token nor this wrapper repairs that path. |

The public API remains small, with no wire/generated contract changes. The exported `client` is available before negotiation; a supported owner must negotiate and use the same handle plus its live callback as the design requires. No additional pre-negotiation dispatch requirement is invented by this review. App/native capture and policy checks are separate dependencies.

## Exact verification

All candidate sources/tests were read with `git show` and copied byte-for-byte into this worker's private notes package. The review worktree stayed at base `6023cfb` with empty status. `notes/source-audit.json` verifies all ten copied package files and records the candidate tree **0cf1f22c479a4b3269577f84bd9fd496cbf445db**.

Commands below use:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-review-connector-operation
```

- `node /home/user/work/app/node_modules/typescript/bin/tsc -p "$W/notes/client/tsconfig.json"` — **exit 0**. Compiled only the private immutable copy; shared TypeScript read-only.
- `node /home/user/work/app/node_modules/typescript/bin/tsc --noEmit --strict --module NodeNext --target ES2022 "$W/notes/client/test/public-api.mts"` — **exit 0**.
- `node "$W/notes/client/test/operation-handle.test.mjs" > "$W/notes/inherited-targeted-direct.log" 2>&1` — **exit 0; 16 passed / 0 failed / 0 skipped**.
- `node "$W/notes/review-probes.test.mjs" > "$W/notes/review-probes-final.log" 2>&1` — **exit 1; 3 failed safety expectations / 3 passed controls and diagnostics / 0 skipped**. Failures are the public-handshake alias, scope string, and numeric digest. The delayed-fetch diagnostic passes by asserting the observed unsupported stale upstream call. Other controls prove handshake promise-propagation retirement and absent-scope refusal.
- `git diff --exit-code 6023cfb e8c3e926219f7a35839996bf79b8790b762857c6 -- packages/typescript/src/generated.ts runtime_protocol/door.py runtime_protocol/timeline_commit_store.py` — **exit 0, unchanged**.
- `git status --porcelain=v1 --untracked-files=all` — **exit 0, empty**; source audit also checks this.

The first `node --test` invocations returned only file-level results in this environment: inherited fixture file exit 0, review probe file exit 1. Direct `node` executions above expose all individual cases; the final detailed logs are authoritative. Initial direct probes also had the same three failures; the final rerun only added the explicit forged-identity diagnostic. No safety assertion was weakened.

**Reused central evidence, not a new run:** `request-test rt-m2-connector-lifetime ts-client-check`, result `rt-m2-connector-lifetime-ts-client-check-1020092823-5847`; service command `cd packages/typescript && PATH=/home/user/work/app/node_modules/typescript/bin:$PATH npm test` — **33 passed / 0 failed / 0 skipped, exit 0**, including build/public API declarations. Its `snap` and `summary` name the exact candidate tree above. The green result is valid but lacks the failing adversarial cases. No full suite or new central request was run.

All executions used in-process local transport fixtures, no browser/server/listen/socket. ACKs are opaque fixtures, not Runtime receipts. Real Runtime acceptance/replay, supported cross-product pair, native capture, browser activation/durability and macOS were **not verified**. No repo, integration worktree, dependency, venv, shared cache, ref or branch was modified. Private compiler output was removed after verification; retained notes contain reproducible sources and logs.

**Next step:** keep the direct API shape, repair findings 1–2 with permanent tests and make finding 3's limitation explicit in exported source, then independently review the exact successor and run its targeted client checks. Do not activate automatic placement or add auth/wire/journal machinery on this evidence. No external blocker prevents this completed review; the rejection is actionable source feedback.

Artifacts: [private immutable candidate source](../workers/rt-m2-review-connector-operation/notes/client/src/operation-handle.ts), [review probes](../workers/rt-m2-review-connector-operation/notes/review-probes.test.mjs), [detailed failing log](../workers/rt-m2-review-connector-operation/notes/review-probes-final.log), [inherited passing log](../workers/rt-m2-review-connector-operation/notes/inherited-targeted-direct.log), [source audit](../workers/rt-m2-review-connector-operation/notes/source-audit.json).
