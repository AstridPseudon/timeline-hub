# Automatic-placement positives — current-tip qualification

## Scope

Applied only the approved 45-line test delta from `ad329e82f26ae777c2d24ec293d780049cae4c75` to the current App tip (`e5c71515d` base):

`src/shared/lib/placement/__tests__/documentPlacement.test.ts`

The four retained legacy positives cover:

- append extent scoped to the selected shot on a shared lane;
- inheritance of the first existing pinned group lane without track creation;
- the shared four-second hold for longer video media, while retaining registry duration;
- explicit collision shifting based on occupied start frames rather than intervals.

Existing test bodies and inputs are unchanged. No product code, canonical writer, owner policy, completion path, or native automatic-placement contract was altered. These tests preserve legacy shared-placement behavior only; they are not native auto-qualification, retirement, or three-products proof.

## Validation

All commands ran from `/home/user/work/wt/app-m2-auto-four-positives-current-qualify` using the standard physical deps8 cache at `/tmp/app-m2-coherent-deps8/node_modules`, the manager snapshot runner, `--configLoader=runner`, `--no-cache`, and `--maxWorkers=1` where applicable.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
  /tmp/app-m2-coherent-deps8/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 \
  src/shared/lib/placement/__tests__/documentPlacement.test.ts \
  src/shared/lib/placement/__tests__/placementService.test.ts \
  src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts \
  src/shared/hooks/shots/__tests__/addImageToShotHelpers.test.ts \
  src/shared/hooks/shots/__tests__/useShotGenerationMutations.test.ts \
  src/tools/video-editor/commands/clipMoveCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts
# PASS: 8 files, 183 tests

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
  /tmp/app-m2-coherent-deps8/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 \
  src/shared/lib/placement/__tests__/documentPlacement.test.ts
# PASS: 1 file, 11 tests

/tmp/app-m2-coherent-deps8/node_modules/.bin/eslint \
  src/shared/lib/placement/__tests__/documentPlacement.test.ts --no-cache
# PASS

git diff --check
# PASS

git diff --stat
# 1 file changed, 45 insertions(+)

git diff --exit-code ad329e82f26ae777c2d24ec293d780049cae4c75 -- \
  src/shared/lib/placement/__tests__/documentPlacement.test.ts
# PASS: current file is byte-equivalent to the approved delta commit

diff -u <(git show e5c71515d:src/shared/lib/placement/__tests__/documentPlacement.test.ts | sed '$d') \
  <(sed -n '1,100p' src/shared/lib/placement/__tests__/documentPlacement.test.ts)
# PASS: all pre-existing test bodies and inputs unchanged
```

No full suite, build, browser/e2e, TypeScript check, install, live socket, or native three-products qualification was run, as required. Manager review and merge gates remain separate.
