# U1-D69 Runtime test audit

Completed a read-only audit against:

- Upstream: `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`
  - Tree: `1d3e06f4d59ed6d459646d24ab185c36eb5be075`
- Actual integration: `8b32cacea617c6d45241d7db90b34893a06d3026`
  - Tree: `a095ecbe8b01b0ff0a7825c4c19bbf41120ec3ed`

No product or test files were modified.

Counts:

- Upstream missing test functions: 16
  - 9 mapped/ledgered
  - 7 restore-needed
- Same-name changed test functions: 129
  - 75 cleared adaptations
  - 54 decision-cited
  - 0 restore-needed
- Alternate all-Python-function AST change count: 176
- Removed assertion/raises fingerprints: 88
- Relaxed comparisons: 0
- Dropped parameter cases: 0
- Added skip/xfail flags: 2, both decision-cited
- Current-only dynamic selectors: 12, explicitly bounded as uncertain
- Upstream JavaScript/TypeScript literal selectors: no missing selectors detected

Restore-needed groups:

1. `tests/test_skip_guard.py`: 2 upstream tests.
2. `tests/test_skip_registry.py`: 5 upstream tests.

Both are bounded Runtime restoration groups with preserved upstream body hashes and acceptance command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python -m pytest -q tests/test_skip_guard.py tests/test_skip_registry.py
```

That command was not run per task restrictions.

Evidence and machine-readable inventory:

- `.../evidence/inventory.json`
- `.../evidence/audit-classification.json`
- `.../test_inventory.py`

These contain qualified names, exact source/body hashes, mappings, assertion fingerprints, classifications, and source-file hashes. Same-name body changes were treated as PRESENT/CHANGED, never missing. No test modules or decorators were executed.

Validation:

- Parser compilation: passed.
- `git diff --check HEAD`: passed.
- Full, targeted, browser, live-socket, and product test suites: not run by instruction.
- Worktree remains clean.

The prior “362” census is not reproduced by this exact AST-qualified scope; I retained the stricter lossless classification above rather than counting changed bodies as missing.

Required commit message and `DONE` marker were written.