## Report

Implemented the installed external-pack root fix.

- `invoke_capability()` now:
  - Requires admitted roots to be fenced and digest-bound.
  - Removes ambient/custom `PYTHONPATH` in installed mode.
  - Carries only validated admitted roots into installed children.
- Added focused regressions in [test_installed_external_pack_roots.py](/home/user/work/wt/agt-F-external-installed-roots-0015/tests/stage1/test_installed_external_pack_roots.py).

Tests:

- `5 passed` — installed-root regression file.
- `7 passed` — source-fence/admission security neighbors.
- Ruff: passed for new test file.
- Mypy: passed for new test file.
- `git diff --check`: passed.

The original positive external-pack test remains unverified: it failed before provider execution with `ModuleNotFoundError: runtime_protocol` in this local child environment. No full suite was run.

Commit message and `DONE` marker were written as required.