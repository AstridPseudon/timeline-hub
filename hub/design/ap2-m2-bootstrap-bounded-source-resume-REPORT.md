# AP2-M2 bootstrap bounded source candidate

## Result

Produced one App test-only bootstrap candidate. It is not live-qualified here
because this task explicitly forbids browser, socket, runner, and central test
execution. No production source, dependency, pin, or authority path changed.

## Source changes

- `tests/e2e/local/three-products.spec.ts:153`: `timelineBase` now uses the
  supplied seed's `projectId`, not `harness.seed.projectId`. Existing seeded
  callers have the same IDs; the New Project journey is the proven caller where
  the IDs differ.
- `tests/e2e/local/three-products.spec.ts:1141-1255`: replaced the failed
  Playwright page/context/CDP request observer with the existing server-side
  `DirectHarness.audit()` boundary and `waitForAudit` flush polling. The
  matcher uses the two exact expected paths and checks create `201`, init `200`,
  create-before-init, and zero legacy POST writes.
- Scope is independently derived from the real gesture: project ID from the
  post-Create-Project URL, requested `projectName` shown by the Select project
  UI, and the UI-selected `timeline` URL after the editor is ready. The
  selected timeline must be present in the created project's Runtime list and
  must not be a shot. The durable outbox scope is matched against
  `{ realmId, projectId, timelineId }` before faulting the first edit.
- The init command assertion remains exact at the accepted Runtime history
  boundary (`timeline.init`, `track.create`, `track.create`, each version `1`),
  because the door audit intentionally exposes method/path/status, not request
  bodies. The real gesture, reserved timeline ID, create-before-init, durable
  outbox, retry/reload/restart/recovery, guarded undo, opaque/credential guards,
  and zero-legacy assertions remain in place.

## Failure classification and evidence

The prior failures are observer/fixture failures, not missing production
writers or refusal behavior. The central context-observer report is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-bootstrap-context-observer-central-gate-REPORT.md`.
Its trace
`/tmp/timeline-normal014-app.cPq73K/browser-output/three-products-M2-real-gat-9f316-ry-restart-and-guarded-undo/trace.zip`
records browser-originated cross-origin POSTs for project
`e97619998da54d0199c7c4c9fe80fa93`:

- create `/api/runtime/v1/projects/e97619998da54d0199c7c4c9fe80fa93/timelines`
  returned `201`;
- native commit `/api/runtime/v1/projects/e97619998da54d0199c7c4c9fe80fa93/timelines/4aab3ff3-0cf0-5219-bda9-70c2af630d26/commit`
  returned `200`.

The later CDP-source trace
`/tmp/timeline-normal014-app.W8KXgL/browser-output/three-products-M2-real-gat-9f316-ry-restart-and-guarded-undo/trace.zip`
likewise records create `201` and commit `200` for project
`db04a78300474489a1e61a7ca66dca5a` and reserved timeline
`631e841f-b8f0-5448-a89e-0250dc2a437a` (create at `21:22:07.378Z`, commit at
`21:22:07.425Z`). The exact mismatch is below the Playwright page/context/
route/CDP observation surfaces; an earlier audit read also raced append-only
server-log flush. The source candidate therefore uses the server audit only for
method/path/status and accepted history for the exact init body.

## Verification run here

These were the only commands run after the final edit:

- `node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --no-cache --max-warnings 0` — passed.
- `node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts --grep "M2 real gate 5 bootstrap actual consumer" --list` — passed; exactly one test collected, no execution.
- `npm run typecheck:strict-islands` — passed.
- `git diff --check` — passed.

No central or local browser/socket/runner test was run by this worker.

## Next command after harness commit

Manager should dispatch the bootstrap-only suite once the harness commits this
candidate:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-bootstrap-bounded-source-resume ap2-m2-bootstrap-observed-request-match-fix) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$(basename "$R")"
```

