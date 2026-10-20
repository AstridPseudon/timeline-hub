# AP2 M2 selected PARAM current shared-first packet

## Result

Delivered the selected-PARAM carrier as two patch packets against current App HOME
220b0f10328358049c15c580470d1a5771ad9bc8:

1. /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-reviewed-current-shared-first.patch
2. /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-reviewed-current-row-local.patch

No App source was changed in this worker worktree. The packets are the handoff for HOME;
they do not claim a browser or hosted journey.

## Exact source and donor basis

- Current HOME base: 220b0f10328358049c15c580470d1a5771ad9bc8
- Donor current-root selected tree: 92cb038f6c26b26bb0f628dcfecbfc490506281b
- Donor selected commits, in required semantic order:
  60bc95121, ff6a55c30, c0af4e411, f90c4e97b
- Donor selected-stack root: 8cfcee9c0403d113463c7859f6c835d3bfd79668

The packets were composed with a three-way merge of donor selected changes onto HOME.
This preserves HOME's newer ordinary, recovery, media, duplicate, and existing Provider
ports, especially in commitSession.ts and useTimelineCommandSession.ts. The only
normalization beyond donor behavior is removal of inherited trailing blank lines from
the two new selected-authority files.

## Required application order

Apply and check the shared packet first, then apply and check the row-local packet:

    git apply --check --recount /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-reviewed-current-shared-first.patch
    git apply --recount /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-reviewed-current-shared-first.patch
    git apply --check --recount /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-reviewed-current-row-local.patch
    git apply --recount /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-reviewed-current-row-local.patch

Both packets pass git apply --check --recount against the untouched HOME base.

## Source map

Shared-first packet, 12 files / 869 insertions and 5 deletions:

- Runtime retained-read adapter: src/integrations/runtime/client.ts,
  src/integrations/runtime/dataProvider.ts, and
  src/integrations/runtime/retainedParamInputs.ts.
- Fail-closed selected authority and tests:
  src/tools/video-editor/commands/selectedParamAuthority.ts and
  selectedParamAuthority.test.ts.
- Native session/save wiring:
  src/tools/video-editor/commands/commitSession.ts,
  src/tools/video-editor/data/DataProvider.ts,
  src/tools/video-editor/hooks/useTimelineCommandSession.ts,
  useTimelineSave.ts.
- Mounted shared port exposure:
  src/tools/video-editor/hooks/useTimelineState.ts,
  useTimelineState.types.ts, and
  src/tools/video-editor/contexts/VideoEditorProvider.tsx.

Row-local packet, 11 files / 515 insertions and 17 deletions:

- Native row helpers and tests:
  clipParamsCapture.test.ts, clipParamsCapture.ts, clipParamsGesture.ts,
  selectedParamPort.test.ts, and selectedParamPort.ts.
- PropertiesPanel route and tests:
  AstridElementParams.mounted.test.tsx, AstridElementParams.test.tsx,
  AstridElementParams.tsx, ClipPanelBody.tsx, PropertiesPanel.test.tsx,
  and PropertiesPanel.tsx.

The packet carries the existing clip.set-params operation and exact Agent-produced
DocumentPin as schema_source. It adds no operation, DTO, endpoint, catalog revision,
latest lookup, alias, browser hash, synthetic P1, or fallback snapshot.

## Verification

- Packet application check: both packets passed git apply --check --recount.
- Private composed overlay, normal Vitest loader, no cache:
  ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism [11 selected and neighbor test files]
  — 11 files, 311 tests passed.
- Current worker worktree remains clean; no product source or build output was left.
- A preliminary overlay launch with --configLoader=runner failed because this repo config
  uses __dirname; the normal project loader passed. This is not counted as product
  test evidence.
- Not run: full suite, browser/e2e, localhost/live sockets, Runtime/Agent qualification,
  or dependency installation.

