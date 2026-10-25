## PASS

- Candidate diff against `e9e3b8f...`: exactly two lines in `tests/editing_conformance/test_native_sheet_current_runtime.py`.
- Both correct `verified['object_id']` to `verified['selection']['object_id']` at lines 123 and 340.
- Compared with `070dfc5ef`: identical outside those two lines.
- AST assertion nodes: 248 before and after; identical.
- Runtime `selected()` returns `object_id` nested under `selection`.
- Agent assembly caller validates `verified['selection']`; no invented records, IDs, fixture values, intervals, opaque data, parent/undo/no-write predicates, or identities.
- `git diff --check`: passed.
- Candidate status: only the expected test file modified.
- No service, browser, or full tests run per instruction.
- Created required `DONE` marker.