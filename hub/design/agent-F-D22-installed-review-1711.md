# F-D22 installed handoff fixture review — 1711

Verdict: **PASS** for faithful unit-fixture isolation and honest coverage.

This PASS is for the original unit's host-bootstrap handoff contract, not a
claim that the full installed Remotion renderer transaction is qualified. The
prior 1653 failure classification remains correct for that separate renderer
gate; it is outside this unit's promise and was not waived or relabelled.

## Reviewed source and scope

- Candidate: `4faad4bcb952cb71ea437e8441cdfa883dc9044e`
- Base/integration: `63baa707b4bce52b36c06dc3345d2fd357b10f66`
- `git log 63baa..4faad`: exactly one commit, the candidate's own
  `test(F-D22): isolate installed handoff fixture render validation`.
- `git diff --name-status 63baa..4faad`: exactly one path,
  `M tests/sdk/test_host_bootstrap_source_identity.py`.
- No production, contract, generated, pin, lock, report, or product files are
  in the candidate diff.

The fixture still exercises the real `host_bootstrap.ensure_pack_host` caller
and handoff path. It changes only this test's independent
`_prepare_render_validation` collaborator. The fake source root is not an
installed distribution, so invoking the real installed-renderer validation
transaction there would test a mismatched external precondition rather than
the host handoff unit. The isolated collaborator performs the expected second
managed-source-inventory read when the supported Remotion profile is present,
then returns no validation marker. The dedicated installed-registry controls
remain real and separate.

## Preservation audit

Independent AST/source audit results:

- Changed target function AST: expected change, base SHA-256
  `8c72537c41c2bcb2b20c33439277a0844a22fcd77eab0c2e4d0b6d4a1245df20`, current
  `c33ddc7780351440d1f2f76ec5bb7502f5755a06a1a363566a95893c9c4242a0`.
- `test_bootstrap_passes_inventory_identity_and_restarts_on_change` AST:
  identical.
- `_materialize_source_closure` AST: identical.
- All other function ASTs: identical.
- Original assertion inventory: **31 base / 31 current**, exact AST equality
  (4 assertions in the target function plus 27 in the reused helper).
- Production guards are byte-identical to `63baa`:
  - `astrid/sdk/host_bootstrap.py` — `50e73b1a9b95528dc06192e0102caad55ec7192b5369ff8a6698cb14c70a0b07`
  - `astrid/core/rendering/remotion_runtime.py` — `84a495de2139c74b22c001094a3bb4d9252803f11715d7803054ecc2f9cc617e`
  - `astrid/core/rendering/_registry_origin.py` — `47af6b12421f44d943a2c00621fc2b08a3d0f2d29fbd66b3c150a328bed88ca2`
  - `astrid/core/rendering/_effect_registry.py` — `a6938299241c6b21b8e882d812cf369e143636b40c72f841b547668db711aa85`
  - `astrid/core/source_identity.py` — `5236481dab209f8803fe9dcd2c93c1610b664bea2102e4370148273ffa4b9a32`

## Authentic target run

The worker1659 harness body was copied without changing its tested body; only
its output directory and `TMPDIR`/script path were redirected to the reviewer's
private `/tmp/w-ac8af09866/fd22-target-run`. The exact command was:

```sh
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent-child-d22-8c3b926e/bin:/usr/bin:/bin PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-9ce4242b" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9ce4242b ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-ac8af09866/fd22-target-run/fd22-pytest /home/user/work/venv-agent-child-d22-8c3b926e/bin/python -P /tmp/w-ac8af09866/fd22-target-run/run-target.py
```

Result: **1 passed in 0.86s**, exit 0. Environment custody was honest and
unchanged before/after; installed imports resolved from the child venv's
site-packages; 1,507 installed files were measured. The observer recorded
`host_status=ready`, three launches, `-I -m` each time, no child
`PYTHONPATH`, a cwd unrelated to the fake source root, and two retired hosts.
Inventory calls were exactly
`['inventory-1', 'inventory-1', 'inventory-2', 'inventory-2', '', '']`.

The second inventory read is deliberate. Production `_prepare_render_validation`
enters the Remotion registry-context path, whose real discovery reads the
managed source inventory. The isolated collaborator repeats that observable
read without pretending to execute installed-registry validation on a fake
non-installed tree. Its `None` result is therefore an explicit unit-fixture
boundary, not hidden renderer evidence.

## Exact nine controls

The command from `controls-command.sh` was run with the same environment and
only the reviewer's private `TMPDIR` path:

```sh
/home/user/work/venv-agent-child-d22-8c3b926e/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_strips_source_pythonpath_and_probes_selected_interpreter tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_refuses_checkout_origins_from_isolated_probe tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_does_not_use_ambient_runtime_checkout tests/sdk/test_host_bootstrap_source_identity.py::test_installed_origin_probe_resolves_without_product_imports tests/core/rendering/test_installed_registry_security.py::test_installed_launch_binding_uses_selected_distribution_instead_of_sdk_caller_tree tests/core/rendering/test_installed_registry_security.py::test_installed_preflight_uses_existing_closure_without_importing_carriers 'tests/core/rendering/test_installed_registry_security.py::test_installed_probe_must_refuse_unbound_tree_or_alias[foreign-tree]' 'tests/core/rendering/test_installed_registry_security.py::test_installed_probe_must_refuse_unbound_tree_or_alias[symlink-alias]' tests/core/rendering/test_installed_registry_security.py::test_installed_missing_carrier_must_fail_in_live_settler
```

Result: **9 passed in 1.36s**, exit 0. No 109/113/full/browser suite was run.

## Quality and integrity checks

- `env PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-ac8af09866/fd22-target-run/ruff-cache /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline` — **2149 current / 2149 baseline**.
- `env PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-ac8af09866/fd22-target-run/mypy-cache-2 /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline` — **1912 current / 1912 baseline**.
- `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — **pass**, manifest matches.
- `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — **pass**, artifacts current.
- `git diff --check` — **pass**.

## Contract and limits

This is a test-only delta. It changes none of the v2 request/reply contract:
the request's `api_version`, project/timeline IDs, base revision/publication
IDs, commands, label, full step fields, `fields|atomic` merge, declared reads,
idempotency key, `dry_run`, source/rationale/group ID; accepted/merged
canonical+receipt replies and records/bindings/effects/dependencies/history/
undo steps; preview `would_status`; or structured error code/path/head/hint/
suggested command.

No repair, guard weakening, skip/xfail, generated/pin/lock/environment change,
daemon, manual provisioning, merge, or Git write was performed. The remaining
unqualified item is the separate full installed Remotion render transaction;
the nine strict installed-registry/neighbor controls are evidence for their
own promises, not substitute renderer E2E evidence.
