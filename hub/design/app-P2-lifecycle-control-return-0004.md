Implemented the authentic D21 bootstrap diagnostic witness.

- Changed only `tests/e2e/local/mounted-readiness-safety.test.ts`.
- Replaced fabricated `page.evaluate` data with:
  - serialized production init script;
  - real `emitTimelineSaveDiagnostic` and `markTimelineSaveRejection`;
  - real `bootstrapMountedBaseline` `finally`;
  - real retention writer/output attachment and JSON readback.
- Covered readiness phases, classified primary failure, security redaction, missing/closed/write-failure paths, and bounded overflow.
- No `helper/app.ts` change; no production behavior blobs changed.

Validation:

- Node tests: 20/20 passed (12 mounted, 8 D21).
- Scoped ESLint: passed with `--max-warnings 0`.
- App, Node, and root TypeScript checks: passed under flock/4096 MB.
- `git diff --check`: passed.
- No browser, backend, HTTP, native, full, or service suites run.

Commit message written and `DONE` marker created.