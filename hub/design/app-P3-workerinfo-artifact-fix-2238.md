## Done

- Fixed D21 artifact persistence for real Playwright `WorkerInfo` vs `TestInfo`.
- Worker artifacts use `project.outputDir/worker-<workerIndex>`, mode `600`.
- Test-scoped artifacts still use `TestInfo.outputPath()` and attachments.
- Added real no-browser lifecycle controls for early artifacts and setup failures.
- Protected P1/P2/P3 journey bodies and harness remain unchanged.

## Tests

- `node --import tsx --test ...` — 13 passed.
- Scoped ESLint — passed, zero warnings.
- Locked root `tsc --noEmit` — passed.
- Playwright `--list`: P3 1, P1 2, P2 8 — exact counts.
- `git diff --check` — passed.

No full/browser/backend suite was run. No blockers.