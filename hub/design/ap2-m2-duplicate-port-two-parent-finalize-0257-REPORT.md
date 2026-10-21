# Duplicate port two-parent finalization

## Result

The resolved App tree is unchanged and matches the approved delivery report.
No content changes were made.

- Resolved tree: `facd9c65accd086b1a15804acaf073620356722e`
- Delivery/base: `tl/ap2-m2-duplicate-row-port-reviewed-delivery-0252`, same
  `facd9c65accd086b1a15804acaf073620356722e`
- Common parent: `743d3464d1ed548986f29249bd9b4215baccf9bb`
- Harness second parent: `1be92c689c77efc3fe1d82eced116e86459139cf`

## Tree verification

The resolved tree contains the two current HOME helper files byte-for-byte,
with the same Git blobs as HOME `1be92c689`:

- `src/tools/video-editor/commands/trackReorderCapture.test.ts`
  (`61d123e0b63d3f3321afaa1218eda9ecef7e3292`)
- `src/tools/video-editor/commands/trackReorderCapture.ts`
  (`81ec771ab972da61654b96e45caa9506e8a797e7`)

The only additional source delta relative to HOME is the approved four-file
row-local port. Each file is byte-for-byte identical to approved candidate
`1bac66b9d`:

- `src/tools/video-editor/adapters/app/generationLookup.ts`
- `src/tools/video-editor/hooks/useAssetManagement.ts`
- `src/tools/video-editor/components/AstridTimelineEditor.tsx`
- `src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx`

The worktree was clean. No code, DTO, pin, activation, test, browser, full
suite, or Git metadata changes were made. Per the task, no unchanged-tree
tests were rerun. The delivery report's existing evidence remains the source
of the prior results: document-shots 11/11, track-reorder 8/8, and the
approved source review's 26 focused tests, controls, types, and lint.

## Live callers unchanged in this finalize step

The existing duplicate-generation menu path remains:

`ClipAction.tsx:241-251` -> `TimelineEditorCoreBody.tsx:807` ->
`TimelineEditorCore.tsx:839` -> `AstridTimelineEditor.tsx:544-625` ->
`generation-utils.ts` / `generationLookup.ts` ->
`useAssetManagement.prepareGenerationAsset` ->
`useTimelineCommandsService.addClip` -> the existing `parentClipAddMedia`
capture/verify/submit carrier.

The HOME-owned shared carrier and its callers were not changed. Other distinct
registration callers, including pinned-shot-group synchronization and
`useAddVariantAsGeneration.ts`, are also unchanged.

## Finalization

The harness `--merge-parent` input records
`1be92c689c77efc3fe1d82eced116e86459139cf` as the genuine second parent. The
harness may now create the two-parent merge using this unchanged resolved tree.
