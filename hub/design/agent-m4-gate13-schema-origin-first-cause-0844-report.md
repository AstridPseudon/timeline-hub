# Gate13 schema-origin first-cause diagnosis

Date: 2026-10-21 UTC

## Verdict

The 1139 result is an environment/profile origin failure, not a Runtime,
Agent source, lock, generated-client, schema, health, or provider defect.

The exact prior run snapshot was Agent commit
`a9f4cfdaee40f3382b51d6cdb291d7012be96b8c`, tree
`93862f0accf8bbe2331ed551b69839b47f7b8e1b`. Its Agent lock, vendored
client metadata, Agent schema, Runtime b92 schema, and normal Runtime95
producer all agree on the ordinary contract. The failing process imported a
different client from the C13 child site-packages because the schema path
was a whole environment rather than a schema-only origin.

The first failure is the health digest check. No handshake validation and no
product assertion were reached.

## Exact origins and selected environment

The 1139 suite command at `ORCH/tests/suites.conf:149` selected:

- Interpreter: `/home/user/work/venv-agent/bin/python`
- Agent source: the service snapshot of tree
  `93862f0accf8bbe2331ed551b69839b47f7b8e1b`
- Runtime checkout: `/home/user/work/runtime`, b92 commit
  `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`
- `PYTHONPATH`: `$PWD:/home/user/work/runtime`
- `ASTRID_RUNTIME_CHECKOUT`:
  `/home/user/work/runtime`
- `ASTRID_TIMELINE_SCHEMA_PYTHONPATH`:
  `/home/user/work/venv-agent-child-c13-a8a40afd/lib/python3.13/site-packages`
- Remotion/C13 node environment:
  `/home/user/work/runtimes/agent-remotion-0013` and its
  `node_modules`

A read-only import probe with that environment, after importing
`astrid.core.timeline.banodoco_schema`, resolved:

- `astrid` from the Agent snapshot/source root
- `runtime_protocol` from
  `/home/user/work/runtime/runtime_protocol/__init__.py`
- `banodoco_timeline_schema` from the C13 child site-packages
- `astrid_runtime_client` from
  `/home/user/work/venv-agent-child-c13-a8a40afd/lib/python3.13/site-packages/astrid_runtime_client/__init__.py`
- child client metadata from the same C13 child directory
- child client digest:
  `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`
- Runtime digest:
  `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`

The child package is the old generated client: its metadata declares
contract version `0.2.13`. It is bundled under the installed
`astrid-0.1.0` distribution; its `direct_url.json` points to a temporary
build source (`file:///tmp/tmp.97Y6NLePQT`) and provides no matching
95bd provenance.

The import-precedence cause is exact:

1. `tests/editing_conformance/test_native_sheet_current_runtime.py:15`
   imports `astrid.core.timeline.duration`, which loads the package
   `astrid.core.timeline`.
2. `astrid/core/timeline/__init__.py:46` imports
   `astrid.core.timeline.banodoco_schema`.
3. `astrid/core/timeline/banodoco_schema.py:32-38` reads
   `ASTRID_TIMELINE_SCHEMA_PYTHONPATH`, resolves the whole C13
   site-packages directory, and prepends it with
   `sys.path.insert(0, str(_schema_root))` at line 38.
4. Later `astrid/sdk/workspace_client.py:20-21` and
   `astrid/sdk/client.py:15-18` import
   `astrid_runtime_client.contract_metadata`; the prepended C13 directory
   wins over the snapshot Agent's vendored `astrid_runtime_client`.

A control import probe using the existing normal schema environment
`/home/user/work/venv-agent/lib/python3.13/site-packages` resolves the
Agent vendored client and reports the same `7d4afa` digest as Runtime.
That directory contains `banodoco_timeline_schema` but no conflicting
`astrid_runtime_client`.

## Contract/source comparison

All read-only hashes below were collected from the pinned/current artifacts:

| Artifact | SHA-256 / value |
|---|---|
| Agent snapshot `runtime.lock.json` | `920f4a3edf3d0e5ce9df5a0b2749f7b02bc2ea7db6fef2ec70db8d02b65be8e7` |
| Agent snapshot lock `source_commit` | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` |
| Agent snapshot `astrid/core/timeline/schema/edit-command.schema.json` | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Current b92 `contract/schemas/edit-command.json` | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Normal95 `contract/schemas/edit-command.json` | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Current b92 `contract/artifacts.json` | `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d` |
| Normal95 `contract/artifacts.json` | `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d` |
| Agent snapshot vendored client metadata | `SCHEMA_DIGEST=sha256:7d4afa...`, file hash `cdedeb72880102ff6557320d908eac9068470b5088256c4441514e9d7db40514` |
| C13 child client metadata | `SCHEMA_DIGEST=sha256:8de823...`, file hash `b8f40d8ea55d5e72beb6e043f74eff60bf81634cac3b8c27d13415e9180b3cca` |

Runtime b92 and normal95 both publish the health digest from their generated
`runtime_protocol/contract_metadata.py` and service health path
(`runtime_protocol/service.py:775`), so the observed `7d4afa` response is
the expected current Runtime identity.

## Actual first-failing stack

For the six native-front-end nodes, the central log's first node was:

`test_http_connected_rational_move_is_lossless_across_native_frontends[python]`.

The first failure path was:

```text
tests/editing_conformance/test_native_sheet_current_runtime.py:592
  runtime.session(name=entry)
tests/editing_conformance/test_native_batch_ingress.py:104
  client=client()
tests/editing_conformance/test_native_batch_ingress.py:99
  AstridClient.open(...)
astrid/sdk/client.py:334
  workspace = connect(endpoint_value, token)
astrid/sdk/client.py:302
  workspace = WorkspaceClient(endpoint_value, token)
astrid/sdk/client.py:304
  _validate_health(workspace.health(), expected_protocol=PROTOCOL,
                   expected_digest=SCHEMA_DIGEST)
astrid/sdk/client.py:128-129
  _digest_mismatch("health", observed, expected_digest)
astrid/sdk/client.py:306
  raise unavailable(exc, operation="health") from exc
```

Observed value: `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`.

Imported-client expected value: `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`.

The stopped-renderer node has the same first failure at
`tests/editing_conformance/test_commit_runtime_native_checkout.py:210`
through `tests/editing_conformance/test_commit_runtime_m1.py:153`,
then `astrid/sdk/client.py:334, 304, 129, 306`. Its renderer-off assertions
were not reached. The later handshake validator at
`astrid/sdk/client.py:320-328` was not reached in any node.

## Daemon launch/origin

There is no external daemon argv in this suite. The Runtime is an in-process
object, not a subprocess:

- Native nodes: `tests/editing_conformance/test_native_batch_ingress.py:58-59`
  call `new_runtime_daemon(..., authoring_profile='astrid').start()`.
- Gate3 node: `tests/conftest.py:54-60` calls the same helper through
  `real_runtime`.
- `tests/helpers/runtime.py:118-124` calls
  `use_runtime(commit)`, initializes the realm, constructs
  `RuntimeDaemon(root, **kwargs)`, and returns it.
- `runtime_protocol/daemon.py:118-123` starts the in-process HTTP server;
  `runtime_protocol/daemon.py:240-300` loads the b92 Runtime provider,
  registers it, creates `RuntimeHTTPServer`, and serves in a thread.

The effective daemon constructor inputs are loopback host
`127.0.0.1`, ephemeral port `0`, a temporary realm/support root, and
`authoring_profile='astrid'`. No subprocess argv or child interpreter is
involved in the failing health path.

## All seven failures

All seven were identical handshake-boundary failures; none reached a product
assertion:

1. `test_http_connected_rational_move_is_lossless_across_native_frontends[python]`
   — health digest mismatch.
2. `... [cli]` — health digest mismatch.
3. `... [sheet]` — health digest mismatch.
4. `test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[python]`
   — health digest mismatch.
5. `... [cli]` — health digest mismatch.
6. `... [sheet]` — health digest mismatch.
7. `test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable`
   — health digest mismatch before renderer-off assertions.

The prior central result remains honestly reported as 7 executed, 0 passed,
7 failed. The earlier 8324 run remains 0 executed because its suite quoting
guard failed before pytest.

## Cheap evidence run

Exact command run in this worker:

```sh
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD:/home/user/work/runtime" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/usr/local/bin:/usr/bin:/bin \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013 \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-c13-a8a40afd/lib/python3.13/site-packages \
  ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0013/node_modules \
  /home/user/work/venv-agent/bin/python -P -m pytest --collect-only -q \
  -o addopts= -p no:cacheprovider -m integration \
  tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends \
  tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends \
  tests/editing_conformance/test_commit_runtime_native_checkout.py::test_authenticated_v1_commit_reload_undo_survives_stopped-renderer-and-preview-reports-unavailable
```

Result: 7 tests collected in 1.59s. No test body, daemon, HTTP, private/native
process, install, render, browser, socket, or full suite was run.

## Smallest bounded correction plan

1. Repair the Gate13 runner/profile seam, not product code: do not put the
   whole C13 site-packages directory in `ASTRID_TIMELINE_SCHEMA_PYTHONPATH`.
   The smallest existing-path correction is the normal schema-bearing
   `/home/user/work/venv-agent/lib/python3.13/site-packages` used by the
   published95 qualification, or an equivalent private schema-only root
   containing only `banodoco_timeline_schema`.
2. Preserve the existing Runtime b92 checkout, normal95 lock/client/artifact
   identities, exact schema and health guards, origin assertions, and all
   seven test selectors. Do not update generated files, pins, schema bytes,
   health handling, or source fallback.
3. Before any third run, perform only read/import/collection preflight:
   `astrid`, `runtime_protocol`, `astrid_runtime_client`, and
   `banodoco_timeline_schema` origins; assert client and Runtime digest
   `7d4afa`; assert the selected schema root cannot resolve
   `astrid_runtime_client`; collect exactly 7.
4. Only after that correction and preflight should the orchestrator decide
   whether to request the one permitted fresh Gate1/3 suite run. Do not replay
   1139 or request it from this diagnosis.

No product mutation or source correction is justified by the evidence.

