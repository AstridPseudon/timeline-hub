# D116/G3 source-only validation

Source outcome: PASS for the scoped setup correction. Behavior outcome: UNRUN by policy.

Commands and results:

```text
PYTHONPYCACHEPREFIX=/tmp/w-e346d4f9cb/app-D116-native-gate3-setup-1756/pycache python3.11 AST/compile: PASS
RUFF_CACHE_DIR=/tmp/w-e346d4f9cb/app-D116-native-gate3-setup-1756/ruff-cache /home/user/work/venv-agent/bin/ruff check tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py: PASS
/home/user/work/venv-agent/bin/mypy --cache-dir /tmp/w-e346d4f9cb/app-D116-native-gate3-setup-1756/mypy-cache --config-file pyproject.toml tests/editing_conformance/native_checkout_current_fixture.py: PASS
git diff --check: PASS
```

Static scope limitations:

- No pytest, test collection, native original, full/family/P4/P2/profile-body run, socket, browser, service, or behavior execution was performed.
- The protected review required before any later Gate3 behavior node is not performed by this worker and remains a prerequisite.
- The requested worker `tmpdir` path was a regular file in the harness; private caches were placed under `/tmp/w-e346d4f9cb/app-D116-native-gate3-setup-1756/` instead.
- No behavior or retirement credit is claimed.
