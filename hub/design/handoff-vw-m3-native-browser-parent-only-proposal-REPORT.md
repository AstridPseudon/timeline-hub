# Native browser parent-only proposal

## Result

Prepared an unapplied Agent-owner patch against current Agent HEAD
`79b33f8a1` (`tl/integration`). The patch has exactly two files:

- `astrid/core/execution/remotion_host_session.py`: forward the already
  admitted `ASTRID_REMOTION_BROWSER_EXECUTABLE` through the fixed host-owned
  projection in `_start`.
- `tests/core/execution/test_remotion_host_session.py`: exercise the real
  request-validation/start boundary for parent precedence, unlisted-env
  dropping, and refusal of a request-supplied browser selector.

The existing `astrid/core/subprocess_env.py` parent-owned precedence policy is
unchanged. The existing project/node/CLI path guards, request environment
allowlist, and exact browser binary path guard are unchanged. No new selector,
flag, API, DTO, authority, install, or launch-validation surface is added.

The rejected unconditional `run.py` project-directory deletion is deliberately
absent. The direct CLI caller still retains its project-directory environment
assignment; that conditional caller patch is a separate reviewed unit and is
not part of this proposal.

## Evidence

- Private archive applicability: `git apply --check` **PASS**.
- Focused overlay lane: **9 passed in 0.66s**.
- Scope check: proposal contains only the two files above; no `run.py` or
  project-directory deletion hunk.
- The focused test observed caller/lease selector `/caller/browser`, parent
  selector `/parent/browser`, and child selector `/parent/browser`; the
  unlisted lease variable was absent. A request environment containing the
  browser selector was refused as outside the admitted projection.

No Agent product file was edited in this worktree. No Node, browser, renderer,
live local server, full suite, install, network, or shared dependency was used.

## Handoff

`proposal.patch` is ready for Agent-owner review/application. After applying,
the owner should rerun the focused subprocess-env and Remotion host-session
tests on the integrated Agent tree, then perform the separate manager-controlled
fresh-native-PNG qualification. This proposal does not claim an MP4
registration failure.
