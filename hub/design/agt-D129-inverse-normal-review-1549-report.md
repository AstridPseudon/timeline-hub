## D129 report

Verdict: **PASS for static/source review** of `a0d8398` against `a4e016b`.

- Diff is exactly one additive 135-line test file.
- Ruff: **PASS**
- Python 3.11 compile (`doraise=True`, TMPDIR output): **PASS**
- AST structure/hash: **PASS**; exactly three tests, no skip/xfail/weakening, hash `3edecac0…91551ca`
- `git diff --check`: **PASS**
- Agent source/lock, protected original test, and three genuine Runtime source hashes: **PASS**
- Mypy: **not applicable**; configured only for `astrid`/`scripts`, with no product changes.
- Pytest/full/provider checks: **not run by task scope**.

Static whole-path tracing confirms the Runtime-owned failure at `timeline_commit_auth.py:1764–1765`: grouped inverse removes the occurrence, then re-resolves the earlier child alias against the post-removal image. The ungrouped comparator keeps the occurrence live and is the passing source comparator.

Farm’s earlier Ruff/compile/AST refusal remains historical **NOTRUN** and was not retried. No source changes, fabricated records, or product/release credit were made.

Evidence: [review.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D129-inverse-normal-review-1549/evidence/review.md), [checks.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D129-inverse-normal-review-1549/evidence/checks.json), [source-hashes.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D129-inverse-normal-review-1549/evidence/source-hashes.json).