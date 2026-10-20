# ACP events fixture current-tip qualification

## Result

APPROVE the two-line test-only delta from `f0e4917ba27005a6022b4b0103ebf2e5c9447adb` for separate manager merge. The current-tip worktree contains only the approved `/events` fixture arm in `useAgentSession.proposal-vertical.test.tsx`:

```ts
: url.endsWith('/events')
  ? { notifications: [], disconnected: false }
```

No product source, route, credential, guard, parser, expected-failure marker, skip, or alternate assertion changed.

## Exact source identity

- Base/current Git `HEAD`: `e5c71515d10dc5e03320aad597bac20c0fd0b579`.
- Base tree: `84a2b8240cb385ae2cd9cc57c68a7b2df78517c4`.
- Candidate post-delta tree (computed without Git writes): `9b88aa71f50d0802993bc0d53bfe8aabc96d4a1b`.
- Changed file base blob: `c10a139785491b332335f52599d18446383e799c`.
- Changed file candidate blob: `e158f0072f742f14b203dfaa3f7d544324b38bb5`.
- The future commit SHA is intentionally not known; the harness commits this worktree.

## Preservation and diagnosis

The original test body remains intact apart from the two approved fixture lines. It still sends `apply proposal`, asserts a request to `/acp/projects/project-1/chat/prompt`, receives HTTP 403 there, expects `session_not_owned`, and asserts that `proposalApply` is not called.

The historical full App baseline had six failed nodes, including this proposal-vertical test. Its failure was `bridge_contract_violation` instead of the intended `session_not_owned`: the mock returned the catch-all ownership-error object with HTTP 200 for `/events`, so strict ACP event parsing stopped before the prompt request. The valid `{ notifications, disconnected }` response now lets the unchanged test reach the prompt and its intended 403 response. This qualification does not claim that the other five historical full-suite baseline nodes are fixed.

## Required evidence

Using the standard physical deps8 tree `/tmp/app-m2-coherent-deps8/node_modules`, exposed through a private overlay at the worker path (including private `.vite`, `.vite-temp`, and `.cache`), the exact review cohort passed:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
  node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  src/tools/video-editor/hooks/useAgentSession.proposal-vertical.test.tsx \
  src/tools/video-editor/hooks/useAgentSession.test.tsx \
  src/tools/video-editor/hooks/useAgentSession.projectContext.test.tsx \
  --maxWorkers=1
# PASS: 3 files, 62 tests, exit 0
```

```sh
node_modules/.bin/eslint src/tools/video-editor/hooks/useAgentSession.proposal-vertical.test.tsx
# PASS, exit 0

git diff --check
# PASS, exit 0
```

No full suite, build, browser/e2e, TypeScript check, install, live socket, or Agent/Runtime execution was run or claimed.

## Handoff

The unit is source-ready and individually mergeable after the manager's gate. No blocker was found. The manager must preserve separate merge order and must not treat this targeted result as a full-suite result.
