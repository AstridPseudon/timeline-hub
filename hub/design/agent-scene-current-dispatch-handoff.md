# Current Scene dispatch handoff

Status: complete bounded port on the current Agent integration base.

## Source

- Repository: Agent (`sdk`), worktree `/home/user/work/wt/agt-m3-scene-dispatch-current-resume`.
- Base `HEAD`: `53af5383802e995f78b3693a22d54b3e86062eff`.
- Central final targeted source-tree fingerprint: `f0683cf88347c2c03a5649a0da55482344aea84d`.
- Donor WIP: `c54949389e819e01479e911b04f116dad791aafd/tl/agt-m3-scene-managed-query-only`.

## Port

The current tree now has the bounded Scene-only path: existing private `_invoke_internal_result`, private scene-only/preflight/media-authority context, `include_media=False`, actual capture identity binding, and `entrypoints.scene`. The executor emits the managed `timeline_filmstrip` bundle with nested `manifest.json` and `scene-answers.json`, using the existing source and prepared host-frame helpers. Catalog pagination uses the registered `rendering.timeline_visualize` fixture. No new endpoint, provider, DTO, source factory, or caller authority was added; no obsolete `scene_answers` or `rendered_video` alias was used.

The tests cover caller preservation, private dispatch, saved and working-copy candidate paths, the real executor writer, page-two catalog discovery, and stale provenance refusal. The live proof helper uses the normal Runtime/pack-host launcher and always retires and waits for the host process group in `finally`.

## Evidence

Offline command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/sdk/test_scene_dispatch_contract.py tests/sdk/test_scene_caller_preservation.py tests/sdk/test_managed_render_invocation.py tests/sdk/test_timeline_visualize_public_surface.py tests/sdk/test_scene_save_core.py tests/packs/rendering/test_scene_only_executor.py tests/packs/rendering/test_timeline_filmstrip_execution.py tests/sdk/test_capture_source_runtime.py tests/sdk/test_timeline_filmstrip.py tests/sdk/test_timeline_filmstrip_invocation.py tests/sdk/test_timeline_checkout.py tests/sdk/test_invocation_observation.py
```

Result: `224 passed, 2 skipped, 44 deselected, 5 warnings in 54.82s`.

Focused Ruff command (`ruff check --no-cache --isolated --select F` over the changed files) reports four pre-existing unused imports in the existing PNG rendering import block; the new test has no remaining unused import.

Final real managed proof request:

```text
agt-m3-scene-dispatch-current-resume-targeted-1020213245-7374
```

Command:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m3-scene-dispatch-current-resume targeted --files "tests/integrations/test_d09_managed_scene_only.py tests/packs/rendering/real_pack_host.py") && echo "$R" && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: `1 passed in 278.65s`; central source-tree fingerprint above. It used the current public13-compatible Remotion profile, normal Runtime discovery and pack-host startup, and real managed saved and frozen-candidate queries. Both results had non-empty Scene answers, exact managed CAS ZIP contents, nested `entrypoints.scene`, provenance whose `video_digest` matched the actual capture identity, and the expected committed/candidate snapshot labels. A tampered provenance digest was refused as unavailable. Scene-only did not require an MP4 or frame prerequisite.

## Limits

- No full suite, browser suite, or live suite other than the explicitly requested central targeted proof was run.
- Public13’s text source evaluates to advisory `UNKNOWN` rather than `COVERED` because its bounds are undeclared; the proof treats that as usable and rejects only `UNAVAILABLE`.
- Ordinary activation remains held pending orchestrator judgment.
- Prior failed/cancelled diagnostic runs were not reused as positive evidence.
- The focused Ruff findings are pre-existing F401s at `filmstrip_execution.py:1238-1240`; they were not part of this bounded Scene delta.
- Runtime, App, Composition, and shared dependencies were not modified.
