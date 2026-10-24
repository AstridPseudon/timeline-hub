## Report

Implemented D83 in:

- `scripts/testing/d66-plain-stack.mjs`
- `scripts/testing/d66-plain-stack.test.mjs`

Added opt-in `p3-diagnostic`:

- Copies the exact current Gate5 spec at runtime.
- Uses installed Playwright `expect.configure({ soft: true })`.
- Applies the existing Gate5 grep only.
- Preserves the original spec and removes the temporary copy afterward.
- Normal P3 remains unchanged.

Tests/checks:

- `Node20 --import tsx --test scripts/testing/d66-plain-stack.test.mjs` — 25 passed.
- Diagnostic and normal `--collect` list-only — both selected exactly one Gate5 test.
- Scoped ESLint — passed.
- Node `--check` — passed.
- Scoped TypeScript parse check — passed.
- `git diff --check` — passed.
- Protected hashes unchanged:
  - Gate5 spec: `93c2bf4c...559a64b`
  - Readiness spec: `2b9723db...301593`

A type-aware TypeScript check still reports existing repository/dependency errors outside this change. No browser, full suite, original run, or service submission was performed; no mismatch is claimed observed yet.

`DONE` and the conventional commit message were recorded.