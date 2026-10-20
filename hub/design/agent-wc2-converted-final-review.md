# Agent WC2 converted approval final review

Decision: **APPROVE**

## Exact review basis

- Candidate commit: `5e30e53eacfbcbf2234e15a3fdca97a92128548c`
- Candidate tree: `a062cd1c5826217f19e7aa8ebb4c878c9f9b7288`
- `tl/integration` base: `a8a40afd37e5560a14fa5e1a09ace6018596793e`
- Base tree: `b614c4d7036ad8b93517969fc595e9f43c9f8ff4`
- Candidate working tree was clean before this report was written.

This is an independent public-behavior/test-conversion review of the whole
candidate, not a review of the earlier HOLD. The new tests use the real
`TimelineSession.queue_proposal` and `flush` boundary against `RuntimeService`
with `publisher='requester'`; they do not call the retired candidate writer or
fabricate accepted history.

## One-to-one mapping

| Removed assertion | Replacement evidence | Verdict |
| --- | --- | --- |
| A changed approved artifact is refused and the writer is not called. | `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_proposal_queue_refuses_tampering_preserves_draft_then_accepts_fresh_request[digest]` mutates the settled proposal digest; the real requester path refuses it. It compares Runtime commit history before/after and verifies the pending commands, in-flight idempotency key, and durable conflict remain in the outbox. | **Mapped** |
| The admitted base/original target is approval-bound and tampering is refused without loss. | The same test's `[target]` case mutates `admitted_target.base_revision_id`; Runtime refuses it, with unchanged history/head and the tampered proposal still durable in the draft. `test_digest_binds_attempt_and_original_target` covers producer identity plus project, timeline, base revision, and base publication digest binding across all fields. | **Mapped** |
| An unchanged approved artifact is accepted once, returns its approval identity, and invokes the writer once. | The fresh half of both parametrized requester tests queues an unchanged copy of the actual settled proposal and accepts it only as `publisher == 'requester'`; the canonical document contains the exact opaque row `[1.0, -0.0, False]`. The existing `test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes` verifies the proposal digest pin, exact retry after Runtime restart, one-shot consumption, and normal undo. The immutable proposal digest is the replacement approval identity; there is no snapshot promotion or writer call. | **Mapped** |
| Frozen render/restart/single-generation tail: live execution, durable replay, lost acknowledgement, render count, and one claim. | `tests/timeline/test_authoring_bundle.py::test_frozen_render_restart_is_single_generation` retains the live execution and all restart/replay, lost-ack, `render_count == 1`, and single-claim assertions. Only the obsolete promotion tail was removed. | **Mapped; live/render assertions preserved** |

The two digest controls also cover every settled-command field and rationale /
extra-command sensitivity. Together with the target controls, they preserve
the original approval, digest, and base-target semantics at the requester
boundary. The new acceptance assertion preserves opaque command data without
normalization.

## Public SDK surface

The removed helper was intentionally public, so this was checked as a public
break rather than justified as dead private code. `approve_authoring_candidate`
remains exported from `astrid/core/timeline/authoring_bundle.py`,
`astrid/sdk/authoring_bundle.py`, and lazy `astrid.sdk`; the retired
`promote_approved_authoring_candidate` is absent from all three surfaces and
has no remaining code references. Direct import smoke checks confirmed the
approval helper remains callable and the promotion helper raises
`AttributeError`/`ImportError`.

The separate filmstrip-cache deletion is internally consistent: its two
helpers were moved into `filmstrip_cards.py`, all consumers import from there,
and no `_filmstrip_cache` module reference remains.

## Verification

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_producer_guard_runtime.py
7 passed in 2.87s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/timeline/test_authoring_bundle.py::test_frozen_render_restart_is_single_generation tests/editing_conformance/test_settled_proposal_contract.py::test_digest_binds_all_settled_command_fields tests/editing_conformance/test_settled_proposal_contract.py::test_digest_binds_attempt_and_original_target
24 passed in 0.61s

git diff --check tl/integration..HEAD
passed
```

The public import/export smoke check passed. No full suite, browser journey,
localhost/live-socket suite, or separate renderer suite was run.

Final verdict: **APPROVE for merge**. The prior HOLD is cleared by the real
requester-side settled-proposal conversion and its one-to-one behavior proof.
