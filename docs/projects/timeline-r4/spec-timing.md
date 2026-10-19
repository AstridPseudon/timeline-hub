# spec-timing.md: the timing compiler workstream (time references, the compiler, sequence identity, cuts)

**Workstream:** TIME · **Brief:** [briefs/WS-TIME.md](briefs/WS-TIME.md)

**Part of** [spec.md](spec.md) (the glossary is there). **Release promises served:** 3 (edits keep their meaning), 5 (stable cuts and story structure) and 8 (motion), in [release-contract.md](release-contract.md). **Rulings:** F4 (the timing compiler + dependency graph + typed evaluators), F6 (stable cuts first), F10 (story and motion in Phase C). Code paths are at trunk f840ec1c, re-pinned by SPEC-0.

## 1. Time references and the one lookup
- **One lookup, three result kinds:**
```python
lookup(tl, text: str, *, expect: Literal["address", "selection", "timeref"]) -> Address | Selection | TimeRef
```
  - **Address** → exactly one thing, else refused. The forms: `c08`, `c08.app`, `n21`, `"Building" in v27 #2`, `@93.5`, an asset key.
  - **Selection** → zero or more things (`chapter=02 role=label`; `parse_selector`, `sdk/timeline/selection.py:40`).
  - **TimeRef** → one instant (`"viral"`, `after "Astrid"`, `"tool" in v20a #2`, `beat 2 after "Astrid"`, `c22`, `end of c30`, `end`, plus offsets `+9f`/`-0.5s`; a bare offset is relative to the clip's own cut start).
- **The grammars stay** `core/timeline/moments.py` (parser :83-141) and `sdk/timeline_address.py` (resolve :70). The lookup is one front over them, so error messages and "did you mean" are shared.
- **Ambiguity is refused** and lists every candidate (e.g. `"viral" is spoken 2 times: say "viral" in n21 or "viral" in n33`).
- **Every view and every change description prints the resolved time beside a TimeRef:** `on "viral" +9f · 12.37 s`.

## 2. The timing representation (KEPT as stored today; additive keys only, written only behind COMPAT-1 capability checks)
No relation-store migration (F4). **All keys live under `app.astrid`** (A1; dual read of the old flat keys).

MUSIC-SEGMENTS retains the current authored bed, normalized unsnapped ripple basis, scoped owner and derived output IDs in `parent.config.app.astrid.music_beds`, behind the existing single integer compatibility checks. See [the adopted carrier/lifecycle contract](amendments/20261015-music-authored-bed-carrier.md). Lazy enrollment occurs only on a real managed keep-end edit; unchanged legacy reads/resolves/renders do not enroll. Generated segments remain ordinary materialized clip output, never timing input for an enrolled source.


| Timing fact | Stored as | Status |
|---|---|---|
| a clip's start tied to a time reference | `on: "<TimeRef>"` | exists |
| its end tied to a time reference / a literal length | `until: "<TimeRef>"` / `for: <seconds>` (setting one clears the other) | exists |
| a param tied to a spatial mark (ƒ(MARK)) | `formulas: {"params.x": {"mark","axis","offset","unit":"canvas"}}` | exists |
| sequence steps laid out as one unit | `sequence`, `sequence_index` on each step; `sequence_fit` (`{land, lead, race, cycle, then}`) on the first step | exists |
| the film's end | `until` on the last picture, written by `film_end` (`reflow.py:461`) | exists |
| the music bed's policy at length changes | **new:** `music: "keep_end" \| "plays_on"` on the bed clip (default `keep_end`; today it is a per-edit keyword, `model.py:828`) | additive |
| a clip follows another clip | **new:** `link: {"to": "<scoped id or uid>", "alias": "c31.book3", "edge": "start\|end", "offset": "+2f"}` | additive (CAT P2-V23) |
| ducking under narration | `duck: {"under": "voice", "by": "-10dB", "attack": "6f", "release": "12f"}` on the bed (stored by `tag()`, `model.py:490`, **never applied today**) | applied by the audio evaluator (§4) |
| an explicit "fixed" pin | **new:** `pinned: true`: the compiler keeps the clip's literal `at`/`hold` | additive |
| z-order relative to another clip | `stack` stays a command that writes `track` + `clip_order` (no stored relation) | unchanged (MATRIX R-9: the renderer still ignores `clip_order`) |

**Absolute timing where no relation is authored.** Today's rules (`retime`, `sdk/timeline/reflow.py:349-447`) become the documented defaults:
- a non-picture, non-audio clip in a cut, with no `on`, **starts with its cut**;
- a clip with no cut and no `on` (for example most audio) **keeps its literal start**;
- the end is `until`, else `for`, else (for visual clips in a cut) the cut's end; **the last cut runs to its picture's end**;
- an orphan (its word is gone) keeps its time and length until it is re-homed.

## 3. The timing compiler (tasks M1a → M1b → M1c; DECISIONS-deep-dives-1 "Timing")

**Delivered in three steps:**
- **M1a, characterization (xhard, Release 1):** lock today's behaviour as tests before touching it. The list is in §3.7.
- **M1b, extraction (xhard, Release 1):** the contract below.
- **M1c, intentional repairs (normal, Release 2):** named follow-ons, each a deliberate behaviour change with its own scenario (§3.8).

### 3.1 Contract
```python
def prepare_timing(base: AcceptedTimingSnapshot, candidate: dict, commands: list[EditCommand],
                   media: FrozenMediaInfo) -> TimingInputs                              # pure normalization, in the commit path
def compile_timing(inputs: TimingInputs) -> TimingResult                                 # the ONLY materializer
# TimingInputs is immutable. It carries the base revision and digest, the direct writes, the narration-piece order and the old
# boundary locations, the explicit ripple policy and exclusions, the sequence weight basis, authored music source and its current ripple basis
# (materialized segments are output/ownership data only for enrolled beds), grid revisions, and the last accepted values for unresolved references.
# Why: two edits with an equal total delta but different ripple locations give different music seams, and those seams
# can't be rebuilt from the film's end plus its beats. Recompiling an accepted document has no new transition, and must
# never infer a ripple from its own compiled values.
@dataclass(frozen=True)
class TimingResult:
    bundle: dict                              # compiled fields written: at/hold/from/to, placement duration_ms, envelopes
    graph: DependencyGraph                    # nodes and edges actually used (for affected intervals and cycle checks)
    times: Mapping[str, ResolvedTime]         # "<id>.<path>" → {seconds, frame, text}
    conflicts: tuple[Finding, ...]            # §5
    digest: str
```
- **The only writer of compiled timing.** "All timing changes use the timing compiler. Adapters may convert units, but must not independently retime content."
- **Today's functions become its evaluators,** not rewrites: `reflow` :149 (the narration layout), `retime` :349 (cuts and clips), `_relay_steps`/`_fit_sequences` :717 (sequences), `film_end` :461, `_sync_film_length`, `music_edit.plan_keep_end`, `moments.resolve` :215.
- `Checkout.resolve()`, `retime()` and `reflow()` keep their public signatures and call it.
- **Quantisation is unchanged:**
  - moments floor to the frame (`moments.floor_frame`: `floor(s·fps + 0.02)/fps`);
  - frame spans use JS rounding (`core/timeline/duration.py:52`).
- **Idempotent:** `compile(compile(d).bundle).bundle == compile(d).bundle`.
- **Runs** at the end of every transaction and at checkout.

### 3.2 The dependency graph (it replaces the fixed order)
**Nodes added by the ruling:**
- `cut:<id>.terminalExtent`: a terminal picture's own literal duration is a root, so `cut.end` of the last cut no longer depends on the film's end;
- `film.pictureEnd` (the editorial extent), separate from `composition.extent` (the render extent; `duration.py:174-270`);
- `music:<bed>.segments`, which takes the ripple locations and the source beats as inputs;
- `beat-source:<asset>:<n>`, immutable and evaluated before music editing;
- `beat-placed:<bed>:<segment>:<n>`, evaluated after it.

These nodes resolve the cut/film and music feedback cycles. A keep-end segment that feeds a placed beat, which feeds the final picture's end, is **rejected, naming the path**. Each output has a single owner, so a second writer is `MULTIPLE_WRITERS`.

**Nodes** are computed properties:
- `line:<id>.start/end` (the narration layout: the previous line's end + `gap_after_s`; the take's length);
- `word:<line>:<n>.start/end`;
- `beat:<bed>:<n>`;
- `cut:<id>.start/end`;
- `clip:<id>.start/end`;
- `group:<sequence>` (a fitted sequence's layout);
- `film.end`;
- `bed:<id>.seams` (keep-end cuts);
- `envelope:<bed>` (duck);
- `param:<clip>.<path>` (mark formulas).

**Edges** come from the stored facts in §2:

| Edge | From |
|---|---|
| `clip.start ← <TimeRef target node>` | `on` |
| `clip.end ← <until target>` \| `clip.start` (+`for`) \| `cut.end` (default) | the end rules |
| `cut.start ← picture clip's on target` | the cut index (§6) |
| `cut.end ← next cut.start` \| `picture.end` (the last cut) | the cut order |
| `group ← cut span, land word` | `sequence_fit` |
| `clip.start/end ← group` | the sequence steps |
| `clip.start ← linked clip edge` | `link` |
| `film.end ← max(end of plate / full-frame pictures)` | today's `_sync_film_length` |
| `bed.seams ← authored source, current ripple locations, source beats` | `music: keep_end`; materialized segments are output only for enrolled beds |
| `envelope ← words` | `duck` |
| `param ← mark` | `formulas` |

**Evaluation:**
- in **topological order** over the graph actually present (Kahn's algorithm with a stable tie-break by node id);
- `film.end` has no edge back into the pictures it is computed from, so it is acyclic by construction.

**This fixes the review's backward-dependency cases:**
- a link to a fitted-sequence step waits for the fit;
- the film's end follows its pictures, not the reverse.

**Cycles are rejected over the complete graph at command time.** A `set`/`move`/`add` whose new edges would close a cycle is refused (`CYCLE`, naming the loop). A cycle is never discovered at render time.

### 3.3 Direct writes vs computed consequences
- A command declares the paths it writes directly. The compiler returns everything else that changed as `consequences` (with `because`: the edge that caused it).
- **Scope and effects guards check direct writes only** (spec-save §3).
- **The affected intervals** (spec-rendering §2) are computed from direct writes ∪ consequences, using the graph.

### 3.4 Pins ("fixed"): written only behind COMPAT-1's capability check; M1c makes a pin a frozen film-coordinate interval, not raw `at`/`hold`
- `pinned: true` keeps a clip's literal `at`/`hold` through every compile. Its graph node has no incoming edges.
- **A pinned clip that conflicts with a dependent rule** (for example it now lies outside its cut, or a sequence fit needs it) is reported (§5), never silently moved.
- `set intent.pinned=true` / `timeline.detach` produce pins. Pins are taught as "for things that must not follow the story".

### 3.5 Performance
- **Measure first:** a full compile of the v8 duplicate, p50/p95 over 20 runs.
- **Target:** p95 ≤ 150 ms. A miss is a decision request (Q15): incremental compile over the affected subgraph vs caching. Don't build incremental compile unasked.

### 3.6 The clock contract (one timeline coordinate, with named conversions)
- **The conversions:** frame ↔ seconds ↔ occurrence-local ↔ clip-local ↔ source. They are conversions, not independent clocks. The App's leaf timing uses seconds (4-decimal rounding), occurrences use ms, and render placement uses frames.
- **Rounding:** keep the named legacy policies (moments floor; SDK `round`; the compositor rounds start and duration separately). **Do not unify them on integer frames.**
- **Speed:** `hold` is a source duration converted through speed (`duration.py:113-142`). Wrappers run outside the speed remap. Combined clip × occurrence speed is explicit.
- **Trims:** a left-edge trim is one atomic transform: `start' = start + δ`, `from' = from + δ·r`, `sourceDuration' = sourceDuration − δ·r`. Translation, source trim and stretch are separate operations. Tests cover speeds 0.5, 1 and 2.
- **Keyframes have a declared origin.** App host keys are in timeline seconds (linear/hold); donor sprite keys are in clip-local frames (held poses). Adapters exist for both.

### 3.7 M1a: behaviours to lock (characterization tests, before any change)
- the reference grammar (words, phrases, occurrences, beat before/after, cut-relative offsets, contextual `end`);
- **the first-word picture exception:** a picture on a line's first word, with no offset, resolves to the take's origin (`moments.py:229-233`, `model.py:1008-1015`);
- the beat "on" tolerance of half a frame;
- the distinct quantizers;
- narration word coordinates are clip-relative and not divided by speed;
- **unanchored SFX movement:** a ripple moves eligible unanchored content, and an already-playing non-music SFX finishes unchanged (`reflow.py:904-919, 1049-1051, 1099-1114`);
- **narration-piece splitting** on opening and closing time (`reflow.py:103-125, 904-938, 1023-1083`);
- gap ownership and the precedence of `gap_after_s`;
- the trimmed-media `until` rule;
- **music seam placement:** the preceding downbeat, else the beat, else the edit point; a 250 ms crossfade; explicit silence when short (`music_edit.py:67-182`);
- ripple-location clustering;
- the music override is temporary and restored;
- the film-length sync uses the last shot only;
- proportional allocation;
- the 60 ms tail on insert;
- split audio.

### 3.8 M1c: intentional repairs (named follow-ons)
- reject the music/film feedback cycle explicitly;
- reject self-cycles, importing a terminal `until="end"` as a compatibility basis;
- strict ambiguity: no rewriting existing references to the nearest occurrence (`reflow.py:539-586`);
- **word identity across takes** (TIMING-FIXES): a word TimeRef binds to that spoken word, never to its ordinal. IDs are stable within one transcript, not automatically across takes. A same-lineage correction preserves identity only with a validated one-to-one match. A take swap requires an explicit old-qualified-ID to new-qualified-ID map with provenance; diff may propose only unambiguous matches. Ambiguity refuses or requires explicit mapping. Unmatched references remain `ORPHAN`, never rebound by ordinal or nearest time. After a validated mapping, rewrite any existing displayed `#n` spelling and list that change; `#n` is not the identity rule. Preserve the existing v9 m11 case (“live-code both front-end **and** back-end features, **and** share”) keeping c14 on “and share” and c15 on “And the LLMs”; preserve all v9/v11 criteria.
- stable sequence-member identity (shared with U1);
- trimmed-media end and trim/speed corrections;
- a pin is a frozen film-coordinate interval;
- explicit bed-scoped beat references with deterministic overlap ownership;
- an explicit source-timed transcript binding for speed-aware narration edits.

The source record is `media.transcript/v1`, subject to actual producer-schema admission; `voiceover_script` remains authoring intent. Preserve the existing hash-bound managed-input declaration at `config.app.transcript`; its canonical media-association/default index is `config.app.transcript.references`. Each occurrence's authoritative immutable reference is `clip.app.transcript.binding`, which freezes the exact document revision, immutable snapshot and digest, media/source identity and clock, segment/word IDs, and occurrence identity while reusing existing trim/speed/placement. Changing the default association does not retarget a bound clip without an explicit rebind command in the same transaction. The compiler validates the pinned snapshot and derives word seconds through existing conversion functions. Missing or mismatched snapshots refuse; replay never consults latest. `app.astrid.words` is transitional or compiler-derived cache only; only the compiler writes derived timing caches, keyed by snapshot/media/clock, trim/speed, occurrence placement, and compiler version. See [the Astra098 contract](amendments/20261016-upstream-transcript-extension-integration.md) for correction, undo, and source-write retry boundaries.

### 3.9 Sequence identity (part of M1b, with U1)
- **The problem today:** a refit rebuilds every step from step 0's template with index ids (`reflow.py:717-780`), so another hand's edit to a step is lost.
- **The fix:**
  - stable authored step ids;
  - semantic output ports `sequence.land` and `sequence.end`;
  - generated members materialized from the layout result;
  - a missing referenced step is a conflict, never rebound by ordinal;
  - legacy terminal sequences with `until="end"` still fit.
- **Acceptance:** another hand's step edit survives a narration refit.

## 4. Typed evaluators (plugged into the same graph)
| Evaluator | Representation | Node | Output |
|---|---|---|---|
| **spatial** | `formulas` mark entries | `param:<clip>.<path>` | the param value (canvas px → stored units via `units.from_canvas`) |
| **audio envelope** | `duck` on the bed | `envelope:<bed>` | volume keyframes on the bed, derived from word spans (attack/release in frames). **Today's audio is base volume + fades only** (the composition's `AudioTrack.tsx:43-77` reads no envelope). The envelope is global and derived from the narration spans: where speech overlaps, the strongest attenuation wins, multiplied with base volume and fades, and projected onto every generated segment. **V-3 builds a real consumer first, with sample-level envelope tests and rendered audio across seams.** It renders only if the composition supports volume envelopes (CAT P2-R7); otherwise V-3 adds that through K3, and until then `duck` reports `DUCK_UNRENDERED` (never faked) |
| **stacking** | `track` + `clip_order` (literal) | — | unchanged (a command, not a relation) |

## 5. Conflicts (reported, never silently resolved)
| Code | When | Behaviour |
|---|---|---|
| `CYCLE` | a new edge would close a cycle | **refused at command time** |
| `ORPHAN` | a TimeRef's target is gone (a deleted word or clip) | keeps the last compiled value; sets `app.astrid.orphan` (as today, `reflow.py:624`); a finding with fix commands (re-tie to the nearest word / pin) |
| `NEGATIVE` | an end compiles to ≤ its start | clamped to 1 frame; **blocking** |
| `OUTSIDE` / `LENGTH` | a clip outside its cut or shot | as today's checks |
| `DUCK_UNRENDERED` | duck without renderer support | a warning |

## 6. Cuts (M4, Release 1: stable cuts first)
### 6.1 One derived cut index (it must keep picture GAPS, OVERLAPS and SEQUENCE RANGES that span cuts)
Two algorithms disagree today: the SDK's plate groups (`lookup.py:288-319`) and `picture_cuts()` with gaps (`cuts.py:125-174`). The one index preserves gaps and overlaps. A sequence may span cuts: c17's sequence runs until c19 across c18, so its end is `c19.start`. **Acceptance:** the c17/c18/c19 case agrees across every consumer. Cut ids are **never reused**: today `_next_cut_id` (`edits.py:115`) checks only present entities, so add reservation/tombstones (U1).

- **One function** derives the cut list. It is today's `picture_cuts` (`core/timeline/cuts.py:139`):
  - one cut per picture-bed clip;
  - consecutive bed clips sharing `app.sequence` form one cut;
  - the id is the picture's `app.astrid.cut`.
- **Every consumer reads it.** Today the consumers are:
  - `sdk/timeline/check.py:321`, `sdk/timeline/lookup.py:75`, `sdk/timeline_cuts.py:246`;
  - `packs/timeline/cli.py:1581,1641`, `packs/timeline/{cli_sweep,cli_log,cli_music}.py`;
  - `packs/editorial/executors/pacing/model.py:325`;
  - the visualize modules (`sweep.py:51`, `filmstrip_cards.py:747`, `motion/{window,sheet,diffview}.py`);
  - `core/timeline/music_edit.py`, `sdk/timeline_adopt.py`, `sdk/timeline_views.py`.

  All of these are re-pinned after the port's T4.
- **The cut index is cached per content digest.**

### 6.2 Stable identity and addressing
**Repairs** (the evidence: OPUS §8.2, L7-01, H-6, Round 1 #10):
- **`tl.cut("c31")` resolves whenever `c31.*` resolves,** including carried layers (`c30.cover` answers to `c29.cover`) and orphaned cuts;
- **ordinals** (`cut 17`) are display-only and map through the index (`sdk/timeline_address.py:626`); commands store ids;
- **a sheet split keeps every existing layer's id** (H-6);
- **new ids** come from `_next_cut_id` (`sdk/timeline/edits.py:139`: `c07` → `c07a`) and are never reused.

### 6.3 Split, lift, delete: the documented semantics
| Command | Effect |
|---|---|
| `split c07 at=<TimeRef>` | a new cut `c07a` opening at the TimeRef. Its picture is a copy of c07's picture, trimmed. Layers stay with the cut they overlap at their start. The film's length does not change (H-1). |
| `lift c24 [--layers stay\|remove]` | c24's picture is removed and the previous cut's picture holds over its span. Layers either stay (re-homed to the previous cut) or are removed. Chapters starting at c24 move to the previous cut's start (until Phase C ranges). |
| `remove c24.plate` (a picture clip) | **refused:** "lift the cut (`lift c24`), or set its asset" |
| `remove n22` (a line) | the narrated ripple delete: the words, the gap and the line go and the film shortens. A cut that opened on those words follows `--visuals remove` (lifted) or `orphan` (it keeps its place, flagged). No silent 10 orphans (Round 1 #10). |

### 6.4 The demonstration test (it decides CUT-REC)

> **14 Oct:** CUT-REC (the conditional stored cut record) is dropped from the plan; this test's result is recorded as a note, and a cut record would be a new decision.
- **In Phase B, M4 writes one scenario per candidate workflow** that would need a cut to exist without its picture:
  - "lift the picture but keep the cut for a replacement later";
  - "an empty cut as a placeholder while generating footage";
  - "swap pictures between cuts when one side is empty".
- **If any of them is a real need** (it appears in TICKETS or the user asks for it), task **CUT-REC** (Phase C, conditional) builds the **smallest persistent cut record**:
  - `parent.config.app.astrid.cuts: [{id, on, why}]`, used only for cuts whose picture is missing;
  - reader capability checks: an older Astrid refuses to edit a film whose `app.astrid.v` is greater than it understands;
  - a lossless, idempotent migration.
- **Otherwise CUT-REC is closed as "not needed",** with the evidence recorded.

### 6.4 CUTS current-source demonstration result (2026-10-15)

F-CUTS-implementation-001 demonstrated the three candidate workflows on synthetic
admitted-source inputs in `tests/timeline/test_cut_index.py::test_cut_record_demonstrations`:
replacement later, a footage-generation placeholder, and swapping an asset with
an empty picture slot. An existing picture slot with its asset cleared retains
its stable cut id; replacing/swapping that asset works. An actually missing
picture is also addressable through surviving orphan members. A lift merges the
cut into its predecessor; it does not promise an independent empty cut after all
members are removed. These are distinct behaviors, not a claim that a stored
empty-cut record exists. No cut record was added and this synthetic result does
not establish a new human workflow need for CUT-REC.

The final focused delivery cohort passed **51/51** checks, including the
parameterized demonstrations, c17/c18/c19 spanning intersections, picture gaps
and overlaps, cut-free sound, actual sheet-split uid preservation across all
three harness paths, orphan addressing, lift, picture-remove refusal, and the
narrated `visuals=remove|orphan` choice. Plain `make parity-guard` passed **12/12**.
Evidence: `projects/F/evidence/F-CUTS-001/delivery.{json,log,xml}` and
`parity-exact.{json,log}`. The note is supported by these actual results.

This is current-source implementation evidence only. Existing harness journal,
reservation/undo and other admitted-parent failures remain visible in the
handback; it does **not** establish that every old addressing/remove harness
assertion passes. Named v8/v9/v11, film duplicates and film cut-free audio proofs
remain held where unavailable. No historical equivalence, card or release
acceptance is claimed.


## 7. Chapters and story structure
- **Release 1:** chapter selection keeps working (`chapter=06`, `show --chapter`). `lift`/`swap` update chapter starts explicitly, listed in the change description.
- **Release 2:** story ranges (M8) and motion timing (MO): [spec-later.md](spec-later.md).

## 9. Tests for this area
| Area | Tests |
|---|---|
| the compiler (M1) | the golden re-flow suites pass **unchanged** (`tests/sdk/test_timeline_reflow_golden.py`, `test_timeline_reflow_keep.py`, and the word-identity case `test_timeline_checkout.py::test_a_take_that_says_a_word_again_keeps_each_moment_on_the_word_it_meant`); `tests/editing_scenarios/timing/*` on every path; compiled output byte-identical on every fixture and on the v8 duplicate; idempotence; **dependency tests**: a link to a fitted step, a film end following its pictures, a gap retime moving only dependent clips; `CYCLE` refused at command time; each conflict code; pins; the bench |
| typed evaluators | a mark formula moves with its mark; the duck envelope follows a re-flow (`runs review` loudness dip ±1 dB under narration, once rendering exists); stacking unchanged |
| cuts (M4) | `tl.cut(x)` ≡ `c x.*` resolution; the H-6 sheet split keeps ids; the split/lift/remove semantics table; every consumer gives identical output before and after on `tiny` and the v8 duplicate; the demonstration scenarios |
| story (M8) | chapter start frames identical after the range migration; ranges follow `move n20a --before n17`; `swap` does not move chapters |
