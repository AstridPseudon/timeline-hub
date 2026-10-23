# F-D22 installed-current-1512

## Verdict

PASS for a fresh bounded harness proof on the actual compatible installed Agent `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe` + Runtime `9ce4242bc01f100bab9efc51032a73985cefb2b2` pair. This is not a claim about the old Runtime `3b926...` pair, the prior full suite, or any wider D22 census.

## Evidence

Central named service:

```
agt-F-D22-installed-current-1512-d22-installed-current-1512-1023151827-7366
4 passed in 181.86s (0:03:01), exit 0
```

The exact four original nodes were:

```
tests/core/execution/test_remotion_host_session.py::test_two_public_command_workers_settle_task_leases_then_host_drains_original
tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[-c]
tests/core/execution/test_worker_startup_identity.py::test_sanitized_child_import_proves_current_host_sdk_version_and_vendored_client
tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result
```

The recipe used child Python `/home/user/work/venv-agent-child-d22-8c3b926e/bin/python`, exact Runtime checkout `/home/user/work/wt/rt-pin-9ce4242b`, Node `v20.19.4`, profile `/home/user/work/runtimes/agent-remotion-v3-819acf-1110`, and the existing read-only schema path `/home/user/work/venv-agent/lib/python3.13/site-packages`. The report-all preflight verified absent `PYTHONNOUSERSITE`, `-I` installed origins, PEP 610 direct URLs, actual module hashes, Runtime commit/tree, profile lock/archive hashes, source/body hashes, and before/after no-write observations.

Body SHA-256 values:

```
2f8c6f0d7709ae3c84bdbcaa8c275fdd4d8534ceface9926772a6247eeecf9ae  test_remotion_host_session.py
32e8958cce8bbcae19f1771f131e043171d0ac5f62732bfdefe8a1dbcd54708d  test_generic_host_actions_v3.py
6fc57103cb5419a3616dd6c4305774d988eb19be2233acd92ae86da4feb38c83  test_worker_startup_identity.py
03d79f9ea17c6c3c899aa1268a3b9ee4f8bd21681063a2f5be018d86eb887417  test_d09_managed_scene_only.py
```

The first invocation exposed one harness setup error because it pointed the schema variable at the child venv, which does not contain the separately pinned schema package. That was corrected to the approved shared read-only schema path; no test body or assertion was edited, and the corrected single cohort passed.

No product/test/schema/client/pin/archive/dependency changes were made. No full suite or historical 3b replay was requested.

