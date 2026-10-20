# App MAIN bebadd0e1 refresh — independent coverage review

## Verdict

**APPROVE** `9699410592a517909cbf9864d7c0094df5717b56` for the refresh worker's
scope. This approval is for the committed tree only, before later integration
work.

## Commit and scope verification

- Resolved commit: `9699410592a517909cbf9864d7c0094df5717b56`
- Resolved tree: `487798dccc88589bc77b059d32696719b35a6bf7`
- Parent 1: `0d5009e18bee8e29f894dabf5db501a0fcea750f` (the Timeline integration base)
- Parent 2: `bebadd0e1283753e3805c2d61688e3dee8b929e2` (`origin/main` / `bebadd0e1`)
- `git show -s --format=fuller` reports `Merge: 0d5009e18 bebadd0e1`; both
  parents are ancestors of the committed tree.
- The refresh patch is exactly the 174-path `574e97f4..bebadd0e1` upstream
  delta; the committed first-parent diff also has 174 paths.
- `git diff --check 0d5009e18 969941059` passed.

## Resolution and infrastructure audit

The resolved tree differs from incoming MAIN in only seven paths. Each
difference is scoped and explained by the source worker's resolution:

- `config/vite/vite.config.ts` retains MAIN's Runtime operation proxy and
  admission plugin while removing stale vendored Composition aliases.
- `package.json` retains the already-integrated Composition 0.0.13 artifact
  and current React pin required by the Timeline integration.
- `scripts/dev-local-workspace.mjs` retains MAIN's operation-origin plumbing.
- `src/app/main.bootstrap-order.test.tsx` differs only by formatting around
  MAIN's preserved bootstrap assertion.
- `src/tools/video-editor/contexts/VideoEditorProvider.tsx` retains MAIN's
  provider and adds the App-owned track-label command ports.
- `tests/e2e/fake-runtime/launch.mjs` differs only in a stale comment.
- `tests/e2e/local/support/harness.ts` retains MAIN's Runtime checkout fallback
  and adds the Timeline authoring/profile and current seed behavior.

No unrelated MAIN infrastructure was displaced by a Timeline assertion or
fallback writer.

## Assertion-preservation ledger

MAIN deletes 152 paths relative to the refresh base. Of those, 118 are retained
in the resolved merge and are byte-identical to the refresh base. These include
the command registry/capture/session/outbox files, current013/viewing fixtures,
native journey sources, and their tests. The remaining 34 deletions stay
deleted; they are MAIN-owned extension-fixture, runaway-timeline, and related
snapshot/caption tests, with no refresh-base Timeline changes on those paths.

The requested high-risk assertions were checked directly:

- `src/tools/video-editor/components/PropertiesPanel/TrackInspector.tsx` and
  `.test.tsx` are byte-identical between both merge parents' base and the
  resolved tree. The test retains the three Inspector preservation/refusal
  cases, including the a04f opaque-value preservation case.
- `tests/e2e/local/three-products.spec.ts` and
  `tests/e2e/timeline/command-outbox.spec.ts` are byte-identical to the base.
  The native journey still asserts opaque data preservation, durable outbox
  recovery, exact retry identity, Runtime restart, and zero legacy snapshot
  traffic (`wire.legacy`).
- Opaque/retry unit coverage remains in
  `authoringBundle.moveOpaque.test.ts`, `authoringBundle.sharedOpaqueRemap.test.ts`,
  `commitOutbox.test.ts`, and `commitSession.test.ts`.
- `useClipDrag.test.tsx` is byte-identical and retains exactly the three original
  `it.fails` cases: free multi-clip drag to a new bottom track, pinned-group
  cross-track drag, and pinned-group drag to a new track. No new expected
  failure was added.

## Test evidence

The source worker ran the following targeted commands against the resolved
working tree with the private public13 dependency overlay, private Vitest
cache/TMPDIR, `--configLoader=runner --no-cache --maxWorkers=1
--no-file-parallelism`, and no writes to shared dependencies:

1. Vitest command/TrackInspector/opaque/outbox/session lane over nine named
   files (`TrackInspector.test.tsx`, `TrackLabel.command.test.tsx`,
   `trackLabelCapture.test.ts`, `trackLabelGesture.test.ts`,
   `useTimelineOps.trackLabel.test.ts`, `clipMoveCapture.test.ts`,
   `authoringBundle.moveOpaque.test.ts`, `commitOutbox.test.ts`,
   `commitSession.test.ts`): **325 passed**.
2. Vitest state/drag/render lane over nine named files (`useClipDrag.test.tsx`,
   `useTimelineOps.test.ts`, `useTimelinePersistence.test.tsx`,
   `useTimelineSave.recovery.persistence.test.tsx`,
   `useTimelineState.history-authority.test.tsx`,
   `useTimelineTrackManagement.test.ts`, `TrackListRenderer.test.tsx`,
   `TimelineCanvas.test.tsx`, `TimelineEditorShellCore.test.tsx`):
   **424 passed, 3 expected failures**.
3. Vitest MAIN-overlap lane over nine named files: **241 passed**.
4. Private-overlay ESLint over 123 changed TypeScript/TSX files: **exit 0**.
5. `git diff --check`: **exit 0**.

This review did not rerun those tests because the source worktree was removed
after harness commit; the committed-tree byte and ancestry checks above verify
that the tested resolved source is the committed tree. No full suite, browser,
localhost/socket suite, build, project TypeScript check, or install was run.

## Applicability boundary

Current `/home/user/work/app` (`tl/integration`, `308ac52ad`) is a descendant
of the refresh base and adds later carrier/label work through the label
reconciliation and native media-import carrier merges. The later net changes
touch `dataProvider.ts`, media-import tests, preview-surface lifecycle,
`timelineOutputProjection.ts`, `timeline-data.ts`, and `timeline-save-utils.test.ts`.
Those later changes are not covered by the source worker's tests or by this
approval; they require their own carrier/label qualification and regression
run after integration.
