## F-D86 report

Changed only `tests/editing_conformance/test_word_binding_recipe.py`:

- ID6 now asserts registered production `clip.anchor` presence.
- ID8 now expects C0 `status == "invalid"`.
- ID9 remains `status == "refused"`.
- All inputs, predicates, undo/head guards, and equal-text positives remain unchanged.
- Proposed D83 behavior-log entry saved under worker evidence.

Checks:

- AST parse: PASS
- Ruff candidate/parent: PASS
- mypy candidate/parent shadow: PASS
- `git diff --check`: PASS
- Tests/collection/helpers/services: intentionally not run per brief.

No blockers. `DONE` created; commit message written with F-D86 subject.