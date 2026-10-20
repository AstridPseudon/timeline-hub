# MAIN17 Root013 final root review

**Verdict: HOLD — refused drafts are lost on whole-row unmount.** The requested existing track tests and package/pin/source checks pass. Ordinary touch-sheet close retains a refused draft correctly. The uncovered combination is a dirty focused row being unmounted, its finish being refused, then the same row being mounted again. No production or repository test edits were made.

## Reviewed source and reused approvals

- App HEAD: `927545cf52fdfbb273afbe7f190e00e11e5e2d70`.
- App tree: `96605f2a46c49fcf96cd12ca3679014f00ae28de`.
- MAIN17 integration base: `751f7703d22f0e8026e2926f93f64d69c65212fd`.
- Approved normal013 root: `171a259acbeb3ced855ca8f72fed0943a2f5a5cb`.
- Approved wrapper root: `cee35da4b1ed653db50dd9d5c26693fab00f04ad`.

Read the latest PLAN, repository CLAUDE.md, `app-main17-root013-label-port.md` and its worker report, `app-label-explicit-intent-final-review.md`, `app-runtime013-pin-independent-review.md`, and `app-current013-wrapper-final-review.md`. Design paths are under ORCH. Reused their bounded approvals rather than rerunning 1,165 tests or reviewing all prior product work. No settled decision is disputed or changed.

## Blocking finding

**P1: synchronous refusal during whole-row teardown silently discards the typed name and original capture.**

In `src/tools/video-editor/components/TimelineEditor/TrackLabel.tsx:459`, the input ref callback calls `finishNameEditRef.current()` when the focused input detaches. At lines 438–447, a refused finish is caught and reported only through `setNameError`. The draft, error and original finish callback all belong to `TrackLabelContent` state/refs (407–414). When the whole component unmounts, none survives and the error has no surviving display. Remounting the same track therefore shows the old committed label, with no recoverable typed value or original capture.

Independent reproduction used the existing `TrackLabel.command.test.tsx` setup: actual `TrackLabelContent`, actual `useTimelineTrackManagement`, and real `captureTrackLabel`/`finishTrackLabel`; only the final session handoff rejects synchronously, as in the existing refusal tests. It focuses the input, types `Keep after refused teardown`, unmounts without blur, verifies one submit attempt and no fallback `applyEdit`, then remounts the same component with the same track/data/port. The desired draft-retention assertion fails on **desktop, phone and tablet**: expected the typed value, received `Original`. This is a private diagnostic reproduction, not a failure claimed in the committed main suites or a real Runtime rejection test.

Synchronous refusal is a real supported boundary: `useTimelineCommandSession.ts:163–168` can refuse while earlier legacy saves remain; `commitSession.ts:289–299` can refuse stale generation/read guards before enqueue. The existing successful-unmount test proves one submission attempt only; it does not cover refusal during teardown. Existing sheet-close refusal tests keep `TrackLabelContent` mounted, so their passing result does not cover this finding.

Recommended next step: orchestrator assigns a bounded fix that preserves the refused draft and original authority across row teardown, or prevents the teardown until that refusal is handled. Keep the existing successful-unmount, blur/close, explicit-value and guard assertions. Add the refused-unmount case to the normal suite and obtain a fresh focused review. This reviewer made no architecture choice or product change.

## Passing bounded review

- Desktop and MAIN17 phone/tablet Name inputs share the capture/draft lifecycle. Focus captures before typing; later track labels and callback props do not replace that finish callback. Typing away and back remains explicit intent because `dirty` records input events. Empty input remains `{values:{label:''},clear:[]}`. The mounted native tests assert the original `Original` expectation, opaque-field preservation and no fallback writer.
- While the row survives, capture and submit refusals retain the draft and visible reason. Submit retries use the original capture/command. Ordinary blur clears the focused flag before close/ref detachment, so blur plus close submits once, including refusal. Closing a focused sheet without blur also finishes once. Clean close releases capture, allowing the next edit to capture the new raw state. Successful focused whole-row unmount submits once. The blocking finding is specifically the refused whole-row case.
- MAIN17's real TrackSheet, shared settings, add audio/video and confirmed delete remain. Original MAIN17 TrackListRenderer tests are a literal unchanged prefix of the final test file. `onAddTrack` and `onTrackLabelEditStart` both survive Canvas/renderer/row forwarding and memo comparison. The four MAIN17 paths outside the manual reconciliation set are exact base bytes: shell source/test, mobile inspector and mobile-sheet constant. This preserves the no-Text shell and tap-to-release Move/Trim source; those shell/move suites were not rerun here.
- Independent Git-tree audit verifies exactly **172 changed paths** from base: the approved **171-path** delta plus `TrackLabel.command.test.tsx`. Across **5,921 nonmanual path identities**, each path equals the approved bytes where that delta changes it and the current base otherwise. Manually reviewed the five reconciled files: TrackLabel, TrackListRenderer source/test and Canvas source/test.
- Of the six server proxy paths, five equal both current base and reviewed `35820a603`. The Vite config equals the clean three-way combination of the current server proxy and approved package-alias cleanup. No server admission/transport change was introduced by this composition. No socket/proxy suite was run.
- `runtime.lock.json`, all three normal generated files, package manifest/lock and public12 archive equal reviewed `171a259a` exactly. All **13** locked destinations equal producer working bytes, committed bytes and lock hashes. Producer HEAD/tree are `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `7ab412cc4bcbe517efcfa806e092336390312e18`; producer stayed clean. Contract remains `workspace.v1` / `0.2.13`, schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.
- Public12 archive SHA256 is `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. All **77** unique safe regular members equal the private installed package. Resolver tests pass for public exports and shared peers, including React 18.3.1 and Remotion 4.0.509.
- Both wrapper files equal approved `cee35da4`. All **seven complete journey bodies**, their reviewed app/Agent helpers and Playwright configs are byte-equal to that approved root. Provider parity and native label capture/gesture source are also exact approved bytes. These are preservation checks, not executed journey evidence.
- `useClipDrag.test.tsx` equals base byte-for-byte. Only its **three original authorized expected-failure markers** remain; no changed repository test adds fails/skip/todo markers. No existing test was weakened, skipped or rewritten to expect lost behavior.

## Exact commands and results

Commands ran from `/home/user/work/wt/app-m3-main17-root013-final-review`. Variables below:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
N="$O/workers/app-m3-main17-root013-final-review/notes"
```

One requested targeted main-suite invocation:

```sh
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx \
  src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx \
  src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx \
  --reporter=default --reporter=json --outputFile.json="$N/targeted.json" \
  > "$N/targeted.log" 2>&1
```

**Exit 0: 3 files, 156 passed, zero failed/skipped**, 28.43 seconds: production rename 27, TrackListRenderer 50, Canvas 79. These exercise the actual desktop input and actual MAIN17 touch sheet with phone/tablet device props in jsdom; they are not real-device/browser qualification.

```sh
env TMPDIR="$N/tmp" node --test --experimental-test-isolation=none \
  config/vite/timelineCompositionPackage.test.mjs > "$N/package.log" 2>&1
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
node scripts/vendor-lock.mjs check runtime.lock.json
node scripts/quality/check-known-failures.mjs
python3 -B "$N/audit.py" > "$N/audit.json"
git diff --check
git diff --exit-code
git diff --cached --exit-code
git ls-files --others --exclude-standard
git status --porcelain=v1 --untracked-files=all
```

All exit 0. Package tests **9/9 passed** with no skips; both vendor checks pass; quality gate reports **3 authorized / 0 forbidden**; source/pin/package audit passes. Tracked, staged and nonignored untracked source lists remain empty.

The new source concern justified one additional private diagnostic invocation:

```sh
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/unmount.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  "$N/row-unmount.review.test.tsx" \
  --reporter=default --reporter=json --outputFile.json="$N/unmount.json" \
  > "$N/unmount.log" 2>&1
```

**Exit 1: all 3 draft-retention assertions fail**, one per device class, 5.14 seconds. Assertions expect retained behavior; no failure marker suppresses them. The first launch of this same command had no collected tests because the external fixture could not resolve `@testing-library/react`. Its log/JSON are retained as `unmount-initial.*`. Adding only `notes/node_modules -> ../private12/node_modules` fixed the fixture resolution; the unchanged assertions then reached the product behavior and failed as described. No shared dependency was modified.

Configs, audit, private reproduction and all result logs/JSON remain in this worker's notes. The review config imports the repository config with only a private cacheDir override; the diagnostic config additionally includes the external fixture. The fixture reuses the existing setup, changing the local TrackLabel import to its equivalent absolute alias and exposing the same Track component for remount. The snapshot preload supplies config-loader `__dirname`; it does not mock product behavior.

## Boundaries and handoff

Only the assigned worktree's ignored node_modules symlink was redirected. This worker created its own `private12/node_modules`, borrowed other packages by read-only symlinks from `/tmp/app-coherent-deps12/node_modules`, and privately extracted the immutable public12 package. Shared node_modules, caches, venvs and runtimes were not written. Runner loading, no-cache flags, private cacheDir/TMPDIR and one worker were used. Private temporary/cache directories were cleaned; no build or temporary output remains in the repository.

No full suite, build, browser, localhost/socket, install, project tsc, central test request, real Runtime acceptance/reload/undo, pixel/audio parity, owner-film or macOS run occurred. No wrapper rerun, new Agent-pair acceptance or broader M3 completion is claimed. Previously documented exact-pair/cap/owner qualifications remain outside this review.

Review work is complete; source integration approval is held for the refused whole-row teardown case. Wrote this design report, worker report, conventional commit message and DONE; no KEEP. No production edits, commits, merge requests, pushes or ref changes.
