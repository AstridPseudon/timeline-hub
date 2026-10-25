# D118d command results

| Check | Result |
|---|---|
| `git status --short --branch` | PASS; clean assigned worktree |
| `git diff --check` | PASS |
| AST parse of inspected Agent fixture/provider/converter files | PASS |
| `PYTHONPYCACHEPREFIX=/tmp/w-11d39d35aa/d118d-identity/pycache python3 -m compileall -q ...` | PASS; 6 private-cache bytecode files |
| JSON parse of retained facts and XML header/structure read | PASS |
| source hash/custody comparison | PASS; projection fixture SHA-256 matches retained reviewed source |
| Runtime pin custody | PASS; commit `5e9ad1c6`, tree `de2954a`, clean |
| retained exact own9 execution | FAIL, pre-existing retained result; exit 1, 9 setup errors, 0 failures, 0 skipped |

Retained own9 exact command and XML/log are in the prior worker’s private evidence. The safe first frame is `tests/sdk/test_timeline_capture_projection.py:311` -> `astrid/sdk/timeline/_command_state.py:369`, with one candidate item row versus zero authenticated expected rows. This worker did not rerun pytest or any body/replay/service suite.

No source, guard, test, generated, schema, dependency, or shared worktree files were modified.
