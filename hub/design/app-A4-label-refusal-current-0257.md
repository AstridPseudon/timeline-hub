Implemented the reviewed A4 label-refusal port.

- Added exact donor test blob: `3133a89659f6f48bcc18936478d81f3731e1a6ac`.
- Removed only the three mapped declarations from `commitSession.test.ts`.
- Preserved ownership, display-basis, and mixed-preview refusals byte-identically.
- No production/helper changes.

Checks:

- Six-file targeted Vitest lane: 128/128 passed.
- Root/App/Node TypeScript checks: passed.
- Scoped ESLint: passed.
- `git diff --check`: passed.
- Completion marker and commit message written.

No full/browser/backend suites run.