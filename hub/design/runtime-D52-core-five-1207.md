## FAIL — F-D52-core-five

Traced production path: `create_runtime_commit_service().commit()` → `commands.execute(..., commit_request=request)` → compiler/materialization validation. Runtime imports came from `/home/user/work/runtime`; this is source-mode, not HTTP proof.

Results:

- Captured config native-order: PASS
- Nested config native-order: PASS
- Retained fork reload/undo: PASS
- Independent parent edit + preview redo: FAIL
- Retained-sibling fork history: FAIL

Exact command: assigned five selectors under the required `PYTHONPATH`, with JUnit output in `evidence/assigned.xml`.

Both failures reach `_commit_patch.py:_materialization_sites` during redo and reject with `history_unavailable: inverse stage image differs from authenticated effects`. The retained original root remains reachable through the sibling, so the accepted inverse record has no after-side `commit.effect` pin; the provider incorrectly requires one. This is a product authentication/materialization seam, not a fixture defect.

No files were changed; all protected test/body AST hashes are unchanged. No fixture repair, Ruff, or typecheck was warranted. `git diff --check` passed and the worktree is clean. Evidence is under the worker evidence directory.