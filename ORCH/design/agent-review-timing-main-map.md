# Review: timing main-map kernel

Status: **approved as a bounded inactive kernel slice**.

Reviewed `tl/agt-m2-timing-main-map-kernel` at `5dc90c42` against its
`cf7448ed` parent. This review does not activate the compiler, add a public
pin/schema, or change a product writer.

## Findings

- Main provenance is real: `_timeline_clip` maps `from_ms`/`to_ms` to the
  corresponding source-second fields only when those fields are absent. The
  kernel admits that alias-only shape and converts with `_timing_number(...) /
  1000`, retaining exact rational boundaries. If both codecs are present, it
  refuses rather than silently selecting one; this is a deliberate pending
  adapter boundary, not a claim that mixed-codec precedence is supported.
- Evaluation runs on a private copy. Raw `from_ms`/`to_ms`, transcript pins,
  and opaque authored data remain unchanged. Raw `source_window` is refused at
  the tested clip, occurrence, placement, timeline, and registry-asset
  scopes; no opaque map schema is inferred.
- Occurrence placement `start_ms`/`duration_ms`, non-default occurrence
  `source_offset`/`speed`, and the existing audio-vs-picture timing branches
  are unchanged. No renderer, DSP, Composition, or copied projection logic
  was added.
- `_timing_number` remains the existing `timeline.units._time_fraction`
  facade. Stable-word source cropping and half-open boundaries remain exact:
  a word ending at source-out is accepted, while an onset at source-out or an
  end beyond source-out is refused.
- Default activation is held. The only product definition/use of
  `compile_timing` remains the opt-in compiler module; no provider or command
  path calls it.

## Capture boundary

Existing `clip.move`, `clip.trim`, `clip.set`, `clip.split`, and occurrence
media capture paths still refuse clip `from_ms`/`to_ms` (and mapped source
fields where applicable). The retained-input `first_selection` helper is a
test-only adapter, not command replay proof.

There is no native recorded WordBinding capture adapter yet. Before that future
adapter consumes these aliases, it must inspect the actual authored clip,
guard mixed/invalid endpoint codecs, preserve the raw source fields in the
command/revision contract, and bind stable IDs against the exact source
window. Likewise, any future trim writer that elects to support the aliases
must replace its current refusal with an explicit adapter and replay tests;
the current trim refusal is correct for this slice.

## Evidence

Run from a private archive of `5dc90c42` with the shared Agent venv (read-only):

- `pytest ... tests/sdk/test_timing_compiler.py tests/sdk/test_timing_cycles.py tests/sdk/test_timeline_checkout_facade.py` — **74 passed**.
- `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime pytest -m integration tests/editing_conformance/test_timing_retained_inputs.py` — **9 passed**.
- `pytest tests/editing_conformance/test_compile_contracts.py -rxX` — **27 passed, 2 unchanged xfailed**. The xfails are the prepared-envelope `fade-in` and `fade-out` audio vectors.
- Ruff on the touched Python files — **passed**.

No full suite, `make check`, renderer/audio parity, or command replay proof
was run or claimed. Recommended next step: retain activation held until the
native word-binding adapter and remaining millisecond placement/duration
adapters have their own guarded command/replay coverage.
