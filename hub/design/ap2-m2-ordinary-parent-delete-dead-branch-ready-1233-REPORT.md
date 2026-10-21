# App ordinary parent-delete dead-branch removal

## Change

- Removed the physically present parent-only `useClipDeletion` snapshot/native ingress from `src/tools/video-editor/hooks/clip-editing/useClipDeletion.ts`.
- Deleted only its helper, branch, toast/error path, and dependency-array entries. The remaining path still filters the requested clip IDs and calls `applyRowsEdit(..., { semantic: true })`, so grouped, occurrence, multi, mixed, unsupported, and pinned-group behavior remains on the existing fallback.
- Removed the direct unit test/import that asserted the deleted branch from `src/tools/video-editor/hooks/useClipEditing.test.ts`. Existing grouped-deletion assertions remain unchanged. The existing parent DELETE e2e proof was not modified or rerun.
- No changes to `useTimelineOps`, commit session, Provider, callers, native activation, pins, or shared dependencies.

Caller/test evidence for review:

- `useTimelineState.ts:982-993` still passes the existing command/editability plumbing to `useClipEditing`; this task did not alter that caller.
- `useClipDeletion.ts:13-35` is now the sole deletion implementation in this hook and preserves the shared `applyRowsEdit` fallback.
- `useClipEditing.test.ts:246-265` preserves the full-group semantic deletion assertion; lines 268-400 preserve grouped blocking assertions.
- Peer overlap doc: `/home/user/timeline-hub/hub/design/peer-app-to-app2-ordinary-cut-frontier-20261021T0735.md` says this parent-only ingress is already covered by the native DELETE proof and that the shared fallback must remain.

## Verification

- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts`
  - PASS: 3 files, 73 tests.
- `./node_modules/.bin/eslint src/tools/video-editor/hooks/clip-editing/useClipDeletion.ts src/tools/video-editor/hooks/useClipEditing.test.ts --max-warnings 0`
  - PASS.
- `flock /home/user/work/.app-tsc.lock ./node_modules/.bin/tsc -p tsconfig.app.json --noEmit`
  - FAILS on 29 pre-existing errors outside the changed files. No error points at the changed deletion files.

## TypeScript errors and owners

The resolved Composition declaration origin is `/home/user/work/app/node_modules/@banodoco/timeline-composition`, package version `0.0.8`. The App manifest/lockfile expects the protected vendor artifact `0.0.13`; the shared `0.0.8` install is the invalid graph called out by the task. The 28 Composition-contract errors below are therefore owned by that dependency graph, not this deletion diff:

- `src/tools/travel-between-images/components/ShotTimelinePreview.tsx:238` — TS2345, `ResolvedTimelineConfig` is not assignable to Composition `TimelineConfig` (`theme` optional vs required).
- `src/tools/video-editor/components/CompactPreview.tsx:46` — same TS2345 Composition `TimelineConfig` mismatch.
- `src/tools/video-editor/components/PropertiesPanel/VideoEditorAssetPanelSurface.tsx:47` — same TS2345 Composition `TimelineConfig` mismatch.
- `src/tools/video-editor/components/TimelineEditorShellCore.tsx:579` — same TS2345 Composition `TimelineConfig` mismatch.
- `src/tools/video-editor/compositions/TimelineRenderer.tsx:1625` — same TS2345 Composition `TimelineConfig` mismatch.
- `src/tools/video-editor/hooks/useDerivedTimeline.ts:71` — same TS2345 Composition `TimelineConfig` mismatch.
- `src/tools/video-editor/hooks/useRenderState.ts:596` — same TS2345 Composition `TimelineConfig` mismatch.
- `src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx:1` — TS2305, missing `CompiledCanonicalTransitions` export.
- `src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.tsx:4` — TS2305, missing `CompiledCanonicalTransitions` export.
- `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.ts:3` — TS2305, missing `CompiledCanonicalTransitions` export.
- `src/tools/video-editor/compositions/AudioTrack.tsx:15` — TS2305, missing `computeMediaTrim` export.
- `src/tools/video-editor/compositions/AudioTrack.tsx:16` — TS2305, missing `encodedEnvelopeSource` export.
- `src/tools/video-editor/compositions/AudioTrack.tsx:18` — TS2305, missing `EncodedEnvelopeSource` export.
- `src/tools/video-editor/compositions/TimelineRenderer.tsx:1` — TS2305, missing `CompiledCanonicalTransitions` export.
- `src/tools/video-editor/compositions/VisualClip.tsx:3` — TS2305, missing `getSanitizedPlaybackRate` export.
- `src/tools/video-editor/compositions/compiledAudioSourceClock.ts:1` — TS2305, missing `getSanitizedPlaybackRate` export.
- `src/tools/video-editor/compositions/compiledAudioSourceClock.ts:1` — TS2305, missing `computeMediaTrim` export.
- `src/tools/video-editor/compositions/playerEvaluation.ts:1` — TS2305, missing `compileCanonicalTransitions` export.
- `src/tools/video-editor/compositions/playerEvaluation.ts:3` — TS2305, missing `clipOpacity` export.
- `src/tools/video-editor/compositions/playerEvaluation.ts:5` — TS2305, missing `getSanitizedPlaybackRate` export.
- `src/tools/video-editor/compositions/playerEvaluation.ts:8` — TS2305, missing `CompiledCanonicalTransitions` export.
- `src/tools/video-editor/hooks/useClientRender.ts:3` — TS2305, missing `CompiledCanonicalTransitions` export.
- `src/tools/video-editor/lib/config-utils.ts:43` — TS2305, missing `computeMediaTrim` export.
- `src/tools/video-editor/compositions/TimelineRenderer.tsx:1309` — TS7006, `input` implicit `any` after the invalid Composition declaration.
- `src/tools/video-editor/compositions/TimelineRenderer.tsx:1607` — TS7006, `track` implicit `any` after the invalid Composition declaration.
- `src/tools/video-editor/compositions/VisualClip.tsx:641` — TS2339, `incomingPolicy` absent from the installed Composition `DrawPlan`.
- `src/tools/video-editor/compositions/playerEvaluation.ts:80` — TS7006, `input` implicit `any` after the invalid Composition declaration.
- `src/tools/video-editor/compositions/playerEvaluation.ts:85` — TS2554, installed Composition function accepts fewer arguments than App source supplies.

The remaining non-Composition error is an existing App/SDK surface mismatch:

- `src/tools/video-editor/commands/clipScalarGesture.ts:26` — TS2322, `elementRef` is allowed by local `ClipScalarArgs.clear` but not by the current `TimelinePatchOperation.clear` type.

## Decisions / limits

- The HOME status did not report this physical branch as already deleted, so I performed the bounded deletion.
- I did not convert the removed native assertion into a refusal/fallback expectation; the direct test for the deleted branch was removed, while all neighboring assertions were retained. The independent parent DELETE native proof remains the behavior evidence.
- No browser/full suite or new launcher was run under the lighter interim rule. No installs, shared dependency edits, pins, or repository docs were made.

## Handoff

The worktree contains only the two intended source/test modifications and is ready for independent diff review and remote merge. The invalid shared Composition install must be corrected by the coordinated dependency owner before the app TypeScript check can pass.
