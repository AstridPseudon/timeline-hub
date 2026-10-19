# spec-rendering.md: the rendering workstream (capture, parity, one evaluator, coverage, the change view, pins)

**Workstream:** RENDER · **Brief:** [briefs/WS-RENDER.md](briefs/WS-RENDER.md)

**Part of** [spec.md](spec.md). **Release promises served:** 6 (truthful seeing), 8 (motion renders) and 10 (schema/composition contracts), in [release-contract.md](release-contract.md). **Rulings:** F5 (three distinct concepts), the X1P experiment, F10 (motion in Phase C). Code paths are at trunk f840ec1c; **SPEC-0 re-pins them**, because the port's T4 reconciled our visualization with Codex's rework.

## 1. Three concepts, never conflated

| Concept | What it is | Truth level | Used by |
|---|---|---|---|
| **rendered frame** | pixels from the composition evaluator (`@banodoco/timeline-composition`, through Remotion) | **the truth** for render and preview | render, preview (after P6), the change view's images, parity tests |
| **coverage model** | metadata about what covers the canvas at a frame: `core/timeline/onscreen.py` `visible_at` (:356) and `coverage` (:406), using element `metadata.coverage/bounds/motion` | an **approximation**: every answer carries `certainty: measured \| declared \| estimated` | checks (GAP, EMPTY, DIP), lint, `tl.at(t).visible()`, the film-length picture test |
| **affected intervals** | time spans that may have changed, computed **conservatively** from a change description's direct writes, its computed consequences and the dependency graph (spec-timing §3.3) | structural (may over-include, never under-include for supported edits) | choosing which frames the change view shows |

**The rules:**
- Preview and render share the composition evaluator.
- Checks use the coverage model and label approximations.
- **Sampling chooses which frames to show. It never proves that unsampled content did not change.**
- An audio change gets audio review.

## 2. Affected intervals (R-SEE): a conservative dependency contract (unknown → included)

> **14 Oct:** = the frames whose scene plans differ between two revisions, plus timing consequences; unknown dependencies are included.
```
AffectedInterval {start, end (half-open, rational seconds), video: bool, audio: bool, entityIds, propertyPaths, causes,
                  certainty: "exact" | "conservative", unknownDependencies: [...]}
```
**The rules (over-reporting is acceptable; under-reporting is a bug):**
- **Traverse the union of the before and after dependency graphs** (timing + render). Include old and new draw spans; a transition extends visibility (`transition-spans.ts:74-86`).
- **Include neighbours** when adjacency or transition ownership changes.
- **Global changes expand:**
  - track opacity, scale or order → its descendants;
  - theme, font or a global effect → all their consumers;
  - an asset replacement → every consumer of that asset;
  - audio edits affect video through audio analysis, and visual clips with embedded media affect audio.
- **An unknown extension dependency widens the scope;** no scope at all means the whole output.
- **A pure time shift is still a change.**
- **The change view never prunes intervals by coverage.** The frame budget chooses which evidence to show, not what changed.
- **"Past its end"** (a draft longer than the published film) is reported, never a failure (Round 1 #1).

**Acceptance:** on exhaustive synthetic fixtures (a deletion, an asset replacement, a track reorder or opacity change, a theme/font change, a long transition, an audio-driven visual, a dependency removal), every changed frame and sample lies inside the reported intervals. The donor sweep's `frame_signature` (it ignores audio) is never the authority.

## 3. The change view (R-SEE)
- **One "see" step** over an EditResult or a journal span: `timelines edit … --verify`, `timelines see TL [--since SEQ] [--lens pairs|motion]`, `tl.see(result)`.
- **It replaces** `edit --verify`, `check --at`, `check --sweep`, `visualize --compare published`, T1-20 and X-41 (the old names become aliases).
- **Frames:** before/after **rendered frames** chosen within the affected intervals (event-centred: the edges, the edited TimeRef instants, transition points).
  - **Budget:** 64 per view (`sdk/timeline/frames.py:31`).
  - **Skipped intervals are listed, never silently dropped.**
- **Audio review** for intervals with `audio: true`: a before/after loudness trace, a waveform strip, a playable clip.
- **Captures** use the path CAP-G proved (admitted actions; no bypass of Runtime custody).
- **Targets** (single-client and under 3 agents): a single edit p50 ≤ 5 s warm; a whole-film change ≤ 60 s.

## 4. The coverage model (R-SEE): qualified evidence, never pixel truth

> **14 Oct:** coverage is answered from the scene plan (explicit unknown), not a separate model with per-property provenance.
- **One coverage API.** Each answer carries **per-property provenance**:
  - `bounds` (`measured | declared | estimated | unknown`);
  - `opacity`;
  - `opaqueCoverage` (`mask | region | unknown`);
  - `role`, `evaluationIdentity`, `frame`, `componentRevision`.
- **Fix the unsound opacity summing.** Today `onscreen.py:375-378` treats summed opacity ≥ 0.999 as covered, so two 0.5 layers count as covered; they really composite to 0.75. Report `unknown` when opaque coverage isn't established. The DOM `BoundsProbe` (`remotion/src/BoundsProbe.tsx:37-64`) measures bounds, not opaque pixels.
- **The invariant is "no unexplained regressions",** not "no verdict changes". Demonstrated false verdicts are corrected, with before/after fixtures.
- **Fixtures:** two half-opacity plates, transparent sprite holes, crop/mask, stale bounds, source-only tracks, a transition extension.
- **The duplicate copies are retired** (or kept only as labelled `estimated` fallbacks):
  - `FULL_FRAME` (`sdk/timeline/reflow.py:91`);
  - `OPAQUE_KINDS`/`hidden_under` (`fast_lane.py:515-519`);
  - the sweep signature (`sweep.py:100`);
  - `boxes_at` (`motion/model.py:633`).
- **Re-pin all of them after the port's T4.**

## 5. Preview/render parity (R-PARITY) and one evaluator (R-EVAL = P6 stages A+B; R-FULL = stage D)

> **14 Oct:** parity = P and R consume the same plan (plan equality) + event-centred pixel/audio spot checks; the 4-surface × 18-row-family harness is not built. The conformance fixtures move to Release 1 (CONFORM).
**The capture surfaces** (compare each separately; never substitute a headless `TimelineRenderer` for the Player):

| Surface | What |
|---|---|
| **P** | the ACTUAL App Player, after seek and readiness |
| **R** | a full, unwindowed composition capture at the authored dimensions |
| **F** | the fast-lane capture of the same frames (it drops audio clips: `fast_lane.py:137-143`) |
| **E** | the encoded render (timestamps, audio, duration, decode) |

- **Primary comparisons:** P↔R and F↔R. E is compared separately.
- **Every capture records its provenance:** input digests, asset/font/component digests, renderer identity, fps, canvas, the requested vs the observed frame, readiness.

**The harness (R-PARITY).**
- **The surfaces** above, with readiness and audio capture.
- **Event-centred sampling:**
  - clip `[s,e)`: s−1, s, s+1, the midpoint, e−2, e−1, e;
  - transitions/fades `[a,b]`: a−1, a, a+1, the quarter points, the midpoint, b−1, b, b+1;
  - keyframes and steps: k−1, k, k+1;
  - short synthetic fixtures: every frame;
  - the film: cut−1, cut, cut+1 at all 45 boundaries, plus motion extrema and TimeRef instants.
- **Thresholds:**
  - **a semantic gate (exact):** frame count, fps, canvas, active clip ids, draw intervals, ordering, transition ownership, counter values; no missing, stale or placeholder frames;
  - **visual:** per-frame, per-channel MAE ≤ 2/255; each of the 16 4×4 regions ≤ 8/255; geometry within 1 authored px; never averaged across frames;
  - **audio:** synthetic PCM onset/offset within 1 sample and gain within 0.1 dB; playback/encoded markers within 1 frame and loudness within 0.5 dB, plus an audible review.

**The runs (R-PARITY).** The row families:
- T1 frame math (24/25/30/60/23.976/29.97 fps; half-frame starts; one-frame clips);
- T2 clock;
- V1 media;
- V2 element look;
- V3 fades and animations;
- V4 geometry and track scale;
- V5 stacking;
- X1 transitions;
- TXT text;
- M1 playback speed;
- M2 motion;
- A1 audio;
- A2 duck;
- SRC roles;
- EXT host capabilities;
- SEAM;
- WIN (the fast-lane window);
- FILM (a 20 s excerpt + all 45 cut boundaries + a full playback/audio review).

The deep dive's case 17 (all render routes) is part of these runs. **Unimplemented capabilities are reported as blocked, never "n/a".**

**P6: a hybrid migration ending in ONE composition evaluator.** The App keeps adapters for assets, readiness, the registry and editor overlays.

| Stage | Task | What |
|---|---|---|
| **A** (Release 1) | R-EVAL | The exact baseline (pin the source, generated registries, fonts, assets, Remotion, browser), plus the **pure evaluator interface** `prepare(document, closure, renderProfile) → EvaluationPlan; video(plan, frame); audio(plan, sampleInterval)`. It needs **public pure-module exports** from `@banodoco/timeline-composition`; today's export map exposes only the duration helper (K3). |
| **B** (Release 1, for the film's features) | R-EVAL | Shared visual/audio semantics in both hosts: output-role filtering, the canonical occurrence projection, component identities, source mapping, track composition (scale), transitions, wrappers, audio fades and envelopes. The App's composition assembly moves onto the shared evaluator. |
| **D** (Release 3) | R-FULL | The full matrix on P/R/F/E, including extensions and motion. Duplicate semantics are retired. |

**The rule:** every new capability (V-3 duck/transitions, MO motion, extensions) ships with three things: evaluator behaviour, a dependency declaration (for §2) and parity fixtures.

**Text/transform compatibility (part of R-EVAL).**
- **Existing films keep their look.** Today the package aliases `text` to `text-card`, whose unbounded branch applies `clip.opacity` itself, so the package's `ClipLook` applies it twice (0.5 → 0.25). The App scales whole tracks, while the package scales only media.
- **The fix:** separate plain-text and card identities, one transform order, and legacy documents adapted, with appearance fixtures.

## 6. Schema, composition, the effective renderer closure (R-PINS), and the capture gate (R-CAPTURE)
- **The effective renderer closure**, recorded by SPEC-0 and pinned by K3/P5: package bytes, generated registries and owners, fonts, the Remotion/browser versions, and the cache identity.
  - **The pins differ today:** the donor uses Remotion 4.0.503 with composition v0.0.7, while the union and App use 4.0.509 with v0.0.6.
  - **The generated effect registry differs** (the package has pack-owner dispatch). Don't blindly replace generated files.
  - **Acceptance:** changing only a component, package or font invalidates the relevant captures; warm and cold captures agree.
- **The capture integration gate (R-CAPTURE).** Before X1P, M6 and M7 build on either capture path, the union's admitted visualization/candidate render and the donor fast lane must be reconciled.
  - **Prove:**
    - admitted draft and revision frames;
    - requests that identify the frozen candidate, the frames, the renderer closure, bounds and budget;
    - **cancellation and native cleanup**, proven for real (the union's `native_cleanup="UNPROVED"`, `renderers/remotion/run.py:149,494`);
    - draft verification before and after the base stops being current (with a policy for each);
    - cold, warm and 3-agent latency.
  - **The union's `remotion_frame_owner.py`** is an unwired model with synthetic-only tests. Its revision diff captures no pixels.
- **K1:** `@banodoco/timeline-schema` 0.0.3 = 0.0.2 + `tracks[].role ∈ {output, source}` (default `output`) + a documented `app` owner convention (`astrid` reserved; `app` opaque).
  - Fork tag now; upstream PR.
  - Astrid's allow-lists are **generated** from it: `_CLIP_ALLOWED`, `_TRACK_ALLOWED`, `_TIMELINE_TOP_ALLOWED`, `_ASSET_ENTRY_ALLOWED` (`core/timeline/banodoco_schema.py:372-415`); the copies in `core/timeline/projection.py:128,261`; the `render_provenance_fields` set.
  - A staleness test.
  - Astrid-internal clip keys (`shot_id`, `shot_occurrence_id`, `shot_name`, `source_uuid`, `generation`, `pool_id`) are an explicit separate list.
- **K3:** composition v0.0.7 upstream (PR #2) with 0.0.3 accepted and **`role: source` tracks excluded** from render and duration.
  - This flips the S0 strict xfail `test_source_role_track_is_excluded_from_render`; remove it in the same commit.
  - Later releases carry the volume envelope (V-3, if needed) and modifiers (MO).
- **P5 (App):** pin the same tags; generate `TIMELINE_CLIP_FIELDS`, `TRACK_DEFINITION_FIELDS` and `ALLOWED_TOP_LEVEL_KEYS`.
- **P7 (App):** seams. Either share the TS, or keep `conformance/fixtures/canonical-timeline-parity.json` passing in Astrid, the Runtime and the App.
- **The clip-fields render table** (`core/timeline/clip_fields.yaml` `render:` per kind) is **checked against the render matrix** in `make check` (no built-in-to-wrapper rewrite; F9). A field's status says `works` only when its matrix cell does.

## 7. Transitions, duck, motion
Release 2 ([spec-later.md](spec-later.md): V-3, MO). Every new capability ships with evaluator behaviour + a dependency declaration + parity fixtures.

## 8. Tests for this area
| Area | Tests |
|---|---|
| affected intervals (M7) | one test per rule in §2; a gap retime marks every dependent clip's span; the past-end case; audio-only edits marked |
| the change view (M7) | budget respected; skipped intervals listed; the audio review produced for a volume change; the targets measured single-client and under 3-agent load |
| coverage (M6) | coverage/check suites unchanged; certainty present on every answer; the grep test (the copies are gone or are labelled fallbacks); the sweep plan still selects the same cuts on the v8 duplicate |
| parity (X1P, P6) | §5 |
| schema/composition (K1, K3, P5, P7) | §6; the render matrix re-measured for every compositor change |
| transitions/duck (V-3) | the R-7 cells pass; the duck loudness dip measured with `runs review`; remove scenarios on every path |
