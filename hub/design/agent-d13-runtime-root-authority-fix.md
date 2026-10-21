# D13 Runtime root authority fix — BLOCKED on the existing launch carrier

No product changes made. The rejected Agent commit remains
`6c37224ed18fdbb3d90ae5f472629205ba9b6d5c`, tree
`36e9bc966687c41dd49aa3f271789bc46da37aec`. It remains unsafe and must not be
adopted. This report follows the task's explicit instruction to report the
exact carrier gap before inventing a field.

Read PLAN.md, repository AGENTS.md, and
`agent-d13-real-source-context-security-review.md` fully. Inspected the actual
required Runtime pin `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` read-only.

## Concrete gap

1. In that Runtime, `astrid_runtime/bootstrap.py:125` has
   `SourceProfile.runtime_checkout`, but `BootstrapResult` at line 261 does
   **not** have it or an equivalent bound Runtime source identity. Its
   `source_profile` is just the profile name (`"astrid"`). The successful
   reconnect/start/connect constructors at lines 874, 1009, and 1047 forward
   only `source.source_checkout`, not the Runtime checkout or its identity.
2. `astrid_runtime/cli.py:200` serializes the dataclass using `asdict`.
   Consequently, this is not solely an Agent allowlist omission: adding
   `"runtime_checkout"` to Agent `_lifecycle_result` cannot forward anything
   from the supported pinned launcher's actual output.
3. The existing Runtime SourceProfile is deliberately provenance, not Runtime
   import authority. `_validate_source_profile` at
   `astrid_runtime/bootstrap.py:341` explicitly says "Reject source metadata
   that attempts to become runtime authority." It checks an absolute,
   symlink-free Runtime pathname, but does not require existence or bind
   Runtime code. `LocalRuntimeBoundary._validate_source` at
   `astrid_runtime/runtime_boundary.py:180` explicitly documents that the
   Runtime/generated client are installed dependencies and the checkout is
   provenance, never an import/launch fallback. Its implementation likewise
   accepts a nonexistent Runtime checkout. The bounded probe below verifies
   both validators accept one while the real imported Runtime is 95bd3c5f.
4. Agent `_lifecycle_result` at `astrid/sdk/autobootstrap.py:295` carries the
   existing worker credential, Agent source checkout, and Runtime instance
   metadata. These do not select or bind a Runtime executable source root.
   `_manifest_from_environment` explicitly delegates profile reading and
   trust validation to the neutral launcher; privately rereading a caller's
   manifest would bypass that boundary.
5. `_host_render_environment` at `astrid/sdk/host_bootstrap.py:740` copies
   ambient environment. `_startup_identity_attestation` at
   `astrid/core/execution/generic_host.py:5084` binds the Agent source/closure,
   target and boot manifest, not a selected Runtime source identity.
   `_host_product_import_origins` at line 1305 preserves current import
   resolution during VibeComfy setup; it does not associate that resolution
   with the launcher-selected SourceProfile. Treating that observation as a
   SourceProfile selection would invent the missing authority relationship.
6. The parked path has a real `DeploymentReference.dependency_closure` and
   `ProjectedLaunch.deployment_digest`, but the ordinary autobootstrap path
   does not receive those. Their existence does not repair the ordinary
   launcher JSON handoff or the direct D13 host setup.

The premise that the supported profile already provides **bound Runtime
source authority** is therefore not borne out by the required pin. The field
exists as provenance; the trusted projection and executable identity binding
do not. This needs a Runtime-owner/orchestrator decision before an Agent-only
implementation can meet the requested condition. No replacement DTO, token,
environment assertion, path allowlist, package/version check, or parallel
profile reader was invented.

## Bounded reproduction

Retained script:
`orch/workers/agt-m2-d13-runtime-root-authority-fix/probe.py`.
It creates and automatically removes private temporary fixtures, never
touching shared dependencies or opening live sockets.

Exact command, run from the assigned Agent worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-d13-runtime-root-authority-fix/probe.py
```

Exit 0: all counterexample assertions reproduced. Observations:

- Loaded Runtime origin was the real `rt-pin-95bd3c5f/runtime_protocol/__init__.py`.
- Supported Runtime profile validators accepted a nonexistent Runtime root.
- Actual BootstrapResult wire projection omitted `runtime_checkout`.
- Agent projection also dropped a hypothetical extra `runtime_checkout`.
- Nonexistent, existing foreign, and symlink Runtime roots became import paths
  in both worker probe environments and the public renderer overlay.
- Fresh worker and renderer Python children actually imported the attacker's
  `runtime_protocol` for both existing foreign and symlink variants.

These are successful reproductions of the vulnerability, **not passing
security-negative regressions**. No permanent regression or fix is claimed.

## Direct strict security neighbours

Exact command, run from the assigned Agent worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/core/execution/test_generic_host_actions_v3.py::test_v3_worker_probe_matches_actual_readiness_context \
  tests/core/execution/test_generic_host_actions_v3.py::test_v3_startup_probes_omit_credentials_without_task_authority \
  tests/core/execution/test_generic_host_actions_v3.py::test_v3_startup_probes_reject_fixed_undeclared_secret \
  tests/core/execution/test_generic_host_actions_v3.py::test_v3_worker_probes_match_exact_host_roots_and_exclusions \
  tests/core/rendering/test_remotion_registry_context_key.py::test_render_in_an_unvalidated_context_is_still_refused \
  tests/core/rendering/test_transport.py::test_absolute_executable_symlink_is_preserved \
  tests/core/rendering/test_transport.py::test_test_harness_isolates_pack_source_inventory \
  tests/packs/rendering/test_render_export_task_adapter.py::test_launch_validation_rejects_context_or_foreign_launch_without_fallback \
  tests/packs/rendering/test_render_export_task_adapter.py::test_launch_validation_missing_reference_does_not_spawn \
  tests/packs/rendering/test_render_export_task_adapter.py::test_clean_probe_rejects_unsupported_consuming_overrides \
  tests/packs/rendering/test_render_export_task_adapter.py::test_parent_owned_reference_survives_worker_and_renderer_filters \
  tests/packs/rendering/test_render_export_task_adapter.py::test_registry_generator_custody_refusal_preserves_primary_and_no_state_publication \
  tests/packs/rendering/test_render_export_task_adapter.py::test_registry_readiness_qualifies_actual_canonical_transport_projection \
  tests/stage1/test_cold_launch_autobootstrap.py::test_envless_bootstrap_never_infers_checkout_authority \
  tests/stage1/test_host_bootstrap_manifest_luna.py::test_host_bootstrap_refuses_noncanonical_runtime_worker_handoff_before_use \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_refuses_checkout_origins_from_isolated_probe \
  tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_refuses_worker_credential_outside_the_pack_host_contract
```

**39 passed, 8 warnings in 28.74s**, exit 0. Warnings are the existing Python
3.14 tar extraction deprecation in the private readiness fixture. This is
unchanged-tree neighbour evidence, not approval of the vulnerable tree.

## Required next step / limits

The Runtime owner should identify an existing trusted launch projection that
can carry the selected Runtime dependency's executable source identity into
the ordinary Agent host launch, or the orchestrator must explicitly authorize
the missing projection work. It must bind actual canonical existing,
symlink-free origin/identity, not merely export SourceProfile's provenance
string. Clarify how that identity is bound for the direct D13 GenericPackHost
launch as well as autobootstrap before introducing an Agent carrier.

Once that gap is resolved: implement the narrow projection/boundary fix, add
permanent negatives for caller/env/foreign/nonexistent/symlink roots and
positive parent/worker identity equality, run those and direct strict
neighbours, then request only `d13-native-positive-render-integration` on the
new exact tree. Independent security review remains required before adoption.

No central suite requested: there is no corrected/new source tree to qualify.
The original native95/C13 node and old 10910 positive were not reused or
claimed as approval. No full suite, broad neighbours, old7012, browser suite,
TLS/CA changes, version changes, shared-dependency writes, PID fallbacks,
weakened assertions, or repo design files. All proposal/outbox/retry/history/
render/ffprobe/undo assertions and product files remain unchanged.
