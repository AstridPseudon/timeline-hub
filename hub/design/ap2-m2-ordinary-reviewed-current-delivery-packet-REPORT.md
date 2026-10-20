# AP2 M2 ordinary reviewed current delivery packet

## Result

Prepared the approved ordinary source delta on current App HOME for harness delivery. No browser, localhost/live socket, request-test, full suite, hosted build, Viewing fallback restoration, schema/pin/dependency change, or whole-row deletion was performed.

## Exact lineage and diff

- Current base: `hub/tl/integration` = `e9d04f4bf0b9c06d184541655f20a4ca832d0370`.
- Donor parent/base: `480db7febe624fe4658a75cbdb66ed5de84c2c61`.
- Donor applied: `966472b615024d8f874379b4e6a5eb3df0145419`, `fix(timeline): repair ordinary mounted journey gate`.
- Donor delta: 9 files, 223 insertions, 12 deletions.

Applied only the donor's reviewed changes:

- exact ten-command generic-capture occurrence read order;
- standalone authoring admission before navigation;
- Scene Phase Markers constants and normal host admission;
- ordinary five-member fixture, exact parity helper, and capture assertions;
- disjoint literal `S1` Agent fixture;
- independent pre-edit + Agent-C undo oracle retaining complete parent payload, shot/internal closure, dependency manifest, opaque/order/legacy/credential/immutable-closure assertions;
- focused authoring/marker regression.

The four added-file blobs match donor blobs exactly. No shared-first patch was needed. Existing current settings/latest harness/7d/5a/trim work was preserved.

Review lineage:

- Independent approval: `design/ap2-m2-ordinary-undo-conversion-review-gate-REPORT.md`; it approved the independent pre-edit + disjoint-`S1` oracle and found no circular expected value or weakened assertion.
- Donor central attempt `...-30322` failed before journey assertions because the hosted build could not import the already-deleted `src/tools/video-editor/lib/theme-api.fallback.tsx`; no journey evidence was claimed and no fallback was restored here.

## Verification

Passed:

```
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/ordinaryRealBatch.test.ts
# 2 files, 17 tests passed

node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/test/threeProductsAuthoring.test.ts
# 1 file, 4 tests passed

ASTRID_CHECKOUT=$PWD/vendor/astrid-browser VITEST_LANE=checkout node --require ./.vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/dev/localExtensions.catalog.test.ts
# 1 file, 2 tests passed

node_modules/.bin/eslint --no-warn-ignored --max-warnings 0 [all 7 changed TypeScript files]
# passed

node_modules/.bin/playwright test tests/e2e/local/three-products.spec.ts --list --config playwright.three-products.config.ts
# Total: 11 tests in 1 file; listing only, no browser run

git diff --check
# passed
ordinary_real_batch.json JSON parse
# valid
```

`node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false` failed on pre-existing baseline errors in Settings/Runtime-generated types, vendored Composition exports, and existing clip-deletion typing. No touched file appeared in the diagnostics.

The first catalog attempt with `ASTRID_CHECKOUT=/home/user/work/agent` exposed that shared Agent HOME has advanced to `haus.astrid.live-scenes`, while this App base expects the pinned Three.js catalog. It was not imported or changed; the valid pinned `vendor/astrid-browser` bounded configuration passed.

## Merge-forward limitation

Attempted:

```
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/merge-forward ap2-m2-ordinary-reviewed-current-delivery-packet hub/tl/integration
```

It failed with `rc=128`: Git could not create `/home/user/banodoco/reigh-app/.git/worktrees/ap2-m2-ordinary-reviewed-current-delivery-packet/ORIG_HEAD.lock` because the Git filesystem is read-only. Status remains ordinary uncommitted changes with no unmerged paths or merge markers. The harness must perform any merge/commit operation.

## Next steps

Harness commits this packet, then the owning manager decides when the existing Viewing build gap is resolved and a fresh central ordinary browser qualification is appropriate. The prior `30322` result is not journey evidence.

