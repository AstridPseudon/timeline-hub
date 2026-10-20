# Final live-policy review and project typecheck

**APPROVE** the final local implementation for the actual final-tree browser gate. **Project tsc PASS: one invocation, exit 0, zero diagnostics.** No implementation HOLD remains and no owner decision is deferred. Actual final browser/cross-product acceptance is **UNRUN**, not implied by this approval.

Read PLAN first, repository CLAUDE.md, `app-label-live-policy-remount-fix.md`, `app-label-remount-production-reachability.md`, `app-root-refused-unmount-final-review.md`, the original MAIN17 HOLD, and the historical cold-composition typecheck report. No settled decision changed. No production, repository test, configuration or tracked file was edited.

## Exact source and pins

| Input | Commit | Tree |
| --- | --- | --- |
| Final App reviewed and typechecked | `b1ef4b9b910ba72375c34cf319692f90d22edc25` | `8d8a10b057ed31fed69517e18a23b8ec3811447a` |
| Immediate comparison base, cold4 included | `cee68b807017efc8669c7d75318cf51aa70ec855` | `b2c510ca8893c4d3c238fb042f9ec7e7252edbc0` |
| Agent keeper | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` | `75354d38c898729bac09619679f5421faba319ed` |
| Runtime/producer keeper | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |

Keepers are `/home/user/work/wt/app-m3-agent013-current-pair-source` and `/home/user/work/wt/app-m3-runtime013-producer-source`; both clean, all tracked bytes checked. MAIN17 `17e46de99b7cef52fe494de1703a9865a8d4be24` is an ancestor. The prior b2 type pass is historical only; this report checks the changed final product.

Normal contract remains workspace.v1 / 0.2.13, producer artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, timeline schema `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`. All 13 App and 15 Agent locked destinations match hashes and producer bytes; Runtime manifest has 75 artifacts. App lock SHA256 `550de9dc3269380c79f44a6db4c87a5d5459058d550ae49e635a6dda809e76a2`. Full pin digests are in `notes/pins-before.json` and identical `pins-after.json`.

Public Composition 0.0.12 archive SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`: package/lock/integrity unchanged, all 77 safe regular members match the private installed package and Agent archive.

## Independent review

Delta versus cee68 is exactly three files: `commands/trackLabelGesture.ts` +3/-0, `hooks/useTimelineTrackManagement.ts` +2/-1, and `components/TimelineEditor/TrackLabel.command.test.tsx` +81/-3. Product net +4; test net +78. All original 43 row test bodies/assertions remain unchanged, with twelve ordinary passing tests added. No lost behavior expectation, fails/skip/todo marker, guard or fixture was weakened.

Each management render binds its existing editability ref to the same command-owner port. A retained finish callback consults that port's current policy ref, checking both checkTimeline and the track check before native finish/submission. The same check also precedes initial capture. Thus the independently remounted management-hook construction now honors lock/readOnly/canonical-shot draft refusal and unlock, while continuously mounted hooks retain the live-ref behavior.

Only local policy freshness changes. The original frozen capture, raw target ID, value-presence/identity expectations, reads, selections, bindings, created IDs, parent pin, local generation/basis, native finish/submit and transport owner remain unchanged. Denied retry runs before native finish or submit, preserving dirty raw text, error and capture. Unlock retries the identical original basis and command. No recapture, guard refresh, second journal, new request identity, global authority, cross-owner draft migration, fallback writer or ACK/outbox change was added. Native stale-generation/read checks and stopped-session refusal remain authoritative.

The port-scoped map and policy stay within the existing session lifetime. Separate same-ID owners have separate maps, captures and errors; accepting one does not clear another. Production has one management owner per port: `useTimelineState` owns both useTimelineSave and useTimelineTrackManagement; useTimelineCommandSession creates a fresh wrapped port per session and disposes old sessions during parent/provider/timeline changes. The earlier actual-parent nine probes are reviewed historical reachability evidence, not newly executed here. They distinguish row-only remount from whole-parent destruction. The old three lock failures were a real internal-composition robustness gap, not an established actual-App UI lifetime; the final fix now handles that construction too. Concurrent distinct management owners with different policies sharing one port are outside this production assembly; this task does not invent that authority model.

The two earlier HOLD findings are cleared for this source: unchanged exact3 proves refused row teardown retention, and unchanged lock3 proves current-policy refusal under hook remount. Lifecycle12 covers same-ID owner isolation, sibling tracks, original basis/command after remote change, and one handoff across blur/sheet-close/unmount. These probes use real row/hook/native capture code with the final local handoff stubbed; they do not claim Runtime ACK/acceptance.

All 5,834 tracked paths retain exact HEAD bytes/modes/symlink text after testing. All 5,831 paths outside the fix delta equal cee68. MAIN17 canvas/renderer/settings/add/delete/shell/mobile-sheet source is preserved, as are cold4 complete bodies (42+46+25+36 = 149 expectations), all seven complete M1/Gate-5 cases/helpers/configs, both wrapper files, all six server/proxy paths, normal13, public12 and source/producer guards. Native capture, commit session and command-session source are unchanged. This is preservation evidence, not fresh broad-suite or browser qualification.

## Exact commands and results

Commands ran from `/home/user/work/wt/app-m3-final-live-policy-review-typecheck`. Abbreviations:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W="$O/workers/app-m3-final-live-policy-review-typecheck"
N="$W/notes"
```

Unchanged private fixtures copied byte-for-byte from the fix worker; audits also compare exact3/lock3 against earlier independent reviewers. Configs import THIS worktree's normal Vitest config, select only those fixtures and set private cacheDir. Every command exited 0:

```sh
for diagnostic in row-unmount lifecycle lock-remount; do
  env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
    node_modules/vitest/vitest.mjs run --config "$N/$diagnostic.config.ts" \
    --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
    "$N/$diagnostic.review.test.tsx" --reporter=default --reporter=json \
    --outputFile.json="$N/$diagnostic.json" > "$N/$diagnostic.log" 2>&1
done

env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx \
  --reporter=default --reporter=json --outputFile.json="$N/normal-row.json" \
  > "$N/normal-row.log" 2>&1
```

| Run | Passed | Failed/skipped | Duration |
| --- | ---: | ---: | ---: |
| Original exact3 | 3 | 0/0 | 6.80s |
| Lifecycle | 12 | 0/0 | 10.90s |
| Lock/remount | 3 | 0/0 | 5.20s |
| Normal row: original43 + new12 | 55 | 0/0 | 20.94s |

Total **73 passed**. Did not rerun the broader 469 controls. jsdom desktop/phone/tablet props are not device/browser qualification.

Additional commands, all exit 0:

```sh
python3 -B "$N/audit.py" > "$N/audit-before.json"
python3 -B "$N/pins.py" > "$N/pins-before.json"
node "$N/preserve-sources.cjs" > "$N/preservation-before.json"
node --experimental-import-meta-resolve "$N/dependencies.mjs" > "$N/dependencies-before.json"
python3 -B "$N/dependency-content.py" > "$N/dependency-content-before.json"
python3 -B "$N/tracked-state.py" > "$N/tracked-state-before.json"
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /home/user/work/wt/app-m3-agent013-current-pair-source/scripts/vendor_lock.py check /home/user/work/wt/app-m3-agent013-current-pair-source/runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
node scripts/quality/check-known-failures.mjs
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/trackLabelGesture.ts src/tools/video-editor/hooks/useTimelineTrackManagement.ts src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx --no-cache --max-warnings 0
git merge-base --is-ancestor 17e46de99b7cef52fe494de1703a9865a8d4be24 HEAD
git diff --check cee68b807 HEAD
sha256sum /opt/pw-browsers/chromium-1194/chrome-linux/chrome
```

Lint zero diagnostics. Known-failures gate: 3 previously authorized markers, zero forbidden. Repeated pins/preservation/dependencies/dependency-content/tracked-state after tsc and compared each JSON pair with `cmp`: all exit 0. Scripts and complete logs/JSON retained in worker notes. All tracked source is byte-exact to the reviewed commit; source identity SHA256 `2d4aa9404bffde642123cf128637a8df6790973e8c90253461463e210fb219b0`.

## Single actual project TypeScript check

Executed once via `bash "$N/run-tsc.sh"`, which refuses a duplicate invocation. Exact child command:

```sh
env npm_config_cache="$N/npm-cache" npm_config_offline=true npm_config_update_notifier=false \
  flock -w600 /home/user/work/.app-tsc.lock \
  env NODE_OPTIONS=--max-old-space-size=4096 \
  npm exec tsc -- --noEmit -p tsconfig.app.json \
  > "$N/tsc-diagnostics.txt" 2>&1
```

Start **2026-10-20T13:15:38Z**, end **13:16:29Z**, elapsed **51 seconds** including lock/npm overhead. **Exit 0; combined diagnostics 0 bytes / 0 lines.** Complete timestamps/exit/diagnostics retained in notes. No rerun, suppression or compiler/config/product adjustment. Used actual strict `tsconfig.app.json` including src, its existing test exclusions and skipLibCheck; did not substitute the empty-root tsconfig.

Worker-private12 overlay uses read-only links to `/tmp/app-coherent-deps12/node_modules`; Composition alone was extracted privately from the immutable public12 archive. No shared dependency/cache/venv/runtime entry was written. Node 22.22.0, npm 10.9.4, TypeScript 5.9.3, Vitest 4.1.5. Compiler `/tmp/app-coherent-deps12/node_modules/typescript/bin/tsc`, SHA256 `8d5fa5bd883fec0979fc2004f1fe1d99aef40570155d550eadc0b03b55513bf0`. App and Composition resolve identical React/ReactDOM 18.3.1, Remotion/Player/Media/Layout Utils/Three 4.0.509 and Three 0.185.1 peers. Full paths and ambient versions are in dependency JSON.

Reachable dependency content/mode/link snapshots before and after compare equal: **32,509 unique files / 452,551,865 bytes / 464 symlinks**, SHA256 `000c2fce8d72665068669e146590e5da4b6452b5219dfcb7247471c53d91190d`. Snapshot includes the private links and their borrowed targets. Private TMPDIR/cacheDir, config runner and --no-cache kept tools away from shared caches.

## Handoff and limits

**APPROVE + tsc PASS applies to b1ef4b9b/tree8d8a for the actual final browser gate.** Bind that gate/cache identity to this App tree and the exact Agent/Runtime pair above, preserving current source/producer/public12 preflights before and after. Rebind stale executor tree/browser expectations; do not reuse a b2 gate result. Use the existing editing Chromium `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, SHA256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95` (hashed, not launched). Cold-open must run in its own fresh Playwright process with `--grep 'M2 cold-open'`; the other three label cases need a separate `--grep-invert 'M2 cold-open'` process. M1/Gate-5 remains separately required. No local implementation owner decision remains.

Actual final browser/cross-product gate is **UNRUN** here. No full suite, central test request, build, install, browser, localhost/live socket, actual Runtime acceptance/reload/undo, frame/audio parity, owner-film or macOS qualification. No new outer VideoEditorProvider browser assembly proof; prior actual-parent9 results are historical and explicitly scoped. No task blocker.

Restored only this worktree's ignored node_modules symlink to `/home/user/work/app/node_modules`. Removed private dependency overlay and transient transformation/Vite/npm/temp caches; no build output or temporary source remains in the worktree. No shared dependency tree was changed. Local design report is ignored by existing repository policy; identical report copies are saved in ORCH/design and worker report.md. commit-msg and DONE supplied; no KEEP/BLOCKED. No git commit/merge/checkout/push/ref operation or integration-worktree edit.
