# Agent D13 current-preserving source candidate

## Result

Prepared the source-only D13 candidate in worker
`agt-m2-d13-reviewed-current-source-forward-1208`.

- Candidate base: `6ae4a1f91f7af02aca6e3980c42d08d084450855`, tree
  `aaa1e671a4d43ce2dd0d11aee0e727ee43892d6a`.
- True merge parent recorded for the harness: `c9ac7c7b0e862ad32a919db33859c5fcbf58ad99`, tree
  `cab0a2aa34ba6dae880657eb484979039e206049`.
- Common current parent used for the working-tree-only join:
  `566307478f43672db23f84fda2a478bb6116a008`.
- Projected resolved candidate tree: `59a4430da5caee66b731cdf4c674e8de8d90e9f1`.
  The harness should commit this tree with parents `(6ae4a1f91, c9ac7c7b0)`.

No integration merge, checkout, rebase, generated-file regeneration, install,
wheel build, native process, HTTP/socket, renderer, browser, or full suite was
run.

## Exact source inventory

The post-`f4edcb4b` reviewed security allowlist is 11 paths. Their candidate
blobs are:

```text
astrid/core/execution/generic_host.py db248339441fe27ead98610138c0a2841e1b3fea
astrid/core/rendering/_effect_registry.py 1e8f14fd341262accd57029f3ba384ab12c73400
astrid/core/rendering/_registry_origin.py 2edcab5aeff228f8bc76d8deb09d2df92ac6c4c4
astrid/core/rendering/remotion_runtime.py 510ca6ac61a11f8f329997da88492e81843d9a2a
astrid/packs/rendering/rendering/renderers/remotion/run.py 69d786993b53a006b3b2c79bbc3cbba0fcfaac7c
astrid/sdk/host_bootstrap.py a74e94ee3be2059b5867b2a34e17205d4d67eab7
scripts/gen_effect_registry.py 75c3331e1c06443e98bda58a8eae7bc5e2bd783a
tests/core/rendering/test_effect_registry_carrier.py b0d065367c1521268756383e45457b88fa90198a
tests/core/rendering/test_installed_registry_security.py 93eb844d48a95d43e43a392412063c57d38274af
tests/core/rendering/test_remotion_registry_context_key.py c6f51f2ebb03465be4b092f3ac30cbdaa1e7a911
tests/test_generic_host.py 4f0f479cdf9aeba852a571781373e8ff48e699c9
```

The previously reviewed nine-path current-forward D13 port is also retained
where it is not already in that security allowlist. These eight retained
consumer/source paths are deliberately not replaced by current's absence:

```text
astrid/core/contracts/runtime_orchestration.py 0d249cb54cb37e46b524e22d8e00878d0fb26d96
astrid/packs/rendering/actions/assemble_timeline/run.py 6bfce1c1cf0e68dd7eb32a14e3f4a01087727381
astrid/packs/rendering/pack.yaml fc4849329629194681e80e2e9f8b929ef37b640f
astrid/sdk/timeline/assembly.py 599dc1f2b85a8b6a3667b54b293bde238ba76900
astrid/sdk/timeline/sync.py 2c000a86fd8170991e084b7f39f98e4f1b045d47
tests/packs/video_editing/test_runtime_publication_chain.py bdecd286e1cfc0dc19a8f3ce2bbf0b797be0b161
tests/sdk/test_timeline_assembly.py 615ff8c08e364f4b401827d822251448a7ec4d81
tests/sdk/test_timeline_sync.py f59189d429fb96ed285c1fdd33d427b1d0d1f885
```

`generic_host.py` is the one overlap between the earlier nine-path D13 port
and the later 11-path security allowlist; the exact `6ae` candidate blob above
was retained. No unresolved overlap remains.

Mechanical custody result: the union of these 19 paths is byte-identical to
the reviewed candidate base; every other one of the 3,274 tracked paths is
byte-identical to current public `c9ac7c7b0`. The comparison found zero
mismatches. `git diff --check` passed. Runtime lock, artifacts, CLI surface,
package, schema, and other pin paths were unchanged between the two input
trees and remain unchanged in the candidate.

## Evidence

Direct source/custody/host projection checks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-d13-reviewed-current-source-forward-1208/pytest-d13-source \
  tests/core/rendering/test_effect_registry_carrier.py \
  tests/core/rendering/test_installed_registry_security.py \
  tests/core/rendering/test_remotion_registry_context_key.py \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_strips_source_pythonpath_and_probes_selected_interpreter \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_refuses_checkout_origins_from_isolated_probe \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_does_not_use_ambient_runtime_checkout \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_origin_probe_resolves_without_product_imports \
  tests/sdk/test_host_bootstrap_source_identity.py::test_python_source_loader_can_read_cache_before_bytecode_write_policy \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter \
  tests/sdk/test_installed_runtime_source_identity.py
57 passed in 66.24s; exit 0
```

The host projection/manifest/publication subset was:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-d13-reviewed-current-source-forward-1208/pytest-d13-host \
  tests/test_generic_host.py -k 'discovery_digest_and_truthful_preflight or claim_only_admits_capabilities_that_are_currently_ready or launch_worker_projection_matches_fixed_execution_context or installed_worker_registry_projection_matches_host_without_second_root or readiness_preserves_network_guard_in_final_command_popen_environment or launch_worker_projects_fixed_registry_selectors_and_transport_filter or launch_command_projection_matches_actual_final_context' \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_legacy_assembler_admission_refuses_before_execution_and_keeps_artifacts
8 passed, 238 deselected in 28.49s; exit 0
```

These are source and custody evidence only. The exact next installed
preflight is the existing
`tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight`,
using one coherent exact Agent/Runtime/client installed pair, selected
interpreter/profile, source closure, RECORD, tool, and resource bindings.
Native proof and the RT07 cut remain **HELD** until that preflight and all
fresh prerequisites are approved; this candidate does not claim either.
