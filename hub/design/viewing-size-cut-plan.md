# Viewing M4 conditional size-cut plan

Status: docs-only measurement handoff, 2026-10-20. This refines the frozen
cut plan; it does not change the M4 boundary or claim that the target has been
met. Counts are nonblank physical UTF-8 lines unless a function-body count is
called out explicitly.

## Result first

The only currently qualified reduction remains Composition's six nonblank
lines in `typescript/src/lib/fade.ts` (Q1). The frozen confirmed Viewing slice
therefore remains **48,337 lines after Q1**, not 20–26k. D09 and D08 are still
conditional: the source map finds more private visibility/evaluator logic than
the previous `375 + 31` summary, but the public-query caller and parity gates
are not complete.

The measured conditional arithmetic is:

| conditional unit | deduplicated body/source count | current confirmed net | measured after range, if the named gates pass |
| --- | ---: | ---: | ---: |
| Q1: `typescript/src/lib/fade.ts` inline | 6 NB source lines | **-6** | 48,337 |
| D09 core: `astrid/core/timeline/onscreen.py` | 375 NB whole file; 69 NB role/coverage seam must remain or move (`element_coverage`, `_coverage_of`, `_has_value`, `role_of`) | 0 until callers and the seam are qualified | **47,962–48,031** (−375 to −306) |
| D09a: `motion/model.py::mouth_state` | 24 NB direct body; `hash_unit` is a separate 9 NB helper; `presenter_words` is shared and is not creditable | 0 | subtract **31–40** only after both lipsync callers and the helper are replaced; combined **47,922–48,000** |
| D09b: `motion/model.py::mouth_box` | 7 NB direct body; shared `presenter_view` is retained | 0 | included in the combined range above only after the pixel caller/aggregate gate |
| D09c: private mouth crop | excluded | 0 | 0; pixel crop/statistics remain KEEP |
| D08: App `lib/audioFade.ts` | 60 NB module / 27 NB executable function bodies | 0 to the confirmed slice (outside its manifest row) | App-local source can fall by at most 60 NB; confirmed Viewing total unchanged |
| D08: App `VisualClip`/`TimelineRenderer` host | `VisualClip.tsx` 648 NB; `TimelineRenderer.tsx` 1,656 NB | 0 | 0 until a complete public host replacement exists; do not count mixed adapters |

The D09 ranges are a conditional arithmetic envelope, not a forecast of a
landing. With the current evidence the honest expected total is still
48,337. A public replacement may add a thin adapter, and a source-qualified
caller may retain more of the old helpers. No vendor, archive, fallback, stale
`dist`, pixel, timing, custom-loader, or unknown-diagnostic deletion is added
to these numbers.

## Frozen accounting boundary and current growth

This table is preserved from the frozen census. It is the accounting base and
must not be silently rewritten using the later Agent head.

| manifest row | baseline files / bytes / NB lines | current files / bytes / NB lines | growth files / bytes / NB lines |
| --- | ---: | ---: | ---: |
| Composition authored `typescript/src/**` | 16 / 45,621 / 1,398 | 79 / 190,523 / 4,097 | +63 / +144,902 / +2,699 |
| Agent `timeline_visualize/**` authored subset | 54 / 1,253,951 / 24,911 | 55 / 1,270,190 / 25,256 | +1 / +16,239 / +345 |
| Agent explicit render/evaluator adapters + elements | 29 / 375,489 / 10,993 | 29 / 366,756 / 10,744 | 0 / −8,733 / −249 |
| Agent `onscreen.py`, `scene_answers.py` | 1 / 18,156 / 375 | 2 / 24,116 / 469 | +1 / +5,960 / +94 |
| Agent Remotion host, adjacent execution excluded | 11 / 24,264 / 573 | 10 / 27,058 / 613 | −1 / +2,794 / +40 |
| App active PreviewPanel/compositions/render source | 29 / 282,934 / 6,932 | 30 / 293,804 / 7,164 | +1 / +10,870 / +232 |
| **confirmed canonical total** | **140 / 2,000,415 / 45,182** | **205 / 2,172,447 / 48,343** | **+65 / +172,032 / +3,161** |

Frozen refs are Composition `46bd700b`, Agent `931d7ec`, and App `18becfb`,
with the full SHAs and reproducible manifest in
`handoff-vw-m4-current-core-census-freeze.json`. The read-only live source map
was also checked against Composition `e80c46b` (same tree), App `18becfb`, and
Agent `df2739f`; the later Agent head measures 25,442 NB lines in the authored
visualize subset and 11,213 NB lines in the explicit adapter/elements subset.
Those two live numbers are inspection facts, not a replacement baseline: the
frozen 48,343 total and its growth columns remain authoritative.

## What the public replacement actually is

The replacement query is the Composition public scene path:

* `typescript/src/scene-evaluation.ts`: `prepareScene`, `querySceneFrame`,
  `querySceneOcclusion`, `SceneLayer.diagnostics`, and the explicit
  `COVERED`/`DIP`/`GAP`/`UNKNOWN` result. It uses evaluated component bounds and
  declared capability facts; it does not guess glyph, sprite, media-alpha, or
  modifier internals.
* Agent `astrid/core/timeline/scene_answers.py`: `frames_at` and
  `host_frames_at` are transport/thin-admission adapters. The latter currently
  imports `element_coverage` and `role_of` from `onscreen.py`, so deleting the
  whole file without moving that 69-NB role/coverage seam would break the
  replacement itself.
* Agent `composed_frame.py::RemotionFrameProvider` and `_observe_scene` bind
  answers to the exact captured timeline, registry, theme, materialized assets,
  source identity, occurrence map, and requested frames. This is source
  authority and capture plumbing, not a second evaluator.

Named evidence that must remain attached to the eventual deletion is
`tests/packs/rendering/test_scene_answers.py`, `test_scene_host.py`,
`test_scene_source_carry.py`, `presenter_selected_cut_query.mjs`,
`presenter_series_inspection.mjs`, `test_presenter_series_inspection.py`, and
`test_presenter_selected_cut_aggregate.py`. The latter is still explicitly an
unapplied consumer proposal and says production lipsync uses `mouth_box`; it
is not a deletion qualification.

## D09: complete private-math map

The following is a source map, not a claim that every line is deletable.
Function counts are deduplicated by the union of their nonblank source spans;
overlapping callers are not counted twice.

| source | measured body | role and status | replacement/caller gate |
| --- | ---: | --- | --- |
| `onscreen.py`: `element_coverage`, `_coverage_of`, `role_of`, `layout_bounds`, `_build`, `_opacity`, `_visible`, `visible_at`, `_classify`, `coverage` and helpers | 375 NB whole-file removal candidate | direct private coverage/opacity/bounds evaluator; **conditional D09 core** | Public `querySceneFrame`/`SceneLayer`; move the 69-NB role/coverage seam first, then prove SDK check, labels, capture and historical/source-bound callers preserve exact IDs, frame order, findings, and UNKNOWN/unavailable distinction |
| `motion/model.py`: presenter/motion/geometry group (`hash_unit`, `presenter_words`, `mouth_state`, `pushed_zoom`, `presenter_view`, `face_box`, `declared_face`, `mouth_box`, props helpers, `props_at`, `_wrap_lines`, `_internal_zoom`, `boxes_at`, `safe_rect`, `intersection`, `area`) | 261 NB union; `boxes_at` alone 68 NB | remaining private visualizer model; **mostly unresolved**, not a 261-line deletion credit | Public component diagnostics/motion facts must cover all current callers. `render_lipsync`, `overlay_bounds`, motion checks, and fast-lane occlusion/zoom currently call these helpers directly |
| `motion/model.py::mouth_state` and unique helper dependency | 24 NB direct; 33 NB with `hash_unit`; `presenter_words` shared | **D09a conditional** | Replace `layers/builtin.py::render_lipsync` and `_presenter_props` with a public per-frame motion/diagnostics query. `presenter_words` remains because `motion/data.py`, `motion/lint.py`, and the built-in layer use it independently |
| `motion/model.py::mouth_box` | 7 NB direct; shared `presenter_view` retained | **D09b conditional** | Replace `layers/builtin.py::render_lipsync` ROI with the source-qualified public mouth diagnostic, preserving the 2% threshold, denominator, selected keys, and planted mismatch |
| `motion/lint.py`: `_clear_face`, `_data_faces`, `composition`, `timing`, `lint_cuts` | 188 NB union | checks and findings; **unresolved/KEEP until public facts cover them** | Public scene findings may supply bounds/diagnostics, but these checks also produce safe-area, text-size, overlap and timing messages. Do not delete or convert them to refusal/UNKNOWN without named behavior tests |
| `layers/builtin.py::render_lipsync` and `overlay_bounds` | 75 NB and 31 NB | presentation/check consumers; **KEEP pending caller migration** | Must retain the visible motion sheet, selected-frame labels, and exact pixel lane while semantic and ROI queries are qualified |
| `fast_lane.py`: `_on`, `_changed_on_screen`, `hidden_under`, `zoom_region`, `_crop` and related helpers | 61 NB selected spans | **pixel KEEP**, not a D09 deletion | Pixel verification, changed-area statistics, selected crop/zoom and the existing `fast_lane` behavior are explicitly preserved. `sweep.py` is likewise not a deletable pool |

This map explains the corrected boundary: `375 + 31` names only the direct
core/mouth deletion units. It omits the 261-NB motion/geometry region, the
188-NB check callers, and the 61-NB pixel spans because those have live
presentation, diagnostics, or pixel consumers. They are measured and
classified, not silently credited as cuts.

## D08: App map and replacement limits

`playerEvaluation.ts` is already absent from current App and cannot be counted
again. The remaining viewer is a mixed host, not a removable evaluator file:

* `VisualClip.tsx` has 648 NB. Its concrete geometry bodies are
  `getClipBoxStyle` (42 NB), `getIntrinsicMediaSize` (17), `VisualAsset` (162),
  `VisualClip` (116), and `VisualClipSequence` (59). They handle readiness,
  missing/unsupported assets, crop/viewport layout, transitions, effects,
  shaders, canonical occurrence caps, and premount timing. The public
  Composition evaluator supplies scene answers, but not this App host contract;
  these bodies are **adapters KEEP**, not D08 credits.
* `TimelineRenderer.tsx` is 1,656 NB. `VisualTrack`,
  `TimelineRendererBody`, dynamic/extension dispatch, shot loading, effect and
  unknown placeholders are host orchestration and capability isolation. The
  public-host tests (`TimelineRenderer.public-host.qualification.test.tsx`,
  `TimelineRenderer.sequence.test.tsx`, `TimelineRenderer.test.tsx`) prove
  behavior that a scene query alone cannot replace.
* `lib/audioFade.ts` is a small genuine duplicate of renderer fade semantics:
  `getAudioFade` (10 NB), `audioFadeGain` (9), and `getAudioVolumeProp` (8).
  `AudioTrack.tsx` calls all three. `audio-envelope.ts`/`applyAudioEnvelope`
  are the possible public replacement, but exact per-frame clip-fade behavior,
  frame offsets, retry/mute/amplify behavior, and App/export parity are still
  open. `lib/audioFade.test.ts` is the caller contract and must remain until a
  public equivalent passes the same crossfade, overlap, invalid-input, and
  delayed-Sequence cases.

Therefore D08 has a measured App-local ceiling of 60 NB, but **zero confirmed
Viewing-slice credit** and zero current net. A package adoption or an App host
rewrite must not be disguised as deletion of `VisualClip`/`TimelineRenderer`.

## Largest remaining modules, ranked by primary treatment

The ranking uses the live Agent/App source map where noted. It is intentionally
not additive: a module may contain retained neighboring behavior, and the
whole-file number is not a deletion claim.

| rank | module | NB | primary classification | reason |
| ---: | --- | ---: | --- | --- |
| 1 | Agent `rendering/elements/catalog.ts` | 6,151 | adapters KEEP / generic main infrastructure | registry, aliases, capabilities and package-owned element admission; not a second visibility evaluator |
| 2 | Agent `timeline_visualize/emit.py` | 1,994 | presentation | projection, structure, relations, diagnostics and action indexes |
| 3 | Agent `timeline_visualize/filmstrip_execution.py` | 1,987 | adapters KEEP | managed output, source/materialization, timing alignment and receipts |
| 4 | Agent `timeline_visualize/layout.py` | 1,961 | presentation | timeline/page geometry and labels; it lays out answers rather than deciding scene coverage |
| 5 | Agent `timeline_visualize/frozen.py` | 1,957 | adapters KEEP / generic main infrastructure | frozen-pack identity, ownership and integrity admission |
| 6 | Agent `timeline_visualize/filmstrip_cards.py` | 1,827 | presentation | captions, cards, audio waveforms, navigation and PNG composition |
| 7 | Agent `rendering/renderers/remotion/run.py` | 1,710 | adapters KEEP / generic main infrastructure | managed renderer host, registry/theme/materialization and render contract |
| 8 | App `compositions/TimelineRenderer.tsx` | 1,656 | adapters KEEP | live App dispatch/host behavior, not a standalone evaluator |
| 9 | Agent `timeline_visualize/inspection_contract.py` | 1,334 | adapters KEEP | input-window, status, provenance and compact receipt contract |
| 10 | Agent `actions/render/managed_timeline.py` | 1,105 | adapters KEEP | managed render input and canonical host boundary |
| 11 | Agent `timeline_visualize/fast_lane.py` | 804 | pixel KEEP | exact decoded pixel comparison, crop/zoom and changed-area statistics |
| 12 | Agent `timeline_visualize/composed_frame.py` | 759 | pixel KEEP / source authority | exact capture source, materialized assets, renderer callback and cache |
| 13 | Agent `timeline_visualize/motion/model.py` | 645 | unresolved evaluator-adjacent | 261 NB of private motion/geometry bodies have live callers; only named mouth units are conditional |
| 14 | Agent `timeline_visualize/audio_analysis.py` | 517 | adapters KEEP / pixel-audio evidence | waveform bins, gaps, loudness and audio identity |
| 15 | Agent `timeline_visualize/motion/element_motion.py` | 503 | unresolved/presentation | generic registered element motion and capability evaluation, not the D09 core |

The true generic untouched infrastructure in this list is the element catalog,
Remotion host, frozen-pack verifier, managed render boundary, and App registry/
extension dispatch. A whole-file census that calls these “evaluator duplicate”
would overcount. Conversely, the motion model and checks are not generic main
infrastructure, but they remain unresolved because their current presentation
and diagnostic callers are real. Pixel statistics/crops, `_timing_evaluators`,
custom loaders, loud unknown reports, and feature playback remain separate KEEP
categories.

## Conditional AFTER table and owner choices

| state | confirmed Viewing NB | what is actually credited | remaining gap to 26k |
| --- | ---: | --- | ---: |
| frozen current | 48,343 | none | 22,343 |
| Q1 qualified | **48,337** | Composition fade helper, −6 | 22,337 |
| Q1 + D09 core, thin role seam | **48,031–47,962** | only if trusted source/caller/parity gates pass; −306 to −375 | 22,031–21,962 |
| also D09a + D09b | **48,000–47,922** | only if public motion and selected-cut ROI gates pass; additional −31 to −40 | 22,000–21,922 |
| D08 audio helper | **unchanged** | App-local −60 maximum is outside the confirmed row; no slice credit | unchanged |

The best measured conditional envelope is still roughly 47.9k, far above the
26k upper target, and the true four-repo core is larger because Runtime and
editing paths are outside this Viewing census. Closing that gap requires
precise owner choices: qualify the D09 source/caller join and accept the
remaining motion/crop behavior as retained, qualify exact App public audio and
host parity, or consciously revise the global size target. It does not permit
cutting the retained viewer, pixel lane, diagnostics, generic host, or owner
film behavior, and it does not permit re-crediting vendor/archive/fallback
deletions that were already excluded.

