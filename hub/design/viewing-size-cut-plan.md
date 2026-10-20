# Viewing M4 conditional size-cut plan

Status: docs-only measurement handoff, 2026-10-20. This refreshes the cut plan
after actual integrated cuts; it does not change the M4 boundary or claim that
the target has been met. Census tables report physical and nonblank UTF-8
lines; function-body counts are called out explicitly.

## Result first

The refreshed canonical slice is **49,103 nonblank / 53,452 physical lines**.
Already-landed deletions are recorded below, but excluded vendor/fallback work
does not reduce that canonical total. The remaining D09 and broad D08 cuts are
still conditional: the source map finds more private visibility/evaluator logic
than the previous `375 + 31` summary, but the public-query caller and parity
gates are not complete. Q1 (`typescript/src/lib/fade.ts`) remains a proposed
six-nonblank-line local deletion; it is still present in the current tree and
is not credited as landed.

The measured conditional arithmetic is:

| conditional unit | deduplicated body/source count | current confirmed net | measured after range, if the named gates pass |
| --- | ---: | ---: | ---: |
| Q1: `typescript/src/lib/fade.ts` inline | 6 NB source lines | **0 (present)** | 49,097 if the named local proof lands |
| D09 core: `astrid/core/timeline/onscreen.py` | 375 NB whole file; 69 NB role/coverage seam must remain or move (`element_coverage`, `_coverage_of`, `_has_value`, `role_of`) | 0 until callers and the seam are qualified | **48,728–48,797** (−375 to −306) after Q1 |
| D09a: `motion/model.py::mouth_state` | 24 NB direct body; `hash_unit` is a separate 9 NB helper; `presenter_words` is shared and is not creditable | 0 | subtract **31–40** only after both lipsync callers and the helper are replaced; combined **48,688–48,766** after Q1 |
| D09b: `motion/model.py::mouth_box` | 7 NB direct body; shared `presenter_view` is retained | 0 | included in the combined range above only after the pixel caller/aggregate gate |
| D09c: private mouth crop | excluded | 0 | 0; pixel crop/statistics remain KEEP |
| D08: App `lib/audioFade.ts` | 60 NB module / 27 NB executable function bodies | **Landed outside the confirmed slice** (`887f26265`); no canonical credit | App-local source is already lower by this excluded helper; broader audio parity remains open |
| D08: App `VisualClip`/`TimelineRenderer` host | `VisualClip.tsx` 648 NB; `TimelineRenderer.tsx` 1,656 NB | 0 | 0 until a complete public host replacement exists; do not count mixed adapters |

The D09 ranges are a conditional arithmetic envelope, not a forecast of a
landing. With the current evidence the honest current total is 49,103
nonblank. A public replacement may add a thin adapter, and a source-qualified
caller may retain more of the old helpers. No vendor, archive, fallback, stale
`dist`, pixel, timing, custom-loader, or unknown-diagnostic deletion is added
to these numbers.

## Refreshed accounting boundary and current growth

This table uses the same manifest and the refreshed current heads pinned in the
census. Physical and nonblank lines are both shown so the deletion arithmetic
does not mix measures.

| manifest row | baseline files / bytes / physical / NB | current files / bytes / physical / NB | growth files / bytes / physical / NB |
| --- | ---: | ---: | ---: |
| Composition authored `typescript/src/**` | 16 / 45,621 / 1,550 / 1,398 | 79 / 190,569 / 4,442 / 4,097 | +63 / +144,948 / +2,892 / +2,699 |
| Agent `timeline_visualize/**` authored subset | 54 / 1,253,951 / 27,700 / 24,911 | 54 / 1,292,896 / 28,504 / 25,663 | 0 / +38,945 / +804 / +752 |
| Agent explicit render/evaluator adapters + elements | 29 / 375,489 / 11,381 / 10,993 | 29 / 363,113 / 11,053 / 10,680 | 0 / −12,376 / −328 / −313 |
| Agent `onscreen.py`, `scene_answers.py` | 1 / 18,156 / 452 / 375 | 2 / 24,162 / 568 / 470 | +1 / +6,006 / +116 / +95 |
| Agent Remotion host, adjacent execution excluded | 11 / 24,264 / 631 / 573 | 10 / 28,084 / 690 / 630 | −1 / +3,820 / +59 / +57 |
| App active PreviewPanel/compositions/render source | 29 / 282,934 / 7,533 / 6,932 | 32 / 314,411 / 8,195 / 7,563 | +3 / +31,477 / +662 / +631 |
| **confirmed canonical total** | **140 / 2,000,415 / 49,247 / 45,182** | **206 / 2,203,235 / 53,452 / 49,103** | **+66 / +202,820 / +4,205 / +3,921** |

Current refs are Composition `5a4e9b72`, Agent `d0a5072b`, and App `20ea14c2`,
with full SHAs in `viewing-size-census.md`. The previous frozen 48,343-line
result remains historical evidence; it is not mixed into the refreshed total.

## What actually landed versus what remains held

Merged cuts: App private trim math (`93cd2f7d4`/`9d518546d`) and
`lib/audioFade.ts` plus its test (`887f26265`); the dead HTML inspector
(`c1a1d4fdb`, integrated by `a760ecca0`) including its CSS/JS/test; App
fallback shims; and App vendored Composition/static copies (`1b4ac8b68` plus
the bounded D10 App landing). The vendor/fallback rows are outside the
canonical total, and the audio helper is outside the manifest row, so none is
double-credited as a fresh canonical reduction.

Held cuts: D08 `VisualClip`/`TimelineRenderer` host replacement and full audio
parity; D09 `onscreen.py`, private motion/mouth/ROI/crop/statistics callers,
and source-identity/parity gates; and the remaining Agent D10 source-adapter
copies pending corrected custom-winner/catalog proof. Q1 is also still
present, so its six nonblank lines are not credited. The dead inspector is a
separate retired path, not D09 closure.

Delivery disclosure: main infrastructure touched but outside this census
includes Agent process-custody/PID-reuse guards, short-lived Remotion
attempt-temp accounting and owner-root cleanup, and retained source-carry,
source-identity, and verified-source request guards. These are accounted
infrastructure changes, not Viewing product cuts.

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
| refreshed current | 49,103 | none beyond already-landed excluded cuts | 23,103 |
| Q1 qualified | **49,097** | Composition fade helper, −6 | 23,097 |
| Q1 + D09 core, thin role seam | **48,791–48,722** | only if trusted source/caller/parity gates pass; −306 to −375 | 22,791–22,722 |
| also D09a + D09b | **48,760–48,682** | only if public motion and selected-cut ROI gates pass; additional −31 to −40 | 22,760–22,682 |
| D08 audio helper | **already landed outside row** | App-local −60 maximum; no canonical slice credit | unchanged |

The best measured conditional envelope is roughly 48.7k from this refreshed
current tree, far above the
26k upper target, and the true four-repo core is larger because Runtime and
editing paths are outside this Viewing census. Closing that gap requires
precise owner choices: qualify the D09 source/caller join and accept the
remaining motion/crop behavior as retained, qualify exact App public audio and
host parity, or consciously revise the global size target. It does not permit
cutting the retained viewer, pixel lane, diagnostics, generic host, or owner
film behavior, and it does not permit re-crediting vendor/archive/fallback
deletions that were already excluded.
