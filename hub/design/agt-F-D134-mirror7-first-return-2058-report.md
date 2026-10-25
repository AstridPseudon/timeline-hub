## D134 mirror7 first return

Implemented the source correction in the two authorized test files:

- Restored the real recipe-family `change-echo` Runtime commit, restart, and recapture.
- Re-resolved mirror references after alias assignment.
- Removed global aliasing so protected/unrelated cases retain original topology.

Validation passed:

- Python 3.11 AST and `py_compile`
- Ruff
- Scoped mypy: no issues in 2 files
- `git diff --check`
- JSON evidence validation

Live exact7 qualification is blocked. No admissible central route exists for immutable Runtime `ab1e4f614198…`; the generic route uses mutable Runtime `e319fdb…`. No fallback or unqualified run was performed.

Evidence and `BLOCKED` marker are under the assigned worker directory.