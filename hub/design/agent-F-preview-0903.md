# Agent F — R1 preview exact-context oracle

Status: bounded slice complete; exact node passes. This is a test-oracle correction, not a production defect.

The direct recipe plan was context-free. The existing provider executor is `commands.execute` with the authenticated request and evaluated head, and therefore emits the C0-required physical `commit.input` binding for the changed intermediate image at command ordinal 2. The test now constructs the expected plan through that same executor/context and retains exact complete-record equality. It does not drop bindings or use a subset comparison.

Changed file: `tests/editing_conformance/test_producer_insertion.py` only. No `_commit_patch.py`, `inverse.py`, Runtime source, generated files, pins, dependencies, or shared environment changed.

Evidence:

- Exact named test, both variants: `2 passed in 11.49s`.
- Focused producer guards: `2 passed in 17.24s`.
- `make ruff PY=/home/user/work/venv-agent/bin/python`: PASS, `2149/2149`.
- Vendor lock: PASS.
- Artifact manifest: PASS.
- `git diff --check`: PASS.
- Mypy baseline command: bounded 45-second retry exited `124` without a count; unverified.

Limits: no full or browser/live-socket suite, P1/P4 HTTP, native14, crash24, heavy journey, or duplicate run. No positive-to-refusal conversion, skip/xfail, baseline increase, synthetic authority, or accept/write behavior change.

Remaining owners are the prior R2 three net-zero recorder cases, V2 scalar and graph fixture cases, V3 Composition adoption mismatch, and the separate Runtime inverse stage-authentication issue. Current source-backed classification does not establish integration causality or upstream-431 status.
