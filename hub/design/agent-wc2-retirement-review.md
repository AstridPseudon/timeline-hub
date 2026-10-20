# Agent WC2 public/test-preservation review

Decision: **HOLD**

Reviewed source tree:

- base `tl/integration`: `4095a3490bde80e20913d216bfd3032b0a41b610`
- WC2 candidate: `5e12f831b7e9fb51317eff8e1abc47c0d5caa0d5`
- candidate tree: `41a4e034376dac5a7c7b92866002a04aab7838fd`

The owner’s 06:59 decision authorizes eventual deletion of the whole-document
fallback writer and says approval must bind the proposal digest, with the
requesting client committing the proposal. It also says the functions remain
held until those replacements land. This review does not relitigate that
decision.

## Public-surface finding

The worker’s “accidentally export-visible” label is not sufficient. On the
review base, `promote_approved_authoring_candidate` is imported and listed in
both `astrid/sdk/authoring_bundle.py` and the lazy `astrid.sdk` `_EXPORTS`
map. `from astrid.sdk.authoring_bundle import ...` and
`astrid.sdk.promote_approved_authoring_candidate` were therefore public SDK
surfaces, regardless of the zero repository production-caller census. The
owner’s planned writer retirement can authorize this public break, but only
with the replacement/adoption evidence below.

## Removed assertion review

| Removed behavior | Evidence on the candidate | Review result |
| --- | --- | --- |
| A changed candidate is rejected against an unchanged approval and the writer is not called. | `test_settled_artifact_mutation_refuses_without_history_or_head_changes` is a real Runtime/requester test and refuses mutated command data, rationale, or proposal digest without changing commit history. The digest tests cover command/producer/target binding, but their module explicitly says they are design goldens, not Runtime acceptance. | **Partial mapping only.** This proves the analogous settled-proposal refusal, not approval-artifact binding. No active test mutates the admitted base target through the requester and proves the approval replacement rejects it. |
| An unchanged approved artifact is accepted, returns the approval identifier, and invokes the writer once. | `test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes` is a real Runtime/requester positive and proves acceptance, exact retry after restart, one-shot consumption, and undo. | **Partial mapping only.** It starts from a settled proposal; it has no approval artifact or approval identifier, so it does not prove the planned approval-to-proposal replacement. |
| Frozen render/restart/single-generation tail. | The renamed `test_frozen_render_restart_is_single_generation` retains the live execution, durable replay, lost-generation, render-count, and single-claim assertions. The deleted tail was only the old helper’s stub writer call. | **Valid removal.** No live generation or restart assertion was weakened. |

The mapped requester tests are genuine and semantically useful; they are not
merely name matches. They still do not provide a one-to-one replacement for
the approval-specific assertions that were removed. In particular, the
candidate branch leaves `approve_authoring_candidate` public and still
candidate-bound, while no current test or production path exercises an
approval bound to a proposal digest and then commits through the requester.

## Smallest unmet dependency / required conversion

Keep WC2 held until the planned approval replacement is implemented and
qualified. Then convert the removed approval test in place (without restoring
the whole-candidate writer) to use the real proposal/requester path and assert:

1. a changed settled proposal or admitted base is refused with no head/history
   change;
2. the unchanged approved proposal is accepted once by the normal requester;
3. exact retry after restart returns the original result, and the normal undo
   path remains valid; and
4. the approval/proposal digest binding is asserted directly, including the
   preserved opaque command data.

Until that adoption exists, the public export deletion and retirement of the
approval-specific test behavior are not independently mergeable. Do not add a
refusal shim, fallback writer, fabricated history, or weakened assertion.

## Verification

Independent bounded command (candidate tree):

```text
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_settled_proposal_contract.py::test_digest_binds_all_settled_command_fields \
  tests/editing_conformance/test_settled_proposal_contract.py::test_digest_binds_attempt_and_original_target \
  tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes \
  'tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_artifact_mutation_refuses_without_history_or_head_changes' \
  tests/timeline/test_authoring_bundle.py::test_frozen_render_restart_is_single_generation
```

Result: **24 passed, 5 deselected in 0.79s**.

Also ran `git diff --check tl/integration..HEAD`: passed. No full, browser,
or broad suite was run. The candidate’s worker-reported 112 targeted plus 5
producer-integration passes were not treated as approval evidence beyond this
bounded independent check.

