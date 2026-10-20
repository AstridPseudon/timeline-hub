# Single-parent split production ingress — source stage

Base: `d1111fd3b05acac5c72f656cd62faae5e60466be` (`tl/app-m2-parent-split029-source-slice`). Assigned branch: `tl/app-m2-parent-split-production-ingress-stage`. Read PLAN and both required reviews first. No decision was changed.

## Result and boundaries

Existing selected-clip, context-menu time, and single-clip playhead hooks now reach the reviewed native split port. `useTimelineState` passes the port into `useClipEditing` with one added line. SDK `createTimelineCommands().splitClip` uses that same session and selects the reserved right clip. The mounted clean-save wrapper forwards the new routing predicate.

A read-only `supports` predicate routes only one literal raw parent row from the session's verified closure and an unambiguous current display binding. Unsupported shapes, pinned groups, multi-selection and occurrence displays retain their existing behavior. Authored `app.canonical` remains opaque. No display suffix is parsed into an identity. This predicate is a conservative ingress boundary; native validation still decides whether capture/finish succeeds.

The existing `createSplitClipId` seam reserves the right ID once before capture. Capture, finish and submit run synchronously with the original immutable basis; the shared session persists that exact command/created ID and request identity through unknown acknowledgements and explicit reload recovery. Duplicate UI calls observe the synchronously advanced draft and produce no second split. Capture/finish errors surface as an error toast or SDK mutation failure and retain the draft; their catch blocks never invoke the old writer.

Native `clipSplitCapture.ts` and the session split capture/finish/submit bodies are byte-identical to base. No native command, guard, inverse, compiler, provider, outbox, recovery protocol or UUID journal was added/replaced. The routing check deliberately precedes capture rather than trying native capture and catching into a snapshot write.

Atomic multi-clip splitting remains one existing config mutation. Generic TimelineOps patches, including compound flows and its reserved/deferred `clip.split` family, are untouched: TimelineOps has no executable split writer to migrate in this bounded task. Main 44f's split hook is identical to this base; inspected Ops/service removals remove older Timeline additions rather than supply replacement split ingress. Main mobile/root/render/bootstrap changes were not imported. The only root-hook edit is the port argument.

## Exact diff and allowlist

Against the assigned base: **9 files, +324/-34 (net +290)**. Product: **+108/-30 (net +78)**. Tests: **+216/-4 (net +212)**. The four test removals are harness setup/return lines replaced to mount actual editing and reuse IndexedDB; original assertions remain byte-identical. Existing sourceport's +516 product lines were already in the base and are not counted again.

```text
43	0	src/tools/video-editor/commands/clipSplitGesture.ts
14	1	src/tools/video-editor/commands/commitSession.ts
2	0	src/tools/video-editor/hooks/clip-editing/types.ts
28	29	src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts
4	0	src/tools/video-editor/hooks/useClipEditing.ts
216	4	src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx
1	0	src/tools/video-editor/hooks/useTimelineCommandSession.ts
15	0	src/tools/video-editor/hooks/useTimelineCommandsService.ts
1	0	src/tools/video-editor/hooks/useTimelineState.ts
```

These nine paths are the exact allowlist; no other tracked path changed. Native split capture/gesture/session suites, all original `useClipEditing.test.ts` group/multi assertions, and the original two mounted split test bodies are preserved. No skip, fails, todo or weakened assertion was added. Source comparison and `git diff --check` passed; details: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split-production-ingress-stage/notes/source-audit.log`.

## Verification

All runs used the existing read-only public12 dependency tree at `/tmp/app-coherent-deps12/node_modules` through this worktree's own symlink. Only that private symlink was changed; no shared dependency file/link/cache was edited. Runner supplies the existing config's `__dirname`. Vitest used runner loading, no cache and one worker. Original dependency symlink restored after verification; no build output or temporary files left in the worktree.

Final targeted command, executed in `/home/user/work/wt/app-m2-parent-split-production-ingress-stage`, **exit 0: 19 files / 725 tests passed** (56.34 seconds):

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split-production-ingress-stage/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipSplitCapture.test.ts src/tools/video-editor/commands/clipSplitGesture.test.ts src/tools/video-editor/commands/commitSession.split.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts src/tools/video-editor/commands/authoringBundle.sharedOpaqueRemap.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/lib/keyboard-delete.test.ts src/integrations/runtime/opaqueRootWriters.test.tsx src/tools/video-editor/lib/timeline-patch.test.ts
```

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split-production-ingress-stage/notes/targeted.log`.

Changed-file ESLint command, **exit 0**, no warnings/errors:

```sh
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/clipSplitGesture.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/hooks/clip-editing/types.ts src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts src/tools/video-editor/hooks/useClipEditing.ts src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useTimelineCommandsService.ts src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx --max-warnings 0
```

Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-split-production-ingress-stage/notes/lint.log`. `git diff --check` also exited 0.

Earlier targeted runs: the mounted ingress suite passed 10/10; then five split/editing suites passed 112/112. These were before final added controls and are superseded by the 725-test final run. Their logs are retained as `ingress-initial.log` and `targeted-initial.log`; neither failed. Initial and final changed-file lint passed.

Added production controls cover all three UI handlers, SDK facade, duplicate click, unchanged capture→finish basis, one reserved ID, exact unknown-ACK retry, explicit remount recovery without recapture, retained draft/error without alternate publication, opaque canonical metadata, successful legacy unsupported/text/animated/relational/transition/occurrence paths, group refusal, multi-clip success, and absent-port SDK success. Existing native session controls cover abandoned reserved capture without preview/request/persisted intent, identical duplicate finish, refused duplicate submit, changed preview rejection, persisted guarded suffix, and inverse request construction. Local `scheduleSave`, `saveTimeline` and `saveTimelineAtHead` spies stay silent for tested native ingress; this is unit evidence, not observed HTTP traffic.

## Not qualified / next steps

**Actual Runtime acceptance, actual browser reload, browser gesture behavior, zero legacy HTTP traffic, and writer retirement remain OPEN.** New mounted tests use real App hooks/session/IndexedDB with a provider test double; existing acceptance/inverse lifecycle uses an in-process fake native server. No real Runtime/Agent paired acceptance, browser/socket/localhost run, full suite, build, project tsc, install, renderer parity or film viewing was run/requested. Group/multi/occurrence/unsupported and atomic compound replacements remain unqualified and retain their established paths.

No blocker. Recommended next step: source-review/harness this bounded unit, compose narrowly with refreshed main and other session ports, then qualify the actual Runtime/browser tuple and observe legacy HTTP before any retirement claim. Shared dependencies stayed read-only; no commits, checkout, merge, rebase, pushes or refs were performed.
