# App parent carrier fix-forward

## Result

Applied only the reviewed correction from `42e47ae11e684cf4abafdab9b0867ea1c2a9a815`
(`ap2-m2-parent-native-eligibility-repair`) onto current App root `0d5009e18bee8e29f894dabf5db501a0fcea750f`.
The current-root tree before the uncommitted fix is
`b323667662d565526d7c2395733f26e2c6380378`; the reviewed commit tree is
`66f515a58d242660accbae204396c8db36e52b49` and its parent is
`ea38656fe62950440b36cafee780698cff2c3f9c`.
The rejected already-merged carrier was `b58f4f1b53f85fa6c2f15a8aabf144460a75300c`.
The working-tree binary diff SHA-256 is
`f899a3ad3c0205870f360c985635a0aeb77aeb214b07294a2ada102f030f29c7`.

## Exact old/new paths

The reviewed carrier has the same six paths on both sides:

- `src/integrations/runtime/dataProvider.ts` → `src/integrations/runtime/dataProvider.ts`
- `src/integrations/runtime/mediaImport.test.ts` → `src/integrations/runtime/mediaImport.test.ts`
- `src/tools/video-editor/commands/provisioning.ts` → `src/tools/video-editor/commands/provisioning.ts`
- `src/tools/video-editor/data/AssetResolver.ts` → `src/tools/video-editor/data/AssetResolver.ts`
- `src/tools/video-editor/hooks/useAssetManagement.ts` → `src/tools/video-editor/hooks/useAssetManagement.ts`
- `src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx` → `src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx`

At this current root, only the first, second, and sixth paths needed a
working-tree change; the other three production carrier paths already matched
the reviewed replacement. No App-owned move, label, `None`, delete, name, or
automatic sections were changed.

`prepareMediaImport` now captures the existing Runtime selection only at the
native-eligible preparation boundary. `prepareAsset` uses the same preparation
machinery with capture disabled, so legacy preparation remains unqualified and
does not issue a `/media-selection` read. Native capture validates the exact
asset, generation, variant, object, and catalog-digest selection carrier
without changing the wire shape; mismatch still refuses. The carrier remains
outside registry serialization and is frozen before propagation.

## Verification

Tests used the established private13 graph
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/full-main574-public13-8bd8f741/private13/node_modules`,
the snapshot preload
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs`,
`--configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism`, and
private `TMPDIR`. The worktree `node_modules` symlink was restored to the
shared read-only install after each run.

The exact broader command was:

```sh
PRIVATE13=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/full-main574-public13-8bd8f741/private13/node_modules
PRELOAD=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs
TMPDIR=/tmp/tl-app-parent-carrier-rejected-fix-forward-private13 NODE_OPTIONS="--require=$PRELOAD" \
node "$PRIVATE13/vitest/vitest.mjs" run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/mediaImport.test.ts \
  src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx \
  src/integrations/runtime/dataProvider.parity.test.ts \
  src/integrations/runtime/dataProvider.test.ts \
  src/tools/video-editor/contexts/VideoEditorProvider.test.tsx \
  src/tools/video-editor/commands/media.test.ts \
  src/tools/video-editor/commands/parentClipAddCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/hooks/useAssetOperations.test.tsx \
  src/tools/video-editor/hooks/useExternalDrop.test.tsx \
  src/features/gallery/hooks/useDropToGeneration.test.tsx
```

The reviewed 175-test command used the same prefix and flags with only the
first five paths through `VideoEditorProvider.test.tsx`.

- Reviewed cohort: the five files `mediaImport.test.ts`,
  `useAssetManagement.mediaImport.test.tsx`, `dataProvider.parity.test.ts`,
  `dataProvider.test.ts`, and `VideoEditorProvider.test.tsx` — **5 files,
  175 tests passed, 0 failed**.
- Broader requested six-neighbor regression surface plus reviewed cohort: the preceding five plus
  `commands/media.test.ts`, `commands/parentClipAddCapture.test.ts`,
  `commands/commitSession.test.ts`, `commands/commitOutbox.test.ts`,
  `hooks/useAssetOperations.test.tsx`, `hooks/useExternalDrop.test.tsx`, and
  `features/gallery/hooks/useDropToGeneration.test.tsx` — **12 files, 327
  tests passed, 0 failed**.
- Scoped ESLint over all six carrier paths — **passed**.
- `git diff --check` — **passed**.

Exact lint/check commands:

```sh
./node_modules/.bin/eslint --no-cache --max-warnings 0 src/integrations/runtime/dataProvider.ts src/integrations/runtime/mediaImport.test.ts src/tools/video-editor/commands/provisioning.ts src/tools/video-editor/data/AssetResolver.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx
git diff --check
```

The carrier tests directly prove that legacy `prepareAsset` makes no
unqualified selection read and that an exact media/object mismatch refuses.
This result does not claim native media activation, `addClip` consumer wiring,
or writer retirement; those remain separate work.

No full suite, browser/live-socket run, build, project typecheck, install,
reset, revert, merge, rebase, or shared dependency/cache write was performed.
