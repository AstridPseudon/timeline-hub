# AP2 M2 ordinary current Scene fixture join

## Result

Ported only the existing standalone prerequisites from the reviewed donors:

- `devLocalExtensions` now appends the existing reviewed
  `scenePhaseMarkersExtension` after the generated Astrid catalog, with the
  catalog-boundary assertion updated accordingly. This restores the existing
  Scene Markers panel/producer to the normal host; it adds no UI or producer.
- `openCommandTimeline` now establishes the existing idempotent Astrid
  authoring baseline before standalone editor navigation.
- Added the donor's focused authoring ordering/refusal regression
  (`src/test/threeProductsAuthoring.test.ts`).

No Scene Markers implementation, readiness forcing, permissions, production
initialization, Runtime/TimelineOps/session/Provider code, schema, pin, or
dependency changed. The ordinary ten-member journey, retry/restart/undo,
opaque-data, and zero-legacy assertions were preserved.

## First causal evidence

The owner-joined gate on App `8c0e1f799` failed at
`tests/e2e/local/three-products.spec.ts:1153` because
`[data-testid="scene-markers-summary"]` was absent. The action was never
clicked, so no capture or command POST occurred. Current `devLocalExtensions`
contained only generated pack entries, while the existing App-owned marker
extension, panel, producer, and reviewed ID remained present. The exact donor
`tl/ap2-m2-ordinary-real-scene-ui-first-failure-fix` restores that admission.
The current shared opener also lacked the exact standalone authoring setup from
`tl/ap2-m2-ordinary-live-action-qualification` /
`tl/ap2-m2-ordinary-enabled-fixture-final-run-source`; that setup is restored
without changing its behavior.

## Validation

Passed:

```text
ASTRID_CHECKOUT=/home/user/work/agent VITEST_LANE=checkout \
node --require ./.vitest-runner.cjs node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism src/test/threeProductsAuthoring.test.ts
1 file, 3 tests passed

ASTRID_CHECKOUT=/home/user/work/agent VITEST_LANE=checkout \
node --require ./.vitest-runner.cjs node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/dev/localExtensions.catalog.test.ts
1 file, 2 tests passed

node --require ./.vitest-runner.cjs node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx
2 files, 47 tests passed

node --require ./.vitest-runner.cjs node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx
1 file, 7 tests passed

node_modules/.bin/eslint --no-cache --max-warnings 0 \
  src/tools/video-editor/dev/localExtensions.ts \
  src/tools/video-editor/dev/localExtensions.catalog.test.ts \
  src/test/threeProductsAuthoring.test.ts \
  tests/e2e/local/three-products.spec.ts
passed

git diff --check
passed
```

The first direct Vitest invocation failed before collection because the repo's
ESM config loader needs the established temporary `__dirname` shim; the
private one-line shim was created in this worktree for the passing runs and
removed afterward. No browser, localhost/live socket, full suite, or
`request-test` was run.

## Next step

After the harness commits this candidate, run exactly:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-current-scene-fixture-join e2e-m2-ordinary-integration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

That browser qualification remains unverified here.
