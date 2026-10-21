# M2 generic marker reference resolver: current-source gap

## Result

No product source or test change is made in this worker. The requested
resolver cannot be implemented against the current Agent tree without
inventing the very `MarkerRef` and authored marker-set carrier that PLAN4.3
requires the foundation to consume. The predecessor frontier's finding is
confirmed: generic marker identity is the smallest missing seam, but its
input carrier is not present yet.

This is an expected source gap, not a decision to broaden the task. The
worker therefore leaves transcript/word anchors, legacy beat playback, and
the current timing refusal unchanged.

## Main authority and exact findings

The current Main timing boundary is:

* `astrid/core/timeline/moments.py:42-79` — `Moment` has `word`, `beat`,
  `downbeat`, `cut`, `cut_end`, `end`, and `cut_start`; `Context` exposes only
  `words()`, ordinal `beats(kind)`, cut lookup, own-cut lookup, and line
  in-point. There is no `MarkerRef`, marker-set type, marker-table protocol,
  or marker resolver.
* `astrid/core/timeline/moments.py:215-254` — `resolve()` resolves ordinal
  beats from `Context.beats()` and text/cut moments. It has no stable marker-ID
  branch and no pinned-set identity check.
* `astrid/sdk/timeline/compiler.py:21-25` — the current pure compiler
  explicitly lists `beats/markers` as refused inputs; `TimingInputs` at
  `:81-105` carries only the captured bundle, verified source rows, word
  bindings, and frame policy.
* `astrid/sdk/timeline/_timing_evaluators.py:232-255` — `moment_rule()` parses
  the existing Moment grammar, refuses `beat`/`downbeat` with
  `needs a captured marker resolver`, and proceeds only through exact word
  bindings or cut dependencies.
* `astrid/sdk/timeline/model.py:1117-1140` — the mutable checkout helper
  supplies `Context.beats()` by reading numeric beat arrays and projecting
  them through a music clip's source offset/speed. This is the existing
  legacy playback helper, not a pinned generic marker resolver.

The only authored marker-like carrier is the legacy beat grid:

* `astrid/core/timeline/astrid_ns.py:15-20` and
  `astrid/sdk/timeline_intent.py:39-42` recognize `app.astrid.beats` and
  `beats_label` as ordinary intent fields.
* `astrid/sdk/timeline_intent.py:136-170` reads numeric `beats`,
  `downbeats`/`bars`, and optional hit rows, and writes a dict through
  `set_beats()`. Numeric rows have no stable opaque marker ID; `source` is a
  display/lineage label, not a set or publication identity/version.
* `tests/sdk/test_timeline_checkout.py:318-320,748-782` and
  `tests/sdk/test_timeline_adopt.py:28-30,55-60` establish this carrier's
  current playback/adoption behavior. They do not establish stable marker
  identity or pinned publication semantics.

The unrelated App fixture field
`haus.astrid.scene-phase-markers` is not an Agent timeline marker-set
carrier: it is opaque App data, has no `MarkerRef` binding or timing helper,
and must remain opaque under the current namespace-preservation rules.

## Frozen R4 authority and why it is not a carrier

The frozen R4 donor confirms the shape of the pure seam but does not supply
the requested identity contract:

* R4 `astrid/core/timeline/moments.py:48-55,79-83,317-328` resolves only
  ordinal `beat`/`downbeat` values through `Context.beats()`.
* R4 `astrid/sdk/timeline/compiler.py:119-168` records dependencies for
  cut/clip/word/beat edges, but its beat path is tied to those ordinal beat
  arrays and music owners.
* R4 `astrid/sdk/timeline/commands.py:1485-1488` records `beat:<index>`;
  that index is not a stable marker identity and cannot be used as a
  `MarkerRef` substitute.

The approved design is explicit about this boundary:

* `extensions.md:157-165` permits only a pure
  `resolve_marker(ref, pinned_marker_table, occurrence/time_map)` seam and
  says missing markers return unavailable without mutation.
* `extensions.md:167-182` labels `MarkerSetPublication` and `MarkerRef` as a
  future M5 data-model proposal, including exact set/publication identity,
  stable marker IDs, coordinate domain, occurrence identity, and follow/fixed
  provenance. It is not an existing current carrier.
* `extensions.md:184-203` requires canonical typed serialization, rational
  coordinates, exact occurrence/time-map projection, half-open range checks,
  and refusal for ambiguity/out-of-range inputs.
* `port-manifest.md:433-441` describes these as dormant extension seams and
  forbids publication/republication, registration, or M5 machinery before the
  hard stop.

## Minimal contract/source gap for the next worker

The smallest safe follow-up must first land or otherwise expose an existing
authored, pinned carrier containing (without IO or mutable-head lookup):

1. exact marker-set identity (project, publishing namespace, logical set ID,
   and source lineage);
2. exact immutable publication identity/version and its input/content
   identity;
3. stable opaque marker ID, rational coordinate, declared coordinate domain,
   and presence (missing is distinct from null/zero where the carrier permits
   those values);
4. the exact placement/occurrence identity and any explicit time-map
   identity required to project source-domain coordinates; and
5. a `MarkerRef` binding that names the selected publication and preserves
   follow/fixed provenance, rather than a display label or ordinal.

Once that carrier exists, the bounded implementation target is one pure
helper at the existing `moments.py`/compiler boundary:

```text
resolve_marker(ref, pinned_marker_table, occurrence/time_map)
    -> resolved rational moment + dependency identities | unavailable
```

It must use the existing `TimingCompileError`/atomic projection boundary and
must refuse, visibly and without mutation, for an absent or foreign set pin,
mismatched publication/version, missing marker ID, ambiguous placement, or an
out-of-range point. It must not search by label/text, choose the latest
publication, ordinal-rebind, clamp to an edge, or mutate opaque authored data.
Existing word bindings and legacy numeric beat arrays remain unchanged.

## Required compact witnesses after the carrier exists

The current tree cannot honestly add the requested positive stable-marker test.
The next source task should add a small pure test neighbor to
`tests/sdk/test_timing_compiler.py` (or the carrier's existing pure timing
test) covering:

* exact stable marker ID + matching set/publication pin resolves to the exact
  rational moment and dependency identity, including one source-domain
  occurrence/time-map projection;
* absent marker ID, foreign set, mismatched version, ambiguous placement, and
  out-of-range point each refuse visibly and leave the captured inputs/bundle
  byte-for-byte unchanged;
* no guessed text, latest publication, ordinal fallback, or opaque mutation;
* current word-anchor tests remain unchanged and continue to prove exact
  transcript identity and no text search (`tests/editing_conformance/test_native_word_anchor.py:406-431`).

No detector, beat-snap, signal, publication/republication service, registry
operation, DTO, store, endpoint, provider, registration, UI, or M5 example is
part of this gap report.

## Verification

No product files were modified. The first direct system-Python attempt could
not start because that interpreter has no `pytest`. The preinstalled shared
Agent venv was then used read-only, with the shared Runtime package supplied
on `PYTHONPATH` (no dependency or cache changes):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timing_compiler.py \
  tests/editing_conformance/test_timing_retained_inputs.py \
  tests/editing_conformance/test_native_word_anchor.py
```

Result: **41 passed, 62 deselected in 0.98s**. No full, native, HTTP,
render, browser, install, or test-service suite was requested.
