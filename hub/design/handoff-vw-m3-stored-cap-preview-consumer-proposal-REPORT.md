# D08 stored-cap preview consumer proposal

Status: unapplied, ready for paired App-producer review.

The consumer patch uses only the approved scalar `clip.app.canonicalTiming.storedOccurrenceDurationMs`. It creates a private invocation copy at the existing bounded-render boundary, replacing only the private copy's effective occurrence duration so the existing public evaluator, compiled transition vector, TimelineFramePreview, client-render input, Player metadata, and bounded extent all consume the same selected cap. The source editor config and authored/read projection are untouched.

The preview composition hook now carries an explicit private config/fact pair. That preserves the existing identity-based provenance boundary and forces a fresh private config when a new accepted/local fact arrives even if its flattened config is identical. The surface uses that pair for revision labels: local → saving → accepted is preserved, a late acknowledgement of A cannot relabel displayed B, and an old known C cannot relabel a fresh A. The panel frame preview receives the same private bounded config. No global save-status or polling graph was made authoritative.

The browser render path receives the selected private config, existing compiled transition vector, and recomputed private extent metadata. No `TimelineData.renderConfig`, DTO, store, source factory, counter, colon-ID parsing, new compiler, authored serialization, pins, projection/session change, or producer implementation was added. When the approved scalar is absent, the existing conservative path remains unchanged.

Files in the unapplied product patch:

- `canonicalRenderBounds.ts`
- `useVideoEditorPreviewComposition.ts`
- `useVideoEditorPreviewSurface.tsx`
- `VideoEditorAssetPanelSurface.tsx`
- `useClientRender.ts`
- `useRenderState.ts`
- `useTimelineState.ts`

The separate test patch adds only the mounted boundary tests described in [the test handoff](handoff-vw-m3-stored-cap-preview-consumer-proposal-tests.md). The exact commands and results are in [COMMAND](handoff-vw-m3-stored-cap-preview-consumer-proposal-COMMAND.md).

Evidence:

- Targeted mounted run: 5 files, 100 tests passed, exit 0.
- Both unapplied patches pass `git apply --check` against the clean b1ef App snapshot.
- No production App worktree, producer branch, or shared dependency was modified.

Decision boundary: this is not production-green evidence. The paired App producer must supply the scalar from the verified original occurrence on graph/local/recovery/accepted paths and prove its authored/wire/storage absence. After that producer lands, apply the two patches together and rerun the mounted suite plus the producer's focused serialization/projection tests.

Unverified by this worker: the producer interface and its recovery/serialization implementation, full App suite, browser/e2e behavior, actual codecs/rendering, and joint merge integration.
