# D116 first-return validation

Source-only checks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/d116-native-topology-first-return-1700-py311 /usr/bin/python3.11 -m py_compile tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS (exit 0)

PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/d116-native-topology-first-return-1700-py /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS (exit 0)

/home/user/work/venv-agent/bin/ruff check --cache-dir /tmp/d116-native-topology-first-return-1700-ruff tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS: All checks passed!

/home/user/work/venv-agent/bin/mypy --cache-dir /tmp/d116-native-topology-first-return-1700-mypy --follow-imports=skip tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS: Success: no issues found in 2 source files

git diff --check
PASS (exit 0)
```

Collection:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider --rootdir=. tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS: 4 tests collected in 0.70s
```

Runtime pin custody: `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree
`de2954a0ceadb4455903d9abdfec3b773318a50f`; Runtime worktree clean.

Functional NEW4: **NOT RUN**, because the brief requires an independent source-pass
review before any functional run.
