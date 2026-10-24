# Read-only census/recovery report

## Verdicts

- Full-suite result: **FAIL** — exit 1.
- Exact 36-node coverage: **PASS** — retained log contains exactly 36 `FAILED` lines.
- Counts: **PASS** — 6479 passed, 36 failed, 26 skipped, 15 xfailed, 0 errors, 0 XPASS, 0 deselected, 12 warnings, 416.59s.
- Snapshot: **PASS** — Runtime HEAD `458595850c...`; retained external tuple matches Agent `b61cebe8...`, App `7135ac72...`, Composition `635f4de0...`.
- Recovery: **PASS** — `/home/user/work/runtime` clean at `458595850c...`; `contract/artifacts.json` is regular, byte-equal to HEAD, SHA256 `7c541b705a9dbc0827ed2e81a847455402b1d475491de702cde7ef85f4a8235d`.
- Pre-existing/D32 classification: **UNKNOWN**, not guessed; no baseline was run.
- Review changes: **PASS** — no source, contract, fixture, client, pin, or schema changes. Worktree remains clean.

## Exact failed nodes

Manifest/conformance — 3:

- `tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current`
- `tests/test_recorded_responses.py::test_rerecording_is_byte_identical_to_committed_responses`
- `tests/test_recorded_responses.py::test_unnormalized_bodies_satisfy_their_contract_schema[publish_conflict_409]`

Retired-route boundary — 2:

- `tests/test_spec_reference.py::test_parent_receipt_compaction_preserves_publication_integrity`
- `tests/test_stage1_runtime_contract_completion.py::test_http_target_mutations_require_idempotency_key`

Headless overwrite — 10:

- `tests/test_timeline_headless_overwrite_refused.py::test_empty_default_over_authored_headless_shell_is_refused_untouched`
- `tests/test_timeline_headless_overwrite_refused.py::test_empty_default_over_empty_headless_shell_is_refused_untouched`
- `tests/test_timeline_headless_overwrite_refused.py::test_empty_default_on_a_fresh_timeline_is_accepted_and_replays`
- `tests/test_timeline_headless_overwrite_refused.py::test_empty_parent_over_hidden_nonempty_content_of_a_headless_timeline_is_refused_untouched`
- `tests/test_timeline_headless_overwrite_refused.py::test_genuinely_empty_headless_timeline_still_accepts_expected_head_null`
- `tests/test_timeline_headless_overwrite_refused.py::test_cas_correct_republish_after_reading_the_head_is_accepted`
- `tests/test_timeline_headless_overwrite_refused.py::test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[timeline_references]`
- `tests/test_timeline_headless_overwrite_refused.py::test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[timeline_shots]`
- `tests/test_timeline_headless_overwrite_refused.py::test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[snapshot]`
- `tests/test_timeline_headless_overwrite_refused.py::test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[dependency]`

Null-speed retained — 6:

- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[None-child]`
- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[None-parent]`
- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[speed1-child]`
- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[speed1-parent]`
- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[3/2-child]`
- `tests/test_timeline_null_speed_retained.py::test_legacy_visual_publisher_cannot_seed_retained_speed_shapes[3/2-parent]`

Legacy occupancy — 15:

- `tests/test_timeline_legacy_occupancy.py::test_legacy_publication_refuses_unrelated_destination_before_any_write[False-False]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_publication_refuses_unrelated_destination_before_any_write[False-True]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_publication_refuses_unrelated_destination_before_any_write[True-False]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_publication_refuses_unrelated_destination_before_any_write[True-True]`
- `tests/test_timeline_legacy_occupancy.py::test_exact_f1_over_http`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_occupied_destination_without_shot_head_is_not_adopted[False]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_occupied_destination_without_shot_head_is_not_adopted[True]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_closure_update_and_exact_retry_precede_live_checks`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_destination_requires_verified_current_closure[receipt]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_destination_requires_verified_current_closure[occurrence]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_destination_requires_verified_current_closure[digest]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_destination_requires_verified_current_closure[projection]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_current_destination_requires_verified_current_closure[removed]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_historical_reuse_keeps_newer_global_shot_head[False]`
- `tests/test_timeline_legacy_occupancy.py::test_legacy_historical_reuse_keeps_newer_global_shot_head[True]`

## Concrete causes

- Manifest: current generated `__init__.py` SHA differs from the tracked manifest entry. Classification: **ours**, R0/generated-artifact setup. Repair: regenerate `contract/artifacts.json`.
- Recorded responses: runtime emits `410 retired_route`, while the committed fixture expects `409 conflict`; `common.json` also excludes `retired_route`. Classification: **ours**, R5 contract/fixture conformance.
- Remaining 33: first exception is the direct `_require_timeline_command()` boundary at `runtime_protocol/service.py:1652`; `publish_parent_composition()` reaches it at line 2796. HTTP variants return 410 before legacy occupancy/headless/speed assertions execute. Classification: **ours**, retired fixtures needing v2 commit-path migration or dedicated 410/no-write assertions.

The retained full command was:

```text
env ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
```

I did not rerun it or any tests. No full-pass or final-gate claim is made.

## Limits and next steps

The worker report establishes that only the named manifest artifact was restored; the transient before-state is unavailable for independent reconstruction. Current HEAD, cleanliness, regular-file status, byte equality, and exact SHA were independently verified.

Recommended next steps are the three targeted repair groups above, then the normal checks: artifact manifest, generated clients/conformance, and the retired-route fixture migration. Production caller usage and the full C0v2 request/reply shapes remain unchanged by this review.