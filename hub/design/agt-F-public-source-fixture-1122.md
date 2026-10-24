## Report

No code changes made. The task is blocked; `BLOCKED` marker and commit message were written.

Diagnosis: `timeline.open()` authenticates and caches `_runtime_document`. Therefore, post-open pair/foreign/digest mutations do not affect `opened.command()`. Moving mutations before `timeline.open()` makes open refuse before the original command oracle runs. Cache manipulation, fake lazy readers, product changes, or weakened assertions are forbidden.

Tests (`--timeout=45`; installed pytest rejects `--timeout45`):

- Source guards: pair/foreign/digest **failed**, outside/previous **passed**
- Whole file: **7 passed, 3 failed**
- Ruff: **passed**
- Qualified mypy: **passed**
- `git diff --check`: **passed**
- Worktree: clean

Target file hash unchanged: `4aef3b6e80337872e346b87769f3664a9d75019c76ab77baecb28c3effc00842`.

Next step requires an orchestrator decision on whether to migrate the three cases to fresh-open refusal semantics or revise the production/test boundary.