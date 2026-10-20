# Runtime native render recovery map

Worker: `rt-m2-complete-native-render-recovery-map`  
Runtime product source: `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`  
Publication test source: `6b43f95ff6abffc7c935685879e38b58472b733d`  
Recovery test source: `4f1cee463d844bab4a800483492f18c79c7b5234`  
Agent source used by the native fixture: `3c4f6de4fa777323b3386c01c7266b619b86af6d`  
Fixture source: Runtime branch `tl/rt-m2-native-publication-fixture-slim`, commit `6b43f95`

## Replacement coverage

The replacement fixture is `tests/test_render_commit_publication_positive.py` and uses the
normal `load_timeline_commit_provider("astrid")` provider. It creates real Runtime tasks,
claims and durable managed proposal output, builds the request through the pinned Agent
provider, and commits through `commit_timeline` as the requester. It does not seed accepted
history, fabricate a proposal carrier, or use a PreparedProvider.

The new recovery cases are in `tests/test_render_commit_recovery_positive.py`:

- `test_actual_native_producer_refuses_cancelled_superseded_attempt_without_film_writes`
  checks a valid-fence mismatch, then retries and claims the real producer task and cancels
  that unsettled attempt. Both requests refuse through the producer contract. Timeline
  history, canonical head, publication checkpoint, and render-task count remain unchanged.
- `test_actual_native_acceptance_replays_after_crash_before_render_admission` accepts the
  native proposal, observes the prepared checkpoint and zero render tasks, closes/reopens
  Runtime, verifies completed-task cancellation is a no-op, replays the exact requester key
  and receipt, and admits the frozen pending render once. The five-field immutable selector
  is checked against the admitted render authority.
- `test_actual_native_render_refuses_stale_revision_selector_without_writes` retains the
  existing actual-film stale-selector negative and its SQL/render-task no-write assertions.

## Exact mapping to the unchanged legacy tests

The three tests in `tests/test_timeline_render_publication.py` are unchanged.

| Legacy function and assertions | Native replacement evidence |
| --- | --- |
| `test_publication_is_fenced_atomic_and_exactly_replayable`: atomic accepted publication, one render task, exact replay after cancellation | `test_actual_agent_publication_is_atomic_pinned_and_exactly_replayable` lines 151–204 in `test_render_commit_publication_positive.py`: accepted receipt/checkpoint, pinned selector, one render admission, cancellation followed by exact commit/task replay after restart. |
| `test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence`: stale fence refusal and cancellation seam leaves film/head/tasks unwritten | `test_actual_native_producer_refuses_cancelled_superseded_attempt_without_film_writes` in the recovery file: actual producer fence mismatch plus a claimed-then-cancelled pre-settlement attempt; exact history/head/checkpoint/render no-write checks. `test_actual_native_render_refuses_stale_revision_selector_without_writes` covers the separate accepted-revision selector refusal. |
| `test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart`: prepared state, restart, retry/resume, one render task | `test_actual_native_acceptance_replays_after_crash_before_render_admission` in the recovery file: accepted receipt and prepared checkpoint survive restart; exact requester replay returns the same result, then the frozen pending render is admitted once. |

The old direct-publish tests prove the retired assembler seam with their legacy fixture;
the new cases prove the settled-proposal/requester seam approved by D13. They are not
claimed to be the same temporal hook: D13 deliberately settles first, preserves completed
attempt identity across restart, and treats completed-task cancellation as a no-op.

## Scope and limits

No old publication test, product code, artifact, schema, or generated client was changed.
No full, browser, registered-real-MP4, or neighboring 86-test suite was run. The fixture
does not claim renderer execution or external requester outbox process death; it proves the
Runtime acceptance/checkpoint/replay and pinned render-admission boundary.

## Central selected-lane evidence

The worker-specific named suite `native-map-marked-gate-agent3c4f-integration` was registered
and run once through the central test service on 2026-10-20. Its exact command was:

```text
test "$(git -C /home/user/work/wt/agt-pin-3c4f6de4 rev-parse HEAD)" = 3c4f6de4fa777323b3386c01c7266b619b86af6d && test -z "$(git -C /home/user/work/wt/agt-pin-3c4f6de4 status --porcelain)" && env ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-3c4f6de4 PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-3c4f6de4 PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_render_commit_publication_positive.py tests/test_render_commit_recovery_positive.py
```

Result: **4 passed in 1.73s**, exit 0. The central snapshot recorded Runtime tree
`e5060cdfa57696ef8f04c76d7c12135869da541c`; its external-source record was Agent
`0b2f662e32e1a6818d58f9cf12130f0a89fb5a3b`, App
`8ffd2164bde532a50007d41376b0e10ce4d67473`, and Composition
`5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`. The test command itself additionally
asserted the clean, exact Agent checkout above. This proves the four selected Runtime
publication/recovery cases against the pinned Agent provider and exact Runtime snapshot;
it does not prove the legacy three-positive tests, registered MP4/outbox whole journey,
renderer execution, browser/live suites, or neighboring tests.
