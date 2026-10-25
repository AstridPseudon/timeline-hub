## Report

- Migrated opaque fixture setup from retired `publish_parent_composition` to genuine registered-provider `doc.patch` commit path in [test_commit_runtime_opaque_items.py](/home/user/work/wt/agt-D86-occurrence-opaque-0121/tests/editing_conformance/test_commit_runtime_opaque_items.py).
- Create/fork tests unchanged; their rehearsal failures are Runtime/product causes.
- Agent HEAD: `219b9ca8…` (tree `9d26efc3…`).
- Runtime harness: `766fd670…`; released source: `a3cd1a32…`; only two capture-test files differ.
- Final target hashes: create `26ecb3e8…`, fork `f9b84bd2…`, opaque `391062bd…`.

Checks:

- AST parse + in-memory compile: PASS.
- Named test/assertion conservation: PASS.
- Scoped Ruff: PASS.
- Ruff baseline: PASS (`2143 = 2143`).
- Mypy baseline: blocked by missing `types-PyYAML` stubs and NumPy/Python target mismatch.
- No pytest, collection, fixture, service, build, or function execution run.
- Diff scope/check: PASS; one allowed file only.

Commit message written: `test(F-D86): migrate opaque baseline to commit path`. `DONE` marker created.

Next: protected review, then normal Agent merge and later functional service qualification.