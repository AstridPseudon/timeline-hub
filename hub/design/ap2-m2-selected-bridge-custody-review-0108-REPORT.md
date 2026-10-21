# AP2 M2 selected bridge-auth custody review

## Verdict

**APPROVE the exact candidate commit for one permitted selected-fixture rerun.**

- Commit: `1d9299867020b64fd80afae0ea5a951601d4dc8d`
- Commit tree: `e12413cdaa3951ee6262a16229dadbfda8f7f8de`
- Changed file hash: `tests/e2e/local/support/harness.ts` — `85ac13b63c1f009465f3a0b6ffd31e2eafc6cc399ac7f6949a3c37541e335fb0`
- Direct parent: `0bcf2efe1e286de4951bbb823c938770a30d7a10`

The named base ref `tl/ap2-m2-selected-runtime-unavailable-causal-source-0102` currently resolves to the candidate commit itself, so the precise changed-fixture check used the direct parent. This is a ref bookkeeping observation, not a source finding.

## Review result

The candidate adds only these four lines to `DirectHarness.startSelectedParamDevServer()`:

- `VITE_ASTRID_BRIDGE_PORT` is the current `this.runtimePort`, which is the same endpoint exposed by `this.runtimeUrl`.
- `ASTRID_BRIDGE_TOKEN` is the existing `this.productToken`, provisioned by the same DirectHarness Runtime.

The existing Vite bridge keeps the token server-only: the variable has no `VITE_` prefix, the proxy injects it as the upstream bearer, and the browser-facing Runtime credential remains `WORKSPACE_RUNTIME_TOKEN_FILE`. The bridge target is loopback and the existing origin handling, Runtime bearer checks, project-path checks, and fail-closed 503 guard are unchanged. No URL, token file, browser bundle, or log path was added.

The issuer and target remain the same harness Runtime after the approved authoring restart. The product actor remains `PRODUCT_ACTOR` and the realm/Runtime instance remain the existing harness identity. The selected project is still created, published, admitted, and addressed through the existing project-scoped paths; the candidate adds no project substitution or broad scope. Approved commits `eee191c1fe5c5bf2625ab640f17923ddabaab000` and `24165cb37b46a5c1a6676bd646d01f18e9552ee9` are ancestors and were not altered. The selected journey spec, original guards, native P1 admission sequence, P2 removal/refusal, retry, reload, undo, and zero-legacy assertions are unchanged.

No forced-connected mode, mock/fake Runtime, scope bypass, profile bypass, new endpoint, alternate credential carrier, or production source change is present.

## Evidence

Passed:

- `node --import tsx tests/e2e/local/support/selected-param-credential.test.ts` — 3 subtests passed: path-versus-token custody, issuer/endpoint/realm/actor binding against stale ambient values, and teardown cleanup.
- `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts` — 1 file-level test passed.
- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts` — passed.
- Direct-parent changed-fixture check — exactly one modified file, 4 additions/0 deletions, `git diff --check` passed, no forbidden shortcut/leak pattern found, and the worktree is clean.

The targeted bridge-policy Vitest command was attempted with `--no-cache`; this worker did not count it as evidence because the runner produced no completion summary in this environment. Existing bridge-policy source/tests were inspected and remain unchanged.

No browser, localhost/live-socket, central gate, full suite, or retry was run, as required. The orchestrator may rerun the one authorized selected fixture gate against the exact commit/tree above.
