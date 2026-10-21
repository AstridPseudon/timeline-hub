# AP2-M2 bootstrap two-entry history triage

## Result

No App product, test, activation, pin, or dependency change was made. The
private gate `14046` is correctly **not qualified**. Its two entries are both
live records for the newly created project/timeline; the first is not fixture
setup and the test must not filter it out:

1. `parent_composition.publish`, `intent: bootstrap`, `previous: null`,
   idempotency key `bootstrap:<timeline_id>`.
2. `timeline.commit`, `intent: recorded`, `previous: <the first entry>`,
   publisher `astrid-e2e-product`, containing the three native commands
   `timeline.init`, `track.create`, `track.create`.

The retained failure's first entry has the newly created project ID and
timeline ID, event `4`, and a `bootstrap:` key. The second has the same scope,
event `5`, and the native commit key. This is not the seeded `seed3` history.

## Exact producer chain

The qualified App source is the `f487c0ca9` bootstrap port (central log source
tuple: App `aeb3ec52020e245ad7875fa89e851a6060070e7d`, Agent
`3c4f6de4fa777323b3386c01c7266b619b86af6d`, Runtime
`202074110717146fc7f08af2306a8dd7f695b0b1`, producer artifact source
`a0dca16975dfe8f5e762703b99d9791a16cf7fd7`). Its live callers are:

- `ensureProjectHasTimeline` (`src/tools/video-editor/pages/VideoEditorPage.tsx:461`,
  and `src/shared/hooks/projects/useProjectCRUD.ts:154`) calls
  `initializeTimeline` for the first project timeline.
- `createCanonicalTimeline` (`src/tools/video-editor/pages/VideoEditorPage.tsx:551`)
  calls the same initializer for an additional timeline.
- `initializeTimeline` calls the live export
  `RuntimeDataProvider.initializeNativeBootstrapTimeline`
  (`src/integrations/runtime/dataProvider.ts:498`), which is the only live
  caller of `initializeBootstrapTimeline`.
- `initializeBootstrapTimeline` calls `resumeBootstrapInitialization`, which
  first dispatches the existing create request and then dispatches the native
  `/v1/.../commit` request. No second App history writer exists.

The normal Runtime create producer is the pinned Runtime source at
`runtime_protocol/service.py:1673-1717` in `202074110717`. After creating the
timeline row and its legacy shell projection, `create_timeline()` calls the
existing `TimelineCommitStore.bootstrap()` at line 1709. The bootstrap method
at `runtime_protocol/timeline_commit_store.py:989-1026` installs the empty
canonical parent, appends `parent.composition.published`, and records the
`parent_composition.publish` receipt. It is therefore a real accepted history
edge, not a read-side or test-only artifact.

The second producer is the same App initializer's existing
`commitTimeline` port (`dataProvider.ts:513`) sending the captured native
commands. Runtime accepts it through its ordinary commit provider and records
the `timeline.commit` edge. This matches the failure chronology exactly.

## Fixture/setup distinction

The harness's seeded setup writes are outside the failing scope:

- `tests/e2e/local/support/harness.ts:759` seeds the harness timeline through
  the legacy composition-revision route.
- `seedExtensions`, `seedMedia`, and `seedThreeProducts` similarly publish
  other seeded timelines (`harness.ts:836`, `871`, `973`).
- The failing test creates a new project and reserved timeline, then derives
  `expectedScope` from the create response and selected UI timeline
  (`tests/e2e/local/three-products.spec.ts:1373-1496`). The returned history
  entries carry that new project/timeline scope, so seeded setup cannot account
  for either entry.

The source-only App contract tests model the same chronology: their synthetic
history starts at H0 with a `parent_composition.publish` entry, then appends
the `timeline.commit` entry after native initialization. The unchanged local
tests therefore do not support classifying the second entry as an accidental
fixture record.

## Smallest correction boundary

There is no safe App-only correction that preserves all of the requested
properties simultaneously. Removing the init commit would lose the required
native `timeline.init` record; filtering the bootstrap row would weaken the
history assertion; and adding a speculative history writer would violate the
one-path/one-history contract. The current Runtime create response also
returns the bootstrap head/publication that App uses as the immutable H0 base,
so simply suppressing the row would make the existing commit contract
incoherent.

The smallest valid correction is a coordinated Runtime/Agent contract change
to make native initialization atomic at the existing create/commit boundary:
the create operation must allocate the empty shell without publishing a
separate accepted parent edge, and the first ordinary `/commit` carrying
`timeline.init` must install the empty baseline and record the one
`timeline.commit` history entry atomically. That requires preserving the
existing request identity, raw commands/order, H0/absence guards, retry,
reload/restart, inverse, and zero-legacy behavior; it must not add a DTO,
endpoint, fallback writer, or history filter. The current Runtime contract
does not expose that behavior, so this is a Runtime/Agent design request, not
an App patch to land here.

Minimal peer request recommendation: ask HOME to keep the 013 rollback and
unknown-operation guard untouched and ask Agent/Runtime owners to confirm
whether an existing contract seam can absorb the baseline publication into
the first native commit. Until they provide an executable source/test change,
do not activate the newer bootstrap path or repeat the browser gate. If they
cannot provide that seam without changing the existing wire/base contract,
the orchestrator must explicitly resolve the contradiction; this worker does
not weaken the one-entry expectation.

## Verification

- Retained central result
  `ap2-m2-bootstrap-approved-bridge-real-gate-ap2-m2-bootstrap-observed-request-match-fix-1021001554-14046`:
  one browser test failed in 86s with expected history length 1 and received 2;
  no repeat was run.
- `NODE_OPTIONS='--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs' node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/createDefaultTimeline.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.test.ts` — **PASS**, 4 files / 128 tests.
- No browser, localhost/socket, central rerun, full suite, activation, or
  pin/adoption was performed.

Changed exports: none. Changed files: none in the App worktree. The only
artifact from this worker is this factual triage report.
