# AP2 M2 literal PARAM fallback deletion — independent review

## Decision: APPROVE

Reviewed `tl/ap2-m2-element-literal-cut-data-safety-review-1233` at
`a058f94d7` against `c85da5427` (`tl/integration`), plus the source worker's
report and direct tests. The source change is bounded to
`AstridElementParams.tsx` and its direct test. I added one assertion to the
existing literal-positive test so it verifies the submitted native command and
preview payload; no new test was added and no original assertion was removed or
converted to an expected failure.

## Safety proof

- Literal PARAM edits now always take the existing native path at
  `AstridElementParams.tsx:81-96`: `captureClipElementEdit` followed by
  `submitClipElementEdit`. The former `onChange(next)` fallback is gone; the
  prop is intentionally unused (`onChange: _onChange`).
- The literal success test retains the native success case and now asserts the
  exact `{ command, preview }` submitted to the native port. The command is
  `clip.set-params`, and the preview source is
  `timeline.native-existing-element` with the expected `clip.update` payload.
  It also asserts `onChange` was not called, covering zero legacy traffic for
  the removed branch.
- Missing literal data/carrier visibly refuses while keeping the selected
  value in the controlled draft (`Literal PARAM native capture is unavailable;
  draft preserved.`). Capture, finish, or submit refusal is caught, shown in
  the inline alert, and does not call the legacy callback.
- The selected project-pack PARAM branch remains the retained-read/native
  carrier path and is unchanged in meaning. Owned/project, SYSTEM8e-adjacent,
  animation, transition, and library operations are not deleted by this diff.
- Presence semantics remain distinct: a native PARAM value of `null` is a
  present write; an explicit `clear` records an absent/delete state. The
  existing primitive test covers `present(null)` versus `absent`, and the
  element-capture tests retain explicit-clear and opaque-field assertions.

## Remaining physical writer

The remaining live element writer is the native adapter/CAS boundary:

- `src/tools/video-editor/components/ElementsLibraryPanel.tsx:68-156` routes
  admitted overlay elements through the native overlay session and other
  element/animation/transition operations through
  `elementOperationAdapter.execute`.
- `src/tools/video-editor/runtime/element-adapter.ts:455-524` is the live
  operation boundary and performs the expected-head save. It remains intact.
- `AstridElementParams.tsx:90-91` is now only the native existing-clip PARAM
  capture/submit path; there is no second direct-save/CAS fallback in that
  component.

## Verification

Passed:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/elementOverlayCapture.test.ts src/tools/video-editor/runtime/element-adapter.test.ts src/tools/video-editor/components/ElementsLibraryPanel.test.tsx src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
8 files passed, 164 tests passed

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipMovePrimitives.test.ts
1 file passed, 25 tests passed

./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx
passed

git diff --check
passed
```

The required actual-project typecheck was run under the shared lock:

```text
flock /home/user/work/.app-tsc.lock node_modules/.bin/tsc -p tsconfig.app.json --noEmit
```

It failed with 29 existing errors outside the changed files. The owning
dependency/source for every diagnostic is:

1. `ShotTimelinePreview.tsx:238` — Composition `TimelineConfig.theme`
   declaration mismatch.
2. `clipScalarGesture.ts:26` — local App `TimelinePatchOperation.clear` type
   does not admit `elementRef`.
3. `CompactPreview.tsx:46` — Composition `TimelineConfig.theme` mismatch.
4. `PreviewPanel/RemotionPreview.tsx:1` — Composition lacks
   `CompiledCanonicalTransitions`.
5. `PreviewPanel/TimelineFramePreview.tsx:4` — Composition lacks
   `CompiledCanonicalTransitions`.
6. `PreviewPanel/useVideoEditorPreviewComposition.ts:3` — Composition lacks
   `CompiledCanonicalTransitions`.
7. `VideoEditorAssetPanelSurface.tsx:47` — Composition `TimelineConfig.theme`
   mismatch.
8. `TimelineEditorShellCore.tsx:579` — Composition `TimelineConfig.theme`
   mismatch.
9. `compositions/AudioTrack.tsx:15` — Composition lacks `computeMediaTrim`.
10. `compositions/AudioTrack.tsx:16` — Composition lacks
    `encodedEnvelopeSource`.
11. `compositions/AudioTrack.tsx:18` — Composition lacks
    `EncodedEnvelopeSource`.
12. `compositions/TimelineRenderer.tsx:1` — Composition lacks
    `CompiledCanonicalTransitions`.
13. `compositions/TimelineRenderer.tsx:1309` — implicit `any` for `input`,
    exposed by the stale Composition declaration.
14. `compositions/TimelineRenderer.tsx:1607` — implicit `any` for `track`,
    exposed by the stale Composition declaration.
15. `compositions/TimelineRenderer.tsx:1625` — Composition
    `TimelineConfig.theme` mismatch.
16. `compositions/VisualClip.tsx:3` — Composition lacks
    `getSanitizedPlaybackRate`.
17. `compositions/VisualClip.tsx:641` — Composition `DrawPlan` lacks
    `incomingPolicy`.
18. `compositions/compiledAudioSourceClock.ts:1` — Composition lacks
    `getSanitizedPlaybackRate`.
19. `compositions/compiledAudioSourceClock.ts:1` — Composition lacks
    `computeMediaTrim`.
20. `compositions/playerEvaluation.ts:1` — Composition lacks
    `compileCanonicalTransitions`.
21. `compositions/playerEvaluation.ts:3` — Composition lacks `clipOpacity`.
22. `compositions/playerEvaluation.ts:5` — Composition lacks
    `getSanitizedPlaybackRate`.
23. `compositions/playerEvaluation.ts:8` — Composition lacks
    `CompiledCanonicalTransitions`.
24. `compositions/playerEvaluation.ts:80` — implicit `any` for `input`,
    exposed by the stale Composition declaration.
25. `compositions/playerEvaluation.ts:85` — Composition API accepts 6–12
    arguments, but this call supplies 13.
26. `hooks/useClientRender.ts:3` — Composition lacks
    `CompiledCanonicalTransitions`.
27. `hooks/useDerivedTimeline.ts:71` — Composition
    `TimelineConfig.theme` mismatch.
28. `hooks/useRenderState.ts:596` — Composition `TimelineConfig.theme`
    mismatch.
29. `lib/config-utils.ts:43` — Composition lacks `computeMediaTrim`.

The theme/type/export/API diagnostics are owned by the stale Composition graph;
the `clipScalarGesture.ts:26` diagnostic is an unrelated local App contract.

The checked-in app graph points to
`vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz` in both
`package.json` and `package-lock.json`; the artifact declares `0.0.13`. The
protected shared install actually used by this check resolves to
`/home/user/work/app/node_modules/@banodoco/timeline-composition` and declares
`0.0.8`. That shared `0.0.8` declaration origin is invalid for this review
(and any shared `0.0.10` origin would likewise be invalid). No install,
shared-dependency mutation, pin change, browser run, or full suite was done.

## Blockers / next steps

The literal deletion itself is approved. The app typecheck remains blocked by
the protected shared Composition installation and the unrelated local scalar
patch type error; refresh/qualify the pinned Composition graph before claiming
a green actual-project typecheck. Browser/full-suite proof was intentionally
not run under the owner’s lighter interim rule.
