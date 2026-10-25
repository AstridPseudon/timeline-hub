# D116 validation

## Source admission

- Agent base: `9350a674a85b9328e7ac1e8192e66dcc65cfbf77`.
- Runtime pin checked: `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`.
- Original native-checkout/frontends/current-word/native-anchor source hashes match the reviewed map; originals were not edited.
- The new fixture uses the registered current provider/pin/anchor seam and the document emitter for the exact `music-bed`/`music-other` media, timing, and opaque topology.
- No product, Runtime, generated, pin, CLI, shared fixture, history, or original-selector changes.

## Static checks

All passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-1195e73128-d116-pycache /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
/home/user/work/venv-agent/bin/ruff check --cache-dir /tmp/w-1195e73128-d116-ruff tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
/home/user/work/venv-agent/bin/mypy --cache-dir /tmp/w-1195e73128-d116-mypy --follow-imports=skip tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py
git diff --check
```

Collection with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6` collected exactly four new cases.

## Functional status

`NOTRUN`: local free space was `4,926,201,856` bytes, below the required fresh light-admission floor of 5 GB. No local functional bypass was attempted.

The central targeted request for the new test file also did not execute the cases: its isolated checkout failed during conftest import with `ModuleNotFoundError: No module named 'runtime_protocol'`. It reported exit 4 before collection.
