# App private392 approved native-environment HTTP result

## Verdict

**UNQUALIFIED / BLOCKED at the first App `RuntimeDataProvider` Door read.**
The already-requested central run entered the real test, but did not reach the
App capture/command-session commit journey. The required PASS criterion—full
authentic App capture, session, outbox, `RuntimeDataProvider`, and Runtime Door
execution—is therefore not met.

This is an environment/connector failure, not evidence for changing the
driver or bypassing the Door. I did not retry or request another run.

## Exact central result

Existing request owned and interpreted:

```text
ap2-m2-private392-existing-native-env-http-proof-v2-ap2-m2-private392-approved-native-env-app-http-integration-1020234027-27797
```

The only wait command used was:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  ap2-m2-private392-existing-native-env-http-proof-v2-ap2-m2-private392-approved-native-env-app-http-integration-1020234027-27797 1
```

It returned immediately with exit `1` (the result was already terminal): one
Vitest file and one test failed in 6.24 seconds. The central command was:

```text
env -u PYTHONPATH -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST \
  ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-1303ce6b \
  ASTRID_PYTHON=/home/user/work/venv-app2-native/bin/python \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-f8da4b6d \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-app2-native/bin/python \
  npm run test:integration:private392-http
```

The runner's lock, exact checkout/interpreter/import, schema/manifest/bundle,
and reviewed-driver guards passed far enough for Vitest to collect and start
the test. The test also passed its identity assertions, started the
`DirectHarness`, created the project, seeded the composition revision, enabled
timeline authoring, and validated Runtime health before the failure.

## Sanitized failure and HTTP evidence

The first command-basis load at
`tests/integration/runtimePrivate392Consumer.test.ts:228` failed while
`RuntimeDataProvider.loadTimelineCommandBasis` opened its Runtime session:

```text
RuntimeUnavailableError: Workspace Runtime is unavailable at
http://127.0.0.1:17340/api/runtime: http_error: HTTP 403
```

The relevant stack was `AstridRuntimeClient.openSession` (client.ts:503),
`withSession` (client.ts:510), `RuntimeDataProvider.loadTimelineCommandBasis`
(dataProvider.ts:804), and the test at line 228. No authorization token,
credential, cookie, request body, or response body was retained. The test
service log and summary retain only this sanitized status/URL evidence.

The runner's temporary harness root was cleaned by its EXIT trap. No secrets
were copied before cleanup; the durable evidence is the sanitized central
summary/log and this report.

## Assertion classification

The reviewed source still contains all requested assertions, but the failure
occurs before any of them can execute:

| Check | Result |
| --- | --- |
| merge/replace lowering | not executed |
| opaque values and ordered data | not executed |
| lost acknowledgement | not executed |
| App reload/recovery | not executed |
| exact idempotency retry | not executed |
| disjoint rebase | not executed |
| guarded undo | not executed |
| stale same-leaf zero-write refusal | not executed |
| zero legacy POST traffic | not executed |

An outbox object was allocated before the failed basis load, but no App command
session was created, no patch was captured or submitted, and no commit request
was sent. The only Runtime interaction after harness setup that reached the
App provider failed at session opening with HTTP 403.

## Source and scope evidence

- Central App snapshot tree: `92c86fc8d6ea8435379044d9b42ce516fd461dea`.
- Reviewed driver SHA-256:
  `85a6f1b2caa7929fb4f6d29855529b6ff837a4ad293b85dd187d080e74d7b981`.
- Runner source SHA-256:
  `50afc7638cd56d33dfc5eeeaf60c46f112ed81d08bcf23c4c69b3f94ef6cfd8e`.
- App lock SHA-256:
  `3ee0aa69fbff9faeff76a44aedc4e7fb70a69970ceec25c0fde788dbdb37d873`.
- Exact producer tuple reached the test: Agent `1303ce6b`, Runtime `f8da4b6d`;
  the test's reviewed schema and manifest guards remained in force.

No source code, suite registration, dependency, lock, shared environment,
hosted UI, public adoption claim, full suite, local socket, or browser run was
made by this worker.

## Next step

The manager should diagnose the concrete HTTP 403 from the supported native
Runtime Door/connector for this already-qualified caller environment. Once
that external state is corrected, the existing named request may be reviewed
by the orchestrator for a single permitted rerun; this worker did not request
one.
