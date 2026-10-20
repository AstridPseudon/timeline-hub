## Report

Updated only `tests/core/timeline/test_clip_fields.py`:

- Default `am-type` opacity assertion now expects `renders`.
- Preserved the explicit 0.0.6/0.0.7 matrix and all unsupported/unknown assertions.
- Confirmed receiving Composition is pinned to 0.0.8; capability metadata supports opacity since 0.0.7.

Tests:

- Pytest: `102 passed`
- `git diff --check`: passed
- Ruff: pre-existing `I001` import-order failure at unchanged line 3; not modified due scope restriction.
- Full/network suites not run per instructions.

Commit messages written to both required paths.