# App2 M2 element current-root flat packet

Base: `ea38656fe` (`tl/integration`, current App root).

## Artifacts

- Shared-port proposal: [app2-m2-element-current-shared-port.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app2-m2-element-current-shared-port.patch), SHA-256 `056b489d0cb2950d229a1b1b322e0741a02f15b12dd702929a6e7fb08818f567`.
  Exactly four shared files: `commands/commitSession.ts`, `hooks/useTimelineCommandSession.ts`, `hooks/useTimelineState.ts`, and `hooks/useTimelineState.types.ts`.
- Row-local proposal: [app2-m2-element-current-row-local.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app2-m2-element-current-row-local.patch), SHA-256 `1e314f0290335dd280c3d216b780adde7be350f29adcf8bf930fdf48c2d7c4f3`.
  Three files: `commands/elementGesture.ts`, `components/PropertiesPanel/AstridElementParams.tsx`, and its test.
- Merged native helper preserved from commit `01f891ab66a5f27b4b7a9823e6f4ddee83807eaf`; current `elementCapture.ts` Git blob is `6d46c13b6b4c48ad6c9ec07fa23b58d7f90d2256`, SHA-256 `a7f5468ed4795a934398ac67ab1a25bd7525ee5749666162754b4ad70e93c2b7`.
- Approved literal-routing repair reference: SHA-256 `73423bfe494c512b1c48643228c830688533f07bae9cc4e6c9101576b9c47efc`.

Apply the row-local patch first, then the four-file shared proposal. The App owner must add the bounded Provider callback/automatic-host join separately; this packet does not edit automatic owner/subscribe construction or `VideoEditorProvider.tsx`.

## Exact port signature

```ts
export interface ElementCapturePort {
  capture(input: {
    clipId: string;
    current: TimelineData;
    edit: ElementEdit;
  }): ElementCaptureBasis;
  finish(
    basis: ElementCaptureBasis,
    edit: ElementEdit,
  ): PreparedElementEdit;
  submit(input: PreparedElementEdit): void;
}
```

The row helper calls `captureClipElementEdit(port, current, clipId, edit)`, then `submitClipElementEdit(captured, edit)`. The session captures the original displayed scope/head and authored bundle, finishes from that immutable basis, validates generation/bundle/command/preview identity, and enqueues exactly one existing outbox intent.

## Boundaries

- Native routing is limited to qualified literal, unowned existing-clip element/PARAM edits.
- Selected-pack PARAM/element edits remain on the existing producer; the native helper's authenticated Agent-schema refusal remains intact.
- Existing overlay creation, transition, remove, full-panel, multi-target, and other valid producers remain reachable. No legacy writer or adapter is deleted.
- There is no post-capture fallback, direct POST, new store/API/DTO, pin/dependency/generated change, or Provider construction edit.
- MAIN574 and TrackInspector changes are unchanged.

## Evidence

Combined private candidate (both proposals applied to `ea38656fe`) passed:

```text
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx
```

Result: **9 files, 235 passed** (the older reviewed root's 229-test count is superseded by six current-root tests).

```text
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/runtime/element-adapter.test.ts src/tools/video-editor/hooks/useClipEditing.test.ts
```

Result: **2 files, 37 passed**.

Static checks passed: `node_modules/.bin/tsc --noEmit --pretty false --incremental false`; targeted ESLint with `--no-cache --max-warnings 0`; `git diff --check`; and `git apply --check --whitespace=error-all` for both packet patches against the current root.

Runtime Door acceptance, reload/undo/exact-retry, browser/socket, full suites, and whole-element-row qualification remain open as required by the task.
