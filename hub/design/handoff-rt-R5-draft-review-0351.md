## R5 independent review — FAIL

- Draft SHA/tree: `ac115014b01fc2e970c53d588b53432f7306a615` / `da7d10da5014fddb6e0a985da4ff6a4481aef640`
- Changed files: `runtime_protocol/server.py`, `runtime_protocol/service.py`, `tests/test_timeline_legacy_authority.py`
- Six legacy service methods are one-line `RetiredRouteError` stubs. HTTP routes authenticate first, then return `410 timeline_commit_required`; document alias/timeline-id smuggling guards are present.
- Bodies/helper removed: parent composition publisher, timeline render publisher, and legacy render-target helper. Generated/schema/pin/artifact files are unchanged.
- Actual Agent-backed commit/bootstrap/restore and mounted HTTP route tests remain live.

Tests:

```text
96 passed in 27.46s
```

Command:

```text
ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/agent \
PYTHONPATH=$PWD:/home/user/work/agent \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/test_timeline_legacy_authority.py tests/test_timeline_commit_routes.py
```

Also passed: `py_compile`, `git diff --check`.

Static limits:

- Runtime venv lacks Ruff and Pyright.
- Supplemental Ruff baseline: service `34→33` diagnostics; server `3→3`; no changed-line diagnostics.
- Module origins verified from this worktree and `/home/user/work/agent`.
- No full/native/browser/heavy suites run.

Blocking finding: neighboring legacy publication tests still invoke retired render/parent-publication methods and expect old conflict/success behavior. The prior author report records 17 failures; these tests are not strict `xfail`s. They must be migrated to assert strict 410/no-write behavior or exercise the real commit path, preserving meaningful assertions.

A3 and G4 are also not merged in `BOARD-HEADER`; merge remains prohibited. `DONE` and the R5 commit message were written.