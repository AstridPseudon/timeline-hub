Implemented the bounded live-policy repair. Ready for the manager's independent final check; this report does not approve the actual UI release.

Base: App `cee68b807017efc8669c7d75318cf51aa70ec855`, tree `b2c510ca8893c4d3c238fb042f9ec7e7252edbc0`. Read PLAN and the root-refused-unmount final-review HOLD. No settled decision changed.

**Production reachability.** `editorRuntimeAssembly.tsx:650` calls `useTimelineState`; that hook unconditionally calls `useTimelineSave` at line 629 and `useTimelineTrackManagement` at line 945. `useTimelineSave.ts:99` calls `useTimelineCommandSession`. Management is a plain hook in this same component lifetime, not an independently keyed child. The only production management call is this one. A row/sheet remount therefore keeps management's existing live ref. A remount of the assembly/state component resets both hooks: the old command-session effect cleans up, clears sessionRef and disposes the session; the new hook starts with a null ref and creates a fresh session/port. Session initialization wraps trackLabelPort in a new object, scoped to the verified project/timeline. Provider/timeline/attempt changes also rebuild it through the existing effect. No production path preserving the exact port while remounting only management was found in this assembly. This is source evidence, not a browser proof or a newly exercised assembly fixture.

The counterexample is nevertheless real at the exported App hook boundary: a caller retaining the same live port can remount management. Replayed the review's lock probes byte-for-byte before changing source: desktop/phone/tablet each submitted a second time despite the new lock (3 failed, expected one submit, observed two). The task explicitly authorizes repairing this local lifetime; no orchestration decision was needed.

**Current gate versus original guards.** The existing command-owner port now has an optional runtime-only `localEditability` ref. Each management render binds its existing editability ref to that port. The retained original finish closure looks up the port's current ref when checking timeline/track editability. A remounted management instance therefore replaces the stale policy source. Continuously mounted management still reads its live ref, including the existing test with a replaced port wrapper. No capture or submission occurs during render. The same current gate runs before capture and before finish.

Only the local gate changes. The captured basis object, original track selection, value/identity expectations, reads, selections, bindings, base/local generation, created IDs, native finish and submit methods all remain original. No reauthoring, refreshed guard, request identity allocation, journal, DTO, global store, outbox/ACK change, extra submission or fallback writer. TrackLabel.tsx, trackLabelCapture.ts, commitSession.ts and useTimelineCommandSession.ts are unchanged. The port reference captured by each edit is unchanged; new project/session ports retain separate draft maps and transport owners. Policy binding follows the existing single-management-owner lifetime per port; concurrent distinct management owners sharing one port are not a supported production assembly and were not qualified.

Refusal leaves the same dirty input and capture intact. The prior error is visible on remount; an explicit denied retry displays the current local gate's reason while retaining the draft. A later unlocked explicit retry submits the identical original command once, and blur/unmount does not submit again. New normal tests cover track_locked, readOnly through check(), and whole-timeline checkTimeline refusal on all three devices, plus the original hook becoming locked before teardown and an unlocked remount succeeding.

**Diff / LOC.** Exactly three tracked files: two product files +5/-1 (net +4); one test file +81/-3 (net +78). `trackLabelGesture.ts` 60→63 lines; `useTimelineTrackManagement.ts` 1088→1089; `TrackLabel.command.test.tsx` 318→396. The existing helper accepts an optional editability argument; all prior 43 label test bodies/assertions remain byte-for-byte unchanged. Twelve new ordinary passing tests, no fails/skip/todo markers.

**Results.** Final targeted run: 12 files / 469 passed / 0 failed / 0 skipped, 63.59 seconds. Per-file counts: label 55, renderer 50, canvas 79, management 28, Ops label 24, gesture 8, capture 73, commit session 72, command hook 15, projection 24, recovery UI 14, outbox 27. The known project-switch/Keep act warning recurs; no unhandled exception or failed test. Earlier focused run passed 80 tests before adding the final three unlock regressions; final targeted evidence includes all edits.

Unchanged external diagnostics: root exact3 3 passed; new lock3 3 passed (previously 3 failed); private lifecycle 12 passed. The lifecycle probes cover independent same-ID owners, sibling tracks, original basis/command preservation after remote change, and one submission across blur/sheet-close/unmount. These use production hooks/rows/native capture and a stubbed final local handoff, not a Runtime ACK. Device evidence is jsdom props, not browser/device qualification.

Targeted ESLint passed with zero warnings. Vendor-lock check passed against pinned producer. Known-failures gate passed: 3 previously authorized markers / 0 forbidden. git diff --check passed.

Preservation audit passed: 5,831 other tracked paths retain exact HEAD bytes, including symlink text. MAIN17 renderer/canvas/shell/mobile inspector/sheet paths and track settings/add/delete behavior remain unchanged (renderer/canvas tests pass). Public12 package/lock/archive and normal013 generated/locked files equal approved pins; all 13 destinations match hashes plus pinned and current producer bytes. Archive SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; all 77 regular archive members equal the private installed public12. All four cold-label journey bodies/config, seven M1 journey bodies/helpers/configs, wrapper files and six server/proxy paths retain exact bytes. This is preservation evidence, not rerun browser/socket qualification.

**Exact commands.** From `/home/user/work/wt/app-m3-label-live-policy-remount-fix`:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
N="$O/workers/app-m3-label-live-policy-remount-fix/notes"

# Before source edit: 3 failed; after the product edit: 3 passed.
# Output names were lock-before.{json,log}, then lock-after.{json,log}.
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/lock-remount.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  "$N/lock-remount.review.test.tsx" --reporter=default --reporter=json \
  --outputFile.json="$N/lock-before.json" > "$N/lock-before.log" 2>&1

# Final normal suites: 469 passed.
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

# Final unchanged external probes: 3 + 3 + 12 passed.
for diagnostic in row-unmount lock-remount lifecycle
do
  env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
    node_modules/vitest/vitest.mjs run --config "$N/$diagnostic.config.ts" \
    --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
    "$N/$diagnostic.review.test.tsx" --reporter=default --reporter=json \
    --outputFile.json="$N/$diagnostic.json" > "$N/$diagnostic.log" 2>&1
  result=$?
  tail -n 9 "$N/$diagnostic.log"
  if [ "$result" -ne 0 ]; then exit "$result"; fi
done

node node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/commands/trackLabelGesture.ts \
  src/tools/video-editor/hooks/useTimelineTrackManagement.ts \
  src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx --max-warnings 0
python3 -B "$N/audit.py" > "$N/audit.json"
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
node scripts/quality/check-known-failures.mjs
git diff --check
```

Initial private probe setup failed module resolution before collecting tests; adding a node_modules symlink inside this worker's notes fixed fixture imports. The first audit retained the prior review's HEAD assumption; corrected it to this worker's cee68 base (which adds the retained cold journeys), then the audit passed. Neither required changing product/test expectations.

Only this worktree's ignored node_modules link was redirected. A private12 overlay lives in this worker's notes; borrowed dependency entries are read-only links and public12 was extracted privately from the immutable archive. No shared dependency/runtime/venv/cache file was changed. Config loader runner, --no-cache, private cacheDir/TMPDIR, and one worker per targeted run were used. Private transient TMP/cache folders were removed after testing; review fixtures, logs, audit and private dependency overlay are retained with KEEP. No build output or temporary source files remain in the worktree.

**Remaining approval and limits.** Manager independent final check after this code is still required. No full/build/browser/socket/install/project-tsc or central test request. No new actual Runtime acceptance/reload/undo, UI release gate, pixel/audio, owner-film or macOS evidence. No blocker to this bounded implementation task; no broader editing-engine work. Harness should commit, manager should review and qualify the final tree before integrating/releasing. report/commit-msg/DONE/KEEP written; no git commit/merge/checkout/push/ref operation or integration-worktree edit.
