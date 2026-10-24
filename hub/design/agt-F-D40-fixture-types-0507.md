Implemented F-D40 typing fix in [external_orchestrator_owner.py](/home/user/work/wt/agt-F-D40-fixture-types-0507/tests/helpers/external_orchestrator_owner.py).

- Added explicit `str`/non-empty origin guards before all three `Path(...)` calls.
- Missing origins now fail closed with `AssertionError`.
- Preserved fixture hashes, direct URL/marker/symlink/origin checks, `tests.__path__`, caller behavior, and fixture assertions.
- Traced caller: `tests/stage1/test_zero_shim_execution_pack_deletion.py`.

Checks:

- Private mypy: PASS, no issues.
- Ruff: PASS.
- `py_compile`: PASS.
- `git diff --check`: PASS.
- No original positive, subprocess, or installed-body tests run per brief.

Deferred actual before/after origin-map and `imported_from` qualification remains for the integrated worker. Commit message and `DONE` marker created.