# D52/G4 rendering source/evidence return

Verdict: source attribution PASS; action gating corrected. No behavior PASS claimed.

Exact membership remains 23 nodes across 11 files:

- `test_conformance.py`: 6 unknowns.
- `test_service.py`: 3 `runtime_protocol` import failures.
- `test_freeze.py`: 1 same import failure.
- `test_remotion_host_session.py`: 1 same import failure.
- `test_threejs_backend.py`: 6 same import failures.
- `test_builtin_registration.py`: 1 same import failure.
- `test_ffmpeg_backend.py`: 1 same import failure.
- `test_remotion_render_contract.py`: 1 stale selected-runtime/profile mismatch.
- `test_render_export_task_adapter.py`: 1 unknown.
- `test_remotion_backend.py`: 1 same import failure.
- `test_media_handoff_render_boundary.py`: 1 unknown.

This preserves 14 child `runtime_protocol` attributions, 8 unknowns, and 1 profile mismatch. The 14 retained failures are child startup/import evidence, not rendering regressions. The eight unknowns retain only missing result files or generic executor return-code/stderr evidence; no cause was invented. The mismatch remains the stale `255b` selected runtime, distinct from corrected existing profile `819acf`.

Current caller/source spans remain:

- Conformance transport and SDK delegation: `test_conformance.py:74–101,132–139,193–349`; `sdk_render.py:44–48`.
- Service and production transport: `test_service.py:949–1228`; `service.py:1905–1946`.
- Freeze: `test_freeze.py:163–190`.
- Remotion host: `test_remotion_host_session.py:18–38,241–315`.
- Three.js: `test_threejs_backend.py:67–119,176–428`.
- Builtin/FFmpeg: `test_builtin_registration.py:188–255`; `test_ffmpeg_backend.py:260–282`.
- Remotion contract: `test_remotion_render_contract.py:49–215`.
- Adapter and production callers: `test_render_export_task_adapter.py:81–142`; `task_adapter.py:291–300,453–466,533–549`.
- Remotion backend: `test_remotion_backend.py:113–158,672–700`.
- Stage1: `test_media_handoff_render_boundary.py:172–236`.

Production callers remain live: service/SDK use `CommandTransport`; adapter/stage1 use `run_executor`. No dead-code or retirement credit is justified.

Corrected next actions:

- The existing 10:16 schema/authorization/child-admission hold remains active for genuine installed-child/source qualification. No overlay, acquisition, new child, source substitution, or blind unchanged rerun.
- Ordinary local source tests that create/adopt no child and acquire no source do not require a new owner-approval gate. They may use the existing qualified venv/profile only when exact route eligibility is proven.
- A local profile-only package mismatch may be assessed against authentic existing `819acf` input, but this does not establish that the 14 `runtime_protocol` imports are fixed.
- After the hold is cleared, any meaningful requalification must retain child stderr, return code, argv, cwd, and result-file state.

The v2 contract requirements remain preserved: complete request fields and `Idempotency-Key`; accepted/merged canonical closure, IDs, digests, commands, `id_map`, records, steps/dependencies/effects/bindings; undo/history/publisher and durable receipt; dry-run `would_status` with null receipt; conflict reason/head; invalid code/path/hint/suggested command.

Checks:

- `git status --short --branch`: clean.
- `git diff --check`: passed.
- No tests, source execution, environment/render/process execution, full suite, gate run, installs, acquisition, or credentials used.
- Official 276-count was not rewritten.
- Required `DONE` marker and task-named commit message were recorded.