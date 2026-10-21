# AP2 M2 selected DEV readiness assertion conversion

## Result

Converted the selected DEV journey's impossible same-origin Runtime status-pill
readiness checks to the existing `openSeededTimeline` readiness surface. The
three `expectConnected(page)` calls in the selected DEV case (initial load,
post-P2 source-removal reload, and post-lost-ack retry reload) were removed,
leaving the existing helper at each point. That helper proves the seeded
project is selected, the timeline control is visible, and the first track data
is rendered. The existing selected clip, `astrid-element-params`, and `Amount`
control assertions remain unchanged and continue to prove P1 data binding.

Only this test file changed:

```text
tests/e2e/local/three-products.selected-param-dev.spec.ts
```

The hosted connection assertion remains unchanged in
`tests/e2e/local/support/app.ts`. No production gating, DOM hook, fake
connected state, transport mock, API, timeout, or behavioral assertion was
added or removed. P1/P2 admission, source removal, refusal, draft/retry,
reload, undo, and zero-legacy-write assertions are preserved.

## Verification

Passed:

```text
TMPDIR=<private temporary directory> node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts
  1 file passed; 0 failed

./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.selected-param-dev.spec.ts
  passed

./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list
  Total: 1 test in 1 file

git diff --check
  passed

sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh
  passed
```

The source guards also confirmed that the selected DEV spec has no remaining
`expectConnected` call, the hosted helper has no diff, and the only changed
path is the selected DEV spec.

## Decision and limits

Source-cause report 0138 establishes that same-origin DEV intentionally does
not render `runtime-connection-status`; its `workspace.json` 404 is expected,
while canonical resolver/admission and frozen imports succeed. The existing
project/timeline/track helper is therefore the direct one-to-one DEV data
readiness equivalent.

No browser, localhost/live socket, central request-test, full suite, or real
gate was run. Independent test-conversion review remains required before any
subsequent real gate.
