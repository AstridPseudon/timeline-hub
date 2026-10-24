## Report

- Updated `scripts/installer/update-manifest.test.mjs` to derive the current App schema digest while retaining the exact `867f…` assertion and independent wrong-digest refusal case.
- No manifest or production updater changes.

Tests/checks:

- Installer tests: 4/4 passed.
- Vitest skew guard: 2/2 passed.
- Runtime schema guard: 2/2 passed.
- Updater `--plan`: unchanged pins/digest.
- JS syntax, JSON validation, ESLint, and `git diff --check`: passed.

No blockers. DONE marker and commit message were created.