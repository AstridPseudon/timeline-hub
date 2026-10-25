## Completed

- Added three D108 snapshot predicates in [tests/test_timeline_render_publication.py](/home/user/work/wt/rt-F-D108-snapshot-coverage-0813/tests/test_timeline_render_publication.py:280):
  - authored `config` equality;
  - authored `registry` equality;
  - durable payload/digest binding to the canonical render task.
- Preserved all existing assertions and production routes.
- Created `DONE` and conventional commit message.

## Verification

- `20 passed`:
  `ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH="$PWD/tests:$PWD/packages/python" python -m pytest -q tests/test_timeline_render_publication.py tests/test_timeline_render_publication_authority.py`
- Ruff: passed.
- Python compile: passed.
- Scoped mypy: passed.
- `git diff --check`: passed.

No blockers. Full suites were not run per instructions.