## Result: PASS — bounded freeze handoff

The U1c draft remains qualified. This is not an integration, gate, full-suite, or pin-adoption PASS.

Facts verified:

- Candidate `40427e8b…`, tree `34ca7af1…`, has exactly two parents:
  - reviewed `0138e3af…`
  - upstream `795379a6…`
- `795379a6…` and `0138e3af…` are ancestors of the candidate.
- Candidate/current integration merge-base is `abd47e68…`; current integration `1d9ddba5…` has not adopted U1c. This intentional hold is not a product regression or revert.
- Candidate delta is exactly:
  - `runtime_protocol/service.py`
  - `tests/test_managed_output_export.py`
- All 69 protected contract/package/generator/schema blobs are byte-identical to both `0138e3…` and `abd47e…`.
- Candidate schema digest remains `sha256:35c2d9c5…`; candidate producer digest remains `sha256:d5f98db3…`.
- Current integration preserves the schema digest and has five protected changes that must survive:
  - D39: `contract/artifacts.json`, `contract/openapi/workspace-v1.yaml`, `contract/schemas/common.json`
  - R0: `generators/python_client_init_template.py`, `packages/python/astrid_runtime_client/__init__.py`
  - Current producer digest: `sha256:6eb9b835…`

Remaining freeze seams:

- Reapply U1c’s `_ensure_export_root` default and its managed-output test. Current integration correctly still has the old configured-root refusal because U1c is held.
- Preserve the separate readiness `_read_history` change in `runtime_protocol/service.py`.
- Preserve D39/R0 protected changes; do not restore the draft’s 69 protected blobs wholesale.
- D40 paths are disjoint: `external_pack_sources.py`, `local_worker_composition.py`, `verified_host_launch.py`, and its test.
- Headless and occupancy changes are disjoint: `tests/test_timeline_headless_overwrite_refused.py` and `tests/test_timeline_legacy_occupancy.py`; qualify them after reapplication.

The mounted production caller is `runtime_protocol/server.py:990-992`, which authenticates `POST /v1/managed-outputs/{association_id}/export` and calls `RuntimeService.export_managed_output`.

C0 v2 request/reply fields, idempotency, attribution, refusal, retry, preview, conflict, invalid, history, and undo shapes remain present in the current contract/schema.

Evidence:

- Reused exact prior targeted command because touched-file bytes are identical:

  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_managed_output_export.py tests/test_visual_seam_admission.py tests/test_canonical_render_admission.py tests/test_skip_guard.py tests/test_skip_registry.py tests/test_skip_policy.py`

  Result: `224 passed`.

- Prior Ruff comparison: 78 baseline diagnostics, 0 new.
- Prior Pyright comparison: 375 vs 375, 0 new.
- Recheck: in-memory compilation passed, `git diff --check` passed, no conflict markers, clean worktree.
- No full, browser, integration, gate, generator, or live-upstream freshness checks were run.

No product files were modified. Recommended next step: have the freeze author apply the two U1c paths onto current integration while preserving the listed history and D39/R0 changes, then run current-integration targeted qualification.