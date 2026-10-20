LEAD 2026-10-20T21:08:28Z | workers 3 | disk 11.2G (guard 13.96G) | ledger rows DELETED: D10-Agent-source-wrappers, D10-App-copies, VW-DEAD-RENDERPIPELINE, VW-DEAD-INSPECTOR; open D08, D09, VW-AUDIO-STEP | lead decisions: item-0 disk relief; f816 106 self-links removed (culprit found); manager on 3h rounds
ITEM 0 (disk) DONE-as-far-as-safe: gzip codex sessions >6h (468 files, +575 MB); caches purged; compact-scratch 20 (1 dir); gzip 589 finished worker logs (log.txt.gz, ~0.6 GB logical) + 1 tar; 4 /tmp host-env roots earlier. Net free is swinging 10.1–11.5 G because a controller test is cloning a 790 MB app pack into /tmp/timeline-controller-test-* and new app worktrees keep appearing. Still under 14 G: top users (MB):
    376 MB  /home/user/work/runtimes
    443 MB  /opt/google
    519 MB  /home/user/work/venv-agent
    548 MB  /opt/google-cloud-sdk
    554 MB  /tmp/vw-m3-public13-host-one-root-catalog-stage
    707 MB  /opt/node22
    825 MB  /home/user/work/app
    924 MB  /opt/pw-browsers
   1190 MB  /root/.codex
   1494 MB  /tmp/timeline-controller-test-ifKMqn
   1564 MB  /home/user/timeline-hub
   2257 MB  /home/user/peteromallet
   2702 MB  /home/user/banodoco
   3672 MB  /home/user/work/wt
   3707 MB  /tmp/claude-0
Releasable only by your decision: KEEP worktrees (scene-host-plumbing 830, ssr-snapshot 483, tab-clean-install 299, tab-short-owned-tmp 299), /tmp/vw-m3-public13-host-one-root-catalog-stage 554 (frozen closure), hub clone timeline-hub 1.5 G, reference clones peteromallet/banodoco (2.3/2.7 G object stores that all worktrees share).
ITEM 1 (frame/audio positives + planted negative, one tuple): 2 pass / 2 fail, failing-case names + workers NOT in manager STATUS yet (asked 20:57; will name next line). Blocked on MP4 staging disk + five-case owner-base leaf fixes. ITEM 2: vw-m4-app-stale-requests-successor-map (resume from checkpoint). ITEM 3: D09 waits for real managed Scene positive (vw-m3-scene-posthandoff-real-binding-cause, HARD Sol) + Agent core/SDK gate. ITEM 4: asked manager for ledger row ids.
CULPRIT f816 self-links (19:46:49Z): vw-m3-d10-full-root-package-build, workers/…/log.txt L7186-7232: for entry in "$OLD"/* "$OLD"/@*; (double glob visits each scope twice) then plain 'ln -s' onto the already-linked scope dir wrote pkg/pkg -> pkg into f816. Prevention: single pass over scopes + 'ln -sfnT' into verified real dir. Report: design/handoff-lead-f816-selflinks-1946-culprit.md. Repaired 20:50Z (0/0/0).
