**Recommendation: clear the production-UI reachability HOLD attributable to the three lock/remount failures.** They reproduce an independent-management-hook lifetime robustness defect, but that lifetime is not assembled by the current App. Keep the parallel fix and its independent review as a separate internal hook-contract follow-up. This is not overall UI/release approval, type qualification, or an M3 gate pass.

Reviewed App HEAD `cee68b807017efc8669c7d75318cf51aa70ec855`, tree `b2c510ca8893c4d3c238fb042f9ec7e7252edbc0`. Read PLAN first, then `design/app-root-refused-unmount-final-review.md`, the original unchanged lock-remount diagnostic, and the refused-row fix's design. No settled decision changed; no product or repository test edited. The parallel fix worker's changes are outside this review.

**Production call graph and ownership.** Paths below are relative to this App worktree.

1. `src/tools/video-editor/contexts/VideoEditorProvider.tsx:877–884`: `VideoEditorProvider` keys its instance by project identity, timeline, user and data-provider generation. Changing `timelineEditability` is an ordinary update, not part of that key. Its effective guard also incorporates the canonical-shot draft lock (`910–912`); runtime context forwards that guard (`1138`).
2. The instance renders `VideoEditorRuntimeProvider` around `InnerProvider` (`1142–1154`). `InnerProvider` calls `useEditorRuntimeSync` (`415`); `contexts/editorRuntimeAssembly.tsx:650` unconditionally calls `useTimelineState`.
3. In ONE React hook owner, `hooks/useTimelineState.ts:629` calls `useTimelineSave`, and `945–955` unconditionally calls `useTimelineTrackManagement`. The latter receives `runtime.timelineEditability` and `save.commands.trackLabelPort`. A descendant row cannot remount that hook independently. Search of production `src` found no second caller of management.
4. `hooks/useTimelineSave.ts:95–99` calls `useTimelineCommandSession` with provider, timeline, commit refs and the current legacy-clean predicate. `hooks/useTimelineCommandSession.ts:114` creates a native command session. At `161–170` it wraps that session's label port with the current legacy-clean predicate and stores the session in `sessionRef`. The returned port is `sessionRef.current?.trackLabelPort` (`240`), not a port supplied by an ancestor outside `useTimelineState`.
5. Command-session effect cleanup (`178–188`) marks its effect disposed, invalidates reads, clears `sessionRef`, and calls native `dispose()`. Effect dependencies include provider, timeline, enabled, initialization attempt and snapshot-write ref. Native `commands/commitSession.ts:490` sets `stopped = true` synchronously before draining/releasing storage asynchronously. All native label `capture`, `finish` and `submit` call `assertReady()` (`104`, `274–322`), which refuses stopped sessions. Late initialization also disposes its session instead of adopting it (`141–143`). A subsequent parent mount creates another session/port.
6. `hooks/useTimelineTrackManagement.ts:253–254` updates the SAME `editabilityRef.current` every render. Its start callback (`906–926`) captures authored basis once, but its finish closure calls `checkEditable()` again, reading that live ref. `components/TimelineEditor/TrackLabel.tsx:409–442` retains dirty value/error/finish in the port's draft map, while detachment (`458–464`) tries finish once. Row-only remount therefore reuses the original capture AND reads current policy. Management-plus-row remount with an externally retained live port instead preserves an obsolete ref: that is the failing diagnostic's construction.

A command-session effect restart can replace a port while management stays mounted; it cannot create the opposite lifetime. A full `useTimelineState`/`InnerProvider` remount replaces both hook instances and disposes the old session. Descendant canvas/row/sheet/device-layout remounts leave both hooks mounted. No current product path was found that remounts only management while retaining the same LIVE session port.

**Actual-parent exercise, not an invented port lifetime.** Reused the existing `useTimelineState.history-authority.test.tsx` fixture's imports, query/render mocks, provider/storage setup and `mounted` helper in the private `notes/parent.probe.test.tsx`. The actual `useTimelineState → useTimelineSave → useTimelineCommandSession → createTimelineCommandSession` and management code all run. The private raw-document seed explicitly labels V1 `Original` and recomputes its fixture digest. Actual `TrackLabelContent` is rendered with the mounted parent's real handlers and real label port. The only forced refusal is a one-shot spy throwing synchronously at that real port's submit handoff; capture/finish, subsequent submission, preview and provider commit are real implementations. No session factory, lifetime, cleanup or port is stubbed.

Nine probes pass, each on desktop/phone/tablet jsdom device props:

| Scenario | Observed |
| --- | --- |
| Row unmount after synchronous submit refusal; parent stays mounted; new track lock then read-only guard; unlock and retry | Same live port AND same start function across guard updates. Dirty value survives. Both new guards refuse before another native finish/submit. Unlock submits the exact original command using the identical original basis object, with capture called only once before handoff. One guarded provider commit, no snapshot save. Draft releases on successful handoff; touch sheet is explicitly closed. |
| Row unmount/refusal, remote label update, parent observes new canonical data, row remount and explicit retry | Same port, one capture, same original basis object on retry. Native finish refuses `Track label changed during the label edit`; no second submit, no provider commit, no snapshot fallback. Original dirty text/error remains. Current display data becoming remote does not refresh authored guards. |
| Full actual parent unmount/remount after row refusal | Immediately after parent unmount, stale port capture/finish/submit AND the retained finish callback all refuse. Storage ownership releases. Remounted actual parent receives a different real port and different empty draft map. Lock applies to a fresh edit; stale draft does not migrate into the new session. No commit. |

The last observation scopes the original feature: refused drafts are transient on a live port. These probes do not promise persistence of a pre-handoff draft through whole-parent destruction/reload. Accepted local handoffs have the existing outbox/recovery path; that separate behavior is covered in the targeted suites and was not changed here.

**Classification of the three old failures.** Copied `lock-remount.review.test.tsx` byte-for-byte from the prior reviewer; `cmp` passes. It still fails **3/3**, at the second-submit assertion: expected one submit, observed two. This is valid evidence that retaining a finish closure across independently remounted management hooks retains old policy. It is not evidence of a current production UI or Runtime authorization bypass. In that fixture the port is an externally owned object and `submit` is a stub; its lifetime is explicitly longer than the hook it supplies. The current App owns the session in that hook's same parent.

The refused-row implementation design explicitly claimed that “both hook and row may remount while the command owner survives.” That broader internal composition promise is real enough to justify the parallel robustness fix; do not dismiss the failing expectations or rewrite them as successful refusal being unsupported. However, `src/sdk/index.ts` defines the public SDK boundary as excluding internal mutation/runtime APIs; searches of `src/sdk` found no export/reference for `useTimelineTrackManagement`, `TrackLabelCapturePort` or `TrackLabelEditStart`. I found no supported PUBLIC SDK ingress that independently owns this port. Thus: demonstrated internal composition-contract gap; no demonstrated public SDK regression; impossible lifetime in the current inspected product assembly. Source-level custom hosts that import internals could construct it, but none was established here. No owner permission decision is needed to describe or fix that local robustness gap.

**Exact evidence.** All commands ran from `/home/user/work/wt/app-m3-label-remount-production-reachability`. Abbreviations:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W="$O/workers/app-m3-label-remount-production-reachability"
N="$W/notes"
```

Actual-parent probes: exit 0, **9 passed / 0 failed / 0 skipped**, 13.05 seconds:

```sh
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  --reporter=default --reporter=json --outputFile.json="$N/parent.json" \
  > "$N/parent.log" 2>&1
```

Unchanged previous split-hook diagnostic: exit 1, **3 failed / 0 skipped**, 4.58 seconds, no expected-failure markers:

```sh
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/lock-remount.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  --reporter=default --reporter=json --outputFile.json="$N/lock-remount.json" \
  > "$N/lock-remount.log" 2>&1
```

Existing repository suites: exit 0, **4 files / 97 passed / 0 failed / 0 skipped**, 31.35 seconds. Breakdown: parent history authority 11, command-session hook 15, management 28, label command 43.

```sh
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/targeted.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts \
  src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx \
  --reporter=default --reporter=json --outputFile.json="$N/targeted.json" \
  > "$N/targeted.log" 2>&1
```

Targeted logs include React act warnings in the existing session tests and intentional invalid-fixture config warnings in the existing history tests; no failed test or unhandled exception. Initial private fixture attempts: dependency resolution first needed a worker-local node_modules link; the first collected run had seven setup/assertion failures because the raw fixture had an absent label; after adding the explicit fixture label, two touch-only assertions still found a later open-sheet draft after async handoff. The final probe retains the immediate AND eventual empty-draft assertions and explicitly closes the touch sheet after successful blur, so a subsequent open-sheet focus cycle is outside the measured handoff. Initial collected logs are retained as `parent.first-collected.log` and `parent.second-collected.log`. No repository expectation was edited, weakened, skipped, or converted to expected failure.

Additional checks all exit 0:

```sh
cmp "$N/lock-remount.review.test.tsx" \
  "$O/workers/app-m3-root-refused-unmount-final-review/notes/lock-remount.review.test.tsx"
git diff --check
git diff --exit-code
git diff --cached --exit-code
git ls-files --others --exclude-standard
sha256sum vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz
```

No tracked/staged/nonignored untracked App changes. Public12 archive SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; all **77** regular archive members match the worker-private extracted package byte-for-byte (`notes/summary.json`). Node 22.22.0; Vitest 4.1.5 from the read-only coherent dependency set. Only this worktree's ignored node_modules link was redirected to its own private12 overlay. Other dependencies are read-only links to `/tmp/app-coherent-deps12/node_modules`. Worker-local configuration uses a private cacheDir, `--configLoader=runner`, `--no-cache`, private TMPDIR and one worker. Private tmp/cache directories removed after testing; no shared dependency/cache writes, install or build. Private fixtures/configs/logs/package retained outside the worktree for review.

**Limits and next steps.** This exercises the actual parent HOOK assembly, not the full outer `VideoEditorProvider`/shell/browser tree. Query delivery and render-state hooks are controlled exactly as in the existing parent suite; IndexedDB and navigator locks are fake fixtures; the real RuntimeDataProvider talks to its in-memory guarded transport, with no actual Runtime process/socket. Device coverage is jsdom props, not hardware. No browser, socket/localhost, build, full suite, central request, tsc, install, pixel/audio, owner-film or macOS qualification ran. No claim that the parallel fix is correct or qualified.

Proceed with independently reviewing the parallel hook-lifetime robustness fix without asking the owner for local implementation permission. Keep all original success expectations and captured value/identity guards; do not recapture on remount to solve policy freshness. For the current source, the three diagnostic failures alone should not block the actual App UI gate: production row-only current-policy behavior is proven and whole-parent cleanup invalidates stale ports. Any broader release HOLD for unrun type/browser/journey qualification remains unchanged. Task complete, no implementation blocker; wrote this report plus worker report/commit-msg/DONE, no KEEP.
