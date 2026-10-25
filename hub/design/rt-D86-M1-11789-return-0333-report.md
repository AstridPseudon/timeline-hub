## Report

- Inspected PLAN, genuine fixture pins, capture/bootstrap source, and actual F-D86 logs.
- No source changes made: the failure is outside the permitted test file.
- Confirmed genuine binding data: transcript `word-1`, historical `elementRef`, binding/media IDs, and preserved opaque graph.
- Blocker: Agent validation rejects supported `timeline.duplicate` birth against the empty bootstrap baseline at `astrid/sdk/timeline/validation.py::_validate_element_reference`.
- D87 frontend6 transitively shares `m1.film`; no D87 behavior claim made.

Checks passed:

- In-memory AST/compile
- Ruff scoped check
- Mypy scoped check
- `git diff --check`

No pytest or fixture execution run. `BLOCKED` and commit message were recorded. Recommended next step: Agent owner fix the duplicate/bootstrap validation seam, then rerun M1 and dependent D87 tests.