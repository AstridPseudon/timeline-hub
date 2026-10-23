# G3/R2 schema-fixture restoration review — PASS

Reviewed exact source tree `44ea025712c53339d78c05919d7de6996efcb1be` (`tl/agt-G3-schema-fixtures-0321`) against base `425ab45946b1436d8f1ad02c065be5e2a788d9b5` and approved independent correction `f2521256c2f705d7ba8a8e9a4d27fce02b5bc2cc`.

Both modified test files match f252 byte-for-byte:

- `tests/sdk/test_timeline_current_union_schema.py`: `d2225bf268ad33073b725eec9fdb9fb184ae4c50`
- `tests/sdk/test_timeline_composed_schema.py`: `14f0953375541c81be4e68b3b40c09319eed5bc0`

Only those two paths differ from base. The canonical schema is unchanged and has SHA-256 `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d` at both HEAD and base. No product/generated/client/pin/lock/historical-fixture changes occurred. This is approved test-floor restoration for the original G3 resolution, not a new contract or feature; the production caller and Runtime corrected-envelope producer remain separate ownership.

The restored controls remove only the approved optional `InverseArgs.steps` shape when reconstructing historical floors; exact current-shape, closed-args, unknown-argument, inverse whole/selected positive, malformed inverse, and operation inventory assertions remain active. The census receives only a minimal valid `doc.patch` sample, so `doc.patch` and `timeline.inverse.steps` remain closed and valid.

Evidence:

- Two schema files: **41 passed** in 163.79s.
- Focused inverse/G3 compound/parent-media compound lane: **3 passed** in 2.34s.
- Scoped Ruff: **passed**.
- Private mypy: **Success: no issues found in 2 source files**.
- `git diff --check`: **passed**.

No full/browser/farm/native14/P4HTTP/live-socket or dependency-write checks were run. No blocker found.

