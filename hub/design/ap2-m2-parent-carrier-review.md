# ap2-m2-parent-carrier-review

## Decision: REQUEST CHANGES

The private preparation/carrier proposal has the right carrier shape and identity checks, but it is not safe to qualify or integrate as written. It makes every completed `prepareMediaImport` call require a new media-selection read, including existing upload/import callers that are not native parent-media consumers.

## Review basis

- Proposal: `b58f4f1b53f85fa6c2f15a8aabf144460a75300c` (`feat(app): carry original media selection through preparation`), parent `590c19795111fd1891bbd50a5f8d48bef3505a26`.
- Assigned integration base: `ea38656fe62950440b36cafee780698cff2c3f9c`.
- The six relevant proposal hunks apply cleanly to the current integration base (`git apply --check` passed); qualification was performed in a disposable current-base copy. No App, Agent, Runtime, or Composition shared worktree was modified.
- Proposal scope is six App files: four production files and two tests. The proposal has 18 total diff hunks; its production carrier/API changes are confined to App and use the existing Runtime client wrapper.

## What is correct

- `toPreparedMediaImport` obtains the selection from the existing scoped `AstridRuntimeClient.getProjectMediaSelection(imported.project, ...)` wrapper. No Runtime endpoint, generated DTO, store, or public command is added.
- The read is keyed by the imported `asset_id`, `generation_id`, and `variant_id`, then checked against the original project (before conversion), all three IDs, and the exact imported `entry.object_id`. `catalog_digest` is carried from Runtime and is not inferred from a content hash or refreshed later.
- `PreparedMediaImport.mediaSelection` is optional, so an already-created/unqualified preparation can remain unqualified. `prepareGenerationAsset` forwards the same value into `TimelineProvisionedAsset`; the direct carrier test proves this propagation.
- `AssetRegistryEntry` remains unchanged. The proposal stores the selection beside `entry`, and `activeRegistry` continues to receive only `prepared.entry`; the direct serialization assertion confirms no `catalog_digest` enters registry serialization.
- Native parent `addClip`/session consumption, exact verified-media reads, retry/reload, and legacy-writer retirement remain separate and are not claimed by this review.

## Blocking finding

`src/integrations/runtime/dataProvider.ts:1211` now awaits `toPreparedMediaImport`, and `:1527` unconditionally calls `/v1/projects/:project/media-selection` for every completed `prepareMediaImport`. This changes the existing preparation contract for `prepareAsset`/`uploadAsset` and other valid import paths. Current import neighbors use a valid completed import fixture without that optional read and now fail with `unexpected GET .../media-selection`.

Required repair: keep legacy/pending and unrelated successful preparation behavior working until a native consumer is eligible. Narrow the selection capture to the original preparation boundary owned by the native parent-media path, or return an unqualified `PreparedMediaImport` when the legacy path has no selection capability. Do not reacquire or synthesize a selection later; a native consumer must fail closed when `mediaSelection` is absent, and a returned selection mismatch must still refuse rather than downgrade silently.

## Exact API/storage scope

The acceptable scope remains:

- App-only changes to `RuntimeDataProvider` preparation and the existing `PreparedMediaImport` and `TimelineProvisionedAsset` internal carriers.
- One existing scoped Runtime query wrapper for original selection, plus no new query/verify endpoint or wire field. The verify wrapper is for the later native consumer and is not part of this carrier patch.
- No `AssetRegistryEntry` field, canonical registry serialization change, store schema, public command, Runtime schema, generated client, `addClip`, or commit-session change.

## Evidence

Commands run against the disposable current-base copy, with shared `node_modules` symlinked read-only and Vitest cache disabled:

1. Direct proposal tests:

   `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/mediaImport.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx`

   Result: **2 files, 9 passed, exit 0**.

2. Existing import neighbors:

   The same command with `src/integrations/runtime/dataProvider.parity.test.ts`, `src/integrations/runtime/dataProvider.test.ts`, and `src/tools/video-editor/contexts/VideoEditorProvider.test.tsx` added.

   Result: **5 files, 174 tests: 168 passed, 6 failed, exit 1**. The six failures are existing `dataProvider`/parity upload and fresh-prepared-media cases, all failing on the unexpected `/media-selection` GET before their prior assertions run. The VideoEditorProvider and the two direct proposal files passed.

3. Lint:

   `./node_modules/.bin/eslint --no-cache --max-warnings 0 src/integrations/runtime/dataProvider.ts src/integrations/runtime/mediaImport.test.ts src/tools/video-editor/commands/provisioning.ts src/tools/video-editor/data/AssetResolver.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx`

   Result: **passed**.

4. Type check:

   `./node_modules/.bin/tsc --noEmit --pretty false`

   Result: **passed**.

5. Patch checks:

   `git -C /home/user/work/app apply --check /tmp/ap2-m2-parent-carrier-review.omczxC/proposal.patch` and `git -C /home/user/work/app diff --check b58f4f1b5^ b58f4f1b5 -- <six proposal files>`.

   Result: **both passed**. Shared worktree status checks for App, Agent, Runtime, and Composition were clean.

No full, browser, live-socket, Runtime pytest, source edit, new test, dependency, pin, commit, merge, or ledger run was made. The only temporary Vitest config adjustment was in the disposable copy to resolve existing ESM `__dirname` usage; no repository config was changed.

## Next step

Repair the preparation boundary so existing import neighbors retain their current positives while the native path receives exactly one frozen original selection. Re-run the direct carrier tests and the actual import-neighbor files; only then hand the carrier to the separate native addClip/session consumer review.
