# PRIVATE392 App HTTP-only runner source

## Result

Prepared the smallest App-owned source setup for the reviewed unmocked private392
Door consumer:

- Added the exact reviewed driver at
  `tests/integration/runtimePrivate392Consumer.test.ts` (source SHA-256
  `85a6f1b2caa7929fb4f6d29855529b6ff837a4ad293b85dd187d080e74d7b981`).
- Registered it in the existing integration Vitest config.
- Added
  `scripts/testing/private392-http-runner.sh`.

The wrapper uses the existing `DirectHarness`, transport, client/provider,
session, outbox, and credential path. It does not add a harness, transport,
client, generator, endpoint, or public pin. It removes only the unnecessary
`npm run build:hosted` prerequisite for this non-mounted test: after all
identity/provenance checks pass, it creates a disposable one-file
`ASTRID_APP_DIRECT_DIST` root because the existing DirectHarness static HTTPS
listener requires `dist/index.html`. The test never mounts or reads that
page.

The wrapper must replace the current central named-suite command's
`npm run build:hosted &&` prefix. The central suite registry is outside this
App worktree and was not edited.

## Dependency fact

The test has no hosted-UI module or browser-page dependency. It does have the
existing DirectHarness listener prerequisite: `harnessUnavailableReason()`
requires an `index.html`, and `DirectHarness.start()` starts the hosted-style
HTTPS listener before Runtime/Door use. A blank disposable index satisfies only
that listener contract; it is not a hosted App build.

## Guard map

| Guard | Before | After |
| --- | --- | --- |
| Agent identity | Driver checked HEAD `1303ce6b`, parent `e010e6a3`, schema392 digest. | Wrapper repeats HEAD/parent/tree, clean checkout, and schema digest checks. |
| Runtime identity | Driver checked f8da commit through test-time assertions. | Wrapper requires f8da HEAD/tree, clean checkout, exact Runtime lock check, 75 artifact entries and hashes, manifest version/file digest, bundle digest, component-manifest digest, Runtime schema metadata, and Agent/Runtime schema byte identity. |
| App generated contract | Driver checked `runtime.lock.json` source/artifact fields and App schema digest at test time. | Wrapper invokes the existing producer-backed `vendor-lock.mjs check`; mismatch is fatal before temp dist or Vitest. |
| Source custody | No wrapper preflight. | Driver hash is pinned; Agent/Runtime checkouts must be clean; all Runtime artifact bytes are checked against the committed manifest. |
| Credentials | DirectHarness provisions product credentials through Runtime and uses its authenticated Door. | Same existing path; wrapper only requires the exact Python executables. |
| Hosted build | Central suite always ran `npm run build:hosted`, failing on Composition `clipOpacity` before collection. | Wrapper never calls a build; it creates only a disposable blank `index.html` after guards. |
| Test scope | Prior selector was one named test file but build ran first. | Exact Vitest selector is the one private392 test file with one collected case. |
| Gate assertions | Reviewed driver retains merge/replace, original guards, opaque null/false/order, lost ACK/reload/exact retry, disjoint rebase, guarded undo, stale refusal, and zero legacy POST assertions. | Driver is copied unchanged; no positive behavior was removed or weakened. |

## Checks run

- `sh -n scripts/testing/private392-http-runner.sh` — PASS.
- Inline Node guard parse with `node --input-type=module --check` — PASS.
- `node_modules/.bin/eslint tests/integration/runtimePrivate392Consumer.test.ts config/testing/vitest.runtime-restore.integration.config.ts --ext ts --max-warnings 0` — PASS.
- `node_modules/.bin/vitest list --config config/testing/vitest.runtime-restore.integration.config.ts --no-cache tests/integration/runtimePrivate392Consumer.test.ts` — PASS; exactly one test collected.
- `node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts` — PASS; 3 files / 30 tests.
- `node_modules/.bin/tsc --noEmit --pretty false` — PASS.
- `git diff --check` — PASS.
- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d` — EXPECTED FAIL before live execution: current App lock still pins public Runtime `2c4ac180...`, while the exact private392 producer is `f8da4b6d...`. This mismatch is intentionally not ignored or relabeled.

No network, localhost/Runtime process, Door request, browser, hosted build,
full suite, or `request-test` run was made. The shared Agent/Runtime venv paths
specified by the existing central suite are absent in this sandbox, so the
runner was not live-executed.

## Handoff/blocker

Before the central HTTP proof, the orchestrator must provide the reviewed
private App generated counterpart/lock (f8da, artifact52df, schema242) without
changing the public pin, and independently review process custody. Then update
the existing named-suite command to invoke:

```text
env ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-1303ce6b ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-f8da4b6d ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python sh scripts/testing/private392-http-runner.sh "$PWD"
```

The runner will fail closed if any exact guard remains unavailable.

