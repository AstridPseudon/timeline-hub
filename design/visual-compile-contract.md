# Visual compile contract

Status: contract draft for the Agent compiler, from the 2026-10-20 03:46 orchestrator decision (popup projection consistency) and the 03:59 revised decision (clip look). Golden vectors: `tests/editing_conformance/fixtures/visual_compile_contract.json`, run by `tests/editing_conformance/test_compile_contracts.py`.

Reference for "visible today": `origin/main` e51595c6. The compiler is `astrid/core/timeline/shot_composition_projection.py`. The renderer is Composition 0.0.6 (`remotion/package.json:18` on main).

## 1. Popup closure: occurrences A (8 s) and B (10 s) on a shared lane

### Closure

Two occurrences of different shot revisions on one lane (`video`):

| Occurrence | Shot revision | Placement | Occurrence duration | Child duration (overhang) |
|---|---|---|---|---|
| occ-1 (A) | shot-alpha rev-a | at 0 s | 8 s | 10 s |
| occ-3 (B) | shot-alpha rev-b | at 8 s | 10 s | 12 s |

Each child overhangs its occurrence by 2 s, which is the case the clamp exists for. Without the clamp, A's child would run into B's window.

### Main's visible result (the reference)

`shot_composition_projection.py:308-326` (`_project_clip`) computes the visible window as `[occurrence start + child at, min(child end, occurrence end))`. It then shortens the child's `hold` or `to` to match. Visible result on main:

| Clip | Visible window | Frames at 30 fps |
|---|---|---|
| A child | [0 s, 8 s) | [0, 240) |
| B child | [8 s, 18 s) | [240, 540) |

The windows are half-open. Neither clip overlaps the other on the lane. The test checks both windows and the no-overlap property.

### Decision applied: the clamp is ON, with one compiled result

- `clampToOccurrenceDuration` in App is not a per-call choice. The 03:46 decision says App uses ONE compiled result for both the local candidate and the accepted projection. Main's clamp is the reference.
- App currently passes `clampToOccurrenceDuration: false` at `ShotTimelinePreview.tsx:99` and `shotTimelineDataProvider.ts:404`, so the overhang stays visible. That diverges from main. App must stop passing the option, not flip the global default just to pass a unit test.
- App's own clamp replica at `src/tools/video-editor/data/shotCompositionProjection.ts:437-449` should go as well, so that App reads the compiled window. App's test at `shotCompositionProjection.test.ts:420` expects the unclamped `hold: 5` for the local candidate; that expectation is App's to change. The raw AuthoringBundle and editor source windows stay as they are.

### Occurrence speed (visual)

Main does not inherit occurrence speed for visuals either (`shot_composition_projection.py:305-307, :354`). Occurrence speed is metadata only, the same rule as audio. The child keeps its own speed.

## 2. Element clips get the clip look (intended change from 0.0.6)

This is a deliberate difference, not lost behaviour (03:59 decision).

- **Main (Composition 0.0.6).** Effect clips are dispatched straight to the effect component and skip the wrapper. `docs/reference/timeline-composition-v0.0.6/TimelineComposition.tsx:121-132` returns `<EffectComponent/>` directly. Media clips go through `VisualClip`, which applies the fade (`VisualClip.tsx:57`, `lib/fade.ts:27-`).
- **Composition 0.0.7** (`6bd784d`, "clip look (opacity, crop, fades, entrance/exit) on element clips"). `TimelineComposition.tsx:81` in `v0.0.7` wraps effect clips in `<ClipLook kind="element">`. `ClipLook.tsx:40-48` applies opacity and crop to element clips only. Media clips get no opacity or crop from ClipLook, because `VisualClip` already handles their fade. But `ClipLook` wraps media clips too (`TimelineComposition.tsx:99,104,119`), so entrance and exit animations apply to media clips as well. Full list of 0.0.7 differences: `design/owner-film-differences.md`.
- **Consequence.** Overlapping independent element clips with fades now DIP where main drew them opaque. The 16-30 DIP golden is approved as intended. Viewing lists the owner's films with overlapping element clips that use fades, opacity or entrance/exit (03:59 condition 3).
- **This tree.** `remotion/package.json:18` pins `file:artifacts/banodoco-timeline-composition-0.0.8.tgz` on the integration tree, so the intended change is already in the pin. `test_render_pin_gives_element_clips_the_clip_look` asserts the pin is at least 0.0.7.

### Proof still owed (not in this contract)

03:59 condition 1: a MAIN replay built from tag `v0.0.6` (git archive reproduces main's locked sha512) compared against the unified result, with real pixels rather than SSR markup. Only the intended clip-look differences may appear. That proof belongs to Viewing. This document does not claim it.

Also in the same 0.0.7 release, per-boundary transitions (dissolve vs dip) changed. The vectors here do not cover that.

## Vectors

| id | Expected | Status |
|---|---|---|
| popup-occurrence-a-start-frame | 0 | pass |
| popup-occurrence-a-end-frame | 240 | pass |
| popup-occurrence-a-duration-frames | 240 | pass |
| popup-occurrence-b-start-frame | 240 | pass |
| popup-occurrence-b-end-frame | 540 | pass |
| popup-occurrence-b-duration-frames | 300 | pass |
| `test_popup_closure_occurrences_are_half_open_on_the_shared_lane` | A's end <= B's start | pass |
| `test_render_pin_gives_element_clips_the_clip_look` | pin >= 0.0.7 | pass |

These are not xfails. The clip look is already in this tree, and the popup clamp is main's current behaviour.

### Render-facing rows (the 6 rows the compiler must emit)

The clock is the rational `fps_rational: [30, 1]` (main's encoding is the `[num, den]` pair, read as `Fraction(*fps_rational)` at `astrid/packs/rendering/actions/timeline_visualize/filmstrip_cards.py:466`). Frames are half-open: `start = round(at * fps)`, `duration = max(1, round(visible_seconds * fps))`, `end = start + duration`, with `round` = JavaScript `Math.round` (`astrid/core/timeline/duration.py:145-156` on main). The six rows are start, end and duration frames for each occurrence:

| Row | Clip | Field | Frames |
|---|---|---|---|
| 1 | A (occ-1, shot-alpha rev-a) | start_frame | 0 |
| 2 | A | end_frame | 240 |
| 3 | A | duration_frames | 240 |
| 4 | B (occ-3, shot-alpha rev-b) | start_frame | 240 |
| 5 | B | end_frame | 540 |
| 6 | B | duration_frames | 300 |

Rows 1-6 are produced by the compiler as it stands. Measured on this branch: `test_compile_contracts.py` passes all six with the rational clock. No strict xfail is needed, because no row is missing from the compiler's output.

The 03:46 premise that main's numeric helpers return NaN on a rational object did not reproduce. `clip_start_frame` and `clip_end_frame` (`duration.py:145-168`) take a Real. A `Fraction` gives the right frames (240 and 540). A `{num, den}` dict or a `[num, den]` list raises `ValueError: fps must be a number` at `_positive_fps` (`duration.py:45-49`). The compiler therefore takes the rational as a `Fraction` built from the pair, and the fixture keeps the pair. Main has no `{num, den}` object: its wire form is the two-element `fps_rational` list.

## Not verified

- The popup closure is the one specified in the 03:46 decision. Its exact placement and child timings are my reconstruction, and the 03:46 decision asks Viewing to confirm the reference against main's frames. This worktree has no rendered frames.
- No frames were rendered and no pixels were compared.
- App's tests were not run here.
