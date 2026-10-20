# AP2 M2 ordinary live-action qualification

## Result

Ported the exact fixture-only authoring admission fix from
`ap2-m2-private014-first-admission-guard-fix` into the ordinary App journey:

- `tests/e2e/local/three-products.spec.ts` now calls the existing,
  idempotent `harness.enableTimelineAuthoring(ASTRID_PYTHON)` at the shared
  `openCommandTimeline` boundary, before any editor navigation.
- `src/test/threeProductsAuthoring.test.ts` registers the real Gate 5 and
  dependency-conflict journey callbacks and verifies authoring startup occurs
  before `openApp`, including refusal-before-navigation.

No product guard, Runtime route, command, producer, authority, recovery,
outbox, or legacy-writer behavior was changed. The ordinary test's existing
explicit authoring call remains; the shared boundary call is intentionally
idempotent and makes a selected standalone journey self-sufficient.

## First actual central result

The prior central candidate was:

- Test ID: `ap2-m2-ordinary-real-scene-ui-first-failure-fix-e2e-m2-ordinary-integration-1020194847-28353`
- App tree: `1e9c7b1f0854a77edb64585f06eac44a1d39c6ee`
- App source head: `1953a1e2599eef3d2a389080393a81d42ea2f01e`
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Result: **fail**, exit 1 in 175s; hosted build and Chromium smoke passed.

The first failing assertion was the native journey boundary at
`tests/e2e/local/three-products.spec.ts:1220`:

```text
after filling the real Scene Phase Markers tail input and clicking
scene-markers-move-shots:
Expected wire.posts.length = 1
Received 0
Timeout 90000ms exceeded while waiting on the predicate
```

The preceding DOM admission (`scene-markers-summary` with two markers) was
not sufficient evidence. The run did **not** verify the required
MoveShots -> four native commands -> one outbox intent -> zero legacy traffic
path. The central log did not retain the browser error-context/trace files in
the accessible result directory, so no narrower native capture guard is
claimed from that run. The shared owner-readiness wait did not fail before the
button action; the observed first failure was the zero native commit POST.

The settled private014 diagnosis identifies the normal fixture defect as
neutral Runtime startup before the verified Astrid authoring baseline, which
can leave the seeded publication without public history (`409
history_unavailable`). This candidate applies that exact existing fixture
repair before editor navigation; it does not relax any product guard.

## Validation

Passed locally:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-private014-first-admission-guard-fix/vitest-runner.cjs \
  node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/test/threeProductsAuthoring.test.ts
PASS: 1 file, 3 tests

node_modules/.bin/eslint src/test/threeProductsAuthoring.test.ts \
  tests/e2e/local/three-products.spec.ts --no-warn-ignored --max-warnings 0
PASS

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-private014-first-admission-guard-fix/vitest-runner.cjs \
  node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx \
  src/tools/video-editor/dev/localExtensions.catalog.test.ts
PASS: 3 files, 53 tests

git diff --check
PASS
```

An initial direct Vitest invocation was not usable because the repository's
ESM config loader raised `ReferenceError: __dirname is not defined`; the
repository-compatible private runner above then passed without changing the
config or shared dependencies.

Not run: local browser, localhost/live sockets, full suite, or another central
request. The task explicitly requires the candidate source to be finished
before the next central run, and central testing must be used for the browser
journey.

## Next request

After the harness commits this candidate, request exactly one fresh central
ordinary integration run:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-ordinary-live-action-qualification e2e-m2-ordinary-integration) && \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

That run must inspect the actual POST body and outbox state, proving exactly
four native commands (`clip.move`, `clip.set`, `clip.move`, `clip.set`), the
lost-ACK/restart/exact-retry/disjoint-Agent-label/guarded-undo assertions,
opaque preservation, and `wire.legacy === []`.
