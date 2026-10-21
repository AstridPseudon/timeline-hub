# Independent review: parent prepared-video cut1220

Decision: **REJECT** `49efc69c5` for merge.

The refusal is data-safe, but it is not a migration of the original supported
gesture. The mounted Gallery “Add to video editor” caller in
`src/domains/media-lightbox/hooks/useAddToVideoEditor.ts:118-126` constructs a
video `preparedAsset` from a `GenerationRow` and calls `commands.addClip` with
only `time`; it carries no `mediaSelection`. The candidate’s guard at
`src/tools/video-editor/hooks/useTimelineCommandsService.ts:555-570` therefore
refuses that exact gesture before the previous local writer. There is no
existing lookup or preparation step that supplies the required five fields
(`asset`, `generation_id`, `variant_id`, `object_id`, `catalog_digest`) for this
Gallery caller.

The existing native carrier is narrower: `useAssetManagement` copies
`mediaImport.mediaSelection` at `:257-259`, and its Runtime-import tests pass a
qualified selection through `handleAssetDrop` to `commands.addClip`. The native
command-session test proves capture/verify/finish/submit and the zero-local-row
result for that already-qualified path. Those are different gestures and do
not establish equivalent success for mounted Gallery video. The staged Gallery
path also remains a separate local `commands.apply(place-prepared-media)` flow
at `VideoEditorProvider.tsx:619-642`; the candidate neither migrates nor
qualifies it.

Image remains positive, and the guard leaves after-anchor and replacement/Main
producer shapes on their existing path. That does not cure the lost simple
video-add positive. The changed Provider test is a valid refusal/data-safety
assertion, but it is a negative test only; no mounted Gallery-video positive
exists. The Provider test file is HOME-owned and was not edited here.

## Verification

- `node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx src/tools/video-editor/hooks/useAddVariantAsGeneration.test.tsx`
  - PASS: 6 files, 128 tests.
- `flock /home/user/work/.app-tsc.lock node_modules/.bin/tsc -p tsconfig.app.json --noEmit`
  - FAIL: exit 2, 29 diagnostics listed below. This is the actual app project
    check; no root `tsc` result was treated as green.
- `node_modules/.bin/eslint --max-warnings 0 src/tools/video-editor/hooks/useTimelineCommandsService.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx`
  - PASS: exit 0.
- `git diff --check`
  - PASS.
- No full suite, browser journey, or localhost/live-socket suite was run.

### Remaining `tsconfig.app.json` diagnostics

The actual declaration origin is the protected shared install
`/home/user/work/app/node_modules/@banodoco/timeline-composition`, whose
`package.json` reports **0.0.8**. This is invalid for the App pin: the App
package/lockfile and bundled artifact are 0.0.13. No shared dependency was
modified.

Composition package/API mismatch (owner: protected Composition package/pin;
the shared 0.0.8 declaration is stale):

- `PreviewPanel/RemotionPreview.tsx:1`, `PreviewPanel/TimelineFramePreview.tsx:4`, `PreviewPanel/useVideoEditorPreviewComposition.ts:3`, `TimelineRenderer.tsx:1`, `playerEvaluation.ts:8`, `useClientRender.ts:3` — missing `CompiledCanonicalTransitions`.
- `AudioTrack.tsx:15-18` — missing `computeMediaTrim`, `encodedEnvelopeSource`, and `EncodedEnvelopeSource`.
- `VisualClip.tsx:3` — missing `getSanitizedPlaybackRate`.
- `compiledAudioSourceClock.ts:1` — missing `getSanitizedPlaybackRate` and `computeMediaTrim`.
- `playerEvaluation.ts:1,3,5` — missing `compileCanonicalTransitions`, `clipOpacity`, and `getSanitizedPlaybackRate`.
- `playerEvaluation.ts:85` — call supplies 13 arguments where the installed declaration accepts 6–12.
- `config-utils.ts:43` — missing `computeMediaTrim`.
- `VisualClip.tsx:641` — `DrawPlan` lacks `incomingPolicy`.

Other App/current-tree diagnostics:

- `ShotTimelinePreview.tsx:238`, `CompactPreview.tsx:46`, `VideoEditorAssetPanelSurface.tsx:47`, `TimelineEditorShellCore.tsx:579`, `TimelineRenderer.tsx:1625`, `useDerivedTimeline.ts:71`, `useRenderState.ts:596` — `ResolvedTimelineConfig.theme` is `string | undefined` but the target `TimelineConfig.theme` is `string` (7 diagnostics; current App/Composition contract boundary).
- `commands/clipScalarGesture.ts:26` — `clear` can include `elementRef`, but `TimelinePatchOperation.clear` excludes it (App2-owned known error).
- `TimelineRenderer.tsx:1309` and `:1607`, `playerEvaluation.ts:80` — implicit-`any` parameters (3 current App diagnostics).

No product edit was made. Recommended next step is to reject this cut and
qualify the mounted Gallery-video carrier through the existing Runtime
media-import/selection path, with a same-gesture success test plus await/epoch
and zero-legacy-write assertions before attempting the deletion again.
