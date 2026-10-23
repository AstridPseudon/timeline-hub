## A4 report

Added one self-contained test: [test_a4_after_positive_doc_patch_witness.py](/home/user/work/wt/agt-A4-after-positive-docpatch-2057/tests/editing_conformance/test_a4_after_positive_doc_patch_witness.py).

It preserves all four reviewed App requests, canonical bases, source pins, production caller binding, exact request lengths/SHA-256 values, immutability checks, and intended positive-field assertions. No product or existing tests changed.

Results:

- Combined targeted tests: `4 failed, 16 passed`
  - Existing track/transcript witnesses: passed.
  - New cases fail at the registered provider with `dependency_changed`: prepared media is outside Runtime-verified inputs.
- Ruff: passed.
- Mypy: passed.
- Vendor lock: passed.
- Artifact manifest: passed.
- `git diff --check`: passed.
- Only changed identity: the single new test file.
- New test SHA-256: `46f5752f351cd0b7463393391484ece1ebd61f36d6d52891f6cd3e3bd9dfbdb3`.

Request hashes:

- Missing hold: `38afc047…c66c738a1`
- Explicit null hold: `a422aaf9…e268269f1`
- Subminimum: `99cf8093…603f17f5`
- Incoming transition: `e1f05b38…35f602825`

Blocked marker written. No product workaround or fabricated authority was added.