# D132a clean-import commands and results

- `git show PLAN.md` — PASS: plan read first; G3 is Agent document-to-`doc.patch` emitter scope, with this task explicitly limited to the two reviewed test blobs.
- `git status --short --branch` before import — PASS: clean assigned worktree on `tl/app-D132a-graph-clean-import-1726`.
- Baseline guard: `git ls-tree 20177e66564f9f91735ed1a11bac821682d60edf -- <two target paths>` versus current HEAD — PASS: both target blobs were unchanged before import.
- Donor custody: `git ls-tree -r b809955fe54988c2ef092b4379030fdf78a8b06c -- <two target paths>` — PASS: expected donor blobs `7309e162…` and `303d076e…`.
- Exact import via editing tool — PASS: only the reviewed donor patch was applied.
- Candidate/donor `cmp` and `git hash-object` — PASS: both candidate files are byte-exact to donor blobs `7309e162c2ef2c1efe95e757c1d8f5c16361cd81` and `303d076e108132d02133171aa77059b565e93e23`.
- Candidate patch versus `20177e6656..160c675a2` donor patch — PASS: exact patch equality.
- Independent AST/input predicate mapping — PASS: fixture 22/90/6 and graph 11/33/7; all test bodies, assertions, and parametrizations AST-equal; created refs and handler order match; two shared consumers byte-exact.
- Outside-tree check — PASS: status contains only the two authorized target paths; `git diff --quiet HEAD -- .` excluding those paths succeeded.
- `/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py` — PASS: all checks passed.
- `MYPY_CACHE_DIR=/tmp/w-10d7c3905f/mypy-cache /home/user/work/venv-agent/bin/mypy --cache-dir /tmp/w-10d7c3905f/mypy-cache <two target paths>` — PASS: no issues found in 2 source files.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-10d7c3905f/pycache /usr/bin/python3.11 -m py_compile <two target paths>` — PASS.
- `git diff --check 20177e66564f9f91735ed1a11bac821682d60edf -- <two target paths>` — PASS.
- Graph9/fixture47/other-consumer behavior tests — NOT RERUN by explicit task instruction; retained independent review result is 8 PASS/1 FAIL in 8.15s on qualified Runtime `5e9ad1c6`.

The retained failure is the authenticated created-child staging inverse/redo case: `invalid_records`, provider occurrence alias outside its boundary, `runtime_protocol/timeline_commit_auth.py:156`. It remains visibly failing and unmodified.
