## Report

Implemented the V2 transition-catalog parity fix.

- Catalog loads once when any transition key exists, before grouping/sorting.
- Non-string-track transition clips still trigger catalog authority.
- Added both requested regression controls; existing tests unchanged.
- Wrote commit message and `DONE` marker.

Tests/checks:

- Targeted pytest: **116 passed**
- Ruff touched files: passed
- Ruff baseline: `current=2148 baseline=2148`
- Runtime lock: passed
- Artifact manifest: passed
- `git diff --check`: passed
- Mypy: pre-existing baseline failure, **1911 errors across 252 files**, none in touched files.

No full suite or unsupported timeline render was run.