## Report

- Changed only `tests/editing_conformance/test_recorded_graph_roots.py`: `gain: None` → `gain: 1`.
- Preserved all assertions and other fixture inputs.
- Static checks passed:
  - Ruff
  - mypy with private cache
  - Python 3.11 compilation
  - `git diff --check`
- No pytest or integration suites run, per task scope.
- Evidence written under the requested `evidence/` directory.
- Commit message written; `DONE` marker created.
- Own9 remains for the independent protected reviewer.
- Frozen `d11417a59` object and candidate fixture path were unavailable; neither was treated as proof of absence.