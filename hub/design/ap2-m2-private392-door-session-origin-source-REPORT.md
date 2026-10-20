# App private392 Door session-origin source fix

## Result

Fixed the first App Door session `403` in the private392 driver by removing
the product token from both `RuntimeDataProvider` instances that use the
existing `DirectHarness` Door transport. The Door-bound client now uses the
supported browser connector seam: `doorTransport` sends the hosted Origin
through `DirectHarness.doorRequest`, and the Door applies the product
credential from its configured credential file. The direct Runtime remote
provider still receives its explicit actor token and was not changed.

This is source-only. No Runtime product code, public DTO, provider, client,
transport, harness, assertion, fixture, lock, or dependency was added or
changed. The private392 scenario assertions remain byte-for-byte unchanged.

## Diagnosis and existing source-proof map

- The failed central run reached
  `RuntimeDataProvider.loadTimelineCommandBasis` and
  `AstridRuntimeClient.openSession` at the Door base
  `http://127.0.0.1:17340/api/runtime`, then received HTTP 403 before capture.
- `DirectHarness.doorBase` is the existing `/api/runtime` Door base at
  `tests/e2e/local/support/harness.ts:379-381`.
- `DirectHarness.startRuntime` starts the supported Door with the hosted
  origin, fixed Door port, and product credential file at
  `tests/e2e/local/support/harness.ts:453-461`.
- `DirectHarness.doorRequest` injects the hosted `Origin` and does not add a
  browser credential at `tests/e2e/local/support/harness.ts:792-798`.
- The passing normal integration connector uses the same Door base and
  transport without a provider token in
  `tests/integration/runtimeRestore.test.ts:55-62`.
- The existing Door controls prove the refusal boundary offline in
  `tests/e2e/local/direct-journey.spec.ts:789-817`: an `Authorization` header
  is refused as `browser_credentials_forbidden`; foreign or absent Origin is
  refused; the supported hosted Origin is accepted. No guard was bypassed.
- The client source documents the same contract: browser credentials come from
  the authenticated connector/proxy, while a token is for direct test/CLI
  clients (`src/integrations/runtime/client.ts:39-42,274-276`).

The runner's driver identity guard was updated from the old reviewed driver
digest to the truthful digest of this two-line connector-only change:

```text
54aa8bf25dee747499ccc3a3f15ebc1c61e95e6cb90c9ab72077d827ae67bd3a
```

The exact Agent `1303ce6b` source/schema, Runtime `f8da4b6d` source,
private App lock, 13 lock entries, and 75-artifact custody guards remain in
place and unchanged.

## Offline evidence

All commands ran in the assigned App worktree and passed:

```text
git diff --check
sh -n scripts/testing/private392-http-runner.sh
node --check scripts/testing/private392-http-runner.test.mjs
node --test scripts/testing/private392-http-runner.test.mjs
  PASS (1 test)
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d
  PASS (matches pinned producer commit)
node_modules/.bin/eslint tests/integration/runtimePrivate392Consumer.test.ts --ext ts --max-warnings 0
  PASS
node_modules/.bin/tsc --noEmit --pretty false
  PASS
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts
  PASS (3 files, 30 tests)
```

## Not run / next step

The private392 live selector was not run here: it starts the DirectHarness and
uses localhost/socket HTTP. Per the task boundary, browser/socket,
request-test, full-suite, and central rerun evidence remain unverified until
an independent connector custody review approves the corrected source.

No credential or token value was recorded.
