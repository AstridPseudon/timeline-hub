# D127 independent protected review

## Verdict

**FAIL overall.** The exact central proof passes, and the helper's bounded leaf/lifecycle source semantics are internally coherent, but the settled acceptance gate is not met:

1. The required exact original assertion-AST custody is false. The parent contains 19 test functions and 160 `ast.Assert` nodes, not 169. All 19 original function names remain, but five existing tests have changed assertion ASTs; the retained-original set has 163 assertion nodes. These edits are not skips or an obvious weakening, but they are not exact preservation.
2. App84857's strict bootstrap validator is incompatible with the candidate output and identity. It exact-keys summaries/sampling/retention, accepts only old lifecycle values, and allows only the old normal/reviewed helper hashes. The candidate adds `lifecycle`, `top_leaf_frames`, per-row `lost_samples`, and `buffer_complete`, changes lifecycle values to `completed|raised|returned_without_response|pending_at_stop`, and has helper SHA256 `4ee0424b...`.

Disposition by dimension:

- `PASS_PROOF`: exact existing central request passed all 23 tests on the exact candidate tree. Own offline controls passed 21 tests; the two socket controls were intentionally deselected locally and are covered by that central receipt.
- `PASS_SOURCE_SEMANTICS`: only the two authorized files changed; nearest-safe leaf projection, truthful lifecycle distinction, buffer completeness, bounds, watchdog cancellation, privacy allowlist, and exception preservation are present in the candidate diff.
- `FAIL_SOURCE/ACCEPTANCE`: exact assertion custody and App validator compatibility remain unresolved. The App seam is App-owned; no App/Runtime fix was made here.

## Source/caller/privacy findings

The helper remains test-only and opt-in. Its existing caller chain is App persisted outbox → `commitSession` → registered `dataProvider.commitTimeline` → generated canonical POST with `Idempotency-Key` → Runtime `RuntimeHandler._dispatch`/`_timeline_commit` and registered provider. No alternate writer, product hook, collector, or new persistence was added.

The diff retains the safe-frame allowlist, route template sanitization, key hashing, private `TMPDIR` sink with exclusive `0600` creation, watchdog cancellation, and strict `8/128/65536/20ms` budgets. No raw bodies, keys, credentials, private URLs, or exception text are introduced. Historical request 3 remains `PENDING`; its missing provider leaf, response, wall denominator, and duration are not inferred.

## App-owned validator seam

Before any reviewed activation, App should update only its own strict validator seam at `tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` (currently `assertRetention` lines 101–151, `assertSampling` 169–216, `assertCaptureEvent` 218–300, and `readCapture` 310–317) and its reviewed hash constant at line 14. The required changes are to allow and validate the new fields/outcomes while preserving all existing bounds/privacy checks. This review did not edit that file.

No safety/classifier/permission refusal occurred. SWAP recovery remains untouched.
