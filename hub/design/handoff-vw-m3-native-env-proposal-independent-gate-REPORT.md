# Native host environment proposal — independent gate

## Verdict

**REJECT as written; revise the Agent-owner proposal before peer port.**

The browser-selector part is approved in principle. The project-directory
deletion is too broad: the proposed removal at
`astrid/packs/rendering/rendering/renderers/remotion/run.py:1138` is inside
`_execute_remotion_locked`, whose `remotion_env_additions` map feeds both the
host-session request and the direct/ephemeral Remotion CLI subprocess.

## Source review

- `astrid/core/execution/remotion_host_session.py::_validate_request` binds
  `request["projectDir"]` exactly to `lease.project` and keeps the request
  environment closed to `TMPDIR`, `TMP`, `TEMP`,
  `ASTRID_TIMELINE_COMPOSITION_SRC`, and `PYTHONPATH`. Therefore the host
  request must not carry `ASTRID_REMOTION_PROJECT_DIR`; the proposed removal
  is correct for that branch.
- `_start` currently projects only the fixed base environment. Adding the
  already admitted `ASTRID_REMOTION_BROWSER_EXECUTABLE` is bounded and relies
  on the existing `build_child_subprocess_env` parent-precedence and
  unlisted-drop policy. No new allowlist/API/DTO/policy/authority change is
  needed.
- In `run.py`, the host path is specifically
  `frame_mode and frame_session is not None` (the call to
  `frame_session.render`). The `else` path invokes `subprocess.run` directly.
  That direct path must retain `ASTRID_REMOTION_PROJECT_DIR`; the ephemeral
  CLI is not covered by the host session's bound `projectDir` field.
- The separate registry-generator assignment at `run.py:465` is not part of
  this finding and should remain unchanged.

## Required minimal correction

Keep the host request free of the redundant field, while preserving it for
every direct CLI invocation:

```python
if not (frame_mode and frame_session is not None):
    remotion_env_additions["ASTRID_REMOTION_PROJECT_DIR"] = str(project_dir.resolve())
```

This condition also preserves the field for the unusual `frame_session`-
provided/non-frame call, because that call still takes the direct subprocess
branch. The focused host selector test should remain; the existing direct CLI
environment regression must stay green and should be rerun on the corrected
proposal.

## Independent evidence

All source was read from Agent integration `30fc8dd15`; no Agent or shared
worktree was modified. The unapplied proposal patch was applied only to
disposable `/tmp` archives.

- Candidate host/env tests: **7 passed in 0.60s**. This covered the existing
  parent-owned selector/unlisted-drop policy, the proposed host-session
  selector witness, runtime-credential exclusion, and host-scope refusal.
- Direct CLI regression with the current source: **PASS** after replacing
  only the prohibited port probe with a fixed test-local value; the test
  observed `ASTRID_REMOTION_PROJECT_DIR` in the direct child environment.
- The same direct regression against the unapplied proposal: **FAIL** with
  `KeyError: 'ASTRID_REMOTION_PROJECT_DIR'` at the existing assertion in
  `tests/packs/rendering/test_remotion_backend.py:1424`.
- A normal pytest invocation of the four small tests also passed the six
  host/env cases, but the direct backend test could not create its port probe
  under this sandbox (`PermissionError: [Errno 1] Operation not permitted`).
  No browser, renderer, server, socket listener, install, network, or full
  suite was used; the direct regression was rerun with a fixed value at that
  probe only.

No Composition files were changed. Agent remains the owner of the core and
caller patch.
