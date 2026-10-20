# AP2-M2 ordinary stale-adapter owner request

App shared-core owner: apply this handoff to current base
`a11dd7a91af76a690f771ee06d9df960db323751` (`hub/tl/integration`). The
artifacts are at these exact absolute destinations:

1. `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-ordinary-stale-adapter-production.patch`
2. `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-ordinary-stale-adapter-regression.patch`
3. `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-ordinary-stale-adapter-peer-fix.patch` (combined alternative)

Use production then regression, or the combined peer-fix alternative, and
commit the App-owned `useTimelineOps` source/test change. The peer-fix SHA-256
is `97fb1c46827199b89f68e81cd912d72f3a6cce9bbe19fcf85d6a3a7bbc743149`.
The changed source paths are exactly:

- `src/tools/video-editor/hooks/useTimelineOps.ts`
- `src/tools/video-editor/hooks/useTimelineOps.test.ts`

The proven defect is a retained extension adapter dispatching stale callbacks
before the generic command port was available. The patch keeps one adapter
identity and dispatches all seven operations through current callbacks,
command-port state, and current edit authority; capture refusal remains
fail-closed. Do not change ordinary action scope based on the predicted fixture
issue that `moveExistingShotsToMarkers` selects five visual clips while the
journey expects two; that is not an observed native failure.

Reuse the existing evidence: 114 targeted tests passed, ESLint passed, and
`git apply --check` passed for all three patch forms against the base above.
After the owner commits the source, run one central
`e2e-m2-ordinary-integration` gate. No browser/socket/full-suite or dependency
work is part of this handoff.
