## Report

- Restored only the separately retired parameter CLI function to its exact original `commands-file` implementation.
- Preserved provider-backed fixtures and all six live selectors/assertions.
- Held base recorded: `95fe9d2e90913bb1ff0b8c5979b372fa87c34ef1`.
- Changed only `tests/editing_conformance/test_commit_runtime_native_checkout.py`; frontends file unchanged.

Checks:

- AST parse/in-memory compile: PASS.
- Exact original-function comparison: PASS.
- Ruff baseline and candidate: PASS.
- Mypy baseline and candidate: PASS.
- `git diff --check`: PASS.
- Pytest, collection, runtime/service/browser/build execution: not run per brief.

Commit message written and `DONE` marker created. Next step: fresh protected review, then normal Agent merge queue and later integrated functional proof.