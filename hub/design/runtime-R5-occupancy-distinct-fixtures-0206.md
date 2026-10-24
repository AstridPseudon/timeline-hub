## Report

Implemented fixture-only changes in `tests/test_timeline_legacy_occupancy.py`:

- Restored exact HTTP `code/message/details` refusal checks.
- Added SQL dump, CAS/head, owner, item, and receipt no-write invariants.
- Distinguished retained `shot-revision:` versus new `shot:` missing-head inputs.
- Left historical-reuse cases unchanged/held.
- No product, schema, client, or guard changes.

Checks:

- Targeted pytest: `3 passed in 8.03s`
- Ruff: passed
- Pyright: 0 final diagnostics; 0 new identities/multiplicities versus original baseline
- AST mapping/assertion check: passed
- `git diff --check`: passed

`--net` is unsupported by this repository’s pytest configuration; reran without it, with HTTP daemon coverage active.

Commit message written and `DONE` created.