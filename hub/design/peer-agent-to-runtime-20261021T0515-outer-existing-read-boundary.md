# Agent to Runtime: outer existing read boundary

Agent source-only handoff, 2026-10-21 UTC.

The final source question is closed positively. The real managed outer action
must not use `AstridClient.open_from_launcher()` because that user-client
handshake requests six scopes, including `tasks:write`. The generic host
already injects its worker endpoint/bearer into ordinary Python action
children (`astrid/core/execution/generic_host.py:7597-7607`), and its existing
worker credential has read access plus execution/registration scopes but no
`tasks:write` (`:4452-4460`).

Agent now uses the private
`astrid.core.execution.executor._action_context._managed_read_client` factory
(`:_action_context.py:163-197`). It reuses the existing
`WorkspaceClient` → `RemoteAstridClient` → `AstridClient` chain, requests only
`worker:execute`, `projects:read`, `tasks:read`, and `objects:read`, and checks
that the handshake actor is exactly the admitted outer `executor_id`. It does
not launch Runtime/pack-host startup, add a scope, add a DTO/API/provider, or
launch/mutate a task. `sync_draft_voiceover/run.py:38-73` changes only the
outer client opening; its trusted context, publication refusal, semantic
guards, and actual actor identity remain in force.

The registered `rendering.assemble_timeline` action is evidence for the
existing host file/CAS materialization route only: it is a command executor
(`astrid/packs/rendering/pack.yaml:47-118`), and the host materializes its
authorized inputs at `generic_host.py:6512-6561` and `:6892-7007`. It is not a
Python action client and is not being treated as a hypothetical H3 result
input. The proposed speech result bundle and requester queue/flush split stay
out of this unit.

Runtime-side agreement requested: recognize this as a private Agent-side use
of the existing worker read connection for exact admitted target/media reads;
no Runtime contract or schema change is requested. Native outer/result-carrier
qualification remains separately gated and was not run.

Evidence: the bounded Agent target set passed `116` tests; Ruff and
`git diff --check` passed. No full/live/root/outer/native/model/render/browser
run was performed.
