## Review report

Verdict: **PASS on independent cause; U2c acceptance remains FAIL/held.**

The cited diagnosis is correct:

- Agent `generic_host.py:12717` authenticates the retained Runtime relay before reading any control frame.
- `AuthenticatedCleanupActor.private_peer()` reaches `_peer_token()`, which rejects non-Darwin at `custody_broker.py:594–596`.
- Linux `ProcessCustody` only retains pidfds for registered child/descendant processes and uses them for signal/exit proof. It is not connected to socket-peer authentication.
- Runtime’s existing `posix_handoff.py` `SO_PEERCRED` helpers are used only for handoff PID/UID checks and do not provide retained birth/executable/cleanup authority.
- Runtime’s production `RoleBoundCustodyBroker` independently rejects Linux at `astrid_runtime/custody_broker.py:907–908`; therefore fixing only Agent’s `private_peer` would not qualify the complete production path.

Actual path traced:

`local_worker_composition._prepare_relay()` → inherited relay socket → `local_execution_supervisor.main()` → `serve_control()` → `NativeHostSession` creates separate host control/activation sockets → GenericHost `--host-control-fd` → `LocalExecutionPreparation.serve_control()` → `private_peer()` before first frame.

Darwin obtains `LOCAL_PEERTOKEN`, derives audit-token PID/UID/pidversion, and re-verifies the pinned actor. No equivalent Linux actor exists.

Smallest proposal, requiring explicit cross-repo scope:

- Add a Linux private-peer actor in Agent custody code using kernel `SO_PEERCRED` plus exact birth binding and a retained pidfd, with executable/UID/birth revalidation. Existing pidfd primitives may be reused, but this is a new authority backend.
- Add the matching Linux Runtime relay/role custody support; otherwise Runtime fails earlier.
- Preserve separate control/activation channels, bounded requests, EOF uncertainty, exact identity predicates, and no UID-only or Darwin bypass.

Checks:

- AST parse of 8 relevant Agent/Runtime source files: **passed**.
- `git diff --check`: **passed**.
- `git diff --exit-code --quiet`: **passed**.
- No tests, sockets, hosts, credentials, probes, or live peer checks run, per brief.
- No product files changed; worktree clean.
- Commit message and `DONE` marker written.