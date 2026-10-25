## D118d report

- No additional diff made on candidate `94ac9347b`.
- `gain: null` is authored input at `test_recorded_graph_roots.py:46–51`, not derived setup.
- Genuine caller uses registered `astrid` provider and `RuntimeService.commit_timeline`; Runtime rejects `PreparedCommit` at `occurrences[2].gain` because schema requires a number.
- D104 does not apply; changing the null would alter authored input. D120 permits only bounded static checks.
- Owner handback: Runtime/Agent C0 schema–producer boundary. No behavior GO or retirement claimed.

Checks passed:

- AST/input/assertion/decorator/hash comparison
- Ruff
- mypy (`--follow-imports=skip`)
- Python 3.11 `py_compile`
- `git diff --check`
- Clean git status

No pytest, body, replay, own9, or full suite run per brief. Evidence written to the four required files; `DONE` and commit message created.