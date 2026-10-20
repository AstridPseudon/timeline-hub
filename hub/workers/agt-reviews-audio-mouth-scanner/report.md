All three reviews are done. Only the audio fixture and design doc changed; the test file was not edited. The scanner got a read-through but I did not run it or its tests.

## 1. Audio
- **Unit:** occurrence `source_offset` is milliseconds, so Viewing's 350 is canonical and our 0.35 was wrong.
  - Runtime `runtime_protocol/visual_seam.py:291-294` divides it by 1000.
  - App `shotCompositionProjection.ts:361` converts `sourceOffsetMs / 1000`, fed by `shotCompositionAdapter.ts:245-246`.
  - Agent `shot_composition_migration.py:779` uses the legacy name `source_offset_ms`.
  - Agent `shot_composition_projection.py:353` passes the value through unchanged, so the compiler result is the same either way. Nothing was rescaled.
- **Reconciliation:** all 11 original vectors are in a table in `design/audio-compile-contract.md`.
  - Vectors 2–5 and 7 are the same rule as ours; vector 6 differed only in the offset value.
  - I added one vector (`gain-unity-keeps-child-volume`) because Viewing's unity-gain row had no counterpart.
  - Viewing's hold-cap, trim-cap and opaque-`effects` rows have no counterpart in our fixture; they are projection or shape cases, so I did not duplicate them.
  - Viewing's combined-fade row differs from our two separate fade vectors, which stay strict xfail.
- **Clock correction:** I also adopted Viewing's correction to the envelope clock. `source_from` is `computeMediaTrim(clip, fps).trimBefore / fps`, which is frame-rounded and checked against composition `lib/trim.ts`.
- **Test:** `tests/editing_conformance/test_compile_contracts.py` through the central service gave 23 passed, 2 xfailed (the two `ENVELOPE_UNRENDERED` vectors), exit 0.

## 2. Mouth proposal: APPROVE
- **Base:** the patch applies at `751dd75e2`, not to this tree, which has no `astrid_motion`.
- **Geometry and padding:** the new rectangle is the actual erase rectangle padded by 1 pixel horizontally and 2 vertically. That equals the legacy `mouth_box` (`x-2, y-3, x+w+2, y+5`, `timeline_visualize/motion/model.py:541-548`).
- **Known/unknown:** default, partial and raw-invalid anchors stay known through `mouthAnchor`, and mosaic stays unknown.
- **API and verification:** there is no new public type, no threshold widening, and the pixel verification stays.
- **Conditions when it is applied:**
  - The legacy default width is 16 and the component's is 19, so partial anchors stay unqualified for equivalence.
  - The `element.yaml` comment is long and should be trimmed.
  - Existing SSR/scene geometry expectations must be updated in the same change.

## 3. Owner scanner: ACCEPT WITH REQUIRED CHANGES
- **What holds:**
  - The sha256 matches and the files match the flat copies. I read the archive in memory only and ran nothing from it.
  - It reads film data read-only and has no network or database code.
  - Output is checked against input aliases, symlinks and hardlinks, and the write is atomic.
  - Rational fps is handled (30000/1001), and failures return `incomplete`.
- **Required changes:**
  1. `curve_honoured` fires for every audio fade, so it would list every film with a fade. It should fire only when the curve is present and not `linear`.
  2. `element_clip_look_overlap` pairs clips only within one track, and even pairs clips with no look property. It should pair across tracks, require a look property on at least one clip, and also report single clips that carry one.
  3. The look property set lacks `crop_*` and element `speed`.
  4. It never reads `transition`, so an empty result could be taken as "no transition differences". At minimum add a `not_covered` list; better, add a transition inventory. This tree's projector does not yet convert incoming transitions, so an inventory is all it can give.
  5. Some source paths point into the projected config, which the owner cannot open. Also `internal_indexes` indexes a de-duplicated dict, so it gives the wrong index if a revision id repeats.
- **Unverified:** I did not run the scanner or its 10 tests, and no real owner closure was available.

The full review is in `design/agent-review-viewing-20261020b.md`. I wrote the commit message to the commit-msg path and created `DONE`; nothing was merged or pushed.
