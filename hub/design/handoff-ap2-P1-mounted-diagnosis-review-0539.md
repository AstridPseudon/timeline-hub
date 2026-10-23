# P1 mounted diagnosis review — 0539

Independent review: **PASS for source/diagnosis classification; actual P1
behavior FAIL/blocked**.

Reviewed unchanged App commit `ec8e8a25cf7ac29247d06bc5a224b94145ee71c3`, tree
`25140dfd23eeea6e731a4168fce10fa4bff87d8f`, against PLAN §3 P1 and C0 §§1–5,7.

Findings:

- `useTimelineSave` gates the production local save path on the verified
  original basis, then recoverable identity, then `createLocalSaveSession`.
- `createLocalSaveSession` filters recoverable owners to nonempty/pending rows
  and eagerly claims an empty owner. `createCommitOutbox` uses
  `astrid.command-outbox`; the production and P1 browser queries read `owners`
  and filter stored `scope.timelineId`.
- The positive `openChain` owner wait and all original P1/C0 assertions remain
  intact; no weakening/removal was found.
- The author-run offline mounted witness passed, but its scratch source/log was
  removed before this review and could not be independently rerun. It is
  lifecycle/storage evidence only, not browser evidence.
- Actual service run 23041 failed both original cases at the pre-split idle-
  outbox assertion after 90 seconds. Its browser trace/error-context artifacts
  and service worktree are absent, so the exact live error/state is unverified.
  The scratch-only missing-default-output error is not attributed to 23041.

Checks: P1 list **PASS** (2 tests); `tsconfig.app.json` and `tsconfig.node.json`
typechecks **PASS**; scoped ESLint **PASS**; closest offline session/outbox/
handoff tests **PASS** (4 files, 73 tests); clean `git status` and
`git diff --check`. No HTTP, browser, socket, service, build, full suite, or
source change was made.

Recommendation: retain the positive wait and original tests; recover or freshly
capture retained browser diagnostics with artifact retention before any App
diagnosis or behavioral retry. Full findings and commands are in the worker
report:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-mounted-diagnosis-review-0539/report.md`.
