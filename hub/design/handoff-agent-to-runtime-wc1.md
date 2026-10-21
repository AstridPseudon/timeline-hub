# Agent -> Runtime handoff: WC1 settled proposal/requester seam

Date: 2026-10-21 04:30 UTC  
Row: WC1  
Result: qualify one real `publish_authoring_candidate` consumer on the
existing settled-proposal -> requester `TimelineSession` seam. Runtime must
accept the unchanged, digest-bound `SettledProducerProposal` through the
existing first `producer.guard`, `producer_attempt` capture, normal `/v1`
commit acceptance, exact replay, and guarded inverse. This is the Runtime half
of the migration; it is not permission to restore or extend the old
`publish_parent_composition` writer.

## Exact base

Agent base used for this handoff: `5a625dd4c01149a085a9df85952b34cad70801f9`.
This is the worker `HEAD` and `refs/remotes/hub/tl/integration` at capture
time. The local `refs/heads/tl/integration` value `634060e09a3881708803587378477231c9f7eff4`
was stale and was not used.

## Boundary and permitted paths

The single Agent consumer to pair is the current whole-candidate path in
`astrid/sdk/timeline/store.py:308-375` (`publish_bundle`), which calls
`astrid/core/timeline/authoring_bundle.py:1620-1655`
(`publish_authoring_candidate`) through a local parent-publication writer.
Those Agent files are read-only context for Runtime. The other
`publish_authoring_candidate` callers are not assigned here: `sdk/remote.py`,
`sdk/authoring_remote.py`, `sdk/timeline_elements.py`, and the detached
document-script caller remain separate WC4/WC5/WC6 work.

Runtime may work only in these Runtime-relative paths:

- `runtime_protocol/timeline_commit_producer.py`
- `runtime_protocol/timeline_commit_port.py`
- `runtime_protocol/timeline_commit_producer_checkpoint.py`, only if an
  existing seam test demonstrates a bounded acceptance/replay gap
- the existing producer/commit test files:
  `tests/test_timeline_producer_guards.py`,
  `tests/test_timeline_commit_producer.py`,
  `tests/test_timeline_producer_checkpoint.py`,
  `tests/test_timeline_producer_record_boundary.py`, and
  `tests/test_timeline_current_union_contract.py`

Do not touch Runtime launcher/origin/custody files (D13/WC10), generated
client/schema or version-pin files, media-selection/raw-media carriers,
transcript/order paths, or any Agent/App/Composition tree.

## Dependencies and seam contract

1. The Agent migration must emit the existing six-key settled proposal:
   original `admitted_target` pair, host-owned `producer` identity, ordinary
   recorded commands, rationale, and canonical `proposal_digest` over the
   authoritative artifact bytes. It must call the existing
   `TimelineSession.queue_proposal`/`flush`, not a new Runtime endpoint.
2. Runtime must keep the current request-scoped `producer_attempt(pin)` and
   exact `producer.guard` dependency. The pin is derived from the settled
   artifact and immutable admitted target; caller JSON, current-head reads,
   latest lookup, or a reserialized digest are not authority.
3. The pair must preserve the original base revision/publication, rationale,
   opaque values and command order through a server-side rebase. A pending
   proposal is retained on refusal; an accepted proposal is one-shot, exact
   replayable after restart, and undoable with the existing inverse path.

## Original positive floor

Keep these existing Agent assertions unchanged and use them as the paired
requester contract:

- `tests/sdk/test_timeline_producer_guard.py::test_proposal_uses_existing_outbox_original_base_reason_and_exact_flight`
- `tests/sdk/test_timeline_producer_guard.py::test_provider_rebase_retains_original_admitted_base_and_capture`
- `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes`
- `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_proposal_queue_refuses_tampering_preserves_draft_then_accepts_fresh_request`
- `tests/timeline/test_authoring_bundle.py::test_candidate_compiler_integrates_with_runtime_atomic_publication`
- `tests/timeline/test_authoring_bundle.py::test_publish_uses_one_compilation_and_returns_complete_mapping`
- `tests/timeline/test_authoring_media.py::test_document_publish_forwards_new_stale_head_to_runtime`
- `tests/timeline/test_authoring_feedback.py::test_target_bound_sdk_defers_replay_and_stale_decisions_to_runtime`

The direct Agent command used for the producer/requester floor is:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_producer_guard.py \
  tests/sdk/test_timeline_producer_guard_runtime.py \
  tests/timeline/test_authoring_bundle.py::test_candidate_compiler_integrates_with_runtime_atomic_publication \
  tests/timeline/test_authoring_media.py::test_document_publish_forwards_new_stale_head_to_runtime \
  tests/timeline/test_authoring_feedback.py::test_target_bound_sdk_defers_replay_and_stale_decisions_to_runtime
```

The direct Runtime seam command is:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_producer_guards.py \
  tests/test_timeline_commit_producer.py \
  tests/test_timeline_producer_checkpoint.py \
  tests/test_timeline_producer_record_boundary.py \
  tests/test_timeline_current_union_contract.py
```

## Preserve, hold, and deletion condition

Preserve every original candidate mapping/group/shared-identity/timing/media
assertion, exact base pair, proposal digest, rationale, opaque field, retry
identity, restart recovery, stale refusal, acceptance receipt, history, and
inverse/ABA guard. Do not encode a missing Runtime proof as an xfail or a
refusal of a formerly positive candidate publication.

No `full*`, browser, renderer, live-socket, installed-launcher, generation,
schema/client pin, or activation run is part of this handoff. Do not mint a
new Runtime pin or activate a private source. The existing published014/95bd
pair remains frozen.

Delete `publish_authoring_candidate` and its public exports only after every
production caller has its own reviewed proposal/requester replacement,
including the separately owned WC4/WC5/WC6 callers, and the exact positive
floor above plus a real paired acceptance/restart/retry/inverse run pass.
This WC1 handoff alone does not authorize that deletion.

## Remote merge route

Runtime manager owns any Runtime source/test change. After the manager has a
committed worker branch and targeted evidence, submit it through the remote
merge route:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-merge-remote runtime <runtime-worker-name> "WC1 settled proposal/requester seam; preserve existing positives"
```

The Runtime home machine merges into its `tl/integration`; Agent reviews the
paired consumer only after that merge. No direct merge, push, pin, or branch
mutation is requested here.
