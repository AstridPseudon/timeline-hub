## Report

Changed only `tests/timeline/test_authoring_media.py`:

- Qualified current Runtime checkout: `rt-pin-8ea0766f`.
- Limited archived Runtime lookup to the film fixture helper.
- Removed archived commit pins from both daemon starts.
- Preserved all 52 assertions and non-setup AST exactly.
- Did not edit the first publication test.

Checks:

- Non-integration tests: `74 passed, 2 deselected`
- Collection: `76 tests collected`
- Ruff: passed
- Mypy baseline: `1911/1911`
- Vendor lock: passed
- Artifact manifest: current
- Import-origin probe: qualified Runtime remained active after archived fixture import
- `git diff --check`: passed

The live integration body was intentionally not executed per task instructions, so daemon runtime behavior remains unverified end-to-end. Commit message and `DONE` marker are ready.