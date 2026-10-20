# ap2-m2-parent-native-eligibility-repair

Implemented the carrier repair in the private App worktree.

## Patch

- Kept `MediaSelection` optional on `PreparedMediaImport` and
  `TimelineProvisionedAsset`, outside `AssetRegistryEntry`.
- Captured the existing five-field selection once from the existing
  `prepareMediaImport` boundary when the Runtime client exposes the existing
  selection read capability.
- Routed legacy `prepareAsset` through the same preparation logic with native
  capture disabled, so unrelated registry preparation does not issue a
  `/media-selection` read and remains unqualified.
- Preserved strict project, asset, generation, variant, and object identity
  checks; a mismatch refuses.
- Propagated the frozen carrier through `prepareGenerationAsset`.

## Evidence

- Direct carrier/import tests:
  `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.worker.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/mediaImport.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx`
  — 2 files, 10 passed.
- Actual import neighbors:
  `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.worker.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/dataProvider.parity.test.ts src/integrations/runtime/dataProvider.test.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx`
  — 3 files, 165 passed. The six previous unexpected `/media-selection` failures are resolved.
- TypeScript: `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- ESLint: `./node_modules/.bin/eslint --no-cache --max-warnings 0 src/integrations/runtime/dataProvider.ts src/integrations/runtime/mediaImport.test.ts src/tools/video-editor/commands/provisioning.ts src/tools/video-editor/data/AssetResolver.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx` — passed.
- `git diff --check` — passed.

The Vitest config used above was a temporary private copy because the checked-in
config currently evaluates `__dirname` under the runner; it was removed after
testing. No full, browser, socket, Runtime, dependency, generated, wire, store,
pin, or Git operations were run. Real `addClip` consumer wiring remains
separate and unverified here.
