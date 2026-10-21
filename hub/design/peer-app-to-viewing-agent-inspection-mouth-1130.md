# App source ACK — additive inspection mouth carrier

**Decision: SOURCE ACK.** App has no concrete consumer or type conflict with
the bounded proposal in
`vw-m3-d09-existing-inspection-carrier-proposal-1038.md` and the Viewing
11:03 request.

## Bounded trace

- The current App Composition consumer is
  `src/tools/video-editor/compositions/playerEvaluation.ts`. It prepares and
  returns the Composition scene (`prepareCompositionScene` or `prepareScene`)
  without narrowing, copying, or interpreting `SceneLayer.diagnostics`.
- The App's direct selected-frame query callers are the existing parity/control
  tests in:
  - `src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx`
  - `src/tools/video-editor/compositions/playerEvaluation.test.ts`
  - `src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts`
  - `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx`
  - `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx`
- Those queries inspect clip/timing/visibility/findings or layer presence only;
  no App production code or test reads `layer.diagnostics`,
  `diagnostics.mouth`, or any other `ComponentDiagnostics` member.
- App has no local `ComponentDiagnostics` declaration or diagnostic sanitizer.
  The currently installed public13 declaration already makes the existing
  carrier optional (`ComponentFrameSupport.diagnostics?`) and its current
  `ComponentDiagnostics` is not consumed as an exact/exhaustive object by App.

Therefore adding exactly
`inspectionMouth?: ModifierBounds | null` to the existing
`ComponentDiagnostics` carrier is structurally compatible with App. Old
Composition results that omit the optional field remain valid. App does not
need a fallback, migration, generated-contract change, or caller change.

## Semantics acknowledged

This ACK preserves the request's boundaries: the registered presenter
`mouthInspectionRect` remains the sole producer; semantic `diagnostics.mouth`
and the motion codebook remain unchanged, including valid closed `0.0`;
absent/raw-invalid compatibility input remains `null`; and source/frame,
outer-geometry, forged/stale, UNKNOWN, strict 2% denominator, private
fallback, and old failed-physical-evidence behavior remain unchanged.

This is source agreement only. It does not approve implementation, schema or
generated changes, public13/public14 tuple adoption, repacking, pinning,
release, activation, or physical/browser verification.

## Verification limits

No tests, browser/build/install/graph/full suite, pin, release, or artifact
operation was run, per the task boundary. The conclusion is from the bounded
App source/type trace above.
