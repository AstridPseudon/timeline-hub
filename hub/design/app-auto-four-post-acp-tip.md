# Automatic-placement positives — post-ACP current-tip qualification

## Scope

On App base `76316e78c43da695abe65037ea449f3352eb6d12`, applied only the
approved 45-line delta from `ad329e82f26ae777c2d24ec293d780049cae4c75` to
`src/shared/lib/placement/__tests__/documentPlacement.test.ts`.

The four retained legacy positives cover:

- append extent scoped to the selected shot on a shared lane;
- inheritance of the first existing pinned-group lane without track creation;
- the shared four-second hold for longer video media, while retaining registry
  duration;
- explicit collision shifting based on occupied start frames rather than
  intervals.

All pre-existing test bodies and inputs remain byte-identical. No product code,
canonical writer, owner policy, completion path, schema, pin, default, or
writer behavior changed. These are retained legacy shared-placement positives,
not native automatic-placement qualification or writer-retirement proof.

## Validation

Commands ran from `/home/user/work/wt/app-m2-auto-four-post-acp-tip` with the
read-only standard deps8 installation at `/tmp/app-m2-coherent-deps8/node_modules`.
Vitest used the notes-only snapshot preload, `--configLoader=runner`,
`--no-cache`, and `--maxWorkers=1`.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs /tmp/app-m2-coherent-deps8/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/shared/lib/placement/__tests__/documentPlacement.test.ts src/shared/lib/placement/__tests__/placementService.test.ts src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts src/shared/hooks/shots/__tests__/addImageToShotHelpers.test.ts src/shared/hooks/shots/__tests__/useShotGenerationMutations.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts
```

PASS: 8 files, 183 tests, exit 0.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs /tmp/app-m2-coherent-deps8/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/shared/lib/placement/__tests__/documentPlacement.test.ts
```

PASS: 1 file, 11 tests, exit 0.

```sh
/tmp/app-m2-coherent-deps8/node_modules/.bin/eslint src/shared/lib/placement/__tests__/documentPlacement.test.ts --no-cache
git diff --check
git diff --exit-code ad329e82f26ae777c2d24ec293d780049cae4c75 -- src/shared/lib/placement/__tests__/documentPlacement.test.ts
diff -u <(git show HEAD:src/shared/lib/placement/__tests__/documentPlacement.test.ts | sed '$d') <(sed -n '1,100p' src/shared/lib/placement/__tests__/documentPlacement.test.ts)
```

PASS: ESLint, whitespace, approved-delta equivalence, and unchanged old-body
and input audit. A separate allowlist check also passed: exactly one changed
file, 45 additions, and zero deletions.

No full suite, build, browser/e2e, TypeScript, install, live socket, or native
three-products qualification was run. The later post-batch full suite remains
the manager/orchestrator gate.
