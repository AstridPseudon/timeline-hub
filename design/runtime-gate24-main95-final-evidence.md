# Runtime Gate2/Gate4 Main95 source evidence

Date: 2026-10-21 UTC. This is a source/evidence review; no suite was rerun.

## Verdict and exact sources

Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`, is the immutable Main95 candidate.
It is contract/client `0.2.14`, Runtime schema
`sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`,
and 76-artifact version
`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.

The final normal Agent source is `6efc81500a0e0688c2bb41e736503f0fc3e04abb`,
tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`. Its first parent is exactly
the Gate2 consumer `e35ad5e72ed9acc61d659a6b4b9c32d69208ab8d`, tree
`a2454c2cb472fa5404289c9f48bb7779d330879e`. The `6ef` commit changes only
five Agent source files and six Agent test files; it changes no generated
client, lock, schema, Runtime, or artifact bytes. Therefore the Gate2 result
transfers only to the unchanged acceptance/provider surface and the explicitly
overlapping cases below—not as blanket equivalence for all of `6ef`.

App’s independently approved normal pin is `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`,
tree `01fd2a04ff0c383ec5281043c7e5a4c843d1d835`, against the same Runtime
`95bd` producer. This is a pin/source approval, not matched adoption or a
cross-product Gate2/Gate4 result.

## Gate2 evidence

The final existing 51-case cohort passed against the exact normal `e35` Agent
and the Runtime95 producer:

- Result: `rt-m2-gate2-final-main014-current-proof-gate2-final-main014-normal-agent-e35ad5e7-proof-1021002537-14311`.
- Central snapshot tree: `e0cb9b7a56b88e0ed6555d930793eaa0f963a34b` (the
  snapshot includes the approved test-only fixture freshness change); the
  immutable producer identity in the preflight was Runtime `95bd` / tree
  `d3a290`.
- Command (exact recorded node list):

  ```sh
  env ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-e35ad5e7 PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-e35ad5e7 PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m "not darwin_native and not live" tests/test_timeline_commit_execution.py tests/test_timeline_commit_acceptance.py::test_atomic_acceptance_exact_recorder_projection_and_same_content_edge tests/test_timeline_commit_acceptance.py::test_identical_retry_after_restart_and_head_advance tests/test_timeline_commit_acceptance.py::test_changed_payload_and_publication_only_cas_refuse_without_writes tests/test_timeline_commit_acceptance.py::test_invalid_prepared_values_are_atomic tests/test_timeline_commit_acceptance.py::test_failure_after_receipt_rolls_back_every_row tests/test_timeline_commit_acceptance.py::test_failure_between_projection_steps_rolls_back_and_restart_retry_publishes_once tests/test_timeline_commit_acceptance.py::test_complete_recorder_roundtrip_and_replay_after_restart tests/test_timeline_commit_integration.py::test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip tests/test_timeline_commit_integration.py::test_real_door_concurrent_disjoint_moves_accept_and_rebase tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary
  ```
- Result: **51 passed in 25.12s**, exit 0. The exact-normal tuple preflight
  passed before pytest. No repository full, browser, render, or release suite
  was run for this result.

The retained corrected-source live HTTP/concurrency/crash proof was result
`rt-m2-gate2-corrected014-concurrency-current-gate2-actual-http-crash-corrected014-1020225848-28982`:
**7 passed in 18.22s**. It used older Runtime `6e845a1` / tree `7f11d7e` and
Agent `b43cd95` / tree `1d44801`; it is useful evidence for the seven selected
HTTP/concurrency/crash behaviors, but is not Main95 source evidence.

### What transfers to final Agent6ef

The five changed source files are `astrid/sdk/timeline/{capture,check,checkout,native_checkout}.py`
and `astrid/sdk/timeline_elements.py`. The final Agent qualification directly
covered the two relevant new seams against Runtime95:

- `agt-m2-main95bd-forward-latest-gates-main95bd-added-gates-integration-1021001525-26586`:
  **4 passed in 22.23s**, exact `6ef`/`2ed2` Agent and `95bd`/`d3a` Runtime.
- `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends`
  covers the `capture.py` output-rate/rational move path and lossless native
  frontends.
- `tests/sdk/test_timeline_selected_schema_runtime.py::test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart`
  covers the retained selected-PARAM source through the new checkout/native
  checkout/elements path, including removal and restart.

These four passes support the affected overlaps; they do not replay the 51
Gate2 assertions with final6ef. In particular, the connected managed-scene
branch added to `check.py`, and the other unexercised branches in the new
selected-PARAM/native-checkout guards, remain outside the 51-case result.

## Gate4 evidence

Runtime candidate full result `rt-m2-main014-reference-fixture-clock-repair-full-retained-owned-temp-integration-1020233140-31902`
passed **5,988**, with 26 skipped, 15 xfailed, and 12 warnings; exit 0, 353.01s.
Its exact central command was `env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-full-temp-retain-all-final/runtime-full-retained-temp.py -- /home/user/work/venv-runtime/bin/python -m pytest -q -n 3`.
The same candidate also has the recorded scoped six-node result
`rt-m2-main014-reference-fixture-clock-repair-reference-fixture-agent-current-integration-1020233053-5889`:
**6 passed in 2.75s**, plus the recorded Gate4 client/generator lanes of **29
Python + 61 TypeScript** passes and the normal artifact checks. This qualifies
the Runtime candidate’s full/transport/client surface. It does not execute the
final Agent6ef semantic source as a synchronized four-product Gate4 run, and
it does not prove App10fa browser/native adoption.

App’s independent pin result was
`ap2-m2-main014-home-pin-independent-qualification-targeted-sourceguard-integration-1021000128-22672`:
**13 vendor-lock + 36 fake-Runtime tests passed**; the independent review also
retains 127 client and 426 capture tests. It verifies App10fa’s lock/generated
bytes and source provenance only. The required same-cohort Agent/App current
source lane remains open.

## Fixture and assertion audit

The only Runtime source delta in this worktree is the approved test helper in
`tests/test_timeline_reference_authority.py`. It imports `sqlite3` and
`now()`, then updates `command_idempotency.created_at` only for copied legacy
`reference.create` and `reference.associate` rows before `RuntimeService`
startup. It does not update any `timeline.commit` row, receipt body, accepted
history, retention/expiry implementation, or production data. Existing expiry,
race, crash, changed-key, and no-write assertions remain intact. No test was
converted to a refusal, skipped, or weakened.

## OPEN gaps and precise next nodes

- No final6ef replay of the full 51-case Gate2 cohort exists. Do not label the
  e35 51-pass result as a blanket final6ef result. If source closure is needed,
  run only the affected current-source nodes against Agent6ef/Runtime95: the
  four recorded Gate2 live acceptance/crash nodes, plus the two final6ef nodes
  named above. Do not submit a duplicate 51-case suite.
- The new managed-scene check is not covered by the final6ef four-case source
  qualification. Its precise remaining node is
  `tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result`.
  This is a viewing/check seam, not evidence that Gate2 failed.
- The current ordinary Main95 hold-clear positive remains open:
  `tests/test_timeline_ordinary_http.py::test_ordinary_http_authored_source_window_hold_clear_preserves_timing`
  failed before Runtime because `clip.add v1` rejects `from`; the bare
  zero-duration refusal passed. The approved setup-only repair must preserve
  the source-window assertions and must not rewrite accepted history.
- Coordinated Agent/App adoption, publication, and activation remain held.
  Runtime95, Agent6ef, and App10fa are individually source-qualified within
  the scopes above; no synchronized current-source browser/full journey is
  claimed.
