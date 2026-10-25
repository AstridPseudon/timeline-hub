# D116 protected review commands and results

Source custody:

```text
git show -s --format='%H%n%T%n%P%n%s' 9350a674a85b9328e7ac1e8192e66dcc65cfbf77
PASS: 9350a674a85b9328e7ac1e8192e66dcc65cfbf77, parent 20177e66564f9f91735ed1a11bac821682d60edf

git -C /home/user/work/wt/rt-pin-5e9ad1c6 status --short
PASS: clean

git -C /home/user/work/wt/rt-pin-5e9ad1c6 show -s --format='%H%n%T%n%P%n%s' HEAD
PASS: 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344, parent de2954a0ceadb4455903d9abdfec3b773318a50f

git diff --check
PASS

git status --porcelain=v1
PASS: empty
```

Static checks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/d116-review-pycache311 /usr/bin/python3.11 -m py_compile tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS (exit 0)

PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/d116-review-pycache /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS (exit 0; venv is Python 3.13.16)

/home/user/work/venv-agent/bin/ruff check --cache-dir /tmp/d116-review-ruff tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS: All checks passed!

/home/user/work/venv-agent/bin/mypy --cache-dir /tmp/d116-review-mypy --follow-imports=skip tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS: Success: no issues found in 2 source files
```

Collection only (not functional):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider --rootdir=. tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS: 4 tests collected in 0.63s
```

Functional NEW4 was not run. Source review failed on D116-PREDICATE-001 and D116-TOPOLOGY-002; no central request was submitted and no duplicate central attempt was made.
