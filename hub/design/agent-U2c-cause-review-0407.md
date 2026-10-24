## U2c cause review — FAIL

Base reviewed: `699236a28581017c4d928137331e4893a1534bea`

No Agent source/tests changed. Evidence is in [evidence/U2c-cause-review-0407.txt](/home/user/work/wt/agt-U2c-cause-review-0407/evidence/U2c-cause-review-0407.txt).

| Verdict | Nodes | Cause |
|---|---|---|
| PASS | `test_real_parked_process_inspection_preserves_identity_guards`; `test_bootstrap_register_observe_commit_and_same_incarnation_recovery[False]`; `[True]`; `test_precommit_failure_revokes_before_stopping_exact_host[ack]`; `[cleanup]`; `test_independent_readiness_rejects_changed_evidence[ready_marker]`; `[registration]`; `[provider]`; `test_uncertain_commit_preserves_exact_host_and_credential` | Stale Agent fixture passes removed `production_worker_credentials=True`; Runtime raises `TypeError` at `tests/helpers/runtime.py:124`. |
| FAIL | Four `test_abort_preserves_primary_failure_without_signaling_after_failed_identity[...]` nodes | Current `astrid/sdk/host_bootstrap.py:1084` aborts before calling `_parked_host_identity_matches`. This is a real promised-safety gap, though pre-existing relative to U2c; it is not a passing census result. |
| PASS | `test_real_disabled_bearer_fails_handshake_and_enabled_bearer_becomes_ready` | Same removed Runtime keyword, raised in the test body. |
| PASS | `test_local_host_control_is_separate_and_survives_multiple_bounded_requests` | Sandbox rejects `socket.socket(fileno=descriptor)` with `PermissionError`; not classifier refusal. Validate through central test service/outside-sandbox or a `--net` worker. |

Runtime history confirmed:

- `d181fbc3` introduced the producer flag.
- `1ac2a367` hardened it.
- `8c9b77d` removed it; current Runtime always provisions the scoped worker actor.
- R4 candidate Runtime `31c7ac3a` predates removal; U1c/current Runtime does not support the flag.

The smallest faithful fixture adaptation is removing the two keyword uses in `tests/integrations/test_generic_host_activation_acceptance.py`. Existing `worker_credential_path` and Runtime readiness authority remain valid; no shim or API revival is needed.

The smallest safety fix is one Agent source change in `astrid/sdk/host_bootstrap.py`: observe parked identity before cleanup/signaling, refuse live unverifiable hosts, preserve the primary exception, and allow only the child-exit race with positive wait proof. Tests must remain unchanged.

Test evidence: prior exact integration command produced `6 failed, 1 warning, 9 errors` in 22.81s. I did not rerun failing bodies. `git diff --check` passed; worktree has only the evidence file.