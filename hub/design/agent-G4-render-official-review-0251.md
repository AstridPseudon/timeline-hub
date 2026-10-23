# G4 official render join review — FAIL

Reviewed candidate `c0976b2389afde9f339def9e5ea7f5ffa2de2bf5` (HEAD), with true requester parent `6ae94db34bfcf26ef19250051d4ba1a2c50ce66b` and official parent `2410c3bbbb14f4ca2b177dc894f5eea0246826ee`. The worktree remained clean; no tracked edits were made.

## Verdict

**FAIL — explicit V4 source-preservation requirement is violated.**

The six retired live-scenes paths are present in the candidate but absent from official parent `2410c3bbb`:

- `astrid/packs/rendering/editor/live-scenes/diagnostics.ts`
- `astrid/packs/rendering/editor/live-scenes/runtime.ts`
- `astrid/packs/rendering/ui/live-scenes/SceneSurface.tsx`
- `astrid/packs/rendering/ui/live-scenes/authoring.ts`
- `astrid/packs/rendering/ui/live-scenes/extension.tsx`
- `astrid/packs/rendering/ui/live-scenes/identity.ts`

Evidence:

- `git ls-tree -r --name-only 2410c3bbb -- astrid/packs/rendering/editor/live-scenes astrid/packs/rendering/ui/live-scenes` returned no paths.
- The same query for HEAD returned all six paths.
- `git show --name-status ef6455ebd` records all six as V4 deletions.
- `git diff --name-status 2410c3bbb HEAD` records all six as added.
- The true requester parent `6ae94db34` contains all six, so the join retained requester-side stale source instead of the official/V4 deletion.

This is the settled decision in the review brief; no reviewer deletion was performed.

## Source-preservation checks

PASS for requester-owned G4 render publication/source behavior: these files are byte-identical to true parent `6ae94db34`:

- `astrid/sdk/timeline/assembly.py`
- `astrid/sdk/timeline/commit_session.py`
- `astrid/sdk/timeline/sync.py`
- `astrid/packs/rendering/actions/assemble_timeline/run.py`
- `astrid/packs/rendering/shared/runtime_stitch.py`
- `astrid/packs/video_editing/shared/runtime_orchestration.py`
- `tests/sdk/test_timeline_render_publication.py`
- `tests/sdk/test_timeline_assembly.py`
- `tests/sdk/test_timeline_producer_guard.py`

The bounded tests cover requester-owned commit assembly, task/attempt/fence/target guards, startup/retry/lost-ack/receipt/outbox behavior, pinned render admission, normal caller client, and the R1/V1/V3/P1-related source neighbors. No old publisher or worker-write authority was credited.

## Generated/client/lock verification

PASS: generated client and lock material are exact official-parent copies:

- `git diff --quiet 2410c3bbb HEAD` passed for `astrid_runtime_client/generated.py`, `contract_metadata.py`, `timeline_commit_types.py`, `runtime.lock.json`, `remotion/package.json`, and `remotion/package-lock.json`.
- `runtime.lock.json` source pin is `21482a416d1f0f976ec563b9e1bf96a765f80e56`.
- Generated and contract metadata schema digest is `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.
- Composition archive and checksum compare byte-for-byte with official parent.
- `scripts/vendor_lock.py check runtime.lock.json` → `ok runtime.lock.json`.

The known official 21482 merged-response decoder defect is unchanged and independently reproduced: `astrid_runtime_client/generated.py:948` accepts only `accepted`/`rebased`, so a valid `status: "merged"` response raises `invalid_response: acceptance requires accepted status and committed receipt`. This is a Runtime-owned blocker, reported separately; no fake transport acceptance, shim, metadata drop, or alternate executor was used.

## Test and quality evidence

All requested bounded lanes passed:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_render_publication.py` → **13 passed**.
- Requester/assembler/render helper lane:
  `... pytest -q -p no:cacheprovider tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_producer_guard.py tests/sdk/test_timeline_sync.py tests/packs/rendering/test_assemble_timeline.py tests/packs/rendering/test_runtime_stitch.py tests/packs/video_editing/test_runtime_orchestration.py tests/stage1/test_final_render_authority_luna.py tests/editing_conformance/test_producer_insertion.py tests/editing_conformance/test_producer_guard.py` → **221 passed**.
- `... pytest -q -p no:cacheprovider tests/sdk/test_timeline_open_commit.py tests/sdk/test_workspace_client_timeline_commit.py` → **25 passed**.
- `... pytest -q -p no:cacheprovider tests/sdk/test_timeline_open_commit_v2.py tests/sdk/test_timeline_commit_v2_errors.py tests/sdk/test_p1_doc_patch_requests.py tests/timeline/test_meta_validator.py` → **48 passed**.
- `... pytest -q -p no:cacheprovider tests/packs/rendering/test_composition_package.py` → **6 passed, 1 deselected**.
- `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ... pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes` → **1 passed**.
- Scoped Ruff → **passed**.
- Private scoped mypy → **passed**.
- Normal Ruff ratchet → **current 2149, baseline 2149**.
- Normal mypy ratchet → **current 1915, baseline 1915**.
- `git diff --check` → **passed**.

No full suite, browser, farm, native-14 duplicate, or broad replay was run.

## Recommended next step

Have the merge owner resolve only the six stale live-scenes additions back to the official/V4-deleted state, retaining the requester-owned G4 source and exact official 21482 generated/lock material. Then rerun the bounded review lanes. The merged-response decoder must be repaired and regenerated by Runtime before any actual-wire acceptance claim; this review does not treat the mocked green lanes as Runtime acceptance.

