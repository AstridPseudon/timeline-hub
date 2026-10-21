# Viewing KEEP/pin lease release — 2026-10-21

## Result

No eligible release was found. No `bin/recycle` call was made. Exact released bytes: **0**.

The only Viewing-owned `KEEP` marker is `vw-pin-5a4e9b72`, the Composition 5a4 source at `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8` (allocated worktree measurement: 839,680 bytes). It is still the frozen Composition input named by the Gate6 source tuple and current one-shot command, so it remains protected even though it is clean and its commit is an ancestor of Composition integration `df7b86308902fae90eda1dc3080d17d8fc30ea78`.

The following were not release candidates: the leased 1054 Runtime stage; Runtime4913/source; the App0d43 source and graph attachment; `vw-m3-scene-host-plumbing`; `vw-m3-runtime-source-lease2`; and the fa25 source. Their notes/leases or current Gate6 source records still protect them. `vw-m3-frame-harness-fix` and `vw-m3-scene-source-carry` are dirty/interrupted WIP and are not eligible for normal recycling. Agent, Runtime, and App pin markers were outside this Composition worker's release scope and were not touched.

## Measurements and checks

- Disk available at 2026-10-21T12:11:36Z: `11,289,960,448` bytes.
- Final disk available after the read-only audit: `11,289,194,496` bytes. The small change occurred without a release; released bytes remain `0`.
- `find "$ORCH/tests" -type f -name running`: 0 local running-test markers.
- Process/cwd scan for the candidate names and Gate6: no relevant external process found (the scan's own shell was excluded from the interpretation).
- `git status --short --branch` in the assigned worktree: clean.
- `git -C /home/user/work/composition worktree list --porcelain`: confirmed the Composition pin and current integration worktrees.
- `git -C /home/user/work/wt/vw-pin-5a4e9b72 show -s --format=... HEAD`: confirmed the exact frozen pin identity.
- `git -C /home/user/work/composition merge-base --is-ancestor 5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8 df7b86308902fae90eda1dc3080d17d8fc30ea78`: exit 0.
- `lsof -nP +D /home/user/work/wt/vw-pin-5a4e9b72`: no open handles reported.

No product tests, build, browser, socket, install, full suite, physical run, deduplication, hardlinking, compaction, branch mutation, or manual removal was performed.

## Evidence paths

- Brief: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/briefs/vw-m4-keeps-release-round-1209.md`
- Current status: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/STATUS.md`
- Runtime stage lease: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/notes/complete-runtime-stage-1054.lease`
- App0d43 leases: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/notes/gate6-app-pin-0d432391.lease` and `gate6-app-pin-0d432391-node-modules-attachment-0930.lease`
- Gate6 Composition pin record: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-pin-5a4e9b72/KEEP`
- Prior release disposition: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owned-keep-release-current-0912.md`
