# App pin release safety report — 2026-10-21

## Disposition

`app-pin-3ee19006`: **RELEASE**. I removed only this marker:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-pin-3ee19006/KEEP`

The detached App worktree remains for the lead's normal `bin/recycle` action;
I did not remove or alter the worktree, `.git`, branch, refs, source, dist, or
dependencies. Commit/tree are
`3ee1900621f5ae27450ce5b1b69a3b7987e4b8c8` /
`38d6f715f05d0c00b89e131c3b8d4ae28a57fd44`, clean, and the commit is an
ancestor of current `/home/user/work/app` `c85da5427944d26242c71e503516d8d203a5f7a7`.
No active process or current farm request references this pin. The remaining
3ee records are completed/blocked historical Gate6 work, which is not a live
consumer under the release rule. Estimated worktree storage for lead recycle:
`1,155,031,040` allocated bytes (`1,028,912,055` apparent bytes).

`app-pin-d00a6613`: **KEEP; do not recycle**. KEEP remains at

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-pin-d00a6613/KEEP`

The exact commit/tree is
`d00a66134f330672ea7471dc69db38c1566d94cf` /
`a8bf53d5d5e865aa88825bbc20f6f530bfbaa7ba`, clean, and an ancestor of
current App integration. The current READY Gate6 farm request
`design/run-on-farm-viewing-gate6-1209.md` explicitly names
`/home/user/work/wt/app-pin-d00a6613/dist`: 339 regular files,
`284,372,591` regular-file bytes, and `dist/index.html` SHA-256
`aeb5d83399b453b15a8cbc67b31260cf2820f8d65770ccd458986ddd551e257b`.
The same farm request names the 0d43 source and the current1054 Runtime stage;
d00's private `node_modules` is also the target recorded by the active 0d43
graph-attachment lease. Exact dist archival has not been performed through the
required normal flat `<50 MB` design transport, so the d00 dist remains
protected. The d00 worktree is approximately `1,154,953,216` allocated bytes
(`1,028,841,621` apparent), but none is releasable while the named dist and
graph consumers remain live.

`app-pin-0d432391`: **KEEP; do not recycle**. KEEP remains at

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-pin-0d432391/KEEP`

The exact commit/tree is
`0d4323913b92c4e0e3830bf14ec7f35d981475ca` /
`5a1e0e85d0f336f642426b91ccf3b3f1984ebd14`, clean, and an ancestor of current
App integration. It is protected by
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/notes/gate6-app-pin-0d432391.lease`
and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/notes/gate6-app-pin-0d432391-node-modules-attachment-0930.lease`.
The current READY farm
request and its HOLD transport export both name this exact source. The
current1054 owned Runtime stage remains protected by
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage`
and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/notes/complete-runtime-stage-1054.lease`; no stage
recycle or graph release is authorized here. Estimated worktree storage is
`869,756,928` allocated bytes (`744,469,047` apparent).

## Safety checks

- `git worktree list --porcelain` confirmed all three exact detached worktrees;
  no branch/ref operation was performed.
- Ancestry checks with `git -C /home/user/banodoco/reigh-app merge-base
  --is-ancestor <pin> <target>` passed for all three pins against current
  App integration `c85da5427944d26242c71e503516d8d203a5f7a7`; all three are
  not ancestors of the unrelated upstream-main checkout.
- `git status --porcelain=v1` was empty in every pin.
- `realpath` checks found the pin roots and d00 dist as real directories. At
  final inspection, 0d43 `node_modules` also resolved as a real directory at
  its own path; the active attachment lease still records the manager's
  earlier one-consumer binding to d00, so that lease remains a blocker rather
  than being inferred away.
- The process scan found no active test, browser, Runtime, Vite, pack-host, or
  other process using any assigned pin. The farm/test marker scan found no
  running result marker. Completed Gate6 suites were not treated as consumers.
- Current farm references checked: READY
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run-on-farm-viewing-gate6-1209.md`, HOLD
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-gate6-farm-1210-REQUEST.md`, and
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/peer-viewing-to-farm-20261021T1246-readiness.md`.
  They use 0d43, d00 dist, and current1054 stage; none uses 3ee.

## Tests and non-actions

No tests, builds, installs, browsers, full suites, live sockets, or farm runs
were started, as required by the task. No source clone, graph copy, hardlink
deduplication, wildcard removal, worktree removal, or shared dependency write
was performed.

The only mutation was deletion of the proven-obsolete 3ee KEEP marker named
above. The lead should run only its normal `bin/recycle` path for 3ee, and must
not recycle d00 or 0d43 until the farm request, leases, d00 dist, and the
current1054 stage are explicitly released or transported under their stated
rules.
