# App2 compiler canary reviewed deletion delivery

## Result

Prepared the approved private compiler-canary deletion on the latest HOME
source. The final net source diff against HOME contains only:

- `src/tools/video-editor/lib/compiler-canary.ts` — deleted, 601 lines.
- `src/tools/video-editor/lib/compiler-canary.test.ts` — deleted, 1,570 lines.

The shared/public source-map runtime, source-code navigation, SDK surface,
native project-data controls, and their retained tests are unchanged. The
fixture-only `com.example.compiler-canary` values remain in retained tests.
No new code, API, DTO, pin, activation, browser, socket, or full-suite work
was added.

## Approval and source identity

The independent retirement review approved the exact candidate in
`ap2-m2-compiler-canary-dead-test-retirement-review-0115-REPORT.md`:

- Reviewed candidate source SHA: `645a5cc94c9730b5dc21757b4c90ad3b97944ae5`.
- Reviewed candidate tree: `9ae9121c0aac4f2cdb385e7831c99d05aeeb100a`.
- Latest HOME parent SHA: `813a85106ecb4abbaf224081abe6c33b8dab0df7`.
- Latest HOME parent tree: `2a19a78bb1bdfb3fd779f568a1b513b094318982`.
- Candidate parent is the exact latest HOME commit; no source divergence was
  found.

The review proved zero live static, dynamic, public, registry, manifest, or
SDK callers. The current source search has no remaining canary symbol or
module-path references outside the intentionally preserved strict-debt entry.

The review also verified the 59-test one-to-one mapping: all 59 declarations
map to ledger rows with the disposition `BEHAVIORGONE: private canary`. No
retained behavior assertion was weakened or removed.

## Strict-debt proposal

The reviewed candidate also removed this one stale entry from
`eslint.strict-debt.js`:

```diff
-  "src/tools/video-editor/lib/compiler-canary.ts",
```

The task requires this outside-the-usual-path hunk to remain a separate HOME
proposal unless owner approval is recorded in the inbox. No such approval was
present, so the entry is preserved in the delivered source. No lint threshold
was changed. This report preserves the exact reviewed hunk for a later
owner-approved separate patch.

## Ledger mapping

Proposed ledger row: the private compiler-canary module and its 59 private
self-tests are ready for the existing M2 deletion row's canary sub-entry.
Current status remains OPEN pending the actual HOME merge SHA. This report
does not mark the row DELETED.

## Verification

Passed targeted retained-neighbor tests:

```text
TMPDIR=/tmp/w-4eed7d5ba6 ./node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/lib/source-map-runtime.test.ts src/tools/video-editor/lib/source-code-navigation.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts
6 files, 439 tests passed
```

Passed final checks:

```text
./node_modules/.bin/eslint eslint.strict-debt.js --max-warnings 0
node --check eslint.strict-debt.js
git diff --check 813a85106ecb4abbaf224081abe6c33b8dab0df7 HEAD
```

No full suite, browser, localhost, live socket, or central gate was run.

## Merge-forward

The prescribed helper was attempted twice against `tl/integration`, including
after the final source adjustment. Both attempts failed before any merge or
conflict with the worker `.git` read-only guard:

```text
fatal: update_ref failed for ref 'ORIG_HEAD': cannot lock ref
'/home/user/banodoco/reigh-app/.git/worktrees/ap2-m2-canary-reviewed-current-deletion-delivery-0120/ORIG_HEAD.lock': Read-only file system
```

No `MERGE_HEAD`, ref update, or HOME merge SHA was produced. The final net
worktree diff against HOME is cleanly limited to the two deleted canary files.
The harness or HOME owner must perform the actual merge and then record its
resulting SHA before marking the ledger row DELETED.

## Recommended next steps

1. Merge this reviewed two-file deletion onto HOME using the outer merge
   mechanism.
2. Record the actual merge SHA and only then mark the canary sub-entry
   DELETED.
3. If desired, obtain owner approval for the exact one-line strict-debt
   cleanup as a separate HOME patch; do not alter thresholds.
