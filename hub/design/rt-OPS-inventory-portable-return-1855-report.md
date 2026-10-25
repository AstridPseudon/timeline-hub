## Report

Implemented the focused portability correction:

- `--check-only` now hashes committed Agent/Runtime blobs against fixture manifest hashes.
- Missing/malformed fixture sources accumulate with all other prerequisites without uncaught aborts.
- Added private mocked census tests for altered committed bytes and simultaneous missing inputs.
- Preserved immutable maker bytes and EOF whitespace.
- Corrected receiving invocation to pass the bootstrap artifact during venue preparation.

Validation:

- Targeted custody/inventory/new census tests: **42 passed**
- `py_compile`, AST, Ruff, additive Pyright: **passed**
- Scoped diff check: **passed**
- Raw historical diff check: **exit 2**, only the two known immutable maker EOF diagnostics.
- Whole-maker E2E: **not run**; available space `4,717,395,968` bytes is below the `5,905,580,032` reserve.

Validated SHA/tree: `674d13e26ce40ce9a158a7e50b226c247fbc9588` / `f2abd214b4b45fa4a6b6de0932ad5371e4f3fc4b`  
Runner SHA: `f02fdcca8ad7c9484866b1817bb67272212933c4576d2212c2d163a07edf1c96`

Changed paths only:

- `ops-child-custody/tests/e2e_inventory.py`
- `ops-child-custody/tests/test_e2e_inventory.py`

Durable evidence and commit message were written; `DONE` created.