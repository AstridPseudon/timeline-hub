# Agent full21969: unclassified owner disposition

Date: 2026-10-21 UTC. Read-only classification of the retained run; no test
was rerun and no source, test, dependency, fixture, suite, or environment was
changed.

## Evidence and identity boundary

Retained result:

    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-venv-agent-child-published14-b9797941-full-1021045238-21969

Retained command:

    env -i ... ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
      PYTHONPATH="$PWD:/home/user/work/runtime" ... \
      /home/user/work/venv-agent-child-published14-b9797941/bin/python \
      -m pytest -q -n 3

Retained result is unchanged: **138 failed, 15,840 passed, 456 skipped,
4 xfailed, 4 errors** (565 subtests passed; exit 1). The executed Agent
source is commit `cc37291af12ac6504eb48dd71ea39b9dfdb56d71`, tree
`0698a30b3eb42d47db84ed5ed2e21221158795c4`. The child is
`venv-agent-child-published14-b9797941`, Python 3.13.16, installed marker
`b97979411`; it lacks `runtime_protocol`/`astrid_runtime` after child
environment sanitization. The retained Runtime input is checkout commit
`b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
`6abc2f117391de8e7e35c0283f575a002199894d`.

This disposition does not reinterpret the retained run as a qualification and
does not claim that the current integration HEAD (`a08a500077c7551fa8455b936d82adc2aae08f41`
in this worker) has these failures. Its only
pass provenance is the same retained source snapshot's 15,840 passing tests;
there is no independent current-base pass/fail result for any node below.
The existing child-environment and Viewing handoffs remain authoritative for
the DIRECT/DERIVED missing-`runtime_protocol` sets and for the rendering
subset. In particular, missing Runtime elsewhere is not used to classify the
nodes below unless their own retained first cause says so.

The 32 nodes below are exactly the exhaustive partition's 31 failures plus one
error. They are disjoint from the 73 DIRECT and 37 DERIVED nodes.

## Repair groups

### 1. Agent custody/platform boundary hygiene — source failure

Owner: Agent execution/platform. The `root_preparation.py` violation is
Viewing-owned rendering code; `outbox.py` is Agent-owned. The retained first
causes are concrete assertions or source scans, not the generic child import
failure.

Nodes and first causes:

```text
tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[command]
  test line 189: observed["denied"] was False, expected True.
tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine]
  test line 189: observed["denied"] was False, expected True.

tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[identity-register]
tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[identity-bind-launch]
tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[inheritability-register]
tests/core/execution/test_pidfd_callers.py::test_custody_post_open_failure_closes_untransferred_handle[inheritability-bind-launch]
  test line 138: patched os.close was called zero times, expected once with fd 73.

tests/core/execution/test_platform_boundary.py::test_agent_native_process_and_lock_boundary
  test line 70: source scan found os.getuid at
  astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:48,
  and fcntl import/flock at astrid/sdk/timeline/outbox.py:4,35.

tests/core/execution/test_platform_helpers.py::test_windows_attempt_directory_is_private_from_creation[False]
tests/core/execution/test_platform_helpers.py::test_windows_attempt_directory_is_private_from_creation[True]
  test line 85: root existed but the patched private_directory helper was
  never called (created == []).
```

Relevant later targeted command (after a coherent Agent+Runtime profile is
available):

    python -m pytest -q tests/core/execution/test_custody_broker.py tests/core/execution/test_pidfd_callers.py tests/core/execution/test_platform_boundary.py tests/core/execution/test_platform_helpers.py

### 2. Generic-host lifecycle assertions — insufficient evidence, likely
child-profile/setup-adjacent

Owner: Agent execution. These terminal blocks show an assertion before a
useful child traceback, so they are not classified as environment-only or
source-owned. The malformed child profile is a plausible contributor because
the same file has neighboring DIRECT/DERIVED missing-module failures, but that
is not proof for these exact nodes.

Nodes and first causes:

```text
tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-False]
tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-True]
  test line 1497: cancellation observed zero receiver URLs, expected one and
  no active processes.

tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-False]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-True]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-False]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-True]
  test line 1770: the child never created the shutdown-entered marker within
  the ten-second wait.

tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_cannot_close_unproved_real_attempt[observation]
  test line 1816: the child never created the uncertain-shutdown-entered
  marker within the ten-second wait.
```

Relevant later targeted command:

    python -m pytest -q tests/core/execution/test_generic_host_actions_v3.py -k 'managed_review_cancel_retires_only_observed_owner_and_preserves_drift or cpu_shutdown_waits_for_real_original_attempt_release or cpu_shutdown_cannot_close_unproved_real_attempt'

Disposition gate: first establish a hermetic child import probe for the
selected Agent+Runtime pair; only then decide whether these are product fixes
or environment/setup fallout.

### 3. Rendering conformance result production — insufficient evidence

Owner: Viewing/rendering qualification. The six nodes fail at the shared SDK
consumer, not at a retained renderer assertion: `tests/core/rendering/test_conformance.py:108`
cannot read `sdk/result.json`. The retained log does not preserve the SDK
child stderr for these nodes, so the first cause is only “producer did not
leave result.json”; it is insufficient evidence for either a source repair or
an environment-only disposition. The existing Viewing handoff explicitly
keeps these six separate from the rendering nodes whose child stderr names
missing `runtime_protocol`.

Nodes:

```text
tests/core/rendering/test_conformance.py::test_minimal_render_wire_parity
tests/core/rendering/test_conformance.py::test_request_sensitive_support_wire_parity
tests/core/rendering/test_conformance.py::test_passthrough_audio_wire_parity
tests/core/rendering/test_conformance.py::test_no_audio_wire_parity
tests/core/rendering/test_conformance.py::test_attachment_wire_parity
tests/core/rendering/test_conformance.py::test_intentional_failure_wire_parity
```

Relevant later targeted command:

    python -m pytest -q tests/core/rendering/test_conformance.py

Do not make a Scene/evaluator repair decision from these six until the
producer's child stderr and a coherent profile are available.

### 4. Installer snapshots and Remotion lock — source failure

Owner: Agent installer/packaging, with Viewing/Composition consultation for
the published Composition/Schema lock entry. The first causes are deterministic
source/fixture mismatches, independent of the missing child Runtime import.

Nodes and first causes:

```text
tests/test_installer_platforms.py::test_service_definitions_match_reviewed_snapshots[darwin-launchd.plist]
tests/test_installer_platforms.py::test_service_definitions_match_reviewed_snapshots[linux-systemd.service]
tests/test_installer_platforms.py::test_service_definitions_match_reviewed_snapshots[win32-task.xml]
  test line 73: rendered service text has one fewer trailing newline than the
  reviewed fixture.

tests/test_installer_schema.py::test_remotion_lock_pins_the_transitive_schema_package
  test line 101: package-lock lacks
  packages["node_modules/@banodoco/timeline-schema"] (KeyError).
```

Relevant later targeted command:

    python -m pytest -q tests/test_installer_platforms.py tests/test_installer_schema.py

### 5. Public boundary, client contract, and RLE setup — mixed disposition

Owner: Agent public boundary/runtime-client for the first five nodes; Agent
test/fixture integration with Viewing for the RLE node. These are grouped as
one boundary qualification task but must not be repaired as one undifferentiated
failure:

```text
tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[status-healthy-local]
  test line 141: expected exit 0, got 1; retained stderr explicitly says
  ModuleNotFoundError: No module named 'runtime_protocol'.
  Classification: ENVIRONMENT for this node, based on its own retained cause.

tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[status-unavailable-shared]
tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[status-unknown-local]
  test line 142: expected stderr empty, retained stderr explicitly reports
  missing runtime_protocol. Classification: ENVIRONMENT for these nodes,
  based on their own retained cause; the expected exit-code assertion passed.

tests/test_public_boundary.py::test_actual_cli_diagnostics_conform_to_bundle[doctor-unknown-shared]
  test line 142: retained stderr reports
  UnboundLocalError: RuntimeCLIError is not associated with a value.
  Classification: INSUFFICIENT EVIDENCE for ownership because the retained
  block has no traceback chain; it is not folded into missing Runtime.

tests/test_generic_host.py::test_vendored_runtime_client_timeout_is_bounded_and_request_correlated
  test line 1511: monkeypatched timed_out expects (_opener, request, *,
  timeout), while generated.py:637 calls _urlopen_loopback(request,
  timeout=...), producing TypeError for the missing request argument.
  Classification: SOURCE/API-contract failure, Agent client ownership.

tests/sdk/test_scene_real_public_summary_rle.py::test_real_public_scene_answers_reach_rle_summary
  setup line 51: fixture native_host not found; available fixtures do not
  include it, and the test body never ran. Classification: INSUFFICIENT
  EVIDENCE at the fixture/plugin boundary, not a Scene/RLE source failure.
```

Relevant later targeted commands:

    python -m pytest -q tests/test_public_boundary.py -k actual_cli_diagnostics_conform_to_bundle
    python -m pytest -q tests/test_generic_host.py -k vendored_runtime_client_timeout_is_bounded_and_request_correlated
    python -m pytest -q tests/sdk/test_scene_real_public_summary_rle.py::test_real_public_scene_answers_reach_rle_summary

The RLE command is a setup check only until the provider/plugin that defines
`native_host` is identified.

## Handoff and next steps

No full or named suite was requested by this worker. No targeted test was run.
The next qualification should provision a coherent private Agent+Runtime
installed profile, record the exact Agent source identity, run the five
targeted commands above, and then update these dispositions from evidence.
Do not replace the retained `138 failed / 4 errors` result or its source
snapshot identities with that future result.
