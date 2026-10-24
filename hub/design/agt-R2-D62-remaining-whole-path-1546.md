# D62 report

- Read-only diagnosis completed; no product/test/schema changes.
- Agent `57779274a` emits the legitimate `timeline.restore` closure-root write at `commands.py:259–262`; inverse generation preserves/reverses it.
- Runtime `8b32cace` authentication `images()` excludes `timeline`. `_inverse_stage_boundaries()` sends that write through `_inverse_stage_state()`, which observes it as absent and raises:
  `inverse stage write differs from its sequential input`.
- `service.py:2504` only maps the rejection; it is not causal.

Conclusion: Runtime auth compatibility defect. Smallest fix belongs in `runtime_protocol/timeline_commit_auth.py`: add a dedicated authenticated `timeline` closure-scope branch for inverse-stage sequential-input validation, preserving exact before/after and existing guards. Do not weaken the check or alter Agent emission.

Evidence:

- Retained command: `59 passed, 1 failed` from `evidence/home.log`.
- Passing structural/retry and guard cases remain intact.
- Failing test: `test_restore_inverse_redo_and_exact_retry_survive_runtime_restart`.
- Agent source hashes and original test hashes match the retained evidence.
- No bodies were rerun.

Requested docs path was absent; read the available Timeline Hub mirror instead. Commit message and `DONE` marker were written.