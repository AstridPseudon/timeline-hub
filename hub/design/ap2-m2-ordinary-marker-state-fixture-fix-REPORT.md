# AP2 M2 ordinary marker-state fixture fix

## Result

Restored the existing ordinary fixture's two Scene Phase Markers in the
direct-harness publication. The seed now writes:

```text
config.app['haus.astrid.scene-phase-markers'].sceneMarkers =
  [{ id: 'ordinary-marker-a', time: 1 }, { id: 'ordinary-marker-b', time: 6 }]
```

This is the seeded project/timeline parent composition that the mounted panel
reads through `TimelineSnapshot.app[extensionId]`. The normal authoring startup
and tracked-timeline navigation guard are unchanged. No production writer,
API, component state, capture port, or producer filtering was added; all five
visual members and the existing ten-command assertions remain untouched.

Added one focused regression tying the fixture constants to the real
`readMarkers` path. The prior retained trace's first failure was therefore a
missing fixture value, not a capture/action failure.

## Verification

Passed:

```text
node --require ./.vitest-runner.cjs node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism src/test/threeProductsAuthoring.test.ts
# 1 file, 4 tests passed

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-private014-first-admission-guard-fix/vitest-runner.cjs \
  node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx
# 2 files, 47 tests passed

node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 \
  src/test/threeProductsAuthoring.test.ts tests/e2e/local/support/harness.ts
# passed

node_modules/.bin/playwright test tests/e2e/local/three-products.spec.ts \
  --list --config playwright.three-products.config.ts
# Total: 11 tests in 1 file

git diff --check
# passed
```

`tsc -p tsconfig.app.json --noEmit --pretty false` was run and remains
blocked by existing baseline errors in `projectDataMember.ts` and the vendored
Composition API (missing exports/types); neither changed file was named in the
diagnostics. No request-test, driver, browser, localhost/socket, build, or
full suite was run by this worker.

The temporary Vitest runner copy was created in this worktree for the focused
run and removed afterward; no build output or temporary file remains.

## Next step

After the harness commits this candidate, the exact absolute driver command is:

```sh
sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-committed-driver-gate/run-central-m2-ordinary.sh /home/user/work/wt/ap2-m2-ordinary-marker-state-fixture-fix
```

That browser qualification remains unverified here.
