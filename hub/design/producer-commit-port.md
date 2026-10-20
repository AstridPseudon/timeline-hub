# Producer attempt port and publication checkpoint

Design only, Runtime `9f9b25c`; PLAN 2026-10-20 and Runtime INBOX 00:35/00:40 govern.
Reconciled with settled completed-cancel, persisted-epoch and numeric-forwarding decisions; exact Agent schema/goldens and executable admitted head-pair builder source still need freeze (design placement ACK 00:54Z). Branch work may proceed; M2 integration merges await the orchestrator M1 record. D13/410 stays held until replacement behavior qualifies.
The REQUESTING App/CLI session consumes settled task output and commits through its existing authority/outbox. Workers receive no write scope.

## Additive request-scoped port (proposed exact shape)

```text
producer_attempt(pin: ProducerAttemptPin) -> VerifiedProducerAttempt
ProducerAttemptPin = {task_id:str, attempt_id:str, executor_id:str, fence:int,
  runtime_epoch:int, admitted_target:{project_id:str, timeline_id:str,
    base_revision_id:str, base_publication_id:str}, proposal_digest:Digest}
VerifiedProducerAttempt = {pin:ProducerAttemptPin}
AgentDependency = {key:"producer_attempt:"+task_id, kind:"authority",
  policy:"exact", pin:verified.pin}
```

DTO objects are closed, IDs nonempty, fence/epoch positive non-bool integers; Digest is `sha256:<64 lowercase hex>`.
This is an in-process port/typing addition, not a new HTTP DTO/CommitRequest field. Never record lease IDs/tokens.
Agent carrier: first `producer.guard` v1/select:null/args:{pin}, followed by EXACT proposal.commands; no extra edits/nested guard/inverse/restore. Agent owns registry/schema/goldens.
Proposal = {schema_version:1,producer:{task_id,attempt_id,executor_id,fence,runtime_epoch},admitted_target,commands,rationale,proposal_digest}; pin flattens producer plus target/digest.
Digest hashes ENTIRE proposal minus only proposal_digest: UTF-8 sorted compact JSON, ensure_ascii=False/allow_nan=False; order/null/presence/capture metadata preserved, no normalization. Reject duplicate keys/nonfinite/unpaired surrogates.
Port call uses `_read` authorization/mutex, returns detached JSON, and privately captures task/run/spec, attempt, settled output and admitted continuation.
Resolve unique `task.result.outputs` object descriptor name `authoring_proposal`, matching declared port from immutable spec/capability; require exact task/attempt/project managed association, durable available/promoted lifecycle, matching digest/size.
Read its Runtime CAS bytes, verify raw size/SHA against descriptor, parse strict JSON and recompute proposal_digest above (distinct from artifact byte digest). Recheck descriptor/association/bytes at accept; never caller paths/URLs/inline authority.
Guard args carry PIN ONLY; reject a forwarded proposal field. Recompute proposal_digest exactly from the authoritative immutable settled artifact under the hash profile above, never from caller-reserialized commands. Require exact derived pin == guard.args.pin. Compare request.commands[1:] and request rationale to artifact commands/rationale using recipe value equality: finite JSON numbers by value (1 == 1.0), booleans distinct from numbers, with object keys/presence/null and array order preserved. This comparison does not change the artifact hash scheme or omit any fields. Render intent derives from immutable admitted spec + caller approval.
Capture is read-only. No preparation checkpoint, task, CAS write or consumption occurs during capture/preview.

## Completed eligibility and errors

`service.settle_attempt:7479` validates live worker identity/fence/epoch and publishes outputs with `_settle_attempt:5202` atomically.
`store.py:5287-5292` stores result_json, sets task completed/attempt settled=1; retains attempt_id, executor_id, lease_fence and runtime_epoch.
`_task_resource:6716` exposes completed as succeeded and preserves result/output descriptors; managed associations bind task/attempt/project/output.
Generic host `_typed_outputs:7064`, `_upload_outputs:7716`, settlement near 9790 already supply artifact custody; the old publication hook must go.
Require task CURRENT attempt == pin.attempt_id, attempt.task_id == task.id, completed + settled=1, and exact executor/fence/epoch on both rows.
Require actual run project == request project == admitted target project; target timeline/base pair must equal immutable admitted spec and original request base.
Agent manager ACK 00:54Z settles the design placement at `spec.runtime_dependencies.publication.admitted_target`, alongside `publication.render`, containing the closed four-field admitted_target above. Agent still must freeze executable builder/schema/golden source for that placement: existing `build_stitch_admission` does not emit the pair, and legacy numeric expected_version cannot supply it. Missing/corrupt original admission pair refuses. Never relabel it to the requesting session's newer head or refresh captured commands/guards. Pending unrelated outbox flight finishes first. Original base remains pinned across ordinary server semantic rebase; prepared.expected_head may advance only under Agent's recorded guards, never recapture replacement intent.
Require the admitted ordered continuation/outputs and selected-media lifecycle bindings; retain the two-child assembler checks for this producer, not every command.
Reject queued/running/failed/cancel_requested/cancelled, missing result, superseded attempt (including retry's NULL current attempt), changed output/proposal or consumed task.
Do NOT call `_validate_attempt_lease:8464`: it rejects settled attempts. Lease expiry/live executor readiness is not completed-result authority.
Require epoch equality with persisted completed task+attempt, not current Runtime boot: restart only recovers running/cancel_requested (`store.py:1162`). This persisted-epoch behavior is orchestrator-approved.
Malformed pins: existing 422 validation_error. Scoped missing/unowned/foreign task/attempt/output/target: uniform 409 conflict/refused `producer_dependency_unavailable`, no foreign facts.
Well-scoped identity/state/digest mismatch: 409 conflict/refused `producer_attempt_mismatch`; consumed: `producer_proposal_consumed`; missing/mismatched capture/authority record: `producer_dependency_unavailable`.
Keep normal 401/403 authority errors, 409 idempotency_mismatch, 503 unknown-outcome reconciliation. No partial candidate/result on refusal.

## Acceptance and one-shot checkpoint

`TimelineCommitStore.accept:648`: current credential authorization, exact scoped ledger lookup, then all producer checks inside existing mutex/outer transaction BEFORE any write.
Extend `RequestCommitPort.validate:321`: bijection between declared producer pins, private captures and exact authority dependencies; reject omitted/extra/forged captures/records.
Re-read current task/attempt/spec/result/checkpoint; compare capture and settled payload. Provider-authored records alone never authorize; cancelled/superseded races refuse zero-write.
Cancel/retry and accept serialize under the same store mutex/transaction. If acceptance wins, later cancellation cannot remove history; if invalidation wins, accept writes nothing.
Exact accepted lookup wins before producer validation both in coordinator and store. Keep live guards OUT of authorize()/port construction; replay survives cancellation, lease expiry, restart and head advance, subject to current user authority.
Reuse `timeline_render_publications` PRIMARY KEY authoring_task_id, authority kind, and command ledger; no table/journal/coordinator. Consume once per TASK, not per attempt/key/digest variant.
In the SAME acceptance transaction, create checkpoint with prepare helper (nested savepoint is safe), persist accepted receipt link and pending render, alongside revision/history/receipt.
Checkpoint `prepared_json` discriminates new producer format from legacy rows and freezes pin, proposal_digest, realm/publisher, original scoped commit key/hash, approved render intent.
Its request_hash binds that frozen semantic payload; do not overwrite it on a later attempt or confuse it with commit request_hash stored inside the payload.
Reuse state prepared for accepted/render-pending; result_json holds accepted receipt plus `{project_id,timeline_id,revision_id,publication_id,content_digest}` (publication_id == receipt.receipt_id).
Presence of this accepted receipt consumes the task. A fresh key, changed actor, or newer attempt cannot commit it again; only exact scoped accepted replay succeeds.
No separately committed prepare before acceptance. If any acceptance/checkpoint write fails, rollback EVERYTHING; historical undo/restore reads do not consume/recheck old producer authority as a new proposal.
State published means render admitted: existing completion helper stores exact task/run locator in the render admission transaction. No new state/column is required.
Legacy checkpoints without the new discriminator are not reinterpreted as accepted command receipts; retain old replay until migration is proven.

## Receipt to render and compatibility

Before clearing commit flight, existing client outbox atomically retains acceptance tuple/receipt + approved pending render; unknown outcome retries exact commit, never a new key.
Freeze exact existing task-admission spec/key durably before dispatch; use approved immutable selector from render-historical-admission.md, not a mutable current-head expectation.
Runtime checkpoint must retain that exact admission identity and atomically link its original task/run/receipt on admission/replay. Persist locator before clearing pending intent.
Crash at ACK/admission boundaries resumes A after head C; never repin to C, recommit A or discard pending render. Render failure leaves accepted edit intact.
Keep interface_version=1 and ordinary edit semantics; exact contract_digest pairing still applies, so this is not arbitrary old/new binary compatibility. Producer code requires callable producer_attempt + paired support; old ports fail closed.
Current startup checks exact interface_version=1 + contract_digest; producer_attempt is not implemented on this base. Ship paired canonical definitions/generated types and synchronous port support, with a callable producer_attempt check in the consuming Agent feature; old/mixed ports fail closed. No producer capability negotiation DTO/framework or automatic ABI2. Only the additive public historical-render selector needs advertisement through existing handshake capabilities; see render-artifact-release.md.
Agent/App must stage canonical schema/goldens and official regenerated pins with Runtime; no generated/wire changes are claimed here.

## Tests and unresolved review (not implemented coverage)

Existing anchors: `tests/test_execution_identity_settlement.py::test_settlement_persists_flat_result_and_rejects_reserved_outputs`; `tests/test_execution_identity_settlement.py::test_settlement_preserves_output_descriptors`.
Keep `tests/test_timeline_render_publication.py::test_publication_is_fenced_atomic_and_exactly_replayable`; `tests/test_timeline_render_publication.py::test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence`; `tests/test_timeline_render_publication.py::test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart` passing until replacement qualifies.
Reuse `tests/test_timeline_commit_acceptance.py::test_identical_retry_after_restart_and_head_advance`; `tests/test_timeline_commit_acceptance.py::test_failure_after_receipt_rolls_back_every_row`; `tests/test_timeline_commit_acceptance.py::test_live_capture_accept_race_rolls_back_history_receipt_and_input_links`; `tests/test_timeline_commit_execution.py::test_all_provider_completions_reconcile_a_durable_winner`; `tests/test_timeline_commit_execution.py::test_authority_is_rechecked_before_disclosing_acceptance`.
Minimal new tests in existing port/acceptance suites: completed artifact success+dry run; parameterized malformed/missing/unowned/target/pin/digest/capture refusals; Node JSON.parse/stringify forwarding of 1.0 accepts, 1.5 refuses, true versus 1 refuses, and artifact-byte/digest tampering refuses; cancel/retry barrier both orders; one-shot competing keys + exact replay after restart/expiry; rollback after checkpoint; pending-A ACK/admission crash recovery. Real Agent provider/goldens required, no fabricated accepted SQL.
1. DECIDED: completed cancel remains main NO-OP; requester declining settled proposal does not commit it and keeps/discards unsent outbox intent. Before-settlement actual cancellation/supersession refuses. No revocation endpoint/journal/status.
2. DECIDED: unconsumed completed proposal survives restart using persisted epoch-matched task+attempt, not current boot. Missing/corrupt admitted spec/output fails closed; no new retention machinery.
3. Agent owns the PIN ONLY producer.guard schema/goldens, proposal artifact hash vectors and original admitted base-pair freeze/builder wiring. The earlier full-copy golden is superseded; its existence is not release qualification. Runtime owns port capture/transaction/checkpoint proofs; App/CLI own outbox receipt-to-render recovery. Viewing owns settled proposal output and removal of the committing worker hook after qualification.
Predecessor evidence (not rerun by reconciliation): 16 existing bounded seam tests passed (2.55s); temporary real-service lifecycle probe confirms retained completed identity/epoch/output across restart, cancel no-op, retry clearing current attempt/result. No new port/checkpoint/race/browser/full-suite qualification.

Release sequence and current versus planned generator support: render-artifact-release.md. No D13 implementation, new coverage or official artifact release is claimed by this reconciliation.
