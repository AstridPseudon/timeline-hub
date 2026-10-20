# AP2 M2 seam report review

## Verdict

**REQUEST CHANGES — source.** The report-only acknowledgement no-save behavior is correct, but the authored-change path silently deletes a legacy stored `visualSeamContract.report`. The full seam row remains **OPEN** because authored render-admission persistence is still the ordinary snapshot writer pending the qualified Agent/Runtime command seam.

## Review scope and source findings

- Reviewed `dcc8d41dd` over `tl/ap2-m2-ordinary-seam-report-retirement` in `/home/user/work/wt/ap2-m2-seam-report-review`; no product source, test, dependency, pin, Git, or shared-worktree files were changed.
- The live writer is `src/tools/video-editor/hooks/useTimelineState.ts:690-711`. The render-state callback is supplied to `useRenderState` at `:712-719`; the UI acknowledgement buttons are wired through `TimelineRenderControls.tsx:354-360`.
- The derived report is recomputed by canonical projection at `src/tools/video-editor/data/shotCompositionProjection.ts:590-601`, then carried through `useRenderState.ts:537-538, 926-940, 1371-1378` and displayed by `TimelineRenderControls.tsx`. No production reader treats a persisted report as authoritative.
- `prepareVisualSeamSnapshotConfig` correctly strips reports for equality at `useTimelineState.ts:90-117`, so a report-only/repeated acknowledgement returns `null` before `buildTimelineData`, `commitData({save: true})`, and `flushPendingSave`.

### Blocking finding

At `useTimelineState.ts:111`, `persistedContract` is the acknowledged contract with `report` deleted. If the current stored contract already contains a legacy report and an authored field changes, the callback saves that report-free object at `:697-710`. This violates the review brief's requirement not to silently erase old stored report/unknown fields. The focused authored test starts from `baseConfig`, which has no report (`useTimelineState.visual-seam.test.ts:67-83`), so it does not expose this case.

The required repair is narrow: when an authored change is actually saved, retain an existing `currentConfig.app.visualSeamContract.report` value unchanged while never copying the newly recomputed acknowledged report; if no legacy report exists, do not add one. The existing report-only equality short circuit should remain. Opaque app data and unknown contract members must continue to be retained, and authored intent/track/gap changes must continue to save rather than become no-ops.

## Behavior verified

- Report-only acknowledgement: no canonical save; current and acknowledged objects are not mutated.
- Authored intent change: ordinary snapshot preparation returns a changed config and retains unrelated app data and opaque contract members, but currently drops a pre-existing report as described above.
- Repeated/report-only acknowledgement: normalized authored content compares equal and returns before the writer/flush path.
- Projection/UI-local path: the report remains recomputed and available to preview/export and render-controls state; this review made no Viewer change.

## Tests and checks

Passed:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/data/visualSeamContract.test.ts src/tools/video-editor/hooks/useTimelineState.visual-seam.test.ts src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx
=> Test Files 3 passed; Tests 25 passed

node_modules/.bin/eslint src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useTimelineState.visual-seam.test.ts --report-unused-disable-directives --max-warnings 0
=> passed

git diff --check
=> passed
```

Not clean, with no error reported in the touched files:

```text
node_modules/.bin/tsc -p tsconfig.app.json --noEmit
=> failed on existing command typing errors and missing Composition exports/types, including elementCapture.ts, elementGesture.ts, genericPatchCapture.ts, occurrenceDuplicateCapture.ts, PreviewPanel/RemotionPreview.tsx, AudioTrack.tsx, TimelineRenderer.tsx, VisualClip.tsx, playerEvaluation.ts, and config-utils.ts
```

No full, browser, localhost, live-socket, dependency, shared-install, or generated-output suite was run. Worktree source status is clean.

## Next steps

Repair the authored-change normalization to preserve an already stored legacy report without persisting the newly derived acknowledgement report, then add/run the missing authored-change-over-existing-report regression alongside the current 25-test lane. The native scoped authored app-config command prerequisite remains outstanding; do not migrate or delete the remaining authored snapshot writer in this row until that seam is qualified.
