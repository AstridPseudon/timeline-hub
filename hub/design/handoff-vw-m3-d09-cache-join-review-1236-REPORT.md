# D09 cached-label source-row join — independent review

Decision: **APPROVE**.

Reviewed author commit `1d69859c8` (`tl/vw-m3-d09-cache-label-row-join-1232`) and its exact handoff patch as source-only. The new `_filmstrip_cache.py` hunk removes only the carrierless `addresses_at` fallback: a missing `scene_for_frame(frame)` leaves PNG evidence usable and sets semantic `addresses` to `null`; an admitted public row continues through the existing source-bound facts/label path with `source_identity` and the existing opacity filter. No changed-hunk counterexample found.

The direct test hunks preserve the public-row positive, stale/forged rejection, exact-key/root-source/PNG-integrity controls, mixed cached/fresh separation, and the carrierless execution expectation as strict xfails. No DTO, source factory, authority/store, public-field, package/pin, saveNode, timing, crop, 2%, or unrelated writer change is present.

## Evidence

- Commands (run with `REVIEW_TMP` set to a temporary extraction of the author branch):
  - `PYTHONPATH="$REVIEW_TMP:/home/user/work/runtime" PYTHONPYCACHEPREFIX="$REVIEW_TMP/.pycache" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/pytest -p no:cacheprovider -q test_labels_overlay.py::test_existing_public_row_carrier_drives_labels_and_rejects_stale_or_forged_rows test_scene_cache_payload.py::test_new_provider_reuses_rows_without_query_or_private_visibility test_scene_cache_payload.py::test_default_provider_keeps_png_only_cache_reusable_across_owners test_scene_source_carry.py::test_mixed_cached_and_fresh_batch_has_facts_only_for_observed_frames test_labels_overlay.py::test_each_frame_index_row_marks_addresses_without_a_source_row_unavailable test_timeline_visualize_labels.py::test_compact_frame_index_rows_mark_unbound_addresses_unavailable test_timeline_filmstrip_execution.py::test_composed_capture_uses_remotion_for_requested_frames_without_video_frame_source` -> `6 passed, 4 xfailed`; the mixed source case also has `[native]`, which errored at missing provisioned Remotion peers.
  - Same command, selecting `test_scene_source_carry.py::test_mixed_cached_and_fresh_batch_has_facts_only_for_observed_frames[transport]` -> `1 passed`.
  - Same command, selecting `test_scene_source_carry.py::test_actual_source_join_queries_historical_scene_and_overlay[transport-text-card]`, stale/forged `test_scene_cache_payload.py::test_planted_stale_or_forged_entry_renders_fresh[{key-transport,root_source-transport,png-transport,forged_row-transport}]`, and integrity `test_payload_bindings_checked_after_owner_integrity[{key-transport,png_sha256-transport}]` -> `7 passed`.
  - `git -C /home/user/peteromallet/astrid-agent show --check --oneline tl/vw-m3-d09-cache-label-row-join-1232` -> passed.

- Source-only narrow run from an extracted author-branch snapshot: `6 passed, 4 xfailed`; the combined selection also attempted one `[native]` parametrization and errored because provisioned Remotion peers were absent. That native case was not used for qualification.
- Allowed transport rerun of the mixed cached/fresh case: `1 passed`.
- Allowed source/cache positive and negative selection (fresh public-row positive; stale/forged `key`, `root_source`, `png`, `forged_row`; binding `key`, `png_sha256`): `7 passed`.
- `git show --check` on the author commit: passed.

The patch was not applied to this review worktree; no product-applied or full/native/browser claim is made. No blockers for this review. Recommended next step: merge through the orchestrator queue and use the author’s reported scoped suite/central suites as the integration evidence.
