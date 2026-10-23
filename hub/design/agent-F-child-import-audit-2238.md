## Result

Root cause is an ordinary child-environment provisioning gap:

- Controller imports `runtime_protocol` from Runtime checkout `8ea0766f` via `PYTHONPATH`.
- Sanitized children receive Agent source plus admitted site-packages, but the current shared `venv-agent` has no `runtime-protocol`, `astrid-runtime`, or `astrid-runtime-client`.
- Import-only control reproduced this with the same interpreter: controller succeeds; sanitized child fails with `ModuleNotFoundError: No module named 'runtime_protocol'`. Adding schema site-packages does not help.
- Owner: child-environment/bench provisioning. No product security guard or source changes were made.

Affected records:

- 60 `test_generic_host_actions_v3` child phases: 53 direct import failures and 7 child-startup/no-marker failures with the same cause.
- 2 additional startup/import nodes:
  - `tests/core/execution/test_remotion_host_session.py::test_two_public_command_workers_settle_task_leases_then_host_drains_original`
  - `tests/core/execution/test_worker_startup_identity.py::test_sanitized_child_import_proves_current_host_sdk_version_and_vendored_client`
- 2 `tests/core/pack/test_source_setup.py` call failures.
- 3 D09 nodes:
  - `test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[saved]`
  - `... [candidate]`
  - `test_public_checkout_check_uses_retained_managed_scene_result`

D09 is the same child-runtime import issue, not a new source-binding problem. All three preserved stderr logs have SHA-256:

`f9c2f483501941a10fde1b7f50b03d11df472da1bb0c981827f46da28f93c37d`

## Bench request

Issued exactly one current-tuple request:

```text
venv-agent-child-f-post-g5-c36-abd47
agent=c36ca8c94b695b0e25b7d42c89f194661f187423
runtime=abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e
base=full-current-v3-1229
remotion=agent-remotion-v3-819acf-1110
```

The dispatcher consumed and refused it because:

```text
FileNotFoundError: /home/user/work/bench-store/owner.json
```

No child venv was created or qualified. Existing F1012/D22 venvs remain correctly treated as old tuples.

## Tests and custody

- No test bodies were run; only bounded import controls were executed.
- Existing full service `agent-full-post-g5-2225-1023222822-25691` remains running; it was not stopped, retried, or duplicated.
- Worktree remains clean at `c36ca8c94b695b0e25b7d42c89f194661f187423`.
- Commit message written and `DONE` marker created.

Unknown: whether a fresh current-tuple child venv resolves all failures, because the authorized request was refused before provisioning.