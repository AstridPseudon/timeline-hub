## Report

- Deleted exactly four dormant files:
  - `parentAfterAnchorCapture.ts` and `.test.ts`
  - `trackReorderCapture.ts` and `.test.ts`
- No production callers or exports found. Pre-delete references were only the modules’ own tests.
- Preserved `transcriptAssociateCapture` and all live A2 behavior.
- D52 owner amendment supersedes D37; ledger was not modified. Replacement rows: existing ledger lines 69–70.

Validation:

- Vitest: 4 files, 49 tests passed under Node 20.19.4/npm 10.8.2.
- Typecheck, serialized with flock:
  - `tsconfig.json`: passed
  - `tsconfig.app.json`: passed
  - `tsconfig.node.json`: passed
- ESLint: not applicable; no surviving changed TS files.
- `git diff --check`: passed.
- Four-file-only deletion/integrity check: passed.
- Residual identifier scan: zero matches.
- Transcript files: unchanged.

Base SHA/tree: `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4` / `542b772e6deed676b917f857708445b7d37a5aa8`.

Commit message and empty `DONE` marker written. No blockers.