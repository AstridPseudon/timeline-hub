## Report

- Updated only `tests/editing_conformance/test_commit_runtime_opaque_items.py`.
- Restored shared physical topology via semantic `occurrence.delete` + `occurrence.place-shared`, then guarded `doc.patch` authored data/order.
- Preserved all test bodies; AST conservation passed.
- Commit message written; `DONE` marker created.

Checks passed:

- In-memory compile
- Ruff baseline and candidate
- Mypy
- `git diff --check`

No pytest collection or execution, fixture/service runs, builds, browsers, or full suites were run per task limits. Functional qualification and independent protected review remain pending.

Source hash: `5ae20ab0a747a16debdd5415516a07f1e6f35118a16a2afdcfbdf1b4716ea770`