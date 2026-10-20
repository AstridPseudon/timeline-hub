# Agent WC2 approval assertion conversion

Status: **ready for final independent review**.

## Exact source and tree

- Worker worktree: `/home/user/work/wt/agt-m2-wc2-approval-test-conversion`
- Base commit: `5e12f831b7e9fb51317eff8e1abc47c0d5caa0d5`
- Base tree: `41a4e034376dac5a7c7b92866002a04aab7838fd`
- Working-tree change: `tests/sdk/test_timeline_producer_guard_runtime.py`, 75 added
  lines; no product source, schema, DTO, API, store, fixture, or legacy writer
  changes.
- Working diff SHA-256: `e58b698b2fec39f6f100b19964f4b12a7956b7d8723c675e287dcb07606aa8bb`

## One-to-one assertion mapping

| Retired test/assertion | Current proof | Mapping |
| --- | --- | --- |
| `tests/timeline/test_authoring_bundle.py::test_approval_is_bound_to_candidate_and_base_revision`: changed approved artifact refuses and writer is not called | `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_proposal_queue_refuses_tampering_preserves_draft_then_accepts_fresh_request[digest]` and `[target]` | The real settled proposal is queued through `TimelineSession.queue_proposal`; a tampered proposal digest or original admitted target is refused by the real Runtime requester path. Accepted history/head is byte-equal before and after refusal, and the queued commands plus in-flight key remain in the outbox draft. |
| Same retired test: unchanged approved artifact is accepted once under the approval | Same test, after refusal, using a fresh requester outbox and an unchanged copy of the actual settled proposal | The normal requester commits it with `publisher == 'requester'`; the accepted canonical document contains the proposed opaque command row unchanged. Queueing the immutable verified proposal is the explicit approval intent; no snapshot promotion or candidate writer exists. |
| `tests/timeline/test_authoring_bundle.py::test_frozen_render_restart_then_approval_promotion_is_single_generation`: live render, durable replay, lost acknowledgement, render count and single claim | `tests/timeline/test_authoring_bundle.py::test_frozen_render_restart_is_single_generation` (existing cut test, line 456) | The candidate-promotion tail was removed, but all frozen render/restart/single-generation assertions remain in place and pass. |

The existing `test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes`
remains unchanged and supplies exact requester retry-after-Restart, one-shot
consumption, and normal inverse/undo evidence. The existing direct mutation test
also remains unchanged; this conversion adds the missing queue-boundary proof.

## Verification

Exact commands from the worker tree:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_producer_guard_runtime.py
7 passed in 2.67s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/timeline/test_authoring_bundle.py::test_frozen_render_restart_is_single_generation tests/editing_conformance/test_settled_proposal_contract.py::test_digest_binds_all_settled_command_fields tests/editing_conformance/test_settled_proposal_contract.py::test_digest_binds_attempt_and_original_target
24 passed in 0.61s

/home/user/work/venv-agent/bin/ruff check --no-cache tests/sdk/test_timeline_producer_guard_runtime.py
All checks passed!

git diff --check
passed
```

No full suite, browser, localhost, live-socket suite, or unrelated passing-case
repeat was run. Final independent review is still required before merge.
