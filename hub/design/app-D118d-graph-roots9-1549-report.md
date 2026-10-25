# D118d report

Updated only [tests/sdk/test_timeline_commit_graph_roots.py](/home/user/work/wt/app-D118d-graph-roots9-1549/tests/sdk/test_timeline_commit_graph_roots.py) to send current v2 `label`, `steps`, `merge`, and `reads` metadata through the genuine Runtime caller. Existing inputs/assertions are preserved.

Checks:

- `py_compile`: PASS
- Ruff: PASS
- mypy: PASS
- `git diff --check`: PASS
- Upstream `924437...` target file: confirmed absent
- Exact nine-node run: NOTRUN; free space was 4,953,280,512 bytes, below the 5,000,000,000-byte floor.

Evidence is in `/tmp/.../evidence/`. Independent protected review remains manager-owned. Commit message and `DONE` marker created.