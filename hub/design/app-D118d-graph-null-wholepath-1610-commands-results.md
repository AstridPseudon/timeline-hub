# D118d commands and results

All repository inspection was read-only. No pytest, own9, live/socket/native/browser/full/family/P2/P4/acquisition/collector command was run.

| Command | Result |
|---|---|
| git status --short --branch | Clean worktree at tl/app-D118d-graph-null-wholepath-1610. |
| git diff --unified=25 94ac9347^ 94ac9347 -- tests/sdk/test_timeline_commit_graph_roots.py | Six insertions and zero deletions: v2 request-envelope fields only. |
| Source-only AST/hash comparison of candidate vs parent/normal graph test | 11 tests, 33 assertions, 7 parametrizations in each; normalized test AST and RuntimeRealm.__init__ AST hashes identical; only 6/0 source diff. |
| Source-only authored/compiler/schema/producer probe | PASS: authored-null, compiler-pass-through, public-number-schema, C0-null rule, and numeric passing producer all matched source. |
| PATH=/home/user/work/venv-agent/bin:$PATH ruff check tests/sdk/test_timeline_commit_graph_roots.py | All checks passed! |
| mypy --cache-dir <private worker cache> --follow-imports=skip tests/sdk/test_timeline_commit_graph_roots.py | Success: no issues found in 1 source file |
| PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tests/sdk/test_timeline_commit_graph_roots.py | Exit 0. |
| git diff --check | Passed. |
| git status --short | Empty after static checks; no product/source changes. |

The prior protected review’s own9 result was inspected, not rerun: it failed before assertions because PreparedCommit.canonical_document.parent_revision.payload.occurrences[2].gain was None while a number was required. This review independently confirms the source seam behind that result.
