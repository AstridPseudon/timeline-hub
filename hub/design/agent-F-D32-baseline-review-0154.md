## D32 baseline review: FAIL

Corrected decision: **0 PASS, 25 OURS**. Exact test-file identity and matching upstream signatures are insufficient because relevant product call paths changed or the failure remains environment/setup-shaped.

Per-entry decisions:

1. `test_remotion_host_session::test_two_public_command_workers...` — **OURS**; `generic_host.py` changed.
2. `test_worker_startup_identity::test_sanitized_child_import...` — **OURS**; isolated child path changed.
3. `test_conformance::test_attachment_wire_parity` — **OURS**; missing-result producer is unproven.
4. `test_conformance::test_intentional_failure_wire_parity` — **OURS**; same.
5. `test_conformance::test_no_audio_wire_parity` — **OURS**; same.
6. `test_conformance::test_passthrough_audio_wire_parity` — **OURS**; same.
7. `test_conformance::test_request_sensitive_support_wire_parity` — **OURS**; same.
8. `test_freeze_real_ffmpeg_transport...` — **OURS**; renderer path changed.
9. `test_real_ffmpeg_audio_reactive...` — **OURS**; renderer path changed.
10. `test_real_ffmpeg_renders... [nominal]` — **OURS**; renderer path changed.
11. `test_real_ffmpeg_renders... [with-audio]` — **OURS**; renderer path changed.
12. `test_real_ffmpeg_render_through_registered_backend` — **OURS**; renderer path changed.
13–17. Five Three.js backend nodes — **OURS**; renderer/service path changed.
18. `test_threejs_support_rejects_unsupported_timelines...` — **OURS**; active cause remains unproven.
19–22. Four VibeComfy bridge nodes — **OURS**; execution/gateway paths changed; runtime import failure is environmental.
23–24. Two doctor smoke nodes — **OURS**; fail at isolated `python -I` import before exercising doctor behavior.
25. `test_bootstrap_environment_is_accepted_by_the_remotion_probe_context` — **OURS**; prior evidence explicitly says no shared cause is proven, and `remotion_runtime.py` changed.

Evidence:

- Comparison artifact: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D32-baseline-0148/evidence/d32-baseline-comparison.json`
- Exact upstream: `90d469808d61e469fbefbb4d00b81cbd307d904e`
- Current parent: `c36ca8c94b695b0e25b7d42c89f194661f187423`
- All 25 old/upstream signatures matched, all were call-phase.
- D14/D23/H9 remain visible with no credit.

Validation:

- Exact upstream targeted run recorded: **28 failed, 8 passed** across 36 nodes.
- `git diff --quiet` checks confirmed all 16 eligible test files are byte-identical.
- `git diff --check` passed.
- No tests were rerun in this review, per task prohibition.
- No product, test, dependency, or environment files changed.

Required `commit-msg` and `DONE` markers were created.