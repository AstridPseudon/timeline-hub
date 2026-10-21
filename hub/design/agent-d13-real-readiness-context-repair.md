# D13 real readiness context repair

Worker repair and exact-node qualification are complete. Independent custody review remains a manager gate before merge/adoption. No public activation is claimed.

## Result and current tuple

- Resumed Agent `ca2a625943b4750d3353cf938d26d321a2bb50e8`, tree `5b2f26b979bbdab0b75413dc4b17f20de672afb3`.
- Final qualified Agent source tree: `36e9bc966687c41dd49aa3f271789bc46da37aec` (central snapshot includes all three changed files).
- Runtime source and unchanged `runtime.lock.json`: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, `/home/user/work/wt/rt-pin-95bd3c5f`.
- Child/host interpreter: `/home/user/work/venv-agent-child-c13-a8a40afd/bin/python`; schema root: its `lib/python3.13/site-packages`.
- Remotion source profile: `/home/user/work/runtimes/agent-remotion-main95bd`, copied per run into private `remotion-current` (including private node_modules). Composition `0.0.13`, Remotion `4.0.509`; unchanged pins/clients/contracts.
- Node: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, through the existing private runner-CA wrapper. No shared dependency files or caches were written.
- Real Runtime started with `real_runtime(authoring_profile="astrid")`. App is not a participant in this node.

## Exact cause

The prior central failure `1021014612-12473` was the retained `runtime validation consumer context differs` guard, wrapped by `worker Remotion readiness context is unavailable`; it was not evidence of a bad installed Remotion package.

The old fixture supplied the complete pytest parent environment as both host and worker. Deriving its variants from the source filter explains the missing combination:

| Effective registry selector | Full parent variant | Filtered parent variant | Claimed command worker |
| --- | --- | --- | --- |
| `PYTHONPATH` after Astrid checkout normalization | Runtime95 root | absent | Runtime95 root |
| `XDG_STATE_HOME` | pytest's private xdg-state directory | absent | absent |
| `ASTRID_PACKS_PATH` | exact snapshot `astrid/packs/rendering` | same | same |
| `ASTRID_RUNTIME_CHECKOUT` | exact Runtime95 source | same | same |

Neither old admitted variant matched the worker. `XDG_STATE_HOME` is filtered at the child boundary; the real command builder explicitly restores the selected Runtime source import root. The exact guard was correct to refuse that unvalidated combination. The native launch projection also omitted the selected Runtime root even though the previous repair's native readiness check included it, and the actual native spawn omitted it as well.

After aligning those projections, the first run passed readiness, real authoring, producer.guard/outbox/lost-ACK/restart/exact retry, and historical render admission, then uncovered the next concrete source-closure break. The renderer transport filters ambient PYTHONPATH. Its source pack launcher imported `atomic_io.py`, which imported `runtime_protocol` before the later Remotion fallback could run. The existing redacted replay bundle recorded `ModuleNotFoundError: No module named 'runtime_protocol'` at that exact import. No guard was loosened to pass it.

## Minimal delta

Three files, 23 insertions / 5 deletions; product delta is 13 insertions / 3 deletions (net +10 lines):

1. `generic_host.py`: include the explicitly selected Runtime checkout in launch-known native/command probe imports and actual native child imports. The prior command builder and native readiness check already carried it. No ambient arbitrary import path is admitted.
2. `transport.py`: carry only that selected Runtime checkout as explicit PYTHONPATH through the existing renderer subprocess environment builder. All other filtering remains intact.
3. Native integration fixture: derive worker environments before validation with the existing `_launch_worker_probe_environments(..., remotion_only=True)`, using the same pack roots passed to the real host. The per-run Remotion stage and real generator are retained.

No new authority, DTO, scope, client, dependency pin, validation fallback, synthetic readiness, mock/provider, fabricated registry manifest, or disabled media check. The guard, source bindings, original waits, lock, process census/custody, immutable admission, and all native assertions remain. The execution/assertion body from `host.discover()` onward is byte-identical to the resumed commit; comparison with original active `6b526a057` confirms no assertion removal (the prior repair had corrected the author claim to `host.client.claim_next`).

## Observed final source and validation fingerprints

The following were read from the real launch artifact during the successful run; the runner removed its temporary pytest directory afterward. Let `A` be `/home/user/work/wt/.test-agt-m2-d13-real-readiness-context-repair-d13-native-positive-render-integration-1021015920-10910` and `T` be `/tmp/pytest-of-root/pytest-128/test_daemon_backed_host_execut0`.

- Exact pack selector: `A/astrid/packs/rendering`; Astrid origin: `A/astrid/__init__.py`; validation module: `A/astrid/core/rendering/remotion_runtime.py`; generator origin: `A/scripts/gen_effect_registry.py`.
- The registry observations imported `/home/user/work/wt/rt-pin-95bd3c5f/runtime_protocol/__init__.py` across every host/worker variant. The original waits use the C13 lexical interpreter above.
- Private tool configuration: `T/node-current-with-runner-ca`, `T/remotion-current`, C13 schema root. HOME is `T/home`; parent XDG state is `T/xdg-state`, and child XDG state is absent.
- Source-settled registry content hash for every host and worker variant: `386dcb3a707934a2bf1054c0a9cf64443028a64ed1df99f7c98d55eee1e95e37`.
- Renderer registry corpus fingerprint for every variant: `afc106fb31038967a75d26d4d062db4cf66148d0b70e8fe08a97219945431af5`, 2387 bound files. Source discovery, generator inputs, module roots and generated readbacks are still checked by the original implementation.
- Validation artifact SHA256: `1da4b544d2723536c1716a6a6c273e6df55e4728c86b27dd4d89161976e30ba7`; probe-source SHA256: `30819353c842f7ec44258bed5ac84b954cd33fdce87c35e1bde689b49c57d0b4`.
- Canonical context SHA256s: full host `1505541ba1baeaa11ab5fd47ac512698444c07cff53083505a4d0b81ba64ac8c`; filtered baseline `944e35d6fd2789ed6da7887b3304b7e31d2d8ec449529828bad8a0cddd279c11`; exact worker with Runtime import root and no XDG selector `880fb21b33e85d88bc000641671363228f492be5e5931c7d647c6fbd8808cee5`.
- Every observed context retained node/schema/schema-discovery original wait exit 0, complete final retained census, and custody_admitted=true. The successful test additionally exercised normal render process custody; no exit certificate or cleanup result was manufactured.

## Exact tests and checks

Only the requested central node was run; no full suite, neighbors, browser matrix, or old7012 replay.

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m2-d13-real-readiness-context-repair d13-native-positive-render-integration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

- First request `1021015551-20590`, tree `8c0ac21e1b196a25e442a431fc01421e3df79a5e`: **1 failed in 102.34s** at renderer source import, after the readiness mismatch was repaired. The existing replay bundle supplied the traceback described above.
- Final request `1021015920-10910`, tree `36e9bc966687c41dd49aa3f271789bc46da37aec`: **1 passed in 167.41s**, service exit 0 (170s).

Exact final service command:

```sh
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default:/root/.local/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-main95bd ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-main95bd/node_modules ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-c13-a8a40afd/lib/python3.13/site-packages /home/user/work/venv-agent-child-c13-a8a40afd/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render
```

This passed the retained ordered managed-media admission, settled native proposal, producer.guard, lost acknowledgement, persisted original flight key, restart/exact retry, receipt/publication identity, one ordinary revision-pinned render task, positive MP4 ffprobe duration, and undo assertions. The test's MP4 assertion uses ffprobe; no separate full-stream decode claim is added here.

Other checks:

```sh
git diff --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check astrid/core/rendering/transport.py tests/packs/video_editing/test_runtime_publication_chain.py
```

Both passed. `git diff --exit-code 36e9bc966687c41dd49aa3f271789bc46da37aec --` also passed, confirming the final worktree exactly matches the qualified snapshot. `ruff check --output-format json astrid/core/execution/generic_host.py` still reports the same 101 baseline diagnostics; comparing (code, message) counts to `git show HEAD:astrid/core/execution/generic_host.py` found no additions. AST parsing passed for all three changed files. A direct `_build_environment` policy assertion retained only the selected Runtime root while rejecting an unrelated PYTHONPATH and undeclared token. No additional pytest suites ran.

## Handoff

The positive is qualified on this exact tuple. No remaining implementation blocker was observed. Manager must dispatch the required independent custody review of the security-sensitive import/environment seams, then decide merge/adoption. The native-spawn alignment is source-checked here; this command-based D13 node is not an independent native-spawn test. Broader suites remain unrun as instructed. No commits, branch operations, pushes, or shared install modifications were performed by this worker.
