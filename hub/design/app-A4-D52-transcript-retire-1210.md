## Report

- Deleted only:
  - `transcriptAssociateCapture.ts` — 573 lines, SHA-256 `a4db5418…`
  - `transcriptAssociateCapture.test.ts` — 397 lines, SHA-256 `56c1c0bb…`
- Rechecked callers at `602f8b1f...`: no production imports or dynamic callers; live `useProjectTranscriptHost` path and negative assertions remain intact.
- Inventory: 5 `it` declarations, 1 `describe`, 40 `expect` calls (no 7 declarations present).
- Tests: 4 pinned Node 20 Vitest files passed, 50 tests.
- Typechecks: `tsconfig.json`, `tsconfig.app.json`, and `tsconfig.node.json` all passed with `--noEmit --incremental false`.
- `git diff --check` passed; diff contains exactly two deletions.
- Lint: N/A per deletion-only scope. Full/browser/backend suites not run.
- Commit message written; `DONE` marker created. Branch remains uncommitted/branch-only for independent review.