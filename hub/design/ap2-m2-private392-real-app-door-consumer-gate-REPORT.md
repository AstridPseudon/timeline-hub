# App private392 real App-to-Runtime Door consumer qualification

## Result

UNQUALIFIED / BLOCKED at the required production-dist prerequisite. The
single central named suite was queued with the exact private392 Agent and
Runtime checkouts and proper venvs, but the existing hosted build recipe failed
before Vitest collection. No HTTP, Runtime Door, provider, or socket assertion
ran.

The failure is the known Viewing-owned current build gap, not a private392
identity mismatch:

```text
[vite:load-fallback] Could not load
.../src/tools/video-editor/lib/theme-api.fallback.tsx
(imported by src/tools/video-editor/compositions/TimelineRenderer.tsx): ENOENT
```

Vite transformed 3,205 modules before failing. I did not restore the deleted
theme/registry fallback and did not replace the production prerequisite with a
static proof.

## Changes in the App worktree

- Added the exact committed driver test from `85ae206b815381da31c229cc9107e322cb9c612f`:
  `tests/integration/runtimePrivate392Consumer.test.ts`.
- Added that test to the existing
  `config/testing/vitest.runtime-restore.integration.config.ts` while
  preserving `runtimeRestore.test.ts` in the config include list.
- Ported the exact prepared private392 generated counterpart and lock hashes:
  `runtime.lock.json`, `src/integrations/runtime/generated-contract-metadata.ts`,
  `src/integrations/runtime/generated.ts`, and
  `src/integrations/runtime/timeline-commit-types.ts`.
- Registered one named cache-crossrepo suite in the central test-service
  allow-list: `ap2-m2-private392-real-app-door-consumer-gate`.

The test uses the real App generic capture, command session, outbox, and
`RuntimeDataProvider` with `DirectHarness`; only fake IndexedDB is used for
outbox persistence. It asserts the declared merge/replace lowering, original
guards, opaque null/false/order preservation, lost ACK plus reload and exact
idempotency retry, disjoint rebase, guarded undo, stale same-leaf refusal, and
zero legacy POST traffic. The retained Agent native-only 10824 PASS2 was not
rerun.

## Exact identities

- Agent checkout: `/home/user/work/wt/agt-pin-1303ce6b`
  - HEAD `1303ce6be32e7bd96ed5c6b35afcb15819e81b50`
  - parent/source `e010e6a3868e963471244491bb6672c3e4a5135e`
  - schema `sha256:39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`
- Runtime checkout: `/home/user/work/wt/rt-pin-f8da4b6d`
  - HEAD `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`
  - health/schema `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042`
  - artifact manifest `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d`

The producer-backed `runtime.lock.json` check passed against the exact Runtime
checkout. The prior integration lock was updated to the exact f8da producer
and full generated hashes so the test does not silently qualify against the
older 2c4ac producer.

## Tests and evidence

Passed locally:

```text
node_modules/.bin/eslint tests/integration/runtimePrivate392Consumer.test.ts config/testing/vitest.runtime-restore.integration.config.ts --ext ts --max-warnings 0
  passed

node_modules/.bin/tsc --noEmit --pretty false
  passed

node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts
  3 files passed; 30 tests passed

node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d
  ok runtime.lock.json (matches pinned producer commit)

git diff --check
  passed
```

One central run was requested, as required:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-private392-real-app-door-consumer-gate \
  ap2-m2-private392-real-app-door-consumer-gate --no-cache
```

Result:

```text
ID: ap2-m2-private392-real-app-door-consumer-gate-ap2-m2-private392-real-app-door-consumer-gate-1020225511-6382
exit=1
phase: npm run build:hosted
test collection: not reached
```

The central command included the exact absolute environment paths and then
the exact one-file command:

```text
env ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-1303ce6b \
    ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
    ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-f8da4b6d \
    ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
    node_modules/.bin/vitest run \
      --config config/testing/vitest.runtime-restore.integration.config.ts \
      --no-cache --maxWorkers=1 --no-file-parallelism \
      tests/integration/runtimePrivate392Consumer.test.ts
```

Evidence log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-private392-real-app-door-consumer-gate-ap2-m2-private392-real-app-door-consumer-gate-1020225511-6382/log.txt`

## Blocker and next step

Viewing must supply the qualified current production build path or repair the
existing hosted build gap involving the missing `theme-api.fallback.tsx`.
After that source/build prerequisite changes, rerun this one named central
suite once. No public pin/adoption, browser/full suite, or replacement
qualification is claimed here.
