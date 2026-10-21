# D13 installed authority source security review

**REQUEST CHANGES — the installed-origin guard does not cover Runtime.**

Reviewed exact commit `38281f7274bfd799d3b87275f38a0a5d14dd2c5f` on `tl/agt-m2-d13-installed-authority-current-repair`, tree `e4f55a810f26946ee2d22d1cfd4ac9bd39e3eeb6`. Compared it with the rejected `6c37224ed18fdbb3d90ae5f472629205ba9b6d5c`, the prior security report, Runtime's installed-authority response, and published Agent `091aa23ec83ea05ffd3b0115a640230d51c8c429`. Read PLAN.md and AGENTS.md. No product source or tests were edited.

## Blocking finding

The proposed authority relies on `astrid/sdk/host_bootstrap.py:705–733`, but `_installed_execution_origins` probes only `host`, `child`, `action`, `client`, and `sdk`. It never validates the origin of `runtime_protocol`, its `platform` module, or `astrid_runtime`. The Runtime import used by the repaired `astrid/core/rendering/remotion_runtime.py:25` therefore lacks the advertised non-symlink installed-tree check.

A bounded reproduction using the exact candidate code succeeded:

1. Create a private Python venv in this worker's scratch directory. Copy the candidate Astrid files and generated client into its site-packages. Copy Runtime there for the baseline. No shared installation is changed.
2. Confirm the real, unmocked `_installed_execution_origins(site, selected_python)` succeeds and returns exactly the five keys above.
3. Replace only `site-packages/runtime_protocol` with a symlink to another private directory outside that installed tree. That directory contains a copy of the real Runtime package with a harmless marker appended to `platform.py`.
4. The real installed-origin guard still succeeds. The real `source_checkout_closure_digest(site)` is unchanged: `source_checkout_closure` at `generic_host.py:4115–4155` covers Astrid and the client, but omits Runtime.
5. Run the selected interpreter with `-I`, a neutral cwd, and no `PYTHONPATH`, importing the unmodified candidate `astrid.core.rendering.remotion_runtime`. Its `platform` import succeeds and exposes the foreign marker. The resolved module path is `<private scratch>/foreign-runtime/platform.py`, outside the selected site-packages.
6. Independently probe a valid installed Runtime, replace it with that symlink after the probe, and perform the same candidate import using the exact `_build_environment` projection. Foreign code is again imported.

Observed output includes:

```text
baseline_guard_keys=action,child,client,host,sdk
missing_checked_host=rejected
symlink_checked_host=rejected
symlink_runtime_source_closure=unchanged
symlink_runtime_guard=accepted
missing_runtime_guard=rejected-indirect-parent-import
runtime_replaced_after_probe=foreign-code-imported-with-transport-environment
```

This is an import-boundary counterexample, not a claim that a complete normal launcher journey succeeded. Missing Runtime currently fails indirectly while the probe imports Agent parent packages; the positive symlink case demonstrates that those incidental imports do not validate Runtime authority. The probe executes real subprocesses without mocking its result or the candidate origin checks. The private marker identifies executed foreign code; it does not simulate acceptance or rendering.

The omission predates this repair and is also present in published 091. Nevertheless, it defeats the explicit requested condition that foreign, symlinked, or replaced executable origins fail closed. The Runtime response's claim that the existing installed guard is sufficient needs this correction; removing the rejected ambient paths alone cannot establish that claim.

**Required correction:** cover the Runtime executable import closure using the existing selected-interpreter/installed-tree authority and existing launch/source guards. Reject foreign and symlinked Runtime origins before importing their code, and enforce the binding at the actual child execution boundary so replacement after an earlier probe fails closed. Add permanent negative tests for the demonstrated cases. Keep checkout fields as provenance and preserve the existing no-PYTHONPATH, neutral-cwd, isolated-interpreter, source, and process-custody rules. This does not require a new public DTO, token, environment map, or authority carrier.

## What the repair does establish

The security commit removes all six rejected ambient Runtime-root import uses: worker probe projection, readiness projection, command worker environment, capability worker environment, renderer transport, and registry generator. It removes the Remotion `sys.path` fallback and drops `ASTRID_RUNTIME_CHECKOUT` from the canonical propagated environment and registry context. Its foreign/missing/symlink environment tests pass.

No public DTO, bootstrap field, token, environment-map entry, custody bypass, or new acceptance/result fake is introduced. The security commit leaves the native integration test unchanged. Against published 091, `host_bootstrap.py`, `process_group.py`, `custody_broker.py`, and `verified_source.py` are byte-identical; the original process/source guards were preserved. Their preservation does not extend their coverage to Runtime.

The candidate and published 091 have common ancestor `6efc81500a0e0688c2bb41e736503f0fc3e04abb`; 382 is not the final composed published tree. This review covers exact candidate source, not a hypothetical merged result.

## Executed checks

Tests ran from an unmodified `git archive` export of the exact candidate under:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-d13-installed-authority-security/source
```

The shared venv was used read-only. The following prefix applies to both pytest commands:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider
```

Bootstrap/environment sweep plus the new adversarial environment cases:

```text
tests/sdk/test_host_bootstrap_source_identity.py tests/core/test_subprocess_env.py tests/core/rendering/test_remotion_registry_context_key.py tests/test_generic_host.py::test_runtime_checkout_is_provenance_not_worker_import_authority
```

Result: **85 passed in 8.05s**. This includes the reported 82-test sweep and three Runtime-checkout variants.

Rendering/projection neighbors:

```text
tests/test_generic_host.py::test_launch_worker_projection_matches_fixed_execution_context tests/test_generic_host.py::test_readiness_preserves_network_guard_in_final_command_popen_environment tests/test_generic_host.py::test_launch_worker_projects_fixed_registry_selectors_and_transport_filter tests/packs/rendering/test_render_export_task_adapter.py::test_parent_owned_reference_survives_worker_and_renderer_filters tests/packs/rendering/test_render_export_task_adapter.py::test_registry_settling_owned_generator_four_file_readback_and_unchanged_skip tests/packs/rendering/test_render_export_task_adapter.py::test_registry_readiness_qualifies_actual_canonical_transport_projection tests/core/rendering/test_remotion_registry_context_key.py
```

Result: **12 passed, 2 warnings in 9.39s**. Both warnings are existing Python tar extraction deprecations. Together these selections also cover all seven tests in the repair's focused security command.

Compact independent negative probe, from the same source directory:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python ../adversarial.py
```

Result: **exit 0, counterexample reproduced**. Reproduction script and final output are retained in this worker's directory as `adversarial.py` and `adversarial-result.txt`. Private venvs and package copies are automatically removed after each invocation. Initial probe setup attempts failed because copied Astrid lacked its source version metadata; copying the unchanged candidate `pyproject.toml` completed that bounded fixture. No guard was weakened.

```sh
git diff --check 091aa23ec 38281f7274
```

Result: **exit 0**.

No full suite, sockets, normal native/launcher run, render, browser, or old 10910 rerun was performed. Pytest's Runtime source path supplies test dependencies only; it is not evidence of installed-package qualification.

## Next step and remaining boundary

Repair the Runtime-origin coverage and replacement fence, then repeat the compact security negatives on that exact commit. The coherent private installed Agent/Runtime/client pair and Runtime `8f70a818…` normal-launcher proof remain separate and unverified. Even a subsequent source-security approval must not claim that proof or lift its hold.
