Implemented U4a-D39 fixture correction in [test_runtime_response_conformance.py](/home/user/work/wt/agt-D39-conflict-fixture-0747/tests/sdk/test_runtime_response_conformance.py).

Changed the scenario to call canonical `commit_timeline` with the exact fixture body and preserved the test name, error assertions, request-body/path checks, and `idempotency_key="k"`.

Tests:

- Conformance file: `18 passed`
- Contract neighbor: `9 passed`
- Ruff: passed
- Compile: passed
- `git diff --check`: passed
- Vendor/lock/generated/artifact diff: unchanged
- Mypy: not applicable; configured only for `astrid` and `scripts/reshape`

Assertion inventory before/after: unchanged—status/code, details/request ID, `ServiceConflictError` mapping, and exact recorded request assertion remain.

Commit message and `DONE` marker written.