# AP2 M2 parent reviewed projection delivery

## Result

Delivered only the independently approved two-file wrong-target projection fix
from `tl/ap2-m2-parent-drop-projection-safety-current-port-0832` onto latest
HOME App source. Changed paths are exactly:

- `src/tools/video-editor/lib/drop-position.ts`
- `src/tools/video-editor/lib/drop-position.test.ts`

Approved donor blob identity is exact:

- `drop-position.ts`: `c634ede997c8ca9c197fcf17d84fcf2630c69889`
- `drop-position.test.ts`: `4ed1d4cde67f32f1b573baafea400ae58bc4dd22`

## Identities

- Latest HOME base: `hub/tl/integration` at
  `32b74fdea165816226b6f0727a16817a6a1a79c3`, tree
  `a3ddc2997e6460bab77d1e4ef7c1ac98ee21ad65`.
- Original worker base: `e2267a418a89d659c1a70524b17dde631f12fd16`.
- Approved source branch:
  `tl/ap2-m2-parent-drop-projection-safety-current-port-0832` at
  `acb97771b70f97d7a25652876e6154e315f4ccb8`, tree
  `8cbeba3a752e2da9b2b6151dce08503bbc07ddc6`.
- Current resolved worktree base after merge-forward: latest HOME
  `32b74fdea…`; final harness commit/tree is pending harness commit.
- Outside the two approved paths, the resolved worktree equals latest HOME;
  `git diff --name-only` listed only those two paths.

## Safety and callers

The correction maps planner rows by rendered `current.tracks` IDs, retaining
existing row actions and using an empty action list only for a missing row. It
preserves the S1 occurrence refusal, actions-by-ID behavior, data-lane refusal,
empty-track behavior, and accepted-state semantics. No session, Provider,
harness, door, preview, retry, writer, proof spec, ORCH artifact, or pin was
copied or changed.

Inspected live callers are unchanged:

- `useDragCoordinator.ts:155-170` consumes `computeDropPosition`.
- `useExternalDrop.ts:621-650` finalizes external drops.
- `external-drop-utils.ts:453-457,512-525` carries the selected target.
- `useAssetManagement.ts:303-317` performs native prepared placement.

## Evidence

Focused Vitest command, run once:

`node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/lib/drop-position.test.ts src/tools/video-editor/lib/clip-drag-planner.test.ts`

Result: `2 files, 39 tests passed`.

Lint passed:

`node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/lib/drop-position.ts src/tools/video-editor/lib/drop-position.test.ts`

`git diff --check` passed. No browser, build, actual journey, install,
socket, full suite, or central test-service run was performed.

## Merge-forward

Ran immediately before finalization:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/merge-forward ap2-m2-parent-reviewed-projection-delivery-0844 hub/tl/integration`

It hit the expected read-only `ORIG_HEAD.lock` failure, with no conflicts or
markers; the worktree aligned to latest HOME. The harness fallback records
original worker base `e2267a418a89d659c1a70524b17dde631f12fd16` as the second
parent. No direct merge, commit, rebase, push, or ref mutation was performed.
