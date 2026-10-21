# Runtime WC8 retained-basis boundary

Date: 2026-10-21  
Result: bounded Runtime ACK; no Runtime mismatch found in the existing
retained-command acceptance seam.

## Reviewed trees and source

- Runtime worktree: `/home/user/work/wt/rt-m2-wc8-runtime-boundary-0439-r1`
- Runtime tree: `b92d3e7a05eec65c142294ef4873edd059e9b31d` (`b92d3e7`), the
  expected Runtime `tl/integration` base.
- Agent context: exact read-only tree
  `5a625dd4c01149a085a9df85952b34cad70801f9`.
- Runtime handoff: `design/handoff-agent-to-runtime-wc8.md` from the shared
  orchestrator design directory.

The existing Runtime seam is sufficient for a future retained native batch:

- `runtime_protocol/timeline_commit_port.py:452-487` requires the prepared
  candidate head to have been observed through the port, preserves identity
  pairs, and keeps restore source pins exact.
- `runtime_protocol/timeline_commit_store.py:555-592` validates the canonical
  closure, document digest, recorder ordinals, identity map, dependencies and
  semantic events without normalizing the retained records.
- `runtime_protocol/timeline_commit_store.py:691-741` verifies the invocation
  and original base pair, refuses a changed expected head, performs the
  existing accepted-versus-rebased classification, and publishes the closure,
  recorder and events in one transaction.

## Gate 2 evidence

The four-file command in the handoff executed 180 tests; one test was
collected but intentionally deselected:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_commit_acceptance.py \
  tests/test_timeline_commit_execution.py \
  tests/test_timeline_commit_contract.py \
  tests/test_timeline_current_union_contract.py
```

Result: `180 passed, 1 deselected in 21.27s`.

The relevant existing tests are:

- Original recorder guards and retained intent: `tests/test_timeline_commit_acceptance.py::test_atomic_acceptance_exact_recorder_projection_and_same_content_edge`, `::test_complete_recorder_roundtrip_and_replay_after_restart`, and the parameterized `::test_valid_json_recorder_corruption_fails_every_durable_read_after_restart`.
- Exact base/publication guard and stale-head conflict without writes:
  `tests/test_timeline_commit_acceptance.py::test_changed_payload_and_publication_only_cas_refuse_without_writes`.
  The test changes the accepted payload under the same key, then attempts a
  stale expected head, and asserts the durable counts are unchanged.
- Atomic validation/no-write refusal: `tests/test_timeline_commit_acceptance.py::test_invalid_prepared_values_are_atomic[bad]` for each of `digest`, `manifest`, `ordinal`, `id_map`, `unknown_field`, `nonfinite`, `event`, and `base_pair`; plus `::test_failure_after_receipt_rolls_back_every_row` and the three parameterizations of `::test_failure_between_projection_steps_rolls_back_and_restart_retry_publishes_once`.
- Exact retry and restart durability:
  `tests/test_timeline_commit_acceptance.py::test_identical_retry_after_restart_and_head_advance` and
  `tests/test_timeline_commit_execution.py::test_durable_original_wins_while_changed_hash_is_active_before_lookup`.
- Changed-key refusal before provider work:
  `tests/test_timeline_commit_execution.py::test_active_hash_mismatch_does_no_provider_work`.
- Concurrent atomic head race:
  `tests/test_timeline_commit_execution.py::test_concurrent_different_keys_cas_one_winner`.
- Wire-level preservation of the exact request body and idempotency key:
  `tests/test_timeline_commit_contract.py::test_generated_python_commit_preserves_exact_envelope_and_retry[False]` and `[True]`.
- Closed command/recorder shape and target-key constraints:
  `tests/test_timeline_commit_contract.py::test_closed_request_rejects_unknown_missing_or_invalid_fields` and
  `tests/test_timeline_current_union_contract.py::test_recorder_target_key_patterns_are_retained`.

The store contains the existing positive rebase branch at
`timeline_commit_store.py:728-735`: when the prepared expected head has
advanced from the request base, the accepted result is marked `rebased` and
records `rebased_onto`; a mismatched head raises `StaleHead` before publish.
This run directly qualifies the refusal and atomicity sides. The four-file
Runtime lane does not contain a separate disjoint-edit positive asserting the
`rebased` result, so this report does not claim that additional scenario as
executed evidence.

## Detached-sheet boundary

The current detached caller remains:

`astrid/packs/timeline/cli.py:3607-3612` ->
`astrid/sdk/timeline_sheet.py:849-1085` ->
`astrid/sdk/timeline/checkout.py:151-169`.

It retains only a whole-document `v` digest and optional local `_exported`
snapshots before mutating a local Checkout through `apply_sheet` /
`merge_sheet` / `Checkout.save`. It does not retain a verified Runtime
publication pin, stable native row references, captured reads/selections/order,
or the original Runtime target and requester flight. Runtime therefore ACKs
the existing retained-command boundary only; the detached sheet is blocked on
Agent author-time retention.

Snapshot diffing cannot reconstruct row intent, selection membership/order,
explicit unchanged writes, or the original target. Refreshing guards at send
time would authorize the mutated current document rather than preserve the
author's basis. Neither is a migration path. The detached grammar, local
three-way/rollback behavior, draft visibility and native positives remain
preserved and held.

## Smallest Agent prerequisite

Before detached mutation, Agent must retain a bounded native command batch for
each supported detached edit containing:

1. the exact original revision/publication basis;
2. stable row references/identity plus recorded reads, selections and order;
3. the writes, including explicit clears and unchanged values; and
4. the original Runtime project/timeline target and exact request/idempotency
   flight for restart-safe retry.

Unsupported legacy or mixed rows must remain visibly held with the existing
grammar and local rollback. Once that seam is qualified, Runtime can consume
the retained batch through the existing `/v1` commit, server-side rebase,
exact guards, durable retry, history and inverse machinery. No new DTO,
endpoint, snapshot migration or Runtime writer is required by this boundary.

The Agent native floor was not rerun, as required. Its exact IDs remain:

- `tests/sdk/test_timeline_sheet_native.py::test_atomic_batch_commit_lost_ack_restart_and_undo`
- `tests/sdk/test_timeline_sheet_native.py::test_stale_original_guards_conflict_without_refreshing`
- `tests/sdk/test_timeline_sheet_native.py::test_disjoint_head_edit_rebases_without_writing_unchanged_cells`
- `tests/packs/timeline/test_cli_native_sheet.py::test_export_preview_apply_and_undo`
- `tests/packs/timeline/test_cli_native_sheet.py::test_lost_ack_immutable_retry_and_pending_export_refusal`
- `tests/packs/timeline/test_cli_native_sheet.py::test_stale_export_refuses_without_recapturing`

The missing dependency is the author-time retention seam above, not a Runtime
test or package.

