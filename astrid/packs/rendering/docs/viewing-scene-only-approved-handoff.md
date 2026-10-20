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
  list returned by the public Scene query, `scene_clips` is the existing
  compiled-clip-to-address map from `snapshot.metadata.scene_clips`, and
  `snapshot_label` is the existing bound revision/candidate label. An
  unavailable query returns the same label shape with status `unavailable` and
  an empty `answers` list.

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
