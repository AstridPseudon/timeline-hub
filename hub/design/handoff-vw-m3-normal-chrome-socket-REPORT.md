# vw-m3-normal-chrome-socket-boundary

## Finding

The normal public13 MP4 path does not use `HostRemotionSession`.  The path is:

`GenericPackHost` (`generic_host.py:7891` command dispatch) -> `RenderService` (`service.py:408-413`, workspace beside `attempt/outputs`) -> `remotion/run.py:1651-1663` (`staging_parent=workspace`) -> `root_preparation.py:111-119` (`.remotion-runtime-*`) -> `run.py:1111-1116` (child `TMPDIR/TMP/TEMP`) -> Chrome.

The central failure log is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-normal-mp4-short-owned-temp-integration-viewing-native-retained-fixture-1020184119-11075/log.txt`

Chrome received this 228-byte socket path:

`/tmp/vw-m3-normal-TGpDXE/tmp/astrid-attempt-e8da1f00235b43cabcbc5a4b3d05c129-tk0y3w29/.timeline-5d66df56-f091-48af-a1c9-1c6fa2007c00.mp4.render-service-yrr6h1rb/.remotion-runtime-9x9u2k0m/com.google.Chrome.F0OceF/SingletonSocket`

The same Remotion/Chrome suffix under the short private parent is 96 bytes.  The attempt root remains the owner of output, authority, and cleanup; only the invocation-scoped browser scratch parent changes.

`HostRemotionSession` is still relevant to the requested lifetime trace: its host-only path allocates `astrid-remotion-host-*` under `attempt_base` at `remotion_host_session.py:187-197`, with `attempt_base` supplied by `GenericPackHost._renderer_task_lease` at `generic_host.py:5501-5517`.  That lease is for `rendering.timeline_visualize`, not normal MP4.

## Proposed owner patch (unapplied)

`owner-fix.patch` is one Agent-owner patch plus two pure tests.  It uses the already-admitted `TMPDIR` seam (`remotion_runtime.py:205`, `_NODE_ENV_KEYS`) and adds no DTO, store field, public option, browser flag, profile, symlink, or global-temp fallback.

The helper accepts `TMPDIR` only when it is absolute, canonical, existing, owned by the current uid, and has no group/other permission bits.  Otherwise it retains the existing attempt-local parent.  The existing `TemporaryDirectory` and `ExitStack` cleanup remain unchanged.  Runtime/Agent owner review is required before applying it, especially for evidence-budget accounting of scratch moved outside the attempt tree.

## Evidence

- `/home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_remotion_root_preparation.py` — **2 passed**.
- `/home/user/work/venv-agent/bin/python -m pytest -q tests/core/execution/test_remotion_host_session.py tests/packs/rendering/test_remotion_root_preparation.py` — **26 passed, 2 failed**.  Both failures were existing socket-channel tests blocked by sandbox `PermissionError: [Errno 1] Operation not permitted`; no browser or renderer was run.
- `/usr/bin/python3 -m pytest -q ...` — could not start because system Python has no `pytest` module.
- The direct normal-audio selection command (`tests/packs/rendering/test_normal_audio_run.py`, `-k 'private_tmpdir or shared_tmpdir or read_only_root_context_holds_normal_pcm_until_query_exits or normal_native_decode_error_releases_attempt_before_consumer'`) produced **1 passed, 1 failed, 26 deselected, 9 errors** because the existing fixture requires unset `ASTRID_REMOTION_PROJECT_DIR`; it is not evidence against this patch.
- No full suite, browser, renderer, or capture run was submitted by this worker.
- `git apply --check owner-fix.patch` — clean; the owner patch is ready for review but remains unapplied.

The repository worktree is clean; the patch is intentionally not applied.
