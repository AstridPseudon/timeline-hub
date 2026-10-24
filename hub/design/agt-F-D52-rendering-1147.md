## D52/G4 report

Read-only assessment complete. Exact membership verified: 23 nodes across the requested 11 files. No code, tests, manifests, registries, contract docs, or caches were changed.

### Findings

| Nodes | Source caller / exact input | Cause classification |
|---|---|---|
| `test_conformance.py` ×6 | `_run_both` → `CommandTransport.run` (`test_conformance.py:193–349`); fixtures: `minimal-render.json`, `support-supported.json`, `support-window.json`, `passthrough-render.json`, `no-audio-render.json`, `attachment-render.json`, `failure-render.json`; SDK path delegates to `astrid.sdk.rendering.renderer_main` (`sdk_render.py:44–48`). | UNKNOWN. Retained traceback ends at missing `sdk/result.json` (full9758 log `8155–8408`); child stderr/return code was not retained. Not enough evidence to assign a shared startup cause. |
| `test_service.py` ×3 | `RenderService.render_request` → `_run_command` → `CommandTransport` (`test_service.py:949–1025, 1080–1108, 1119–1221`; production transport `service.py:1905–1946`). Inputs: generated 160×90 blue MP4, plain/AAC variants, and 640×360 audio-reactive timeline with WAV tone/events. | Genuine setup/source-environment failure: retained child traceback is `ModuleNotFoundError: runtime_protocol` (full9758 log `14138–14620`). Not an FFmpeg rendering regression. |
| `test_freeze.py` ×1 | Reuses `_real_media_inputs` and calls `service.render_request` with `rendering.ffmpeg` (`test_freeze.py:163–190`). | Same retained child `runtime_protocol` import failure (full9758 log `8408–8555`). |
| `test_remotion_host_session.py` ×1 | `GenericPackHost._run_command_definition` with two leases, fake frame worker, 320×180/18-frame request (`test_remotion_host_session.py:18–37, 241–315`). | Genuine setup/source-environment failure: child `generic_host_worker` imports `astrid.core.execution`, then fails on `runtime_protocol` (full9758 log `7826–8154`). |
| `test_threejs_backend.py` ×6 | Public `support()` calls over empty/text timelines, unsupported clip variants, passthrough/none audio, 24/30-fps windows, identity, and namespace config (`test_threejs_backend.py:67–119, 176–428`). | Genuine setup/source-environment failure: all retained failures stop in child transport with `ModuleNotFoundError: runtime_protocol` (full9758 log `18070–18320`). No D46 remote-provider scope involved. |
| `test_builtin_registration.py` ×1 | Registry candidate → `CommandTransport.run("render")`, generated 160×90 blue MP4 (`test_builtin_registration.py:188–255`). | Same retained `runtime_protocol` child import failure (full9758 log `17664–17743`). |
| `test_ffmpeg_backend.py` ×1 | Direct `CommandTransport.run("support", ("python3", "run.py"))` from rendering pack root (`test_ffmpeg_backend.py:260–282`). | Same retained `runtime_protocol` child import failure (full9758 log `17744–17786`). |
| `test_remotion_render_contract.py` ×1 | Selected Remotion runtime plus Node SSR script rendering public `text-card` markup (`test_remotion_render_contract.py:49–215`). | Stale/mismatched selected runtime fixture: assertion shows selected `agent-remotion-composition14-255b6856/package.json` differs from tracked snapshot package data (full9758 log `17787–17826`). |
| `test_render_export_task_adapter.py` ×1 | `execute_render_export_task` → `RenderExportTaskAdapter.execute` → `run_executor("rendering.render")` (`test_render_export_task_adapter.py:81–142`; adapter `task_adapter.py:291–300, 447–466, 533–549`). Input is the `broll.mp4` managed-object handoff and 2-second 1920×1080 timeline. | UNKNOWN. Retained evidence is only `RenderExportRefused: executor exited with returncode 1` and generic stderr; child traceback/result cause is missing. |
| `test_remotion_backend.py` ×1 | Manifest command through `CommandTransport` from owning pack root, empty timeline/fake project (`test_remotion_backend.py:113–158, 672–700`). | Same retained `runtime_protocol` child import failure; expected fail-closed launch-validation result was not reached. |
| `test_media_handoff_render_boundary.py` ×1 | `GenericPackHost` materialization → `run_executor("rendering.render")`, locally generated 1280×720 black MP4 and object-ID registry (`test_media_handoff_render_boundary.py:172–236`). | UNKNOWN. Retained evidence is only external executor returncode 1 and `renderer command exited with status 1`; child traceback was not retained. |

### Boundaries and follow-ups

- The D52 package remains authoritative: 276 total nodes, 157 summary-only; no D32 baseline credit, no dead-code retirement proof, and no deletion assignment.
- Existing corrected installed-profile facts for Node 20 / Remotion archive `819acf` were reused; no new environment or rendering probe was run.
- No row supports “code retired with no caller and exclusive tests.” Production transport/adapter callers remain present in source.
- D46 owner-deferred remote providers do not apply to these 23 local rendering/transport rows.

Recommended next steps:

1. Requalify the 14 `runtime_protocol` rows on the already-corrected installed profile, preserving import provenance.
2. Capture child stderr, return code, argv/cwd, and result-file state at the transport boundary for the six conformance rows, adapter row, and stage1 row.
3. Only if failures persist after source qualification, assign owner-specific product fixes; do not weaken or remove tests.

Tests were intentionally not run per task scope. Read-only source/log inspection completed; worktree remains clean.