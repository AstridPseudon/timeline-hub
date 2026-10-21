# Viewing lead handoff — 2026-10-20 ~21:25Z (read LEAD.md first; this is machine-specific)
Machine: viewing (home of composition). ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch. Orchestrator: session_01NCfFG4UM2PAWDGuSNXfJtu (send_message). Codex signed in here (ChatGPT login); bwrap, PulseAudio 16.1, ffmpeg, Chrome 155 (H.264) at /opt/google/chrome/chrome.
## Start / recover (all from the lead's own shell, NEVER inside a subagent sandbox)
- `$ORCH/bin/lead-recover` (LOCAL, idempotent): aborts a stuck hub-clone rebase; finishes finished-but-unfinalized workers (DONE/report) or marks dead ones 137+INTERRUPTED (only if no process AND log idle 10 min); marks dead tests; starts any dead daemon: dispatcher-daemon, `hub-syncd viewing`, adopt-watch; restarts the manager (`bin/run-manager viewing`, 3 h Codex rounds) unless STATUS says COMPLETE/BLOCKED. Refuses if it can't see the live dispatcher pid. Run it after every "worker process was restarted".
- LOCAL scripts (not in kit, so syncs don't overwrite them): lead-recover, lead-watch/lead-wait (event watch; ~10 min waits), lead-checkin (Codex READ-ONLY subagent → hub/status/viewing-lead.md + ACTIONS), lead-disk (oldest-first bin/recycle until target), adopt-watch (ADOPT, REHYDRATE, release-bulk, auto lead-disk <10 GB), adopt-remote-worker, lead/f816-compare.py, lead/node-modules-repair-compare.py. Protocol + history: $ORCH/lead/LEAD-PROTOCOL.md.
- Gotchas: never `pkill -f`/`pgrep -f` with a pattern that also appears in your own command (killed my shell 3x) — kill by literal pid/pgid. Every `rm` of a variable path must be `"${x:?}"`. Don't edit a script while an instance runs (bash reads incrementally).
## Graphs, leases, verification
- f816 clean peer graph: /home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules (KEEP). Verify: `python3 -I $ORCH/lead/f816-compare.py $ORCH/design/handoff-vw-m3-main-cap-controller-final-gate-graph-pre.json` → 21488/21488, 0/0/0, sha 9e556a876a02…c425. Repaired 18:05Z (nested @banodoco/timeline-composition/package from vw-m3-d09-labels-native-clean-proof's tar-through-symlink).
- Scene-host graph: /home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules (KEEP). Verify `python3 -I $ORCH/lead/node-modules-repair-compare.py` → 21495, 0/0/0 (106 self-links removed 16:42Z, owner-approved).
- private12 clean-project graph: workers/vw-m3-app-private12-clean-install + worktree vw-m3-tab-clean-install-source-compose (KEEP). Keep list: $ORCH/lead/keep-worktrees (+ ssr-snapshot, scene-host-plumbing, agent-gate, frame-harness-fix hard-coded in lead-disk).
- Shared App /home/user/work/app/node_modules: npm ci 16:43Z from App lock (HEAD d12d09097) → Composition 0.0.13 (== reviewed tarball 9412ae25…, 77/77), react 18.3.1, remotion 4.0.509; READ-ONLY (chmod -R a-w) except .vite/.cache/.vite-temp; root bypasses mode bits. Re-provision = `chmod -R u+w` first, then npm ci, then re-chmod.
- Pinned toolchain /home/user/work/toolchain/node-v20.19.4-linux-x64 (npm 10.8.2), installed 20:2xZ sha-verified — used by bin/make-runtime; never delete.
- Composition tl/integration history joined to upstream 67b8aa3 (e80c46ba, 09:17Z; proofs on hub).
## Watching now
- Gate 6 (Player/export frame + audio parity, planted negative) OPEN: frame 2 pass / 2 fail. M3 active, M4 incomplete. f816 requalification worker vw-m3-f816-live18-root6-reproof dispatched ~19:2xZ.
- Manager asked to re-request runtime agent-remotion-viewing13-d0a5072b (was EBADENGINE before the toolchain existed).
- App PEER REQUESTs in Viewing INBOX (L1159 five-case source ready; L1167 App2 → D10 reference catalog; L1245 app2 20:06Z) — manager's to answer; check they're acknowledged.
- Capacity: manager tends to run 0–4 live workers but many 2–6 min tasks (throughput OK); nudge via INBOX "LEAD NOTE" when <5 with open rows; restart if no dispatch for 30 min.
- Disk: keep >10 GB; worktrees nearly exhausted; bulk copies inside $ORCH/workers are freed only via manager's lead/release-bulk.txt (adopt-watch applies it, guarded). Stale /tmp worker scratch: prefer kit bin/sweep-tmp.
## Recent "Lead decided"
20:05 manager restarted onto 3 h rounds · 20:2x pinned Node toolchain provisioned · 18:05 f816 repair · 17:16–17:35 bulk releases (~2 GB) · 16:41–16:44 owner-approved graph repairs + App read-only · 14:25 no restart (manager adopted rules) · 14:48 no restart after capacity alarm (11 short workers).
## Only I know
- Check-in subagent once ran lead-recover inside its sandbox (22:34Z, 10-19) and falsely interrupted 3 live workers → it is now read-only and lead-recover refuses in a sandbox.
- My 10-19 lead-recover deleted live wt/.test-* snapshots at check-ins until 03:12Z; runs listed in INBOX 03:12Z/04:09Z were re-run.
- Notifications from the orchestrator queue behind a long turn: call ReadNotifications between every wait.
## Update 21:25Z
- f816 re-drift culprit (19:46Z): vw-m3-d09-labels-native-clean-proof tar-through-symlink style write; rule = real scope dirs + `ln -sfnT` + realpath check; manager/orch informed (design/handoff-lead-f816-selflinks-1946-culprit.md). f816 + scene-host stay KEEP until orchestrator OKs release (manager STATUS says lead may end obsolete protections after reader checks).
- Disk: sweep-tmp + npm/pip cache purge gave 13.5 GB free (owner target 13.0e9 decimal; manager-measured MP4 stage 580 MB). Re-run `bin/sweep-tmp` first when short.
- Lead line format (hub/status/viewing-lead.md): LEAD <UTC> | workers N | disk G | ledger rows DELETED x, in progress y | merges pending z | lead decisions since last hour. Report each work-list item 0-4,7.
- Gate 6 failing cases: cases.ts:239 (native-size Player frames vs CPU Remotion output), cases.ts:249 (picture-only patch mismatch after full baseline). Standing worker vw-m3-gate6-current-suite-owner.
- lead-watch now only flags vw-* worker exits (agt-* imported workers ignored).
## Update 00:42Z
- Manager restarted 22:43Z (capacity rule) and 00:42Z (kit 90-min rounds, orchestrator item 10). READY queue: bin/request-ready (dispatcher auto-starts under 5 live; log lines "READY viewing live=N" in dispatcher.log). Capacity swings 0-5 as short workers end together; only restart if <4 live for >15 min with empty ready/.
- Gate 6 one-shot worker failed closed 00:05Z for lack of a manager grant; orchestrator 00:09Z: manager sign-off is enough; put "authority: manager grant <ts>, tuple <ids>" in the run worker's brief. lead-checkin overwrites hub/status/viewing-lead.md with the subagent text; rewrite my own line after each check-in.
## Update 06:55Z
- Gate-6 pack-host failures = container env NODE_OPTIONS/NODE_PATH refused by remotion_runtime.py:222 probe_context; fix belongs in the run.sh (unset them), not the dispatcher. Told manager 06:55Z.
- Harness auto-mode DENIES releasing KEEP worktrees (ssr-snapshot/f816, fa25) and variable-path rm; literal-path rm of unreferenced finished-worker scratch and gzip are allowed. Disk hovers 10.8-11.1 GB (floor 10.74).
- Manager rounds are 90 min and auto-restart; live count swings 0-5; restart only if <4 for >15 min after a LEAD NOTE (orchestrator rule).
