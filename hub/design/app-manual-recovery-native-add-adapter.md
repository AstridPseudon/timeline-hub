# Manual recovery native ADD adapter — source staging

Base: `bcd610db8e530454da7029e0479fe81e52bbd156`. Source work complete; **production activation, actual App/Agent/Runtime pair and writer-retirement gates remain OPEN**. No integration worktree, package/pin/generated source, automatic producer, proxy, or legacy writer changed.

## Delivered binding

`createRuntimeRecoveryPlacement({client, getBinding})` is the actual optional `RuntimeRecoveryChooser.onRequestPlacement` callback implementation. It accepts the existing frozen selected project/timeline/head, raw occurrence/shot/internal revision/parent lane/child track and original five-field media selection. Its stable local binding contains the already-open `TimelineCommandSession` and the **same client object** used for task/output/selection/head/identity/VerifiedMedia reads. Mismatched client, scope, actor/realm, replaced binding, stale head/publication, changed source, missing/ambiguous raw bindings and cancellation refuse with the draft retained.

The session adds only `scope` and `addOccurrenceMedia`. It requires an idle owner, exact displayed/known head pair, original accepted canonical document and equal reconstructed authoring bundle. After the asynchronous conversion it checks chooser lifetime again. It captures the native command and appends through the existing enqueue/persist/pump/outbox path with no optimistic preview. The original command includes all native reads, selections, bindings, expectations, authorship and reserved IDs. The adapter reserves the child ID once per unchanged choice, preserves the selection alias, and never recaptures a submitted choice. An uncertain request stays in the existing owner's outbox; explicit owner Retry/recovery reuses its exact body/key/IDs. The callback adds no second queue, automatic recovery/claim, coordinator, task producer guard, accepted receipt store or Placed state.

Chooser edits and unmount now abort the callback's signal before capture. A command already durably captured remains the command owner's responsibility; aborting UI lifetime does not pretend to cancel an accepted server edit. Source/gallery data and the unknown-old-intent **Placement unconfirmed** versus readable-retirement **Not placed** distinction are unchanged.

## Old actual manual semantics and explicit proposal

Traced `TasksPane -> useShotActions.handleAddToShot -> useAddImageToShot/runAddImageMutation -> placeGeneration -> placeGenerationInDocument`, on this exact base:

- `useShotActions.ts:56` uses the selected lightbox shot, then current/last-affected shot; its placed-state display is optimistic. It supplies a generation ID and no timeline frame.
- `placementService.ts:172` resolves that generation's primary media via `resolveGenerationAsset`, resolves a default/first project timeline, and performs the legacy snapshot CAS cycle. Display URLs are not immutable source pins.
- `documentPlacement.ts:223` replaces the existing shot/generation pair, appends after the group's last clip when frame is absent (or nudges explicit frames past occupied starts), and uses a **four-second hold**. A null frame pools membership. The authored row uses `source_uuid`, which native occurrence ADD refuses. This flow supplies no raw occurrence binding, explicit source window, speed, transcript/word anchor, or parent-to-child conversion.

Those legacy defaults are not imported. The approved chooser already supplies three initially blank explicit second values. This source proposal interprets its “Timeline start” as parent timeline seconds: `child.at = on - explicit occurrence start_ms/1000`; `hold = to - from`. Video retains explicit `[from,to)` and native default rate 1, with no frame rounding. Image requires `from=0`, uses the explicitly entered interval as its hold, and emits no source-window fields. No four-second duration, source endpoint, append/collision placement, pool, shared write, default track/timeline, anchor or latest/primary media is inferred. **These new explicit chooser semantics are not claimed as parity with the old append action; the image labels/time-coordinate presentation still need actual-surface qualification before activation.** Unsupported native maps, ownership, timing, media/window/track/registry shapes refuse visibly.

## Native source and goldens

Retained App source: `938e454b5`, occurrenceMediaCapture/Primitives and their tests. Only those recipe files and tests were carried; no stage root/session/hook/proxy/pin cohort was imported. Current Agent was frozen once at **`cf7448ed6c1298b172d004914cfe2bb8c99048e7`**, archived privately, and executed unmodified with the dependency-only shared venv. Its native occurrence-media source SHA256 was `6f52844135592eb081ff8fb37377b985a1998e6b0df64fc632d01187b7e1dea6`.

The old stage failed authoritative current replay because current ADD records `placement.owners`, absent/present pool and legacy group reads, and child membership earlier. Ported just those native recorder changes (15 product lines); no consumed-clip/automatic producer support was added. The original current compact fixture SHA256 is `cf9650d82a3171236dd72a14ca1df2fabee8184edbef63d2020f5eeebcc15d69`. The Agent's unmodified official `fixture_loader.py` expands it for existing TS tests; expanded fixture SHA256 is `c4f4e65d27e367c0811cbe57e4ea39abccb7bf0faad48df651db364595ec6abc`. Both ADD and SWAP retain identical original input, verified media and authored output versus the retained App fixture. Full command/record claims are compared, not a manufactured guard table. Own-key cases were regenerated only by unmodified native capture/execute/replay/inverse; SHA256 `522ba04be6c34a9c7dff607b8b593f33fb1b43e2856665e4a471304f4a798b54`.

## Allowlist and size

13 repository paths: **+5063/-6, net +5057 lines**. Product: six paths, **net +475**, including 345 carried recipe/primitive lines and 130 net adapter/session/chooser lines. Tests: five paths, net +683. Native fixtures: two paths, +3899 (one own-key fixture is compact JSON). No lint/debt allowlist entry was added or changed.

Only the new session ingress can produce `occurrence.add-media@1`, with `intent:{ownership:'occurrence'}` and exactly `args:{row,media}`. The retained pure helper still contains SWAP for its unchanged parity tests, but the new manual adapter/session exposes no SWAP, parent ADD, consumed-clip or automatic placement route. Read calls are existing task, managed-output, immutable media-selection, current timeline, recoverable identity and official VerifiedMedia operations. Only the existing session/provider performs the normal commit. No legacy writer follows capture.

Product paths:
- `src/features/tasks/components/TasksPane/utils/runtimeRecoveryPlacement.ts`
- `src/features/tasks/components/TasksPane/utils/runtimeRecoveryDestinations.ts` (read-helper capability type only)
- `src/features/tasks/components/TasksPane/RuntimeRecoveryChooser.tsx` (cancellation only)
- `src/tools/video-editor/commands/commitSession.ts` (additive ingress only)
- `src/tools/video-editor/commands/occurrenceMediaCapture.ts`
- `src/tools/video-editor/commands/occurrenceMediaPrimitives.ts`

## Missing activation seams / evidence boundary

1. This base's generated WorkspaceClient and AstridRuntimeClient wrapper do **not** expose the official VerifiedMedia method. The new structural local capability describes the published method; it does not hand-edit generation, invent HTTP transport or instantiate a second client. A coordinated normal client/pin adoption plus same-client wrapper is required. `0132c4` from the brief resolves in neither available Runtime object store. Observed Runtime source `57d0f325da5af8794d9b63a418f42d3153d37337` includes native ADD and `getProjectVerifiedMedia(projectId, selection)` using the required five fields at the normal `/media-selection/verified` read. That observation does **not** verify the missing exact published ref or release pairing.
2. `useTimelineCommandSession` retains its actual session privately; TasksPane has no production binding that supplies it and its bound authenticated client. TasksPane therefore still passes no callback. The concrete proposed wiring is to create the callback with the existing stable `{client, session}` binding and pass it through the existing optional chooser prop, invalidating the binding when that actual owner closes. This worker adds no parallel context/global coordinator.
3. Outside an active editor, this base has no qualified timeline-scoped normal session opener. Existing `commitOutbox` locks include **ownerId** in their key, so opening a fresh owner cannot exclude another active timeline owner. The adapter visibly refuses absent/busy owners rather than creating a second session or inventing claim stealing. A manager-owned normal opener/binding seam is required before that fallback is enabled.
4. The base's inherited pump, recovery, unknown-ACK scheduling, root remapping, hook/legacy-save fences and projections were not replaced by the larger staged cohort. Positive real productionContext/native Runtime acceptance, exact published pair, RAW reload, inverse/redo, restart/retry, mixed edits and zero-legacy traffic remain unverified and OPEN. Detached typed acceptance in the new tests is explicitly a fixture, not Runtime proof. No writer retirement is claimed.

## Final evidence

Private Composition12 dependencies via this worktree's own symlink to `/tmp/app-coherent-deps12/node_modules`; all shared dependency files/symlinks/caches stayed read-only. Vitest used a private runner configuration/cache, `--configLoader runner --no-file-parallelism --maxWorkers=1 --cache=false`.

- Final targeted cohort: **14 files, 572 tests passed, exit 0**, 40.38 seconds. Includes native full-claim/own-key parity, explicit image/video timing, five independently mismatched pin fields, raw owner/track routing, cancellation/races, refusal/draft retention, one durable outbox/exact body/key retry, unchanged chooser/task surfaces and session/hook/provider neighbors.
- Scoped ESLint: **exit 0**, zero warnings.
- Frozen native Agent: **2 original goldens + 15 complete capture/execute/replay/inverse cases + 12 occupied-alias refusals + 12 stale-capture refusals verified**, exit 0.
- `git diff --check`: **exit 0**.

No passing behavior test was rewritten to expect refusal/loss; no skip/xfail/disable was added. No full suite, build, browser, socket, project TypeScript check, install or central request ran.

Development failures retained honestly: initial runner startup failed on the repository helper's `__dirname`; the private runner config supplies that existing path without product changes. Initial current-Agent parity rejected the old stage's missing native reads; corrected with the bounded native recorder delta above. The first expanded App run had 565 pass/1 new failure because the fabricated conflict omitted `details.status`; the fixture now uses the existing typed conflict shape and its original conflict expectation passes. Intermediate focused runs passed 225, 97 and 255 tests; these overlap the final 572 and are not additional coverage.

Exact final commands and logs: [worker report](../workers/app-m2-manual-recovery-native-add-adapter/report.md). Next: review this bounded proposal, provide the exact available publication ref and normal same-client/active-session binding, then separately authorize and qualify production activation and actual pair gates. No KEEP requested.
