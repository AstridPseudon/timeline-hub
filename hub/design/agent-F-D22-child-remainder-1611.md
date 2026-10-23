# F-D22 child-environment qualification remainder

Status: bounded remainder run completed; one genuine current failure is handed back to Agent SDK/rendering ownership. No product repair was made.

## Inventory and exclusions

The sole inventory was `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-F-D22-terminal-classify-1442-e0036c850d1a7b7c.json`.

| group | inventory | selected |
| --- | ---: | ---: |
| `child-probe` | 17 | 16 |
| `child-import-or-recipe` | 87 | 84 |
| `child-import` | 9 | 9 |
| **total** | **113** | **109** |

Excluded exact nodes, because they already had named proof in the existing installed environment:

- `tests/core/execution/test_remotion_host_session.py::test_two_public_command_workers_settle_task_leases_then_host_drains_original`
- `tests/core/execution/test_worker_startup_identity.py::test_sanitized_child_import_proves_current_host_sdk_version_and_vendored_client`
- `tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[-c]`
- `tests/packs/rendering/test_remotion_backend.py::test_manifest_command_runs_from_owning_pack_root`

The exact 109-selector manifest is `/tmp/w-c970366b1f/d22-remainder-selectors.json`; its inventory and exclusions were checked against the sole inventory before collection.

## Environment and custody

- Agent source: commit `98ef2f9c95fd43d88cca2909d8d1518302e3050c` (central snapshot tree `ed007d6efc06135b5978d8a11a71609b0f476f14`, synthetic harness head `a2c3e5a2c24681ddef57c30ae79207ad908c39e5`, parent is the source commit).
- Installed child: `/home/user/work/venv-agent-child-d22-8c3b926e/bin/python`, Agent `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`.
- Runtime pin: `9ce4242bc01f100bab9efc51032a73985cefb2b2`, runtime tree `92ab1f5f739ffdfedf7b25fbd2a7b46ae42c5d1a`.
- Node: `v20.19.4`; profile archive SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`; profile lock SHA-256 `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`; runtime-protocol SHA-256 `4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2`.
- Composition version: `0.0.14`; PEP 610 and `-I`/parent-child imports were checked.
- Current product-relevant execution/rendering/bootstrap source: 246 byte-equal files versus installed Agent 8c. Relevant failure-owner hashes: `astrid/sdk/host_bootstrap.py` = `50e73b1a9b95528dc06192e0102caad55ec7192b5369ff8a6698cb14c70a0b07`; `astrid/core/rendering/remotion_runtime.py` = `84a495de2139c74b22c001094a3bb4d9252803f11715d7803054ecc2f9cc617e`.
- All 113 original node AST body hashes were captured; current and installed-8c hashes matched. Full per-node hashes and before/after custody snapshots are in `/tmp/w-c970366b1f/d22-state.json`.
- Preflight ran before and after the body. Installed package imports, runtime pin, profile lock/archive, source status, and module hashes remained unchanged. No shared dependency or environment was modified.

## Central service run

The one actual central request was:

```text
D=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-F-D22-child-remainder-1611 d22-child-remainder-1611 --files d22-remainder-selectors)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test $D
```

An initial submission with an absolute `--files` path was rejected by the service argument validator before snapshot or test execution; it produced no test result. The tokenized request above was the sole request that executed collection and bodies.

Harness command:

```text
python3 /tmp/w-c970366b1f/run-d22-remainder.py d22-remainder-selectors
```

The harness did one exact `pytest --collect-only` and one exact body invocation, both with the installed child interpreter, `-P`, `-q`, `-o addopts=`, and `-p no:cacheprovider`. Collection was 109/109. Body result: **108 passed, 1 failed in 1266.10s**; service result directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-F-D22-child-remainder-1611-d22-child-remainder-1611-1023161619-2130/`

## Current failure and handback

Exact failed selector:

`tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter`

Traceback path: `host_bootstrap.ensure_pack_host` -> `_prepare_render_validation` -> `prepare_remotion_validation` -> `_settle_registries` -> `_registry_probe`; it raises at `astrid/core/rendering/remotion_runtime.py:721`:

`RemotionValidationError: installed registry launch source binding is unavailable`

Captured stderr diagnostics were `registry_settle=failed` and `launch_transaction=failed` for process `23349`. The installed child, profile, runtime, imports, and byte-equal current source all passed custody checks, so this is classified as a current Agent SDK/rendering source behavior failure, not relabeled as an environment failure. No product repair or test weakening is in scope. The old full-10679 failure classifications remain **UNCONFIRMED**; current passes do not promote them.

Existing proof retained without rerunning those bodies: representative 4 passed in 181.86s (1512), process 9 passed in 29.94s (1532), manifest 1 passed in 10.46s (1550).

## Limits and next step

No full suite, P1-P4, native14, browser, inverse, or private duplicate was run. The next owner should investigate the installed registry launch source binding in `astrid/sdk/host_bootstrap.py` / `astrid/core/rendering/remotion_runtime.py` and then rerun the affected selector under its normal qualification process. The historical full-10679 result remains unchanged.
