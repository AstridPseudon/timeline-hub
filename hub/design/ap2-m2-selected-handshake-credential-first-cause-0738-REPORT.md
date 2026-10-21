# AP2 M2 selected8082 first-cause report: Runtime handshake credential

## Verdict

The first selected8082 failure is a wrong Runtime selection at the Agent
launcher boundary, not a malformed credential, wrong token production, wrong
realm/actor grant, or Runtime verifier defect.

The selected fixture mints a valid `astrid-selected-param` credential for the
harness Runtime, writes it in the shape Agent accepts, and passes the file path
as `ASTRID_RUNTIME_CREDENTIAL`. However, its child environment also inherits
the owned runner's `ASTRID_RUNTIME_DATA_ROOT` and does not provide the four
case-local `ASTRID_TIMELINE_EVAL_*` fields used by the normal App admission
path. Agent 6ef therefore falls through to `ensure_runtime()` and selects the
runner workspace. It presents the harness Runtime's credential to that other
Runtime, which correctly returns `invalid bearer credential`.

This is the exact cause supported by source contracts and the first failure
stack. No actual/replay/retry was run and no product source was changed.

## Exact cohort and first failure

- App source: `ba02c8f246ec61cd65d178a1ada686788df3`, tree
  `7fe8c15b56da9944ae31e8273d41d3ceb21b3677`.
- Agent source: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Runtime source: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Owned runner: `run-owned-selected-final95.sh`, SHA-256
  `dcda1b820fa2feb68db6ae99b56cdc8cd4277016c3eaf939a5ded423c9b25ee0`.
- Central result: selected8082, one test collected.
- First failure: `tests/e2e/local/three-products.selected-param-dev.spec.ts:39`
  -> `harness.ts:589` -> `seedSelectedParamDev()` at `harness.ts:650`
  -> Agent `project-pack init` -> handshake, with Runtime's
  `unauthorized: invalid bearer credential`.

The original 18585 cause remains UNKNOWN; this report does not reinterpret it.

## Credential production and exact value contract

The selected harness path is explicit and internally consistent:

1. `tests/e2e/local/support/harness.ts:562-571` generates the selected actor's
   token in Node memory, POSTs it to the current harness `this.runtimeUrl`
   `/v1/credentials` route with the owner credential, then writes
   `{token, actor_id}` to the selected credential file with mode `0600`.
2. `harness.ts:39-42` sets `ASTRID_RUNTIME_CREDENTIAL` to that file path, not
   the bearer value.
3. `harness.ts:641-650` builds `selectedParamEnv`, preserving inherited
   `process.env`, setting `ASTRID_RUNTIME_ENDPOINT` to `this.runtimeUrl`, and
   setting the project-pack paths. It does **not** set
   `ASTRID_TIMELINE_EVAL_ENDPOINT`, `ASTRID_TIMELINE_EVAL_CREDENTIAL`,
   `ASTRID_TIMELINE_EVAL_REALM_ID`, or `ASTRID_TIMELINE_EVAL_ACTOR_ID`.
4. The selected `project-pack init` is launched with that environment at
   `harness.ts:589-594`.

Pure witnesses, with only presence/type/length/hash reported, establish the
file and authority prerequisites:

- Agent 6ef `_read_credential()` and `resolve_runtime_connection()` accepted a
  temporary JSON object with a string token and selected actor metadata; the
  resolved endpoint was loopback, the token was present and a string, and the
  resolved token matched the file content. No socket was opened.
- Runtime 95 `CredentialStore.provision_static()` followed by `require()`
  accepted the same kind of token with `handshake` scope. No daemon or HTTP
  request was used.
- The frozen App witness
  `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts`
  passed: 1 test file, 2 subtests, 0 failures. It confirms the child receives
  the credential path and the JSON file is mode `0600`.

The two pure Python witnesses were run with the exact pinned checkout roots
`/home/user/work/wt/agt-pin-6efc8150` and
`/home/user/work/wt/rt-pin-95bd3c5f`; their temporary fixture credentials were
not printed. The loader result was `present=true`, `type=str`, with a
loopback endpoint and matching file/token resolution. The Runtime result was
`stored_token_present=true`, actor type `str`, actor present, and
`handshake` scope present.

No credential value was printed in this report or in the source evidence.

## Environment/value propagation and verifier path

The owned runner establishes a separate launcher workspace before invoking the
App test:

- `run-owned-selected-final95.sh:500` exports
  `ASTRID_RUNTIME_DATA_ROOT=$run_root/runtime-data` and the private source
  manifest.
- `run-owned-selected-final95.sh:503-504` creates/inspects that runner
  workspace.
- The runner does not unset that data-root binding before the App test.

The selected harness starts its own Runtime under its throwaway
`<tmp>/realm`/`<tmp>/support` paths (`harness.ts:492-505`), mints the selected
credential against that Runtime (`harness.ts:562-571`), and passes its endpoint
only as `ASTRID_RUNTIME_ENDPOINT` (`harness.ts:644`). Agent 6ef does not use
that variable in `open_from_launcher()` when the eval override is absent:

- `astrid/sdk/client.py:363-387` first checks the all-or-nothing
  `ASTRID_TIMELINE_EVAL_*` override.
- With no override, `client.py:389-394` calls
  `ensure_runtime(start_pack_host=False)`.
- `client.py:402-424` then uses the explicit `ASTRID_RUNTIME_CREDENTIAL` file
  but takes endpoint/realm/actor from the launcher result. The inherited
  runner `ASTRID_RUNTIME_DATA_ROOT` is therefore authoritative for endpoint
  selection.

Runtime 95 then follows the expected verifier path:

- `runtime_protocol/server.py:108-116` extracts the bearer after requiring the
  Authorization scheme and delegates to `CredentialStore.require()`.
- `runtime_protocol/auth.py:223-242` compares the bearer against the selected
  Runtime's credential generations and checks scope. A credential minted by the
  harness Runtime is absent from the runner Runtime's store, producing the
  observed `invalid bearer credential` at `auth.py:237`.

The Agent and Runtime generated clients are the matched 0.2.14 contract with
the same protocol/schema/component metadata; this is not a client-generation
or transport-shape mismatch.

## Main normal admission comparison

The working normal three-product path is in
`tests/e2e/local/support/astrid.ts`:

- `astrid.ts:145-160` builds a fresh environment rather than inheriting the
  parent environment. It supplies the harness discovery endpoint and the
  actor-specific credential file through all four
  `ASTRID_TIMELINE_EVAL_*` variables, plus the harness realm and actor.
- `astrid.ts:166-171` launches with `exactEnv: true`.
- Agent 6ef `client.py:373-387` consequently calls explicit `AstridClient.open`
  against the harness Runtime and does not invoke ambient launcher selection.

The selected fixture has the same intended identity/grant contract but omits
that normal case-local context and retains the runner's ambient data-root
selection. This is the precise divergence.

## Minimal proposed correction and owner

Owner: **HOME/App source**, not Agent, Runtime, or the owned runner. HOME owns
`tests/e2e/local/support/harness.ts`; this worker made no edit there.

At the selected environment assembly around `harness.ts:641-648`, add the
existing normal-path case-local context using the already minted selected
credential and the current harness identity, without adding any auth source,
DTO, grant, store, route, timeout, or guard relaxation:

```ts
const discovery = this.discovery();
this.selectedParamEnv = {
  ...selectedParamCliEnv(process.env, credentialFile),
  ...this.runtimeEnv(),
  ASTRID_RUNTIME_ENDPOINT: this.runtimeUrl,
  ASTRID_TIMELINE_EVAL_ENDPOINT: discovery.endpoint,
  ASTRID_TIMELINE_EVAL_CREDENTIAL: credentialFile,
  ASTRID_TIMELINE_EVAL_REALM_ID: this.realmId,
  ASTRID_TIMELINE_EVAL_ACTOR_ID: 'astrid-selected-param',
  // existing project-pack/artifact/build fields remain unchanged
};
```

HOME should apply this as a minimal source hunk, retain the existing
`ASTRID_RUNTIME_CREDENTIAL` path and all original assertions, then rerun only
the bounded prerequisite/selected gate under fresh orchestrator authority.
The actor literal must remain identical to the actor passed at
`harness.ts:637`; no new credential is minted and no identity/grant assertion
is converted.

No owned-runner proposal is needed: the runner's source/tuple/pin custody is
correct and was independently preflighted. Its inherited data root is the
triggering ambient input, but the source-owned normal admission contract is
the proper minimal correction because only the harness knows the fresh
Runtime's endpoint, realm, actor, and selected credential path at fixture time.

## Controls and limits

Passed or retained from the bounded packet:

- Runner syntax, source/tree/tuple/artifact/graph custody and planted negative
  guards: PASS.
- Exact one-test collection: PASS.
- Frozen App selected credential shape/cleanup witness: PASS (command above).
- Agent 6ef pure credential loader/value-resolution witness: PASS (Python
  one-shot against the pinned Agent and Runtime generated-client roots; no
  socket).
- Runtime 95 pure credential generation/scope witness: PASS (Python one-shot
  against the pinned Runtime root; no daemon or HTTP).
- No source, helper, dependency, lock, generated file, or worktree change was
  made in this worker.

Unknown/not run by design:

- The corrected handshake has not been exercised.
- No handshake/socket/daemon/browser/build/install/full suite/actual/replay or
  retry was run.
- The selected behavior assertions remain unqualified: mount, P1/P2, source
  removal, refusal/draft retention, lost-ACK exact retry, reload/recovery,
  inverse/undo, and zero-legacy-POST.

Live callers and guarantees remain unchanged. The proposed correction only
selects the same case-local Runtime context already used by the normal
admission path; it does not alter selected authority resolution, command
identity, grants, Runtime routes, or assertion semantics.
