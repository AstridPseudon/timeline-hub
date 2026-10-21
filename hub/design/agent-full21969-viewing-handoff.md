# Agent full21969 -> Viewing: bounded rendering handoff

Date: 2026-10-21 UTC

## Scope and identity

This is a narrow handoff of rendering-owned failures/errors from the already
terminal central run. It is not the overall full-suite classification (owned
by `agt-m4-full21969-first-failure-triage`). No test was run, re-run, fixed,
skipped, or replayed for this note.

- Result: `agent-venv-agent-child-published14-b9797941-full-1021045238-21969`
- Source commit/tree: `cc37291af12ac6504eb48dd71ea39b9dfdb56d71` /
  `0698a30b3eb42d47db84ed5ed2e21221158795c4`
- Retained source checkout: `/home/user/work/agent`
- Executed snapshot root appearing in tracebacks:
  `/home/user/work/wt/.test-agent-venv-agent-child-published14-b9797941-full-1021045238-21969`
- Child interpreter: `/home/user/work/venv-agent-child-published14-b9797941/bin/python`
  (Python 3.13.16; installed marker `b97979411`)
- Runtime checkout: `/home/user/work/runtime`, Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d`
  (tree `6abc2f117391de8e7e35c0283f575a002199894d`)
- Published014 producer source: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`.
  The run's C13 Remotion input was
  `/home/user/work/runtimes/agent-remotion-published14-091aa23e`, with Node
  `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node` and node modules
  `/home/user/work/runtimes/agent-remotion-published14-091aa23e/node_modules`.
- Schema path supplied to the child:
  `/home/user/work/venv-agent-child-published14-b9797941/lib/python3.13/site-packages`.

The child profile is not a coherent Agent+Runtime install: the installed
Agent/client are present, but `runtime_protocol` and `astrid_runtime` are not.
The central command had parent `PYTHONPATH` including `/home/user/work/runtime`,
but the child launch sanitizes that path. Therefore this note does not call
all 138 failures environmental or product failures; it only records the
rendering subset and its exact observed boundaries.

## Four Scenehost/RLE error nodes

### Executed Scenehost setup nodes: one first cause

These three nodes entered `prepare_remotion_validation` and the worker
registry probe before failing:

- `tests/integrations/test_d09_managed_scene_only.py::test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[saved]`
- `tests/integrations/test_d09_managed_scene_only.py::test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[candidate]`
- `tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result`

The first rendering traceback is the probe import at:

```text
/home/user/work/wt/.test-agent-venv-agent-child-published14-b9797941-full-1021045238-21969/astrid/core/rendering/remotion_runtime.py:26
from runtime_protocol import platform
ModuleNotFoundError: No module named 'runtime_protocol'
```

The host-side surfaces are `remotion_runtime.py:687` (`_registry_probe`),
`remotion_runtime.py:632` (`_require_completed_probe`), and
`remotion_runtime.py:974` (`prepare_remotion_validation`). The exact retained
probe files were `/tmp/astrid-probe-logs/registry_discovery-44oj9mu6.stderr.log`,
`registry_discovery-_evjpe8b.stderr.log`, and
`registry_discovery-ep7krkfo.stderr.log`; each contains the same import
traceback. The surfaced error reports `phase=registry_discovery`,
`original_wait_exit_code=1`, `census_complete=true`, and `custody_admitted=true`.

This is an executed child-profile failure, not evidence that Scene evaluation
or the saved/candidate source itself is wrong.

### RLE node: fixture-before-yield

`tests/sdk/test_scene_real_public_summary_rle.py::test_real_public_scene_answers_reach_rle_summary`
never entered the test body. Collection/setup stopped at

```text
/home/user/work/wt/.test-agent-venv-agent-child-published14-b9797941-full-1021045238-21969/tests/sdk/test_scene_real_public_summary_rle.py:51
fixture 'native_host' not found
```

The available fixture list contains no `native_host`. This is a separate
fixture/plugin boundary and is not explained by the `runtime_protocol` child
traceback. No Scene/RLE repair attribution is justified from this node.

## Other rendering-owned failures in the same run

### Rendering pack nodes (10)

All ten terminal `tests/packs/rendering` nodes carry a
`RendererInternalError`/executor failure whose retained error text ends with
`ModuleNotFoundError: No module named 'runtime_protocol'`:

- `tests/packs/rendering/test_remotion_backend.py:684` —
  `test_manifest_command_runs_from_owning_pack_root`; host surface
  `astrid/core/rendering/errors.py:110`, backend `rendering.remotion`.
- `tests/packs/rendering/test_render_export_task_adapter.py:123` —
  `test_render_export_adapter_writes_real_mp4_and_is_callable`; host surface
  `astrid/packs/rendering/actions/render/task_adapter.py:466`.
  This block retains the child chain `astrid/packs/rendering/actions/render/run.py:9`
  -> `astrid/core/execution/persistent_supervisor.py:17` -> missing
  `runtime_protocol`.
- `tests/packs/rendering/test_threejs_backend.py`:
  `test_threejs_support_accepts_empty_and_exact_text_fields` (line 212),
  `test_threejs_support_rejects_unsupported_timelines_with_clip_reasons` (line 227),
  `test_threejs_support_rejects_non_rendered_audio_ownership` (line 375),
  `test_threejs_support_accepts_window_and_rejects_fps_mismatch` (line 388),
  `test_threejs_identity_invariants_never_claim_remotion` (line 408), and
  `test_threejs_own_namespace_config_is_strict` (line 422). Each surfaces at
  `astrid/core/rendering/errors.py:110`, backend `rendering.threejs`; the
  captured error text has the same missing-module cause, but these blocks do
  not retain the child file/line beyond that text.
- `tests/packs/rendering/test_builtin_registration.py:254` —
  `test_real_ffmpeg_render_through_registered_backend`; surface
  `astrid/core/rendering/errors.py:110`, backend `rendering.ffmpeg`, same
  retained missing-module text.
- `tests/packs/rendering/test_ffmpeg_backend.py:271` —
  `test_manifest_command_dispatches_from_pack_root`; surface
  `astrid/core/rendering/errors.py:110`, backend `rendering.ffmpeg`, same
  retained missing-module text.

These are actual render/pack command attempts under the captured source and
C13 Remotion paths, but the child cannot import the Runtime package. Viewing
should make its normal source/repair decision only after a coherent installed
Agent + Runtime profile exists; this handoff does not request a product fix.

### Core rendering nodes (10)

The same run also failed these rendering-core nodes:

- Conformance: `tests/core/rendering/test_conformance.py` lines 203, 234,
  282, 300, 318, and 357 (`test_minimal_render_wire_parity`,
  `test_request_sensitive_support_wire_parity`, `test_passthrough_audio_wire_parity`,
  `test_no_audio_wire_parity`, `test_attachment_wire_parity`, and
  `test_intentional_failure_wire_parity`). The first visible traceback is the
  harness sink at `test_conformance.py:108`, reading a missing SDK
  `result.json`; the retained block does not include the child stderr, so this
  report does not over-claim a deeper cause for these six nodes.
- `tests/core/rendering/test_freeze.py:174` —
  `test_freeze_real_ffmpeg_transport_one_video_one_committed_sidecar`;
  `astrid/core/rendering/errors.py:110`, backend `rendering.ffmpeg`, retained
  error text ends in the missing `runtime_protocol` import.
- `tests/core/rendering/test_service.py:1106` —
  `test_real_ffmpeg_renders_through_generic_service[nominal]` and
  `[with-audio]`; `astrid/core/rendering/errors.py:110`, backend
  `rendering.ffmpeg`, retained missing-module text.
- `tests/core/rendering/test_service.py:1219` —
  `test_real_ffmpeg_audio_reactive_through_generic_service`;
  `astrid/core/rendering/errors.py:110`, backend `rendering.ffmpeg`, retained
  missing-module text.

The non-rendering `stage1`/generic-host failures are intentionally not part of
this peer handoff.

## Evidence boundary and request

Executed scope: the three D09 nodes reached the managed registry probe; the
ten rendering-pack nodes and the core freeze/service nodes launched renderer
or executor paths and retained the child import failure. Fixture-before-yield
scope: the RLE node stopped at missing `native_host`. The six conformance
nodes only prove their missing-result sink from the retained log; their child
stderr was not preserved.

Please inspect the exact paths above and make the Viewing team's normal
repair/source decision only if a coherent profile later demonstrates a
rendering-owned issue. Do not treat this terminal run as current product or
Scene/RLE qualification, and do not replay it from the stale child profile.

Tests: none run by this worker, per task scope.
