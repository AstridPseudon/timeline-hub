# A2 D141 protected review — PASS

Candidate `a1955216f947f9d84c3154d3bd715e65bc945452`, tree `af51793b7cc9b2d0426e629bce1d9e4529a7edb6`, direct parent `867cb2737af1b46dc608c7cd37c349e920fe9422`. Worktree was clean before and after review; no product files were modified.

## Commands run by this reviewer

All commands used Node 20 and private Vitest config/cache paths; shared dependencies were read-only.

```sh
PATH=/opt/node20/bin:$PATH /opt/node20/bin/node node_modules/vitest/vitest.mjs run src/tools/video-editor/lib/shot-group-pack-commands.test.ts src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts --maxWorkers=3 --no-cache --configLoader=runner --config /tmp/w-8b9db9f860/vitest-d141.config.mjs
```

Result: exit 0; 2 files and 22 tests passed (shot-group 6/6, Workspace v1 guards 16/16).

```sh
PATH=/opt/node20/bin:$PATH npx --no-install tsc --noEmit -p tsconfig.app.json
PATH=/opt/node20/bin:$PATH npx --no-install tsc --noEmit -p tsconfig.node.json
PATH=/opt/node20/bin:$PATH npx --no-install eslint src/integrations/runtime/dataProvider.ts src/tools/video-editor/data/DataProvider.ts src/shared/lib/placement/placementService.ts src/tools/video-editor/lib/shot-group-pack-commands.ts src/tools/video-editor/lib/shot-group-pack-commands.test.ts
git diff --check
```

All four commands exited 0 with no diagnostics.

## Independent conservation checks

- Parsed original and candidate protected test ASTs with TypeScript ESTree. Removing only the added `loadTimelineCommandBasisWithDisplay` mock method (range `[2634,3377]`, 743 added bytes) restored the entire original file byte-for-byte; normalized ASTs then matched. All six original titles were enumerated and unchanged. This also proves fixture and pre-existing mock bodies/preimages are unchanged, including the `loads=2` assertion and original commit-side subtraction.
- `git diff --name-status base..candidate` listed exactly the five approved files; no deletions or out-of-scope paths.
- Base ancestry check passed; final commit/tree/parent hashes are recorded in `source-manifest.json`.
- The candidate’s reviewed source path preserves a cold combined basis/display read, exact revision/publication pairing, full closure validation, the post-validation fresh pair, bounded retry, no-intent-on-local-stale behavior, accepted canonical adoption, and the existing outbox/Runtime commit path.

## Reviewed author evidence

The author’s private six-control cold/await source exercise was read and treated as source-path evidence, not as live Runtime/auth/pack qualification. It covers numeric display-version turnover, publication mismatch across the combined-reader await, two cold caller basis reads, revision/publication changes after awaited preflight, single-use consumption, and post-validation mismatch before owner/transform.

No full App, browser, live socket, live Runtime, pack-task, schema/wire, or P1/P2/P3 integrated-head suite was run or claimed.
