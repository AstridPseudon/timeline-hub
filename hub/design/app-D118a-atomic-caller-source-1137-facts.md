# D118a facts

Applied one production-only caller repair in `astrid/packs/rendering/docs/scripts/timeline_document.py`: the detached document publisher now uses `TimelineSession._capture_bundle(session_state)`. That existing private session seam calls the authenticated exact revision/publication `fetch_bundle` and retains `_runtime_document` for the emitter; caller-visible `_bundle` privacy remains unchanged.

Qualified Runtime: commit `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, clean.

Evidence:

- Original node passed unchanged: `1 passed in 2.68s`.
- Existing private-pair source/no-write set passed: `4 passed in 19.52s`.
- Ruff, mypy with `--follow-imports=skip`, private-cache `py_compile`, and `git diff --check` passed.
- Original test SHA256 is unchanged and its AST is equal to the base AST.
- Worktree change is exactly one product file, one line changed; no test changes.
