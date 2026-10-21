# Independent review: App clip scalar public-patch type fix

## Verdict

**Approve the minimal 1220 hunk.** No product-source changes were made by this review.

The candidate changes only `clipScalarGesture.ts` and its existing test assertion:

- `clipScalarPreview` filters only `elementRef` from the public `TimelinePatch.clear`, with a typed predicate matching the existing public contract (`hold | asset | transition`).
- The durable `ClipScalarArgs.clear` carrier remains `hold | asset | transition | elementRef`; no SDK widening, cast, DTO, new field, normalization, caller, or dependency change was introduced.
- For a paired native clear (`clear: ['transition', 'elementRef']`), the public preview is intentionally `clear: ['transition']`. The native command still carries the exact pair. This is the correct separation because `elementRef` is not a public patch-clear leaf.
- Native capture/execution still requires the paired clear, retains the original guards, records the `elementRef` and `transition` writes, removes both authored leaves, and preserves the inverse. Existing tests cover both `elementRef` and legacy `element_ref` storage spellings and unsafe-reference refusal.

The changed existing assertion is one-to-one with that boundary: its paired-clear case asserts the submitted command retains the exact original `args`, while the submitted public preview contains only the permitted `transition` clear. Existing native capture tests separately assert exact command/record/raw-output/inverse behavior. I found no concrete gap requiring a new native assertion or a test matrix.

## Verification

Working directory for the commands below:

`/home/user/work/wt/ap2-m2-clip-scalar-type-fix-independent-review-1228`

- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/commitSession.clipScalar.test.ts`
  - **PASS** — 3 files, 99 tests.
- `./node_modules/.bin/eslint src/tools/video-editor/commands/clipScalarGesture.ts src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/commitSession.clipScalar.test.ts --report-unused-disable-directives --max-warnings 0`
  - **PASS**.
- `git diff --check HEAD^ HEAD`
  - **PASS**.
- `flock -w 300 /home/user/work/.app-tsc.lock bash -lc './node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false > /tmp/ap2-m2-clip-scalar-type-fix-independent-review-1228-tsc.log 2>&1; echo TSC_STATUS:$?; wc -l /tmp/ap2-m2-clip-scalar-type-fix-independent-review-1228-tsc.log; cat /tmp/ap2-m2-clip-scalar-type-fix-independent-review-1228-tsc.log'`
  - **NONZERO (expected baseline condition)** — exit 2, 28 diagnostics. The current log is byte-for-byte identical to the saved 1220 typecheck log: 28 error lines, with no diagnostic in either changed file. The pre-fix 1220 source diagnostic at `clipScalarGesture.ts:26:37` is absent; only the existing package/Composition diagnostics remain.

## Typecheck dependency record

The exact declaration origin used by this run is:

- `realpath node_modules/@banodoco/timeline-composition` → `/home/user/work/app/node_modules/@banodoco/timeline-composition`
- package JSON → `/home/user/work/app/node_modules/@banodoco/timeline-composition/package.json`
- resolved version → `0.0.8`
- declarations → `dist/index.d.ts` and its `dist/*.d.ts` imports

The worktree `package.json` and `package-lock.json` request `file:vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz` / version `0.0.13`, but the protected shared install actually used by this run is 0.0.8. No install, cache write, shared-node_modules mutation, pin change, or baseline change was performed. This is the existing HOME-owned dependency/pin issue, not a regression in this hunk.

The 28 remaining diagnostics are:

- `TS2345` optional `ResolvedTimelineConfig.theme` versus package `TimelineConfig.theme` at `ShotTimelinePreview.tsx`, `CompactPreview.tsx`, `VideoEditorAssetPanelSurface.tsx`, `TimelineEditorShellCore.tsx`, `TimelineRenderer.tsx`, `useDerivedTimeline.ts`, and `useRenderState.ts`.
- Missing package exports `CompiledCanonicalTransitions` at `RemotionPreview.tsx`, `TimelineFramePreview.tsx`, `useVideoEditorPreviewComposition.ts`, `TimelineRenderer.tsx`, `playerEvaluation.ts`, and `useClientRender.ts`.
- Missing package export `computeMediaTrim` at `AudioTrack.tsx`, `compiledAudioSourceClock.ts`, and `config-utils.ts`.
- Missing package exports `encodedEnvelopeSource` and `EncodedEnvelopeSource` at `AudioTrack.tsx`.
- Missing package export `getSanitizedPlaybackRate` at `VisualClip.tsx`, `compiledAudioSourceClock.ts`, and `playerEvaluation.ts`.
- Missing package export `clipOpacity` and `compileCanonicalTransitions` at `playerEvaluation.ts`.
- `TS2339` missing `incomingPolicy` on package `DrawPlan` at `VisualClip.tsx`.
- `TS7006` implicit `any` parameters at `TimelineRenderer.tsx` (two) and `playerEvaluation.ts` (one).
- `TS2554` argument-count mismatch at `playerEvaluation.ts`.

No green typecheck claim is made.

## Not run / next step

No browser, proof harness, full suite, frozen packet, or live-socket test was run. No blocker remains for this review. HOME should reconcile the declared 0.0.13 package pin with the actual protected install before relying on a green app typecheck.
