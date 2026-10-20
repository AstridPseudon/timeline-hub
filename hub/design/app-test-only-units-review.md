# App test-only units review

Review base: `tl/integration` at `1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff`.
The two candidate branches are independent test-only changes. A two-dot diff
against the current integration tree shows no overlap with existing content:

| Unit | Source SHA | Current-tree diff | Finding |
| --- | --- | --- | --- |
| ACP proposal baseline fixture | `f0e4917ba27005a6022b4b0103ebf2e5c9447adb` | 2 added lines in one test | **APPROVE content; HOLD merge** |
| Automatic-placement legacy positives | `ad329e82f26ae777c2d24ec293d780049cae4c75` | 45 added lines in one test file | **APPROVE content; HOLD merge** |

Both holds are procedural: the exact then-current full App snapshot must be
launched and completed before either unit is merged. The manager owns merge
order. These branches must remain separate; this review does not combine or
apply either branch.

## 1. ACP proposal baseline fixture — APPROVE

The candidate changes only the `/events` arm of
`src/tools/video-editor/hooks/useAgentSession.proposal-vertical.test.tsx` to
return:

```json
{"notifications": [], "disconnected": false}
```

This matches the closed ACP response contract in
`src/integrations/astrid/acpRoutes.ts:23-26`, which is the schema used by
`events()` at lines 229-235. The old fixture's catch-all
`{"error":"session_not_owned",...}` was returned with HTTP 200 for `/events`,
so the strict success parser correctly raised `bridge_contract_violation`
before `/chat/prompt` was reached. The fixture fix therefore removes a
test-owned malformed transport response; it does not hide a provider
regression.

The original test name, input (`apply proposal`), prompt request assertion,
expected 403 error code (`session_not_owned`), and `proposalApply` negative
assertion are unchanged. The prompt remains the only route receiving HTTP
403 in the mock. No product code, parser/order, edge proposal import, skip, or
expected-failure marker changed.

Acceptance evidence from the candidate source SHA:

```sh
/tmp/app-m2-coherent-deps8/node_modules/.bin/vitest run \
  --config config/testing/vitest.config.ts \
  src/tools/video-editor/hooks/useAgentSession.proposal-vertical.test.tsx
# PASS: 1 file, 1 test

/tmp/app-m2-coherent-deps8/node_modules/.bin/vitest run \
  --config config/testing/vitest.config.ts \
  src/tools/video-editor/hooks/useAgentSession.proposal-vertical.test.tsx \
  src/tools/video-editor/hooks/useAgentSession.test.tsx \
  src/tools/video-editor/hooks/useAgentSession.projectContext.test.tsx
# PASS: 3 files, 62 tests

git diff --check
# PASS
```

The untouched baseline was intentionally run first and failed with
`bridge_contract_violation` instead of `session_not_owned`; this is the
expected RED-to-GREEN diagnosis. No full suite, build, browser/e2e, TypeScript
check, or install was run.

## 2. Automatic-placement legacy positives — APPROVE

The candidate adds four ordinary positive tests at
`src/shared/lib/placement/__tests__/documentPlacement.test.ts:102-145` and
leaves all prior tests and inputs unchanged. Each assertion matches the
retained implementation and the prior placement source audit:

1. Auto append reads only the selected shot's latest clip extent. A clip in a
   sibling shot on the same lane does not move the target shot's append point.
   This follows `latestOccupiedFrame()`'s shot-group lookup at
   `documentPlacement.ts:204-215`.
2. A new shot inherits the first existing pinned group's lane and does not
   create a track. This is the current `ensureShotGroup()` behavior at
   `documentPlacement.ts:69-79`.
3. Shared placement retains a four-second clip hold even when the registry
   records a longer video duration. The implementation uses
   `DEFAULT_CLIP_HOLD = 4` when constructing the clip at
   `documentPlacement.ts:250-258`, while preserving the registry duration.
   This is deliberately distinct from the historical completion insertion
   path, whose completion video/image insertion used a five-second window.
4. Explicit collision shifting checks occupied start frames only, not occupied
   intervals. That is the behavior of `occupiedFrames()` and
   `nextFreeFrame()` at `documentPlacement.ts:185-201`.

These are compatibility tests for the old visible shared-placement behavior,
not a native automatic-placement contract. They do not restore the removed
completion trigger, infer canonical ownership from display IDs, add a command
operation, or authorize a snapshot-writer retirement. The plan's canonical
shot-ownership policy remains the future domain-owner guard; pinned groups are
still migration-only there. The four tests preserve the legacy behavior until
the owner-approved native policy and its guards replace it.

Acceptance evidence from the candidate source SHA:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts \
  src/shared/lib/placement/__tests__/documentPlacement.test.ts \
  src/shared/lib/placement/__tests__/placementService.test.ts \
  src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts \
  src/shared/hooks/shots/__tests__/addImageToShotHelpers.test.ts \
  src/shared/hooks/shots/__tests__/useShotGenerationMutations.test.ts \
  src/tools/video-editor/commands/clipMoveCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts
# PASS: 8 files, 183 tests

./node_modules/.bin/eslint \
  src/shared/lib/placement/__tests__/documentPlacement.test.ts
# PASS

git diff --check
# PASS
```

The separate outside-repository native RED patch remains RED at the
zero-snapshot assertion; its positive behavior/readback assertions pass. It
must not be converted into a passing test by refusing the legacy behavior or
by fabricating a native sender. No full suite, build, browser/e2e, TypeScript
check, install, Agent/Runtime execution, or live socket qualification was run.

## Merge gate

After the manager has the exact then-current integration snapshot, launch the
central full App suite once and wait for completion. Merge each candidate as
its own unit only after that snapshot's result is available; this worker did
not request the full suite under the task's restriction. Current product
source in this review worktree is untouched.
