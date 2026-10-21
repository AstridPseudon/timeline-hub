# App2 transcript digest consumer stage-ready — 2026-10-21

## Result

Prepared the smallest dormant App-owned carrier patch for the forthcoming
Runtime PUBLIC018 ordinary transcript result.

Changed only:

- `src/tools/video-editor/data/typed/projectTranscript.ts`
  - preserves optional server-derived `content_digest` on ordinary transcript
    resources;
  - validates the exact lower-case `sha256:<64 hex>` form while accepting old
    resources that omit the field;
  - maps a digest-bearing result to the existing
    `DocumentPin { document_id, version, content_digest }` with
    `transcriptDocumentPin`.
- `src/tools/video-editor/data/typed/projectTranscript.repository.test.ts`
  - direct list/get/create/update carry-through;
  - exact original P1 pin and key presence;
  - old replay omission returns no native pin;
  - null/malformed rejection and valid key-presence recovery.

No HOME-owned `src/integrations/runtime/dataProvider.ts` or shared session
hunks changed. No generated files, root/runtime pins, package graph, live host
caller, writer deletion, native activation, browser lookup, content hashing,
or latest-document lookup changed. Existing successful snapshot association
remains the only live association path.

The existing dormant `transcriptAssociateCapture` implementation is not
duplicated or modified. The new mapper is only a result seam; no live caller
uses it yet.

## Current dependency and disposition

Runtime status currently identifies the reviewed PUBLIC018 candidate as
`8ed79a31e66d02e2e2e7062b9a368e3266cea9db` /
`f52aa1456fc6b65a7c634d4876aa4d6adfd9f822`, with the ordinary Agent
`0cfa4ad14664cec9df430637d8f68f2d1f2b487f` and derived document digest
source `4e`. Runtime says the coordinated release/pin unit still awaits
the independently reviewed Agent and HOME App normal-018 stages.

The current App status still records published014 as current and keeps the
HOME-owned normal generated/provider/session/pin work separate. Therefore this
is source/test evidence only. It must not be activated on014 or treated as a
qualified native association until the HOME stage supplies the digest-bearing
generated/runtime result and the containing original native target tests cover
new association, old replay refusal with draft preservation, reload/retry,
inverse, and zero-legacy behavior. The old replay behavior is deliberately
compatible at this seam: missing digest is preserved as missing and maps to
`undefined`, so the future native proposal can visibly refuse while leaving
the existing draft/outbox and snapshot path intact.

The initial-pin authority question was not revisited; this patch consumes only
the agreed server-produced field.

## Evidence

All targeted commands used the existing protected shared install. No installs
or shared dependency/cache writes were performed.

- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/data/typed/projectTranscript.repository.test.ts src/integrations/runtime/projectTranscriptRepository.test.ts src/tools/video-editor/lib/project-transcript-host.test.ts`
  - PASS: 3 files, 32 tests.
- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/transcriptAssociateCapture.test.ts src/tools/video-editor/data/typed/projectTranscript.repository.test.ts src/integrations/runtime/projectTranscriptRepository.test.ts src/tools/video-editor/lib/project-transcript-host.test.ts`
  - PASS: 4 files, 39 tests.
- `./node_modules/.bin/eslint src/tools/video-editor/data/typed/projectTranscript.ts src/tools/video-editor/data/typed/projectTranscript.repository.test.ts --report-unused-disable-directives --max-warnings 0`
  - PASS.
- `git diff --check`
  - PASS.
- `flock /home/user/work/.app-tsc.lock node_modules/.bin/tsc -p tsconfig.app.json --noEmit`
  - EXIT 2. No diagnostic points at either changed file. The actual graph resolves
    `node_modules/@banodoco/timeline-composition` to shared
    `/home/user/work/app/node_modules/@banodoco/timeline-composition`,
    version 0.0.8, while this worktree declares 0.0.13; this is the explicitly
    invalid protected graph, not a green App check.

### Remaining real App typecheck diagnostics

The 0.0.8 Composition dependency owns the following missing exports/type
mismatches:

- `ShotTimelinePreview.tsx:238`: `ResolvedTimelineConfig` is not assignable to `TimelineConfig` (`theme` may be undefined).
- `CompactPreview.tsx:46`: same `ResolvedTimelineConfig`/`TimelineConfig` mismatch.
- `PreviewPanel/RemotionPreview.tsx:1`,
  `PreviewPanel/TimelineFramePreview.tsx:4`, and
  `PreviewPanel/useVideoEditorPreviewComposition.ts:3`: missing
  `CompiledCanonicalTransitions`.
- `VideoEditorAssetPanelSurface.tsx:47`, `TimelineEditorShellCore.tsx:579`,
  `TimelineRenderer.tsx:1625`, `useDerivedTimeline.ts:71`, and
  `useRenderState.ts:596`: the same `ResolvedTimelineConfig`/`TimelineConfig`
  mismatch.
- `AudioTrack.tsx:15-18`: missing `computeMediaTrim`,
  `encodedEnvelopeSource`, and `EncodedEnvelopeSource`.
- `TimelineRenderer.tsx:1`: missing `CompiledCanonicalTransitions`.
- `TimelineRenderer.tsx:1309` and `:1607`: implicit-any parameters caused by
  the stale Composition declarations.
- `VisualClip.tsx:3`: missing `getSanitizedPlaybackRate`; `:641`: missing
  `DrawPlan.incomingPolicy`.
- `compiledAudioSourceClock.ts:1`: missing
  `getSanitizedPlaybackRate` and `computeMediaTrim`.
- `playerEvaluation.ts:1-8`: missing `compileCanonicalTransitions`,
  `clipOpacity`, `getSanitizedPlaybackRate`, and
  `CompiledCanonicalTransitions`; `:80`: implicit-any parameter; `:85`:
  call has 13 arguments where the stale declaration permits 6–12.
- `useClientRender.ts:3`: missing `CompiledCanonicalTransitions`.
- `config-utils.ts:43`: missing `computeMediaTrim`.

One unrelated App-owned diagnostic is also present:

- `src/tools/video-editor/commands/clipScalarGesture.ts:26`: clear union
  includes `elementRef`, but the currently resolved Composition/App type
  permits only `hold | transition | asset`. App status assigns the approved
  two-file scalar correction to App2 and the containing Composition14 pin; it
  was not folded into this transcript patch.

No browser, full suite, localhost/live-socket suite, or new launcher was run.

## Worktree scope

Changed paths are exactly the two App2-owned source/test files above. No build
output or temporary file was left in the worktree.

