# FAIL — D118 sheet15 caller review

- Candidate scope was correct: one modified file, exactly two substitutions at lines 123 and 340.
- `original070dfc` and parent `e9e3b8f...` share the same file blob; all 248 AST assertions and 10 tests are unchanged.
- Runtime `selected()` returns `selection.object_id`, with no top-level `object_id`.
- However, the same verified response is stored in `role_media` at line 339, then incorrectly read as top-level `['object_id']` at lines 345 and 352. The two-line correction therefore leaves a further `KeyError` path.
- Authored IDs, values, intervals, opaque data, parent/undo/no-write predicates, fixtures, product code, and schemas were unchanged. No prepared record or identity was invented.
- The retained `CommitConflict` and `AssertionError` failures remain unmodified/open; no functional tests were run.

Static checks: `git diff --check` passed; AST parse/conservation passed. Service, browser, full, and targeted functional tests were intentionally not run.

Created `DONE` and the required commit message.