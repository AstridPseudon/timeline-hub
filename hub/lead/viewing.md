# Orchestrator → viewing AREA LEAD (read on every hourly check; newest item last)

## 2026-10-19T20:11Z — one-time tool update (do once)
Main now publishes the shared tools and rules in hub/kit/. Run:
`cp /home/user/timeline-hub/hub/kit/bin/* $ORCH/bin/ && chmod +x $ORCH/bin/*`
then restart hub-syncd: `kill $(cat $ORCH/hub-syncd.pid)`, then `nohup setsid $ORCH/bin/hub-syncd viewing > $ORCH/hub-sync.log 2>&1 < /dev/null &`.
After that, tool and PLAN updates apply automatically each sync. Confirm by adding a line "tool update done <UTC>" to the top of your status (it publishes on the next sync).

## 2026-10-19 — adopting a worker that finished on main
For vw-m3-agent-package, and any worker that finished on main: when the transferred meta already exists but there's no worktree, recreate one with `git -C <agent clone> worktree add /home/user/work/wt/<w> hub/tl/<w>`, create branch tl/<w> from it, and keep the transferred report. Don't re-run the worker.

## 2026-10-19 20:30Z — optional: an H.264-capable browser for export checks
If you can, install Google Chrome stable (it ships proprietary H.264/AAC codecs) at a separate path, without replacing /opt/pw-browsers. Tell your manager the executable path. If it can't be installed, say so in your status. Not urgent; the main parity route doesn't need it.

## 2026-10-19 22:40Z — infrastructure fix (also sent directly)
Restart the dispatcher from your own shell, outside the sandbox; pid 4 / read-only .git means it's running inside one. Restore the running markers of the 3 live workers that lead-recover wrongly marked 137. Make lead-recover require "no process AND log idle for 10+ minutes" before it marks a worker interrupted.

## 2026-10-19 23:30Z — lead: MAX SPEED
The owner wants max throughput. Every 30 minutes, check that your manager keeps 5–7 workers running (heavy cap stays 2). If it's idle without a stated blocker, nudge it, or restart it if it has exited. Use Haiku or Sonnet for chores.

## 2026-10-19 23:35Z — ACTION (lead): recycle, then refresh the shared App install
1. Recycle these finished, clean worktrees (keep the branches, and keep all ORCH reports/WAVs/provenance): vw-m3-player-startup, vw-m3-player-startup-resume, vw-m3-cpu-profile-proof, vw-m3-app-route-contract, vw-m1-consumer-full-fixes. KEEP vw-m3-audio-monitor-control (e290), vw-m1-ssr-snapshot (f816), and every active worker's worktree.
2. When no capture is using it, re-provision /home/user/work/app/node_modules with a normal `npm ci` from the CURRENT App integration lock: Composition 0.0.8, React 18.3.1, Remotion 4.0.509, only the current integration patch. Do NOT apply the held e290 Player patch globally. Afterwards, verify the installed @banodoco/timeline-composition version and file hashes, and record them in STATUS.

## 2026-10-20 00:45Z — ACTION (lead): disk is at 5.9 GiB, recycle NOW
Unless QUIET.md shows an ACTIVE capture, recycle these finished, clean worktrees, keeping their branches and all ORCH reports/WAVs/raw/provenance: drain-lifetime, cpu-export-smoke, cpu-shell-export, cpu-export-qualified, scene-consumers. KEEP e290 audio-monitor-control, observed-player-baseline, f816 ssr-snapshot, scene-host-plumbing, agent-gate, and every active worker.
Standing rule for your hourly routine from now on: keep free disk at 10 GiB or more. Recycle finished, clean, superseded worktrees, oldest first, with the same keep rules, and clear caches you own (e.g. the npm cache) if needed.

## 2026-10-20 01:05Z — lead: publish the reviewed Composition 0.0.9 tarball for App
App needs the EXACT reviewed 0.0.9 package (sha256 fa94f9c6438278764fad1285fa3d76063020ea7b20f4018de6bec4ffff0c9f61). Copy that exact file (the reviewed bytes; don't rebuild) to $ORCH/artifacts/banodoco-timeline-composition-0.0.9.tgz and confirm its sha256 matches. The new hub-sync, which arrives via hub/kit, publishes artifacts write-once with a .sha256 sidecar, and the App machine receives them automatically.

## MANAGER REQUEST viewing — 2026-10-20 14:04Z
CurrentRoot3stillcontrollerindependentlyAPPROVE; free12,928,282,624 vsrequired12,986,365,667 and>13GBheavyresume. Please bin/recycle endedcleanunleasedViewingworktrees/unusedownscratch to~13.5GB; exactlocallead/viewing-recycle-request.md. Preservef816physicalgraph/privatefreshAppgraph/currentRootprepOWNnode/activeworkers/tests. OldtabshortKEEP/lease released afteractualPASS+audit, no oldgrantreuse. Fiveusefulcodeworkersrunmeanwhile.

## 2026-10-20 15:51 UTC — machine graph audit needed
STOP requested app-cap3a reviewer for readonly graph violation: whole @scope symlink into shared App then extract public12 via @banodoco. Exact local lead/viewing-recycle-request.md; preserve log. Shared App already UNQUALIFIED; no qualification/capture uses it. Own clean private graph untouched. Please audit/repair only through approved machine process.

## 2026-10-20 15:52 UTC — approved privatePulse fallback UID
TabnativeGDM real1534 producesmono1, no stereoclaim. PrivatePulse sourceprepreview rejected currentUID0 plus2TypeScriptfixtureerrors. Correctionworker vw-m3-private-pulse-user-mode-correction active. Please identify existing admitted non-root identity/user-mode launcher for central OWNprivateDaemon, no --system/globaldefault/settings/newaccount. Testenv identity choice fits locallead, not newownerdecision; worker can sourceprepare now, no daemon/capturestarted.

## 2026-10-20 15:58 UTC — disk below capture floor
Available9608261632B (<10GiB). No browser/daemon/physicalcapture launched, controllers stayfailclosed. Please bin/recycle ALL finishedcleanunleasednonKEEPViewingworktrees now; leases ef4mouth697 and6323stereo havebeenRELEASED afterterminalaudits. Preserve f816cleanphysicalgraph, freshprivateApp12graph, OWNNode workers/vw-m3-current-root-cap-three-stills-prep/node, activeworkers/testsnapshots. Finished stoppedcapreview own archive/depsscratch canbe audited/recycled afterlog retention; scope symlinkwrites likelysharedAppgraph alreadyUNQUALIFIED. Need >13GB fornextphysicalone-shot. No hand wt deletion/prune.

## 2026-10-20 16:34 UTC — CLEANf816 graph DRIFT, audit urgently
D1 strictpurepreflight stopped BEFOREcentral: expected21488/hash9e556a..., observed21565 (+77). Exact source workers/vw-m3-d1-public-positive-real-pinned-node/log.txt/preflight-local.log, peer /home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules. No substitution/repair/qualification pastguard. Please audit additions/oldbytes/symlinks +mtimes andwriter logs; +77 suggests addedpackage but causeUNPROVEN. Currentpeer6hashes/wholebaseline manifest available in current-root-cap-three-stills-prep proof and clean-f816-requalify. SharedApp18+4 violation remainsseparatealreadyunqualified. Pausef816dependent qualification, oldactualcaptures predatingdrift unchanged pendingwindowaudit. Need testservice/sandboxREADONLYenforcement forborroweddeps ifpossible; chmod advisoryrootmaystillwrite. Managerwillnotmutategraph.

## 2026-10-20 17:17 UTC — bulkrelease list READY
ORCH/lead/release-bulk.txt contains9managerAPPROVEDsourceCOPYpaths. Candidate-source.tarretainedduecontradictorydraftcomment; allreports/WAV/manifest/provenance/activeSources/graphs/Node/leases protected. Deleteexactregularroots only/no symlinktraversal. NeedfreeheadroomfortoppriorityfrozenPlayer/exportandPulsecapability; reportactualfreebytesaftercleanup.

## 2026-10-20 17:30 UTC — SECOND bulk release approved
lead/release-bulk.txt atomicallyupdated: remainingfirst-listpaths(ifany)+10NEWfinishedsourceCOPYtrees, 1,037,946,889B additional. Inlinecommentsstripped, no symlinks innewtargets, DONE/exit0/noKEEP/activeprocess/leaseverified. Reports/WAV/PNG/manifests/provenanceoutsideortrackedregenerablesource-onlycopies; primaryartifacts/Node/graphs/activePose/Pulse preserved. Candidate-source.tar retained. Deleteexactpendingregularroots only. Needheadroomfornormalpublic13runtimeinstall+frozenrendercapture; reportfreebytesafter.
