# Agent WC2 dead-helper test map

Status: **proposed; independent reviewer approval required before manager merge**.
This note must not be read as a `DELETED` ledger update: the WC2 row changes only
after the harness merges the worker result.

## Census and decision

The worker started at Agent `tl/integration`, source `4095a349` (the current
integration head at dispatch). An exact repository search for
`promote_approved_authoring_candidate` found no product/config/resource/docs
caller. Before this change the complete set of references was:

| Kind | References | Result |
| --- | --- | --- |
| Definition | `astrid/core/timeline/authoring_bundle.py:1571-1617` | dead approval-gated whole-candidate writer |
| Production callers | none | zero |
| Tests | `tests/timeline/test_authoring_bundle.py:471,476,623` plus import at `:23` | helper-only |
| SDK boundary | `astrid/sdk/authoring_bundle.py` import/`__all__`; `astrid/sdk/__init__.py` lazy export | unused re-export only |
| Canonical core boundary | no import from `astrid/core/timeline/__init__.py` | not part of canonical core `__all__` |

The helper was therefore an accidentally export-visible but unconsumed SDK
symbol, not a live/public product consumer. The settled WC2 decision applies:
approval must bind a settled proposal digest and the requester commits it; no
candidate-level promotion writer remains. WC1 `publish_authoring_candidate`
and its writer, feedback, codec, closure, and retained-field paths are outside
this cut and remain present.

The narrative execution guide still mentions candidate approval/promotion, but
does not call or import this exact helper. It belongs to the proposal-digest
approval follow-up, not this deletion-only WC2 cut.

## Proposed source/test diff

| Existing behavior/test | WC2 action | Replacement or retained proof |
| --- | --- | --- |
| `test_approval_is_bound_to_candidate_and_base_revision` (`:458-480`) | Retire the whole test: both the stale-candidate refusal and the successful writer call are unreachable helper-only behavior. | No one-to-one replacement is claimed. The active proposal integrity suite already covers the governing replacement contract: `tests/editing_conformance/test_settled_proposal_contract.py::test_digest_binds_all_settled_command_fields` and `::test_digest_binds_attempt_and_original_target`; the real requester path is covered by `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_artifact_mutation_refuses_without_history_or_head_changes` and `::test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes`. |
| Promotion tail of `test_frozen_render_restart_then_approval_promotion_is_single_generation` (`:617-627`) | Remove only the candidate approval/promotion tail; rename the test to `test_frozen_render_restart_is_single_generation`. | All live render execution, durable replay, lost-generation, and single-claim assertions remain unchanged in the same test. |
| `promote_approved_authoring_candidate` definition | Delete exactly the 47-line function body plus surrounding blank-line diff. | No refusal shim, replacement writer, schema, history, or producer authority is added. |
| Helper exports | Remove its one core-module `__all__` entry, the SDK facade import/`__all__` entries, and the lazy SDK export. | `publish_authoring_candidate` remains exported and untouched for WC1. `approve_authoring_candidate` remains for the separate proposal-digest rewrite; this cut does not claim that rewrite. |

The implementation diff is intentionally limited to 50 product lines, 3 SDK
export-boundary lines, and 42 test lines removed, with the live render test
renamed in place. No assertion on publish, feedback, authoring closure, media,
opaque fields, retained inputs, or active proposal/requester behavior was
weakened.

## Reviewer checklist

- Confirm the exact-symbol census remains zero production callers at merge time.
- Confirm the three active proposal/requester tests named above remain positive
  and are not changed by this worker.
- Confirm `publish_authoring_candidate` and all authoring codec/closure/feedback
  paths remain present.
- Confirm the WC2 ledger row is not marked `DELETED` until the harness merge.
