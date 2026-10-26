# H3 — what the editor preview needs to draw a shot as one nested layer

Repo read: /Users/hannahomalley/Developer/astrid-video/astrid-local/labs/app-gallery-bar (branch feat/gallery-bar, HEAD e62f98690). Read-only.
Paths below are relative to `src/tools/video-editor/` unless marked otherwise.

## 1. ShotClipSequence today (compositions/TimelineRenderer.tsx)

Dispatch: `TimelineRenderer.tsx:1415` `if (clip.clipType === 'shot') return <ShotClipSequence .../>` inside `VisualTrack` (L1278). So a shot is a clip living on a normal visual track, and it is drawn inside that track's AbsoluteFill (so the track's opacity/blendMode/scale apply to the shot as a whole).

`ShotClipSequence` (L212-276):
- Resolves the child via `timeline_document_id` from `clip.params` (L214-217). Loads through `provider.loadReferencedTimeline` into a module-level cache (`shotChildCacheByProvider`, L139; `loadReferencedTimelineIntoCache` L141-187) using `useSyncExternalStore` (L221-236). Child config is passed through `resolveTimelineConfig` (L170).
- Renders `<Sequence key from={round(clip.at*fps)} durationInFrames premountFor={ceil(fps*2)}>` (L244-256). Parent `fps` is used for `from`/`premountFor`.
- Child: `<TimelineRenderer config={childConfig} />` (L262). While unresolved: an `AbsoluteFill` with `backgroundColor '#0b0b0b'` and "Loading shot…" (L264-275, testid `shot-preview-loading`).
- Config passed to the child is the whole child `ResolvedTimelineConfig` (no overrides, no fps override, no track filter).

Nesting mechanics:
- The nested `TimelineRenderer` (L1766, memo, provides its own `AstridElementHostContext`) runs its own `TimelineRendererBody` (L1566): own visualTracks reversed (L1598), own clipsByTrack, own accumulate loop (L1664-1701), own audio tracks (L1753-1760), own `AudioAnalysisProvider`, own `LocalFontFaces`.
- Background: the nested root is `<AbsoluteFill style={{ backgroundColor: 'black', overflow: 'hidden' }}>` at L1727. This is OPAQUE. A shot therefore covers everything painted below it in the parent. (Nothing in the nested path passes a transparent flag.)
- Premount (verified in Remotion source, node_modules/remotion/dist/esm/index.mjs:2409-2410): a premounted Sequence's wrapper gets `display: none` by default (`hideWhilePremounted` default). So premounted child content (2 s = fps*2 frames before `from`) is mounted but NOT visible until `from`. The shots test confirms this shape (shots.test.tsx:377-419: `data-active="false"`, `style.display === 'none'`, child content still mounted; L361-375 asserts `data-premount-for` = 60 at fps 30).
- Audio inside the shot: the nested body renders `AudioTrack` for the child's audio tracks (L1753-1760), each in the child's own Sequence tree. AudioTrack has its own premount (`AUDIO_PREMOUNT_SECONDS = 2`, AudioTrack.tsx:20-24); the comment says premounted audio is kept paused and pre-seeked, so it should not play before `from`. Not separately verified in a browser.
- Effects inside the shot: scoped to the child's own tracks (the nested accumulate loop only sees the child's tracks). See section 2.
- Transitions at shot boundaries: NONE. Each shot is its own Sequence and its own opaque layer; there is no cross-shot transition code in this file (grep "transition" hits only L417-421 inside the *timeline* renderer for clip transitions, L1355 for elementRef transitions). Within a shot, `VisualClipSequence` gets `predecessor` per track (L1551, from the track's sorted clips), so transitions between two clips on the same inner track work.
- fps/time: parent `fps` drives `from` and `premountFor` (L246-255). The child body uses `renderConfig.output.fps` (L1600ff) for its own clips' time. Nothing enforces child fps === parent fps on this legacy path. The canonical projection hard-codes the parent's output fps for every child (shotCompositionProjection.ts:547, `outputBaseConfig.output`). If a child timeline's fps differs, child clip time would be wrong on this path. Risk, not observed.
- Performance: one nested `TimelineRenderer` subtree per shot clip, mounted inside the parent Player (not a separate Player). Premount window = ±2 s around each shot, so ~2-3 shot subtrees are mounted at a boundary. `TimelineRendererBody` calls `useCurrentFrame()` so every mounted nested body re-renders each frame; `visualContent` is memoised (L1664) so child tracks are not rebuilt unless config changes. Each nested body also has its own AudioAnalysisProvider and LocalFontFaces.

Tests: `compositions/TimelineRenderer.shots.test.tsx` (14 cases, L203-478). All 14 cover the child cache, not the visual output. They assert:
- explicit host B passes through two nested shot levels; context host A retained without override; explicit host with no context; host change without remount (L211-281);
- throws when no Astrid host (L282);
- one load for sequential mounts and concurrent mounts (L292-336); synchronous reuse on remount, no loading placeholder (L337);
- premount = 60 frames at fps 30 (L361-375);
- hidden premount keeps child content mounted, `display:none` before the canonical boundary, then shown at frame 30 with no reload (L377-419);
- invalidation after save reloads (L421-459); failed load shows placeholder and retries (L460+).
They do NOT assert: background colour, blend/opacity/scale, effect-layer scope, audio, transitions, fps.

## 2. Effect layers: scope today

- `EffectLayerSequence` (compositions/EffectLayerSequence.tsx:19-72) wraps `children` in a Sequence with `wrapWithEffect(...)` for the effect's time range; outside range it returns children unchanged.
- The wrapping happens in the accumulate loop (TimelineRenderer.tsx:1664-1701). For each visual track in draw order (bottom first), `lowerTrackContent = accumulated` (everything already drawn = all tracks BELOW this one in the stack, L1674-1675), then each effect-layer clip on this track wraps `lowerTrackContent` (L1686-1697).
- So an effect-layer on track T wraps ALL tracks below T in the parent stack, not only T's own clips. That is the intended rule for the main timeline.
- Flattened canonical path (today's editor preview for canonical projects, `userId === null`): `shotCompositionProjection.ts` puts every shot child clip onto its ORIGINAL track id: `projectClip` (L318-ff): line 359 `const track = text(rawClip.track) ?? occurrence.trackId ?? 'video'`. Track definitions are merged by id (`tracksFor` L271-ff, skips ids already in the parent, L273-274). Clip ids are namespaced (`${occurrenceId}:${clipId}`, L~322) but track ids are NOT.
- Consequence (answers the question): YES. A shot-internal `effect-layer` clip on track `fx` (the shared id) goes into `clipsByTrack.effectLayers['fx']` and wraps `accumulated` = every main track below `fx` (sprite, plate, ...). Shot-internal fx clips today affect main-timeline tracks below them, and the shot's own fx clip is not confined to the shot. Same for any inner track id shared with the parent.
- The legacy lane (userId !== null, ShotClipSequence) does confine effects to the child, because the child is its own renderer. That is the behaviour the owner wants, and it exists only on that lane.

## 3. Per-track opacity / mixBlendMode / scale (VisualTrack, L1278-1330)

- L1312-1313: `opacity: track.opacity ?? 1`, `mixBlendMode: track.blendMode` on the track's AbsoluteFill. L1315-1322: `scale` + `overflow:hidden` on the track when `scale !== 1`.
- Track-level effects create CSS stacking contexts (opacity < 1, transform). Blend modes on an element blend against its stacking-context backdrop. So today, a blend mode on a shared inner track (flattened) blends against all main tracks drawn before it in the same parent context. That is what leaks.
- If a nested shot root is transparent AND has no stacking context of its own, an inner track with `mixBlendMode` would blend against the MAIN tracks below the shot. Opacity/transform on the shot's own inner tracks would isolate those tracks but the shot root itself would not isolate the group.
- Recommendation if option A: the nested root needs `isolation: 'isolate'` (or the shot occurrence gets its own stacking context) so inner blends only see the shot's content, and the whole shot composites as one group under its occurrence track's blend/opacity. This is CSS reasoning; not verified in a browser.

## 4. Options

### (A) Nested renderer at the occurrence's slot, transparent background
What exists: ShotClipSequence already is (A) on the legacy lane (L212-276). Gaps for A on the editor's real lane:
1. Background: nested root L1727 hard-codes `backgroundColor: 'black'`. Needs a prop (e.g. `transparent` threaded through `TimelineRenderer` -> `TimelineRendererBody`) that omits it. Without it, a shot hides everything below. Cheap (~5-10 lines).
2. Isolation: add `isolation: 'isolate'` on the nested root when transparent (1 line plus test).
3. Canonical lane: `projectCanonicalComposition` removes shot clips (`shotCompositionProjection.ts:532`, `filter(clip.clipType !== 'shot')`) and splices child tracks into the parent list (`tracksFor` L271-ff). A nested option needs the projection to KEEP one `shot` clip per occurrence and carry its child config inline (the canonical child is an immutable revision under `internal_timeline_revision.timeline`, `childTimeline` L~214), not a `timeline_document_id` loaded via provider. This is the big change: the projection's output shape and every consumer of the flattened `clips`/`tracks` (occurrence hit-testing, overlay, timeline rows, `useShotGroups`) assume flat tracks. Rough size: medium-large (projection + editor consumers + tests), a few days.
4. Export: Astrid's remotion renderer (`@banodoco/timeline-composition` 0.0.6, per shared context) renders flattened config. Preview and export would diverge unless export also gets a nested path. Out of scope of this note; flag.
5. Cost: one more Remotion subtree per shot, premounted ±2 s. Keep AudioAnalysisProvider per nested body or lift it.
Breaks: nothing in the legacy lane's tests; the canonical lane and the export path need the change.

### (B) Flatten with namespaced inner track ids, inserted at the occurrence slot
Mechanics: give each occurrence's inner tracks ids like `occ:<occurrenceId>/<trackId>` (in `tracksFor`, L271-ff, and `projectClip` L359), and splice them in the parent order at the occurrence's track position (the existing splice logic already tries this, L282-296, but with shared ids). The flat accumulate loop (L1664-1701) then yields nested order because the shot's inner tracks are adjacent in the stack.
Where it works: no duplicated ids; loose main clips below the shot's track draw under the whole shot (owner rule) provided the shot's inner tracks are inserted at the occurrence's slot; per-track `VisualTrack` already gives per-inner-track opacity/blend/scale; transitions are per track so they keep working.
Where it FAILS:
- Effect layers: the loop wraps `accumulated` = everything below the effect's track in the whole stack. An inner `occ:X/fx` effect would wrap main `sprite`/`plate` below the shot. To confine it, the accumulate must be scoped per shot group, i.e. a recursive group structure, which is option A in disguise. Flat B cannot express "wrap only the inner tracks below me" without a group boundary.
- Blend modes: flat inner tracks have no isolation group, so an inner blend leaks into main tracks below the shot (same as section 3). Fixing needs a group wrapper = A.
- Shot-level opacity/scale: the shot has no track of its own in B (its occurrence sits on the parent track). Shot-as-a-whole opacity/blend would have to be added as a new group anyway.
- Track count and UI: every inner track becomes a separate row in the editor (rows = tracks in array order, lib/timeline-row-layout.ts:70-76), so B changes what the editor shows.
- Size: smaller than A on the canonical lane (projection-only + loop tweak), but it does not fix effect scope or blend isolation, which are the two things the owner's rule needs.

## 5. TimelineRenderer vs @banodoco/timeline-composition

- App `compositions/TimelineRenderer.tsx` is its OWN copy (1771 lines). It imports from the package only `@banodoco/timeline-composition/theme-api`, `registry.generated`, and `ThemeProvider/useTheme` (L35, installed-themes.ts:4, sequences/registry.ts:3). It does not import the package's `TimelineComposition`.
- Vendored copy: `vendor/timeline-composition/typescript/src/TimelineComposition.tsx` (315 lines, package 0.0.2). Differences in the shot/track/effect handling:
  - Track loop: same idea (`getVisualTracks` reversed, L257) and per-track `AbsoluteFill` with `opacity`/`mixBlendMode` (L224-227). The App version adds `scale` and `overflow:hidden` at track level (L1312-1322) and the vendor only applies scale per clip (L87-94, `isolation: isolate` on the scaled clip wrapper).
  - Effect layers: vendor returns `null` for `clipType==='effect-layer'` (L61-63) and never wraps tracks in an EffectLayerSequence. App wraps tracks (L1686-1697). So effect layers do not exist in the vendored copy at all.
  - Shot: vendor has no `shot` clipType handling (grep `shot` = no hits). App has `ShotClipSequence`.
  - Background: vendor root uses `props.theme?.visual.color.bg ?? 'black'` (L263), App uses hard `black` (L1727).
  - Transitions: vendor has a transition helper (L185); App has its own (L417-421).
- Conclusion: separate copies that have drifted. The App's copy is the one the editor preview uses; the package (0.0.6, used by Astrid's renderer per shared context) is a third version. Any option needs to change the App copy; the package would need the same change for export.

## Summary of answers
1. Shot = one nested TimelineRenderer under a Sequence (premount 2 s, hidden with display:none), opaque black background, audio and effects scoped to the child, no transitions at shot boundaries, parent fps drives timing with no fps check. Tested only for child caching and host propagation (shots.test.tsx).
2. Today's canonical flattened path: shot-internal effect-layers wrap MAIN tracks below them when their track id is shared with the parent. Confirmed by reading the loop (L1664-1701) and projection (shotCompositionProjection.ts:359, 271-ff).
3. Blend/opacity/scale are per track in one shared stacking context: inner blends leak into main tracks today; a nested transparent root needs isolation.
4. A is nearly there (legacy lane), needs a transparent flag, isolation, and a canonical projection change; B cannot fix effect scope or blend isolation without becoming A.
5. Separate copies; the App copy is the editor's; the vendored package has no effect layers and no shot support.
