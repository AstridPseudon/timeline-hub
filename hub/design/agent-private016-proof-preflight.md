# Agent private016 paired-proof preflight

Status: **source/report preflight prepared; artifact tuple pending**.

This is the sole approved private line: Agent commit `10226a7f08a739ba3e41f8e91de6971eed63aa9d`, tree `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`, raw schema SHA-256 `9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`, canonical schema SHA-256 `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`, 65 definitions / 37 closed clauses. The immediately preceding raw-OLD floor is reconstructed as raw `9e4b4421…`, canonical `d3274d7…`, 64 definitions / 36 clauses. Private015/C3d/3e6c is superseded and receives no further execution.

The requested `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/luna/reports/` source directory was not present in this environment. This preflight therefore uses the available ORCH/design reports, frozen Agent source/tests, and the referenced historical worker reports. No new run was made to fill that provenance gap.

## Non-negotiable execution boundary

This document is source/reports-only. Do not generate, pin, install, build, invoke native/renderer paths, or run an outer/HTTP pair until the artifact tuple and both independent source reviews are complete. Do not replay historical runs. Reuse the exact fixtures and existing passes below; do not create a new matrix or new tests.

The public014/ordinary line remains out of scope. Its ordinary floor is `6ba7b51e…` (55 definitions / 29 clauses); it must not receive the private 65/37 schema, raw reference, raw-OLD successor, transcript successor, grouped-track, or free-multi behavior. Keep the current public refusal boundary, including the retired direct-reference route (`410 timeline_commit_required`) and the public RT08 typed-item-reference refusal. No public release, consumer pin, integration adoption, or activation is authorized.

## Four required Runtime source counterparts

The Runtime counterpart must be based on current Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree `6abc2f117391de8e7e35c0283f575a002199894d`, and must preserve its current retry/source/transcript guards. The plan identifies these four source counterparts; none is an accepted generated 0.2.16 artifact yet.

| counterpart | frozen source to reuse | required current-base work | preflight status |
| --- | --- | --- | --- |
| RT08 materialization | Runtime `83a982eb1185477e50817e10b8c61212c43c8e03`, tree `becc776a4f0c88ae2f4c8ba9350116a040d223c7` | Port `runtime_protocol/timeline_materialization.py` and only the minimal port/store validation/invocation hunks. Preserve `PROJECT_PACK_KIND` and `TRANSCRIPT_KIND`; the old source removed the latter and must not be copied wholesale. The read-only join must cover project/timeline, content digest, shot/internal/item membership, parent/source pins, bindings, source owner/provenance, inverse support, and `materialization.source:` / `materialization.owner:` edges. | Source exists; current-base port, independent review, generated tuple, and matched proof are missing. |
| RT03 raw capture | Runtime `f53bf588…`, tree `d82f…`; source tests `tests/test_timeline_raw_capture.py` | Carry the exact `MediaManifestEntry {media_id, content_digest}` contract, managed-project ownership, one CAS descriptor, regular identity/size/full-SHA/stable-descriptor checks, declaration and acceptance revalidation, ledger-first replay, and no-write refusal. | Reviewed source exists; current-base counterpart and paired normal proof are missing. |
| RT03 reference projection | Runtime `449d13d…`, tree `47d5f06…` | Add the exact reference projection source/store hook. Keep role `source`, equal digest, one manifest entry, global active/archived occupancy, previous-carrier/live-row ownership, transactionally coupled closure/publication/head/version, and ledger-first retry. No catalog or placement writer. | Reviewed source exists; current-base counterpart and paired normal proof are missing. |
| generator | Reviewed private generator support for `generators/agent-command-source.json`, `validate_command_schema(source_path)`, source-pin validation, and dynamic Python `*Args` package-root exports | Current b92 generator needs guarded `--agent-command-schema` support. It must reject malformed/unpinned input, preserve ordinary-schema byte identity, include new top-level `*Args` such as `TranscriptAssociateArgs`, and exclude `*Variant`. It must be reviewed before any invocation. | Source-support report exists; exact committed generated-support tuple and independent reciprocal review are missing. |

The future counterpart must retain the current b92 source anchors and not introduce a new DTO, endpoint, store authority, wire authority, or public route. Historical artifact/client/lock bytes are evidence only, not the pending 0.2.16 tuple.

## Existing proof inventory

### 1. Original owned-raw, unplaced reference

Source branch: frozen private016 `tl/agt-m2-private016-paired-proof-preflight` at `10226a7f…`; the reviewed predecessor source is held on `tl/agt-m2-review-owned-raw-reference-source` at `d1f5f782…`.

Agent source and exact existing nodes:

- `tests/editing_conformance/test_recipe_m2_parent_reference.py::test_empty_parent_raw_reference_is_unplaced_and_round_trips_exactly`
- `tests/editing_conformance/test_recipe_m2_parent_reference.py::test_raw_reference_replays_in_order_and_inverse_redo_preserves_order`
- `tests/editing_conformance/test_recipe_m2_parent_reference.py::test_raw_reference_requires_exact_verified_owned_media` (parameterized: missing verified media, missing metadata, wrong object id; atomic unchanged)
- `tests/editing_conformance/test_recipe_m2_parent_reference.py::test_raw_reference_does_not_overwrite_an_occupied_stable_identity`
- `tests/editing_conformance/test_recipe_m2_parent_reference.py::test_raw_reference_does_not_alias_an_ordinary_asset_with_the_same_user_id`

These use the existing empty-parent bundle and explicit fake `MEDIA`/`VERIFIED` fixtures. They witness the original owned-raw/unplaced shape and local refusal/atomicity, but the fake boundary is not Runtime custody. The original source review is Agent `d1f5f7824a5ede5587088735fad6e6870f0b95db`, tree `ca825c4bf900400487f9a1ca6b8c1651d63d5a68`; Runtime raw source is `f53bf588…`/`d82f…`.

Runtime historical exact controls and planned proof nodes are already identified:

- positive accepted opaque raw reference with role `source`, exact reference/object identity, zero placement/shot/occurrence/clip writes;
- missing, unowned, and foreign raw refusal before writes;
- restart retry returning the same receipt/bytes from the ledger without provider/raw reread;
- changed payload under the same key returning visible 409 without writes;
- a different key attempting an occupied identity returning 409 without writes;
- retained retired-route 410 controls.

The historical direct Runtime positive is `tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting` (old strict-xfail source, lines 81–124), with refusal controls in `tests/test_timeline_reference_authority.py:151-213`. The direct RT03 retry witness is `f53:tests/test_timeline_raw_capture.py::test_exact_retry_after_restart_replays_ledger_before_raw_capture`.

**Missing:** one normal current Agent/Runtime paired proof for all seven nodes above, with real Runtime custody, normal `/v1` authority, exact private 65/37 command pin, and no-zero collection evidence. The old positive/strict-xfail evidence must remain an expected failure until nodes 1–7 are genuinely available; do not rewrite it as a refusal.

### 2. Raw-OLD swap positive and controls

Source branch: `tl/agt-m2-raw-old-swap-closed-successor` at `9b9baa01…`; the current private016 consumer is the frozen `tl/agt-m2-private016-paired-proof-preflight` line.

Existing Agent source/test witness:

- source review commit `9b9baa01…`, tree `f924720…`;
- `tests/editing_conformance/test_raw_old_swap_successor.py::test_new_versions_are_unoccupied_and_raw_old_is_exactly_two_fields`;
- parametrized `::test_raw_old_swap_preserves_original_scope_and_replays` for `owner=parent` and `owner=occurrence`;
- `::test_raw_old_swap_keeps_aba_and_new_alias_guards`;
- `::test_provider_without_optional_raw_reader_fails_closed_before_writes`;
- neighboring existing fixtures/tests in `test_recipe_parent_media.py` and `test_recipe_occurrence_media.py`.

The module carries `pytestmark = pytest.mark.usefixtures(runtime_abi.__name__)`; retain this runtime-ABI guard. Existing source evidence reports 158 focused passes (including schema/conformance/diff checks), and the Runtime raw-OLD source review reports 69 exact focused passes. These are historical source evidence, not current paired qualification.

The raw-OLD tuple is the 64/36 raw `9e4b4421…` / canonical `d3274d7…` floor before the approved transcript successor; current private016 is 65/37 and must remain the only active line.

**Missing:** generated private016 Runtime counterpart and one matched normal pair proving parent and occurrence positive swaps plus occupied/new-alias, ABA, optional-reader, unowned/foreign, restart/retry, and inverse controls. Do not infer current Runtime acceptance from the historical raw-OLD source ACK.

### 3. Original grouped-track and free-multi recipes

Reuse the existing source fixtures and permanent nodes:

- group fixtures: `tests/editing_conformance/fixtures/recipe_m2_group_move.json` (hash `488b7f…`) and `recipe_m2_group_migration.json`;
- group nodes: `tests/editing_conformance/test_recipe_m2_group_migration.py`, `test_recipe_m2_group_move.py`, `test_current_group_slice.py`, and `test_group_read_view.py`;
- free-multi fixture: `tests/editing_conformance/fixtures/recipe_m2_free_move_set.json`;
- exact free-multi node: `tests/editing_conformance/test_recipe_free_move_set.py::test_exact_app_drag_golden_selection_order_and_created_track_are_one_unit`;
- exact free-multi output: one transaction, `track.create(V3)` followed by `clip.move-set`, V1/V2/V3, clip-1 on V2 at 1, clip-2 on V3 at 3, hold2, no pinned group, selection `[clip-2, clip-1]`.

The reviewed group source is branch `tl/agt-m2-group-full-carrier-source-compose`, commit `c0644cf1a7b63c9bcff7f70502b953a07879c9f3`, tree `0699f877a4c809005536a80f5956b8051a814ef7`, schema 58/32, with only `timeline.migrate-groups` and `occurrence.move`. The free-multi corrected source is branch `tl/agt-review-free-multi-corrected-current`, commit `a19192ea789a209260da46bfbdd5b616fc7cc4ac`, based on `922317bd…`, schema `ba0c42…`, 60/34. These are source candidates, not the private016 frozen artifact tuple.

The original App success expectations are already present and must remain intact as `it.fails` at `src/tools/video-editor/hooks/useClipDrag.test.tsx` lines 774, 1120, and 1230: free-multi created-track ordering, pinned-group existing-lane movement, and pinned-group move onto V3. Preserve these expectations until a real matched implementation exists. Current frozen Agent 10226 contains the free-multi and group fixture/test files, but does not contain the separate `test_recipe_m2_group_new_parent_track.py` held by the staged group source review; do not invent a replacement test.

**Missing:** a single generated private016 tuple that includes the approved grouped/free-multi source, independent Runtime materialization/ownership review, normal paired Runtime proof for group migration/move and free-multi/new-track semantics, and the corresponding App acceptance/native proof. The historical group source passes (170) and free-multi focused/full source passes (38 / 138) are not Runtime or App qualification.

### 4. Transcript nested V1/V2 accepted closure

Source branch: frozen private016 `tl/agt-m2-private016-paired-proof-preflight` (also held as `tl/agt-m2-complete-union-final-eof-handoff`) at `10226a7f…`; the reviewed Runtime source is `3dcae183…`/`4fa58…`.

The frozen Agent source is the approved transcript successor in the 10226/e2c08 line. Reuse these exact nodes:

- `tests/editing_conformance/test_recipe_film_transcript_association.py::test_association_records_source_planes_and_roundtrips_canonically`;
- `::test_association_uses_guarded_inverse_and_replay`;
- `::test_replacement_requires_and_retains_exact_prior_pin`;
- `::test_serialized_replacement_inverse_restores_source_item_order`;
- `::test_association_reconciles_real_caption_and_review_leaves_without_asset_on_caption`;
- `::test_association_refuses_caption_destination_collision_atomically`;
- `::test_association_refuses_shared_review_ownership_atomically`;
- `::test_normal_serialization_reload_preserves_nested_carrier_through_inverse_and_redo`;
- `::test_rejected_parent_level_prototype_never_becomes_a_second_carrier`;
- `::test_missing_persisted_bundle_is_created_as_nested_recorded_container`;
- accepted-history witness `tests/editing_conformance/test_gate1_transcript_accepted_reload.py:56-208`.

The accepted-history witness checks nested V1/V2 carrier state, exact new/prior pins, inverse/restart/redo behavior, and accepted closure. The carrier is only `parent.config.bundle.transcriptReferences` with `itemsBySchemaRef["astrid.transcript_segment/v1"]`; legacy parent/root spellings refuse. Runtime source `3dcae183…`, tree `4fa58…`, retains V1 after V2 update/live-row removal/restart and preserves exact new/prior pins. Existing Runtime controls are `tests/test_timeline_source_document_boundary.py`, `tests/test_timeline_pack_document_read.py`, and `tests/test_timeline_commit_inputs.py`.

Historical Agent transcript/schema/conformance evidence is 186 passes plus a 13-test focused lane; the accepted reload/source review reports 11 focused passes, and the corrected App dormant source reports one exact data-provider and one exact persistence hook test. All are direct-service, dormant, or source-level evidence; none is normal daemon `/v1` acceptance.

**Missing:** normal `/v1` paired accepted-closure proof that publishes V1, replaces with V2, removes the live row, reloads/restarts, and verifies nested V1/V2 closure, exact prior/new pins, inverse, and redo through the real Runtime/App boundary. Do not promote the direct-service accepted-history witness to native qualification.

## Historical commands and results (source evidence only)

These commands/results are copied from the available reviews and were not replayed for this preflight:

- Parent-reference/schema floor: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-f53bf588" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --timeout=60 tests/editing_conformance/test_recipe_m2_parent_reference.py tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py` — 67 passed in 175.22s.
- Raw-OLD/schema lane: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_raw_old_swap_successor.py tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py` — 69 passed in 160.23s.
- Group source lane: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py tests/editing_conformance/test_pristine_initialize.py tests/editing_conformance/test_current_group_slice.py tests/editing_conformance/test_group_read_view.py tests/editing_conformance/test_recipe_m2_group_migration.py tests/editing_conformance/test_recipe_m2_group_move.py` — 170 passed in 151.88s.
- Free-multi/timing lane: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_free_move_set.py tests/sdk/test_timing_compiler.py` — 138 passed in 12.97s.
- Transcript/schema/source lane: `pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_film_transcript_association.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_grouped_clip_cache_inverse.py tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py` — 186 passed in 215.51s; the focused transcript lane reported 13 passed in 2.66s.

## Environment, fixture, and collection guards

When execution is eventually authorized, use the immutable source/archive paths named by the paired review and the shared dependency policy. Agent historical commands used `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH` pointing at the Agent source plus the matched Runtime archive, and `/home/user/work/venv-agent/bin/python`; Runtime uses its dedicated `/home/user/work/venv-runtime/bin/python`. No shared venv, node_modules, runtime, or cache may be modified. Native/HTTP/App runs belong to the central test service, one full suite at a time; this preflight does not request one.

Every selected command must assert that its exact nodes were collected and run: fail the orchestration if pytest/Vitest reports `0 collected`, `0 passed`, or only deselected tests. Keep the raw-OLD `runtime_abi` fixture marker, the RT03 strict xfail marker, and the three App `it.fails` expectations. Do not use a broad `-k` expression that can silently select nothing, blanket-deselect, skip, weaken, or delete a behavior test. A strict xfail/`it.fails` may be flipped only after the corresponding paired behavior is actually demonstrated.

## Bounded missing-prerequisite list

1. Publish the exact normally generated Runtime private016 artifact tuple: version, commit/tree, raw/canonical schema digests, generated client/package bytes, lock/manifest bytes, and artifact-manifest digests. It must be derived from current Runtime b92 plus the four counterparts above, not from superseded private015.
2. Complete independent Runtime review of the joined b92-based source and exact Agent 10226/e2c08/raw9cb9/canonical3227 pins; verify no new authority, route, catalog, placement writer, or transcript-kind regression.
3. Complete independent Agent review of the generated private016 Runtime artifacts and reciprocal tuple comparison before any pin/native/outer action.
4. Run exactly one matched normal Agent/Runtime proof for raw owned/unplaced reference and all listed refusal/restart/retry/inverse/occupancy controls; preserve zero-placement evidence.
5. Run exactly one matched normal raw-OLD parent and occurrence proof with its existing controls and no public/private015 fallback.
6. Qualify the existing grouped-track/free-multi recipes against the generated private tuple, including group migration/move, free-multi created-track ordering, and the held new-parent-track source where required; then qualify the three existing App success expectations.
7. Qualify nested transcript V1/V2 accepted closure over normal `/v1`, including publish/replacement/reload/restart/inverse/redo and exact pin preservation.
8. Record the public014 refusal/boundary checks and confirm no public route, public schema, consumer pin, or release was changed.
9. Keep private015/C3d/3e6c explicitly superseded with no further generation, pinning, native, or outer execution.
10. Resolve the absent `scratchpad/luna/reports` provenance path or explicitly carry this report’s provenance limitation into the independent reviews.

Until items 1–3 and reciprocal review are complete, the remaining items are prerequisites only. Artifact tuple remains pending.

## Evidence boundary for this preflight

No tests, generators, installers, package builds, source copies, artifact mutations, pinning, native execution, renderer execution, HTTP/outer run, or public activation were performed in this task. The pass counts and commands referenced above are historical evidence from the source/review reports and must not be reported as current paired qualification.
