## U2c cause report

No Agent source or test changes were made; worktree is clean.

| Outcome | Node IDs | Cause |
|---|---|---|
| 9 errors | `test_real_parked_process_inspection_preserves_identity_guards`; both `test_bootstrap_register_observe_commit_and_same_incarnation_recovery`; both `test_precommit_failure_revokes_before_stopping_exact_host`; all three `test_independent_readiness_rejects_changed_evidence`; `test_uncertain_commit_preserves_exact_host_and_credential` | Runtime fixture mismatch: frozen U1c Runtime `40427e8b`/`8ea0766f` lacks `RuntimeDaemon(..., production_worker_credentials=...)`. |
| 1 failure | `test_real_disabled_bearer_fails_handshake_and_enabled_bearer_becomes_ready` | Same Runtime API mismatch, raised in the test body. |
| 4 failures | All four `test_abort_preserves_primary_failure_without_signaling_after_failed_identity[...]` nodes | Pre-existing Agent source/test mismatch: `abort()` does not invoke `_parked_host_identity_matches`, although these tests expect that observation. Not caused by U2c’s changed files. |
| 1 failure | `test_local_host_control_is_separate_and_survives_multiple_bounded_requests` | Harness refusal: sandbox raised `PermissionError` when the control thread wrapped the detached socket descriptor. |

The U1c frozen branch does not provide the required API. The producer was introduced in Runtime `d181fbc3`, hardened in `1ac2a367`, and removed by `8c9b77d`; a normal Runtime peer checkout with the compatible producer is required. No adapter or shim was added.

Tests:

- Activation command: **6 failed, 1 warning, 9 errors** in 22.81s.
- Neighbor run was interrupted at 65% after unrelated baseline failures; no result claimed.
- `git diff --check`: passed.
- No full/browser/original readiness journey or installation run.

No readiness green claim is made. Commit message and `DONE` marker were written.