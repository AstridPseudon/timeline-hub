# D134 root-008 source validation

Status: **UNAPPLIED**. Behavior status: **NOTRUN** by task instruction.

- Exact 96a6 baseline: PASS. `HEAD` is `96a6b2deea46eb33ba5184203a10e966cc5e9179`.
- Exact root-008 membership: PASS. 18 members match the supplied cluster JSON; no member was edited.
- AST input/predicate conservation: PASS. Both owned files have identical function-body ASTs to 96a6; owned blobs are identical to their 96a6 blobs.
- `/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_fork_abi1_binding_set.py tests/editing_conformance/test_recipe_occurrence_fork.py`: PASS (`All checks passed!`).
- `/home/user/work/venv-agent/bin/mypy tests/editing_conformance/test_fork_abi1_binding_set.py tests/editing_conformance/test_recipe_occurrence_fork.py`: PASS (`Success: no issues found in 2 source files`). This is the unchanged-source baseline.
- `PYTHONPYCACHEPREFIX=/tmp/w-74f1cfcea0/pycache /usr/bin/python3.11` AST parse and compile for both owned files: PASS.
- `git diff --check`: PASS.
- Outside-scope Git blob equality: PASS. Worktree is clean and no files changed.

Not run by instruction: pytest, collection, service/runtime calls, sockets, browser, native replay, original18, family/full/core/tour/profile/collector/build/install suites.
