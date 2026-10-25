# D132a protected source review commands and results

- git rev-parse HEAD / git rev-parse HEAD^{tree} — PASS: 160c675a2d58ab9ec2dde7517860075ad85e41d2 / b809955fe54988c2ef092b4379030fdf78a8b06c.
- git diff --name-only 20177e66564f9f91735ed1a11bac821682d60edf -- — PASS: exactly the two authorized test files.
- Independent AST/input/predicate/custody script — PASS: fixture 22/90/6 and graph 11/33/7 bodies/assertions/parametrizations unchanged; exact root-value differences are only metadata null -> {} and gain null -> 1; semantic-reservation and created-root-stage-redo files byte-exact; created refs match handler order; Runtime pin clean and hashes exact.
- Import-origin check with the prescribed Agent/Runtime PYTHONPATH — PASS: Agent modules resolve from this worktree and Runtime modules from rt-pin-5e9ad1c6.
- Ruff on the four touched/neighbouring files — PASS.
- Mypy with private cache on the four touched/neighbouring files — PASS: no issues in 4 source files.
- Python 3.11 py_compile on the four touched/neighbouring files — PASS.
- git diff --check against 20177e66564f9f91735ed1a11bac821682d60edf — PASS.
- Fresh decimal free-space check immediately before admission: 5028933632 bytes — PASS (>= 5000000000, stop threshold 4000000000).

The earlier author result (47 passed; graph9 8 passed, 1 failed in 14.36s) remains unqualified evidence and was not rerun or used as review credit.

- Exact admitted graph9 command with the prescribed Agent/Runtime environment, registered astrid provider, no cache provider, 45-second timeout, JUnit XML, and the nine node IDs from the 1549/1658 facts — RUN ONCE; 8 passed, 1 failed in 8.15s. Raw evidence is private evidence/own9.xml and evidence/own9.log.
- First/only failure: tests/sdk/test_timeline_commit_graph_roots.py::test_authenticated_created_child_stages_reload_inverse_redo_exact_closure; invalid_records, provider occurrence alias is outside its boundary, runtime_protocol/timeline_commit_auth.py:156. The preceding created-claim refusal is cleared.
- Finite source-only comparison of root-only passing versus child-stage failing command execution — PASS as a comparison: created refs and root writes are identical; child stage adds occurrence:new-occ/collection:clip, occurrence:new-occ/clip:title, selection/binding, and child reads/writes. No Runtime or test correction was applied.
