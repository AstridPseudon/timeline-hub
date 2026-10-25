# D132 report

- Traced the genuine registered Agent provider through capture, document compilation, Runtime port, and frozen `PreparedCommit` validation.
- Confirmed `payload.metadata = null` is authored by the shared fixture, preserved unchanged, and rejected by frozen `ShotPayload.metadata -> OpenMap` validation.
- Omission and `{}` are valid but semantically distinct; explicit null is invalid at this field.
- Audited all shared seed consumers. Proposed fixture/schema seams remain unapplied for manager decision under D104/D120.
- No repository source, test, fixture, assertion, schema, product, generated file, or pin changes.

Checks:

- Whole-repository AST parse: PASS.
- Whole-repository JSON parse: PASS.
- Python 3.11 compileall in worker scratch: PASS.
- `git diff --check`, clean-tree checks: PASS.
- No pytest or own9 rerun.

Evidence: `facts.json`, `source-custody.json`, `commands-results.md`, `verdict.md`. `DONE` and commit message were created.