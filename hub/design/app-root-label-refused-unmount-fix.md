# Refused track-label row teardown fix

Implemented on App `927545cf52fdfbb273afbe7f190e00e11e5e2d70` (tree `96605f2a46c49fcf96cd12ca3679014f00ae28de`). **Worker implementation complete; actual paired gate remains HOLD until independent approval.** No settled plan decision changed.

## Original failure and change

The Main17 final review identified that focused whole-row teardown invokes finish once, but a synchronous refusal is caught only in disappearing component state. Reproduced its exact three desktop/phone/tablet expectations in the normal `TrackLabel.command.test.tsx`, unchanged: original source gives **27 passed / 3 failed**, each remount receiving `Original` instead of `Keep after refused teardown`.

Retained the existing unsent label lifecycle on the existing `TrackLabelCapturePort`: an optional in-memory draft map holds raw value, dirty intent, original finish callback, capture refusal and submission error. The management hook exposes the same map through its existing start callback, so both hook and row may remount while the command owner survives. It does not capture on render/remount. The existing callback forwarding remains unchanged.

The component reads this owner-specific draft and mutates it on input/refusal. A clean finish or successful local session handoff releases it; the existing outbox still owns accepted handoffs and acknowledgement/retry. Successful display continues to show the typed name until track props update. Dirty means an input event occurred: typing away and back, explicit empty input, original guards, and ordinary clean sheet close keep their existing semantics. Input detachment retains the focused owner's finish closure, clears its focus marker first, and attempts finish once. A remount alone does not submit. A refused attempt retains the original capture and visible error for user retry. Capture refusal also survives teardown and never auto-recaptures.

Why this lifetime: a hook-local ref would still fail the review's remount of the hook with the same live port; a component ref disappears with the row. This is transient state on that existing port, not a durable store, journal, history, wire field or model. Another command port receives another map; the test switches the same row to another owner and back without redirecting its retained draft. Once the old session/port and consumers are released, its transient map is collectible. No disposal behavior, automatic new guard choice, request identity allocation, ACK handling or other product behavior was changed.

Product delta is **65 added / 47 removed lines (net +18)** across `trackLabelGesture.ts`, `useTimelineTrackManagement.ts`, and `TrackLabel.tsx`. The normal command test adds 16 cases (27 → 43) and adjusts only the setup to expose remount and an optional test port. Every original committed test body/assertion and the exact three reviewer test bodies remain byte-for-byte unchanged, verified by `notes/audit.py`. Entire task delta: four files, **190 added / 50 removed lines**. No expected-failure/skip/todo marker added.

## Evidence

Ran from `/home/user/work/wt/app-m3-root-label-refused-unmount-fix`. Exact common command prefix (shell variables only shorten repeated absolute paths):

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W="$O/workers/app-m3-root-label-refused-unmount-fix"
N="$W/notes"
```

Original-source reproduction, after adding the unchanged exact three expectations:

```sh
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx \
  --reporter=default > "$N/before.log" 2>&1
```

Exit 1: **27 passed / 3 failed**, 11.32 seconds; only the exact reviewer remount expectations failed.

Final-source targeted run:

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
  --reporter=default --reporter=json --outputFile.json="$N/targeted.json" \
  > "$N/targeted.log" 2>&1
```

Exit 0: **10 files / 416 passed / zero failed or skipped**, 50.36 seconds. Breakdown: label command 43, renderer 50, canvas 79, management 28, Ops label 24, gesture 8, native capture 73, commit session 72, command hook 15, projection 24. These are jsdom device-class tests, not physical-device/browser runs. A pre-existing act warning in the project-switch/Keep test appears in both initial and final runs; no failed test or unhandled exception.

The six added finish/submit-refusal retry cases verify the same original basis object, retained dirty name/error after remote change, no remount-triggered handoff, one explicit retry, and no second detach attempt after blur. The three capture-refusal cases prove no capture refresh. Three clean teardown cases prove the next intentional edit captures the new remote state. One owner-switch case proves draft isolation. The unchanged native session suite proves synchronous stale/remote refusal, exact unknown-ACK retry, restart/recovery identity, and that only explicit Keep after definitive rejection authors a new intent/key with fresh guards; ordinary retry does not mint a replacement request.

Focused recovery neighbors:

```sh
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/components/TimelineCommandRecovery.test.tsx \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  --reporter=default --reporter=json --outputFile.json="$N/recovery.json" \
  > "$N/recovery.log" 2>&1
```

Exit 0: **2 files / 41 passed / zero failed or skipped**, 2.90 seconds. Total final evidence: **457 passed across 12 files**.

Other exact checks:

```sh
node_modules/.bin/eslint src/tools/video-editor/commands/trackLabelGesture.ts src/tools/video-editor/hooks/useTimelineTrackManagement.ts src/tools/video-editor/components/TimelineEditor/TrackLabel.tsx src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx --max-warnings 0 > "$N/eslint.log" 2>&1
node scripts/quality/check-known-failures.mjs
node scripts/vendor-lock.mjs check runtime.lock.json
python3 -B "$N/audit.py"
git diff --check
```

All exit 0. ESLint has zero warnings/errors. Known-failures gate: 3 original authorized markers / 0 forbidden. Runtime lock check: `ok runtime.lock.json`. Audit verifies exact original source HEAD, exactly four changed tracked files, no nonignored untracked files, every original test body and exact3 unchanged, and all other tracked source unchanged. Thus Runtime13/public12/MAIN/proxy/pins/wrapper/seven journey bodies are unchanged from the reviewed starting root; those journeys and transport were not executed here. Main17 settings/add/delete neighbors pass in the renderer/canvas suites; shell no-Text source is unchanged.

An initial candidate run (`targeted-first.log/json`) had **400 passed / 3 failed**: its successful handoff displayed the remote label instead of retaining the explicit original-value choice. Corrected the component presentation state, preserved those existing test assertions, and reran the final 416-test invocation above. No failure was suppressed or expectation weakened.

## Environment and handoff

Only this worker's ignored node_modules symlink was redirected. Its private12 overlay borrows dependency entries read-only from `/tmp/app-coherent-deps12/node_modules` and privately extracts the repository's immutable public12 archive. The test config imports this worktree's normal config and changes only cacheDir to this worker's notes. Used config runner, no cache, one worker, no file parallelism, private TMPDIR. Shared node_modules/runtimes/venvs/caches were not modified. Private temporary/cache directories were removed after testing; no build/temp output is in the worktree. Retained private12 and notes for review.

No full suite, build, browser, socket/localhost service, install, project tsc, central suite request, real Runtime acceptance, owner-film, pixel/audio or macOS qualification was performed. The prior `927` typecheck applies only to that original tree. No new typecheck pass is claimed.

No blocker to handing off this implementation. Recommended manager follow-up: independently review this exact patch and retained exact3 tests; run scoped/full type qualification as appropriate; keep the actual paired gate **HOLD** until the fix is approved and the manager's required exact-tuple qualifications pass. Wrote design/report/commit-msg/DONE/KEEP. No commit, merge, checkout, push, ref change or integration-worktree edit.
