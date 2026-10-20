# AP2-M2 real configured-provider bootstrap gate

## Result

Prepared the smallest current App candidate on top of `449ae7c00067169f1f6c4db727ac4b0fa702e0e2`.
The approved three-file production candidate remains unchanged; this worker adds
one real mounted consumer journey and its one import:

- `tests/e2e/local/three-products.spec.ts`

The journey uses the production New Project flow and the configured App client.
It asserts Runtime `/v1` timeline creation, native `timeline.init` plus the two
`track.create` commands, the sole native bootstrap history entry, no legacy
`composition-revisions` publisher traffic, a post-bootstrap edit, lost ACK,
reload, Runtime restart, exact persisted retry, and guarded `timeline.inverse`
undo. It deliberately uses the existing harness, outbox inspection, Runtime
restart, and token-safety helpers; no route, DTO, store, provider fallback, or
public pin was added.

## Exact private dependency tuple

- Agent: `3c4f6de4fa777323b3386c01c7266b619b86af6d`, tree
  `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`
- Runtime: `202074110717146fc7f08af2306a8dd7f695b0b1`, tree
  `ee39286bd0eb27d4075074cc4785d6d15e33f243`
- Runtime immutable producer: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`
- Runtime artifact: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`
- Shared schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

The App public013 lock and generated files remain unchanged. The current
working-tree diff from candidate `449ae7c00067169f1f6c4db727ac4b0fa702e0e2`
is 106 additions / 1 deletion in the e2e spec, with SHA-256
`76b26d46baa8cf1dda9ece0e3a5c9865fb6e72199ba663d7f04586475224fa8c`.

## Checks run

```text
node --require <existing private vitest runner> node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/createDefaultTimeline.test.ts \
  src/integrations/runtime/bootstrapInitialization.test.ts \
  src/tools/video-editor/commands/bootstrapCapture.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/integrations/runtime/client.test.ts \
  src/integrations/runtime/clientSharedSession.test.ts
```

**PASS — 6 files, 158 tests.** This includes the configured
`AstridRuntimeClient -> RuntimeDataProvider -> createDefaultTimeline -> durable
bootstrap owner` direct native fixture, fresh creation, bounded headless
repair, exact reserved IDs, opaque/pristine guards, and exact lost-response
replay. The fixture rejects legacy bootstrap publishing.

```text
node node_modules/eslint/bin/eslint.js --no-cache --max-warnings=0 \
  tests/e2e/local/three-products.spec.ts
```

**PASS.**

```text
npx playwright test --config playwright.three-products.config.ts \
  --list tests/e2e/local/three-products.spec.ts
```

**PASS — 10 tests collected**, including the new bootstrap journey at line
1141. `git diff --check` also passed.

## Central qualification boundary

The live central browser/Runtime journey was not submitted from this worker:
the candidate is necessarily dirty until the harness commits it on worker exit,
and the task explicitly forbids a dirty-tree request. Therefore no App
consumer qualification, private Agent/Runtime live result, or cutover claim is
made here.

After the harness commits this exact candidate, submit the existing private
normal014 suite once (its selector now includes the new test title):

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-bootstrap-real-configured-provider-gate \
  normal014-integration-e2e-gate5) && \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

That existing runner supplies the exact 3c4f/202+a0/f021/6ba private tuple,
private App dependency graph and caches, and runs the established Gate 5 plus
this bootstrap test through the real Runtime/browser harness. Do not submit
the request before the harness commit, do not substitute public013 sources,
and do not request a full suite.

## Decision and next step

No new design decision was made. The production adapter remains the approved
`449ae7c0` candidate, and public013 remains untouched. The only source addition
is the missing positive App-consumer proof. The next decision is whether the
central result is positive; only then should the orchestrator consider the
smallest cut candidate for adoption and any legacy-writer ledger update.
