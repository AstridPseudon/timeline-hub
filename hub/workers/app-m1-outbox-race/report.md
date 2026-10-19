Fixed only `commitOutbox.ts` and its test.

- Latest ACK now retains its intent identity and exact acceptance. Delayed B preserves `basis.after`, original payload/guards/IDs, uses base HA, and gets a fresh request key.
- Released claims cannot begin transmission. Exact retries and stale-completion fencing remain intact.
- Added six cases covering late append/reload, unsupported predecessors, independent versus dependent conflicts, and release before send. Original 17 tests retain their strength.

Validation:

- `npx vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/commands/commitOutbox.test.ts` — **23 passed**.
- `npx eslint src/tools/video-editor/commands/commitOutbox.ts src/tools/video-editor/commands/commitOutbox.test.ts --max-warnings 0` — passed.
- `npx tsc --noEmit --strict --target ES2020 --lib ES2020,DOM --module ESNext --moduleResolution bundler --skipLibCheck src/tools/video-editor/commands/commitOutbox.ts` — passed.
- `git diff --check` — passed.

Bounded API choice: late handoff supports only the latest accepted predecessor when the queue is empty, preserving tail ordering without accepted history. Independent work stays unconflicted but remains blocked behind a rejected prefix.

No blockers or plan deviations. Full/browser tests were not run; browser durability remains unverified. Next: manager review and integration.

[Commit message written](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m1-outbox-race/commit-msg). No manual Git mutation performed.