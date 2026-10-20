# AP2-M2 bootstrap explicit-scope helper fix

## Result

Produced the test-only harness candidate. The shared timeline path helper now
has an explicit `TimelineScope` (`projectId` + `timelineId`). Existing seeded
callers retain their original default scope: `harness.seed.projectId` and the
passed seed's `timelineId`. The bootstrap history lookup passes the independently
observed `expectedScope` from the created-project URL and selected timeline.

No public/runtime DTO, product source, browser flow, or transport assertion was
changed.

## One-to-one correction map

- Replaced the invalid `seed.projectId` read with the test-only scope formatter.
- Preserved every existing `timelineBase(harness, seed)` caller through the
  default `{ projectId: harness.seed.projectId, timelineId: seed.timelineId }`.
- Removed the bootstrap spread object that fabricated `projectId` on
  `ThreeProductsSeed`; `history(harness, seed3, expectedScope)` now uses the
  created project's exact project and reserved selected timeline IDs.
- Preserved the exact audit path/status matching, requested-name/UI/URL
  identity, create-before-init ordering, accepted-history init command list,
  outbox scope, retry/reload/restart/recovery, guarded undo, opaque-data, and
  zero-legacy assertions.
- Added one pure direct fixture test covering seeded and created-project path
  formatting; no matrix or live fixture was added.

## Checks

- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — PASS (1 test).
- `npx eslint tests/e2e/local/three-products.spec.ts tests/e2e/local/support/timeline-scope.ts tests/e2e/local/support/timeline-scope.test.ts --report-unused-disable-directives --max-warnings 0` — PASS.
- `npm run typecheck:strict-islands` — PASS.
- `npx playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts --grep "bootstrap actual consumer" --list` — PASS; exactly 1 test collected.
- `git diff --check` — PASS.

No request-test, runner, browser, socket, or full suite was run. The actual
bootstrap journey remains unverified here.

## Later bootstrap-only review/gate command

After the harness commits this candidate, dispatch exactly the existing
bootstrap-only suite and wait for its result:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-bootstrap-explicit-scope-helper-fix ap2-m2-bootstrap-observed-request-match-fix) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$(basename "$R")"
```

The suite's private wrapper must retain its pre-build `--list` proof of exactly
one test using the unique `bootstrap actual consumer` substring and the frozen
source tuple; do not run the neighboring Gate 5 or full suite.
