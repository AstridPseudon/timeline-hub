# Runtime integration full: `a020` result classification

## Decision

The one requested central run completed, but it is not a product pass. The
seven established baseline failures remain, and the additional failures/errors
are environmental free-space-floor refusals. No changed-product assertion
regression, import failure, or new genuine Runtime failure is established by
this artifact. The run must not be treated as an all-green gate.

## Immutable run identity

The service request was for `integration:runtime`, suite
`full-restore-integration`, requested at `2026-10-20T20:17:08Z`.

| Item | Recorded value |
|---|---|
| Run | `runtime-full-restore-integration-1020201708-8649` |
| Snapshot tree | `9243cb9227d97515bf87a46bd694a7c72c520c04` |
| Source commit for that tree | `a020a1c77a07aa657efb60b0442450209e55e470` |
| Snapshot key | `932fe1861af8148b0d28170a2141cefe` |
| External Agent | `53af5383802e995f78b3693a22d54b3e86062eff` |
| External App | `20ea14c26526fe4924354f10a177aebbaf6002bc` |
| External Composition | `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8` |
| Service status / exit | `fail` / `1` |

The service snapshot files (`request`, `snap`, `ext`, `summary`) are under
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/runtime-full-restore-integration-1020201708-8649/`.
Later integration changes, if any, are outside this result.

## Exact command and counts

The central service ran:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
```

Result: **5409 passed, 36 failed, 18 skipped, 18 xfailed, 12 warnings, 92
errors** in `500.36s` (`8:20`); service elapsed `502s`. The error count is
included separately by pytest; the 36 failed count is the node list under the
failure summary.

The manager reported 8.9 GiB free after guarded cleanup before requesting this
run. During the run, the service log records the storage guard refusing
admissions; observed free space reached 3.8 GiB, and the post-run filesystem
check showed 4.1 GiB free with `/tmp/pytest-of-root` at 5.0 GiB. This is real
storage-floor behavior, not a floor override. No under-floor product result is
claimed.

Representative admission evidence from the log reports:

```text
available_bytes=4556783616
floor_bytes=4294967296
required_bytes=269552151
scratch_bytes=268435456
reason=insufficient_storage
```

The first exception for the additional cohorts is consistently:

```text
runtime_protocol.errors.ConflictError: task admission refused: storage estimate would cross the free-space floor
```

The log contains no `ModuleNotFoundError`, `ImportError`, or comparable import
failure.

## Comparison with the established seven-node baseline

The prior classification `runtime-full30033-classification.md` recorded
`5524 passed / 7 failed / 18 skipped / 18 xfailed`, with exactly the seven
known boundary nodes. The current result contains those same seven node IDs,
plus 29 failed nodes and 92 setup/test errors caused by storage admission.

The seven inherited baseline nodes are:

| Node | First cause in this run | Classification |
|---|---|---|
| `tests/test_runtime_boundary.py::test_token_signal_exit_race_uses_only_retained_child_exit` | `AttributeError: '_CustodyChild' object has no attribute 'returncode'` at `runtime_protocol/platform.py:698` | Inherited Linux custody/test-double baseline |
| `tests/test_runtime_boundary.py::test_unverifiable_live_owner_retains_cleanup_uncertainty` | Same `returncode` `AttributeError` at `runtime_protocol/platform.py:698` | Inherited baseline |
| `tests/test_runtime_boundary.py::test_primary_start_error_retains_cleanup_uncertainty_as_cause` | Primary `OSError("ready reply failed")` is followed during cleanup by the same `returncode` `AttributeError` | Inherited baseline |
| `tests/test_runtime_boundary.py::test_unowned_handle_does_not_infer_termination_from_poll` | Same `returncode` `AttributeError` at `runtime_protocol/platform.py:698` | Inherited baseline |
| `tests/test_runtime_boundary.py::test_runtime_spawn_retains_owner_and_wires_escrow_before_seal` | Expected `RuntimeCustodyLaunchUncertain` was not raised | Inherited Linux custody/test-double baseline |
| `tests/test_runtime_boundary.py::test_retained_stop_owner_reclaims_release_before_term_kill_and_positive_wait` | Fake `Child` cleanup reaches the missing `returncode` attribute at `runtime_protocol/platform.py:698` | Inherited baseline |
| `tests/test_zero_shim_boundary.py::test_start_does_not_inject_checkout_into_child` | Mocked identity first raises `KeyError: 'pid'`; cleanup then reaches fake-process `returncode` `AttributeError` | Inherited baseline |

The current snapshot does not modify either baseline test file or
`runtime_protocol/platform.py` relative to the prior `30033` snapshot. The
node set and first causes therefore remain inherited rather than changed by
the current integration batch.

## Every additional failed node

All 29 additional failed nodes have the same exact first cause: the test
fixture's first task/media admission is refused by the real storage guard
before the intended assertion or publication/authority behavior is reached.
They are environmental-floor outcomes, not assertion failures.

### Effect authority (8)

- `tests/test_timeline_effect_authority.py::test_same_key_changed_admission_refuses_without_snapshot_writes[service-both-managed-render-current]`
- `tests/test_timeline_effect_authority.py::test_same_key_changed_admission_refuses_without_snapshot_writes[http-both-managed-render-absent]`
- `tests/test_timeline_effect_authority.py::test_exact_managed_snapshot_replay_keeps_identity[service-allowed-current]`
- `tests/test_timeline_effect_authority.py::test_exact_managed_snapshot_replay_keeps_identity[service-allowed-stale]`
- `tests/test_timeline_effect_authority.py::test_exact_managed_snapshot_replay_keeps_identity[service-allowed-absent]`
- `tests/test_timeline_effect_authority.py::test_exact_managed_snapshot_replay_keeps_identity[service-controlled-forbidden-fixture-current]`
- `tests/test_timeline_effect_authority.py::test_exact_managed_snapshot_replay_keeps_identity[service-controlled-forbidden-fixture-stale]`
- `tests/test_timeline_effect_authority.py::test_exact_managed_snapshot_replay_keeps_identity[service-controlled-forbidden-fixture-absent]`

First cause for each: `ConflictError` from task admission with “storage
estimate would cross the free-space floor”, before the changed-key or replay
assertion.

### Render publication (3)

- `tests/test_timeline_render_publication.py::test_publication_is_fenced_atomic_and_exactly_replayable`
- `tests/test_timeline_render_publication.py::test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence`
- `tests/test_timeline_render_publication.py::test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart`

First cause for each: the render fixture's task admission raises the same
storage-floor `ConflictError`, before publication/fence behavior runs.

### Render publication authority (17)

- `tests/test_timeline_render_publication_authority.py::test_tracked_target_refuses_without_invalidating_canonical_history`
- `tests/test_timeline_render_publication_authority.py::test_existing_same_project_unadmitted_target_refuses_before_checkpoint`
- `tests/test_timeline_render_publication_authority.py::test_missing_or_malformed_admitted_target_fails_closed[publication0]`
- `tests/test_timeline_render_publication_authority.py::test_missing_or_malformed_admitted_target_fails_closed[False]`
- `tests/test_timeline_render_publication_authority.py::test_missing_or_malformed_admitted_target_fails_closed[publication2]`
- `tests/test_timeline_render_publication_authority.py::test_missing_or_malformed_admitted_target_fails_closed[main]`
- `tests/test_timeline_render_publication_authority.py::test_missing_or_malformed_admitted_target_fails_closed[publication4]`
- `tests/test_timeline_render_publication_authority.py::test_missing_or_malformed_admitted_target_fails_closed[publication5]`
- `tests/test_timeline_render_publication_authority.py::test_missing_or_malformed_admitted_target_fails_closed[publication6]`
- `tests/test_timeline_render_publication_authority.py::test_missing_or_malformed_admitted_target_fails_closed[publication7]`
- `tests/test_timeline_render_publication_authority.py::test_missing_or_malformed_admitted_target_fails_closed[publication8]`
- `tests/test_timeline_render_publication_authority.py::test_inconsistent_native_target_cannot_override_legacy_admission`
- `tests/test_timeline_render_publication_authority.py::test_corrupt_immutable_spec_cannot_supply_target_authority`
- `tests/test_timeline_render_publication_authority.py::test_canonical_tracking_after_prepare_refuses_before_publication_writes`
- `tests/test_timeline_render_publication_authority.py::test_exact_published_checkpoint_replays_before_live_target_changes`
- `tests/test_timeline_render_publication_authority.py::test_tracking_is_scoped_to_the_publication_target`
- `tests/test_timeline_render_publication_authority.py::test_legacy_head_without_canonical_publication_remains_publishable`

First cause for each: the authoring/render fixture's initial admission raises
the same storage-floor `ConflictError`, before target-authority or publication
assertions run.

### Text selection (1)

- `tests/test_timeline_text_selection.py::test_media_selection_still_rejects_text`

First cause: `settle_media()` cannot create the prerequisite task because the
storage estimate crosses the free-space floor; the text-selection assertion is
not reached.

## Errors

All 92 pytest `ERROR` outcomes are likewise setup/fixture failures whose first
Runtime exception is the same storage-floor `ConflictError`. They cluster in
the producer checkpoint, producer record-boundary, producer guard, and
verified-media suites. The log's error summary begins at the checkpoint and
record-boundary nodes and includes the producer-guard and verified-media
families; it does not show an independent import or assertion cause.

## Recommended next step

Do not repair product code, weaken assertions, mark these nodes xfail, or rerun
this full. The actionable owner is the Runtime manager/test-service operator:
repeat the affected targeted cohorts only after guarded cleanup restores the
documented free-space headroom, preserving the real storage guard. Separately,
the existing seven-node Linux custody baseline remains owned by Runtime and
needs its own small boundary/test-double repair before an all-green full can be
claimed. This run provides no evidence requiring a new product fix.

## Scope

This worker waited on the already-requested run and read its immutable service
artifacts. It did not request another full or any new test, edit product code,
modify integration, install/pin/release dependencies, or override the storage
floor.
