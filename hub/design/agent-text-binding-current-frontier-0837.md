# Agent text-binding current frontier — 2026-10-21 08:37 UTC

This is a documentation-only reconciliation of the Agent-owned contract and
ledger row against Runtime's final P1/P2 and O1–O7 response.

## Exact inputs

- Agent current tree: commit `a9f4cfdaee40f3382b51d6cdb291d7012be96b8c`, tree
  `93862f0accf8bbe2331ed551b69839b47f7b8e1b`.
- Runtime response source: commit `b92d3e7a05eec65c142294ef4873edd059e9b31d`,
  tree `6abc2f117391de8e7e35c0283f575a002199894d`.
- Reconciled docs: `design/m2-text-binding-contract.md` and the
  `AG-M2-TB01` row in `design/deletion-ledger.agent.md`.

## Settled contract

Runtime's response confirms the existing request-scoped `text_selection`
method and existing acceptance transaction. P1 is exact project-owned UTF-8
selection, including zero bytes, with acceptance recheck at
`runtime_protocol/timeline_commit_port.py:276-283,387-403,584-629`. P2 is the
server-derived before/after live projection and append-only event at
`runtime_protocol/timeline_commit_store.py:712-832`.

The Agent contract records the settled O1–O5 boundaries:

- New authored rows contain only binding identity and immutable descriptor;
  Runtime projection fields stay derived. Old pinned rows remain compatibility
  data (`astrid/sdk/timeline/native_text_binding.py:9-12,64-67`).
- New input uses `text/plain; charset=utf-8`; retained authenticated
  descriptors may use legacy `text/plain`.
- The v1 selector is `occurrence:<id>`, and the command is fail-closed outside
  exclusive occurrence ownership (`native_text_binding.py:36-45`).
- Recorded collection membership/order is authoritative; no Runtime sort or
  order field is introduced (`native_text_binding.py:45-67`,
  `_command_state.py:367-388`).
- Shared ownership is not qualified and does not close the ledger.

## Only remaining native/consumer evidence

1. Qualify the exact matched public Agent/Runtime tuple, including the current
   generated artifact/version and coordinated pins. The existing tests naming
   the required behavior are:

   - `tests/editing_conformance/test_commit_runtime_text_binding.py::test_runtime_declares_and_captures_exact_text_port`
   - `::test_text_input_is_reverified_at_atomic_acceptance`
   - `::test_first_use_capture_projects_exact_text_and_retry`
   - `::test_clear_removes_row_and_undo_restores_empty_exactly`
   - `::test_disjoint_first_birth_rebase_keeps_captured_intent_and_actual_order`
   - `tests/editing_conformance/test_recipe_text_binding_native.py` (closed
     shape, empty/presence, exact inverse, order, exclusive-owner and rebase
     cases)
   - Runtime `tests/test_timeline_text_selection.py` and
     `tests/test_timeline_text_binding_clear.py` (selection, acceptance,
     projection, presence and clear custody).

   These references identify the remaining proof surface; this worker did not
   run them and no matched public qualification is claimed.

2. Keep the original retained-legacy positives open until that matched proof:

   - `tests/editing_conformance/test_commit_runtime_text_binding.py::test_rebind_existing_main_descriptor_undo_is_exact`
   - `::test_clear_existing_main_descriptor_and_inverse_are_exact`
   - Runtime original controls in `tests/test_shot_text_bindings.py`:
     `test_set_is_deterministic_project_scoped_and_replays`,
     `test_set_rebind_and_event_order`,
     `test_invalid_utf8_and_size_are_zero_write`, and
     `test_identity_digest_is_sha256`.

3. Keep Main compatibility inputs and consumers live/held under O6. The exact
   existing references are `tests/timeline/test_authoring_bundle.py:118` for
   the inline `{slot, text}` row, `tests/timeline/test_authoring_media.py:578-615`
   for the retained catalog text binding, and the legacy consumers at
   `astrid/sdk/remote.py:2347-2359`,
   `astrid/sdk/timeline/publish.py:201-224`, and
   `astrid/packs/rendering/docs/scripts/timeline_document.py:172-200`.

O6 therefore remains open for an explicit Agent-owned recorded migration that
preserves those positives and callers. O7 is a Runtime compatibility ACK, not
release, generation, artifact, pin, or consumer-cutover authorization. No new
DTO, endpoint, port, journal, schema, or generation design is proposed.

## Evidence and limits

No tests were run by this worker because only shared docs/handoff files were
changed. No native, HTTP, browser, renderer, install, full-suite, public pin,
or writer-retirement claim is made.
