# ap2-m2-element-session-patch-review

## Verdict

- **Source/helper and literal existing-clip session plumbing: APPROVE**, bounded to the qualified literal clip.set-element / clip.set-params path.
- **Patch as a consumer integration: HOLD.**
- **Consumer gate: HOLD.**
- **Whole-element-row gate: HOLD.**

The patch was reviewed from base 01f891ab66a5f27b4b7a9823e6f4ddee83807eaf in a private copy only. The app worktree remained unchanged.

## Exact finding

### Blocking: selected-pack PARAM edits are blanket-denied once the session is available

In the patched src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx:53-58, every edit uses the native port whenever elementPort && timelineData; the branch does not test whether the clip has a project-pack owner.

The approved helper intentionally refuses selected-pack capture:

- src/tools/video-editor/commands/elementCapture.ts:261-265
- src/tools/video-editor/commands/elementCapture.ts:280-287

Therefore a mounted selected-pack parameter edit calls captureClipElementEdit, throws 'selected project pack capture requires authoritative Agent schema capture', and never reaches the existing onChange producer. The existing producer is reachable through ClipPanel.tsx:31 -> PropertiesPanel.tsx:527 -> useClipEditing.ts:235-282 -> the existing applyEdit/snapshot path. This is a real positive producer, not a mock-only path.

This violates the settled migration boundary: valid selected-pack producers remain until their qualified migration; unsupported native coverage must not replace them with blanket denial. It also means the refusal is a synchronous UI throw rather than the existing producer or a visible retained-draft/session refusal path.

Recommended correction for the eventual patch: select the native route only for a clip whose actual element reference is literal/unowned (no packId), and leave selected-pack edits on the existing producer until the authoritative Agent/provider seam is wired. Do not add a fallback after a native capture has begun; unsupported native capture should refuse with its original draft/basis preserved.

## What is sound in the bounded source path

- elementCapture.ts retains the raw authored bundle basis and native guarded claims.
- Literal element/PARAM paths read both elementRef and element_ref.
- PARAM capture retains explicit clears, unchanged/opaque values, and asset registry guards.
- elementGesture.ts checks the captured edit again at finish, checks command shape/selector/version at submit, and preserves the exact prepared command/preview through the existing outbox enqueue.
- commitSession.ts records the captured before, after, local generation, and predecessor/head basis; it does not snapshot after native capture.
- The session hook applies the existing legacy-clean barrier to capture, finish, and submit.

## Evidence

Private patched-copy commands and results:

- node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx — 9 files, 228 passed.
- node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/runtime/element-adapter.test.ts src/tools/video-editor/hooks/useClipEditing.test.ts — 2 files, 37 passed.
- node_modules/.bin/tsc --noEmit --pretty false --incremental false — passed.
- node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/commands/elementGesture.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useTimelineState.types.ts src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/contexts/VideoEditorProvider.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx — passed.
- git apply --check .../handoff-ap2-m2-element-concrete-session.patch — passed against the clean base worktree.
- git diff --check — passed; source worktree remains clean.
- Direct private-copy helper probe with a selected-pack clip — refused as designed with 'selected project pack capture requires authoritative Agent schema capture'.

No full, browser, localhost/live-socket, or Runtime acceptance run was made. No source changes, new tests, generated files, pins, dependencies, shared worktree, or Git refs were modified.

## Gate status and next steps

The qualified literal source path is ready for the orchestrator's consideration. Keep the consumer and whole-row gates HOLD until:

1. the consumer routes only qualified literal edits through this bounded native path while preserving selected-pack positives;
2. a mounted production-path zero-legacy spy proves a real literal edit submits through session/outbox and does not call the legacy writer;
3. Runtime acceptance/reload/undo/exact-retry evidence is collected;
4. overlay, transition, remove, and full-panel producers each receive their own qualified native migration before any legacy retirement.

