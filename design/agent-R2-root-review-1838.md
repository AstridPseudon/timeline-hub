# R2 root-baseline review — PASS (narrow)

Review target: `d146b4204` over `0b735c13710d74600cc51bf55e4963b54163087e`.
This is an independent review of the root-baseline change only. It does not
approve the `0b` ancestry or claim the whole R2 task. No source or test files
were changed by this review.

## Scope and decision

PASS for the declared root-only scope:

- `astrid/sdk/timeline/_root_inverse.py` (31-line change);
- `tests/editing_conformance/test_transient_root_baseline.py` (111-line focused
  test module);
- the candidate's flat worker design report.

The source change accepts only an authenticated native stage. It checks that
the `_inverse_stage` source command is present in the accepted entry, that the
submitted native writes equal the exact accepted `native_write_range` slice,
and that the detached projection can replay the accepted command writes with
the existing `guard` operation. The projection is made from a deep-copied
accepted-before `State`; it is not installed as live state and does not execute
the accepted effect patch.

The only new source import is the existing `_RestoredShot` provenance type;
the root helper does not import a later R2 artifact or route.

The projected stage root is checked against the accepted after boundary,
including the canonical root value and exact owner set. The live root must
match the projected pre-removal root, the native removal's full before-value,
and both accepted-before and projected owner sets. The live value is then
wrapped with the existing `_RestoredShot` provenance carrying the complete
accepted runtime document. No authored root is copied from a request or from
an untrusted capture.

## Guard review

PASS for the requested root checks:

- full payload and internal timeline: compared through the complete root value;
- root identity and owner set: fixed by the accepted write reference and exact
  owner-set comparisons;
- native before/after values: replayed with `guard`, then compared at the live
  root boundary;
- native slice and range: accepted source command membership plus exact
  `native_write_range` slice equality;
- canonical final root/closure boundary: projected root is guarded against the
  accepted after boundary before owner comparison;
- ABA and later-consumer behavior: unchanged inverse, selected-step, physical
  binding, surviving-consumer, and later-history checks remain outside this
  narrow helper. They were not reimplemented or waived here.

Source document scope, revision/digest validation, closure pins, and retained
`_RestoredShot` compiler provenance remain owned by the existing compiler and
inverse paths. The root helper does not independently re-implement those
checks; this review therefore does not claim whole-R2 or Runtime integration.
The bounded source-mapping probe showed the transient recorded root is
intentionally not in `source_mapping.shots`; no source-retarget acceptance was
introduced by this change.

## Behavioral evidence

All commands used the Agent venv, `PYTHONDONTWRITEBYTECODE=1`, and Runtime pin
`/home/user/work/wt/rt-pin-2a9e347f` as shown below.

1. Unchanged original transient-root behavior:

   `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-2a9e347f:/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-root-review-1838/evidence" /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p validation_capture tests/editing_conformance/test_provider_step_undo_v2.py::test_create_edit_whole_undo_redo_retains_transient_roots`

   Result: **1 passed** in 2.97s. The capture recorded module hashes before
   validation and full inverse/root inputs in permanent worker evidence.

2. New strict root-baseline guards:

   `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-2a9e347f" /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_transient_root_baseline.py`

   Result: **10 passed** in 4.94s. This includes authored payload/internal/
   owner damage, foreign source command, altered range/slice, native before and
   after proof damage, and mismatched source after-boundary; each asserts
   `history_unavailable` and no mutation.

3. Existing root-restore controls:

   `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-2a9e347f" /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_captured_redo_media_closure.py -k "not exact_captured_redo"`

   Result: **8 passed, 1 deselected** in 0.81s. The deselected integration
   test requires the separate Runtime/manual lane and was not claimed here.

Static checks:

- scoped Ruff on both touched files: **All checks passed**;
- private mypy on both touched files with a worker-local cache: **no issues**;
- `git diff --check`: **clean** for the candidate scope.

## Limits and next step

No full suite, Runtime integration, HTTP/browser test, old matrix, SDK-four,
or unrelated historical rerun was performed. The original source failure was
reviewed as the candidate's deterministic reconstruction rather than a newly
instrumented retained pre-patch execution. Recommended next step is the
orchestrator's serial merge decision, followed by Runtime-owned integration
evidence; do not treat this report as approval of the full R2 ancestry.

Evidence:

- candidate report: `/home/user/work/wt/agt-R2-root-review-1838/design/agent-R2-root-review-1838.md`;
- permanent review capture: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-root-review-1838/evidence/original-postpatch.json`;
- module hashes and input trace are recorded in that capture; the worker
  evidence directory also contains `SHA256SUMS` and `credential-scan.json`.
