# AP2-M2 bootstrap created-timeline scope source

## Result

Fixed the first scoped bootstrap failure as a test-fixture race. The test read
the created project’s Runtime timeline list before the App’s reserved timeline
was created, then compared that stale page with the later UI-selected ID.

The retained browser trace showed the normal resource shape (`{items: [...]}`
with canonical `timeline_id`), the created-project URL scope, and the exact
ordering: list read first, then `POST /v1/projects/{created}/timelines`, then
native `/commit`; the UI later selected that created timeline. This is not
evidence of a product identity bug or an unregistered timeline.

## Changes

- Added a pure `timelineFromList` exact-ID helper and regression covering an
  exact match and a missing ID; seeded and created path callers remain explicit.
- Bootstrap now waits for the outbox reservation with the exact realm/project/
  timeline scope, then polls the normal Runtime list until that exact selected
  `timeline_id` is present. It never accepts an arbitrary timeline or derives
  scope from undo.
- Existing create/init ordering, history, retry, reload/restart, undo, opaque,
  and zero-legacy assertions are preserved unchanged after the corrected gate.

## Validation

- `./node_modules/.bin/eslint tests/e2e/local/support/timeline-scope.ts tests/e2e/local/support/timeline-scope.test.ts tests/e2e/local/three-products.spec.ts --ext ts --report-unused-disable-directives --max-warnings 0` — PASS.
- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — PASS.
- `./node_modules/.bin/tsc -p tsconfig.json --noEmit --pretty false` — PASS.
- `./node_modules/.bin/tsc -p tsconfig.node.json --noEmit --pretty false` — PASS.
- Targeted scope-only TypeScript check over both scope files — PASS.
- `git diff --check` — PASS; changed-file list is exactly the three intended
  App test files.
- `./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false` —
  FAIL with pre-existing unrelated diagnostics in `dataProvider.ts`,
  `shotSetCapture.ts`, and Composition/evaluator imports; none involve this
  change.

No central request-test, runner, browser/socket, full suite, product/API/DTO,
pin, dependency, or shared-install change was made. The corrected bootstrap-only
central gate is the next step:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-bootstrap-created-timeline-scope-source ap2-m2-bootstrap-scoped-audit-central-gate)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```
