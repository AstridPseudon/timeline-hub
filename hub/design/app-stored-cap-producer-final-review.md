# REJECT — App stored-cap producer/serialization final review

Reviewed the final harness candidate, not the starting review tree:

- Candidate commit: 4720a864c81dc7002a9e95dbacf10cec8df5da81
- Candidate tree: aa9eb31281e915fe32e7af6e4c7a30a2ff85e8ad
- Parent/base: b1ef4b9b910ba72375c34cf319692f90d22edc25
- Candidate subject: fix(timeline): preserve stored occurrence caps at preview boundaries
- git diff --check 4720a864c^ 4720a864c: exit 0

## Verdict

The producer/raw-basis behavior is otherwise acceptable, but I reject this
exact tree for merge because it is not compatible with the root ES2020
TypeScript library target. The candidate still uses Object.hasOwn at
src/tools/video-editor/lib/serialize.ts:43 and also at
src/tools/travel-between-images/components/shotTimelineDataProvider.ts:146.
The root tsconfig.json declares target: ES2020 and lib: ["ES2020", "DOM",
"DOM.Iterable"]; this API is newer and was previously the TS2550 failure.
Replace both calls with the existing
Object.prototype.hasOwnProperty.call(... ) helper/form before typecheck or
merge. Do not loosen the lib target. No product files were changed in this
review.

This is a narrow source-compatibility rejection, not a behavioral rejection.
After that trivial source correction, rerun the focused controls below.

## Producer/raw-basis findings

- projectCanonicalComposition emits exactly one
  app.canonicalTiming.storedOccurrenceDurationMs per projected child, using
  the verified original occurrence duration while preserving the existing
  effective duration and editor/read geometry.
- The graph/bootstrap, local preview, recovery and accepted-command paths all
  retain or rebuild that scalar from their verified graph. The focused command
  projection tests cover initial, local/recovery (4000), and accepted (4500)
  cases; the popup/provider path exercises actual draft/publication seams.
- Serialization accepts an explicit retained raw basis only on internal
  arguments. Identity-map/raw-ID matching is used; display-prefix or
  canonicalTiming-shape inference is not. Missing/null or ambiguous basis
  refuses visibly, and the draft remains in the editor.
- Authored/storage exits remove only the newly derived scalar while restoring
  raw same-named canonical/canonicalTiming values, including null, unknown
  keys, own __proto__, nested values and ordering. Raw parent clips in mixed
  projections remain intact.
- The draft writer snapshots an authored form once and uses it for the draft
  and save attempt. Existing pending/retry request bytes are reused; no scrub
  or rewrite of pending request payloads was found.
- No new persisted carrier, store, DTO, wire member, SDK export or
  renderConfig was introduced. The scalar occurs only in existing derived
  canonicalTiming metadata and its explicit strip/rebuild paths.
- Import inspection found no new circular runtime import: serializer imports
  the projector; the projector does not import the serializer; the popup
  provider imports both.

## Independent controls

All final runs used the immutable candidate archive with read-only
/tmp/app-coherent-deps12/node_modules, an owned .review-cache, the repo-local
__dirname preload, --configLoader=runner --no-cache, and --maxWorkers=1. No
project typecheck, full suite, build, browser, live socket, install or
pixel/audio capture was run.

1. Producer/serializer/popup controls:

   env -u ASTRID_CHECKOUT node --require /tmp/app-stored-cap-final-review.wpRxPn/dirname-preload.cjs /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run --config /tmp/app-stored-cap-final-review.wpRxPn/review-vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts src/tools/video-editor/hooks/useTimelinePersistence.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/travel-between-images/components/ShotTimelinePreview.test.ts

   Result: 179 passed, 0 failed, 5 files, exit 0.

2. Captured-4000 and 4000/4500 separation controls:

   env -u ASTRID_CHECKOUT node --require /tmp/app-stored-cap-final-review.wpRxPn/dirname-preload.cjs /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run --config /tmp/app-stored-cap-final-review.wpRxPn/review-vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts src/tools/video-editor/data/shotCompositionProjection.test.ts

   Result: 60 passed, 0 failed, 5 files, exit 0. The source-only
   captured-4000 control is green and the 4000/4500 flattened-config
   separation is green. The test explicitly states it does not render/sample
   pixels; actual pixel evidence remains separate.

An initial optional-Astrid-source startup attempt was not used as evidence:
the candidate worker's retained source copy lacked its Tool catalog. The
final focused files do not require that optional source and passed with the
source lane unset.

## Flat producer handoff for Viewing

Viewing may review this exact producer unit at commit
4720a864c81dc7002a9e95dbacf10cec8df5da81, tree
aa9eb31281e915fe32e7af6e4c7a30a2ff85e8ad. Its input contract is one derived
scalar from each verified original graph; editor/read geometry stays
unchanged. Its output contract is an existing render-boundary consumer input,
with the scalar stripped from authored/storage serialization and raw opaque
collisions restored from the retained identity-matched basis. Missing basis
fails closed with the draft retained. Independent producer evidence is 239
passing tests (179 + 60); actual pixels, audio, browser delivery and
consumer qualification are outside this handoff. Viewing should not treat
this report as approval of its separate consumer delivery review.

