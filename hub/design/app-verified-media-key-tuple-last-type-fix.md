# App verified-media key tuple and CAP composition

## Result

Fixed only the remaining `dataProvider.ts:1637` `MediaSelection` indexing
diagnostic. `sameMediaSelection` now uses a five-element `as const` key tuple,
so each lookup is typed against the existing `MediaSelection` carrier. The
exact five-key count, project-scoped comparison, mismatch refusal, and
immutable selection behavior are unchanged. No `any`, suppression, API, or
semantic change was added.

Composed the approved 30-path CAP candidate from
`dca891972840f502c974fbf3c3b1d585855842c` (read-only merge-base
`c57dcc26162642f503532f143ceb96bb185273aa`) onto current integration
`180d2aaeaa7b330ca5677e0e11f985e2d00d9116`, retaining the four current trim
port files. Added the prior `shotSetCapture` narrowing unchanged. The final
worktree has 32 task paths: 30 CAP paths, the prior shot narrowing, and this
tuple typing fix. No new semantic CAP edit was made.

The final source is uncommitted; the harness will assign its committed tree
hash. Source root/merge parent for handoff: `180d2aae` / `c57dcc26`.

## Verification

- Verified-media Vitest:
  `node /home/user/work/app/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/mediaImport.test.ts`
  — exit 0; 2 files and 80 tests passed.
- Targeted lint:
  `node /home/user/work/app/node_modules/eslint/bin/eslint.js --no-cache --max-warnings 0 src/integrations/runtime/dataProvider.ts`
  — exit 0.
- `git diff --check` — exit 0.
- One locked private13 project typecheck, with `NODE_OPTIONS=--max-old-space-size=4096`,
  `flock -x /home/user/work/.app-tsc.lock`, and `tsc --noEmit -p
  <private-leaf>/tsconfig.app.json --pretty false` — exit 0; zero diagnostics.
- Private13 overlay: version 0.0.13, 77 regular files. Archive: 77 regular
  members, SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
  Shared Composition resolution remained version 0.0.10 and was not written.

No full suite, install, browser, render, deep import, pin, package mutation,
or shared dependency/cache write was performed. The fallback Viewing ACK
remains separate and is not claimed here.

## Next step

Have the harness commit this worktree and run the orchestrator's integration
qualification on the resulting commit.
