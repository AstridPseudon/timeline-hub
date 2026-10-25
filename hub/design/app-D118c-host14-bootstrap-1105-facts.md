# D118c host-bootstrap14 facts

- Genuine validator evidence identifies `PYTHONNOUSERSITE` in `_UNSUPPORTED_PYTHON_STARTUP` and rejects it in `probe_context()`.
- `astrid/sdk/host_bootstrap.py` now removes only that proven inherited startup override from the copied child environment. `NODE_OPTIONS` and `PYTHONHOME` remain strict validator refusals, preserving the protected boundary.
- Required `ASTRID_REMOTION_PROJECT_DIR`, `ASTRID_NODE_EXECUTABLE`, and `ASTRID_TIMELINE_SCHEMA_PYTHONPATH` values are retained by the additive actual-callable regression.
- Caller `os.environ` remains unchanged; the child mapping is sanitized.
- Protected `tests/sdk/test_host_bootstrap_source_identity.py` is byteexact against the parent, SHA256 `08dfa8dcafeb80c347923630864a29d58dea97e257428e204fc316567795161b`; the two target functions retain 16 assertions in both parent and current ASTs.
- Targeted additive tests: `3 passed`.
- Ruff, mypy (`--follow-imports=skip`), py_compile, and `git diff --check` passed for changed files.
- The protected 14-node selector was not run: this worker had no genuine local Remotion profile/environment, and no substitute was used.
