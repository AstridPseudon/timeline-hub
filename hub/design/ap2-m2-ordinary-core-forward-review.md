# ap2-m2 ordinary core forward review

Verdict: **APPROVE source** at `4a48638b2483e50d0659cc4c3395746151c3134b` (tree `91ba1d5b4facb4877b6f8c121df8c30920eb3784`), based directly on `48576cfa2783331f2c7c8309ff4069162a3afd11`.

The delta is limited to the approved ordinary generic classifier/port/forwarding/dispatcher and its focused tests: 8 files, `224` additions and `5` deletions. Existing element, parent-media, overlay, move/label/None/delete/shot/automatic sections remain present; no source deletion or legacy-writer retirement was introduced. The generic session uses the existing preparation and outbox path, preserves the dependent `lastIntent` basis, and submits one command list. No new DTO, store, arbitrary-command submit, direct POST/API, or post-capture fallback is present.

Behavior verified from the actual source:

- `classifyGenericPatch` runs before owner resolution/capture. Fully supported batches use the generic port; mixed batches enter the port and `captureGenericPatch` refuses the whole batch before resolving any owner or executing a member; all-unsupported batches remain on `validateTimelinePatch`/`compileTimelinePatch`/guarded `commitData` before native capture.
- Original generation, display-basis, bundle identity, prepared-entry, and exact-preview checks remain in the session. Existing tests were retained; the branch adds rather than removes the relevant behavior tests.
- The new session test proves one outbox intent across lost acknowledgement/restart and exact retry of command body, serialized body text, and idempotency key.
- Native capture retains ordered commands, ordinals, guards, opaque fields, immutable projection behavior, and mixed atomic refusal.

Integration overlap: current `tl/integration` is `0d5009e18bee8e29f894dabf5db501a0fcea750f` (with `22788084f` in its ancestry), and already contains the same generic port through `052b94b64`. Comparing the current files shows no semantic forward port is needed for session/command-session/ops/state wiring. Apply only the narrow helper typing delta from this branch in `genericPatchCapture.ts` (`const hold = number(command.args.values.hold, 'hold', true);`); do not replay the whole `4a48638b2` patch. The remaining differences are import/order noise and an unused test import.

Tests run:

```text
./node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/lib/compiler-canary.test.ts \
  src/tools/video-editor/lib/source-map-runtime.test.ts
=> 9 files, 278 tests passed

./node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/elementCapture.test.ts \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  src/tools/video-editor/commands/parentClipAddCapture.test.ts \
  src/tools/video-editor/commands/media.test.ts \
  src/tools/video-editor/components/PropertiesPanel/TrackInspector.test.tsx
=> 5 files, 24 tests passed

./node_modules/.bin/eslint \
  src/tools/video-editor/commands/commitSession.ts \
  src/tools/video-editor/commands/genericPatchCapture.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.ts \
  src/tools/video-editor/hooks/useTimelineOps.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineState.ts --max-warnings 0
=> exit 0

git diff --check 48576cfa2..HEAD
=> exit 0
```

Typecheck evidence is intentionally not false-green:

- Real worktree `NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false` exits 2 with 25 diagnostics. Sixteen are the known Composition/package skew from the shared 0.0.8 install. The remaining 9 are known App helper/consumer fixes: `elementCapture.ts` (1), `occurrenceDuplicateCapture.ts` (3), `elementGesture.ts` (3), and `AstridElementParams.tsx` (2). There is no diagnostic in the changed ordinary-core files.
- A private current-HEAD source archive run against the locked graph (`app-ap2-m2-locked-graph`, Composition 0.0.13) exits 2 with exactly those 9 known helper/consumer diagnostics and the ordinary probe exits 0, producing `clip.set,track.set` with hold `1.23456789`, label `ordinary-🎬`, and the existing move command. This confirms the package-skew classification.

Remaining prerequisites before integration/gate claims: apply the one-line typed-helper forward port; preserve the integration `052b94b64` generic implementation and later `0d5009e18` changes; resolve the known helper/consumer type fixes for a green locked-graph project tsc; then run the central `full-e2e-three-products` against the exact committed tree with the matching Agent/Runtime candidate, real Runtime door, Chromium, and configured `ASTRID_CHECKOUT`/`ASTRID_PYTHON`. Gate 6 still needs the real representative-gesture zero-legacy/direct-legacy-rejection proof. No full, browser, localhost, live-socket, Runtime-door, dependency, pin, generated-file, or Git operation was run here.

No source changes were made by this review; the review worktree is clean.
