# App2 peer courier delivery diagnosis — 2026-10-21

Snapshot: 2026-10-21T11:52:15Z. Read-only diagnosis; no product, hub, Git, daemon, network, credential, or queue mutation was performed.

## Verdict

Partial delivery delay, not an App2 outgoing-push failure.

- App2 STATUS and the named peer files reached the local hub mirror and `origin/main`.
- The last App2→App inbox peer delivery visible is the 11:12 popup request, delivered at 11:14:38Z.
- The 11:40 remove-ownership request is present in `hub/design` but absent from `hub/inbox/app.md`; this is the oldest unsent App inbox item. The 11:46 fixture update is also absent from that inbox.
- Therefore the remaining dependency is the existing hub-sync/main fan-out into App’s inbox, followed by the App/HOME owner ACK. Do not infer that App2’s peer work failed merely from the missing ACK.

## Exact source → hub mirror → inbox evidence

| Item | Source/mirror evidence | Hub identity | App inbox state |
|---|---|---|---|
| App2 STATUS dated 11:39 | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app2/STATUS.md`; SHA-256 `a32d4a2e…72f711`. The body of `/home/user/timeline-hub/hub/status/app2.md` is byte-identical; its sync header is expected. | Commit `ddbc0828ca833ee4e5ed8ad4cb2933be1825d348`, `refs/heads/main` and `refs/remotes/origin/main` both point here. | STATUS is in the mirror; no ACK is expected in `hub/inbox/app.md` for STATUS itself. |
| Popup explicit birth carrier, 11:12 | `/home/user/timeline-hub/hub/design/peer-app2-to-app-20261021T1112-popup-birth-carrier.md`, SHA-256 `ade3fc0a…443494`; the remote App2 source is not present under this machine’s local `orch/design`. | Commit `c507053569e8f0edb43052d17585c1da46bb33fd`, 11:13:34Z. | Present at `hub/inbox/app.md` section `2026-10-21T11:14:38Z`, and therefore successfully delivered. |
| Remove ownership, 11:40 | `/home/user/timeline-hub/hub/design/peer-app2-to-app-20261021T1140-remove-ownership.md`, SHA-256 `da640ce8…3638a57`. | Commit `fa6bf75f218b4e99abba8d3da55ac9e1f8894661`, 11:45:09Z. | **Absent** from `hub/inbox/app.md`; no HOME ACK can be expected yet. |
| Fixture/build update, 11:46 | `/home/user/timeline-hub/hub/design/peer-app2-to-app-20261021T1146-fixture-build.md`, SHA-256 `44bfaa60…bfa9a65`. | Commit `ddbc0828ca833ee4e5ed8ad4cb2933be1825d348`, 11:51:25Z. | **Absent** from `hub/inbox/app.md`; this is an update, not the missing ACK dependency. |

`hub/inbox/app.md`’s latest file commit is `ad3c1048533ebf43db9f2f091e6d021abe18aa3a` (11:35:03Z), which contains the popup delivery but neither the 11:40 nor 11:46 item.

## Clocks, queue, dispatcher, and locks

- Current UTC clock: `2026-10-21T11:52:15Z`.
- `hub-push.ok`: `2026-10-21T11:51:28Z`.
- `hub-sync.heartbeat`: `2026-10-21T11:51:28Z`.
- `dispatcher.heartbeat`: `2026-10-21T11:52:15Z`.
- `/home/user/timeline-hub` is clean at `main`, with local `HEAD == origin/main == ddbc0828…`; the named STATUS/peer files are therefore pushed to the local remote-tracking mirror.
- App2 queue has no recent `pending` or `refused` item. Recent `done` includes the diagnosis dispatch and the relevant App2 work. Two App2 `running` markers remain: the parent build worker and this diagnosis worker; neither was touched.
- PID files contain `27687` (dispatcher) and `27688` (hub-syncd), but no matching process was visible to this sandbox’s `ps`. The fresh heartbeats and current hub commit show activity, but process liveness is not independently proven here.
- No Git `*.lock`/`index.lock` was found in the hub clone or assigned App worktree. `$ORCH/.hub-sync.lock` exists as the expected flock anchor; its presence alone is not lock contention.
- `hub-sync` is configured with the current expected ORCH path `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`; no old/wrong ORCH path was found in the relevant scripts or markers.

## Historical transport errors and large files

The hub-sync log records earlier push failures, but they do not explain the current STATUS reaching `origin/main`:

- First logged push rejection: GitHub GH001 for `hub/design/app-ap2-m2-locked-graph-source.tar` at 286.89 MB, above the 100 MB limit (log lines 112–129; the log has no per-line UTC timestamp). That path is not currently present in the mirror, and was not moved or deleted by this diagnosis.
- Repeated `fatal: expected 'acknowledgments', received 'packfile'` / “push negotiation failed” and concurrent `cannot lock ref refs/heads/main` races appear later in the same log. Subsequent commits through `ddbc0828…` and the fresh `hub-push.ok` show that named App2 files eventually got through.
- Two still-present policy-rejected archives are 59,134,823 bytes and 63,765,389 bytes: `orch/design/handoff-vw-m3-main-image-cap-source-vector-main-source.tar.gz` and `orch/design/handoff-vw-m3-pcm-caller-current-land-unit-TREE.tar.gz`, with corresponding copies under `/home/user/timeline-hub/hub/design`. They are unrelated to the named App2 messages. Do not delete or move them without an owner/lease decision.

## Repair ownership / next step

The existing approved repair mechanism is the normal `bin/hub-sync` / `hub-syncd` design-to-inbox fan-out. The main/orchestrator hub-sync owner must reconcile the missing `hub/design` → `hub/inbox/app.md` delivery for `peer-app2-to-app-20261021T1140-remove-ownership.md` (oldest unsent, 11:40Z) and the 11:46 update. Then the App/HOME owner must ACK the remove request. No manual copy, delete, move, push, or daemon restart is authorized by this diagnosis.

## Commands/evidence run

Read-only commands included `date -u`, `stat`, `sha256sum`, `cmp`/`diff`, `git status`, `git log`, `git show`, `git show-ref`, `git rev-list`, `find`, `rg`, `ps`, and `cat`/`sed`/`tail` on the exact control files, hub paths, queue entries, and relevant log lines above. No product tests were run: this was a transport diagnosis and made no product change.
