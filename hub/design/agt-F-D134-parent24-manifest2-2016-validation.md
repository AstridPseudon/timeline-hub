# Validation

Base source was verified at `a30e74e901a28b39c28facba3deb00d76f186e23`.

Passed:

- `python3.11` AST/`py_compile` for both assigned test files, compiling to a private `/tmp` output directory.
- `/home/user/work/venv-agent/bin/ruff check --no-cache tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py` — `All checks passed!`
- `make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python` — `Mypy findings: current=1902 baseline=1902`; baseline passed.
- `git diff --check`.

Known baseline:

- Ruff on the unchanged parent test reports pre-existing `F811` for the duplicate unused `RemoteTimelines` import at line 226. The parent file hash is unchanged.
- The first mypy environment (`/home/user/work/venv-agent/bin/python`) could not check because its installed stubs/dependency versions are incompatible; the documented typecheck environment passed with no regression.

Targeted behavior:

- Parent cohort file: `1 passed, 24 errors in 23.2s`; every exact parent24 cohort case errors during readonly shared setup at `occurrence_media.py:93` with `CommandError: replacement changes provider-managed edges`.
- Manifest inverse file: `2 errors` (`[add]`, `[swap]`), both at the same readonly shared setup boundary. The previous missing-required-arguments error is no longer present.

No full, family, browser, render, collector, Store, child, D130, or other prohibited suite was run.
