# RT02 key-required positive mapping

## Result

The key-required RT02 positive is now a genuine native selected integration
case on Runtime `a6bce81`, merged from
`tl/rt-m2-rt02-key-required-positive-mapping` after independent review
`96d473c` (APPROVE). It keeps the original test name and scope:

`tests/test_runtime_p1_blockers.py::test_project_shot_updates_require_idempotency_keys_at_service_boundary`

The case registers the real Astrid provider and submits the film edit through
the timeline commit path. It preserves the retired direct-shot refusal and
zero-write checks, refuses missing, blank, and overlong keys before mutation,
accepts the valid keyed edit, and verifies exact replay without invoking the
semantic provider again.

## Original RT02 positive mapping

The exact four original names remain the ledger's mapping list:

| Original test | Current mapping |
| --- | --- |
| `tests/test_runtime_e2e.py::test_project_shot_crud_isolated_idempotent_and_restart_durable` | Direct project-shot writer remains a strict-xfail gap. |
| `tests/test_runtime_domains.py::test_project_shot_mutations_roll_back_before_idempotency_replay` | Direct project-shot writer remains a strict-xfail gap. |
| `tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting` | Shot/reference creation conversion remains open; its separate review found the timeline-reference assertion missing. |
| `tests/test_runtime_p1_blockers.py::test_project_shot_updates_require_idempotency_keys_at_service_boundary` | Genuine native provider-backed mapping above; selected only with `-m integration`. |

The default pytest expression still deselects integration tests. The three
unmapped original positives and the legacy refusal controls remain unchanged;
this is not an all-RT02 completion claim.

Evidence sources: the independent key-conversion review, the Runtime manager
STATUS snapshot, and the exact merge record at
`2026-10-20T22:11:47Z runtime rt-m2-rt02-key-required-positive-mapping a6bce81`.
