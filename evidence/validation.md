# D134 review validation

## Independent read-only checks

- `git -C /home/user/peteromallet/astrid-agent show tl/agt-F-D134-media48-2016:tests/editing_conformance/test_commit_runtime_occurrence_media.py | sha256sum` — PASS; `cf73444ebe59c7a5e62f29cff072d3c3dea87ead85043d92ef632d433cb110a1`.
- AST parse and `compile()` of the exact Git-show source using `/home/user/work/venv-agent/bin/python` — PASS.
- `git diff --name-status a30e74e901a28b39c28facba3deb00d76f186e23^ a30e74e901a28b39c28facba3deb00d76f186e23` — PASS for the no-D134-delta claim; only the two graph-root test files changed.
- Byte comparison of author evidence to permanent `design/agt-F-D134-media48-2016-*` copies — PASS for `source-manifest.json`, `predicate-map.json`, `setup-proof.md`, `validation.md`, and `outcomes.json`.
- Current Agent `tl/integration` equals the author D134 ref — PASS; both resolve to `a30e74e901a28b39c28facba3deb00d76f186e23`.
- Current Agent `tl/integration` `_command_state.py` differs from held D100 product source — PASS; this confirms the D100 boundary is not currently applied.
- JSON parsing of all review evidence JSON — PASS.

## Author checks observed, not repeated

- `PYTHONPYCACHEPREFIX=/tmp/w-bc995b7564/agt-F-D134-media48-pycache /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/test_commit_runtime_occurrence_media.py` — author reported PASS.
- `ruff check tests/editing_conformance/test_commit_runtime_occurrence_media.py` — author reported PASS; Ruff `0.16.9` is installed in the current environment.
- `/home/user/work/venv-agent/bin/mypy tests/editing_conformance/test_commit_runtime_occurrence_media.py` — author reported PASS; mypy `1.17.0` is installed in the current environment.
- `git diff --check` and clean author status — author reported PASS.
- Targeted author command: `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=/home/user/work/runtime:. /home/user/work/venv-agent/bin/python -m pytest -m integration -q tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-add] --tb=short` — author reported the expected setup refusal `shot item correspondence changed` before the behavior body.

## Qualification limits

The targeted command used the mutable `/home/user/work/runtime` path; it did not bind a qualified immutable `ab1e4f6...` receipt. That checkout is now `e319fdbd` / tree `d5cb9335`, so the historical result is not current-runtime qualification. The D100 Agent behavior lane was not run; App currentproof1939 own9 had 9 setup errors and projection acceptance was not run. No unchanged provider/test-body retry, full suite, family suite, or D134 body acquisition was performed.
