# App parent carrier 42e fix-forward

## Result

Applied only the reviewed b58f-to-42e stale-peer correction onto current App
root `0d5009e18bee8e29f894dabf5db501a0fcea750f`.

- Current base tree: `b323667662d565526d7c2395733f26e2c6380378`
- Rejected/stale carrier: `b58f4f1b53f85fa6c2f15a8aabf144460a75300c`
- Reviewed correction reference: `42e47ae11e684cf4abafdab9b0867ea1c2a9a815`
- Correction reference parent: `ea38656fe62950440b36cafee780698cff2c3f9c`
- Working-tree diff SHA-256: `9ed1b46b9aabc2c4c921e70670bcb76628db1162344e1fd37d9fb964f7aa7dcf`

## Narrow diff

Changed only:

- `src/integrations/runtime/dataProvider.ts`
- `src/integrations/runtime/mediaImport.test.ts`

`prepareMediaImport` now calls the existing preparation boundary with native
selection capture enabled. `prepareAsset` calls that same boundary with capture
disabled, so legacy preparation remains unqualified and does not issue a
selection read. Native capture remains capability-gated, validates the exact
five fields/identities against the imported descriptor, freezes the original
selection, and carries it outside registry serialization. The test adds the
legacy no-selection-read control. No generated schema, wire/API, registry
field, helper, or consumer implementation was added.

## Verification

All runs used the approved private13 dependency graph, the snapshot preload,
`--configLoader=runner`, `--no-cache`, one worker, and no file parallelism:

```sh
TMPDIR="$RUN_TMP" NODE_OPTIONS="--require=$PRELOAD" \
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

Result: **12 files, 327 tests passed, 0 failed**.

Additional checks:

- `./node_modules/.bin/eslint --no-cache --max-warnings 0 src/integrations/runtime/dataProvider.ts src/integrations/runtime/mediaImport.test.ts` — passed.
- `git diff --check` — passed.
- `git status --short` — exactly the two intended modified files.

No full suite, typecheck, build, browser/live-socket run, install, shared
dependency write, generated change, reset, revert, merge, rebase, or history
rewrite was performed. No whole-row retirement claim is made; the native
consumer remains separate.
