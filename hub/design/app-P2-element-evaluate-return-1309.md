## Completed

Fixed `readElementApplyUiState` so `page.evaluate` no longer depends on module closures. Added VM coverage executing the actual serialized function across all Apply states, malformed fallback, and redaction.

Changed only:

- `tests/e2e/local/support/p2-element-diagnostic.ts`
- `tests/e2e/local/support/p2-element-diagnostic.test.ts`

## Tests

- Node diagnostic suite: 28 passed
- Isolated mounted Vitest: 97 passed
- TypeScript: `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json` passed
- Scoped ESLint: passed
- `git diff --check`: passed
- Playwright list-only: 23 tests collected; no browser execution

## Finding closure

Resolved the reported `ReferenceError` caused by serialized evaluation missing `applyButtonState` and `UNKNOWN_UI`.

Current file hashes:

- Diagnostic: `d91eea281af85c8b61e74ba810441059e038ebebce7a8c9eeb366c3cd9fc6c59`
- Test: `797882ac07e61250a54e5d3d315dde653b27581b14cfd7fb76e0a72478d4b607`

The shared receipt helper remains owned by the parallel register task.

| ID | Scope | Status | Evidence |
|---|---|---|---|
| P2/D58-element | Self-contained evaluated Apply UI sampler and regression test | PASS, branch-only | Node 28, Vitest 97, three typechecks, lint, diff, list-only |

Commit message written and `DONE` created. No full/browser/service suite run.