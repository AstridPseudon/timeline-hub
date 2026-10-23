# F installed Agent + Runtime prerequisite

Status: private environment qualified; test-service activation intentionally not performed.

## Exact private environment

- Root: `/tmp/w-827c512f9a/installed-runtime-ef851-1365`
- Python: `/tmp/w-827c512f9a/installed-runtime-ef851-1365/venv/bin/python` (Python 3.13.16, regular private file)
- Site packages: `/tmp/w-827c512f9a/installed-runtime-ef851-1365/venv/lib/python3.13/site-packages`
- Existing four-field profile: `/tmp/w-827c512f9a/installed-runtime-ef851-1365/profile/astrid.json`
- Qualified dependency source: read-only `/home/user/work/venv-agent-child-s2`
- Pin inventory: 164 entries; SHA-256 `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`

## Source and artifacts

- Agent commit `ef851b22c506245441b9a630c093b3460e39cbdc`, tree `b11eee891208d11e23c55950f8954ddd3377d5a8`
- Runtime commit `1365e4b17b31c4a7093d5943674637067fd2bab4`, tree `6c69c3dc47822fffbaf27cd63815d2895155ffaa`
- `astrid-0.1.0-py3-none-any.whl`: SHA-256 `c33e831be2d5c276bd2993b9bf2a07508b39049e41590e2f79b5743ab69dd235`
- `astrid_runtime-0.1.0-py3-none-any.whl`: SHA-256 `ae920cd13fbf3be54c2c85f46b9fb303d8f3b0290d1ea89e6bd059f3643f8256`
- `astrid_runtime_client-0.2.14-py3-none-any.whl`: SHA-256 `de220beb14e6272dcab38897a75c75fe51ac11a8b5a595b86ac8f7cfbaad531e`
- The Runtime wheel contains both real package namespaces `runtime_protocol` and `astrid_runtime`; the client wheel came from its exact `packages/python` source.

## Evidence

- `python -I -B` import audit: PASS for `astrid`, `astrid_runtime_client`, `runtime_protocol`, `astrid_runtime`, `banodoco_timeline_schema`, NumPy, Pillow, OpenCV, and PyYAML; all origins are below the private site-packages root.
- Distribution closure: PASS for all 164 inventory entries plus the three product distributions (`astrid==0.1.0`, `astrid-runtime==0.1.0`, `astrid-runtime-client==0.2.14`). RECORD paths are private and symlink-free.
- Contract: client `0.2.14`, installed schema digest `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.
- Installed CLI checks: `python -I -B -m astrid_runtime --help` and `astrid-runtime-protocol --help`: both exit 0.
- Hermetic doctor: exit 1 with the normal `runtime_unavailable` result. It has no missing `runtime_protocol`/`astrid_runtime` traceback and no wrapper `UnboundLocalError`; the expected local absence is catalog/Remotion state. Reported limits were bundle 1,048,576 bytes, 200 events, 65,536 log bytes, and a 5,000 ms observation deadline.

## Cost and limits

- Private environment measured 941,099,739 bytes (`du -sb`), 992 MB allocated (`du -sh`); final free space was 15,073,243,136 bytes. The 15 GB floor was not crossed.
- No shared venv, node_modules, checkout, Runtime worktree, product source, tests, fixtures, guards, bindings, or launcher was modified.

## Test-service boundary

No new installer or D09 run was submitted. The existing `suites.conf` rows hard-code shared interpreters/paths and do not accept a per-run private environment. The D09 fixture also sets its existing Runtime and schema paths internally. Therefore the exact test qualification remains pending the independent review/activation of the narrow proposal below; no local localhost/socket/browser/native run was attempted.

Proposed, not activated, row (outside bytes preserved). Exact command:

agent agt-F-installed-runtime-child-0958-private-env-one-installer-d09 env -i HOME=/tmp/w-827c512f9a/installed-runtime-ef851-1365/test-home LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONPATH="$PWD" PATH=/tmp/w-827c512f9a/installed-runtime-ef851-1365/venv/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 ASTRID_RUNTIME_CHECKOUT=/tmp/w-827c512f9a/installed-runtime-ef851-1365/venv/lib/python3.13/site-packages ASTRID_RUNTIME_SOURCE_MANIFEST=/tmp/w-827c512f9a/installed-runtime-ef851-1365/profile/astrid.json /tmp/w-827c512f9a/installed-runtime-ef851-1365/venv/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[False-0] tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result

The next action is independent review of this one row and its installed-path bindings, then one central test-service run if approved. No product or fixture change is proposed.
