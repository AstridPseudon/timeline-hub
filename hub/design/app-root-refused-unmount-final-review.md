**Verdict: HOLD pending the live-port / management-hook lifetime decision.** The original refused-row-unmount defect is fixed: the prior external exact3 diagnostic passes unchanged on desktop, phone and tablet. One additional hook-remount probe fails on all three device classes: a retained finish callback bypasses the new hook's track lock. This is a reproduced hook-contract counterexample, **not a demonstrated actual-App UI or Runtime authorization bypass**. No source or repository test was edited.

Reviewed App HEAD `2b75c7e684afe44283ce0d5fe31c72fc9da2b7c6`, tree `098023fc386ebd1ab949b79eda44e0bb2b4bb502`, against `927545cf52fdfbb273afbe7f190e00e11e5e2d70`. Read PLAN, the implementation design/brief, prior MAIN17 final-review HOLD, its external fixture and failure JSON, and the earlier clean-focus review. No settled plan decision was changed.

**Finding requiring an orchestrator judgment.** At `useTimelineTrackManagement.ts:906–924`, the captured finish callback closes over that hook instance's `editabilityRef`. `TrackLabel.tsx:427` stores this callback in the port-owned draft; remount reuses it at line 442. When the management hook also remounts under the same live port, the retained callback still consults the old hook's ref. The newly mounted hook's guard is never consulted for this draft. Retaining the original authored capture is correct; retaining obsolete host editability is the concern. `timeline-editability.ts` explicitly requires checking current host locks at commit time, and the existing management suite tests that requirement for a continuously mounted hook.

Private reproduction uses the same hook-plus-row lifetime as the unchanged exact3 fixture, actual label capture/finish functions and the actual production row, with only the final session handoff stubbed:

1. Mount an unlocked row under a live port, focus/type `Keep guarded intent`, and unmount. The first submit refuses synchronously; the draft survives.
2. Permit that stubbed handoff to succeed, then remount the management hook and row with the **same port**, now passing `createTimelineEditability({lockedTrackIds:['V1']})`.
3. Focus/blur to explicitly retry. Expected: no second submit, `track_locked`, retained draft. Observed: **second submit occurs**, still with only one capture. All three device cases fail at the second-submit assertion; later alert/draft assertions are not reached.

Evidence: `notes/lock-remount.review.test.tsx`, `lock-remount.log` and `lock-remount.json`. These are ordinary success expectations with no fails/skip/todo markers. No failed expectation was rewritten or suppressed.

Reachability limit matters: the current App calls both `useTimelineSave` and `useTimelineTrackManagement` within `useTimelineState` (lines 629 and 945). Ordinary row-only remount leaves the management ref live; the existing current-lock tests pass. I did not establish an actual UI path that remounts only management while keeping its command port. The implementation design explicitly claims hook-plus-row remount support, and its exact3 proof uses that lifetime. Recommended decision: either qualify/enforce the narrower supported lifetime, or assign a bounded fix that checks the live host editability while retaining the original captured basis and port. Do not refresh authored value/identity guards or allocate replacement request identities to solve this. Fresh independent approval is still required before the actual UI gate.

**Passing review and preservation evidence.**

- Existing main-suite targeted tests: **12 files / 457 passed / zero failed or skipped**, 51.87 seconds. Label command 43; renderer 50; canvas 79; management 28; Ops label 24; gesture 8; native capture 73; commit session 72; command hook 15; projection 24; recovery UI 14; outbox 27. The known project-switch/Keep act warning reappears; no failed test or unhandled exception.
- Original external exact3: **3 passed**, 4.42 seconds. Copied byte-for-byte from the prior reviewer; its earlier JSON records the three `Keep after refused teardown` versus `Original` failures. The same exact test block is now present unchanged in the normal label suite. All 27 original committed test bodies/assertions are unchanged.
- Independent private lifecycle probes: **12 passed**, 6.41 seconds. Same-ID owners A/B retain separate dirty values/errors/captures through remount; accepting A clears A without clearing B. Sibling tracks share a port without mixing drafts; accepting or releasing a clean V2 leaves refused V1 intact. Blur followed by touch-sheet close and row unmount attempts finish/submit once, for both refusal and successful handoff. Remount itself does not capture or submit. A retry uses the identical original basis object and command after a remote label change. These project/session identities are simulated owners, not real provider switching or Runtime acceptance.
- Normal suites additionally cover capture refusal persistence, clean focus/teardown release, typed-away/back explicit intent, explicit empty input, original raw guards, native stale/generation refusal, exact unknown-ACK/restart retry, owner-fenced ACK/discard/recovery, and explicit Keep choosing a new guard/key. Existing outbox discard and ACK implementations are unchanged. Unsent row drafts are released on clean finish or successful local handoff; no new row-draft discard UI was added or independently qualified here.
- Source delta versus 927 is exactly **four files: 190 added / 50 removed**. Product delta: three files, net +18 lines. **5,828 other tracked paths** retain exact base bytes, including symlink identity. The new map is transient on the existing command port, keyed by track ID. No new durable store, journal, history, wire/model field, automatic recapture, ACK behavior or fallback writer was introduced. The actual command-session port is created per session; provider/timeline cleanup disposes it, and native stopped-session checks remain unchanged. The passing hook/outbox suites cover cleanup and late-ACK fencing.
- MAIN17 renderer/canvas settings, audio/video add and confirmed delete tests pass. The MAIN17 shell/test, mobile inspector and sheet constant retain exact 927 bytes, preserving no-Text and Move/Trim source. All six server/proxy paths, both wrapper files, the seven complete journey bodies/helpers/configs and provider parity source remain unchanged. This is preservation evidence, not rerun browser/journey/proxy qualification.
- Normal013 manifest/generated files, package manifest/lock and public12 archive equal approved `171a259a`. All **13** locked destinations match their hashes and pinned producer committed/current bytes. Public12 SHA256 remains `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; all **77** safe regular archive members match this review's private installed package. Wrapper/journey comparisons use approved `cee35da4`.

**Exact commands.** All ran from `/home/user/work/wt/app-m3-root-refused-unmount-final-review`. Variables only abbreviate paths:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W="$O/workers/app-m3-root-refused-unmount-final-review"
N="$W/notes"
```

Main-suite targeted run:

```sh
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx \
  src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx \
  src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx \
  src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/commands/trackLabelGesture.test.ts \
  src/tools/video-editor/commands/trackLabelCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/components/TimelineCommandRecovery.test.tsx \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  --reporter=default --reporter=json --outputFile.json="$N/targeted.json" \
  > "$N/targeted.log" 2>&1
```

Diagnostic invocations, respectively **3 passed**, **12 passed**, **3 failed**:

```sh
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/unmount.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  "$N/row-unmount.review.test.tsx" --reporter=default --reporter=json \
  --outputFile.json="$N/exact3.json" > "$N/exact3.log" 2>&1

env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/lifecycle.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  "$N/lifecycle.review.test.tsx" --reporter=default --reporter=json \
  --outputFile.json="$N/lifecycle.json" > "$N/lifecycle.log" 2>&1

env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/lock-remount.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  "$N/lock-remount.review.test.tsx" --reporter=default --reporter=json \
  --outputFile.json="$N/lock-remount.json" > "$N/lock-remount.log" 2>&1
```

Other checks, all pass:

```sh
python3 -B "$N/audit.py" > "$N/audit.json"
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
node scripts/quality/check-known-failures.mjs
git diff --check 927545cf5 HEAD
git diff --exit-code
git diff --cached --exit-code
git ls-files --others --exclude-standard
```

Vendor check reports `ok runtime.lock.json (matches pinned producer commit)`. Known-failures gate: **3 original authorized markers / 0 forbidden**. The first local audit attempt incorrectly compared symlink target contents to Git's stored link text at CLAUDE.md; corrected the private audit to compare link text, then the full audit passed. No product/test correction was made.

**Limits and handoff.** No full suite, build, browser, socket/localhost, install, project tsc, central test request, real Runtime acceptance/reload/undo, owner-film, pixel/audio or macOS run. Previous 927 type qualification does not qualify the changed source. All device tests use jsdom device props. No new wrapper/Agent-pair acceptance or M3 completion is claimed.

Only this worktree's ignored node_modules symlink was redirected. This worker created a private12 overlay: dependency entries point read-only at `/tmp/app-coherent-deps12/node_modules`, while public12 was privately extracted from the immutable archive. Shared dependency trees, runtimes, venvs and caches were not modified. Config runner, no-cache, private cacheDir/TMPDIR and one worker were used. Private temporary/cache directories were removed; private fixtures/logs/JSON/overlay are retained for review outside the worktree. Repository tracked/staged/nonignored untracked changes remain empty.

Review task complete. Wrote design/report/commit-msg/DONE; no KEEP or BLOCKED. No commit, checkout, merge, push, ref change or integration-worktree edit. The orchestrator should resolve the lifetime boundary above before deciding whether to request a fix or another final approval, then arrange the separately required type/UI qualification.
