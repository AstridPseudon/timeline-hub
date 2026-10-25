## Result

Blocked by an out-of-scope Runtime defect. Only the assigned test file changed.

Changes:
- Registered the genuine provider before timeline bootstrap.
- Added the required v2 caller envelope fields.

Tests:

- Retained nodes: `3 failed in 32.96s`
  - scalar/compound: Runtime `timeline_commit_auth.py:1607`
  - separate: Runtime `timeline_commit_auth.py:1755`
- Public caller: `1 passed in 2.72s`
- Ruff, mypy, py_compile, and `git diff --check`: passed.

Runtime receipt verified clean:

`42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`.

Evidence, commit message, and `BLOCKED` marker are in the worker directory. No production/runtime changes were made.