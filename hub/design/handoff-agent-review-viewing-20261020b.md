# Agent review of Viewing's M3/M4 proposals (2026-10-20, second pass)

Reviewer: Agent domain. Base `tl/agt-visual-contract-correct`. Three items: audio vector reconciliation, the corrected mouth proposal, and the owner scanner package. No product code was changed.

## 1. Audio vectors: reconciled, unit settled

Full table and evidence are in `design/audio-compile-contract.md` ("Reconciliation with Viewing's authored 11"). Summary:

| Viewing # | Our vector | Result |
|---|---|---|
| 1 unity gain, child .8 | 15 `gain-unity-keeps-child-volume` (added) | same rule |
| 2 absent volume, gain .5 | 3 | same |
| 3 mute | 6 | same |
| 4 .8 x .5 | 1 | same |
| 5 1.5 x 2 | 2 | same |
| 6 source_offset **350** | 7 | **differed**: ours was .35. Fixed to 350 |
| 7 occurrence speed 1.5 | 8 | same |
| 8, 9 hold / trim cap | none | Viewing-only projection caps; not audio policy, not duplicated |
| 10 combined fades .1/.1 on .05..0.55 | 10, 11 | differs (separate .5 fades from 0); both stay strict xfail |
| 11 opaque `effects` shape | none | Viewing-only; nothing for the compiler to pin |

**Unit: occurrence `source_offset` is milliseconds; 350 is canonical.** Runtime `runtime_protocol/visual_seam.py:291-294` divides it by 1000 (alias `source_offset_ms`); App `shotCompositionProjection.ts:361` (`sourceOffsetMs / 1000`) fed by `shotCompositionAdapter.ts:245-246`; Agent `shot_composition_migration.py:779` uses the legacy name `source_offset_ms`; Agent `shot_composition_projection.py:353` passes the value through verbatim. Nothing reads it as seconds. Our .35 was a seconds reading. The compiler result is the same (metadata only), so no rescaling anywhere: the fixture now carries Viewing's literal 350.

Also adopted from Viewing's proposal after checking `composition/typescript/src/lib/trim.ts`: `source_from` is `computeMediaTrim(clip, fps).trimBefore / fps` (frame-rounded), not raw `from`; `playback_rate` is `getSanitizedPlaybackRate(speed)`. The curve question was already closed (honoured).

Not adopted: Viewing's proposal wording that App's four RED requirements are "ordinary RED". That is App/orchestrator scope.

Test: `tests/editing_conformance/test_compile_contracts.py` via the central service: 23 passed, 2 xfailed (the two strict `ENVELOPE_UNRENDERED` vectors), 2s.

## 2. Mouth proposal (`preserve-known`): APPROVE

Checked against base `751dd75e2` (patch applies there; it does not apply to this tree, which has no `astrid_motion` motion.ts, so applying it is a separate step).

- **Shared actual erase geometry**: `mouthInspectionRect(raw)` is `mouthEraseRect(mouthAnchor(raw))` padded, and `scene.ts` keeps the same `presenterAt` view and `pixelGeometry` transform. No second geometry formula.
- **Legacy-sized padding**: erase rect is `x-1..x+w+1, y-1..y+3`. Padding 1 px horizontally and 2 vertically gives `x-2..x+w+2, y-3..y+5`, which equals the legacy `mouth_box` (`timeline_visualize/motion/model.py:541-548`: `x-2, y-3, x+w+2, y+5`). For the explicit `151/104/19` anchor this is the `(298,202,345,219)` crop the proposal cites.
- **Default / partial / raw-invalid stay known**: the rect uses `mouthAnchor` normalisation (`anchorOr` clamps and defaults), so those inputs keep a known normalised region. The earlier narrowing to unknown is gone.
- **Mosaic unknown**: unchanged branch in `scene.ts`.
- **No new public type or API**: one new exported helper in the element's own `motion.ts`; the scene return shape is unchanged.
- **No threshold widening, pixel verification not replaced**: the plan keeps the `>2%` decision, copies-only planted controls and the private crop/fallback until a separate qualification.

Conditions (not blockers):
1. The legacy default differs from the component default for partial anchors (legacy `w` 16, component 19; legacy has no clamp). The proposal already calls those inputs unqualified for equivalence. Keep that wording; do not let a consumer claim equivalence for them.
2. The `element.yaml` comment is long; trim it when applying.
3. Applying changes the public `diagnostics.mouth` rect, so the geometry expectations in the existing SSR/scene tests must be updated in the same change, as the proposal's test plan says. Those tests must not become refusals or xfails.

## 3. Owner scanner package (`owner-film-viewing-tools-v1.tgz`, sha256 fc9d90a4...): ACCEPT WITH REQUIRED CHANGES

Archive checked in memory (python `-I`, tarfile read only, nothing extracted or run): sha256 matches; 11 regular members; scanner, test and README are byte-identical to the flat handoff copies. I read the scanner source; I did not execute it or its tests.

What holds:
- **Read-only on film data**: the input is read once with `read_text`; `--input` must be a regular, non-symlink file; output is rejected if it is the input, a symlink or a hardlink, re-checked after the temp file is written; the write is a temp file in the output directory then `os.replace`. The only write outside the output file is `mkdir` of its parent directory.
- **No network or media**: no socket/http/database imports in the scanner. The Agent registry load uses `include_missing_roots=False` and `default_sources()` is empty, so it does not create directories (`registry.py:215-218,268-277`). Run with `-B` as documented.
- **Rational fps**: `output.fps` goes through `capture.rate`, giving `Fraction(30000, 1001)`, reported as `[30000, 1001]`. Frame helpers then take the float quotient, which is how `duration.py:_positive_fps` treats every caller. The list form `[n, d]` raises, so the scan reports `incomplete` (fail closed).
- **Uses the canonical projector** (`project_runtime_parent_composition`) and `clip_fields.describe` / `audio_curves.validate` rather than guessing by suffix.
- **Fail closed**: missing closure keys or projection failure give `status: incomplete`; `clean_claim` is always false.

Required changes before the owner uses it as the hard-stop list:
1. **`curve_honoured` must list only fades that carry a non-linear `curve=`.** Today every audio fade (with or without a curve) gets a `curve_honoured` finding (`known = audio_known and curve_known`), so the "films that use `curve=`" list in `owner-film-differences.md` section 1 would contain every film with a fade. Emit it only when `params.fadeInCurve` / `fadeOutCurve` is present and not `linear`. `continuous_audio_fade` keeps covering all fades.
2. **`element_clip_look_overlap` is over- and under-selective.** It pairs every two registered element clips that overlap on the same track, even when neither carries a look property, and it never pairs across tracks. The approved difference (`visual-compile-contract.md` section 2) is: element clips now get opacity, crop, fades and entrance/exit, and independent fades on overlapping element clips dip. Pair overlapping element clips on any track, and only when at least one has a look property. Also report single element clips that carry a look property, because those change even without overlap.
3. **Look property set is incomplete.** `_LOOK_NAMES` lacks `crop_*`, and element `speed` != 1 (v0.0.7 remaps element time; `owner-film-differences.md` section 2 item 3). Add both, and media `entrance`/`exit` (item 2) as a separate known-property listing, or state below that they are not covered.
4. **Transitions are not covered at all, and the report must say so.** Canonical `clip.transition` is INCOMING (ratified 23:06 on 2026-10-19), the Agent compiler converts it to the compiled outgoing form, and per-boundary dissolve/dip planning changed in 0.0.7 (`owner-film-differences.md` section 2 item 4). The scanner never reads `transition`. Minimum: add a `not_covered` list to the output and README (transitions, element speed, media entrance/exit, as applicable) so an empty result cannot read as "no transition differences". Preferred: add a `transition_boundary` inventory of canonical incoming declarations with clip id, transition id/type, interval and source path. This tree's projector does not convert transitions yet (`shot_composition_projection.py` has no transition code), so the scanner cannot compute converted boundaries; an inventory is all it can honestly give today.
5. **Source paths are partly in projected-config space.** `config.tracks[i].role` and `registry.assets[...]` name the projected document, not the owner's input file, so the owner cannot open them. Prefix them as `projected.` or map them to the closure input. Also `internal_indexes` indexes the de-duplicated dict rather than the input list, which gives a wrong `internal_timeline_revisions[i]` if a revision id repeats; enumerate the input list instead.

Not verified: the scanner's own 10 tests and a run on a synthetic closure (not executed, per the instruction to run nothing from the archive); Agent import side effects beyond the registry (pack discovery reads, no network seen); behaviour on a real owner closure (none exists in reach).
