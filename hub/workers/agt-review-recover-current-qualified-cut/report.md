## Review: HOLD / REJECT

Reviewed `7d9860fc` against merge base `f82da322`.

Blocking defect: `TimelineSession.flush` converts restore transport errors from `WorkspaceClientError` to `ConnectionError`, breaking the existing contract and causing:

`test_restore_lost_ack_retries_exact_request_after_reload` — failed.

Tests: `189 passed, 1 skipped, 1 failed`. `git diff --check` passed.

Also noted:

- Catalog forwarding and native restore routing are otherwise correct.
- Integration overlap is only `astrid/sdk/timeline/sync.py`; preserve WC7’s `_flush`/`explicit_outbox` changes during merge-forward.
- Final restore coverage checks only the parent row, not the full closure.

Report: [agent-recover-qualified-cut-review.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-recover-qualified-cut-review.md)

`commit-msg`, `commit-msg.txt`, and `DONE` were written.