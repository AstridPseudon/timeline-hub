# D13 selected installed contract: final independent source review

**APPROVE — bounded SOURCE contract only. No D13 or installed-launcher qualification is claimed.**

Reviewed `tl/agt-m2-d13-preimport-cache-fence-fix` at final committed Agent
`c2ba60bebc5edeff80c5cfbcf0e8e16b70e69bf4`, tree
`ae043b0dbafeded00374ad376388c41aa1a671df`. The assigned review worktree's
HEAD and tree equal that base. No product or test files were changed.

Read PLAN.md, repository AGENTS.md, the task's shared-dependency read-only
rules, `runtime-d13-trusted-installed-boundary-0451.md`,
`agent-d13-installed-authority-security-review.md`, and
`agent-d13-installed-source-order-triage.md`; also checked the earlier
real-source-context review and Runtime's installed-authority response.
No settled decision was changed.

## Authority and verdict

The authority is the selected private `runtime_environment`, its coherent,
non-editable, immutable installed Runtime/client/Agent set, and the trusted
controller entry. Checkout fields remain provenance; an Agent installed-host
handoff must name the actual installed product root rather than select an
alternative checkout. This preserves Main's trust assumption and PLAN's cut
of additional attestation machinery.

Within that boundary I found no remaining concrete wrong-environment or
foreign cache-search-path defect in the reviewed Agent projection. This is
an origin/selection and existing process-custody conclusion, **not proof that
Python executes authenticated source bytes**. It does not expand the ordinary
Runtime controller's guarantees or certify the actual installed proof setup.

## Supported source guarantees

| Concern | Source conclusion |
|---|---|
| Selected interpreter and tree | `host_bootstrap.py:102-123` preserves the selected venv executable spelling. `_installed_execution_origins` at `:705-768` runs that interpreter with `-I`, neutral cwd and an environment without `PYTHONPATH` or `ASTRID_RUNTIME_CHECKOUT`. Required origins must be real absolute files under the selected tree, without symlink components. |
| Runtime/Agent/client origin closure | The probe checks host, child, action, client, SDK, `runtime_protocol`, its platform module, and `astrid_runtime`. It resolves each parent with explicit `PathFinder` searches, checks exact source origins and package search locations, rejects namespace-only entrypoints and symlink aliases, and scans both Runtime package trees for symlinks. It does not import a product measurement helper or dotted product parents. This closes the earlier Runtime-origin omission and the probe's incidental-parent-import finding. |
| Direct isolated host guard | `execution/__init__.py:3-6` calls `verify_installed_host_startup` before Runtime-dependent execution imports. `source_identity.py:102-124` restricts this guard to the actual isolated `-m astrid.core.execution.generic_host` startup, binds `--source-checkout` to its installed tree, rechecks Runtime origins and compares the existing closure digest. Ordinary source launches keep their existing later startup identity checks. |
| Existing source measurements | `source_identity.py:29-75` retains the existing component scheme and adds both adjacent Runtime trees when present. Component symlinks are refused; source-checkout, closure, inventory, target and boot bindings remain in the existing startup/readiness flow. `_startup_identity_attestation` remains before host construction, discovery and registration (`generic_host.py:13628` onward). |
| Ordinary and foreground actor | `ensure_pack_host` at `host_bootstrap.py:1393-1411` probes installed origins and requires exactly the existing `astrid-pack-host` actor and scope tuple. Foreground also requires its selected interpreter to match the current interpreter. It enters the same `_cli` and identity/readiness flow through `run_pack_host_foreground` (`:1781-1797`), with the Runtime-owned process and normal worker credential; no extra actor or authority is introduced. |
| No ambient Runtime checkout fallback | `_host_render_environment` removes `PYTHONPATH` for installed hosts; the direct host uses `-I` and a support cwd. Parked installed preparation repeats the selected-origin check and removal. Worker/readiness/renderer/registry changes in `38281f727` remove the unbound Runtime-root insertion and Remotion `sys.path` fallback. `subprocess_env.py` no longer propagates `ASTRID_RUNTIME_CHECKOUT`; renderer transport uses the canonical filter. Paths derived from the already selected Agent tree and admitted dependencies are distinct from an ambient checkout fallback. |

The reviewed Agent source scope was `astrid/sdk/host_bootstrap.py`, relevant
`sdk/autobootstrap.py` handoff code, `core/source_identity.py`,
`core/execution/__init__.py`, GenericHost's source identity, projection,
startup and service-entry paths, `core/subprocess_env.py`,
`core/rendering/transport.py`, `core/rendering/remotion_runtime.py`, and
`astrid/services.py`. Relevant tests and the three repair diffs were read.
Runtime controller/services code was read with `git show` at the peer's exact
`b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
`6abc2f117391de8e7e35c0283f575a002199894d`; this was not a Runtime execution.

## Explicit limits retained

The ordinary `astrid-runtime up` daemon command does not use `-I`/`-S` or
carry an admitted source digest/import binding. Runtime's daemon spawn
inherits its configured controller environment; services strip
`PYTHONPATH`/`PYTHONHOME` and use the declared service cwd. Consequently this
approval does not assert universal isolation of an arbitrary controller
invocation from a foreign shell cwd, Python startup configuration or prior
imports. The trusted controller/coherent installed-entry prerequisite must
hold in the manager's normal installed proof. No new checkout authority is
derived from these upstream launch mechanics.

The foreground service imports installed code before the subsequent closure
measurement and does not traverse the isolated direct-host guard. There is
no ordinary pre-import byte-attestation carrier to compare against there.
This remains a limit, not a missing feature to replace with circular
self-validation in this task.

`_source_digest` still excludes `__pycache__`. A `.py` origin and
`SourceFileLoader` can execute an accepted cache; `-B` suppresses writes,
not reads. The trusted loader-source regression confirms that limitation.
No new cache redirection was found under the coherent immutable installed-run
assumption. An inconsistent or hostile pre-existing cache, active replacement
before controller entry, post-measurement writes/TOCTOU, and native/OS byte
protection are not established by these checks. The earlier cache and
pre-entry findings therefore remain valid against a stronger byte-security
claim; they are not blockers for this clarified bounded SOURCE contract.
The earlier foreign/symlink Runtime-origin finding was a real selection defect
and is addressed by the origin/closure repair, independently of that scope
clarification.

## Executed checks

From the assigned worktree, this exact compact trusted selection ran:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
WORKER="$ORCH/workers/agt-review-d13-selected-installed-contract-final"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp="$WORKER/pytest-tmp" \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_strips_source_pythonpath_and_probes_selected_interpreter \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_refuses_checkout_origins_from_isolated_probe \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_does_not_use_ambient_runtime_checkout \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_origin_probe_resolves_without_product_imports \
  tests/sdk/test_host_bootstrap_source_identity.py::test_python_source_loader_can_read_cache_before_bytecode_write_policy \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter \
  tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_refuses_worker_credential_outside_the_pack_host_contract \
  tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_refuses_runtime_health_without_ok_status \
  tests/core/execution/test_worker_startup_identity.py::test_startup_attestation_normalizes_and_records_exact_target \
  tests/core/execution/test_worker_startup_identity.py::test_source_closure_digest_changes_when_sdk_or_launcher_changes \
  tests/core/execution/test_worker_startup_identity.py::test_startup_fails_before_readiness_on_source_mismatch \
  tests/core/execution/test_worker_startup_identity.py::test_startup_fails_before_readiness_when_required_target_is_missing \
  tests/core/execution/test_worker_startup_identity.py::test_startup_rejects_malformed_target_before_claims \
  tests/core/test_subprocess_env.py::test_ambient_runtime_checkout_does_not_cross_child_boundary \
  tests/test_services.py::test_declaration_matches_runtime_contract_with_space_containing_paths
```

**18 passed in 1.76s; exit 0.** Log: `WORKER/trusted-targeted.log`.
These are mocked launch/origin, pure identity, service-declaration and
nonexecuting AST/loader-source neighbors. They do not prove real installed
origins or a live foreground actor. Runtime on this test-only `PYTHONPATH`
supplies dependencies; it is not installed execution authority. The shared
venv was used read-only, bytecode/cache writes were disabled, and temporary
pytest output was removed.

Also executed, both exit 0:

```sh
git diff --exit-code 091aa23ec83ea05ffd3b0115a640230d51c8c429 c2ba60bebc5edeff80c5cfbcf0e8e16b70e69bf4 -- astrid/core/execution/process_group.py astrid/core/execution/custody_broker.py astrid/core/rendering/verified_source.py tests/core/execution/test_worker_startup_identity.py
git diff --check 38281f7274bfd799d3b87275f38a0a5d14dd2c5f c2ba60bebc5edeff80c5cfbcf0e8e16b70e69bf4
```

The first confirms those existing guards and the original startup test file
are byte-identical to published Agent `091aa23ec`. The reviewed bootstrap test
delta extends the required origin-key lists and adds tests; it does not turn
a passing behavior into refusal or remove an expectation. This review left
all strict tests unchanged and added no DTO, profile, token, environment
authority, scopes, store, attestation framework or Main-infrastructure change.

No adversarial payload generation/execution, active package/cache tamper
fixture, full suite, localhost/browser/native/render/D13 run or installed
launcher rerun occurred. No historical green result is recast as evidence on
this exact source tree.

## Handoff

No bounded SOURCE blocker remains. The manager may now coordinate the one
normal installed proof on a coherent private Runtime/client/Agent set using
this approved Agent source, verifying actual interpreter/package origins and
the ordinary foreground actor. Keep D13 and native/render qualification held
until their separately authorized evidence exists. Any composed successor
must preserve these reviewed source and custody checks; this verdict is for
the exact commit/tree above.
