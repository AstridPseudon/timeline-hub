## PASS

Implemented in:

- `scripts/testing/d66-plain-stack.mjs`
- `scripts/testing/d66-plain-stack.test.mjs`

Added exact selectors:

- `p2-popup-add`
- `p2-parent-move`

Preserved P2 aggregate count: 8; P3 count: 1. No original specs or product files changed.

Tests/checks:

- Node20 targeted test: `22/22 PASS`
- Node20 `--check`: PASS
- Scoped ESLint: PASS
- `git diff --check`: PASS
- List-only collections: all eight selectors `1`; P2 `8`; P3 `1`
- Six protected spec SHA-256 values: unchanged
- No browser, normal body, full suite, credentials, or test-service run

Base source: `c184bd0bec5d10292647600272329534e058d474`

Commit message and `DONE` marker created. Recommended next step: manager merges, then runs meaningful isolated P2 qualification after Runtime’s native wait fix.