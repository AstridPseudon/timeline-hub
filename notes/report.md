# ASSIGNED10 report: Agent view-write caller port

## Source and scope

Implemented only the assigned Agent caller port from:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`
- `/home/user/timeline-hub/hub/design/runtime-view-write-scope-handoff.md`

Changed `astrid/sdk/workspace_client.py`, `astrid/sdk/remote.py`, the direct native SDK tests, and the requested flat design/report documentation. No generated client, pin, endpoint, flag, authority scope, integration worktree, or Git metadata was changed.

## Exact changes

`WorkspaceClient.create_timeline_view` now takes required keyword `idempotency_key` and forwards it to the generated client. `_RemoteFamily._typed` treats view creation as a mutation, allocates a stable key for each logical request, and passes it as `idempotency_key` at dispatch. Exact retries preserve key/options; a fresh `visualize(..., mode="inputs")` call gets a new key. Inspection remains on the read path.

## Exact tests and results

```text
/home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_workspace_client_timeline_commit.py tests/sdk/test_native_timeline_facades.py
31 passed in 1.28s

/home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_timeline_route_integration.py tests/sdk/test_timeline_visualize_public_surface.py
26 passed in 57.87s

Central named command (`request-test agt-m2-view-write-caller client-cutover-integration`; service command `env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/stage1/test_runtime_client_cutover.py`):
34 passed, 5 failed in 68.49s
```

The system `pytest` invocation was not usable because its environment lacked `jsonschema`; the shared Agent venv was used as required and passed the targeted suites.

## Decisions

The documented final generated-client signature was used even though this worktree still contains the old generated client. No bypass or manual generated-client edit was made. Composed capture and revision-diff callers retain their existing task/invocation behavior; only native inputs view creation crosses the write-authorized mutation boundary.

## Blocked / unverified

The paired Runtime F1/F2 final union and official generated-client/pin are not yet present. Consequently, live Runtime qualification of the new `/views` write call is unverified here and must be run after the coordinated pin. The old local generated client is expected to reject the new keyword until that pin lands. No full suite was requested.

The five named-lane failures are the existing `tests/stage1/test_runtime_client_cutover.py` direct-shot-write expectations; they fail with `retired_route` and do not exercise the view caller port.

