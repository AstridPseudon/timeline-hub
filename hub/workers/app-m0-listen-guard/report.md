## Completed

- Updated both listener helpers to reject original `server` errors promptly and remove temporary error listeners on success.
- Covered both paired transport listener sites.
- Preserved cleanup, assertions, and address checks.
- Changed only the two permitted files.

Validation:

- `git diff --check` — PASS
- File-scoped ESLint — PASS
- Loopback suites — not run, deferred to targeted `--net` worker as instructed.

Reports:

- [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m0-listen-guard/report.md)
- [commit-msg](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m0-listen-guard/commit-msg)