## Report

Implemented the test-only migration in [test_capture_closure_source.py](/home/user/work/wt/agt-F-capture-closure-fixture-0015/tests/sdk/test_capture_closure_source.py:140).

- Replaced the fake Runtime task double with the existing real Runtime closure fixture.
- Preserved both original saved and candidate post-admission assertions.
- Added only the local generator/context-manager and task-shape adapter required by the current fixture.
- No production, schema, pin, or Runtime files changed.

Tests/checks:

- Original two positives: `2 passed`
- Inline boundary plus Runtime controls: `12 passed`
- Full touched test file: `28 passed`
- Ruff: passed
- Private mypy baseline: `1911 = 1911`
- Normal Ruff baseline: `2148 = 2148`
- Artifact manifest, vendor lock, and `git diff --check`: passed

Producer-qualified vendor check reports the expected frozen-pin mismatch (`34eac004` lock vs mandated `8ea0766f` test Runtime); no pin was changed.

Module origins were verified against this Agent worktree, the `8ea0766f` Runtime checkout, and the shared schema environment. Commit message and `DONE` marker were written.