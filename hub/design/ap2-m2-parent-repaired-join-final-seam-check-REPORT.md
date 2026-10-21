# AP2-M2 repaired parent-consumer final seam check

## Verdict

**HOLD.** Do not approve `ae6347d4b987e4c00cf35b80b74c70ba783f2487` or activate
`ap2-m2-parent-current-repaired-consumer-join-shared-proposal.patch` yet.

## Remaining defect

The repaired async propagation is complete for the generation and general-asset
helpers, but not for the outer file-drop acceptance result. In the joined
`src/tools/video-editor/lib/external-drop-utils.ts`:

- `handleFileDrop` starts the image/video skeleton work in a detached
  `void (async () => ...)()` at lines 464-538. Its `dropAsset` calls are awaited
  and false/rejection cleanup is preserved at lines 479-499 and 521-537, but
  `handleFileDrop` returns unconditional `true` at line 541 before that work
  settles.
- The direct unsupported-media and oversized-media refusals at lines 335-348,
  and the caught direct prepared-placement refusal at lines 399-403, also fall
  through to that same unconditional `true`.
- `useExternalDrop.ts:115-135` treats that `true` as accepted. The drop handler
  then executes `onSeekToTime` at lines 656-657.

Therefore a native prepared-video false/rejection can remove its skeleton yet
still seek immediately, and an immediate unsupported/oversized file refusal
also seeks. This violates the requested “no seek” behavior for every external
drop refusal. The added test at
`src/tools/video-editor/hooks/useExternalDrop.test.tsx:295-326` covers the
general asset dispatch, but no focused assertion covers the file-drop path
where the detached async work returns `true` first.

The narrow repair must preserve the existing positive file-drop behavior and
skeleton cleanup while distinguishing “file event handled” from “placement
accepted” (or otherwise delaying the acceptance/seek decision until the
relevant placement settles). Add a focused file-drop test for native false and
rejection asserting skeleton cleanup, pending-operation cleanup, and no seek;
also cover immediate unsupported/oversized refusal if that path remains
accepted by the dispatcher.

## Confirmed repaired seams

- `useAssetManagement.placePreparedAsset` now branches on every prepared video,
  visibly refuses missing selection or missing command carrier, never calls
  local `applyEdit` for those cases, and surfaces bounded native refusal text.
- The native call forwards `forceNewTrack`, `insertAtTop`, and
  `removeClipId`; the existing native carrier refuses unsupported combinations
  rather than silently dropping intent.
- The multi-generation, single-generation, and general asset helpers now await
  `dropAsset` and propagate false/rejection. Existing positive assertions were
  retained; no assertions were removed, skipped, or weakened.
- The joined diff contains only the five row-local source/test files plus the
  reviewed evidence wrapper. The existing carrier, provider, store, session,
  selection, trim, and stale-adapter files are unchanged versus HOME.
- The unchanged native/service/session sources still capture a detached row and
  media basis before the verified-media await; the existing parent-session
  `localGeneration`, basis, displayed-head, clean/dirty, and submit fences and
  the parent capture stale-selection/owner/track tests remain in place.
- The shared construction proposal is inactive, uses the existing command
  carrier, and applies cleanly to both the worker HOME snapshot and shared HOME.
  No source pin or gate evidence is claimed.

## Checks

Independently verified:

- donor byte-equivalence checks for all six joined paths: PASS;
- `git diff --check hub/tl/integration...tl/ap2-m2-parent-current-repaired-consumer-join`: PASS;
- `bash -n` on the joined evidence wrapper: PASS;
- `git -C /home/user/work/app apply --check --whitespace=error /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-current-repaired-consumer-join-shared-proposal.patch`: PASS;
- same `git apply --check` from this review worktree: PASS.

The joined worker recorded the allowed focused Vitest run as 4 files/43 tests
passed, ESLint passed, strict-islands typecheck passed, shell syntax passed,
and the evidence failuretrap probe passed. I did not run browser, localhost,
socket, request-test, full-suite, or source-pin work.

## Next step

Repair and test the file-drop acceptance/seek boundary, then rerun the same
focused controls and obtain the required seam approval before applying the
inactive shared proposal. Keep the evidence wrapper’s current15 guards and
failure-before-cleanup behavior; add a new source pin only after final HOME
composition.
