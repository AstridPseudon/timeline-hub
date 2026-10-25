## D102c report

Source comparison proves a regression in `689`:

- `runtime_protocol/service.py:2464-2507`, `_execute_timeline_commit` adds `context["request_id"]`.
- `runtime_protocol/timeline_commit_execution.py:214-234`, coordinator forwards it through `port_factory` and provider context.
- `runtime_protocol/timeline_commit_port.py:174-204`, `RequestCommitPort` accepts and retains the full context in sequential capture.
- Agent `astrid/sdk/timeline/commit.py:1160-1173`, `RuntimeCommitService.commit` deep-copies the extra key; no Agent top-level strict-key rejection occurs.
- Agent `astrid/sdk/timeline/_commit_preview.py:85-90`, the context enters the retained sequential proof.
- `runtime_protocol/timeline_commit_store.py:793-838`, `_historical_sequential` replays accepted ledger entries and calls strict validation.
- `runtime_protocol/timeline_commit_store.py:817`, `validate_commit_value(context, "CommitContext")` rejects `request_id` because `runtime_protocol/schemas/timeline-commit-bundle.json:4248` has `additionalProperties: false` and does not define that key.
- `runtime_protocol/timeline_commit_execution.py:198-208`, `_lookup` converts the replay exception to `CommitOutcomeUnknown` (503).
- `runtime_protocol/service.py:2523-2535`, this propagates as the standard nonexception 503 path; `public_failure` is not involved.

`request_id` does not alter canonical identity or authentication: `runtime_protocol/timeline_commit_store.py:41-44`, `request_identity`, excludes it. The change is therefore a private-context persistence/replay bug, not an auth or request-hash change. In `0c62`, the key is absent and the same accepted path completes normally.

Minimal candidate for the original author: retain `request_id` only for live diagnostics, strip it before storing sequential capture context, and normalize already-retained captures before strict replay validation. Do not widen the public/generated schema. Accepted/merged/refused status, body, authentication, and genuine 503 behavior must otherwise remain unchanged.

The exact native-seed 12031/4757 real-sequence comparison remains UNKNOWN: the authentic request/session/scopes and per-request App/Agent receipts were not available. Existing native-seed 503 records are facts, not standalone proof.

Tests were not run, per task prohibition against pytest/provider/service execution. Worktree product source is unchanged. `DONE` and the required commit message were created.