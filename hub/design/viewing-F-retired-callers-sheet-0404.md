## PASS

Updated only [test_native_sheet_current.py](/home/user/work/wt/vw-F-retired-callers-sheet-0404/tests/editing_conformance/test_native_sheet_current.py).

- Preserved all 24 retained scenarios and existing semantic assertions.
- Python permutation now submits explicit v2 `label`, `steps`, `merge`, and `reads`.
- Added validation that all four callers submit complete v2 request structure.
- No product files changed; retired routes were not restored.

Tests/checks:

- `pytest ... test_native_sheet_current.py`: **38 passed**
- Ruff: **passed**
- Mypy: **no issues**
- Vendor lock: **passed**
- Artifact manifest: **current**
- `git diff --check`: **passed**

Module origins: Agent modules resolve from this worktree; Runtime modules from `/home/user/work/runtime`.

The test uses the existing generated transport fixture, so live Runtime acceptance remains unverified here. Commit message and `DONE` marker created.