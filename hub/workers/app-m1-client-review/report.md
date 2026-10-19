Consumer fixes complete: guarded restore uses the returned closure; fixtures have valid hashes/receipts; malformed links refuse; opaque occurrence fields survive; late ACKs preserve newer cache state; transient typed failures remain retryable.

Validation:

- Central targeted run: **203 passed / 8 files**.
- Final direct consumer run: **103 passed**.
- `npm run test:contracts`: passed.
- File-scoped ESLint, official vendor-lock checks, `git diff --check`: passed.

**Artifact hold remains.** Reviewed source `a24e7d24343a965dc0d3f0eada141bd45c8192d7` is byte-equal locally, but Runtime’s manifest still omits `timeline-commit-types.ts`. Generated files and pins remain unchanged. Runtime must publish reviewed manifest coverage before App refreshes the lock.

No full/browser suite or full typecheck ran. Commit message written. [Detailed report with exact commands and artifact tuple](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m1-client-review/report.md).