## Report

- **Fixture preservation: PASS.** `d7390a90d4` changes only the trusted v2 setup in `test_authoring_bundle.py`; all 11 assertions and original `_closure` topology/raw media are preserved.
- Trusted seed origin is exact Runtime state: parent `parent-1`, shot `shot-shared/shot-rev-1`, internal timeline `main/internal-1`. Both `occ-1` and `occ-2` intentionally reference that same physical shot.
- Authoring aliases are distinct:
  - `occ-1` → `shot-placement-1e58a2be...`
  - `occ-2` → `shot-placement-ad727b5e...`
- The candidate changes only the first alias (`items[0].media_id`, `clips[0].asset`, and adds `new-picture`). The second remains unchanged. Both resolve to `shot-revision:shot-rev-1`, producing the exact contradictory root pair at path `[]`.
- The guard is correct and independently tested: `tests/sdk/test_timeline_public_command.py::test_public_free_edit_cannot_broadcast_one_shared_alias`.
- **Causal owner: PASS — Agent authoring publication path, owner 0152.** `authoring_commit.py` routes the shared-alias candidate through generic `emit_document_commands`; the existing legitimate materialization logic is in `compile_authoring_candidate`, but no valid semantic/fork projection bridges this case. Runtime fixture mapping is not the defect.
- No product fix, fixture correction, guard change, or known-failed integration rerun was made.

Checks:

- `pytest --collect-only ...::test_candidate_compiler_integrates_with_runtime_atomic_publication` — **1 collected**
- Ruff changed file — **passed**
- Mypy changed file — **passed**
- AST assertion mapping — **11 original / 11 current; exact assertion multiset preserved**
- `git diff --check` — **passed**
- Worktree — **clean**

The target integration remains unverified/blocked at the known Agent `DocumentPatchError`; the concrete Runtime publication receipt ID was not claimed because rerunning the failed body was prohibited.