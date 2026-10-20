# App native-None port — MAIN574/public13

## Identity

- Target commit: `1c9da5c159c75d778ff74f314c549efb9b218fc7`
- Target HEAD tree: `cbfc15d3f775e0817b038333291172ce960cfafe`
- Candidate worktree tree (including uncommitted changes): `f5de50dcd56fad16ec99d0a57b583b1cc247873a`
- Frozen source: `46c15aee5fd08aa71a49b0378eb694491f8482da`, tree `93042fb19a46d121a9a843a75a9fe85b426fe67a`
- Port boundary: only `3599fc49ad76dfdd7847ab4c813fc9317a0304eb..46c15aee5fd08aa71a49b0378eb694491f8482da`:
  - `d36fe2e9d` — command-backed scalar/native-None capture, preview, outbox, recovery and two-case gate.
  - `fa1a87f80` — bulk native sentinel renders as `None`.
  - `46c15aee5` — own-data writes and JSON-byte-preserving Playwright outbox inspection.
- Runtime/Composition qualification tuple named by the task: Agent8130, Runtime2c4, public13 Composition archive 0.0.13; source launcher constants remain the required Runtime `2c4ac180...`, Composition 0.0.12 for the existing current013 harness. No older main/public12 product files were copied over MAIN574.

## Ported behavior

- Restored exact source files for scalar capture/gesture, command-session integration, preview, focused tests, scalar fixture, launcher/contract support, and the two native-None browser journeys.
- Added the `clip.update.clear` preview type and preserved recorded ABSENT-vs-present guards.
- Kept single and atomic bulk transition clears on the command session; the fallback callback remains only for standalone controls with no capture port.
- Preserved MAIN574 Inspector/touch tabs, TrackInspector, registry/display-name behavior, PCM13 progress, restored tests, and the original three drag markers.
- Merged the source prop joins into current MAIN574 files only:
  - `ClipPanelBody.tsx`: scalar capture prop flows through the current Inspector body to effects.
  - `PropertiesPanel.tsx`: current single/bulk Inspector entry points supply scalar capture ports.
  - `VideoEditorProvider.tsx`: current editor-ops projection carries `clipScalar`.
- No new generic writer or portal path was introduced.

## Caller census / retirement boundary

Production native-None callers are the single `ClipTransitionSection` and bulk `BulkClipPanelBody` controls, reached through `PropertiesPanel` and `PropertiesPanelBody`. They call `submitClipScalarEdit` / `submitClipTransitionClears) when the command-session capture ports are present. The only retained `onChange({ transition: undefined })` / `onChangeDeep` paths are explicit standalone compatibility fallbacks when those ports are absent. Other scalar/effect/parameter writers remain outside this bounded D01 unit.

## Evidence

Targeted Vitest core:

```
node --require .../runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/clipScalarCapture.test.ts \
  src/tools/video-editor/commands/clipScalarGesture.test.ts \
  src/tools/video-editor/commands/commitSession.clipScalar.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/lib/clip-scalar-preview.test.ts \
  src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx
```

Result: 8 files, 216 passed, 0 failed.

Nearest neighbors:

```
node --require .../runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/lib/timeline-patch.test.ts \
  src/tools/video-editor/commands/trackLabelGesture.test.ts \
  src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts \
  src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx \
  src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx \
  src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx \
  src/shared/lib/media/mediaCrossOrigin.test.ts
```

Result: 13 files, 536 passed, 0 failed.

Additional checks:

- `node --test --test-concurrency=1 scripts/testing/current013-integration.test.mjs`: 1 passed.
- `node --experimental-vm-modules --test --test-concurrency=1 tests/e2e/local/support/current013-native-none.test.mjs`: 1 passed.
- `node --test --test-concurrency=1 tests/e2e/local/support/native-transition-clear.contract.test.mjs`: 1 passed.
- Scoped ESLint over all changed TS/TSX and native-None support files with `--max-warnings 0`: passed.
- `git diff --check`: passed.
- Exact frozen-source additions were hash-checked against source `46c15aee5): passed.

## Not run / next step

No browser/live-socket run was launched locally, per the orchestration rule. The configured central suite list has native-None suites hardcoded to the older public12/source trees; it has no exact MAIN574/public13 two-case entry. Running one of those would not be valid evidence. The orchestrator should register/run the new wrapper against candidate tree `f5de50dcd56fad16ec99d0a57b583b1cc247873a`, Agent8130, Runtime2c4, public13 archive 0.0.13, private cache, and Chromium141. That is the remaining evidence for actual reload, inverse, lost-ACK/restart exact retry, real 409 draft retention, and zero legacy traffic. No full suite, build, TSC, install, or shared dependency write was run.

