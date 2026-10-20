# App private392 unmocked Door driver source

## Result

Added one repo-native integration case at
`tests/integration/runtimePrivate392Consumer.test.ts` and included it in the
existing `vitest.runtime-restore.integration.config.ts` lane. The case uses
the App's real generic patch capture, command session, IndexedDB outbox, and
`RuntimeDataProvider`; its transport sends HTTP through `DirectHarness`'s
authenticated Runtime browser Door. Runtime storage/provider semantics are
not mocked. Fake IndexedDB is used only for App outbox persistence. A second
App session uses the same builders over a separate real Runtime credential to
make the intervening writer.

The case asserts the exact tuple before starting: Runtime `f8da4b6d`, Agent
pin `1303ce6b` with parent/source `e010e6a3`, Agent schema `39211e63`, App
Runtime artifact manifest `52df520b`, and Runtime health schema
`242d2bc1`. It covers declared merge/replace lowering, original namespace and
leaf guards, opaque null/false/order preservation, lost acknowledgement plus
dispose/reload/exact idempotency retry, stale disjoint rebase, guarded undo,
same-leaf stale zero-write refusal, and zero legacy POST traffic.

## Checks run

- `node_modules/.bin/eslint tests/integration/runtimePrivate392Consumer.test.ts config/testing/vitest.runtime-restore.integration.config.ts --ext ts --max-warnings 0` — passed.
- `node_modules/.bin/tsc --noEmit --pretty false` — passed.
- `node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts` — 3 files / 30 tests passed.
- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d` — passed.
- `git diff --check` — passed.

The attempted `--configLoader=runner` form failed before test collection
because this repository config uses `__dirname`; no tests ran in that attempt.
The normal loader command above is the valid focused result.

## Later central command

Do not run locally. After the orchestrator supplies an exact Agent checkout
whose HEAD is `1303ce6be32e7bd96ed5c6b35afcb15819e81b50` and whose parent is
`e010e6a3868e963471244491bb6672c3e4a5135e`, with the exact Runtime checkout
at `/home/user/work/wt/rt-pin-f8da4b6d`, run centrally:

```sh
AGENT_CHECKOUT=/absolute/exact-agent-1303-checkout
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-f8da4b6d \
ASTRID_CHECKOUT="$AGENT_CHECKOUT" \
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
node_modules/.bin/vitest run --config config/testing/vitest.runtime-restore.integration.config.ts \
  --no-cache --maxWorkers=1 --no-file-parallelism \
  tests/integration/runtimePrivate392Consumer.test.ts
```

If the Runtime venv, production `dist/index.html`, or exact Agent checkout is
unavailable, the test fails with the named prerequisite rather than producing
a synthetic native pass. No live HTTP/Door/provider/browser/socket test was
run in this source-only worker, per task instructions. No public pin,
activation, or integration adoption was performed.
