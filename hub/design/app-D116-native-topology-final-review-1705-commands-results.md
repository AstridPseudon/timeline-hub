# D116 final review commands

## Source and custody

```text
git diff --stat 9350a674a85b9328e7ac1e8192e66dcc65cfbf77 HEAD
PASS: exactly the two authorized new files

git diff --stat b24d99bd3c286336c09d4d0661e9691d3b160559 HEAD
PASS: 2 files, 13 insertions(+), 3 deletions(-); distinct suffix key and separate music/music-other topology

git status --porcelain=v1
PASS: empty

git diff --check 9350a674a85b9328e7ac1e8192e66dcc65cfbf77 HEAD
PASS

Runtime 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344
PASS: tree de2954a0ceadb4455903d9abdfec3b773318a50f; Runtime worktree clean

sha256sum of all eight protected original files
PASS: all match source-custody.json
```

## Scoped static checks

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/d116-native-topology-final-review-1705/py311 /usr/bin/python3.11 -m py_compile tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS (exit 0)

PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/d116-native-topology-final-review-1705/py /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS (exit 0)

/home/user/work/venv-agent/bin/ruff check --cache-dir /tmp/d116-native-topology-final-review-1705/ruff tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS: All checks passed!

/home/user/work/venv-agent/bin/mypy --cache-dir /tmp/d116-native-topology-final-review-1705/mypy --follow-imports=skip tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS: Success: no issues found in 2 source files
```

## Collection and functional gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider --rootdir=. tests/editing_conformance/test_native_checkout_current_equivalent.py
PASS: exactly 4 new tests collected

df -B1 --output=source,avail,target . /tmp
AVAILABLE: 4876791808 bytes
FLOOR: 5000000000 bytes
SHORTFALL: 123208192 bytes
FUNCTIONAL NEW4: NOT RUN; source passed but fresh light space was below the required floor
```

No central request was submitted, and no functional body, original node, broader suite, collector, profile, browser, native, service, or full run was executed.
