# AP2-M2 ordinary shared absolute artifact delivery

The three committed donor patches were copied byte-for-byte from the worker
branch into the actual shared ORCH design directory. The required owner
request was added at the same flat destination because it was absent from the
donor commit.

## Destinations and SHA-256

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-ordinary-stale-adapter-peer-fix.patch` — `97fb1c46827199b89f68e81cd912d72f3a6cce9bbe19fcf85d6a3a7bbc743149`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-ordinary-stale-adapter-production.patch` — `8a1ce7c8db7e9b5ffa8fb315ac95021e59733768bbe9d2e6f0480336628f2b79`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-ordinary-stale-adapter-regression.patch` — `96c0a1c50ab8c0920df51361b51b46fe99533b8a026b8a0c938df0041b3875b5`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-ordinary-stale-adapter-owner-request.md` — `26764cc71d24b301760aa2c97b928af82540a6f4d7f5a3d8c1a8eee2c44617af`

## One-screen owner instruction

Applicability is current base `a11dd7a91af76a690f771ee06d9df960db323751`
(`hub/tl/integration`). Apply production then regression, or use the combined
peer-fix, then commit the App-owned `useTimelineOps` source/test change. Exact
paths and the central post-commit gate are in
`handoff-ap2-m2-ordinary-stale-adapter-owner-request.md` at the absolute
destination above. Do not alter ordinary action scope for the predicted
five-visual-clips fixture mismatch; it is not an observed native failure.

## Evidence reused and scope

Existing evidence is 114 targeted tests passed, ESLint passed, and
`git apply --check` passed for all three patch forms against the current base.
No product/source edits, dependency work, browser/socket/full-suite run, or
private App copy was made here. After the owner commits, run one central
`e2e-m2-ordinary-integration` gate.

Exact reused commands and results:

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

git apply --check handoff-ap2-m2-ordinary-stale-adapter-peer-fix.patch
git apply --check handoff-ap2-m2-ordinary-stale-adapter-production.patch
git apply --check handoff-ap2-m2-ordinary-stale-adapter-regression.patch
=> all passed against current base a11dd7a91af76a690f771ee06d9df960db323751
```

These commands were run by the donor diagnosis/handoff evidence and are
reported here as reused evidence; this placement worker did not rerun tests.

The owner request is the only newly authored handoff text; all three patch
artifacts are exact donor copies. Final destination verification:

```text
97fb1c46827199b89f68e81cd912d72f3a6cce9bbe19fcf85d6a3a7bbc743149  handoff-ap2-m2-ordinary-stale-adapter-peer-fix.patch
8a1ce7c8db7e9b5ffa8fb315ac95021e59733768bbe9d2e6f0480336628f2b79  handoff-ap2-m2-ordinary-stale-adapter-production.patch
96c0a1c50ab8c0920df51361b51b46fe99533b8a026b8a0c938df0041b3875b5  handoff-ap2-m2-ordinary-stale-adapter-regression.patch
26764cc71d24b301760aa2c97b928af82540a6f4d7f5a3d8c1a8eee2c44617af  handoff-ap2-m2-ordinary-stale-adapter-owner-request.md
```
