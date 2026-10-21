# Fresh-caption joint-row handoff

Status: observed positive, no activation. The compact JSON companion contains the exact before fixture, builder patch, compiler result, wire-row projection, opaque siblings, and order.

## Observed Main path

Main `860d43b331fb4422b16bc0dbd7b08666a0` (tree `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`) uses the real transcript builder at `src/tools/video-editor/dev/transcript-lane/extension.ts:288-476`. The existing success fixture is `src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx:1017-1043`, with source item `source-1@clip-1`, interval `1..2`, and text `Zażółć 🌍`.

With the existing caption track present, the normal builder returns exactly:

1. `clip.add` target `transcript-caption-ca055bff87805488`, `{track, at: 1, clipType: "text"}`, order 0.
2. `clip.update` for the same target, `{track, at: 1, hold: 1, x: 128, y: 418, width: 1024, height: 101, text, label, app.__generated__, mode: "merge"}`, order 1.

The existing caller context is `haus.astrid.transcript-lane` / `transcript-caption-foundry`, schema `astrid.transcript_segment/v1`, version `1.3.0`, and `preserve-output`. `managedBy` is absent from both operations and remains absent; this handoff does not assign ownership.

The real compiler entrypoint is `src/tools/video-editor/lib/timeline-patch.ts:1012-1029`. Its add path creates the structural row at `:1120-1173`; update merge and meta synchronization are at `:1229-1316`; row/config materialization is at `:1936-1978`. The observed raw birth row is:

```json
{"id":"transcript-caption-ca055bff87805488","at":1,"track":"transcript-caption-foundry-track","clipType":"text","hold":1,"x":128,"y":418,"width":1024,"height":101,"text":{"content":"Zażółć 🌍","fontSize":48,"color":"#ffffff","bold":true,"align":"center"},"app":{"__generated__":{"extensionId":"haus.astrid.transcript-lane","contributionId":"transcript-caption-foundry","provenance":{"contractVersion":1,"sourceSchemaRef":"astrid.transcript_segment/v1","sourceItemId":"source-1","sourceFingerprint":"astrid-fnv1a64-v1:45455185c9f937d7","sourceRevision":17,"generatorVersion":"1.3.0","outputFingerprint":"astrid-fnv1a64-v1:a3ab11fde87e6f3d","conflictPolicy":"preserve-output"}}},"label":"Zażółć 🌍"}
```

`src/integrations/runtime/dataProvider.ts:1072-1098,1131-1144` shows the existing publication shape: the compiled authored clips become both `parent_composition.config.clips` and top-level `parent_composition.clips`. This is raw-shape evidence, not a live HTTP/persistence run. The companion JSON records the exact before parent/config, source item, preserved source clip text/params/app siblings, track/project app siblings, and per-track order.

## Native boundary

Current integration dispatches any non-unsupported patch to the native port at `src/tools/video-editor/hooks/useTimelineOps.ts:267-275`. `src/tools/video-editor/commands/genericPatchCapture.ts:109-162` classifies this batch as `mixed`: structural `clip.add` is supported, but the rich `clip.update` is not. `captureGenericPatch` refuses atomically at `:517-545`, before owner resolution and before an authored write. The current native gap is therefore a visible mixed-batch refusal; the compiler never receives this producer batch through that route.

This is not authorization to route the batch through a snapshot writer. Preserve the old legacy behavior/draft while unqualified and do not activate anything. Agent owns the smallest native recipe using existing command carriers; Runtime owns custody. No new op, silent owner assignment, DTO, store, or public API is proposed. Any future lowering must preserve the existing extension/contribution context, absent `managedBy`, generated metadata, opaque siblings, and order.

## Verification

Runnable targeted command (no browser, HTTP, full suite, install, pin, or product edit):

```sh
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/lib/timeline-patch.test.ts \
  src/tools/video-editor/lib/timeline-reader.test.ts \
  src/tools/video-editor/lib/timeline-reader.planner-contract.test.ts
```

No live callers changed. See the JSON companion for the exact generated export and source identities.
