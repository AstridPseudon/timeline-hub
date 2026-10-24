## Done

Updated [test_generic_host_child_bridge_d18.py](/home/user/work/wt/agt-U2-D18-loader-0803/tests/core/execution/test_generic_host_child_bridge_d18.py:971) to load the selected Runtime client in an isolated real package context, preserving the Agent-vendored client and cleaning all isolated modules afterward.

Tests:

- D18 capacity target: **1 passed**
- Focused regression controls: **5 passed, 2 deselected**
- Collection: **402/607 integration tests collected**
- `compileall`: passed
- `git diff --check`: passed
- Ruff diagnostics: unchanged from `ccf87`; no new diagnostics
- Only the intended test file changed; no generated/vendor/schema/pin changes.

Commit message and `DONE` marker created. No blockers; no full suite run.