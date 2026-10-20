# WC3 real HTTP parent-media retry handoff

## Source tuple

- Agent source snapshot used by the final named service: `c87504fdece3b1113dccef9ebda6f7e690863247`.
- Agent checkout HEAD before harness commit: `3dae5bd4ed9e68295725272a9c34823401a8dd22`.
- Runtime source: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, via `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a0dca169`.
- Adapter tuple: public `AstridClient.timelines.replace_parent_media` / generated `WorkspaceClient` transport -> real `RuntimeHandler` HTTP `/v1/projects/{project}/timelines/film/commit`, image and video.

The test captures the exact per-request `RuntimeHandler._request_id()` and asserts it is non-empty, together with exact path, idempotency key, serialized body, and receipt. Request IDs are runtime-generated and are not stable across service snapshots; the central result log does not emit the captured value.

## Change

Added one bounded real HTTP proof in `tests/editing_conformance/test_commit_runtime_parent_media_swap.py`. It creates a fresh parent-owned clip with genuine five-field CAS media, injects a lost ACK after durable acceptance, restarts the daemon, and verifies exact retry body/key/receipt, canonical order/opaque/config mirror, reload, guarded undo/redo, and later-head keyed replay. Unrelated and wrong-typed pending intents are refused with byte-for-byte outbox preservation. No product code changed.

## Evidence

Exact named service command:

```text
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-current ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a0dca169 ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-current/node_modules /home/user/work/venv-agent-child-s2/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/packs/video_editing/test_runtime_publication_chain.py tests/editing_conformance/test_commit_runtime_parent_media_swap.py
```

Final service request: `agt-m2-wc3-real-http-retry-final-registered014-render-integration-1020164021-12618`.

Result: `2 failed, 24 passed, 1 deselected`. Both parametrized WC3 real HTTP cases passed. The two failures are pre-existing `tests/packs/video_editing/test_runtime_publication_chain.py` cases: pinned a0 lacks the retired-route compatibility expected by one and rejects `production_worker_credentials` passed by the other.

Static evidence: `git diff --check` passed; AST parse passed; only the intended test file is modified.
