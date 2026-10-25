Implemented the fixture repair in [test_commit_runtime_shared_inverse.py](/home/user/work/wt/agt-D86-main-inverse-return-0003/tests/editing_conformance/test_commit_runtime_shared_inverse.py).

- Replaced unsupported generic membership creation with native `occurrence.place-shared`.
- Preserved original shared shot/revision identity and all ten scenarios/tests.
- Confirmed production registration/allocation via `native_occurrence_shared.py:295-334` and `commands.py:95-96`.
- AST conservation, compile, Ruff, mypy, and `git diff --check`: passed.
- Baseline Ruff/mypy: passed.
- Pytest/service qualification: intentionally not run per D85/D86.
- Commit message written; `DONE` created.