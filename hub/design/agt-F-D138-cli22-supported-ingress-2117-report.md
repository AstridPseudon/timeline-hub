## Report

- Migrated the root-045 test caller to genuine `TimelineSession.commit_many(..., via="cli")`.
- Preserved authored inputs, guards, pins, retries, metadata, refusal predicates, and file bytes.
- Parser-only retired CLI test remains unchanged and visibly failing.
- Partition: migrated 22 / legacy-only 0 / stopped 0.

Validation:

- Python 3.11 AST/compile: pass.
- Ruff: `2143/2143`, pass.
- Mypy: `1902/1902`, pass.
- `git diff --check`: pass.
- Central exact-22 run collected all cases but deselected them due the integration lane; behavioral results remain unverified.

Only `tests/editing_conformance/test_native_batch_ingress.py` changed. Evidence and commit message are in the assigned worker paths; `DONE` created.