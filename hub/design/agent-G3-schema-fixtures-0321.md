# G3/R2 schema fixture repair — PASS

Against canonical restoration base `425ab45946b1436d8f1ad02c065be5e2a788d9b5`,
restored the approved `f2521256c` test-only expectations in exactly:

- `tests/sdk/test_timeline_current_union_schema.py`
- `tests/sdk/test_timeline_composed_schema.py`

The historical S1/S2 reconstruction now strips only the approved optional
`InverseArgs.steps` addition and asserts that current shape exactly. The
registered-operation inventory receives one minimal valid `doc.patch` sample;
closed canonical args and unknown-argument rejection remain unchanged. The
whole/selected inverse-step positive and malformed-shape checks are restored.

The test blobs match `f2521256c` byte-for-byte. No product/schema/generated/
lock/pin/fixture snapshot changes were made. Canonical schema SHA-256 remains
the required `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`,
matching `425ab4594`, `fc515591b`, `cedc07280`, and `7d3562028`.

Results: the two complete schema files `41 passed`; explicit inverse-schema,
G3 compound, and parent-media compound checks `3 passed`; scoped Ruff passed;
private mypy passed with no issues in two files; `git diff --check` passed.

No full/browser/farm/native14/P4HTTP or dependency-write checks were run.
