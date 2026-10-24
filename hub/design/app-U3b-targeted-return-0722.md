## U3b report

- Fixed legacy derived-label resurrection in `timeline-data.ts`; explicit user labels remain preserved.
- Added no test changes or dependency changes.
- A3 provenance confirmed: all 36 failures were one missing Node20 `navigator` fixture; passed with documented private preload shim.

Checks:

- Exact 27-file Vitest union: **27 files, 695/695 tests passed**
- Gate 5: **12/12 passed**
- Node20 typechecks: root, app, node **passed**
- Scoped ESLint, `git diff --check`, Astrid conformance: **passed**
- Ancestry check: `2a288e6…` is ancestor of `HEAD`
- Playwright discovery listed 15 tests but exited 1 because all were marked NOT RUN; no browser run performed.
- No full suite, browser, backend, HTTP, build, or provisioning run.

Commit message and `DONE` marker created.