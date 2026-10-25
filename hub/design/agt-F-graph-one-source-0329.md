Implemented the faithful graph-root test setup in [tests/sdk/test_timeline_commit_graph_roots.py](/home/user/work/wt/agt-F-graph-one-source-0329/tests/sdk/test_timeline_commit_graph_roots.py).

- Replaced fabricated history with an authenticated `DetachedRealm.call` acceptance.
- Preserved both root assertions, reservation refusals, and no-write checks.
- No product or other test files changed.
- Root inputs and opaque closure data remain unchanged.

Verification:

- Ruff candidate/parent: passed.
- Mypy candidate/parent: passed.
- In-memory compile: passed.
- `git diff --check`: passed.
- Pytest/service/full suites: not run per instructions.

Independent protected review and MAIN1 remain pending orchestrator handling.