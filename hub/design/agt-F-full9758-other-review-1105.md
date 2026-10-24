# FAIL — F9758 non-core cause review

- Traceback custody is inconsistent: the exact census retains tracebacks for only 55/171 assigned failures; 116 have none. This conflicts with the candidate’s claim of 231 traceback sections.
- The 29 “product” rows are not accepted. The evidence has no production-caller proof. At least the `_Writer`/`_runtime_document` TypeError/KeyError rows, nested `failed_execution` TypeError, and `StaleWriter` AttributeError are test-double failures, not production defects.
- 18 rows labeled environment have domain failures (missing identity/source, inverse-stage mismatch, or missing word bindings). Runtime-import restoration is not a valid next action for them; reclassify as fixture/provider input or leave unknown.
- The manifest says ba55 is unavailable, but `ba55ac1e9e...` is present and its tree is exactly `c13d368...`. Current c2b is tree `1a5cd...`; this is corrected in the verdict only.

Validated:

- 171 assigned rows exactly match the 231 failed census nodes minus 60 reserved-core nodes; 45 errors are excluded.
- JSONL/CSV parity, JSON syntax, source/tree hashes, and `git diff --check`: PASS.
- All 171 test files are identical between c13 and c2b. c13→c2b changes only `_commit_patch.py`, `inverse.py`, six WC6 test/helper files, and documentation/baseline files.
- Read `PLAN §3`, BOARD-HEADER, and `commit-v2.md §§1–5`; required v2 request/reply/undo/history fields remain present. No contract changes made.

No product tests, full/gate suite, source edits, or data rewrites were performed. Product type/lint: N/A.

Commit message and `DONE` marker created.