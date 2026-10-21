# Agent outer existing read boundary

Date: 2026-10-21 UTC  
Status: source-only closure; no live, root, outer, native, model, render,
browser, or full-suite proof.

## Decision

An exact existing read adapter is available. The managed Python action may use
the host's already-issued worker connection for admitted target/media reads;
it must not call `AstridClient.open_from_launcher()`.

The host injects `ASTRID_RUNTIME_ENDPOINT` and the worker bearer into ordinary
Python action children at
`astrid/core/execution/generic_host.py:7597-7607`. The worker credential is
the existing least-privilege host credential, whose declared scopes are
`handshake`, `worker:register`, `worker:execute`, `projects:read`,
`tasks:read`, `objects:read`, and `objects:write` at
`astrid/core/execution/generic_host.py:4452-4460`. The action does not request
or receive `projects:write`, `tasks:write`, or any new permission.

## Exact adapter and source change

`astrid/core/execution/executor/_action_context.py:163-197` now provides the
private `_managed_read_client(context)` factory. It:

1. requires the active, lifetime-fenced `_ActionContext`;
2. consumes only the endpoint and bearer already supplied by the host;
3. uses the existing `WorkspaceClient` and `RemoteAstridClient` classes;
4. handshakes with only `worker:execute`, `projects:read`, `tasks:read`, and
   `objects:read`;
5. requires the handshake actor to equal the admitted outer `executor_id` and
   the returned scopes to equal that read-only request; and
6. returns the existing `AstridClient` wrapper without invoking launcher
   startup or changing its identity.

`astrid/packs/video_editing/actions/sync_draft_voiceover/run.py:38-73`
replaces only the outer `open_from_launcher()` call with this private factory.
The existing `_PreparationClient` still supplies the trusted outer producer
coordinates, and `_PreparationTarget.publish()` still refuses worker-side
publication. No action input, public client method, authority field, provider,
delegation edge, or mutation task was added.

The compact trusted fixture at
`tests/core/execution/test_python_action_context.py:129-174` proves the
host-worker actor and exact read scopes are retained, and that an inner actor
is refused. Existing action fixtures patch this private factory rather than
the six-scope launcher (`tests/packs/video_editing/test_sync_draft_voiceover_action.py:42-53`,
`tests/packs/video_editing/test_draft_voiceover_managed.py:198-204`).

## Why the registered assembler is not this adapter

The already-qualified `rendering.assemble_timeline` action is a command
executor, not a Python action: its declaration is
`astrid/packs/rendering/pack.yaml:47-118`, and its implementation consumes a
staged `runtime/resolved-children` JSON file at
`astrid/packs/rendering/actions/assemble_timeline/run.py:416-420`.
The generic host materializes authorized CAS/file inputs through its existing
worker read connection at `astrid/core/execution/generic_host.py:6512-6561`
and `:6892-7007`. That qualifies the host's immutable file-read route; it does
not expose a Python action client or prove that the voiceover action can use a
launcher client. The voiceover action therefore uses the same host credential
through the existing SDK read adapter above, while its proposed result-bundle
input remains a separate requester-split decision and is not implemented here.

## Preserved guards and limits

The action context remains installed only by the verified runner at
`astrid/core/execution/executor/runner.py:425-429`; producer/target identity,
PID/thread, output-directory, nested-use, and expiry checks are unchanged.
The action still uses the real actor from the Runtime handshake, not the inner
speech task or ambient `ASTRID_NETWORK_ADMISSION`. Existing script pinning,
media-selection/verified-metadata reads, byte-hash checks, native capture,
proposal guards, startup custody, and original22 voiceover assertions remain
unchanged. This source change does not make the current helper's inner speech
submission valid; the requester/result-carrier split remains separate.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/core/execution/test_python_action_context.py \
  tests/packs/video_editing/test_sync_draft_voiceover_action.py \
  tests/packs/video_editing/test_draft_voiceover_managed.py \
  tests/packs/video_editing/test_draft_voiceover.py
116 passed in 11.11s

ruff check astrid/core/execution/executor/_action_context.py \
  astrid/packs/video_editing/actions/sync_draft_voiceover/run.py \
  tests/core/execution/test_python_action_context.py \
  tests/packs/video_editing/test_sync_draft_voiceover_action.py \
  tests/packs/video_editing/test_draft_voiceover_managed.py
All checks passed

git diff --check
PASS
```

No full or live-socket suite was requested.
