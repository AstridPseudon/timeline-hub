# App transcript typing triage — 2026-10-21

## Result

Ready-to-merge one-file candidate on App HEAD `1a54d30521945c7ea1ab7148e840011c8893c78d` (tree `941ff4c78ea72a48f6e83f310e54a4258f45e24b`). Only `src/tools/video-editor/commands/transcriptAssociateCapture.ts` changed.

The fix is type-only: it makes existing JSON/object/array guards explicit to TypeScript and annotates callback element types. It does not add a DTO, schema, operation, field, cast, writer, activation, or caller.

## Source and graph provenance

- Actual source cwd: `/home/user/work/wt/ap2-m2-transcript-own-type-origin-triage-fix-0535`.
- App source SHA/tree before the edit: `1a54d30521945c7ea1ab7148e840011c8893c78d` / `941ff4c78ea72a48f6e83f310e54a4258f45e24b`.
- Project TypeScript executable: `/home/user/work/app/node_modules/typescript/bin/tsc`.
- TypeScript package origin: `/home/user/work/app/node_modules/typescript/package.json`; version `5.9.3`.
- The target helper's compiler program resolved its local imports to this worker tree, including `timeline-commit-types.ts`, `timelineBundle.ts`, `projectTranscript.ts`, and `clipMovePrimitives.ts`. External React/Zod declarations resolved read-only from the shared install.
- App's immutable Composition archive: `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, exactly 77 regular members.
- Worker-owned temporary overlay resolved `@banodoco/timeline-composition` to version `0.0.13`, with TypeScript declarations at its private `dist/index.d.ts` / `dist/evaluation.d.ts`. Peer links were read-only links to the existing shared peers; no shared install was changed.
- The shared App `node_modules` resolves Composition `0.0.8`, while `package-lock.json` declares `0.0.13`; it was not used as Composition qualification evidence. The helper itself has no Composition import, so its target diagnostics are independent of that stale shared package. The private 0.0.13 module/declaration resolution was independently verified with the same TypeScript 5.9.3 resolver.

## Diagnostics

The prior HOME 71/52 capture was not used. It was invalid because it omitted the source cwd and resolved shared Composition 0.0.10.

Using the existing project compiler with a temporary target-only project config:

- Before: 52 diagnostics owned by `transcriptAssociateCapture.ts`, including unknown/nullable JSON narrowing and implicit callback types.
- After: 0 diagnostics for the target helper.
- External diagnostics: none in the target-only program. No whole-project typecheck claim was made.

## Tests and checks

- `./node_modules/.bin/tsc -p tsconfig.transcript-own-type.tmp.json --noEmit --pretty false` — before 52 target diagnostics; after exit 0 with 0 diagnostics. The temporary config was removed.
- `TMPDIR=/tmp/ap2-m2-transcript-own-type-tests-0535 PYTHONDONTWRITEBYTECODE=1 ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --no-file-parallelism --maxWorkers=1 src/tools/video-editor/commands/transcriptAssociateCapture.test.ts` — 1 file, 7 passed.
- Same Vitest options over `transcriptAssociateCapture.test.ts clipMovePrimitives.test.ts clipMoveCapture.test.ts authoringBundle.test.ts sourceMap.test.ts` — 5 files, 157 passed.
- `npm run typecheck:strict-islands` — passed.
- `./node_modules/.bin/eslint src/tools/video-editor/commands/transcriptAssociateCapture.ts src/tools/video-editor/commands/transcriptAssociateCapture.test.ts --ext ts,tsx --max-warnings 0` — passed.
- `git diff --check` — passed.
- No full, browser, socket, native, live route, schema-generation, install, or whole-project compile was run.

## Preservation and dormancy

The existing transcript tests retain exact command/record/read/write/dependency/order/opaque-field assertions and deep-equality atomicity checks; the 157-test neighbor cohort also passed. The edit does not alter JSON construction or mutation order. No live callers were found outside the helper's direct test; the helper remains dormant. The approved prior dormant capture/test files were otherwise untouched.

Ready for the harness commit; no blocker remains.

