## Completed

- Added local refusal for `disabled: true` captured tracks.
- Added occupied-V2 positive coverage through the real mounted command service and A2 outbox.
- Strengthened `ShotTimelineMediaControls` mounted caller coverage.
- Preserved all existing negative and ordinary-placement tests.

## Verification

- Focused Vitest, Node 22.22.0: 8 files, 180/180 passed.
- Node 20.20.0: 7 files passed; `shotTimelineDataProvider.a3.test.ts` has an existing setup failure because `globalThis.navigator` is undefined.
- TypeScript (`tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`), Node 20: passed.
- ESLint on all changed files, Node 20: passed.
- `git diff --check`: passed.

No browser, backend, or full suite was run per instructions.

Commit message and `DONE` marker were written.