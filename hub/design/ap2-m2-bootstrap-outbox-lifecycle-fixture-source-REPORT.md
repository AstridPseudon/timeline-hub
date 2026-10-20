# Bootstrap outbox lifecycle fixture source

## Result

Corrected the bootstrap outbox wait without changing product, shared API, store, schema, or pin code.

- Added a Playwright support fixture that holds the real `/v1/projects/{project}/timelines` create request.
- The Gate 5 bootstrap journey now derives project/timeline scope from that real request, observes the reserved owner while create is pending, releases create, observes the same owner while `timeline-init` is pending, then releases the acknowledgement.
- The post-init assertion accepts the valid drained state (or retained owner with no pending/intents) instead of requiring a completed owner to remain.
- Added a pure bootstrap owner/scope lifecycle regression covering deterministic pending create, pending init, exact scope/identity, and drain after ACK.

The source evidence showed the owner uses the normal `astrid.command-outbox` `owners` store and exact `[realmId, actorId, projectId, timelineId, ownerId]` key. The prior browser wait ran after initialization could already have drained the owner, so it was observing an invalid lifecycle phase rather than a different schema or arbitrary mapping.

## Verification

- `./node_modules/.bin/vitest list --config config/testing/vitest.config.ts --configLoader=bundle src/integrations/runtime/bootstrapInitialization.test.ts` — passed; 65 tests collected.
- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --configLoader=bundle --no-cache src/integrations/runtime/bootstrapInitialization.test.ts` — passed; 65/65.
- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — passed; 1/1.
- `./node_modules/.bin/eslint src/integrations/runtime/bootstrapInitialization.test.ts tests/e2e/local/support/app.ts tests/e2e/local/three-products.spec.ts --ext ts --report-unused-disable-directives --max-warnings 0` — passed.
- `./node_modules/.bin/tsc -p tsconfig.node.json --noEmit --pretty false` — passed.
- `git diff --check` — passed.

No request-test, browser, socket, or full suite was run, as required. The central bootstrap-only gate remains for the orchestrator to run after this source candidate is committed.

## Handoff

No blockers. The harness should commit the worktree using the supplied commit message.
