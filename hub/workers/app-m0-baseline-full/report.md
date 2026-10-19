## App M0 baseline report

Completed the full requested suite:

```text
npm test -- --maxWorkers=2 --reporter=verbose
```

Result: exit `1`, completed in `39m48s` (under the 60-minute ceiling; no manual termination).

- Test files: `1432 passed, 15 failed, 0 skipped / 1447`
- Tests: `17954 passed, 56 failed, 0 skipped / 18010`
- Errors: `24`
- Full log: [/tmp/app-m0-baseline-full/npm-test-maxWorkers2-verbose.log](/tmp/app-m0-baseline-full/npm-test-maxWorkers2-verbose.log)

Additional evidence:

- `npm run test:contracts`: 1 file / 1 test passed.
- Chromium explicit probe passed; Playwright-managed lookup lacked `chromium_headless_shell-1223`.
- Worktree clean; `git diff --check` passed.
- No product/config/test edits made.

Reports written:

- [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m0-baseline-full/report.md)
- [app-baseline.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-baseline.md)
- [commit-msg](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m0-baseline-full/commit-msg)

The report contains every failed test, representative reasons, exclusions, and recommended next steps.