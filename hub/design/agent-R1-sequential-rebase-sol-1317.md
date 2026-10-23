# R1 sequential physical rebase — blocked draft

Worker `agt-R1-sequential-rebase-sol-1317`; Agent parent `f6116e1b658514021cbbf08d5a6f16a240523f1a`; Runtime `3b926efab2eed122d374540baee297d4cdcec62a`.

**BLOCKED. Do not integrate this draft. End-to-end RED/GREEN is not achieved. G5 remains draft only / P1 NO-GO.**

## Changes

Only `_commit_patch.py` and new `tests/editing_conformance/test_doc_patch_sequential_rebase.py` change in the worktree. The candidate retains staged physical declared-read and patch bindings. It represents their source as an earlier step's generated materialization, resolves that source through authenticated intervening history, and obtains the successor from that step's actual replay input/output and captured writes. It checks the owner and complete owners list; no future ID is calculated, alias retargeted, closure imported, read discarded, or Runtime guard changed. Step attribution and the request remain intact. Recursion follows strictly earlier command boundaries, including repeated physical roots.

The independent direct provider regression is reduced from the retained G5 commands (`cross.at: 3.5 → 4.0 → 4.1`) and the verified sequential materialization. It uses the existing `flat_film` / `saved_source` fixture, genuine media ingest, genuine provider registration, genuine Runtime service/store and the current pin. Setup uses the existing trusted seed fixture seam; there is no new provisioning mechanism or alternate executor. The peer changes `late.params.text` in the same physical internal timeline. Tests cover fresh/moved head with and without explicit step reads, exact current input digests and landing-head attribution, distinct steps, preview no-write, exact retry, request metadata, and same-field / consulted-read / membership / changed-source / forged-continuation refusal with complete SQLite dump equality. Original success expectations remain; neither failing positive is skipped, xfailed or rewritten as refusal.

Read the shared `design/agent-G5-helper-sequential-cut-1258.md` report and retained `boundary-004-resolve-error.json`, `boundary-005-execute-error.json`; the report is not present in this base worktree. No helper/G5 changes are required to reproduce the failure.

## Evidence that the assigned Agent-only scope is insufficient

The original failure is confirmed at the specified parent: the two moved-head cases fail before acceptance. The candidate corrects both omissions and completes real provider replay. **Pinned Runtime then independently refuses the unchanged submitted staged ID.** This is an additional boundary, not evidence that Runtime's guard should be waived.

Durable capture `workers/agt-R1-sequential-rebase-sol-1317/evidence/capture-003-auth-error.json` contains the complete request, prepared records/canonical document, authenticated base/source, initial continuation map, actual import origins and traceback. `capture-001-execution.json` and `capture-002-execution.json` contain complete original and replay plans, bindings and effects. The instrumentation is outside the worktree and only records/delegates to existing execution and validation.

In that capture, command 2 submits original staged internal `8c0c963bb29709e99bc660afe7a6d14b881ef341da5ad949125d211fce37edcb`; actual replay step 1 produces internal `c231879cef885560a0a6e0583af071c716dce0bdd66b14f7a246118b27fd8335`. Both are `internal-revision:authoring-timeline-revision-…` refs. The peer history authenticates initial internal `internal-film` → `22a0eeabc105e3e214b33e37c2ec95e60fac3ee33abd0e53473076533dc36338`. Replay authenticates that peer internal → replay step-1 output. There is no authenticated outgoing edge for the original unlanded staged internal.

Runtime `timeline_commit_auth.py:1043` calls `validate_step` at each actual step input. With declared reads, `validate_step:302` → `validate_read:231` → `normalized:207` → `site:170` rejects the original staged physical ref: `invalid_records`, HTTP 422, `provider alias is outside its authenticated boundary`. Without step reads, the same refusal occurs normalizing the submitted step patch at `validate_step:336`. `_binding_continuations` supplies accepted history edges; validation adds actual replay `commit.materialization` edges after each step. Neither computes/authenticates the original unlanded execution. `validate_claims` also requires the executed command args to equal the original request, so substituting the replay ref in the wire/command would violate the guard and the brief. A fabricated materialization edge is not admissible: validation requires its source to be in the actual input and checks its managed owner edges.

Therefore the task's assertion that existing source-backed sequential provenance suffices for **acceptance by unchanged Runtime3b**, while retaining the complete original physical request, is not established by the current code; this direct case disproves it. I did not change Runtime or try to bypass that refusal. The success assertions after that rejection (merged canonical/history/binding/undo behavior) remain unverified on the moved head. Fresh-head acceptance and existing rebase/inverse guards pass.

## Exact commands and results

All commands ran in `/home/user/work/wt/agt-R1-sequential-rebase-sol-1317` unless specified. Evidence logs are under this worker's durable `evidence/` directory.

Pytest prefix:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider
```

- At unchanged parent product code, prefix plus `tests/editing_conformance/test_doc_patch_sequential_rebase.py --basetemp=/tmp/w-688c2a909e/red --tb=long --showlocals -s`: **2 failed, 6 passed in 15.05s**, exit 1 (`red.log`). This was before adding the forged-history case. Both moved-head positives failed with the original outside-closure evaluation error.
- First candidate, prefix plus `tests/editing_conformance/test_doc_patch_sequential_rebase.py --basetemp=/tmp/w-688c2a909e/green --tb=long --showlocals -s`: **2 failed, 6 passed in 18.51s**, exit 1 (`green.log`). The filename does not mean a green result: failures moved to actual Runtime acceptance validation.
- Named-neighbor run: prefix plus `tests/editing_conformance/test_doc_patch_sequential_rebase.py tests/editing_conformance/test_doc_patch_v2.py::test_rebase_requires_source_bound_materialization_and_exact_managed_edges tests/editing_conformance/test_doc_patch_v2.py::test_authenticated_successor_chain_lands_on_exact_physical_image tests/editing_conformance/test_doc_patch_v2.py::test_still_reachable_original_image_does_not_follow_other_owners_branch tests/editing_conformance/test_doc_patch_v2.py::test_rebase_follows_shared_physical_successor_for_disjoint_child_fields tests/editing_conformance/test_doc_patch_v2.py::test_declared_qualified_scope_read_follows_authenticated_shared_successor tests/editing_conformance/test_doc_patch_v2.py::test_semantic_creation_then_patch_rebases_over_unrelated_parent_field tests/editing_conformance/test_doc_patch_v2.py::test_history_aba_is_a_conflict_even_with_equal_final_value tests/editing_conformance/test_doc_patch_v2.py::test_ordered_read_detects_shape_aba_and_membership_read_ignores_reorder tests/editing_conformance/test_doc_patch_v2.py::test_inherited_native_read_conflicts_with_later_dependency_writes tests/editing_conformance/test_doc_patch_v2.py::test_provider_merges_disjoint_fields_and_inverse_uses_actual_landing_head --basetemp=/tmp/w-688c2a909e/targeted --tb=long --showlocals -s`: **2 failed, 33 passed in 34.78s**, exit 1 (`targeted.log`). All selected existing guards passed. These existing tests retain their existing detached ABI fixture; the new regression uses real Runtime.
- Final broadened neighbor file: prefix plus `tests/editing_conformance/test_doc_patch_sequential_rebase.py tests/editing_conformance/test_doc_patch_v2.py --basetemp=/tmp/w-688c2a909e/final --tb=long --showlocals -s`: **2 failed, 109 passed in 18.53s**, exit 1 (`final.log`). All 102 existing v2 cases and seven new cases passed. Both moved-head success expectations remain failures. New-case actual provider/Runtime origins print before and after each case.
- Diagnostic capture: same prefix with `PYTHONPATH=.:/tmp/w-688c2a909e:/home/user/work/wt/rt-pin-3b926efa`, plus `-p capture_r1 'tests/editing_conformance/test_doc_patch_sequential_rebase.py::test_sequential_physical_inputs_land_at_actual_step_boundaries[True-True]' --basetemp=/tmp/w-688c2a909e/capture --tb=long --showlocals -s`: **1 failed in 6.36s**, exit 1 (`capture.log`), full structured capture above.
- Refusal diagnostic: prefix plus `tests/editing_conformance/test_doc_patch_sequential_rebase.py::test_sequential_refusal_has_no_writes --basetemp=/tmp/w-688c2a909e/refusals --tb=long --showlocals -s`: **5 passed in 11.63s** (`refusals.log`). Exact reasons: field/consulted `value_conflict`, membership `selection_changed`, changed physical source `outside_closure`, forged materialization edge `history_unavailable`. Final run additionally asserts those exact reasons.

Quality commands:

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-688c2a909e/ruff /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-688c2a909e/mypy-current /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/editing_conformance/test_doc_patch_sequential_rebase.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Ruff: **2149/2149**, PASS. New test Ruff: PASS. Vendor lock: `ok runtime.lock.json`; artifact check: `artifacts.json is current`; diff check: PASS. Mypy and diagnostic identity results recorded below after completion.

No full suite, central full-suite request, browser, HTTP/socket, daemon, helper suite, prohibited journey repeat, shared dependency/cache mutation, Git mutation, integration write, branch/ref deletion or push. No schema/generated/pin/contract changes. No permission denial occurred.

## Next owner

Orchestrator must resolve the cross-boundary source-proof requirement before calling this an independently mergeable Agent fix. Runtime must be able to authenticate the original sequential boundary and its corresponding replayed boundary, preserving root identity, owners and previous/read/order guards; this is not permission to add a waiver. Once that bounded work is authorized/available, review the retained provider candidate and rerun these exact direct regressions. Keep the two positive expectations unchanged. No integration deletion or G5/P1 promotion is justified by this draft.
