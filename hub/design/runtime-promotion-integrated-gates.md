# Runtime catalog-promotion integrated gates

## Verdict

The reviewed catalog-promotion candidate is present on actual Runtime integration and is qualified by the bounded promotion gates. The required post-merge full is **not green**: its failures are seven known Runtime baseline nodes plus seven new visual-seam nodes that remain unclassified here. No promotion node failed.

The review document's **APPROVE** verdict for `4c1a1a30a6dfed4b1d0c7674fe6f8bfc23aab15f` / tree `67f0f65ff6df9595b452f23c2c0fbbf262898cee` is supported. At verification time actual integration was merge `81f8c7e0b22c34804015c054762af3d737e4698a`, tree `0e3a5b938d9ca489fc760b09d34b02d4ac9aad51`, with `4c1a1a3` as its second parent. The candidate is still an ancestor of the later actual integration head.

## Bounded gates

All central snapshots below used Runtime tree `0e3a5b938d9ca489fc760b09d34b02d4ac9aad51`.

```text
request-test integration:runtime targeted --files \
  tests/test_shot_candidate_promotion.py::test_candidate_promotion_is_atomic_fixed_point_and_byte_stable_on_replay \
  tests/test_shot_candidate_promotion.py::test_candidate_provenance_is_verified_before_promotion \
  tests/test_timeline_shot_authority.py::test_http_auth_and_scope_checks_precede_retirement[item-promote] \
  tests/test_timeline_shot_authority.py::test_http_foreign_project_never_mutates_shot[item-promote] \
  tests/test_timeline_verified_media_http.py::test_public_verified_image_old_new_video_and_closed_query_without_writes \
  tests/test_timeline_verified_media_http.py::test_verified_read_requires_credential_scope_and_door_origin
```

Result `runtime-targeted-1020150541-31828`: **6 passed**. This covers the two original HTTP promotion positives and unchanged current scope/auth/MIME controls, without an Agent checkout.

```text
request-test integration:runtime occupancy-integration --files \
  tests/test_shot_candidate_promotion.py::test_catalog_promotion_preserves_accepted_film_and_retries_before_live_guards \
  tests/test_shot_candidate_promotion.py::test_catalog_promotion_prevents_native_overwrite_after_historical_reuse \
  tests/test_timeline_projection_occupancy.py::test_actual_provider_historical_slot_rematerializes_after_verified_restore
```

Result `runtime-occupancy-integration-1020150638-8672`: **3 passed** with `ASTRID_CHECKOUT=/home/user/work/agent` and `PYTHONPATH=$PWD:/home/user/work/agent`. These are the accepted-film/current-catalog, newer-owned-slot/C4 refusal, and existing C4 rematerialization controls.

```text
request-test integration:runtime restore-integration --files \
  tests/test_project_reference_catalog.py::test_catalog_changes_after_accepted_move_preserve_pinned_film_head_history_and_cas
```

Result `runtime-restore-integration-1020150732-31448`: **1 passed**, with the same Agent-aware environment.

Local bounded checks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider tests/test_shot_candidate_promotion.py::test_catalog_promotion_checks_bytes_and_rolls_back_before_receipt
# 1 passed

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B scripts/artifact_manifest.py --check
# contract/artifacts.json is current

git diff --check 16acbb6..HEAD
# pass
```

## Required full

Exactly one full request was made: `rt-m2-promotion-integrated-gates-full-restore-integration-1020150647-16434`. It waited behind an already-running Agent full; no second Runtime full was submitted.

START-authoritative snapshot:

```text
tree: 0e3a5b938d9ca489fc760b09d34b02d4ac9aad51
command: env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
external Agent: 30fc8dd154015a7c58cf4ce7b065ccc46f470ee8
external App: 9d518546df880ec515f2f424c55073193f2a2e64
external Composition: 5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8
result: 5523 passed, 14 failed, 18 skipped, 22 xfailed, 12 warnings, 351.09s
```

Comparison with prior full `runtime-full-restore-integration-1020130236-16608`: **5533 passed / 8 failed / 18 skipped / 24 xfailed**. The inherited `test_door_transport.py::test_audit_lines_without_credentials` failure is absent after `16acbb6`; the seven baseline failures remain. The full is therefore not an all-green claim.

The seven baseline failures, unchanged from the recorded baseline, are:

```text
tests/test_runtime_boundary.py::test_token_signal_exit_race_uses_only_retained_child_exit
tests/test_runtime_boundary.py::test_unverifiable_live_owner_retains_cleanup_uncertainty
tests/test_runtime_boundary.py::test_primary_start_error_retains_cleanup_uncertainty_as_cause
tests/test_runtime_boundary.py::test_unowned_handle_does_not_infer_termination_from_poll
tests/test_runtime_boundary.py::test_runtime_spawn_retains_owner_and_wires_escrow_before_seal
tests/test_runtime_boundary.py::test_retained_stop_owner_reclaims_release_before_term_kill_and_positive_wait
tests/test_zero_shim_boundary.py::test_start_does_not_inject_checkout_into_child
```

The seven additional full-run failures are visual-seam nodes. They are new relative to `16608` and remain unclassified in this attribution record:

```text
tests/test_visual_seam_admission.py::test_managed_render_freezes_child_effects_and_offset_from_pinned_closure
tests/test_visual_seam_admission.py::test_managed_render_preserves_asset_identity_from_the_pinned_asset_scope[parent]
tests/test_visual_seam_admission.py::test_managed_render_preserves_asset_identity_from_the_pinned_asset_scope[parent-media-id]
tests/test_visual_seam_admission.py::test_managed_render_preserves_asset_identity_from_the_pinned_asset_scope[shot]
tests/test_visual_seam_admission.py::test_managed_render_preserves_asset_identity_from_the_pinned_asset_scope[internal]
tests/test_visual_seam_admission.py::test_publication_and_render_preserve_uncovered_child_with_advisory_report[clips0]
tests/test_visual_seam_admission.py::test_publication_and_render_preserve_uncovered_child_with_advisory_report[clips1]
```

The raw log records the observed admission failure, but this report does not promote that observation into a final classification. These seven nodes are unverified under a sufficiently free disk and should not be relabeled as promotion regressions without a clean rerun.

## New/changed-node classification

- Original promotion HTTP positives: both passed in the explicit central lane and did not appear in the full failure set.
- New byte/receipt rollback control: passed locally.
- New accepted-film/retry and newer-owned-slot/C4 controls: **3/3 passed** in Agent-aware central integration, including the existing C4 rematerialization neighbor.
- New promotion authority parameter cases (`item-promote` auth and foreign-project): passed in the explicit central lane.
- New native historical-render retry node from the preceding merge: no failure in the full result.
- Changed direct-store stale-version authority control: no failure in the full result.
- The seven visual-seam failures above are newly observed full-run failures relative to `16608`; they are not new promotion nodes, and remain unclassified.

## Limits and next steps

The full START snapshot is authoritative. During the full run, actual `/home/user/work/runtime` advanced after START to merge `a51af885ea631c695a857985239c7fe7bf2e871f` / tree `7c6ab6700307309a7942e64eb4d0c6c7cc42b681` (`tl/rt-m2-selected-media-cas-integrity`); that later CAS merge was not part of the full result. The separate `c45` text resolution was also not part of it. The promotion candidate remains an ancestor of the later source.

No product/test/fixture/schema/client/pin change was made by this worker. The seven baseline failures remain open, and the seven new visual-seam failures need a future central rerun when the test service has enough free space; they remain unclassified here. No browser, live external service, or owner-film claim follows from this report.

