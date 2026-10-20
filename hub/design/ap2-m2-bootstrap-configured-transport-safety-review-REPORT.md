# AP2-M2 configured-provider bootstrap transport safety review

## Verdict

**APPROVE — bounded private configured-provider bootstrap candidate.** This is
approval of the three-file App source diff only. It is not public package
activation, browser/native bootstrap activation, or paired Agent/Runtime
qualification.

## Scope and source identity

- Repository: App worktree, `tl/ap2-m2-bootstrap-configured-transport-safety-review`.
- Candidate: `449ae7c00067169f1f6c4db727ac4b0fa702e0e2`.
- Comparison base: `db10eac8e`.
- Changed paths: `src/integrations/runtime/dataProvider.ts`,
  `src/integrations/runtime/createDefaultTimeline.ts`, and
  `src/integrations/runtime/createDefaultTimeline.test.ts` only.
- Candidate working-diff SHA-256: `753076141ade30c7d91f76cd670a6a0ee6742048669bbfd10cce23bd42016ea0`.

## Findings

No blocking findings.

`RuntimeDataProvider` now accepts the already configured `AstridRuntimeClient`
and `createDefaultTimeline` passes its client into that provider. The adapter's
create, history, immutable composition-revision read, and commit ports all call
that same `this.client` (or the provider method that calls it). There is no new
client, global-fetch fallback, endpoint, DTO, store, or second persistence
authority in the changed source.

The unchanged bootstrap owner remains the durable `createCommitOutbox`: it
reserves the exact timeline ID and create request before network I/O, discovers
and recovers the same owner after restart, retains uncertain create/init work,
and verifies the original initialization request and returned receipt before
completion. The unchanged `ensureProjectHasTimeline` headed-timeline guard
does not reapply defaults; the existing headless repair path remains bounded to
the reserved identity. Existing opaque-field/pristine protections remain in
the bootstrap and timeline tests.

The fresh-create regression fixture removes `globalThis.fetch`, so a separately
constructed client cannot make the test pass. The headless repair and recovery
coverage remains present and continues to exercise the configured transport
sequence.

## Evidence

Reran the decisive focused command in this worktree:

```sh
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/bootstrapInitialization.test.ts \
  src/tools/video-editor/commands/bootstrapCapture.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/integrations/runtime/createDefaultTimeline.test.ts \
  src/integrations/runtime/client.test.ts \
  src/integrations/runtime/clientSharedSession.test.ts
```

Result: **6 files passed, 158 tests passed** (8.07s).

Also checked `git diff --check`: **PASS**. The candidate report's additional
evidence, not rerun for this read-only review, is `npm run
typecheck:strict-probe` PASS and the focused ESLint command PASS.

No full, browser, localhost/live-socket, Runtime-door, public-package, or
activation run was performed.

## Smallest real provider qualification

After the manager-owned allow-list registration, run the exact paired suite:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:app bootstrap-fixed-pair-native-integration)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Its prepared exact-source harness is expected to report 47 passed across the
Agent real-provider tests and Runtime scope/repair neighbors. That qualification
is still pending and is the next gate before any activation decision.
