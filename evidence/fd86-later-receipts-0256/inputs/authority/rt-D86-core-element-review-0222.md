## F-D86 protected review — PASS_SOURCE

Reviewed actual HEAD `f643a5e12a` against author base `8dadab251a9b9c1a0d31655125d62338f1ee4482`.

Only change:

- [`tests/core/test_timeline_element_publication_runtime.py:605`](/home/user/work/wt/rt-D86-core-element-review-0222/tests/core/test_timeline_element_publication_runtime.py:605)
- `rebased` → `merged`
- Base blob: `91b8d15affa7f21f46eef6cfef32a0f30e9d651a`
- Candidate blob: `a46bb9e8ab9e4065064017f674cfd848a30d6265`
- Candidate SHA-256: `f03e19caa0b6505a42d17fc0eaca77a4794fafb863619bdc4876b14bd63b0357`

Source review confirms the v2 producer sends `merge='fields'`; pinned Runtime `a3cd1a3214fa1632879c21d82d1abb9ea720b1de` emits `merged` for non-base modern commits while preserving historical `rebased` receipts and exact retries. All other assertions, inputs, decorators, branches, undo, ABA, and no-write predicates remain unchanged.

`FAIL_SOURCE`: none.

Validation:

- `git diff --check`: PASS
- Ruff baseline and candidate: PASS
- AST conservation and in-memory compilation: PASS
- Agent producer and pinned Runtime source AST/compile: PASS
- Mypy baseline and candidate: identical existing environment diagnostic: missing `types-PyYAML`; no candidate-specific diagnostic

No pytest, collection, fixture/helper execution, services, browsers, builds, or full suites were run.

The separate lost-ACK failure remains open at Runtime’s sequential metadata guard (`timeline_commit_auth.py:2414-2415`); this review claims no closure.

Proposed existing D83 log entry, not written:

`F-D86 core-element protected review: PASS_SOURCE; v2 disjoint landing uses merged, historical rebased retry and separate lost-ACK metadata refusal remain; functional qualification pending MAIN.`

Commit message and empty `DONE` marker were created.