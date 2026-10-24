## U2 whole-path audit

No product or test files changed. Commit message and `DONE` marker were created.

### Findings

- D18 remains unbounded at `tests/core/execution/test_generic_host_child_bridge_d18.py:3639`: restore `future.result(timeout=5)`. Selector: `test_materialization_pending_writes_consume_capacity`.
- Activation refusal at `tests/integrations/test_generic_host_activation_acceptance.py:251-268` is unreachable. Runtime commits in `remote_worker_activation.py:352-374`, enables the credential at `388-400`, then reaches readiness at `401-404`. The production caller remains `witness.launcher.activate(...)` at test line 287.
- The same activation test patches `_parked_host_identity_matches` at line 417, but production `abort()` calls retained `terminate_group()` directly at `astrid/sdk/host_bootstrap.py:1089-1111`. That patch cannot observe the abort path.
- The current ready-file cleanup assertion is vacuous: the fixture uses `not-ready.json` but never creates it.

### Smallest faithful seams

- Keep the real `launcher.activate()` path and machine-placement receipt flow.
- Add a same-realm, separately registered/enabled worker collaborator before activation. Invoke the real `RuntimeProtocolClient.claim_next()` before acceptance is recorded; assert `waiting_reason == "remote_activation_missing"`, no `attempt_id`, and task status remains `queued`. Do not mutate activation state or add a guard waiver.
- Move refusal assertions out of `ready()`, where activation is already committed.
- Test abort through the imported retained authority `host_bootstrap.terminate_group`: use a deterministic refusal collaborator for the live/unverifiable case, preserving `cleanup_error`, primary exception cause, `aborted == False`, and no `killpg`/numeric signal. Use the real retained cleanup path for the child-exit case and assert a real matching ready marker is removed.
- Existing comparators: `tests/test_generic_host.py:999-1012`, `1038-1072`; `tests/integrations/test_generic_host_activation_acceptance.py:451-498`; `tests/sdk/test_host_bootstrap_source_identity.py:654-736`.

### Verification

Read-only source audit only; no subprocess, process probe, network, test body, new realm, full suite, or browser/gate run. `git diff --check 1f15f27482 HEAD` passed; worktree is clean. Prior reports’ targeted/static results remain historical and were not re-run.