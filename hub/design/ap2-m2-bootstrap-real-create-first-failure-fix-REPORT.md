# AP2-M2 first real bootstrap failure fix

## Result

Implemented the proven fixture-only fix in
`tests/e2e/local/three-products.spec.ts`: the bootstrap journey now observes
Runtime requests from the Playwright `BrowserContext`, rather than only the
`Page`. All original create, commit-body, native-command, zero-legacy-traffic,
history, retry, restart, and undo assertions remain unchanged.

No production App source, Runtime authority, provider, schema, DTO, dependency,
or pin changed.

## Diagnosis

The earlier central trace proves the real New Project gesture completed the
production path. For project `cd8956a47311486fbbd8dcb12665faa2`, the trace
contains:

- `POST /api/runtime/v1/projects/<project>/timelines` → `201`
- `POST /api/runtime/v1/projects/<project>/timelines/<timeline>/commit` → `200`
- a native commit containing `timeline.init` and two `track.create` commands
- no legacy snapshot write for this bootstrap

The same trace's browser request log contained those Runtime requests, while
the test's `page.on('request')` collection was empty at the assertion. This is
an observation-fixture failure, not a missing create hookup or a headless/pristine
refusal. The context-level observer covers requests issued through the browser
context, including the service-worker-routed request path, while preserving the
test's existing route normalization and assertions.

## Verification

- `git diff --check` — passed.
- Bootstrap-only central command:

  ```sh
  R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-bootstrap-real-create-first-failure-fix ap2-m2-bootstrap-committed-service-qualification) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$(basename "$R")"
  ```

  Result: failed before browser execution with the existing exact-title
  selector (`Error: No tests found`); the central wrapper's selector needs to
  use the unique bootstrap substring rather than an anchored full title.

- Central fallback command:

  ```sh
  R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-bootstrap-real-create-first-failure-fix normal014-integration-e2e-gate5) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$(basename "$R")"
  ```

  Result: failed in the established neighboring M1 gate before the bootstrap
  test ran (`mounted editor must claim a new durable command owner`). The
  private build and frozen tuple/artifact checks passed. This does not qualify
  or disqualify the corrected bootstrap observer.

## Blockers and next step

The source fix is complete, but live post-change bootstrap qualification is
unverified because the bootstrap-only central wrapper selector fails before
collection and the fallback run is serially stopped by the neighboring M1
failure. Correct the wrapper's grep to the unique substring
`M2 real gate 5 bootstrap actual consumer`, then run that one bootstrap test
once on the same frozen tuple.
