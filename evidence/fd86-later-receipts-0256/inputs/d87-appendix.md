# Appendix: F-D87 native-batch retirement mapping

Status: source-only evidence for manager publication. The manager-owned
`design/deletion-ledger.agent.md` is unchanged and remains the sole publisher.

Retained input: the D85 550 rollup/source manifest at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-native-cli-sol-2350/evidence/source-manifest.json`
and its retained `tests/editing_conformance/test_native_batch_ingress.py`
selector list. Current integration HEAD is `0d142f7951`; the retained b9f
branch remains unmerged.

## Settled scope

This appendix applies the explicit ORCH 00:03:56 decision on the current
normal integration base, not held b9f. There is no native batch envelope and
no resurrected G5 interface. The retained D85 source manifest has exactly 24
parameterized native-batch records. All 24 are mapped below to current,
assertion-bearing behavior tests. The separate protected checkout parameter
case is row 25; it is not a broader retirement. The other six checkout cases
remain live. No native-batch runtime or helper fixture is deleted.

Every row carries the required decision references: D87/G5/D52/D72(1).
Retired packet fidelity (arbitrary captured native commands, native claims,
native rationale, or `source.via=cli`) is not a current promise after this
decision and is called out where relevant; it is not counted as an uncovered
current capability.

## Exact retained IDs and current assertion mapping

| # | Canonical retained ID (exact source node) | Decision | Current test and real assertion covering the promised behavior |
|---:|---|---|---|
| 1 | `tests/editing_conformance/test_native_batch_ingress.py::test_batch_original_claims_one_publication_reload_inverse[cli-False]` | D87/G5/D52/D72(1) | `tests/packs/timeline/test_cli_document_commit.py::test_document_commit_uses_the_authenticated_commit_door` (81-90) asserts accepted status, label, receipt key, reads, and no publication file; `test_document_commit_human_output_keeps_label_and_receipt` (185-190) asserts terminal accepted-revision/label/receipt output; `tests/packs/timeline/test_cli_commit_move.py::test_cli_accepted_redo_inverts_undo_publication_and_preserves_disjoint_edit` (227-234) asserts accepted inverse and restored state. |
| 2 | `tests/editing_conformance/test_native_batch_ingress.py::test_batch_original_claims_one_publication_reload_inverse[cli-True]` | D87/G5/D52/D72(1) | The current commit-door acceptance assertions (81-90), `tests/packs/timeline/test_cli_document_commit.py::test_document_commit_human_output_keeps_label_and_receipt` terminal assertions (185-190), and native edit inverse assertions (227-234) cover the promised current behavior; the retired native claim envelope itself is not promised. |
| 3 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[disjoint-False]` | D87/G5/D52/D72(1) | `tests/packs/timeline/test_cli_document_commit.py::test_document_commit_retry_uses_runtime_idempotency_without_history_scan` (103-110) asserts byte-equivalent replay, one send, and the same key twice; `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[False]` (134-150) asserts the durable flight is replayed exactly before the suffix is sent. |
| 4 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[disjoint-True]` | D87/G5/D52/D72(1) | The current `commit --file` exact-key replay assertions (103-110) plus the native move/trim restart assertions (134-150) cover durable retry and subsequent suffix ordering; native envelope claims are retired. |
| 5 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[relevant-False]` | D87/G5/D52/D72(1) | `test_document_commit_retry_uses_runtime_idempotency_without_history_scan` (103-110) asserts one accepted write with two identical requests; `test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[False]` (134-150) asserts exact flight replay and suffix acceptance. |
| 6 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[relevant-True]` | D87/G5/D52/D72(1) | `test_document_commit_retry_uses_runtime_idempotency_without_history_scan` (103-110) asserts exact retry; `test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[True]` (134-147) asserts the relevant peer change returns `CommitConflict` and leaves the suffix pending. |
| 7 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[aba-False]` | D87/G5/D52/D72(1) | `test_document_commit_retry_uses_runtime_idempotency_without_history_scan` (103-110) asserts same-key replay without a second write; `tests/packs/timeline/test_cli_native_sheet.py::test_lost_ack_immutable_retry_and_pending_export_refusal` (193-200) asserts retry without fetching or recapturing and exactly one accepted result. |
| 8 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[aba-True]` | D87/G5/D52/D72(1) | `test_document_commit_changed_body_with_same_key_is_runtime_refusal` (203-211) asserts same-key mutation is refused with `idempotency_conflict` and no second write; `test_stale_export_refuses_without_recapturing[True]` (162-168) asserts the relevant basis refusal preserves both files and makes no call. |
| 9 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[delete-recreate-False]` | D87/G5/D52/D72(1) | `test_document_commit_retry_uses_runtime_idempotency_without_history_scan` (103-110) asserts durable exact replay; `test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[False]` (134-150) asserts the original flight and new suffix are separate writes. |
| 10 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[delete-recreate-True]` | D87/G5/D52/D72(1) | `test_document_commit_changed_body_with_same_key_is_runtime_refusal` (203-211) asserts changed request bytes cannot reuse the key; `test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[True]` (134-147) asserts the peer conflict leaves the suffix intact. |
| 11 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[disjoint-False]` | D87/G5/D52/D72(1) | `test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[False]` (148-153) asserts the disjoint suffix is accepted and both authored edits remain; `test_document_commit_refuses_a_stale_base_pair` (251-262) asserts the file route does not silently write from a stale pair. |
| 12 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[disjoint-True]` | D87/G5/D52/D72(1) | `test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[False]` (148-153) asserts accepted suffix state; `test_document_commit_refuses_a_stale_base_pair` (251-262) asserts stale base is refused with no new history entry. |
| 13 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[relevant-False]` | D87/G5/D52/D72(1) | `test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[True]` (142-147) asserts `CommitConflict`, pending suffix, and unchanged authored values; `test_document_commit_refuses_a_stale_base_pair` (258-262) asserts no write on stale basis. |
| 14 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[relevant-True]` | D87/G5/D52/D72(1) | `test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[True]` (142-147) asserts the relevant CAS conflict and preserved suffix; `test_document_commit_refuses_a_stale_base_pair` (258-262) asserts the current file route leaves history unchanged. |
| 15 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_refusal_is_atomic_and_keeps_file[claims]` | D87/G5/D52/D72(1) | `test_document_commit_changed_body_with_same_key_is_runtime_refusal` (203-211) asserts the current idempotency refusal code and no additional accepted write; `test_stale_export_refuses_without_recapturing[True]` (162-168) asserts current stale-basis refusal keeps the edited file and outbox unchanged. Native claims bytes are retired. |
| 16 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_refusal_is_atomic_and_keeps_file[late-invalid]` | D87/G5/D52/D72(1) | `tests/packs/timeline/test_cli_native_sheet.py::test_unsupported_edits_leave_text_and_outbox_intact` (208-217) asserts the unsupported edit is refused, makes no call, and preserves the edited text/outbox. |
| 17 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_refusal_is_atomic_and_keeps_file[media]` | D87/G5/D52/D72(1) | `test_unsupported_edits_leave_text_and_outbox_intact` (208-217) asserts current sheet refusal is atomic with no call and unchanged bytes; the retired native media packet is not a current writer. |
| 18 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_refusal_is_atomic_and_keeps_file[empty]` | D87/G5/D52/D72(1) | `tests/packs/timeline/test_cli_document_commit.py::test_document_commit_clean_raw_empty_app_is_a_noop` (144-155) asserts `unchanged`, null receipt, no send, and no history mutation. |
| 19 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_refusal_is_atomic_and_keeps_file[envelope]` | D87/G5/D52/D72(1) | `test_document_commit_refuses_a_stale_base_pair` (251-262) asserts current file validation returns an error at `/file` with no new entry; the retired native envelope format has no current acceptance promise. |
| 20 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_parser_requires_both_original_pins_and_describes_registry` | D87/G5/D52/D72(1) | `tests/packs/timeline/test_cli_document_commit.py::test_document_commit_uses_the_authenticated_commit_door` (81-90) asserts the current parser reaches the authenticated Runtime door with base/reads and receipt; `test_document_commit_refuses_a_stale_base_pair` (258-262) asserts missing/invalid current basis does not write. |
| 21 | `tests/editing_conformance/test_native_batch_ingress.py::test_captured_file_retry_refuses_boolean_to_number_claim[reads]` | D87/G5/D52/D72(1) | `tests/packs/timeline/test_cli_native_sheet.py::test_original_identity_never_coerces_boolean_to_number[pending]` (273-291) asserts the current sheet route refuses boolean/number identity drift with no call and unchanged outbox; `test_document_commit_changed_body_with_same_key_is_runtime_refusal` (203-211) asserts durable same-key body mismatch refusal. |
| 22 | `tests/editing_conformance/test_native_batch_ingress.py::test_captured_file_retry_refuses_boolean_to_number_claim[expect]` | D87/G5/D52/D72(1) | `test_original_identity_never_coerces_boolean_to_number[bundle]` (273-291) asserts bundle identity drift is refused without coercion or a write; `test_document_commit_changed_body_with_same_key_is_runtime_refusal` (203-211) asserts the current durable idempotency refusal. |
| 23 | `tests/editing_conformance/test_native_batch_ingress.py::test_file_preview_keeps_batch_for_one_real_publication` | D87/G5/D52/D72(1) | `tests/packs/timeline/test_cli_document_commit.py::test_document_commit_preview_has_no_accepted_receipt` (222-230) asserts preview status/would-status, null receipt, no history mutation, dry-run request, and unchanged file. |
| 24 | `tests/editing_conformance/test_native_batch_ingress.py::test_batch_capture_never_refreshes_after_concurrent_ack` | D87/G5/D52/D72(1) | `tests/packs/timeline/test_cli_document_commit.py::test_document_commit_retry_does_not_scan_a_long_history_page` (124-130) asserts exact-key replay without a long history scan; `tests/packs/timeline/test_cli_native_sheet.py::test_lost_ack_immutable_retry_and_pending_export_refusal` (193-200) asserts retry without fetching a bundle or recapturing intent. |
| 25 (separate) | `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_attached_param_commands_keep_exact_cli_ingress_and_unchanged_write_history` | D87/G5/D52/D72(1) | `tests/packs/timeline/test_cli_native_sheet.py::test_cli_trim_clear_and_params_are_one_captured_batch` (333-354) asserts one current sheet request contains trim/set/set-params, pins the original base, accepts once, and restores through undo; `tests/packs/timeline/test_cli_document_commit.py::test_document_commit_uses_the_authenticated_commit_door` (81-90) asserts current `commit --file` reaches the authenticated door. This is the one separately mapped checkout case; the original commands-file assertion remains live and is not rewritten. |

## Counts and gap decision

- Exact retained D85 native-batch records: **24**.
- Exact retained records mapped to current assertion-bearing tests: **24/24**.
- Additional checkout parameter case mapped separately: **1**.
- Current promised capability gaps: **0**. No new targeted test was needed.
- Checkout cases left live: **6**; no broader retirement was inferred.
- Product/test/helper deletions or edits: **0**.
- Native packet-envelope claims/rationale/source fidelity: retired interface behavior,
  intentionally not counted as a current capability gap.

## ZIP migration note — exact Runtime handback text

The following bytes are for handback to the Runtime ZIP README owner. The
Runtime-owned README is not edited by Agent.

```text
### Timeline write-route migration

The delivery retires the native `edit commands-file`/native-batch ingress and
the other separate native/publish writers (`edit --native`, `apply --native`,
`undo --publication`, `publish`, `publish_bundle`, and the old three-way
writer). A document edit now uses `timelines commit --file ... --message ...
--idempotency-key ...`; the Runtime `commitTimeline` door owns accepted,
merged, conflict, and invalid replies, durable exact-key retry, and the
receipt/history. A single move or trim uses the current native `timelines edit
...` route. Cut-sheet edits use the current `timelines apply <sheet> ...` /
`NativeSheet` route, which emits registered commands through that same Runtime
door and preserves the draft on refusal. No native packet envelope,
commands-file alias, detached document overwrite, or resurrected G5 interface
is included.
```

