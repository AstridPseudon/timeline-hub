## Report

- Updated `tests/timeline/test_authoring_bundle.py` to use the approved trusted v2 seed, provider, and authenticated transport. Retired publication calls removed; assertions and operations preserved.
- No product code or other tests changed.

Checks:

- Targeted pytest: **failed** at existing product boundary: `DocumentPatchError: closure root 'shot-revision:shot-rev-1' has contradictory authoring aliases`.
- Ruff: passed.
- Mypy: passed.
- AST: 11 original target assertions retained; top-level test set unchanged.
- `git diff --check`: passed.

Commit message written and `DONE` marker created. Next step: Agent owner should address shared-alias emission/semantic handling; no guard change was made here.