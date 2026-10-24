FAIL_SOURCE — F-D85 protected review

- Reviewed author commit `a7056a2779` against integration `3edc45cb26`; delta is only the assigned test file.
- AST conservation passed: all 7 test functions and 11 parameter expansions are unchanged. Baseline hash `e001...cad4`; candidate `6b27...0d9`.
- Findings:
  - [line 240](/home/user/work/wt/agt-F-native-sheet-review-2342/tests/editing_conformance/test_native_sheet_ordinary_runtime.py:240): two `track.create` commands are captured from the same bundle, then batch-executed. In-memory execution rejects the second with `selection_changed`.
  - [line 248](/home/user/work/wt/agt-F-native-sheet-review-2342/tests/editing_conformance/test_native_sheet_ordinary_runtime.py:248): after sequential capture, `internal:film.registry.assets.source` claims `before: present({})`, but the native bootstrap leaves that field absent. In-memory execution rejects it with `previous_value_mismatch`.
  - Shared native-batch coverage still expects retired `edit commands-file`; current CLI exposes `edit --file`/`commit` and no `commands-file`. This is outside the author delta and remains for the D86 owner.

Checks:

- In-memory compile baseline/candidate: PASS.
- Scoped Ruff baseline/candidate: PASS; repository Ruff baseline: PASS (`2143 == 2143`).
- Mypy: blocked before comparison by environment diagnostics: missing YAML stubs and incompatible NumPy stubs, exit 2.
- `git diff --check`: PASS.
- No pytest, service, build, render, or functional proof run.

No merge request was queued because source review failed. No worktree files changed. `DONE` and the F-D85 commit message were written.