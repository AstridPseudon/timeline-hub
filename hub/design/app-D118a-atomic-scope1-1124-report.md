# D118a report

Result: **UNAPPLIED / BLOCKED**. No test or production files changed; worktree remains clean and target hash is preserved.

The exact node failed at `astrid/sdk/timeline/emitter.py:271` with missing `'_runtime_document'`. The current caller uses `TimelineSession._bundle()`, which strips that authenticated source image. The supported `fetch_bundle(revision_id, publication_id, client)` producer retains it. This requires an Agent/Runtime owner fix; no test bypass was added.

Checks:

- Exact node: failed, exit 1.
- Ruff: pass.
- Mypy `--follow-imports=skip`: pass.
- External-cache `py_compile`: pass.
- `git diff --check`: pass.

Evidence and handoff facts are under the worker evidence directory. `BLOCKED` and the D118a commit message were written as required.