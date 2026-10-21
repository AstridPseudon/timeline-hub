# Agent full-wrapper prefix repair — MAIN registration handoff

Status: **HOLD for independent delta review**. This note makes the intended
MAIN registration concrete; it does not edit `tests/suites.conf`, activate a
lease, request a suite, or authorize a full run. Handoff 1010 owns activation
and the final request.

## Reviewed source artifact

The worker source is `scripts/full_coherent_public_current_integration.sh` on
`tl/agt-m4-full-wrapper-client-prefix-firstcause-repair-1014`, based on
`475fb69df31fc5af059669343f1fae4545e8e723`.

- current worktree blob: `594c16e1f21340f179296fa341e22233df7efa54`
- current worktree SHA-256: `5d899819082448b90f583cd83268fd768fdbf8138aca290be43c15bb05a5314d`
- the harness commit will publish the same file under a new commit/tree

The repair is c4b-scoped, as required by this worker brief. MAIN must update
the wrapper's exact Agent source constants if the final request uses the fbba
source tuple from handoff 1010; this artifact must not be relabelled as an
fbba-qualified wrapper without that update and a delta review.

## Intended named suite entry

After the successor wrapper is published under the durable MAIN runner root,
the one suite line should be equivalent to the following single command. The
profile, wheel, pins, source checkouts, and C13 paths are the concrete MAIN
layout in `run-on-main-agent-coherent-public-current.md`:

```text
agent full-coherent-public-current-integration env -i HOME=/root LANG=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin SOURCE_ROOT=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/agent-fbba7c5a2 ASTRID_RUNTIME_CHECKOUT=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/runtime-b92d3e7a RUNTIME_CLIENT_CHECKOUT=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/client-95bd3c5f ASTRID_REMOTION_PROJECT_DIR=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/composition-c13-30da0a5e ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy FULL_COHERENT_PUBLIC_PROFILE_ROOT=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/profile/agent-coherent-public-current-fbba7c5a2 FULL_COHERENT_PUBLIC_AGENT_WHEEL=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/profile/agent-coherent-public-current-fbba7c5a2/wheelhouse/astrid-0.1.0-py3-none-any.whl FULL_COHERENT_PUBLIC_PINS=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/profile/agent-coherent-public-current-fbba7c5a2/metadata/venv-agent-child-s2.txt bash /home/user/work/main-timeline/coherent-public-current-fbba7c5a2/runner/approved-current-wrapper/full_coherent_public_current_integration.sh
```

The line is intentionally recorded here rather than installed in the shared
suite file. It must remain paired with the wrapper's unchanged direct
`exec "$PROFILE_PY" -m pytest -q -n 3 "$@"` and the original no-marker,
no-cache, no-basetemp behavior.

## Intended input lease

MAIN should activate one lease covering the suite line, the successor wrapper
blob/SHA-256, the exact Agent/runtime/client commits and trees, C13 source and
tarball hash, profile root and Python executable, all three product wheels and
hashes, the 164-pin carrier and hash, Node 20.19.4, and the VibeComfy,
ffmpeg/ffprobe, and private C13 node_modules prerequisites. The lease should
state that no full request is valid until all inputs are clean, symlink-free,
and positively preflighted, and should be retired only after the MAIN result
document records the terminal decision.

No live suite or lease is claimed by this worker. The 0948 lease is retired;
the 1010 handoff remains the owner of the eventual MAIN request.
