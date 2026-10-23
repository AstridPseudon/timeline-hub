# F-D22 child-pair qualification

## Disposition

- Diagnosis: **PASS**. The representative `runtime_protocol` child error is explained by the source-mode import projection and the original child launch boundary.
- Exact-pair qualification: **FAIL / not qualified**. The one sanctioned child-venv job completed, but it installed Runtime `9ce4242bc01f100bab9efc51032a73985cefb2b2`, not the required Runtime `3b926efab2eed122d374540baee297d4cdcec62a`.
- No new bounded original nodes were run. The exact Agent+Runtime pair was not ready, so no child result is counted as qualification evidence.
- No product, test, harness body, dependency, pin, generated file, or shared-install changes were made.

## Sanctioned child-venv evidence

The existing request/result was read from:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/provision/venv-agent-child-d22-8c3b926e.txt`

and queue item:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/childvenv-venv-agent-child-d22-8c3b926e`

Observed installed tuple:

| item | observed |
|---|---|
| Agent marker | `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe` |
| Runtime marker | `9ce4242bc01f100bab9efc51032a73985cefb2b2` |
| required Runtime | `3b926efab2eed122d374540baee297d4cdcec62a` |
| venv | `/home/user/work/venv-agent-child-d22-8c3b926e` |
| Python | `3.13.16` |
| PEP 610 Agent URL | `file:///home/user/work/.child-venv-source-venv-agent-child-d22-8c3b926e-20261023T150645Z-21613.xcwNA1/agent` |
| PEP 610 Runtime URL | `file:///home/user/work/.child-venv-source-venv-agent-child-d22-8c3b926e-20261023T150645Z-21613.xcwNA1/runtime` |
| installed origins under `-I` | `astrid`, `astrid_runtime`, `runtime_protocol`, and `astrid_runtime_client` all resolve under `/home/user/work/venv-agent-child-d22-8c3b926e/lib/python3.13/site-packages` |
| `PYTHONNOUSERSITE` | absent |
| free space at check | `15,145,512,960` bytes on `/home/user/work` (above the 15 GB floor) |

The Runtime mismatch is substantive: `git diff 3b926...9ce424...` reports changes in `runtime_protocol/timeline_commit_auth.py`, `timeline_commit_port.py`, three Runtime tests, and two fixtures (`579` additions / `21` deletions in the protocol source diff). This is a setup/provisioning identity failure, not evidence against Agent product code.

The generated row named `venv-agent-child-d22-8c3b926e` is also not a child-venv invocation. Its exact command in `tests/suites.conf` uses `/home/user/work/venv-agent/bin/python` and `/home/user/work/wt/rt-pin-3b926efa`; the row SHA-256 is `7198821768a832f65a48e188eb5b64e88c8d42b27be0fc80293d95adb564b629`. This must be repaired by the harness/provisioning owner before qualification; this worker did not mutate it.

## Independent source diagnosis

The exact Agent `8c355...` source has these relevant rules:

- `astrid/core/generation/vibecomfy_dependency.py:131-145` accepts ambient `PYTHONPATH` dependency roots only when the path basename is `site-packages` or `dist-packages`.
- `astrid/core/execution/generic_host.py:1883-1887` builds a source-mode child `PYTHONPATH` from the product parent, those filtered dependency roots, and admitted pack roots.
- `astrid/core/execution/generic_host.py:8454-8464` reconstructs the worker child `PYTHONPATH` from the network hook, product parent, filtered dependencies, and admitted import roots; arbitrary ambient child `PYTHONPATH` is excluded.
- The original body `tests/core/execution/test_generic_host_actions_v3.py` has SHA-256 `32e8958cce8bbcae19f1771f131e043171d0ac5f62732bfdefe8a1dbcd54708d`. Its `-c` representative constructs `PYTHONPATH` from the product checkout and temporary script directory, then invokes `python -m astrid.core.execution.generic_host_worker`.

Direct bounded source check (read-only, no test body execution):

```text
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-3b926efa" \
  PATH=/home/user/work/venv-agent/bin:/usr/bin:/bin \
  /home/user/work/venv-agent/bin/python -P -c 'from astrid.core.generation.vibecomfy_dependency import dependency_pythonpath; print(dependency_pythonpath({"PYTHONPATH": "/home/user/work/wt/rt-pin-3b926efa:/home/user/work/venv-agent/lib/python3.13/site-packages:/tmp/arbitrary"}))'
```

Result:

```text
('/home/user/work/venv-agent/lib/python3.13/site-packages',)
```

The required Runtime checkout is therefore removed from the source child projection. The retained full-service traceback shows the resulting child failure at `runtime_protocol` import (`log.txt` line 1487); the retained child-environment report records 68 `runtime_protocol` and 9 `astrid` missing-module fingerprints. This proves the representative mechanism only; it does **not** prove that all 114 environment-classified failures are cleared.

Relevant source hashes:

- `generic_host.py`: `fc020cc2f6256642203fc4d36a9bb661265fa9a9589d386a46963528d11791d3`
- `subprocess_env.py`: `ae1aefbdec52e7db70b2ddfe7b2f75698bfc5aece1b5506030bc30569a3ee42b`
- Runtime3b `runtime_protocol/__init__.py`: `4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2`
- full-service raw terminal: `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`

The prior full-service recipe retained the locked profile and Node identity:

- profile: `/home/user/work/runtimes/agent-remotion-v3-819acf-1110`
- profile lock SHA-256: `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`
- Composition archive SHA-256: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`
- Composition version: `0.0.14`
- Node: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, `v20.19.4`
- full-service `PYTHONNOUSERSITE`: absent
- full-service Runtime origin: `/home/user/work/wt/rt-pin-3b926efa/runtime_protocol/__init__.py`

Its exact runner argv was `env -i ... /home/user/work/venv-agent/bin/python -P -c '... pytest.main(["-q", "-n", "3"])'`, with `PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-3b926efa"` and `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa`; the complete command is retained in the full-service summary and D22 terminal JSON. That service's child stderr includes the `runtime_protocol` traceback cited above. No new exact-pair child argv/env/stderr exists because qualification was correctly stopped at the identity mismatch.

## Exact next owner and bounded cohort handoff

Next owner: child-venv dispatcher/provisioning plus test-harness owner. They must reconcile the existing request to an immutable installed pair with Agent `8c355...` and Runtime `3b926...`, and make the named child suite invoke that venv. No duplicate request was issued here.

After the exact pair and row are proven, run at most four original nodes, one per distinct child cause, retaining argv, effective env, child stderr, `-I` import origins, body hash, profile hashes, Node 20 identity, and absent `PYTHONNOUSERSITE`:

1. `tests/core/execution/test_remotion_host_session.py::test_two_public_command_workers_settle_task_leases_then_host_drains_original` — child-probe.
2. `tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[-c]` — child-import-or-recipe.
3. `tests/core/execution/test_worker_startup_identity.py::test_sanitized_child_import_proves_current_host_sdk_version_and_vendored_client` — child-import.
4. `tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result` — D09 probe.

The remaining current full-service environment cohorts are 17 child-probe, 87 child-import-or-recipe, 9 child-import, 3 D09 probe, and 1 D13 preflight node. The existing full result remains `185 failed, 16,733 passed, 4 skipped, 19 errors`, exit `1`; it is not reclassified as a qualification result.
