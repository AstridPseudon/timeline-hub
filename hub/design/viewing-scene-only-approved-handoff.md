# Approved scene-only handoff

This is the private handoff between the Agent SDK caller and the existing
`rendering.timeline_visualize` executor. It is not a public CLI envelope or a
new Runtime DTO.

- The mode field is the existing top-level `mode` in the managed visualization
  authority object (the JSON carried in `filmstrip_authority` / the host
  authority context). The approved value is `scene_only`.
- The executor selects the existing `capture_snapshot` first, then the
  existing `filmstrip_snapshot`. It uses the saved/candidate snapshot and the
  host's already-admitted `timeline` and `assets_registry` files.
- The managed output artifact key remains the existing `filmstrip_bundle`.
  Its existing nested manifest entrypoint is extended with the relative
  `scene-answers.json` artifact; no new managed-output route is introduced.
- The scene artifact keeps the existing data names: `answers` is the ordered
  list returned by the public Scene query, `scene_clips` is the exact
  compiled-clip-to-address map carried by the same host-verified source that
  prepared Root, and `snapshot_label` is the existing bound
  revision/candidate label. The executor never copies either value from the
  outer authority metadata. A successful result has `snapshot_label.status`
  `committed` or `candidate`, `answers` for every frame in
  `range(duration_frames)`, and map keys exactly equal to the verified
  compiled `config.clips` IDs. An unavailable query has
  `snapshot_label.status` `unavailable`, label `revision unavailable`, empty
  `answers`, and an empty `scene_clips` map.

The executor treats `returncode: 0` as “the action ran”; it is not a Scene
success assertion. The Agent caller must check `snapshot_label.status` before
feeding answers into `scene_problems` or other findings, and must treat
`unavailable` as advisory unavailable rather than as an empty successful
scene. No new public exit-code policy is introduced here.

Before querying, the bound source must contain a well-formed `config.clips`
list with unique non-empty string IDs and the carried map must contain exactly
those IDs. After querying, the executor validates the complete ordered frame
extent and that every returned layer `clipId` belongs to that map. Missing,
stale, forged, or malformed source/config data is advisory unavailable; it
cannot publish the authority metadata's map.

The Agent caller should request the full canonical frame extent from the
snapshot's existing `duration_frames` value. The executor does not sample,
render PNGs, or change visibility/threshold rules.

The query helper is:

```python
_prepared_host_frames_at(
    timeline_path, assets_path, frames, *,
    staged_video, provenance_out_path, project_dir, composition_id,
    theme_path, min_free_gb, frame_output_dir,
    review=None, materialized_root=None, staging_parent=None,
    materialized_objects=None, composition_clip_types=frozenset(),
    encode_aac_at_stitch=False, composition_duration_frames=None,
) -> list[dict[str, Any]]
```

It depends on the host-owned `inherited_source(timeline_path, assets_path)`
from `astrid.core.rendering.verified_source`. That source is validated before
and after the query and the query runs inside the existing
`_prepared_remotion_root` lifetime. A source mismatch, stale input, forged
reference, or unavailable public host produces no scene answers and remains
advisory unavailable.
