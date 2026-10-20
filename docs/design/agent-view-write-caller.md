# Agent view-write caller port

## Source

- Settled plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`.
- Runtime handoff: `/home/user/timeline-hub/hub/design/runtime-view-write-scope-handoff.md`.
- Agent worktree base: `df2739f9` (`tl/integration` ancestry).
- Handoff Runtime implementation basis: `642eef7`, with F1/F2 still requiring the final coordinated Runtime release.

## Changes

- `astrid/sdk/workspace_client.py` now requires an explicit keyword `idempotency_key` for `create_timeline_view` and forwards it unchanged to the generated client.
- `astrid/sdk/remote.py` no longer classifies `create_timeline_view` as a read. The existing mutation-key allocator therefore gives each logical native-input view request a key, and the dispatch passes that same key to the generated client.
- Native SDK tests cover `projects:write` refusal propagation, successful view calls, exact retry key/options, and a fresh key for a new request/head refresh.
- Existing inspection/read and composed/diff paths remain unchanged. No endpoint, CLI key flag, authority scope, generated client, or contract pin was added or changed.

## Results

- `/home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_workspace_client_timeline_commit.py tests/sdk/test_native_timeline_facades.py` — **31 passed**.
- `/home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_timeline_route_integration.py tests/sdk/test_timeline_visualize_public_surface.py` — **26 passed in 57.87s**.
- Central named `client-cutover-integration` — **34 passed, 5 failed**. The failures are pre-existing retired direct-shot-write expectations in `tests/stage1/test_runtime_client_cutover.py`, not view-caller failures.

## Blocked pair / qualification boundary

The checked-in `astrid_runtime_client.generated.WorkspaceClient.create_timeline_view` still has the old three-argument signature and does not accept `idempotency_key`. This branch intentionally targets the documented final official client signature; it does not add a compatibility bypass. The paired Runtime F1/F2 final union and generated-client pin must land before live write qualification or release. The expected old-client mismatch is therefore reported, not hidden.

