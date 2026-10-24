Implemented G4 media admission in `Checkout.publish()`.

- Added canonical `media.admit` inputs from compiled candidate media and Runtime catalog lookups.
- Preserved existing command ordinals, steps, reads, retries, receipts, and history behavior.
- Added focused accepted/retry and foreign-media no-write regressions.
- No fixture, `authoring_commit.py`, Runtime, schema, or generated-file changes.

Tests:

- Targeted acceptance: **20 passed**
- Ruff: **passed**
- Vendor lock: **passed**
- Artifact manifest: **passed**
- `git diff --check`: **passed**
- `make mypy`: blocked by pre-existing missing YAML stubs and incompatible NumPy stubs.

No full/browser suites run. Completion marker and commit message were written.