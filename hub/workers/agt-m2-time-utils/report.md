## Report

Implemented exact time utility relocation:

- Moved seven utilities into `astrid/sdk/timeline/units.py`.
- Preserved all `timeline_editing` and `astrid.sdk` import routes, including private helpers.
- No behavior or tests changed.
- Diff: `+115/-2` in `units.py`, `+9/-108` in `timeline_editing.py`.

Tests:

- `pytest -q tests/test_timeline_editing_helpers.py` — **12 passed**
- Import smoke — **passed**
- Ruff changed-code check — **passed**
- `git diff --check` — **passed**

The requested `tests/sdk/test_timeline_units.py` does not exist; no replacement test was invented. Full suite was not run per instructions.

Two pre-existing unused `element_schema` imports remain in `units.py`; baseline verification confirmed they predate this change.

Both commit message files were written. Retimer deletion remains dependent on later compiler consumer parity and validation gates.