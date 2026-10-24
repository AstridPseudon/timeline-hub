## Report

No product, test, fixture, guard, profile, pin, or generated-file changes. Worktree remains clean; commit message and `DONE` marker were written.

### Evidence

- Full run: `agent-full-post-g5-2225-1023222822-25691-17158`; all 21 nodes were exact `call`-phase failures.
- Compared rendering/source chains between `c36ca8c...` and `f88cc52...`; no relevant source/test diff.
- Read retained longreprs, runner log, replay bundles, and immutable 819acf archive. No tests or producers were invoked.

### Shared causal finding

The retained parent environment includes Runtime at:

`/home/user/work/wt/rt-pin-8ea0766f`

But `CommandTransport._build_environment()` applies `build_child_subprocess_env()`. Its allowlists omit `PYTHONPATH` and do not propagate `ASTRID_RUNTIME_CHECKOUT` as an import root. Rendering pack launchers add only the Agent checkout to `sys.path`.

Therefore child processes import `astrid`, then fail on:

`astrid/core/foundation/atomic_io.py:16` → `from runtime_protocol import platform`

This is an execution-environment/OPS issue, owned separately by `agt-F-env-cohort-2356`; no rendering backend source regression is evidenced.

### Exact node map

All nodes below failed in `call`.

- SDK conformance, six missing `sdk/result.json` files:

  `tests/core/rendering/test_conformance.py::test_minimal_render_wire_parity`  
  `tests/core/rendering/test_conformance.py::test_request_sensitive_support_wire_parity`  
  `tests/core/rendering/test_conformance.py::test_passthrough_audio_wire_parity`  
  `tests/core/rendering/test_conformance.py::test_no_audio_wire_parity`  
  `tests/core/rendering/test_conformance.py::test_attachment_wire_parity`  
  `tests/core/rendering/test_conformance.py::test_intentional_failure_wire_parity`

  Source chain: `sdk_render.py` → `renderer_main()` → `_support_report()`/`_backend_render()` → `atomic_io`. The outer harness observes absent result files. Child stderr/cwd/effective sanitized environment was not retained for these six, so the shared environment attribution is probable but marked `UNCONFIRMED` pending bounded capture.

- Direct FFmpeg/Three.js/Remotion failures, 14 nodes:

  `tests/core/rendering/test_freeze.py::test_freeze_real_ffmpeg_transport_one_video_one_committed_sidecar`  
  `tests/core/rendering/test_service.py::test_real_ffmpeg_renders_through_generic_service[nominal]`  
  `tests/core/rendering/test_service.py::test_real_ffmpeg_renders_through_generic_service[with-audio]`  
  `tests/core/rendering/test_service.py::test_real_ffmpeg_audio_reactive_through_generic_service`  
  `tests/packs/rendering/test_builtin_registration.py::test_real_ffmpeg_render_through_registered_backend`  
  `tests/packs/rendering/test_ffmpeg_backend.py::test_manifest_command_dispatches_from_pack_root`  
  `tests/packs/rendering/test_remotion_backend.py::test_manifest_command_runs_from_owning_pack_root`  
  `tests/packs/rendering/test_threejs_backend.py::test_threejs_support_accepts_empty_and_exact_text_fields`  
  `tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons`  
  `tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_non_rendered_audio_ownership`  
  `tests/packs/rendering/test_threejs_backend.py::test_threejs_support_accepts_window_and_rejects_fps_mismatch`  
  `tests/packs/rendering/test_threejs_backend.py::test_threejs_identity_invariants_never_claim_remotion`  
  `tests/packs/rendering/test_threejs_backend.py::test_threejs_own_namespace_config_is_strict`  
  `tests/stage1/test_media_handoff_render_boundary.py::test_host_derived_registry_executes_canonical_ffmpeg_executor`

  Retained stderr directly reports `ModuleNotFoundError: No module named 'runtime_protocol'`. The stage1 trace is `actions/render/run.py` → `astrid.core.execution` → `persistent_supervisor`.

- Render-export adapter, one node:

  `tests/packs/rendering/test_render_export_task_adapter.py::test_render_export_adapter_writes_real_mp4_and_is_callable`

  `run_executor()` returns `returncode: 1`; retained outcome lacks the child stderr/cwd. The source chain reaches the same canonical render executor, so this remains `UNCONFIRMED` pending bounded child-log capture.

Minimum authorized fix: qualify the existing managed child environment with the Runtime import root/package, preserving installed-profile and source-custody controls. No backend behavior or success/refusal predicates should change.