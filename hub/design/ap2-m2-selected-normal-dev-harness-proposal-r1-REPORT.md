# App2 selected normal-DEV harness parity proposal

## Verdict

Prepare, but do not apply, the one-file harness correction below. The
selected DEV caller currently points Vite at the Runtime's raw loopback
endpoint. The existing normal DEV launcher starts
`scripts/runtime-discovery-proxy.mjs`, points Vite at that proxy, and lets the
proxy reread `support/discovery.json` and its product credential per request.
The proposal gives the selected caller that same existing discovery path.

This is a source-only proposal. It does not qualify the selected case and
does not claim to fix old18585: its historical mount boundary remains
UNKNOWN. It does not change the selected spec, App2's row-local code, product
bootstrap, routes, selectors, timeouts, recovery navigation, or authority.

## Exact source identity

The proposal is against current `tl/integration` and this worker tree:

```text
HEAD/tree: e75a96c69576c5744d8c49848e1f15a92e4f1c5a
tests/e2e/local/support/harness.ts: 0b5ac38fc5c11794d2e9ed75d03adf4e085262825a56db36aa73b08e4d630a14
tests/e2e/local/three-products.selected-param-dev.spec.ts: 2cd9703de2282282a477f5661d600049c8507fb93df1ef0424a06e7978a8b6a0
scripts/runtime-discovery-proxy.mjs: 93989e634008d1c9a6aaeddbca7b0aa0f97c40a7ce232860157d04bc6b2155c0
scripts/dev-local-workspace.mjs: b367c6045f2ad6fa568b5ea77b0b5fac4e2554e93d5bfb19c9a03f35f722afe5
config/vite/vite.config.ts: 5f26c8fa9beae5691c7c94ae11d008eb6c548eb28aaa2b66887b7512efe6c70d
```

The worktree is clean and equal to `tl/integration` at this identity.

## Existing seam and exact small patch

The selected caller is `tests/e2e/local/support/harness.ts:708-737`.
The normal launcher is the already-existing reference path:

- `scripts/dev-local-workspace.mjs:553-580` gives Vite the proxy URL,
  discovery path, credential file, and expected identity.
- `scripts/dev-local-workspace.mjs:672-682` starts the existing proxy and
  waits for its loopback port.
- `scripts/runtime-discovery-proxy.mjs:79-105,404-416` serves
  `/runtime-config/v1/workspace.json` from validated discovery and emits only
  non-secret identity.
- `scripts/runtime-discovery-proxy.mjs:48-57,418-464` rereads discovery and
  forwards authenticated Runtime traffic without browser credentials.

The complete unapplied patch is
[`ap2-m2-selected-normal-dev-harness-proposal-r1.patch`](ap2-m2-selected-normal-dev-harness-proposal-r1.patch).
It changes only `tests/e2e/local/support/harness.ts`:

1. Allocate one throwaway loopback port with the existing `freePort()`.
2. Start the existing discovery proxy as a managed child using the existing
   `support/discovery.json` authority and the selected Vite origin for the
   existing operation-origin fence.
3. Wait for the existing workspace-config endpoint, failing with the proxy's
   bounded stderr tail if the child exits.
4. Set only `VITE_WORKSPACE_RUNTIME_URL` to the proxy port.
5. Stop the proxy before the Runtime in the existing teardown.

`WORKSPACE_RUNTIME_TOKEN_FILE` remains the existing product credential file;
no token is copied into browser-visible environment or headers. The existing
selected Agent credential, expected actor/realm/instance, element resolver,
Vite command, and 60-second Vite startup wait remain unchanged.

## Preserved selected contract

The patch deliberately leaves
`tests/e2e/local/three-products.selected-param-dev.spec.ts` byte-for-byte
unchanged. In particular it preserves the exact original P1 input and
schema-source pin, P2 source removal, refusal assertion, lost-ack retry body
and idempotency key, both existing reloads, recovery, inverse/undo, legacy
traffic assertion, and original budgets (`CEILING` 90 seconds and selected
fixture timeout 240 seconds). The existing startup precondition and selector
are not edited. No second selected case is part of this proposal.

## Negative controls

An implementation may proceed only if all of these remain true:

- `git diff --name-only` contains only
  `tests/e2e/local/support/harness.ts`; the selected spec, App2 row-local
  files, product source, Vite config, proxy source, and Runtime source remain
  unchanged.
- The selected spec's original input, assertions, `CEILING`, fixture timeout,
  `page.goto`, selector/precondition calls, reload count, and recovery/undo
  path compare byte-for-byte with this source tree.
- The selected Vite environment contains a loopback proxy URL, not the raw
  `this.runtimeUrl`; `WORKSPACE_RUNTIME_TOKEN_FILE` remains a path, and no
  bearer value is introduced into `env`, browser code, or request headers.
- Removing or corrupting `support/discovery.json` makes the proxy's existing
  workspace-config request fail closed; the selected caller does not fall
  back to the raw Runtime endpoint or invent a second proxy.
- A proxy child exit aborts startup with its existing bounded diagnostic, and
  teardown stops Vite, then the proxy, then Runtime; no managed child is left
  behind.
- Existing proxy operation-origin/host admission and discovery identity
  checks remain the controls: no new route, flag, DTO, authority source,
  timeout, retry, reload, or recovery navigation is introduced.

## Required independent review

Before any selected actual is authorized, an independent App reviewer should
review the unapplied patch against this exact tree and answer:

1. Does it touch only the shared harness seam and mirror the normal launcher's
   existing proxy lifecycle?
2. Does every Runtime request and workspace-config read use discovery-backed
   proxy authority, with no browser credential exposure or raw-endpoint
   fallback?
3. Are process startup failure and teardown ordering bounded and leak-free?
4. Are the selected spec, P1/P2 input, original budgets, retry/inverse/reload
   assertions, and App2-owned row-local code untouched?

The reviewer should run static patch checks and existing proxy unit tests, but
must not approve based on a browser run. Only after that verdict may HOME
decide whether to request the single authorized selected case through the
central test service. That later run must still report old18585's startup
cause separately; proxy parity is not causal proof.

## Verification and limits

Read-only inspection passed for PLAN.md, COMMON.md, CLAUDE.md, the requested
startup accounting report, peer05:29, predecessor reports, current harness,
normal launcher, proxy, Vite config, and selected spec. `git status --short`
was clean; no repository source was edited.

The following were intentionally not run: browser/localhost/live-socket
execution, another selected case, central test service, full suite, build,
install, TypeScript check, or any source patch application. The proposal is
therefore unqualified. The prior-research directory named by COMMON.md is
absent in this environment; the available predecessor reports and shared
design reports were read instead.
