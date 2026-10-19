Implemented [commitOutbox.ts](/home/user/work/wt/app-m1-outbox/src/tools/video-editor/commands/commitOutbox.ts) and its tests. It persists exact requests before sending, fences ownership by exclusive lock and generation, atomically ACKs only the matching prefix, preserves dependent intent, and retains rejected work as conflict.

Exported API:

- `createCommitOutbox()` exposes `create(scope, callback)`, `list(scope)`, and explicit `recover(scope, ownerId, callback)`.
- Claimed handles expose `read`, `append`, `cancel`, and `dispatch`.
- Each intent represents one atomic command batch. Builders receive original payload and resolved base; retries bypass builders and reuse stored method/path/body/key.
- Transport returns `accepted`, `rejected`, or `retry`. Runtime DTO construction and response validation remain adapter responsibilities.

Verification:

- `npx vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/commands/commitOutbox.test.ts` — **17 passed**.
- `npx eslint src/tools/video-editor/commands/commitOutbox.ts src/tools/video-editor/commands/commitOutbox.test.ts --max-warnings 0` — passed.
- `npx tsc --noEmit --strict --target ES2020 --lib ES2020,DOM --module ESNext --moduleResolution bundler --skipLibCheck src/tools/video-editor/commands/commitOutbox.ts` — passed.
- `git diff --check` and individual untracked-file whitespace checks — passed.

No blockers or plan deviations. The core stays transport-opaque because generated commit types are absent. Abort tests add rollback semantics to the vendored fake; browser durability and full suites remain unverified, as scoped.

Commit message written to `ORCH/workers/app-m1-outbox/commit-msg`. Next: wire the Runtime adapter and gesture capture, then run the adversarial reload journey.