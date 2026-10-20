# Native host environment bounded proposal

## Result

Prepared an unapplied Agent-owner proposal for the two source-level native-host
blockers from `handoff-vw-m3-native-fresh-export-label-join-REPORT.md`.

No Agent source or test file was edited in this Composition worktree. The
proposal is based on Agent tree `30fc8dd15` (`tl/integration`, with the already
approved browser-selector admission in `astrid/core/subprocess_env.py`).

### Proposed source changes

1. In `astrid/core/execution/remotion_host_session.py::_start`, add only the
   already admitted `ASTRID_REMOTION_BROWSER_EXECUTABLE` to the fixed inherited
   projection. Do not add a new env API or alter `build_child_subprocess_env`.
   Its existing parent-owned merge remains authoritative: with lease/caller
   value `/caller/browser` and parent value `/parent/browser`, the child gets
   `/parent/browser`; an unrelated `ASTRID_UNLISTED_BASE` remains absent.

2. In the owned Remotion caller
   `astrid/packs/rendering/rendering/renderers/remotion/run.py`, remove the
   redundant `remotion_env_additions["ASTRID_REMOTION_PROJECT_DIR"]` assignment.
   The request already carries `projectDir`, and the host session binds and
   validates it against `lease.project`. Keep `_validate_request`'s environment
   allowlist closed; do not accept arbitrary caller project overrides or add a
   project env allowlist entry. Existing toolchain, lock, launch-validation,
   source, and lifetime checks remain unchanged.

3. Add one host-session test that reaches `manager.request()` and the normal
   `_validate_request`/`_start` boundary before native allocation, asserting the
   exact parent-precedence and unlisted-drop behavior above. The existing
   `test_subprocess_env.py` parent-precedence test remains unchanged and is part
   of the focused evidence.

The complete unapplied diff is in the adjacent
`handoff-vw-m3-native-host-env-bounded-proposal-proposal.patch`.

## Evidence

- Patch applies cleanly with `git apply --check` to a private archive of Agent
  `30fc8dd15`.
- Focused private-snapshot test command: **9 passed in 0.62s**. It covered the
  existing subprocess-env parent-precedence/unlisted-drop test, the proposed
  host projection witness, runtime-credential exclusion, host-scope/path
  refusal, and unsupported render-field refusal.
- Source witness: **PASS** — the redundant project-dir caller assignment is
  absent and the browser selector projection is present.
- Differential Ruff witness: **14 baseline / 14 candidate diagnostics; 0 new,
  0 removed** across the three affected Agent files. The diagnostics are
  pre-existing tree findings, not introduced by this proposal.

The exact commands and observed parent/child values are recorded in the
adjacent `handoff-vw-m3-native-host-env-bounded-proposal-COMMAND`.

## Boundaries and next step

The report's two items are source findings, not physical render failures. No
browser, renderer, live service, full suite, network install, shared dependency,
or Agent integration change was run here. The Agent owner should review and
apply the proposal, then run the focused tests on the integrated Agent tree;
physical fresh-PNG qualification remains a separate manager-controlled step.
