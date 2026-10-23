Implemented A4 bridge and focused test.

- Added test-only producer under `src/tools/video-editor/commands/fixtures/`.
- Uses real prepared-media command, preview, handoff, local session, and outbox paths.
- Captures before Runtime acceptance; no fake acceptance response.
- Validates exact five-field image selection and refuses missing/malformed inputs without output.
- Exposes `producePreparedImageRequestFromPaths(inputPath, outputPath)`.

Tests/checks:

- Vitest: 6 files, 106 tests passed.
- Producer test: 1 passed.
- Root/App/Node `tsc --noEmit`: passed under flock.
- Scoped ESLint `--max-warnings 0`: passed.
- Diff/scope check: only the two requested fixture files changed.

Dynamic output includes the real idempotency key, outbox step ID, generated clip ID, and SHA-256 of the exact request JSON. Bare `tsx` CLI invocation still requires the App’s existing Vite Astrid-pack alias resolver; the external-path interface is verified through configured Vitest. No full, browser, Agent, or Runtime fixture suites were run.