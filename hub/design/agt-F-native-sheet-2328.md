## PASS_SOURCE

Changed only `tests/editing_conformance/test_native_sheet_ordinary_runtime.py`.

- Migrated fixture setup to current `RuntimeService` bootstrap, native capture commands, and `commit_timeline` provider.
- Removed subprocess/frozen-runtime migration, direct SQL, and legacy publication setup.
- Preserved all assigned test bodies, decorators, parameters, assertions, and 11 selectors exactly.

Source hashes:

- Baseline: `e001ccb91bc88807e77a86e753ff90713698b5ad85e2c4811398f61df112cad4`
- Candidate: `6b271dd5b1069cd8aeb7617f13195fe265d6e43174705fa3bb7d1cb9da4660d9`

AST map: all 7 containing test functions are exact; assigned expansions are `2 + 1 + 1 + 1 + 1 + 1 + 4 = 11`.

Checks passed:

- `python3 -m py_compile ...`
- Ruff baseline and candidate
- mypy baseline and candidate
- `git diff --check`

No pytest, functional suite, or test-service run per instruction. Functional acceptance remains for the manager-owned batched rerun.

Commit message written and `DONE` created. Protected review is the next step before merge.