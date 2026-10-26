# H8 smells: shot and track duplication, dead paths, divergent copies (read-only)

Repo roots: App = /Users/hannahomalley/Developer/astrid-video/astrid-local/labs/app-gallery-bar (src/tools/video-editor = "App" below),
Astrid = /Users/hannahomalley/Developer/astrid-video/astrid-local/live-door/Astrid, Runtime = /Users/hannahomalley/Developer/astrid-video/astrid-local/live-door/Runtime.
Convention used below: array index 0 = top layer (App preview, App timeline rows, Remotion 0.0.6). "Verified" = read in code this session; "opinion" = labelled.

## 1. Visual track ordering: every implementation

| # | Location | Rule | Agrees with index0=top? |
|---|---|---|---|
| T1 | App src/tools/video-editor/compositions/TimelineRenderer.tsx:1598 (`[...getVisualTracks].reverse()`), accumulate loop 1670-1701 | later DOM = on top | YES (index0 = top) |
| T2 | App lib/timeline-row-layout.ts:70-76 | timeline UI rows in array order (index0 top row) | YES |
| T3 | App vendor/timeline-composition/typescript/src/TimelineComposition.tsx:257 (`.reverse()`) | same as T1 | YES, but dead at runtime (see C2) |
| T4 | Astrid remotion/node_modules/@banodoco/timeline-composition@0.0.6 TimelineComposition.tsx:266 (`.reverse()`) | same; this is the DEFAULT render path (rendering.remotion, Root.tsx imports TimelineComposition) | YES |
| T5 | Astrid remotion/src/ThreeTimelineComposition.tsx:343-387 (text planes): `paintIndex = n-1-i`, `z = -paintIndex`, `renderOrder = i` | index0 gets the most negative z (farthest from camera at +z, doc comment 28-38) = BOTTOM | NO (opposite) |
| T6 | Astrid remotion/src/ThreeTimelineComposition.tsx:451 (live-scene DOM stack, `[...getVisualTracks(props)].reverse()`) | index0 appended last = top | YES, so T5 and T6 disagree inside the same file |
| T7 | Astrid packs/rendering/rendering/renderers/ffmpeg/command.py:78-88 | ignores track order entirely: base clips (no `hold`) sorted by `at`, then overlays (`hold` present) sorted by `at` | N/A (third rule: layering = presence of `hold`) |

Edge case that is NOT a track-order rule but matters: App shotCompositionProjection.ts:45-47 `if tracks.length===0 push {id:'video'}` (fallback track id 'video' that clips may not reference); Astrid shot_composition_migration.py:596 and Runtime visual_seam.py:206 and seam_intent.py:78 default a missing track to the literal "video".

## 2. Shot-only track splicing (merge-by-neighbour), all copies

Same precedence in every copy (verified by reading each):
1. No following shared track in the shot's own order -> APPEND at end (bottom of stack).
2. Else nearest preceding shared track -> insert right after it.
3. Else nearest following shared track -> insert right before it.

| Copy | Location | Agrees with the others? |
|---|---|---|
| S1 App | src/tools/video-editor/data/shotCompositionProjection.ts:271-315 `tracksFor` | reference |
| S2 Astrid SDK | astrid/sdk/timeline_restructure.py:212-245 `flatten.add_track` (rule 1 at line 31) | same precedence |
| S3 Astrid SDK | astrid/sdk/timeline_restructure.py:451-470 `_layer_order` (used by plan at line 432) | same precedence |
| S4 Astrid core | astrid/core/timeline/shot_composition_projection.py:241-270 `_track_merge` (rule 1 at line 22-25) | same, EXCEPT divergence D1 below |
| S5 Runtime | runtime_protocol/visual_seam.py:312-313 `child_tracks = {**body_tracks, **parent_tracks}` | not a splice: dict merge, parent definition wins; used for role lookup and extent only, not order |

Consequence (verified, applies to all of S1-S4): a shot-only layer whose only shared neighbour sits ABOVE it (no later shared layer) is appended under every film layer, including plate/fx/sprite, because rule 1 overrides rule 2. In S1 that is line 38 overriding line 30-33 (both Python and Astrid do the same). This is the same failure class as the 17 Oct "titles hidden under plate" and the 23 Oct loose-clip-over-shot observation in CONTEXT.

Divergence D1 (verified by reading, effect not run): S1 skips shot tracks whose role is 'source' (line 287-289 `trackRole(...) === 'source'`); S4 `_track_merge` has no role filter, so a source-role shot track is inserted into the Python projection's track list but not the App's. Consequence unverified (source tracks may be dropped downstream by output projection, see C4).

## 3. Shot expansion / flattening / projection: every implementation

| # | Location | Role | Production callers |
|---|---|---|---|
| P1 | App data/shotCompositionProjection.ts:440-590 `projectCanonicalComposition` (+ `projectClip` 318-) | flattens canonical shot children into the parent timeline; parent `clipType:'shot'` clips filtered out (line 532) | App canonicalCompositionState.ts:61 (preview+export lane), lib/timeline-shot-summaries.ts (second caller, `playedProjection`) |
| P2 | App compositions/TimelineRenderer.tsx:212-276 `ShotClipSequence` + dispatch at 1415-1416 | legacy: nested `<TimelineRenderer>` per `clipType:'shot'` clip, Sequence at clip.at, premountFor 2*fps | only reached when a config still contains `clipType:'shot'` clips (see L1) |
| P3 | Astrid core/timeline/shot_composition_projection.py (686 lines) `project_shot_composition`, `project_runtime_parent_composition` | Python twin of P1 (identity, timing, tracks) | storyboard run.py:285, managed_timeline.py:962, authoring_render_preview.py:18, snapshot.py:278 |
| P4 | Astrid core/timeline/expand_shots.py:37-271 `expand_shot_clips` (legacy clipType=shot flattener) | legacy twin of P2/P3 | NONE in production: only tests (tests/core/timeline/test_expand_shots.py, tests/test_storyboard_repair_p4_p5.py) |
| P5 | Astrid sdk/timeline_restructure.py:`flatten` (chapter shots -> one film with copies) and `split` | chapter round trip, copies track defs into film + every chapter (docstring 19-22) | sdk/timeline/publish.py:97,131,146,234; checkout.py:39,325; timeline_duplicate.py:22; timeline_intent.py:264,271; timeline_cuts.py:485; packs/timeline/cli_working.py:473 |
| P6 | Runtime runtime_protocol/managed_render_snapshot.py:28-220 `expand_shot_clips` (a 4th copy of P4) | legacy flattener, kept alive for inspection only | runtime_protocol/timeline_inspection.py:499-506, which FABRICATES a `clipType:'shot'` parent around pinned occurrences to reuse it |
| P7 | Runtime runtime_protocol/store.py:1911-1927 | fail-closed: refuses `clipType:'shot'` render admission ("retired") | enforces that P6 is not on the render path |
| P8 | App lib/timeline-domain.ts:855-958 `repairConfig` (track dedupe, -dup clip id stripping, legacy pinned-group repair) + commands/timelineData.ts:26, hooks/useTimelineCommit.ts:572,635 `migrateToFlatTracks` (infers clipType 'text'/'hold'/'media' on every commit) | repair/migration on every save path | yes, every commit |

## 4. Composition renderer copies

- C1 (LIVE): App src/tools/video-editor/compositions/TimelineRenderer.tsx (1771 lines). Used by components/PreviewPanel/RemotionPreview.tsx, components/PreviewPanel/TimelineFramePreview.tsx, hooks/useClientRender.ts, pages/Home/PublicAstridQualificationSurface.tsx. Imports theme-api and registry.generated from the package (not the composition component). Its own VisualClip.tsx (689 lines) and AudioTrack.tsx (353) are the live ones.
- C2 (DEAD at runtime in App): App vendor/timeline-composition (package version 0.0.2, `file:vendor/timeline-composition` in App package.json:114). vendor/.../src/TimelineComposition.tsx (315 lines) is exported from vendor index.ts:14 but NO App source file imports `TimelineComposition`/`HypeComposition` from the package. The only references are the vendor's own index comment ("Banodoco CLI render path") and scripts/astrid-landing/public-source.patch:287 (`DEFAULT_COMPOSITION_ID = "TimelineComposition"`). Vendor AudioTrack.tsx and VisualClip.tsx are imported only by tests (compositions/AudioTrack.test.tsx:15, vendoredTimelineCompositionAliases.test.ts). Stale: diff vs 0.0.6 (only meaningful diff, TimelineComposition.tsx ~L75) is that 0.0.6 passes `assetEntry` to EffectComponent and 0.0.2 does not.
- C3 (LIVE default render): Astrid remotion/node_modules @banodoco/timeline-composition 0.0.6 via remotion/src/Root.tsx:7 (TimelineComposition). Selected by Astrid renderers/remotion (rendering.remotion is the default selector: packs/rendering/actions/render/run.py:422,614).
- C4 (OPT-IN): Astrid remotion/src/ThreeTimelineComposition.tsx (registered Root.tsx:173, lazy-loaded 91; used only by renderers/threejs/run.py, selected explicitly). Its own track-to-z rule is the opposite convention (T5). Also a third copy of the text-overlay logic in ffmpeg/text.py:194 (comment says it mirrors ThreeTimelineComposition wrapText).
- C5 (DEAD in App runtime): App vendor VisualClip.tsx and AudioTrack.tsx (only tests).
- Verdict: the only composition that matters for the owner's "preview vs export" question is C1 (preview/client render) vs C3 (default Remotion export). They share the track-order convention (T1 vs T4) but are two separate code bases; there is no test that compares them beyond the vendored-alias guard.

## 5. Legacy / migration residue around shots

L1 (reachable, but only for unmigrated or harness data): clipType 'shot' in the App renderer. Lane decision: App src/tools/video-editor/data/canonicalCompositionState.ts:36-39 `canonicalLane = userId===null && hasShotComposition && (hasShotClips || composition)`. If a Runtime doc has `clipType:'shot'` clips but NO prepared shotComposition, the lane is 'legacy' and the raw shot clips reach TimelineRenderer.tsx:1415 (nested ShotClipSequence). Also reached in the DEV ExtensionHarnessPage (pages/ExtensionHarnessPage.tsx:86,581,664 with userId 'extension-harness-user', route gated import.meta.env.DEV in app/routes.tsx:15,109). No production caller passes a non-null userId to the editor: VideoEditorPage.tsx:149,168 hard-code `userId: null`, the tour sets null, PublicAstridEditorProvider passes none.
L2 (verified): the canonical contract forbids the legacy shapes: App data/shotComposition.ts:96 and Astrid core/timeline/shot_composition.py:342-343 ("pinnedShotGroups is migration-only"), App shotComposition.ts:128 (Astrid equivalent not located exactly) ("clipType=shot is migration-only"), Astrid invocation.py:1416-1420 refuses clipType=shot in canonical timelines.
L3 (legacy field still WRITTEN in App production paths): App shared/lib/placement/documentPlacement.ts:70-99,187,206,277 writes/reads `config.pinnedShotGroups`; used by shared/hooks/shots/useShotGenerationMutations.ts:20, shared/lib/timelineFrameBatchPersist.ts:2, shared/lib/placement/placementService.ts:31. commands/runner.ts:213-250 and commands/media.ts:284,625,691 and hooks/useExternalDrop.ts:256,413 carry `pinnedShotGroupsOverride` through the command runner. Net: the Shots page still mutates the legacy field, while the canonical contract rejects it when present.
L4 (legacy field still READ in Astrid production): packs/rendering/actions/timeline_visualize/emit.py:1856 emits warning SHOT_GROUPS_ABSENT when `pinnedShotGroups` is not a list; migration deletes it (shot_composition_migration.py:866), so a canonical film gets that warning unless its path is canonical-aware (not checked in detail). sdk/timeline_filmstrip.py:743,1031 `pinned_shots` from pinnedShotGroups; runtime_protocol/timeline_cutover.py:67-80 counts legacy shapes ("legacy_shape"). Storyboard run.py:300-330 DOES prefer the canonical occurrences first (verified), so it is fine.
L5 (allowlists carrying legacy fields): Astrid core/timeline/projection.py:134 `_PROJECTED_TOP_ALLOWED` includes "pinnedShotGroups"; core/timeline/banodoco_schema.py:351 includes it; Astrid sdk/timeline/selection.py:21 and invocation.py:1013 list "shot" as a valid clipType/selector; App runtime/managedRuntimeClipTypes.ts:9 lists 'shot'; App runtime/exportGuard.ts:1050 `isManagedShot`.
L6 (UI branches for legacy nesting): App components/TimelineEditor/TimelineEditorCore.tsx:575 and TimelineEditorCoreBody.tsx:549 `hasNestedShots`; components/TimelineEditor/ClipAction.tsx:601; TimelineEditorCore.tsx:348 and TimelineEditorCoreBody.tsx:340 and AstridTimelineEditor.tsx:298 filter `clipType==='shot'`.
L7 (no producer): nothing in current code writes `clipType:'shot'` except the one-shot migration (shot_composition_migration.py, 1095 lines, only called from its own tests and the explicit migration entry; no production importer found in Astrid). So for canonical docs the clipType 'shot' branch is reachable only via un-migrated stored documents.
L8 (chapter split copies): sdk/timeline_restructure.py:19-22 docstring says track definitions are copied into the film and every chapter shot, with "the film's definition wins" on conflict. Same copies documented in CONTEXT (16 Oct chapter split; 22 Oct RT3-05 drift). flatten requires contiguous chapters from 0 (line 205-206: TimelineEditError) => the round trip only works for split films.
L9 (dead-ish): Astrid expand_shots.py (P4) and Runtime managed_render_snapshot.py (P6) exist for the legacy shot-expansion shape; P6 is only alive through the inspection fabrication hack.

## 6. Hidden flags / modes that change shot or track behaviour

- H1 userId sentinel (strongest hidden mode). `userId === null` selects the canonical lane in 8+ places: useRenderState.ts:568-574, components/PreviewPanel/useVideoEditorPreviewComposition.ts:10-21, components/CompactPreview.tsx:28-34, hooks/useFinalVideoAvailable.ts:309, components/AstridTimelineEditor.tsx:116, lib/timeline-shot-summaries.ts:15, hooks/useTimelineState.ts:1136 (playedShotComposition). The same null also means "signed out" in shared/contexts/AuthContext.tsx:55,87 and means "Runtime mode" in shared/contexts/useProjectSessionCoordinator.ts:14. Three meanings, one value. Any non-null userId silently changes which shot code runs.
- H2 ExtensionHarnessPage (DEV route) forces the legacy lane via a fake userId (see L1).
- H3 Renderer selector: rendering.remotion (default) vs rendering.threejs (opposite z convention, T5) vs rendering.ffmpeg (ignores track order, T7). Changing the renderer changes layering.
- H4 `?localBrowserRender=1` (App hooks/useRenderState.ts:278-281, requires isLocalTestMode) and `?transcriptLaneFixture=` (VideoEditorPage.tsx:378-386, DEV/test only): neither touches shot or track behaviour.
- H5 Env vars: grep of packs/rendering, sdk/timeline, core/timeline and Runtime runtime_protocol found NO env flag that changes shot or track ordering (only storage, progress, lock and identity variables).

## 7. Ranked smells (opinions labelled)

1. [VERIFIED, real failure] Shot-only layer placement rule duplicated in 4 copies (S1-S4) with the append-at-bottom override (S1 line 38, S4 line 23-25 and 34-37). A shot-only layer whose only shared neighbour is above it ends up under plate/fx. Cause of the 17 Oct and 23 Oct symptoms. "Shot = nested layer" deletes this entirely (the sub-timeline occupies one slot; no splice). Opinion: strongest candidate.
2. [VERIFIED, real divergence] Track z-order convention is inconsistent: T5 (text planes, index0 bottom) vs T6 (live scene DOM, index0 top) in the same ThreeTimelineComposition.tsx, and vs T1/T4 everywhere else. Also ffmpeg (T7) ignores track order. Failure: text and live-scene layers in a threejs export can stack in opposite order. Not run. "Shot = nested layer" does NOT remove this; it only reduces the number of places that need the convention. Opinion.
3. [VERIFIED, two projections] P1 (App) and P3 (Python) are two independent implementations of the same canonical flatten (identity, timing, track splice). D1 shows they already differ (source-role filter). Failure: preview and export can differ for the same graph. "Shot = nested layer" removes most of the flatten (clip re-timing, identity mapping, track splicing); the Python side still needs a nested-render path.
4. [VERIFIED, two live shot renderers] P2 (legacy nested renderer) and P1 (canonical flatten) implement the two DIFFERENT shot models in one renderer. Note: P2 (ShotClipSequence) is already the owner's requested model (a nested sub-timeline at the shot's track position); the canonical lane flattens it away. Opinion: the owner's decision is closer to the legacy lane than to the canonical flatten, so the flatten (P1, P3, S1-S4) is what a nested-layer change deletes, not P2.
5. [VERIFIED, dead code] P4 Astrid expand_shots.py (271 lines) and P6 Runtime managed_render_snapshot.py (220 lines): no production caller; P6 kept alive only by a fabricated clipType:'shot' parent in timeline_inspection.py:499-506. "Shot = nested layer" deletes both.
6. [VERIFIED, dead code] C2 App vendor TimelineComposition.tsx (315 lines) and vendor VisualClip/AudioTrack copies: no runtime importers; stale (0.0.2 vs 0.0.6 assetEntry). Failure today: none at runtime; risk: a fix to the vendor copy never reaches preview. Not shot-specific; delete candidate. Nested-layer change: no effect.
7. [VERIFIED, legacy field still written] L3: App Shots page still writes pinnedShotGroups via documentPlacement.ts and the command runner, while the canonical contract rejects that field (shotComposition.ts:96). Failure: a Runtime-mode doc that acquires pinnedShotGroups is refused by the canonical contract; visualize warns SHOT_GROUPS_ABSENT for canonical films (L4). Nested-layer change: would not remove it unless the Shots page stops using pinned groups.
8. [VERIFIED, hidden mode] H1 userId sentinel overloaded three ways across 8+ call sites. Failure: any editor entry that passes a real userId silently flips to the legacy lane (H2 shows it has happened in a harness). Opinion: "one lane, chosen by document content, not by user id" is the fix; nested-layer change removes the need for the lane split.
9. [VERIFIED, copy drift] L8 chapter split copies film track definitions into every chapter (timeline_restructure.py:19-22). Failure: documented drift (RT3-05, 22 Oct). Nested-layer change deletes the copies (chapters reference the film's one copy).
10. [VERIFIED, duplicated UI] App components/TimelineEditor/TimelineEditorCoreBody.tsx (978 lines) vs TimelineEditorCore.tsx (1017 lines): 221 differing diff lines; Body is used by pages/Home/PublicAstridEditorParts.tsx:88 and app/onboarding/BrowserTourEditor.tsx:66; Core by AstridTimelineEditor and TimelineEditor. Both carry shot-group code (66 vs 60 matches). Failure: fixes land in one copy only (opinion: likely). Not removed by nested-layer change.
11. [VERIFIED, lossy repair] App lib/timeline-domain.ts:855-958 repairConfig strips any `-dup-N` suffix from clip ids (line 653, 879) and dedupes tracks, on every save path (timelineData.ts:26, useTimelineCommit.ts:572,635). Failure: a legitimate id that ends in -dup-N is silently renamed. Opinion: low risk, but it is a second repair pass on top of the projection.
12. [VERIFIED, divergent default] App shotCompositionProjection.ts:45-47 falls back to a track id 'video' when the list is empty; several Runtime/Astrid paths default missing track to "video" (visual_seam.py:206, seam_intent.py:78, shot_composition_migration.py:596). Failure: clips with a different track id are orphaned into a track that may not exist. Not run.
13. [VERIFIED, allowlists] projection.py:134 and banodoco_schema.py:351 still allow pinnedShotGroups on the projected/saved top level while the canonical contract forbids it. Opinion: remove with the field.

## 8. Not verified / caveats
- Whether ShotClipSequence's nested renderer has a black background (CONTEXT says so): only the loading placeholder is #0b0b0b (TimelineRenderer.tsx:264); the nested root's background was not checked.
- Whether D1 (source-role filter) changes output: not traced past the projection.
- Whether emit.py:1856 fires for canonical films: the guard checks only pinnedShotGroups; canonical-aware branch not traced.
- ffmpeg, ThreeTimeline, and Remotion 0.0.6 behaviour: read from code only, no render was run (read-only task).
- No tests were run (read-only task).
