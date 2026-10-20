# Runtime native render recovery map

Worker: `rt-m2-complete-native-render-recovery-map`  
Runtime tree: `740fc9db023c79b9a2fab793d72083f2cdc0caeb`  
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
