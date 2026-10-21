## Fast-lane producer activation

The managed rendering callback does not survive its executor lifetime:
`RemotionFrameProvider` retains `CaptureSceneLabels` only while the capture is
running and closes before the result is returned. The existing durable carrier
is the managed `filmstrip_bundle` result with `scene-answers.json` and its
provenance.

`prepare_pair` now reuses the existing private `scene_only` mode for the exact
published render and the candidate source. It validates the returned bundle
through the existing `_scene_only_spans` / `_scene_only_bundle_payload` join,
then materializes source-bound `CaptureSceneLabels` rows for the already
approved fast-lane `frame_providers` seam. No live provider crosses cleanup;
there is no new public entrypoint, DTO, authority field, store, or certificate.

The original no-carrier path remains unchanged. A direct regression proves a
successful materialized result reaches public labels while private visibility
math is forbidden. Stale, forged, incomplete, or unavailable artifact rows
remain advisory-unavailable through the existing scene join.

Evidence: 24 direct scene/fast-lane tests, 5 managed prepare-pair integration
cases, 4 checkout fast-lane cases, 36 adjacent rendering tests, Ruff, and
`git diff --check` all passed. No full/browser/socket/install suite was run.
