## Report

Implemented the two admission-hole fixes in the allowed component/test files:

- Rejects all caller-supplied additional wheels until independent authority exists.
- Recursively authenticates the full schema subtree, including ignored files/directories, symlinks, ownership, modes, hashes, and selected commit/tree binding.
- Added adversarial tests for forged wheels, ignored links/files/directories, and tree mismatch.

Tests/checks:

- Required pytest: **17 passed**
- Ruff: **passed**
- Normalized mypy: **passed**
- Plain mypy: only missing `pytest` stub
- Compile and `git diff --check`: **passed**

No full suite run. Authentic schema custody remains unverified because the pinned source is unavailable after the documented HTTP403/access refusal; no acquisition or reconstruction was attempted. Commit message and `DONE` marker were written.