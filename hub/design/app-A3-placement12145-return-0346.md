## A3/P2 return report

Reverted the unsafe singleton-only raw-placement policy across the four owned files. Ordinary `trySnapToEdge` behavior is restored; protected tests/oracles remain unchanged.

Source decision: current metadata proves canonical composition scope, but not the verified active child owner/current scope/head required to authorize raw overlap. The existing fixture therefore remains:

- host `[0,12)`, pointer `4.5`, hold `5`
- raw `[4.5,9.5)`
- ordinary snap `9` → `[9,14)` → Runtime refusal

Required future raw predicate: exact embedded occurrence identity, matching project/timeline/head, one unambiguous canonical match, unique active non-source visual track/image. Missing, wrong, ambiguous, parent, or uncertain ownership must retain ordinary collision behavior. No safe source-derived policy was available here, so no raw guard was retained.

Tests:

- Node20 focused suite: 3 files, 29 passed.
- Node20 related union: 9 files, 183 passed; `shotTimelineDataProvider.a3.test.ts` failed before test execution because the bundled harness lacked `globalThis.navigator`.
- TypeScript app/node checks under flock: passed.
- Scoped ESLint `--max-warnings 0`: passed.
- `git diff --check`: passed.

No browser, Runtime service, full suite, protected-oracle edits, or fixture changes were made. Commit message written and `DONE` created.