# Validation

Verdict: `PASS_SOURCE`.

## Targeted behavior

- Exact required command, Node `20.19.4`: `npm exec vitest -- run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 src/tools/video-editor/components/AgentChat/NewChatMenu.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMenu.test.tsx --reporter=dot` — **2 files, 127 passed**.
- Own warm-up predicates only, Node `20.19.4`: `npm exec vitest -- run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 src/tools/video-editor/components/AgentChat/AgentChat.projectContract.test.tsx -t 'recovers a (generic|setup) warm-up failure without creating another session' --reporter=verbose` — **2 passed, 37 filtered by the explicit test-name expression**.
- Central ordinary test service targeted snapshot of the two affected files — **2 files, 127 passed**; used only as service mechanics confirmation.

## Static/source controls

- `npm exec tsc -- -p tsconfig.app.json --noEmit --incremental false` under Node `20.19.4` — **PASS**.
- `npm exec tsc -- -p tsconfig.node.json --noEmit --incremental false` under Node `20.19.4` — **PASS**.
- Scoped `npm exec eslint -- --max-warnings 0` over all touched/resolved App TypeScript files — **PASS**.
- `git diff --check` — **PASS**.
- `git ls-files -u` — **0 unresolved entries**.
- Conflict-marker scan over the source tree — **0 markers**.
- Test AST hygiene scan — no `.skip`, `.only`, `.todo`, or `.fails` modifiers in the affected menu tests.
- Source/test SHA-256 manifest checks — **PASS**.
- Merge-tree/outside-blob audit — exactly seven expected resolution deltas and exactly three final return files.
- Ancestry checks for `d5a1`, `002a`, `36e1`, and `e904` to the reviewed tip — **PASS**.
- Manifest JSON/pin audit — Agent, Runtime, schema digest, VibeComfy, and OMP preserved; producer cut pins remain pending.

No full, browser, e2e, live-socket, native, profile, build, ZIP, merge, push, checkout, ref deletion, credential, hub, or external product write was performed. Final producer-first cut acceptance is not claimed by this source review.
