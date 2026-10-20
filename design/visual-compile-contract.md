# Visual compile contract

Status: contract draft for the Agent compiler, from the 2026-10-20 03:46 orchestrator decision (popup projection consistency), the 03:59 decision (clip look) and the 04:44 correction (exact native fixture). Golden vectors: `tests/editing_conformance/fixtures/visual_compile_contract.json`, run by `tests/editing_conformance/test_compile_contracts.py`.

Reference for "visible today": `origin/main` e51595c6. The compiler is `astrid/core/timeline/shot_composition_projection.py`, identical to main's file in this tree. The renderer is Composition 0.0.6 (`remotion/package.json:18` on main).

## 1. Popup closure: the native ADD fixture

The closure is the output of App's native `occurrence.add-media` on occurrence A, not a reconstruction. Source: App commit `309cb7a463833126e3af730fb3c6ff536d9e457c`, `src/tools/video-editor/commands/fixtures/recipe_m2_occurrence_media.json` (blob `22be20593b2b53dd35d1b0b71031f3cf128bf32e`), key `add.output`. The fixture stores that object verbatim as `native_add_output`.

### Closure

Two occurrences on the shared `picture` lane, both 10 s long:

| Occurrence | Shot (pinned revision) | Placement | Occurrence duration | Source window child (`clip-a`) |
|---|---|---|---|---|
| occ-a (A) | `shot-placement-17545…` (`authoring-shot-revision-e0bb…`, which adds `reserved-child`) | at 8 s (`placement.start_ms` 8000) | 10 s (`duration_ms` 10000) | at 1, hold 4, from 2, to 6, speed 2 |
| occ-b (B) | `chapter-shot` (`shot-1`) | at 10 s (`placement.start_ms` 10000) | 10 s (`duration_ms` 10000) | at 1, hold 4, from 2, to 6, speed 2 |

Other fields that the projection carries through:

- Each source window child has a timeline length of `hold / speed` = 4 / 2 = 2 s (`duration.py:113-142`). Its absolute window is therefore 9-11 s in A and 11-13 s in B.
- Each occurrence also has `clip-b` (at 5, hold 2, so 2 s). A's `clip-b` is 13-15 s, B's is 15-17 s.
- A has `reserved-child` (at 0.125, hold 4, from 2, to 6, speed 2, so 8.125-10.125 s). Its `opaque` is `[null, false, {}]` and its `params` is `null`. The projection keeps both.
- The parent's own `clip-a` and `clip-b` (on the same lane, at 1 and 5, not occurrence-owned) are excluded from the rows. They carry no `shot_occurrence_id`.
- Occurrence `speed` is 1 and `source_offset` is 0 on both occurrences.

### What main does with this closure

- The projection is `project_runtime_parent_composition`, which calls the same `_project_clip` as the reference. The visible window is `[occurrence start + child at, min(child end, occurrence end))` (`shot_composition_projection.py:308-313`).
- **The overhang clamp is not exercised by this closure.** No child extends past its occurrence end. Largest child ends: A 15 s against an end of 18 s; B 17 s against an end of 20 s. With the clamp on or off, the rows are the same. The 03:46 premise, that A's child runs into B without the clamp, came from the reconstruction and does not reproduce on the native fixture.
- **Occurrence spans overlap.** A spans 8-18 s and B spans 10-20 s, an 8 s overlap on the lane. Main accepts this and does not reject it. The source-window children do not overlap: A's child ends at 11 s, where B's begins. Whether overlapping occurrence spans on one lane are intended is an open item for the orchestrator (section "Open").
- The clamp decision itself is not settled by this fixture. The 03:46 "clamp is ON" decision in this document is a policy statement, not evidence from this closure. App's `clampToOccurrenceDuration: false` (`ShotTimelinePreview.tsx:99`, `shotTimelineDataProvider.ts:404`) makes no difference to these rows.

### Rational clock

The native fps is `{"numerator": 30000, "denominator": 1001}` (NTSC, 29.97). Main's frame helpers take a Real. `Fraction(30000, 1001)` gives the right frames. Passing the `{numerator, denominator}` object, or the two-element `fps_rational` list, to `clip_start_frame` or `clip_end_frame` raises `ValueError: fps must be a number` at `_positive_fps` (`duration.py:45-49`). The test builds `Fraction(numerator, denominator)` from the fixture's `fps` and keeps the pair in the fixture. No frame is computed from a dict or list.

Frames are half-open, with JavaScript `Math.round` semantics (`duration.py:145-171`): `start = round(at * fps)`, `duration = max(1, round(visible_seconds * fps))`, `end = start + duration`.

### Physical reference (not produced here)

The physical reference is the approved executable analog (04:40 decision, Viewing's inbox): tiny generated playable media with the exact durations, explicitly labelled as an analog of the native fixture, plus the real host dispatch. MAIN is fed its own numeric fps, `Fraction(30000, 1001)`, and its frames are the reference. This worktree generated no media and rendered no frames. The reference belongs to Viewing, and it is valid only after MAIN's rational path and managed bytes are supplied. The rows below are the compiler's expectation for that reference.

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

The six render-facing rows are the source-window child of each occurrence. Each row is a frame value from the projected clip (`shot_occurrence_id` plus `app.astrid_shot_composition.source_clip_id` = `clip-a`).

| id | Occurrence / child | Field | Expect | Status |
|---|---|---|---|---|
| popup-occurrence-a-start-frame | occ-a / clip-a (9 s) | start_frame | 270 | pass |
| popup-occurrence-a-end-frame | occ-a / clip-a (11 s) | end_frame | 330 | pass |
| popup-occurrence-a-duration-frames | occ-a / clip-a | duration_frames | 60 | pass |
| popup-occurrence-b-start-frame | occ-b / clip-a (11 s) | start_frame | 330 | pass |
| popup-occurrence-b-end-frame | occ-b / clip-a (13 s) | end_frame | 390 | pass |
| popup-occurrence-b-duration-frames | occ-b / clip-a | duration_frames | 60 | pass |
| `test_closure_places_occurrences_at_eight_and_ten_seconds_on_the_picture_lane` | occ-a at 8 s, occ-b at 10 s, both 10 s | placement | as stated | pass |
| `test_popup_closure_source_windows_are_half_open_on_the_shared_lane` | A's child end <= B's child start | order | 330 <= 330 | pass |
| `test_native_child_keeps_its_opaque_and_null_params_fields` | occ-a / reserved-child | `opaque`, `params` | `[null, false, {}]`, `null` | pass |
| `test_render_pin_gives_element_clips_the_clip_look` | pin >= 0.0.7 | pin | >= 0.0.7 | pass |

These are not xfails. Every row the compiler must emit is produced on this branch, and the clip look is already in this tree.

Measured on this branch with `/home/user/work/venv-agent/bin/python -m pytest`: 22 passed, 2 xfailed (the two audio vectors 10-11). No visual row needs an xfail.

## Open

1. **Clamp decision.** This native closure does not exercise the clamp. The "clamp ON" policy stays as the 03:46 decision says, but it needs another closure to be evidence. Orchestrator call.
2. **Overlapping occurrence spans on the picture lane.** A (8-18 s) and B (10-20 s) overlap by 8 s. Main accepts it, and the source-window children do not overlap. Orchestrator to confirm this is intended for a shared lane.
3. **Physical reference.** Viewing produces it (analog, MAIN at `Fraction(30000, 1001)`) and checks these six rows against it. Not done here.

## Not verified

- No media was generated, no frames were rendered and no pixels were compared. The vectors test the compiler's output fields only.
- App's tests were not run from this worktree. App's own clamp replica (`src/tools/video-editor/data/shotCompositionProjection.ts:437-449`) and its `clampToOccurrenceDuration: false` callers were not changed here.
