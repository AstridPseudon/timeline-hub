# F-D89 R2 protected source verdict

Verdict: `PASS_SOURCE` (independent; functional qualification and merge remain held).

Candidate: `tl/agt-R2-legacy-proof-sol-0131` at `89642bafc8adbd2e56000dd3b1c89323107354f6`, tree `cb59440f0587f459c8539a5cf94497e43f2aed04`, parent `2050221347a536d0fd698817c4a200004f960564`.

Scope is exactly `astrid/sdk/timeline/inverse.py` and `tests/sdk/test_timeline_commit_provider.py`; `_commit_patch.py` is unchanged. Candidate hashes are `06bd41f404a40c17a1ec06b49c8443e0e755f622134822ede55fb3ca79234cee` and `cde797633e42e21fc7219c2b5288ce8238cdacf92e094450e02e4e746c871434`. The unchanged `_commit_patch.py` hash is `05a1ebc6b251c75f4d5dc272598adc295ce5bf5a8c4596ad08497de6676264be`.

The source seam is bounded: the conditional `include_inverse_stages=materialized` activates stage transitions only when accepted records carry `commit.materialization`; effect-only v2 stages retain the prior no-materialization representation. Existing exact checks for physical endpoints, owners, managed edges, boundaries, step IDs, ordinals, fixed policy, empty dependencies, uniqueness, missing proofs, and unexpected proofs remain in place. Existing original tests and fork-proof damage/whole/step/preview controls are unchanged by AST; 62 existing test functions are identical. The added regression is the intended 2x2 matrix: legacy dual-proof/v2 effect-only × whole/step, with preview no-write and full canonical redo closure.

Original protected worker handoff: `tl/agt-R2-provider-physical-sol-0118`, SHA `219b9ca8b196bcf4ee6fda6e08c2e50ae251ae4b`, tree `9d26efc30836abb7ae3a19882e6e917405db2f89`. Original source hashes: provider test `06228341db69c9604af57a786d4b8fc462ba881e59c195281c7151f2ce2e0ef4`; add/delete `02cae41f93c28b6167f11e342e70d0f717de97a7121342a11a7f7932ac6c1f67`; semantic reservations `6112aa1743b0958da91eaec8354a2861a7189b43b3c5bfab2f91c5a82c13e6f0`; fork guard `8302871093213098be70496272b51fba529296e78bb6bc1e53cc608e868a93c6`; inverse `0702cda4d096589e34485295cb40ffe00b0f11692bbb01fbfa5228daa1da69d4`; `_commit_patch.py` `05a1ebc6b251c75f4d5dc272598adc295ce5bf5a8c4596ad08497de6676264be`.

Original selector argv/handoff:

```text
tests/sdk/test_timeline_commit_provider.py::test_restore_undo_redo_exact_full_closure_and_unknown_fields
tests/sdk/test_timeline_commit_provider.py::test_restore_inverse_proof_representations_allow_preview_and_redo
tests/sdk/test_timeline_semantic_reservations.py::test_aggregate_children_are_retired_in_their_occurrence_scope
tests/sdk/test_timeline_inverse_fork_guard.py
```

The two unchanged original redo selectors remain the existing route; no new route or body was substituted. No product merge is requested. MAIN must run both unchanged original redo failures, the new regression, and the strict fork controls at the exact candidate source.

Static evidence: AST parse/in-memory compile passed; Ruff baseline/candidate passed; mypy with `--follow-imports=silent` passed for `inverse.py` and produced the identical NumPy 3.12-stub diagnostic for both provider-test sides; mypy with `--python-version 3.13` passed for both provider-test sides; `git diff --check` passed. No pytest, collection, helper/fixture execution, service, build, browser, render, or probe ran.
