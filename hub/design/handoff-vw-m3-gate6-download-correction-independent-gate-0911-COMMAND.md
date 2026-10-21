# Gate6 download-correction independent review commands

All commands were read-only; no browser, render, Runtime, helper, socket,
central, install, token, marker, or full suite was run by this review.

```text
sed -n '1,240p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md
sed -n '1,240p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/briefs/vw-m3-gate6-download-correction-independent-gate-0911.md
sed -n '1,260p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-gate6-download-name-source-diagnosis-0910-REPORT.md
sed -n '1,260p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-gate6-download-name-source-diagnosis-0910-PATCH.patch
git -C /home/user/banodoco/reigh-app show d00a66134f330672ea7471dc69db38c1566d94cf:tests/e2e/timeline/viewing-parity/cases.ts
git -C /home/user/banodoco/reigh-app show d00a66134f330672ea7471dc69db38c1566d94cf:src/tools/video-editor/lib/renderRouter.ts
nl -ba /home/user/work/app/src/tools/video-editor/lib/renderRouter.ts
nl -ba /home/user/work/app/src/tools/video-editor/hooks/useRenderState.ts
nl -ba /home/user/work/app/src/tools/video-editor/components/TimelineRenderControls.tsx
nl -ba /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-short-temp-device-inode-source-fix-0845/gate6-20261021T0845/playwright-output/player-export-normal-profi-d4d71-without-a-parity-comparison-native-codec-chrome155/error-context.md
sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-gate6-download-name-source-diagnosis-0910-PATCH.patch
git -C /home/user/work/wt/vw-m3-gate6-download-correction-independent-gate-0911 apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-gate6-download-name-source-diagnosis-0910-PATCH.patch
```

Results:

- Diagnosis FINAL report present and read; it classifies the first failure as
  a fixture/assertion mismatch.
- Patch SHA-256 matched the packet checksum:
  `679aade875b0131225ec8afbbfbbcf6c0918087ef8cb27e5f851b5f19605afef`.
- `git apply --check`: PASS; the patch was not applied.
- Relevant frozen d00/current HOME source paths were compared read-only.
- Diagnosis pure regression: frozen expectation **red**, exit 1; proposed
  timeline-id pure expectation **green**, exit 0. The browser assertion was
  not physically exercised.
- Review worktree remained clean; no product files were edited.

