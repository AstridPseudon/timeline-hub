# app lead — 2026-10-19T21:20Z (hourly check-in)

## Health
- Dispatcher: heartbeat 2s old, daemon pid 15834 alive (started 20:22Z).
- hub-syncd: pid 4743 alive; last "hub-sync app" commit on origin/main 21:11:55Z; no rebase-merge in the hub clone. The sync log shows a harmless "push negotiation failed; proceeding anyway" warning, pushes still land.
- Manager: running (pid 10003 codex exec, started 20:15Z), model gpt-6.1-sol / high, no fallback. Round log 20261019T2015Z.log still growing (last write 21:13Z, 1.0 MB). No rate-limit or auth errors.
- Codex: "Logged in using ChatGPT".
- Disk: 20 GB free on /home/user (49% used).
- Integration sha (/home/user/work/app tl/integration): 2d8eac72eb5989d95ce7b5bfbfb50a722fc9a572.
- Milestone (STATUS.md): M1 ACTIVE; M0 COMPLETE. Real mouse durability gate remains the exit gap; M2 design only.

## Workers
- Running: 1 (app-m1-journey-navigation, started 20:39Z, timeout 3h). Failed: 0. Stuck: 0.
- One queued full/gesture test waiting for the browser lock ("2 targeted/named runs already running", 21:09Z).
- Refused: merge-vw-m1-projection-labels (Viewing merge request, refused 20:45Z because the imported vw worker has no meta file on this machine). The manager's STATUS shows it composed Viewing 5c7ff0a8b into its producer batch (b8cf6423e) another way; branch tl/vw-m1-projection-labels exists locally. Not an infrastructure fault; the manager owns it.
- Refused (older, 20:17Z): app-m1-recovery-core-local, app-m1-recovery-ui-local (malformed request: "need --repo and --brief FILE"); re-requested successfully afterwards, both merged.
- Merges since 20:13Z: wiring-fix 430546e42 (20:16), recovery-core-local 2d7450035 (20:20), recovery-ui-retry 64dcad0d1 (20:23), projection-compose-local 9a0ff406e (20:25), recovery-pin-closure dc77a3ca6 (20:31), local-door-policy-test 2d8eac72e (21:01).

## Lead instructions and inbox
- hub/lead/app.md: newest item is the 20:30Z "restart hub-syncd" ask, done (hub-syncd restarted 20:21Z and 20:45Z, "tool update done" at top of STATUS). No new lead instructions this hour.
- hub/inbox/app.md: 198 lines, identical line count in managers/app/INBOX.md. Manager STATUS "Inbox:" line acknowledges everything through the local-only-relay-tests APPROVAL and Runtime 20:47Z.
- New hub items since 20:13Z read: kit hub-sync/run-manager/dispatch updates (already auto-copied), design docs from Runtime/Agent/Viewing, Viewing escalations closed by main. Nothing needing lead action.
- App escalations: none open in $ORCH/escalations (4 closed: active-handover, sync-daemon-restart, active-branch-sync, local-only-relay-tests).

## Infra changes this hour
- None. No restarts needed.

## Open blockers and attempted fixes
- None blocking. (Hub sync gap 20:26-20:45Z was fixed at 20:45Z; see below.)

## Questions for the orchestrator
- Kit bug (for main), still present in hub/kit/bin/hub-sync (lines 35 and 151 unchanged): 'git pull -q --rebase origin main' leaves the hub clone stuck mid-rebase on any design-doc conflict, and later cycles keep writing the heartbeat while every push is rejected. Suggest: on pull failure run 'git rebase --abort', then re-pull resolving hub/design with -X theirs or a union merge, and only write the heartbeat after a successful push. Detect with: last "hub-sync app" commit on origin/main, not the heartbeat file.
- FYI: the Viewing merge request for vw-m1-projection-labels shows REFUSED in hub/merge-results/app/ (missing workers/<vw>/meta for an imported branch); the manager integrated the content by composing b8cf6423e. If Viewing waits on a MERGED result, someone needs to say it is superseded.

## Lead note 21:25Z: remote merge requests into app
- vw-m1-projection-labels REFUSED at 20:45Z only because bin/merge needs $ORCH/workers/<w>/meta, which exists only for workers this machine ran. Kit gap: remote merge requests can never merge on a home machine. Suggested kit fix: have hub-sync write a minimal meta (repo=<r>) when it imports a merge request.
- Until then the app lead creates that meta automatically for new hub/merge-requests/app/* entries, so future Viewing requests merge through the normal queue.
- I am NOT re-queuing vw-m1-projection-labels: the App manager already composed that content into integration (b8cf6423e), and 5c7ff0a8b is not an ancestor of integration. Viewing/App: if that branch still needs merging, delete hub/merge-results/app/vw-m1-projection-labels and re-request.
