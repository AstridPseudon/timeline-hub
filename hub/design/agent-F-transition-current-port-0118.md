## Report

Ported cumulative `070c9ef7e → 7bcb6f4ca` into the current integration head.

- Lazy catalog loading occurs only when any transition key exists.
- Catalog loads once before grouping/sorting.
- Added both precedence regression tests.
- Source and test are byte-identical to `7bcb6f4ca`.
- Only the two assigned files changed; current unrelated hunks preserved.

Tests/checks:

- Exact author lane: `116 passed`.
- Differential counterexamples: old `ValueError/OK`; current catalog-integrity `RuntimeError` for both.
- Touched Ruff: passed.
- Mypy: `1911` diagnostics, expected baseline; no new path/message/code identities.
- Vendor lock: passed.
- Artifact manifest: passed.
- `git diff --check`: passed.
- Full suite/prohibited integration runs: not run.

Note: repository Ruff baseline reports current `2147` vs baseline `2148`, an unrelated pre-existing improvement. No new review was requested because this was an exact conflict-free port. Commit message and `DONE` marker written; harness will commit.