# AP2-M2 ordinary service-only gate

## Classification

**FAIL — App journey/product-path failure; not a worker-sandbox or central-browser environment failure.**

The actual central test service ran the committed tree. Chromium smoke passed, the hosted App build completed, and the selected Playwright test reached the Scene Phase Markers UI. The first observable causal failure was that clicking `scene-markers-move-shots` emitted no ordinary commit request.

## Exact run

- App source: `ebb762a774bd997b836947cbecc0828f797cbcfe`
- App tree: `c79b342f648d415ce2ff284e5903e16626aa00ad`
- Central request ID: `ap2-m2-ordinary-enabled-fixture-final-run-source-e2e-m2-ordinary-integration-1020200249-15359`
- Request command:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-enabled-fixture-final-run-source e2e-m2-ordinary-integration`
- Wait command:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-ordinary-enabled-fixture-final-run-source-e2e-m2-ordinary-integration-1020200249-15359`
- Result: `fail exit=1 in 187s`; `1 failed`
- Central result log:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-ordinary-enabled-fixture-final-run-source-e2e-m2-ordinary-integration-1020200249-15359/log.txt`

The service reported its internal invocation as `sh "$PWD/scripts/testing/run-central-m2-ordinary.sh" "$PWD"`; that script was not run from this worker sandbox.

## First causal failure

`tests/e2e/local/three-products.spec.ts:1222`:

```text
Expected: 1
Received: 0
Timeout 90000ms exceeded while waiting on the predicate
```

Immediately before the assertion, the journey filled the playhead tail with `3` and clicked `data-testid="scene-markers-move-shots"`. The wire recorder's `posts` remained empty, so this is earlier than Runtime acceptance, retry, Agent label, restart, or guarded undo. Those downstream stages are unverified.

The log also records `chromium-smoke PASS page launch, DOM assertion, page close`, a successful hosted Vite build, and one selected Playwright test. There is no EPERM/SIGTRAP in this service result.

## Smallest next action

Debug and repair the first no-post path in the App: `scene-markers-move-shots` → `moveExistingShotsToMarkers` → `ctx.creative.timeline.apply` → generic ordinary capture/outbox dispatch. In particular, determine whether the callback is a no-op/refusal or whether `clip.move`/`clip.update` ordinary members are not reaching the outbox. Then request this same named central suite once on the resulting new tree. Do not requalify this failed tree or change pins/environment as the next action.

## Scope and evidence

No source files were changed. No local browser/socket invocation, full suite, fix, pin, guard, or duplicate central request was made. The only test execution for this task was the named central service run above.
