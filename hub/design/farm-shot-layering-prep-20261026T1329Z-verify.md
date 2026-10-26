# F-shot-layering-prep part 2: settle the four "not yet verified" items (code reading only)

Worker tf-shot-layering-verify-1320, 2026-10-26. Read-only. No renders, test runs, installs, fetches or source writes. Machine-readable copy: `verify.json` in this folder.

## Heads (checked)

| Repo | Commit | Checkout | Tree |
|---|---|---|---|
| Agent | ecdc242ed9b673f641759ecf029f95e89a2c6f92 | /home/user/work/wt/agt-pin-ecdc242e | clean |
| App | 82e9e13ddf1d7ec6c736521b2eb091dca9877598 | /home/user/work/wt/app-pin-82e9e13d | clean |
| Runtime | 95d98f038320d5d46bd679ac000ab3e15825c935 | /home/user/work/wt/rt-pin-95d98f03 | clean |
| App upstream tip | 00a014e2a393ebfb080c4fd85d5a08bc97bc6671 (origin/main, read at /home/user/work/app, no fetch) | | |
| Composition | 635f4de06fda22a85fc2e4cfc764d0153a4c9f40 | /home/user/work/wt/tf-shot-layering-verify-1320 | clean |

Upstream tip contains 636444302b and e2bfb1304d. App head 82e9e13d does not contain e2bfb1304d.

## Verdicts

| Item | Verdict | One line |
|---|---|---|
| (a) pinned-row AI buttons (e2bfb1304d) | VERIFIED | The buttons only draft composer text. The one clip-writing path on the row is an add flow the plan does not list. |
| (b) guard in remapIndependentInternalTimeline | PARTIAL | Guard behaviour is settled. The plan's line ref is wrong. A settings-only edit to a shared shot can double-prefix clip ids (code read, not run). |
| (c) expand_shot_clips callers outside Runtime | VERIFIED | None in production outside Runtime. Agent's same-named helper is used only by its tests and a doc. |
| (d) element frames clip-local in the renderer | PARTIAL | Clip-local with no transition, in preview and export. With transitions it depends on policy; needs a render to settle. |

## (a) Pinned-row AI buttons, upstream e2bfb1304d: VERIFIED

Commit e2bfb1304d ("pinned bottom row with AI generation, extension and effect buttons", 2026-10-26) is on upstream main.

- The three buttons are AI generation (Sparkles), extension (Spline) and effect or animation (Layers). `origin/main` TimelineCreateTools.tsx:7-9 defines the drafts (not sent); :79-83 are the AI and extension buttons; :85-103 is the effect button, which is a drag source when `effectDragSource` is set and otherwise a plain button; :92 sets `effect-layer` drag data.
- `origin/main` TimelineCanvas.tsx:1067 `handleCreateEffect` calls `openDraft`. :1484-1488 wires the AI and extension buttons only when `hasPromptHost` is true. `effectDragSource = !onOpenElementCreationPrompt`.
- `origin/main` TimelineEditorShellCore.tsx:315-320: `openElementCreationPrompt` activates the timeline chat, calls `requestComposerPrompt(prompt)` and locks the tasks pane. It writes no clip. It is passed unconditionally at :909.
- So in the shell the three buttons put an unsent draft in the composer and create nothing.
- The only clip-writing path on the row is the effect drag fallback. It runs only when no prompt host is passed. The drop goes through `useExternalDrop.ts:117-120` to `handleEffectLayerDrop` (external-drop-utils.ts:223-236) and `insertEffectLayerAt` (external-drop-utils.ts:148-221). That places an effect-layer clip on a visual track at the drop time, or on a new visual track, with no shot-row check. The plan's section 4.3 add-flow list does not name it. Add it.
- e2bfb1304d also removes the T text drag tool and the `onAddTextAt` and `onOpenSequenceCreator` props from TimelineCanvas. The plan's text-drag add-flow reference is stale for upstream.

Unverified: whether an agent-sent draft later writes clips onto a shot row (the agent patch path, the plan's clip.add item). Whether `handleAddTextAt` (useClipTextOverlay.ts:23) is still reachable from a control. The pinned row only reaches our App when the catch-up merge lands, so re-read the merged file then.

## (b) Guard in remapIndependentInternalTimeline: PARTIAL

- App head `shotCompositionEditor.ts:157-171`. The guard is `:160`: `if (!timeline || !Array.isArray(timeline.clips)) return internal;`. The clone is returned unprefixed. Otherwise each clip with a string id is prefixed `${prefix}:${id}` (:161-169). Only clip ids change.
- The plan's ":305-309" is not a guard inside the function. Line 305 is the conditional spread of `internal_timeline_revision` in `updateCanonicalShotRevision`. The call-site guard is `:317` (`if (updatedRevision.internal_timeline_revision)`) inside `if (sharedSource)` at `:310`. The post-remap digest guard is `:331`. The plan's "148-160" is now 157-171.
- The only caller is `:318`, reached only when `sharedSource` (`:258-261`). The settings path is `updateCanonicalShotSettings` (`:404-410`) -> `ShotEditorView.tsx:161`, which passes no timeline. So `updatedInternal` is undefined and the stored source clips go through remap again.
- Code-read risk, not executed: occ-1 gets a timeline edit on a shared shot, which gives new shot S1 with clip ids `S1:x` (`:169`). `duplicateLinkedOccurrence` (`:628-640`) keeps `shot_id` (`withOccurrenceIdentity`, `:103`), so occ-3 shares S1. A settings edit on occ-1 sets `sharedSource` true and remaps `S1:x` to `S2:S1:x`. The guard at `:160` does not detect already-prefixed ids.
- Tests: `shotCompositionEditor.test.ts:256-275` asserts the prefix on a shared timeline edit. `:277-294` covers a shared update with bare ids. `:178-197` covers a settings-only shared update, checking only the item_id prefix. I found no test with a timeline missing its clips array, and none with an already-prefixed shared source.

Unverified: whether a real shot's internal timeline can lack a clips array (the guard's negative branch; only one caller was read). The impact of the double prefix, including the save-side prefix stripping at `shotTimelineDataProvider.ts:135-156`. Whether removing the function in the plan also removes this risk (the settings path would still need checking).

## (c) expand_shot_clips callers outside Runtime: VERIFIED

- Agent (`agt-pin-ecdc242e` HEAD and integration `/home/user/work/agent` HEAD): the definition is `astrid/core/timeline/expand_shots.py:37` (`__all__` at :28). Other references: `tests/core/timeline/test_expand_shots.py:17` and its calls from :128 on; `tests/test_storyboard_repair_p4_p5.py:11,91,130`; `docs/plans/shot-generation-timeline.md:32` (prose); `tests/.test_durations` (data). No production import. Agent's managed_timeline.py does not reference it.
- App pinned (82e9e13d) and upstream (origin/main): zero matches for `expand_shot_clips | expand_shots | ShotExpansionError`.
- Composition HEAD and integration Runtime: zero matches outside Runtime's own files.
- Runtime: definition `runtime_protocol/managed_render_snapshot.py:28`. Production call `runtime_protocol/timeline_inspection.py:505` (import at :16, call inside `_attach_render_timing`, :491-520). Tests: `tests/test_asset_identity.py:7,36`; `tests/test_direct_render_admission.py:15,452-570`.
- The comment at `timeline_inspection.py:491` ("same shot clipping producer as managed rendering") is false. Nothing in managed rendering calls `expand_shot_clips`, in Runtime or Agent.

Unverified: only HEAD of each checkout was searched. Non-HEAD refs (the R4 candidate branches and others) and repos not listed were not searched. No network.

## (d) Element frames clip-local in the renderer: PARTIAL

Mechanism (verified by reading):
- Remotion, App node_modules `dist/cjs/use-current-frame.js`: `useCurrentFrame()` returns the timeline frame minus `cumulatedFrom + relativeFrom` of the nearest Sequence. Inside a Sequence it is Sequence-local.
- am-sprite `component.tsx:149` calls `useCurrentFrame()`, and keyframes are compared against it at :64-66 (`key.frame <= sf`). am-footage `:186` follows the same pattern. No file under `astrid/packs` reads `globalFrame`.

App preview:
- Effect elements: `TimelineRenderer.tsx:1355-1368` -> `AstridEffectPreviewSequence` (:356-403) mounts the component in `<Sequence from=round(clip.at*fps)>` (:382-384). Frame 0 = clip start. Transitions are ignored on this path.
- Animation elements: `AstridAnimationPreviewSequence` (:405-430) uses `from = secondsToFrames(clip.at) - transitionFrames` when there is a predecessor transition (:417-420, :426). Frame 0 = clip start minus pre-roll.

Export (composition repo, the package Agent's remotion/package.json:18 names by artifact file, content not compared):
- Element `EffectComponent` is mounted inside `ClipLook` (`TimelineComposition.tsx:84-112`). The visual clip sits in `<Sequence from={plan.drawStart}>` (:166-170), with `TransitionLayer` when `needsLayer`.
- No transition: `drawStart = span.start` (`transition-spans.ts:103-104`). Clip-local.
- Default outgoing dissolve or dip: the incoming `drawStart` moves back by T (`transition-spans.ts:139-140`). `TransitionLayer.tsx:17-19` wraps the content in `<Freeze frame={contentFrame}>`, and `contentFrame = ownFrame` (`evaluation.ts:63-64`, `transition-spans.ts:183-190`). So the content clock is clip-local. Freeze's offset semantics were read only in part (`freeze.js:43-53`).
- Opt-in `preroll-crossfade` (only fade or cross-fade may declare it, `transitions.tsx:62`; set at `transition-spans.ts:94-97`, `:144-145`): no Freeze (`TransitionLayer.tsx:17`). `contentFrame` is draw-local (`evaluation.ts:64`; comment `TransitionLayer.tsx:4-6`). Element frame 0 is T frames before the clip start.

So App effects and export agree for elements without transitions. With transitions they can disagree: App effects ignore them, App animations shift by pre-roll, export shifts only under the preroll policy.

Unverified: whether the film or the chapters timelines have transitions on am-sprite or other element clips (not checked). The final frame values with transitions (needs a 2-clip render, not run here). Freeze's semantics in the installed Remotion version.

## Other findings

1. The plan's section 4.3 add-flow list omits `insertEffectLayerAt` / `handleEffectLayerDrop` (external-drop-utils.ts:148-236).
2. Upstream e2bfb1304d removes the text drag tool. The plan's text add item is stale for upstream.
3. Plan line refs drift at App head 82e9e13d (e.g. remapIndependentInternalTimeline 148-160 is now 157-171). I did not re-map all refs; that is lead job step 1.

## Not done (outside this brief)

- Lead job step 1 (re-map every PLAN.md file:line against the heads).
- Lead job step 3 (draft `conformance/fixtures/shot-layering-v1.json`).

## git status --porcelain (checkouts used; must be empty)

Recorded in the final report.
