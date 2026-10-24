Implemented the fixture correction in [test_timeline_public_command.py](/home/user/work/wt/agt-F-public-source-return-1130/tests/sdk/test_timeline_public_command.py).

- `pair`/`foreign`/`digest` now use a fresh `timeline.open`; `outside`/`previous` retain `opened.command`.
- Preserved mutations, exception handling, assertions, and all other test bodies.
- Exact-five tests: **5 passed**
- Whole file: **10 passed**
- Ruff: **passed**
- Qualified mypy: **passed**
- `git diff --check`: **passed**
- Independent AST/no-weakening review: **passed**
- No production/API changes; no blockers.
- Commit message and `DONE` marker created.