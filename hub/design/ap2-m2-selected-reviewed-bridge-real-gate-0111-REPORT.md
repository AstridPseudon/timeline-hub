# AP2 M2 selected reviewed bridge real gate

## Disposition

The custody-approved bridge repair was run through the one authorized central
selected gate. The source checks and private preflight passed, but the central
gate failed before selected P1, so this row remains HELD. No native-success,
writer-retirement, or `DELETED` claim is made.

## Reviewed source identity

- Reviewed custody decision: APPROVE
- Source commit: `1d9299867020b64fd80afae0ea5a951601d4dc8d`
- Source tree: `e12413cdaa3951ee6262a16229dadbfda8f7f8de`
- Direct parent used for the exact hunk check: `0bcf2efe1e286de4951bbb823c938770a30d7a10`
- Changed file: `tests/e2e/local/support/harness.ts`
- Changed file SHA-256: `85ac13b63c1f009465f3a0b6ffd31e2eafc6cc399ac7f6949a3c37541e335fb0`

The exact reviewed hunk is four additions and no deletions. It supplies the
existing selected Runtime port as `VITE_ASTRID_BRIDGE_PORT` and the existing
server-side product credential as `ASTRID_BRIDGE_TOKEN` in
`DirectHarness.startSelectedParamDevServer()`. The existing Vite bridge keeps
the token server-only, injects it upstream, and retains its origin checks and
fail-closed auth guard. No App API, DTO, scope, profile, authority, seed,
timeout, status assertion, retry behavior, or production source changed.

Live callers remain the existing harness environment assembly, the Vite bridge
policy in `config/vite/astridBridgeProxy.ts`, and the selected journey
`tests/e2e/local/three-products.selected-param-dev.spec.ts`.

## Offline checks

Passed:

```text
offline reviewed-source checks: PASS
commit=1d9299867020b64fd80afae0ea5a951601d4dc8d tree=e12413cdaa3951ee6262a16229dadbfda8f7f8de changed=1 file additions=4 deletions=0
```

The checks verified the exact commit/tree, clean worktree, one-file four-line
diff, `git diff --check`, the two reviewed environment assignments, retained
bridge auth guard/upstream-header source, and the selected journey's connected
status plus P1/P2/removal/refusal/draft/retry/reload/undo/zero-legacy guards.

## Preflight

Command:

```sh
TMPDIR=<private-owned-directory> SELECTED_WORKSPACE_PREFLIGHT_ONLY=1 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh /home/user/work/wt/ap2-m2-selected-reviewed-bridge-real-gate-0111
```

Result: PASS — `selected DEV private workspace preflight: ready`. The frozen
Agent `8130a401...` / Runtime `2c4ac180...` identities, public Composition
0.0.13 artifact, private workspace create/inspect, clean-source, shell, and
disk checks passed. The owned temporary directory was cleaned on exit.

## Central selected gate

Exactly one central request was submitted after custody approval:

```text
request-test ap2-m2-selected-reviewed-bridge-real-gate-0111 ap2-m2-selected-real-p1-history-fixture-fix --no-cache
```

Authoritative result:

- ID: `ap2-m2-selected-reviewed-bridge-real-gate-0111-ap2-m2-selected-real-p1-history-fixture-fix-1021011305-23934`
- Exit: `1` / fail in 95 seconds
- App tree: `e12413cdaa3951ee6262a16229dadbfda8f7f8de`
- Build: passed
- Collection: one selected test
- Failure: `tests/e2e/local/three-products.selected-param-dev.spec.ts:45`
- Assertion: the real `[data-testid="runtime-connection-status"]` element did
  not appear with `data-state="connected"` within 20 seconds

The retained trace shows the reviewed bridge repair is active: selected
`/api/astrid/v1/health` and `/api/astrid/v1/handshake` returned 200, as did the
Runtime health/handshake/realm/project reads. The selected page mounted its
timeline, but the connected status element was absent for the complete truthful
20-second wait. Existing ACP chat requests returned 500 and the existing
`runtime-config/v1/workspace.json` fallback returned 404; neither is claimed as
the selected P1 admission result.

Bounded failure evidence was retained by the central runner:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace`

No local browser, full suite, retry, pin change, credential exposure, URL leak,
forced-connected mode, mock Runtime, scope/profile bypass, or assertion
weakening was used.

## Remaining physical cut

The selected-pack legacy snapshot writer is already absent in the current App
integration source, as documented by the prior 0059 cut review. The remaining
`onChange(next)` branch in `AstridElementParams.tsx` serves unowned/literal
fallback data and stays live. It is not safe to delete it from this selected
row. The row therefore remains open and is not marked `DELETED`.

## Next step

The selected connection-status failure needs a separately reviewed source
diagnosis before any further central run. This task performed the one permitted
preflight and one permitted central run; no retry was made.
