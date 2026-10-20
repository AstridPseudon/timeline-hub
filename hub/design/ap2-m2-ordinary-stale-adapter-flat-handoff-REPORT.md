# AP2-M2 ordinary stale-adapter flat handoff

## Result

Created a remotely consumable, flat App handoff with no product edits:

- `design/handoff-ap2-m2-ordinary-stale-adapter-peer-fix.patch`
- `design/handoff-ap2-m2-ordinary-stale-adapter-production.patch`
- `design/handoff-ap2-m2-ordinary-stale-adapter-regression.patch`
- `design/handoff-ap2-m2-ordinary-stale-adapter-owner-request.md`

The peer-fix file is byte-identical to
`workers/ap2-m2-ordinary-zero-post-causal-diagnosis/peer-fix.patch` and has
SHA-256
`97fb1c46827199b89f68e81cd912d72f3a6cce9bbe19fcf85d6a3a7bbc743149`.
The production and regression files are likewise byte-identical to the
diagnosis worker's split files.

## Applicability and source

- Current HOME base: `a11dd7a91af76a690f771ee06d9df960db323751`
  (`hub/tl/integration`).
- Diagnosis candidate source: `17655a570f92229635092013f28d2c5025f31ef0`.
- `git apply --check` passed for peer-fix, production, and regression patches
  against current HOME; no Git state was mutated.
- Changed production paths are exactly
  `src/tools/video-editor/hooks/useTimelineOps.ts` and
  `src/tools/video-editor/hooks/useTimelineOps.test.ts`.

The proven first causal defect is the App-owned retained `TimelineOps` adapter:
its activation-time `apply` callback captured no generic command port, so the
real action used legacy whole-document publication. Runtime correctly returned
`409 timeline_commit_required`; there were zero ordinary `/commit` POSTs and
the outbox had no pending command. The patch preserves one adapter identity and
dispatches all seven operations through current callbacks, including current
command-port and authority state. Capture refusal still propagates; no fallback
or guard was weakened. App owns this shared core, so the worker did not edit or
compete with it.

## Evidence

The diagnosis worker's private patched-copy validation passed:

```text
npm exec vitest run --no-cache --configLoader=runner \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/ordinaryMoveMember.test.ts \
  src/tools/video-editor/commands/ordinaryScalarMember.test.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts
=> 5 files, 114 tests passed

npm exec eslint -- --max-warnings 0 \
  src/tools/video-editor/hooks/useTimelineOps.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts
=> exit 0
```

The two added regressions were RED on old source (43 passed / 2 failed in the
45-test file) and GREEN after the production patch. This worker additionally
verified byte equality, the peer-fix SHA, and `git apply --check` on all three
patch forms. No full suite, browser/socket gate, dependency install, pin/API
change, or private App copy was run here.

## Owner sequence and unresolved prediction

The owner request gives the exact apply order (production, then regression;
combined peer-fix is an alternative), targeted commands, and the central
`e2e-m2-ordinary-integration` command to run only after the owner harness
commits the source.

The next fixture concern is explicitly a prediction, not an observed native
failure: `moveExistingShotsToMarkers` selects **all five visual clips** (two
parents plus three occurrence-child display clips), while the journey expects
only two parents. Do not filter producer scope or weaken assertions. The first
child's 12-second-to-6-second move may also meet an occurrence boundary; follow
the first restored native result before changing anything.

## Blocked / next step

No owner source commit or post-fix central qualification exists in this worker.
The App shared-core owner should apply and commit the handoff, report the exact
source hash/tree, then run the named central gate once. PLAN2/3/6 ordinary
critical-path qualification remains pending that gate.
