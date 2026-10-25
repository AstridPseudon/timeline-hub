# D127c Runtime clean carrier validation

Worktree: `/home/user/work/wt/app-D127c-Runtime-clean-source-2010`

- `/root/.local/bin/ruff check tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — PASS.
- `PYTHONPYCACHEPREFIX=/tmp/app-D127c-Runtime-clean-source-2010/pycache python3.11 -m py_compile tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — PASS.
- `git diff --check e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9` — PASS.
- `git diff --name-only e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9` — exactly the two authorized test paths; outside tracked blobs unchanged.
- Working-tree SHA-256 and Git blob SHA-1 checks against `368f53f4454d5908c86de53d174f0bedcf23781c` — PASS for both files; modes remain `644` / Git `100644`.
- Expected reviewed source tree from `git show -s --format=%T 368f53f4454d5908c86de53d174f0bedcf23781c` — `8d5683702f36034f27ee7f49737665d66dbc2b75`.

The central targeted Runtime result `30318` was reused as directed: `61 passed in 3.62s`. No pytest was rerun or newly requested. No full, browser, live socket, product, App, or activation test was run.

The first compile attempt targeted the harness-provided `tmpdir` path, which is a pre-existing regular file rather than a directory; the successful compile used the private `/tmp/app-D127c-Runtime-clean-source-2010/pycache` path and did not modify the harness file.
