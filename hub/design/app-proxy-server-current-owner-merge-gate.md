# App proxy server current-owner merge gate

**READY TO MERGE** the bounded, inactive server unit. No blocker or new design decision.

Base: `6ff21cac9deee3aae014e5c9e65d9871a3452f77` (tree `27d41c1b0e64ff9028f78576804f3b8cb3b9f1d5`). Final candidate and both central snapshots: **`ee34b6a1b24ccb76133edc9223d5030c3be4310e`**. Branch: `tl/app-m2-proxy-server-current-owner-merge-gate`. Harness supplies the final commit after exit; no commit/merge/checkout was run by this worker.

## Scope and source

Read PLAN, the Runtime proxy agreement, server security review, Vite nomination repair, coupled final review and response-regression final approval. Followed the 11:54 owner direction without changing the agreed transport.

Extracted exactly these six paths from approved `ad05c5bd3554cc7b86c2ba3e7b8c0fb7a38e69ca`, relative to `7bb885b638838588a0dff81b64b7c34960ac07f3`:

- `config/vite/runtimeProxy.ts`
- `config/vite/vite.config.ts`
- `scripts/dev-local-workspace.mjs`
- `scripts/runtime-discovery-proxy-operation.test.mjs`
- `scripts/runtime-discovery-proxy.d.mts`
- `scripts/runtime-discovery-proxy.mjs`

All six were unchanged between 7bb and 6ff before extraction. All final bytes equal ad05; the five product/declaration files also equal `66fc28fafabcc074c688e7a7b50b296df41fc70f`. Candidate diff is exactly **6 files, +1016/-9**, including the new 620-line operation suite. An explicit allowlist assertion and a complete file-content/mode comparison against the central Git tree passed. Every other tracked path equals 6ff, including its parity configs, existing tests, MAIN/chat behavior, src, generated clients and package/lock/runtime pins. Current locally available `origin/main` is `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa`, an ancestor of 6ff. `git cat-file -e '17e46de99^{commit}'` exits 128: the newer MAIN17 object is absent, so no ancestry or qualification against it is claimed.

The unit installs the local operation route, immutable server-owned handle binding and retirement, then strips raw/normalized Connection nominations before Vite/http-proxy rewrites them, including the Expect path. Admission is checked before and after stripping; nominated handles refuse locally. Only the pinned Runtime bearer is injected upstream. Browser-facing responses use the existing restricted header set and no-store. Existing ordinary discovery/cache/routing remains separate.

No browser operationHost, dataProvider or host-integration fixture was imported. Production requester remains inactive. The handle route is local HTTP same-origin only; hosted/paired transport remains unsupported. Existing tests/fixtures/expectations were not edited or weakened: the new operation test file is byte-identical to the approved source.

## Exact verification

Here `$ORCH` is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`.

Both named central suites ran once after the final source edit, on tree `ee34b6a1b24ccb76133edc9223d5030c3be4310e`:

```sh
$ORCH/bin/request-test app-m2-proxy-server-current-owner-merge-gate proxy-operation-integration
$ORCH/bin/wait-test app-m2-proxy-server-current-owner-merge-gate-proxy-operation-integration-1020120734-27607 0
$ORCH/bin/request-test app-m2-proxy-server-current-owner-merge-gate proxy-operation-neighbors-integration
$ORCH/bin/wait-test app-m2-proxy-server-current-owner-merge-gate-proxy-operation-neighbors-integration-1020120734-28729 1
```

- Operation lane: **exit 0, 19 passed, 0 failed/skipped/cancelled**, 6s service time. Executed `node --test scripts/runtime-discovery-proxy-operation.test.mjs`.
- Neighbor lane: **exit 0, 136 passed** = 61 launcher + 12 chat + 63 Vitest, no failures/skips/cancellations, 40s service time. Exact command:

```sh
node --test scripts/dev-local-workspace.test.mjs && env TSX_DISABLE_CACHE=1 node --import tsx --test scripts/astrid-project-chat-runtime.test.ts scripts/astrid-project-chat.test.ts && node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/paired/objectCachePolicy.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts src/integrations/runtime/workspaceRuntimeConfig.test.ts src/integrations/runtime/client.runtimeOrigin.test.ts
```

The operation lane retains the original actual Vite → proxy → synthetic Runtime x-first/x-second negatives; duplicate raw/mixed-case nominations; Expect variants; nominated-key/handle, invalid-origin and metadata refusals; upstream credential/handle negatives with Authorization exactly the pinned bearer; and downstream Authorization, Proxy-Authorization, Cookie, handle, Set-Cookie, nominated headers and CORS negatives. Normal body/path/query/method/Range and no-store positives pass. Existing lifecycle, timeout, upload, stream and restart cases pass.

Direct checks, all exit 0:

```sh
git diff --check
node --check scripts/runtime-discovery-proxy.mjs
node --check scripts/dev-local-workspace.mjs
node --check scripts/runtime-discovery-proxy-operation.test.mjs
node --test --experimental-test-isolation=none --test-name-pattern='^pure:' scripts/runtime-discovery-proxy-operation.test.mjs
node node_modules/eslint/bin/eslint.js config/vite/runtimeProxy.ts config/vite/vite.config.ts
git diff --check HEAD ee34b6a1b24ccb76133edc9223d5030c3be4310e
```

Pure run: **7 passed, 0 failed/skipped/cancelled**. The source-equality, six-path allowlist and complete snapshot-content/mode assertions also passed. Initial nonblocking waits returned 124 while running; the same requests were waited without resubmission. Central evidence is in `tests/<request-ID>/{snap,summary,log.txt}` for the two IDs above.

## Limits and handoff

No full, broad 363-case host lane, browser, build, install, tsc or affected-941 qualification was run or claimed. All listeners ran in the central service. Shared dependencies, caches, venvs and runtimes were read-only; Vite fixtures use removable private cache directories, Vitest disables cache with runner config loading, and tsx caching is disabled. No temporary/build output remains in the worker tree.

These synthetic transport gates do not establish real Runtime acceptance/receipts, exact retry after lost ACK/restart, undo, requester/outbox/native capture composition or browser activation. Two-process retirement cannot undo already dispatched acceptance; remote credential revocation/port reuse is not synchronously observable. Those previously agreed activation limits remain.

Recommended next step: harness commit and orchestrator merge of this six-path unit onto 6ff; refresh MAIN17 separately when its object is transferred and qualify any resulting composition separately. Report and commit-msg written; DONE and KEEP markers retained as requested so this exact worktree remains available for review. No BLOCKED marker.
