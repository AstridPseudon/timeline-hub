# D132a/G3 report

- Source review: **PASS**. Exact tree `160c675a2` / `b809955f`; only the two authorized test files differ.
- Verified 90 fixture and 33 graph predicates, all other inputs/consumers, created refs/order, registered `astrid` provider, and clean Runtime `5e9ad1c6` / `de2954a`.
- Ruff, mypy, Python 3.11 compile, import origins, and `git diff --check`: **PASS**.
- Fresh admission space: `5,028,933,632` bytes.
- Exact original graph9: **8 passed, 1 failed in 8.15s**.
- Failure: `invalid_records: provider occurrence alias is outside its boundary` at `runtime_protocol/timeline_commit_auth.py:156`, child-stage inverse/redo node.
- No retry, alternate route, source fix, or speculative correction. Classified as a later Runtime authenticated closure-boundary seam involving `occurrence:new-occ/clip:title`.

Evidence is under the assigned worker `evidence/` directory, with private `own9.xml` and `own9.log`. Commit message includes `D132a`; `DONE` created.