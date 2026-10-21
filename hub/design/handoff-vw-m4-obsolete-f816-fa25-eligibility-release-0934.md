# Viewing obsolete KEEP eligibility — 2026-10-21 09:34Z

## Result

No worktree was released. The approved recycle tool refused the eligible f816 candidate because its legacy worker metadata has no `worktree=` field. Per the task instruction, stop on that harness refusal; fa25 was not submitted to recycle.

## Candidate decisions

| Candidate | Eligibility evidence | Decision |
|---|---|---|
| `/home/user/work/wt/vw-m1-ssr-snapshot` (f816) | HEAD `f8164bef73215272562c4d6974acadbd82c2898a`, tree `4946dfa80999f3f9d828840c701544a67c8fe2b8`; `git -C /home/user/work/agent merge-base --is-ancestor f8164bef73215272562c4d6974acadbd82c2898a HEAD` exited 0; clean; worker ended; no candidate lease; no queued/running test marker; no live process/fd claimant. Current physical/partial proof is independent runtime4913/public13/ac4 evidence, and f816 M1 evidence remains in its branch, worker reports and retained raw media. | Eligible in substance, but retained because `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/recycle vw-m1-ssr-snapshot` returned `vw-m1-ssr-snapshot: no worktree` (exit 0). Physical worktree remains. |
| `/home/user/work/wt/vw-m3-pulse-fa25-pure-and-unsigned-grant` (fa25) | HEAD `fa25e6c8014cea998bebdc5a624399295e096b73`, tree `35616d4187bbc6e8a822647b7f03acc54f6ac65d`; clean, but `git -C /home/user/work/app merge-base --is-ancestor fa25e6c8014cea998bebdc5a624399295e096b73 HEAD` exited 1 (merge-base `6ff21cac9deee3aae014e5c9e65d9871a3452f77`), so the commit is not an ancestor of HOME App integration. Explicit lease remains at `managers/viewing/notes/pulse-fa25-pure-and-unsigned-grant.lease`; worker report is `BLOCKED_CENTRAL_SUITE_REGISTRATION`. | Retain. The required HOME-integration ancestry proof and stale-lease successor basis are absent. No recycle invocation was attempted after the f816 harness refusal. |

The active worker census contained only `vw-m3-gate6-physical-graph-clone-readiness-0934`, `vw-m3-partial697-snapshot-dependency-diagnosis-0932`, and this worker. The 0934 brief uses separate App pin0d43/graph8bdc and does not claim either candidate; no active brief claimed either candidate. There were zero queued/running test markers, and no process/fd claimant for either path.

Protected and untouched: current App0d43/d00 dist and graphs4913+8bdc; b70/helper/5a4/d0a/8f pins; scene-host; peer worktrees; shared installs, runtimes, snapshots, branches, reports and raw media.

## Storage measurements

Filesystem `/home/user/work`, block size 4096:

- Before recycle invocation: 2,778,075 free blocks = **11,378,995,200 free bytes**.
- After refused invocation: 2,778,050 free blocks = **11,378,892,800 free bytes**. No release reclaimed space; the 102,400-byte decrease occurred during the read-only audit/tool process.
- f816 allocated worktree before/after: **505,909,248 bytes / 505,909,248 bytes**.
- fa25 allocated worktree before/after: **312,766,464 bytes / 312,766,464 bytes**.

The owner00:50/lead01:08 authorization and actual floor refusals 32009 and 16444 are recorded in `managers/viewing/INBOX.md`; no guard was lowered and no other storage was touched.

## Tests and limits

No tests, browser, helper, render, install, socket, or bulk scratch operation was run. This was a storage/eligibility audit only. The only mutation attempt was the approved `bin/recycle` call, which refused without removing the f816 worktree.
