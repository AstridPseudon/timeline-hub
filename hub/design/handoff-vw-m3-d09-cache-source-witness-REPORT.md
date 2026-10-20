# D09 cached-source witness

## Verdict

The retained-source proof after c456 is sufficient for successful fresh
frames, but not for cached PNG cards. Do not retire the private `visible_at`
fallback for cache hits yet. No product adapter was applied.

## Actual path inspected

- `astrid/sdk/timeline_filmstrip.py:852-913` builds the immutable capture
  authority, `capture_identity`, candidate working-copy marker, and compiled
  `scene_clips` ID/address map.
- `astrid/packs/rendering/actions/timeline_visualize/composed_frame.py:603-645`
  verifies that retained source, config, registry, and canonical Root profile
  agree. The provider adds `fps_rational`, `duration_frames`, and
  `resolved_theme` to its snapshot.
- `composed_frame.py:663-714` validates the final Root props, materialized
  asset bytes, resolved profile, and public `host_frames_at` rows.
- `composed_frame.py:795-812` retains rows only after every requested fresh
  PNG was copied successfully, then writes the PNG cache entry.
- `composed_frame.py:772-783` reads a cache hit as bytes only. It never
  restores `CaptureSceneLabels`.
- `composed_frame.py:750-751` exposes rows only for
  `fresh_scene_frames`.
- `filmstrip_cards.py:1684-1688` therefore calls legacy `addresses_at` when a
  card is cached; the public-row branch is only `1689-1694`.

## Witness results

The added pure test file is
`tests/packs/rendering/test_d09_cached_source_witness.py`. It calls the actual
`frame_cache_key` and `FrameCaptureCache`; it does not call a renderer, Root,
source preparation, or a scene-query process.

With a stable renderer-environment digest, changing each retained input
changed the exact cache key:

| Input | Current retained location |
| --- | --- |
| canonical revision | `metadata.capture_authority.parent_revision_id` |
| candidate | `metadata.working_copy.candidate_digest` |
| compiled ID/address map | `metadata.scene_clips` |
| Root profile inputs | `resolved_theme.visual.canvas` (plus snapshot `fps_rational` / `duration_frames`) |
| material/component asset digest | `registry.assets[*].digest` |
| source hash | `metadata.capture_identity` |

The same key is intentionally retained when only an
`astrid-attempt-*` materialization path changes. Existing environment-source
tests also show that changing renderer/effect source changes the key.

The cache directory after a write contains exactly `<key>.png`; it contains no
source identity, public rows, address map, profile, or asset/source digest.
Thus a cached PNG can be identified as bytes for the request, but cannot be
matched to computed public rows without another retained source binding.

The existing transport-only mixed-batch proof remains unchanged:
`test_mixed_cached_and_fresh_batch_has_facts_only_for_observed_frames` proves
one fresh card gets public rows while the cached card has no scene capture and
uses the legacy address fallback. This is the protected successful-fresh /
cache-card behavior and was not weakened.

## Minimal contract for orchestrator approval

If cache labels are to become public-row-only, extend the existing cache entry
with one optional source-bound public-row payload, written only after the same
successful fresh batch as the PNG:

```text
<key>.png + existing public scene payload:
  source_identity: existing capture_identity
  frames: {frame: existing host_frames_at answer}
  addresses: existing scene_clips projection
  basis: existing Root width/height/fps basis
```

The `frame_cache_key` remains the binding for the canonical revision,
candidate, compiled IDs, profile, registry/source hashes, frame, resolution,
and renderer environment. The payload is only the already-public
`host_frames_at` rows and existing address projection; it is not private
geometry, a journal, a cache-clear mechanism, an authority certificate, or a
new source factory/class schema.

Positive approval cases:

1. A successful fresh frame writes PNG plus rows; a new provider cache hit
   restores rows and labels through `labels_for_scene`, with `visible_at` made
   to fail the test.
2. A same-source retry with only an ephemeral attempt path change reuses the
   key and rows.
3. A changed canonical revision, candidate, compiled address map, Root
   profile, component/material digest, source hash, frame, resolution, or
   renderer source produces a different key and does not reuse the rows.

Negative approval cases:

1. Missing payload, mismatched `source_identity`, mismatched basis/address
   map, or incomplete frame set makes that card unqualified; it must not mint
   rows. Preserve the existing legacy/`UNCERTIFIED` label behavior until the
   replacement is approved.
2. A cache hit alone, with no successful fresh rows, never creates
   `CaptureSceneLabels` or calls `host_frames_at`/`visible_at` as if it had
   observed the frame.

This contract is a proposal only; no adapter, cache schema, or retirement was
landed in this worker.
