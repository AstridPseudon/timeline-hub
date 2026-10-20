# Runtime M2 retirement test census

Scope: Runtime `845db0a` (`tl/rt-m2-replay-cohort-seventh`), beyond the existing 43-test `tests/test_shot_composition_runtime.py` map. This is a static source census plus pytest collection; it is not a full-suite result.

## Disposition

- **Fixture-only migration:** the retired writer only builds canonical rows needed by a read, restore, render-admission, or integrity test. Replace that setup with a captured realm or a trusted `/v1` commit fixture; preserve the assertions about the surviving behavior.
- **Supported behavior requiring replacement:** the test asserts a positive edit, retry, CAS, idempotency, media pin, shot/item/reference, binding, or render-settlement behavior. Keep the test and port the behavior to EditCommands or revision-pinned `rendering.render`; do not delete it or blanket-xfail it.
- **Authority rejection already proven:** the test intentionally exercises a retired route/effect and asserts zero-write refusal. Keep the rejection proof; it is not a migration target.

## Positive legacy consumers requiring replacement

### Canonical timeline/clip writers

- `tests/test_timeline_clip_replacement.py`: `test_replace_timeline_clip_is_atomic_cas_and_exactly_replayable`, all six source-integrity/refusal cases (`test_replace_timeline_clip_rejects_cross_project_source` through `test_replace_timeline_clip_generic_visual_media_requires_video_stream`), `test_replace_timeline_clip_replays_after_intervening_edit_and_reopen`, and `test_replace_timeline_clip_public_http_route`. The setup at `:59` and `:211` also calls retired `create_timeline_document`; preserve atomic replacement, source ownership/type/duration checks, exact retry, and reopen behavior through a command.
- `tests/test_stage1_runtime_contract_completion.py::test_targeted_mutations_replay_the_same_committed_receipt`: `update_timeline`, archive, and recover are positive legacy timeline edits. Preserve receipt/event ordering and replay through command coverage; the ordinary `document.create` assertion in the same test remains supported.
- `tests/test_runtime_domains.py::test_generated_python_client_exercises_versioned_domains_on_real_daemon`: positive `update_timeline` and stale-version behavior. `test_generated_domains_preserve_project_media_and_timeline_recovery` additionally covers timeline update/archive/recover plus mounted shot/reference edits; it is a supported-domain journey, not a route-retirement test.
- `tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`: positive timeline shot/reference create replay, changed-key conflict, and non-overwrite behavior. Port the assertions to canonical shot ownership and command idempotency.

### Project shot/item, reference/association, and text binding writers

- `tests/test_runtime_e2e.py::test_project_shot_reference_crud_isolated_idempotent_and_restart_durable`: the whole CRUD journey at `:191-234` is still a positive direct-writer consumer. It covers project isolation, exact create replay, changed-key conflict, shot archive/recover, reference archive/recover, item add/reorder/remove, association primary selection, reference linking, and restart reads. It needs the Agent command schemas and Runtime exact media/reference pins; it must remain an end-to-end preservation test.
- `tests/test_shot_candidate_promotion.py::test_candidate_promotion_is_atomic_fixed_point_and_byte_stable_on_replay` and `test_candidate_provenance_is_verified_before_promotion`: shot creation, item creation, candidate promotion, stale-head refusal, provenance validation, invalidation of dependent plate/proxy/timeline assets, and byte-stable replay. This is supported shot/item behavior, not an authority refusal.
- `tests/test_shot_text_bindings.py::test_set_is_deterministic_project_scoped_and_replays`, `test_set_rebind_and_event_order`, `test_invalid_utf8_and_size_are_zero_write`, and `test_identity_digest_is_sha256`: positive text-binding set/rebind semantics plus validation and event ordering. Runtime can retain immutable media reads, but Agent must provide command-based source/speech binding captures.
- `tests/test_runtime_domains.py::test_project_media_mutations_roll_back_before_idempotency_replay`: the positive create/replay half still covers atomic rollback and exact idempotency for shot/reference writes. Replace the direct setup with a command fixture while retaining the failure seam and no-row assertions.

### Render publication/settlement

- `tests/test_timeline_render_publication.py::test_publication_is_fenced_atomic_and_exactly_replayable`, `test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence`, and `test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart`: positive `publish_timeline_render` behavior remains a migration target. Preserve fence checking, atomic output/publication rows, changed-payload conflict, cancel behavior, crash recovery, and restart retry under revision-pinned `rendering.render`. Its `create_timeline_document` setup at `:47` is fixture-only.
- Cross-manager dependency: Agent/Viewing must supply the revision-pinned render-settlement contract and retry/restart proof; Runtime should not restore a publication alias or scene evaluation in save.

## Fixture-only legacy consumers

- `tests/test_timeline_native_inspection.py`: the 20 inspection/read families from `test_config_only_parent_clips_project_maple_and_parent_media_rows` through `test_inspection_timing_context_keeps_off_page_transition_siblings` call `publish_parent_composition` only to seed canonical parent/child closure. Migrate the common `_service`/publication setup to a trusted commit or captured closure. Preserve selector/range ordering, rational timing, pinned revision reads, omission/byte-budget evidence, cursors, PNG custody, and canonical-head naming.
- `tests/test_timeline_commit_restore_port.py`: `_seed` calls `publish_parent_composition` for every restore test. Replace only that seed with the captured restore-history fixture or command acceptance; retain all restore chronology, exact bytes, source closure, authority, and idempotent retry assertions, including both budget parameters.
- `tests/test_timeline_cutover.py`: `_service` uses `create_timeline_document` and `publish_parent_composition` for the three cutover/audit tests. Seed the legacy shell and canonical head from the fixture/verified baseline; keep the audit and public-route retirement assertions.
- `tests/test_realm_admission_hardening.py::test_revision_admission_legacy_declared_media_boundaries`: the two publisher calls create a deliberately malformed dependency graph before offline inspection. Replace setup with a canonical fixture/commit plus the same controlled dependency mutations; retain the missing/foreign/digest/duplicate/ordinal diagnostics.
- `tests/test_streaming_media_io.py::test_concurrent_upload_and_real_timeline_view_preserve_health_and_receipts`: publication is setup for the concurrent view/health test. Seed a committed revision; retain upload concurrency, view behavior, and receipt/health assertions.
- `tests/test_visual_seam_admission.py::test_publication_rejects_unsafe_resolved_child_without_partial_rows`, `test_managed_render_freezes_child_effects_and_offset_from_pinned_closure`, `test_managed_render_preserves_asset_identity_from_the_pinned_asset_scope`, and `test_publication_and_historical_render_reject_uncovered_child_atomically`: migrate the publisher setup to commit/fixture input. The durable surviving behavior is pinned closure/materialization and strict render admission; save-time scene evaluation remains cut per the plan and belongs to Viewing’s advisory seam tests.
- `tests/test_runtime_p1_blockers.py::test_project_updates_require_idempotency_keys_at_service_boundary`: setup currently creates retired shot/reference rows. Replace setup with a command/captured resource and preserve the decorator’s missing/oversized-key validation ordering if still part of the Runtime boundary contract.

## Generic reserved Document calls

Canonical `timeline:*` / `timeline.composition` writes are retired. The positive consumers are the `create_timeline_document` setup in `test_timeline_clip_replacement.py`, `test_timeline_render_publication.py`, and `test_timeline_cutover.py`, plus `test_timeline_clip_replacement.py::test_replace_timeline_clip_replays_after_intervening_edit_and_reopen` at `:191`. Migrate those setups/edits with command fixtures.

Do **not** classify ordinary source/config/transcript documents as retired canonical writers: `tests/test_preferences.py`, `tests/test_transcript_documents.py`, `tests/test_timeline_commit_inputs.py`, `tests/test_timeline_commit_acceptance.py`, `tests/test_timeline_commit_port.py`, `tests/test_timeline_commit_restore_port.py`, `tests/test_timeline_reads_after_cut.py::test_precut_catalog_reference_shot_and_binding_pins_survive_source_change`, and `tests/test_timeline_legacy_authority.py::test_http_actual_create_command_restore_rename_and_ordinary_artifact_metadata` intentionally exercise supported mutable source documents or read-side pinning.

## Task effects

- Canonical edit effects are already rejected and zero-write covered by the parametrized families in `tests/test_timeline_effect_authority.py`: admission, direct store admission, unknown effects, forbidden replay/new-key behavior, final/delegated policy, existing-attempt settlement, and store dispatch before callbacks. No replacement writer is implied by these tests.
- `tests/test_task_admission_replay_identity.py::test_changed_snapshot_and_identity_refuse_before_any_store_publication` uses `timeline.update` only as a changed replay input; it must remain a no-write identity-conflict test, not become a positive effect test.
- `project.update` effects in `tests/test_runtime_reboot.py`, `tests/test_runtime_control2.py`, `tests/test_runtime_e2e.py`, and `tests/test_render_admission_exact_retry.py` are outside the forbidden canonical timeline/shot/reference/text-binding set and are not retirement findings.

## Authority proofs already covering the closed surface

Do not migrate or weaken the qualified rejection suites: `tests/test_timeline_legacy_authority.py`, `tests/test_timeline_shot_authority.py`, `tests/test_timeline_reference_authority.py`, `tests/test_timeline_document_authority.py`, `tests/test_timeline_render_authority.py`, `tests/test_timeline_commit_port.py::test_tracked_legacy_publication_rejected_before_writes`, `tests/test_timeline_cutover.py::test_public_timeline_document_routes_are_retired`, and the canonical-effect families above. `tests/test_precut_variants.py::test_canonical_documents_have_genuine_create_receipts_and_refuse_bypass` is also a refusal/receipt-integrity proof, not a positive document writer.

## Next three smallest preservation patches

1. **Text bindings (4 tests):** port `tests/test_shot_text_bindings.py` to a `shot.text_binding.*` command fixture. Dependency: Agent binding schema/capture and Runtime immutable managed-text selection; App later converts producer calls.
2. **Revision-pinned render publication (3 tests):** replace `tests/test_timeline_render_publication.py`’s old publisher with `rendering.render` admission/settlement. Dependency: Agent/Viewing revision-pinned snapshot and retry contract; Runtime supplies fence/idempotency only.
3. **Candidate promotion (2 tests):** port `tests/test_shot_candidate_promotion.py` to canonical shot ownership. Dependency: Agent item/promotion command semantics, Runtime exact media pins and guarded child/occurrence invalidation; App popup producers consume it later.

The next larger patch is `tests/test_timeline_clip_replacement.py` (9 tests), whose media selection and intervening-edit guards should be implemented before removing its fixture dependence. None of these recommendations deletes assertions or converts supported behavior to blanket 410/xfail.

## Evidence and limits

Command run: `python -m pytest --collect-only -q` over the selected Runtime files covering the families above. Result: **724/748 tests collected, 24 deselected**, with only the existing unknown `timeout` config warning. No test bodies, full suite, localhost/browser suite, or mass execution was run. The current focused 1122/42 proof counts therefore do not establish whole-suite green.
