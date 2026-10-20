# AP2 M2 ordinary final committed runner

## Result

Applied the reviewed `46d540f6c` legacy-hold fix to the ordinary candidate. A
cross-track or mixed alignment batch now keeps every hold member on the guarded
legacy `{ hold, mode: 'merge' }` envelope; wholly same-track native batches
retain `{ values: { hold }, clear: [] }`. Native execution and the joined
ordinary journey source were otherwise unchanged.

Added the committed runner `scripts/testing/run-central-m2-ordinary.sh` and
registered `app e2e-m2-ordinary-integration`. The runner fails closed before
temporary setup unless the authoritative source repos resolve the exact full
commits and trees below, verifies Composition 0.0.13, rebuilds a private
per-run node graph/bin directory, builds the hosted App, and runs only:

```text
npm run test:e2e:three-products -- --grep "M2 ordinary extension batch"
```

The previous invalid Runtime value ending `...26a2` is explicitly absent. The
valid Runtime SHA is the 40-character `...e26a` value below.

## Exact identities

| Source | Commit | Tree |
|---|---|---|
| Agent | `8130a401bf44a518d5a40ae274d398b8c560be55` | `236c3e57e0265c52b81ba8085de3193026176bff` |
| Runtime | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |
| Composition | package `0.0.13` | tarball SHA `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` |

App pre-commit base is `684227f755a88d7acab8290d1cb2b1e78ba9bd47`, tree
`d1ee570825d22db6bea78bc109679facc49b164b`. The tracked source patch SHA is
`cff6ccd1af6200f5c8fac7e5646427ae5d1cbbf128f56e1b74546b3b04f257b3`; the
runner file SHA256 is
`6f0e76501a28057d0fec0be7e5e8c1648872847275acf61203706739dc181026`.
The harness-generated post-change commit SHA is not available until worker
exit; central execution must wait for that clean committed source.

## Validation

Passed:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/commands/ordinaryMoveMember.test.ts \
  src/tools/video-editor/commands/ordinaryScalarMember.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts
# 6 files, 112 tests passed

node_modules/.bin/eslint \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/dev/scene-phase-markers/extension.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts --max-warnings 0
sh -n scripts/testing/run-central-m2-ordinary.sh
node_modules/.bin/playwright test tests/e2e/local/three-products.spec.ts \
  --config playwright.three-products.config.ts --list
# 10 tests collected, including M2 ordinary extension batch
git diff --check
node --test scripts/testing/current013-integration.test.mjs
# 1 source-guard test passed
```

The exact Agent/Runtime commit and tree guards, Composition 0.0.13/tarball
guard, and bad-suffix rejection were also run directly and passed. No browser,
localhost, socket, full suite, or central run was performed in this worker.

## Central handoff

After the harness commits the worktree and confirms it is clean, run exactly:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-final-committed-runner e2e-m2-ordinary-integration --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Record the harness-generated App commit SHA before queueing. The current App
readiness fix remains unavailable in the reviewed handoff; no App-owned
initialization was edited or overlaid.
