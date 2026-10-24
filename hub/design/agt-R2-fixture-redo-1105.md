Implemented R2 fixture migration in the two requested test helpers only.

- Native redo fixtures now use production compiler/document materialization without effect facts.
- M2 cases use authenticated provider materialization proofs.
- Test bodies/ASTs unchanged; hashes match HEAD.
- No product or Runtime changes.

Validation:

- Targeted six-case pytest: `6 passed`
- Ruff and `make ruff`: passed
- Typecheck-v2 mypy: passed
- `git diff --check`: passed
- JUnit: `evidence/redo.xml`
- No full suite, codec-positive, or ABA tests run.

Independent review/homeproof remains for the orchestrator.