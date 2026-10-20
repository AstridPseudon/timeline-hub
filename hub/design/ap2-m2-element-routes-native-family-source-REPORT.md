# ap2-m2-element-routes-native-family-source

## Result

Implemented the smallest agreed native family: the repaired literal incoming-transition source (`ca9f5f8e` product repair, `a70f...` schema/source handoff). The existing overlay family (`f83`) and retired `None` cohort were left untouched.

- `clipScalarCapture` now captures native transition values with an exact `elementRef`, preserves opaque transition data, records the same-track predecessor/order guard, verifies adjacency and duration bounds, and refuses mismatched/compiled-only data atomically.
- `clipScalarGesture` omits an empty preview `clear` for transition SETs because the existing timeline patch validator rejects non-hold payloads when `clear` is present.
- `ElementsLibraryPanel` routes built-in/rendering transitions through the existing `useTimelineEditorOpsSafe().clipScalar` session seam as one `clip.set`, targeting the selected second clip and preserving type, revision, pack ID, IDs, and draft-on-refusal behavior. The old transition adapter remains in place pending cross-repo acceptance.
- Hosted project-pack transitions are explicitly refused until the normal hosted binding supplies a genuine `DocumentPin`/verified-read source; no alias, fake pin, provider, wire, store, or public activation was added.

No HOME/shared patch was needed. The existing App seam already exposes `clipScalar` from the command session through `useTimelineEditorOpsSafe`; the metadata seam is the existing catalog entry (`id`, `kind`, `revision`, `packId`, publication/admission), and the narrow peer dependency is the repaired Agent `clip.set` transition source/schema becoming accepted by the shared integration.

## Evidence

- `TMPDIR=/tmp/ap2-m2-element-routes-native-family-source-vitest node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/commands/commitSession.clipScalar.test.ts src/tools/video-editor/components/ElementsLibraryPanel.test.tsx src/tools/video-editor/runtime/element-adapter.test.ts` — **5 files, 92 tests passed**.
- `node_modules/.bin/tsc --noEmit --pretty false --incremental false` — **passed**.
- `node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/commands/clipScalarCapture.ts src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/clipScalarGesture.ts src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/components/ElementsLibraryPanel.tsx src/tools/video-editor/components/ElementsLibraryPanel.test.tsx` — **passed**.
- `git diff --check` — **passed**.

## Cut/review conditions

Keep the legacy transition writer until the repaired Agent source/schema is integrated and a shared direct commit/Runtime qualification proves native `clip.set` acceptance, atomic refusal, owner-qualified reads, and no legacy transition traffic. Then review the transition adapter removal separately. Hosted project-pack positive behavior remains blocked on the existing retained metadata/read-adapter seam providing the real pin and verified reads; this worker did not invent a positive path.

No full, browser, socket, or `request-test` suite was run, per task scope. Fresh cross-repo SDK/Runtime qualification and hosted project-pack positive behavior remain unverified.
