Implemented D69 on base `61f0fb613a`, scoped to `placementService.ts` and its two focused test files.

- Retry requires a locally detected head-pair change **before durable intent creation**, bounded to one retry.
- Submitted Runtime conflicts/refusals remain durable; placement no longer clears or semantically replays them.
- Added actual handoff/LocalSaveSession controls for dependency, binding, field, selection, atomic-scope and stale-head conflicts, retained recovery, and single intent/publication.
- Frozen test bodies remain unchanged. Their sibling-publication hooks now exercise the permitted pre-authoring race.
- Production `placeGeneration → LocalSaveSession → RuntimeDataProvider` path remains intact.

Validation used `/opt/node20/bin/node` (`v20.20.0`):

```bash
NODE_OPTIONS='--import=data:text/javascript,globalThis.__dirname=process.cwd()+String.fromCharCode(47,99,111,110,102,105,103,47,116,101,115,116,105,110,103)' PATH=/opt/node20/bin:$PATH /opt/node20/bin/node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/shared/lib/placement/__tests__/placementService.test.ts src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts src/shared/lib/placement/__tests__/documentPlacement.test.ts
```

Old source: **5 new controls failed, 33 passed**, exposing duplicate requests. Final source: **41/41 passed**.

```bash
flock -w 600 /home/user/work/.app-tsc.lock bash -c 'for config in tsconfig.json tsconfig.app.json tsconfig.node.json; do printf "%s\n" "$config"; NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc -p "$config" --noEmit --pretty false --incremental false || exit; done'
PATH=/opt/node20/bin:$PATH /opt/node20/bin/node node_modules/eslint/bin/eslint.js src/shared/lib/placement/placementService.ts src/shared/lib/placement/__tests__/placementService.test.ts src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts --report-unused-disable-directives --max-warnings 0
git diff --check
```

All passed. Frozen declarations exactly match upstream `3881e944…`:

- `fcf8e413ce400977be026208d424ea211f4e464cf68db8fd2d7eece5fce8dd0d`
- `80bd6c080820a5855c56fdc48e9ed988627b0d7fbf8fda32afc18957d6a1183b`

No blockers. No full/browser/service suites run; live Runtime behavior remains independently unverified. The local safeguard adds a verified basis read per attempt. D69 commit message and `DONE` written. Next: harness commit, then cumulative independent review.