# App M2 parent-delete zero-POST triage

## Finding

The browser failure was a setup race, not a selection or keyboard-focus failure. The delete spec already selected the real `.clip-action`, asserted `data-selected="true"`, focused that same element, asserted it was focused, and sent the real `Delete` key.

The old readiness check only looked for any empty, non-pending IndexedDB outbox. `createTimelineCommandSession` can claim and persist that owner before `useTimelineCommandSession` stores the session in its ref and exposes `clipDeletePort` to the editor. The gesture could therefore run during the gap: the durable owner existed, but the native delete port was not yet mounted, producing zero Runtime POSTs.

## Change

`tests/e2e/local/clip-delete-command.spec.ts` now uses a local `openCommandTimeline` setup helper for both parent-delete cases. It snapshots existing owners before opening the timeline, then waits for a newly claimed owner that is empty and non-pending before performing either real Delete gesture. This mirrors the established readiness gate in `tests/e2e/local/three-products.spec.ts` and is a permanent focused regression for the session-mount race.

No production key handling, deletion fallback, command assertions, `useClipEditing.test.ts`, or legacy/opaque-data assertions were changed.

## Verification

- `git diff --check` — passed.
- Central exact suite requested once: `e2e-parent-delete-wave2-committed-tree92fd62-agent8130-runtime2c4-e2e-integration`.
- Result `app-m2-delete-wave2-zero-post-triage-fix-e2e-parent-delete-wave2-committed-tree92fd62-agent8130-runtime2c4-e2e-integration-1020173400-8750`: did not reach either browser case. The service snapshot was tree `97f0c5e7cd0933685464db541d49a0c2756ba84d`, while the registered suite pins `TIMELINE_CURRENT013_APP_TREE=92fd62f4adecdb3f93acf92a5444bf035d6aa19e`; its source audit failed before test execution. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-delete-wave2-zero-post-triage-fix-e2e-parent-delete-wave2-committed-tree92fd62-agent8130-runtime2c4-e2e-integration-1020173400-8750/log.txt`.

The browser gate remains unverified until the central suite accepts the candidate tree. The smallest peer action is to rerun the same suite with its App-tree audit parameterized to the committed candidate tree (or register an equivalent candidate-tree entry); no local browser or substitute test was run.
