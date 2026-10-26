# Validation

All commands used the author-approved pinned Node 20.19.4 binary at `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node`.

- `PATH=... node --import tsx --test tests/e2e/local/support/d141j-visibility.test.ts` — PASS, 3/3.
- `PATH=... npm exec -- eslint tests/e2e/local/support/d141j-visibility.ts tests/e2e/local/support/d141j-visibility.test.ts --max-warnings 0` — PASS.
- `node --max-old-space-size=6144 node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.test.tsx` — PASS, 13/13. The run emitted only the existing React `act(...)` warning.
- Positive `/home/user/.../node scripts/testing/check-d141j-visibility.mjs <review scratch>/visibility-proof.json` — PASS, two reads, five occurrences, five groups.
- Negative checker against the deliberately stale artifact — expected FAIL, rejected non-unique stale `accepted-read-2` association.
- `flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 PATH=... /home/user/work/wt/app-A3-D141j-mounted-capture-review-1305/node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json` — PASS, exit 0.
- Same locked command with `-p tsconfig.node.json` — PASS, exit 0.
- `git diff --check` — PASS. Candidate worktree remains clean; the author commit contains only the two bounded support files.
- Read-only SHA-256 census confirms unchanged `app.ts`, popup spec, production collector module, and checker blobs.

Not run by instruction: full suite, browser/service/request/body/collection, test service, preflight, registry/CAS/queue, package installation, native mounted diagnostic, merge, or build. The author’s prior route packet’s wrong coordinate and missing checkout in a normal recipe were reviewed as unrelated packet issues.
