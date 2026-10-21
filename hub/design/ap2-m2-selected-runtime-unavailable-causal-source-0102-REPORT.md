# AP2 M2 selected Runtime unavailable causal-source repair

## Result

Repaired the existing selected-PARAM DEV fixture lifecycle in
`tests/e2e/local/support/harness.ts:730-741`. The DEV Vite process now sends the
existing boot/auth bridge probe to the same Runtime port and uses the already
provisioned product credential:

- `VITE_ASTRID_BRIDGE_PORT=${runtimePort}`
- `ASTRID_BRIDGE_TOKEN=${productToken}`

The Runtime data proxy remains unchanged (`VITE_WORKSPACE_RUNTIME_URL` plus
`WORKSPACE_RUNTIME_TOKEN_FILE`). No App API, DTO, store, authority, scope,
profile, seed, timeout, status assertion, retry behavior, or production seam
was changed.

## Exact first refusal

The retained central27230 Playwright network trace is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/trace.zip`

Relevant network records in `0-trace.network`:

1. Source/editor origin: `http://127.0.0.1:45843/tools/video-editor`.
2. `GET http://127.0.0.1:45843/runtime-config/v1/workspace.json` returned
   `404`. This was a fallback identity read, not the refusal: the selected
   fixture already supplied the compiled actor/realm/instance identity.
3. First causal refusal: `GET
   http://127.0.0.1:45843/api/astrid/v1/health` returned `503 Service
   Unavailable`, with `X-Astrid-Bridge-Version: v1`,
   `Content-Type: application/json`, and `Content-Length: 120`.

The 120-byte response exactly matches the existing Vite guard at
`config/vite/astridBridgeProxy.ts:131-148`:

```json
{"error":"astrid_bridge_auth_not_configured","detail":"ASTRID_BRIDGE_TOKEN is required for real Astrid bridge requests"}
```

That guard runs before the bridge proxy and before the Runtime receives a
request. The browser request had the local Vite Host/Referer and no actor,
project, Authorization header, or project path; this is the pre-project boot
health probe. The intended server-side actor was the existing
`astrid-e2e-product` product credential, with the existing selected realm and
Runtime instance. No Runtime-door health response, Runtime handshake, or
project request was reached in central27230.

Causal chain: `startSelectedParamDevServer()` supplied the product credential
only to the existing `/api/runtime` proxy. It omitted
`ASTRID_BRIDGE_TOKEN`, so `resolveAstridBridgeProxyPolicy()` produced no
bridge token and the existing fail-closed auth guard returned 503. The default
bridge target was also not the selected Runtime. The App correctly rendered
“Workspace Runtime is unavailable” after the bridge health probe failed.

## Changed exports and live callers

- Changed exports: none.
- Changed live caller: the existing `DirectHarness.startSelectedParamDevServer()`
  environment assembly only.
- Existing consumers: `config/vite/vite.config.ts:58-80` reads the bridge
  port/token; `createAstridBridgeAuthPlugin()` and
  `createAstridBridgeProxyOptions()` are unchanged.

## Tests and verification

Passed:

- `git diff --check`
- `npx eslint tests/e2e/local/support/harness.ts --ext ts --max-warnings 0`
- `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts`
  — 1 test file, 3 subtests passed.

An attempted targeted Vitest collection was not evidence: the first invocation
produced no result and was terminated after no progress; the cache-disabled
runner invocation exited during config loading because this repo's config uses
`__dirname`, which `--configLoader=runner` does not provide. No source test
was weakened. No browser, central request-test, full suite, live socket gate,
or retry was run after the causal review.

## Scope decisions

The smallest repair is in the selected fixture lifecycle, not HOME production
code: the trace and source prove the refusal is the fixture's missing existing
bridge credential, while the production/local launcher already sets these same
bridge variables. Approved seed `24165`, issuer context `eee191`, all P1/P2
and later removal/refusal/draft/retry/reload/undo/zero-legacy assertions remain
untouched.

The central browser gate remains unverified after this change and should be
rerun only by the orchestrator after review.

